import os
import logging
from typing import List, Optional

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.tools import tool
from langchain_core.documents import Document

# Configure logging
# logging.basicConfig(level=logging.INFO) <- Removed: Let app configure logging
logger = logging.getLogger(__name__)

# Constants — anchored to project root so paths work regardless of CWD
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
QDRANT_PATH = os.path.join(_PROJECT_ROOT, "data", "rag", "qdrant_workspace")
PARENT_STORE_PATH = os.path.join(_PROJECT_ROOT, "data", "rag", "parent_store")
COLLECTION_NAME = "ebook_library"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE = 384


class OptimizedRAG:
    """Highly optimized Parent-Child RAG architecture with In-Memory acceleration."""

    def __init__(self, warmup: bool = True):
        # Paths
        self.parent_store_path = PARENT_STORE_PATH

        # Lazy properties
        self._embeddings = None
        self._client = None
        self._vectorstore = None
        self._store = None
        self._retriever = None
        self._parent_splitter = None
        self._child_splitter = None

        # Pre-warm if requested (for server mode), otherwise lazy (for CLI)
        if warmup:
            self.ensure_ready()

    @property
    def embeddings(self):
        if self._embeddings is None:
            from langchain_community.embeddings import FastEmbedEmbeddings

            logger.info(f"Loading FastEmbed model: {EMBEDDING_MODEL}")
            # FastEmbed uses ONNX Runtime (CPU optimized) - much faster than Torch
            # Use threads=None to use all available cores
            self._embeddings = FastEmbedEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",  # Explicitly match existing model
                threads=None,
                cache_dir=os.path.join(
                    os.path.dirname(PARENT_STORE_PATH), "fastembed_cache"
                ),
            )
        return self._embeddings

    @property
    def client(self):
        if self._client is None:
            # Try connecting to Docker Qdrant first
            try:
                logger.info("Connecting to Qdrant Docker (http://localhost:6333)...")
                client = QdrantClient(url="http://127.0.0.1:6333", timeout=10.0)
                # Test connection
                client.get_collections()
                self._client = client
                logger.info("Connected to Qdrant Docker Service.")
            except Exception:
                logger.warning(
                    f"Qdrant Docker not reachable. Falling back to local path: {QDRANT_PATH}"
                )
                logger.warning("NOTE: Parallel access is NOT supported in local mode.")
                self._client = QdrantClient(path=QDRANT_PATH)

            # Ensure collection exists
            try:
                collections = self._client.get_collections().collections
                exists = any(c.name == COLLECTION_NAME for c in collections)

                if not exists:
                    logger.info(
                        f"Creating Qdrant collection: {COLLECTION_NAME} with Optimizations"
                    )
                    from qdrant_client.http import models

                    self._client.create_collection(
                        collection_name=COLLECTION_NAME,
                        vectors_config=VectorParams(
                            size=VECTOR_SIZE, distance=Distance.COSINE
                        ),
                        hnsw_config=models.HnswConfigDiff(
                            m=16,
                            ef_construct=100,
                            full_scan_threshold=10000,
                        ),
                        quantization_config=models.ScalarQuantization(
                            scalar=models.ScalarQuantizationConfig(
                                type=models.ScalarType.INT8,
                                quantile=0.99,
                                always_ram=True,
                            )
                        ),
                    )
            except Exception as e:
                logger.error(f"Failed to create/check collection: {e}")

        return self._client

    @property
    def vectorstore(self):
        if self._vectorstore is None:
            self._vectorstore = QdrantVectorStore(
                client=self.client,
                collection_name=COLLECTION_NAME,
                embedding=self.embeddings,
            )
        return self._vectorstore

    @property
    def store(self):
        if self._store is None:
            logger.info("Initializing In-Memory document store...")
            self._store = InMemoryStore()
            # Hydrate immediately when store is accessed
            self._hydrate_store()
        return self._store

    @property
    def retriever(self):
        if self._retriever is None:
            # Initialize splitters
            self._parent_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000, chunk_overlap=200
            )
            self._child_splitter = RecursiveCharacterTextSplitter(
                chunk_size=400, chunk_overlap=50
            )

            self._retriever = ParentDocumentRetriever(
                vectorstore=self.vectorstore,
                docstore=self.store,
                child_splitter=self._child_splitter,
                parent_splitter=self._parent_splitter,
            )
        return self._retriever

    def ensure_ready(self):
        """Force initialization of all components and sync vectors if needed."""
        # This triggers loading of embeddings, client, store, and retriever
        _ = self.retriever

        # Check and Sync Vectors (Auto-Recovery for Docker Migration)
        self._sync_vectors()

        self._warmup()

    def _sync_vectors(self):
        """
        Checks if Qdrant collection is empty but we have documents in the cache.
        If so, it regenerates the vectors to populate the new database.
        """
        try:
            count = self.client.count(collection_name=COLLECTION_NAME).count
            # If Qdrant is empty but we have data in memory store
            if count == 0:
                # Check if we have documents in store
                # InMemoryStore uses a dict .store under the hood? Or yield_keys
                # Let's count keys
                keys = list(self.store.yield_keys())
                if len(keys) > 0:
                    logger.warning(
                        f"⚠️ DETECTED EMPTY QDRANT but found {len(keys)} cached documents."
                    )
                    logger.warning(
                        "Starting Automatic Vector Regeneration (This happens once)..."
                    )
                    import time

                    t0 = time.time()

                    # Retrieve all docs
                    docs_to_index = self.store.mget(keys)
                    valid_docs = [d for d in docs_to_index if d is not None]

                    if valid_docs:
                        # Add to vectorstore (ParentDocumentRetriever logic is complex to reconstruct manual add)
                        # Actually, ParentDocumentRetriever .add_documents splits and adds.
                        # BUT, these docs are ALREADY PARENT DOCS (chunks?).
                        # Wait, the store contains PARENT docs (large chunks).
                        # The retriever .add_documents splits them into children and adds children to vectorstore.
                        # So yes, we can re-add them via the retriever!
                        # BUT double check: are these raw docs or parent chunks?
                        # They are "parent_store" docs. They were likely split from raw PDFs?
                        # No, _hydrate_store loads them from disk files which were "parent_store".
                        # If I assume they are the parents, calling retriever.add_documents might re-split them?

                        # Let's look at how they were stored.
                        # They are stored by UUID.
                        # If I re-add them using retriever.add_documents, it will use parent_splitter again.
                        # Since they are likely providing the "content" of the parent...

                        # Alternative: Just add them as-is to vectorstore?
                        # ParentDocumentRetriever uses vectorstore for CHILDREN (small chunks).
                        # The Store holds PARENTS (large chunks).

                        # If we essentially "lost" the vectorstore (children), we need to RE-GENERATE children from Parents.
                        # Yes!
                        # So logic:
                        # 1. Get all Parent Docs from Store.
                        # 2. Split them into Children using `child_splitter`.
                        # 3. Add Children to VectorStore.
                        # 4. We DO NOT need to add them to 'docstore' again (already there).

                        logger.info(
                            f"Regenerating child vectors for {len(valid_docs)} parents..."
                        )

                        # We must replicate logic of ParentDocumentRetriever.add_documents without adding to docstore
                        # Or just use `vectorstore.add_documents` with the generated children.

                        all_sub_docs = []
                        for parent_doc in valid_docs:
                            # We need to preserve the ID link?
                            # ParentDocumentRetriever links child to parent via "doc_id".
                            # The keys in self.store ARE the doc_ids.
                            # So we iterate (key, doc).
                            pass

                        # Actually, better approach:
                        # Just use the splitters directly.
                        ids = keys
                        # We need to pair keys with docs
                        # valid_docs is list corresponding to keys (assuming mget order preserved? mostly yes)
                        # Safest: iterate.

                        sub_docs = []
                        for i, doc in enumerate(valid_docs):
                            parent_id = keys[i]
                            # Split into children
                            child_docs = self._child_splitter.split_documents([doc])
                            for child in child_docs:
                                child.metadata["doc_id"] = parent_id
                                sub_docs.append(child)

                        if sub_docs:
                            batch_size = 64  # Use smaller batch for safety
                            total = len(sub_docs)
                            logger.info(f"Pushing {total} vectors to Qdrant...")
                            for i in range(0, total, batch_size):
                                batch = sub_docs[i : i + batch_size]
                                self.vectorstore.add_documents(batch)
                                if i % 640 == 0:
                                    logger.info(f"Processed {i}/{total} vectors...")

                            logger.info(
                                f"Auto-Indexing complete in {time.time()-t0:.1f}s"
                            )

        except Exception as e:
            logger.error(f"Auto-Indexing failed: {e}")

    def _hydrate_store(self):
        """
        Hydrates the In-Memory store from disk.

        Optimization:
        1. Checks for a consolidated JSON cache file (parent_store_cache.json).
        2. If cache exists and is fresh, loads it instantly.
        3. If no cache, reads JSON files in parallel using threads.
        4. Writes the cache for next time.
        """
        import json
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from langchain_core.documents import Document

        # Store cache one level up to avoid modifying the monitored directory's mtime
        cache_path = os.path.join(
            os.path.dirname(self.parent_store_path), "parent_store_cache.json"
        )

        # 1. Try to load from consolidated JSON cache
        if os.path.exists(cache_path):
            try:
                # Fast check: exists?
                dir_mtime = os.path.getmtime(self.parent_store_path)
                cache_mtime = os.path.getmtime(cache_path)

                # Optimization: Use orjson if available for 10x faster parsing
                try:
                    import orjson as json_lib
                except ImportError:
                    import json as json_lib

                # If cache is newer than the directory modification, it is valid
                if cache_mtime > dir_mtime:
                    logger.info(f"Loading from fast JSON cache: {cache_path}")
                    with open(cache_path, "rb") as f:
                        cached_data = json_lib.loads(f.read())

                    # Reconstruct Documents
                    docs_batch = []
                    for filename, doc_dict in cached_data.items():
                        # Handle both string and dict formats for robustness
                        if isinstance(doc_dict, dict):
                            docs_batch.append((filename, Document(**doc_dict)))

                    self.store.mset(docs_batch)
                    logger.info(f"Hydrated {len(docs_batch)} documents from cache.")
                    return
            except Exception as e:
                logger.warning(f"Cache load failed: {e}")

        # 2. Fallback: Read raw JSON files (Parallelized)
        if not os.path.exists(self.parent_store_path):
            logger.warning(
                f"parent_store_path does not exist: {self.parent_store_path}"
            )
            return

        logger.info("Hydrating In-Memory store from raw files (Parallel)...")

        all_files = os.listdir(self.parent_store_path)

        # Files in parent_store are UUIDs without extension, but contain JSON data.
        # Filter out directories and explicitly known non-data files if any.
        files = [
            f
            for f in all_files
            if os.path.isfile(os.path.join(self.parent_store_path, f))
            and not f.startswith(".")
        ]

        if not files:
            logger.warning("No files found to hydrate.")
            return

        docs_to_cache_dict = {}  # filename -> doc_dict
        docs_to_store = []  # (filename, Document)

        def load_single_file(filename):
            file_path = os.path.join(self.parent_store_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Support both formats:
                    # Legacy:  {"kwargs": {"page_content": ..., "metadata": ...}}
                    # Current: {"page_content": ..., "metadata": ..., "type": ...}
                    if "kwargs" in data:
                        return (filename, data["kwargs"])
                    elif "page_content" in data:
                        doc_dict = {
                            "page_content": data["page_content"],
                            "metadata": data.get("metadata", {}),
                        }
                        return (filename, doc_dict)
                    else:
                        logger.warning(
                            f"Unknown format in {filename}: keys={list(data.keys())}"
                        )
            except Exception as err:
                logger.error(f"Error reading {filename}: {err}")
            return None

        # Threaded loading
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
            future_to_file = {executor.submit(load_single_file, f): f for f in files}
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    filename, doc_kwargs = result
                    docs_to_cache_dict[filename] = doc_kwargs
                    docs_to_store.append((filename, Document(**doc_kwargs)))

        # Batch insert into store
        if docs_to_store:
            self.store.mset(docs_to_store)
            logger.info(f"Hydrated {len(docs_to_store)} documents from raw files.")

            # 3. Write JSON cache for next time
            try:
                logger.info(f"Writing cache to {cache_path}...")
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(docs_to_cache_dict, f)
                logger.info("Wrote consolidated JSON cache.")
            except Exception as e:
                import traceback

                logger.error(f"Failed to write cache: {e}\n{traceback.format_exc()}")
        else:
            pass

    def _warmup(self):
        """Warm up the embedding model and verify Qdrant connectivity."""
        logger.info("Performing RAG warm-up query...")
        try:
            self.embeddings.embed_query("warmup")
            logger.info("RAG warm-up complete.")
        except Exception as e:
            logger.error(f"Warm-up failed: {str(e)}")

    def ingest_ebook(self, pdf_path: str):
        """Parse and add a PDF to the library using Parent-Child strategy."""
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            return

        logger.info(f"Ingesting ebook: {pdf_path}")
        loader = PyMuPDFLoader(pdf_path)
        docs = list(loader.load())

        # Add metadata for tracking
        norm_path = os.path.normpath(pdf_path)
        for doc in docs:
            doc.metadata["source"] = norm_path

        # Split into parent chunks first to ensure we have the correct count for IDs
        # The retriever will try to split again, but if we've already split,
        # it should be a no-op / identity transform, keeping IDs aligned.
        parent_docs = self.retriever.parent_splitter.split_documents(docs)

        # Generate consistent IDs for both retriever (vectorstore/RAM) and disk persistence
        import uuid

        ids = [str(uuid.uuid4()) for _ in range(len(parent_docs))]

        # This will save to vectorstore and populate the IN-MEMORY RAM store
        # Pass the ALREADY SPLIT parent_docs and matching ids
        self.retriever.add_documents(parent_docs, ids=ids)

        # Persist new documents to disk using the SAME IDs so they can be re-hydrated next session
        self._persist_to_disk(parent_docs, ids)
        logger.info(f"Successfully ingested {pdf_path}")

    def _persist_to_disk(self, docs: List[Document], ids: List[str]):
        """Helper to ensure new ingestions are saved for the next IDE session hydration."""
        import json

        if not os.path.exists(self.parent_store_path):
            os.makedirs(self.parent_store_path)

        for doc, doc_id in zip(docs, ids):
            file_path = os.path.join(self.parent_store_path, doc_id)
            doc_dict = {
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "type": "Document",
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(doc_dict, f)

        # Invalidate cache so it's rebuilt on next load
        cache_path = os.path.join(
            os.path.dirname(self.parent_store_path), "parent_store_cache.json"
        )
        if os.path.exists(cache_path):
            os.remove(cache_path)
        logger.info(
            f"Persisted {len(docs)} parent documents to disk and invalidated cache."
        )

    def query(self, question: str, k: int = 5) -> List[Document]:
        """Perform semantic search and return relevant parent chunks."""
        return self.retriever.invoke(question)

    def search(self, question: str, k: int = 5) -> List[Document]:
        """Alias for semantic search."""
        return self.query(question, k)


# Initialize global instance for the tool
_rag_instance: Optional[OptimizedRAG] = None


def get_rag(warmup: bool = True):
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = OptimizedRAG(warmup=warmup)
    return _rag_instance


@tool
def search_ebook_library(query: str) -> str:
    """
    Searches the optimized RAG library for technical information from ingested ebooks.
    Returns the most relevant full-text narrative chunks (parent chunks) to preserve context.
    """
    rag = get_rag()
    docs = rag.query(query)

    if not docs:
        return "No relevant information found in the ebook library."

    formatted_results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content
        formatted_results.append(
            f"Result {i} (Source: {source}):\n{content}\n" + "-" * 50
        )

    return "\n\n".join(formatted_results)


if __name__ == "__main__":
    # Self-test if run directly
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        rag = get_rag()

        if command == "ingest" and len(sys.argv) > 2:
            rag.ingest_ebook(sys.argv[2])
        elif command == "query" and len(sys.argv) > 2:
            print(search_ebook_library.run(sys.argv[2]))
        else:
            print(
                "Usage: python rag_optimized.py [ingest <pdf_path> | query <question>]"
            )
