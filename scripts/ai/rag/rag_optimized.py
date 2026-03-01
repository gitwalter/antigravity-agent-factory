import os
import hashlib
import logging
import re
from typing import List, Optional, Dict, Any
from collections import defaultdict

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_core.stores import InMemoryStore
from langchain_classic.retrievers import ParentDocumentRetriever
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.tools import tool
from langchain_core.documents import Document
import fitz

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

    def _compute_file_hash(self, file_path: str) -> Optional[str]:
        """Compute SHA-256 hash of a file for deduplication."""
        try:
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (FileNotFoundError, OSError):
            return None

    def list_sources(self) -> List[Dict[str, Any]]:
        """Return a deduplicated list of all indexed sources with metadata."""
        seen_sources: Dict[str, Dict[str, Any]] = {}
        for key in self.store.yield_keys():
            docs = self.store.mget([key])
            doc = docs[0] if docs else None
            if doc is None or "source" not in doc.metadata:
                continue
            source = doc.metadata["source"]
            if source not in seen_sources:
                seen_sources[source] = {
                    "source": source,
                    "file_hash": doc.metadata.get("file_hash"),
                    "chunk_count": 1,
                    "has_toc": doc.metadata.get("is_toc", False),
                }
            else:
                seen_sources[source]["chunk_count"] += 1
                if doc.metadata.get("is_toc", False):
                    seen_sources[source]["has_toc"] = True
        return list(seen_sources.values())

    def get_library_info(self) -> Dict[str, Any]:
        """Return library-wide statistics and per-source metadata."""
        sources = self.list_sources()
        total_chunks = sum(s["chunk_count"] for s in sources)
        return {
            "total_documents": len(sources),
            "total_chunks": total_chunks,
            "sources": sources,
        }

    def _score_toc(self, toc_text: Optional[str]) -> float:
        """Score TOC quality from 0.0 (garbage) to 1.0 (excellent).

        Heuristic scoring based on:
        - Line count (more lines = more structure)
        - Chapter/section keywords
        - Hierarchy markers (indentation, numbering)
        - Penalties for copyright, short, or title-only content
        """
        if not toc_text or not toc_text.strip():
            return 0.0

        text = toc_text.strip()
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        score = 0.0

        # Penalty: too short (< 3 lines)
        if len(lines) < 3:
            return min(0.1 * len(lines), 0.2)

        # Penalty: copyright/publisher content
        copyright_keywords = [
            "copyright",
            "published by",
            "all rights reserved",
            "o'reilly",
            "isbn",
            "edition",
            "printed in",
        ]
        copyright_hits = sum(1 for kw in copyright_keywords if kw in text.lower())
        if copyright_hits >= 2:
            return 0.1

        # Reward: chapter/section keywords
        structure_pattern = re.compile(
            r"(chapter|part|section|anhang|kapitel|teil|abschnitt)\s+\d",
            re.IGNORECASE,
        )
        structure_hits = len(structure_pattern.findall(text))
        score += min(structure_hits * 0.1, 0.4)

        # Reward: bullet points or numbered items
        bullet_lines = sum(1 for l in lines if l.startswith(("-", "•", "*")))
        score += min(bullet_lines * 0.03, 0.2)

        # Reward: page number references
        page_refs = len(
            re.findall(r"\(p\.\s*\d+\)|\bpage\s+\d+\b|S\.\s*\d+", text, re.IGNORECASE)
        )
        score += min(page_refs * 0.02, 0.15)

        # Reward: line count (more = more structured)
        score += min(len(lines) * 0.02, 0.25)

        return min(score, 1.0)

    def get_toc(self, name: str) -> Optional[str]:
        """Fast TOC lookup by document name — direct metadata scan, no semantic search.

        Args:
            name: Partial document name (case-insensitive fuzzy match on basename)

        Returns:
            TOC text content or None if not found
        """
        needle = name.lower()
        for key in self.store.yield_keys():
            docs = self.store.mget([key])
            doc = docs[0] if docs else None
            if doc is None:
                continue
            source = doc.metadata.get("source", "")
            is_toc = doc.metadata.get("is_toc", False)
            if is_toc and needle in os.path.basename(source).lower():
                return doc.page_content
        return None

    def delete_toc(self, name: str) -> bool:
        """Delete the TOC chunk for a document (by fuzzy name match).

        Returns True if a TOC chunk was found and deleted.
        """
        needle = name.lower()
        keys_to_delete = []
        for key in self.store.yield_keys():
            docs = self.store.mget([key])
            doc = docs[0] if docs else None
            if doc is None:
                continue
            source = doc.metadata.get("source", "")
            is_toc = doc.metadata.get("is_toc", False)
            if is_toc and needle in os.path.basename(source).lower():
                keys_to_delete.append(key)

        if keys_to_delete:
            self.store.mdelete(keys_to_delete)
            logger.info(f"Deleted {len(keys_to_delete)} TOC chunk(s) for '{name}'")
            return True
        return False

    def _extract_toc(self, pdf_path: str) -> Optional[str]:
        """Multi-strategy TOC extraction with 3-tier fallback.

        Strategy 1: PyMuPDF native TOC (doc.get_toc())
        Strategy 2: Regex heuristic (chapter/section patterns)
        Strategy 3: LLM extraction (Gemini, last resort)
        """
        filename = os.path.basename(pdf_path)

        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            logger.error(f"Failed to open PDF for TOC extraction: {e}")
            return None

        # --- Strategy 1: PyMuPDF native TOC ---
        try:
            native_toc = doc.get_toc()
            if native_toc:
                lines = []
                for level, title, page in native_toc:
                    indent = "  " * (level - 1)
                    lines.append(f"{indent}- {title} (p. {page})")

                toc_text = "\n## Table of Contents (Native)\n\n" + "\n".join(lines)
                score = self._score_toc(toc_text)
                if score >= 0.3:
                    logger.info(
                        f"Native TOC extracted for '{filename}' and scored {score:.2f}"
                    )
                    doc.close()
                    return toc_text
                else:
                    logger.warning(
                        f"Native TOC for '{filename}' rejected (score {score:.2f} too low)"
                    )
        except Exception as e:
            logger.debug(f"Native TOC extraction failed: {e}")

        # --- Strategy 2: Regex heuristic ---
        try:
            chapter_pattern = re.compile(
                r"^\s*(Chapter|Part|Section|CHAPTER|PART|Kapitel|Teil|Abschnitt)\s+\d+[.::\s]",
                re.MULTILINE,
            )
            toc_entries = []
            max_pages = min(20, len(doc))
            for i in range(max_pages):
                page_text = doc[i].get_text("text")
                for line in page_text.split("\n"):
                    if chapter_pattern.match(line.strip()):
                        toc_entries.append(f"- {line.strip()}")

            if toc_entries:
                toc_text = "\n## Table of Contents (Regex Extracted)\n\n" + "\n".join(
                    toc_entries
                )
                score = self._score_toc(toc_text)
                if score >= 0.3:
                    logger.info(
                        f"Regex TOC extracted for '{filename}' and scored {score:.2f}"
                    )
                    doc.close()
                    return toc_text
                else:
                    logger.warning(
                        f"Regex TOC for '{filename}' rejected (score {score:.2f} too low)"
                    )
        except Exception as e:
            logger.debug(f"Regex TOC extraction failed: {e}")

        # --- Strategy 3: LLM extraction (last resort) ---
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import PromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            extracted_text = []
            max_pages_llm = min(40, len(doc))
            for i in range(max_pages_llm):
                page_text = doc[i].get_text("text").strip()
                if page_text:
                    extracted_text.append(f"--- PAGE {i+1} ---\n{page_text}")

            raw_text = "\n\n".join(extracted_text)
            if raw_text:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.1,
                    max_tokens=2048,
                )

                template = """
You are an expert librarian and data extraction agent.
Your task is to analyze the front-matter pages of a technical book and extract a perfect, hierarchical Table of Contents (TOC).

Source Book: {filename}

Here is the raw text extracted from the first few dozen pages:
<RAW_TEXT>
{raw_text}
</RAW_TEXT>

INSTRUCTIONS:
1. Locate the actual Table of Contents within the raw text. Ignore introductory praises, copyright pages, and prefaces unless they are listed IN the TOC.
2. Extract the hierarchical structure (Parts, Chapters, Sections) and page numbers if available.
3. Format the output STRICTLY as Markdown bullet points.
4. Use headers (e.g., `## Part 1`) if the book is divided into parts.
5. Do not include any conversational filler (e.g. "Here is the TOC:"). ONLY return the markdown TOC itself.
6. If you cannot find any indication of a Table of Contents, return exactly "NO_TOC_FOUND".

RETURN ONLY THE MARKDOWN TOC:
"""
                prompt = PromptTemplate.from_template(template)
                chain = prompt | llm | StrOutputParser()

                logger.info(f"Invoking LLM for TOC extraction on: {filename}...")
                result = chain.invoke({"raw_text": raw_text, "filename": filename})

                if result.strip() != "NO_TOC_FOUND":
                    toc_text = "\n## Table of Contents (AI Extracted)\n\n" + result
                    score = self._score_toc(toc_text)
                    if score >= 0.3:
                        logger.info(
                            f"LLM TOC extracted for '{filename}' and scored {score:.2f}"
                        )
                        return toc_text
                    else:
                        logger.warning(
                            f"LLM TOC for '{filename}' rejected (score {score:.2f} too low)"
                        )
        except Exception as e:
            logger.error(f"LLM TOC extraction failed for '{filename}': {e}")
        finally:
            if "doc" in locals() and doc:
                doc.close()

        return None

    def delete_document(self, source_path: str):
        """Remove all chunks associated with a specific source path from the library."""
        norm_path = os.path.normpath(source_path)
        logger.info(f"Deleting document from library: {norm_path}")

        # 1. Collect IDs to delete from the docstore
        keys_to_delete = [
            key
            for key in self.store.yield_keys()
            if (doc := self.store.mget([key])[0])
            and os.path.normpath(doc.metadata.get("source", "")) == norm_path
        ]

        if not keys_to_delete:
            logger.warning(f"No document found with source path: {norm_path}")
            # Still attempt Qdrant cleanup just in case docstore is out of sync

        # 2. Optimized Batch Delete from Qdrant vectorstore (One call for all chunks + TOC)
        from qdrant_client.http import models

        try:
            self.client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="metadata.source",
                                match=models.MatchValue(value=norm_path),
                            )
                        ]
                    )
                ),
            )
        except Exception as e:
            logger.error(f"Qdrant delete failed for {norm_path}: {e}")

        # 3. Delete parents from InMemoryStore
        if keys_to_delete:
            self.store.mdelete(keys_to_delete)

            # 4. Delete parent files from disk
            for doc_id in keys_to_delete:
                file_path = os.path.join(self.parent_store_path, doc_id)
                if os.path.exists(file_path):
                    os.remove(file_path)

        # 5. Invalidate cache
        cache_path = os.path.join(
            os.path.dirname(self.parent_store_path), "parent_store_cache.json"
        )
        if os.path.exists(cache_path):
            os.remove(cache_path)

        logger.info(f"Successfully deleted document {norm_path}")

    def ingest_ebook(self, pdf_path: str, force: bool = False) -> Optional[str]:
        """Parse and add a PDF to the library using Parent-Child strategy.

        Returns a status string describing the result.
        """
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            return f"Error: File not found: {pdf_path}"

        norm_path = os.path.normpath(pdf_path)
        file_hash = self._compute_file_hash(pdf_path)

        if not force:
            # Dedup check: hash-based and path-based
            existing_hashes = set()
            existing_sources = set()
            for key in self.store.yield_keys():
                docs = self.store.mget([key])
                doc = docs[0] if docs else None
                if doc is None:
                    continue
                if "source" in doc.metadata:
                    existing_sources.add(os.path.normpath(doc.metadata["source"]))
                if "file_hash" in doc.metadata:
                    existing_hashes.add(doc.metadata["file_hash"])

            if norm_path in existing_sources:
                msg = f"Skipped (already indexed by path): {norm_path}"
                logger.info(msg)
                return msg

            if file_hash and file_hash in existing_hashes:
                msg = f"Skipped (duplicate by hash): {norm_path}"
                logger.info(msg)
                return msg

        logger.info(f"Ingesting ebook: {pdf_path}")
        loader = PyMuPDFLoader(pdf_path)
        docs = list(loader.load())

        # Add metadata for tracking
        for doc in docs:
            doc.metadata["source"] = norm_path
            if file_hash:
                doc.metadata["file_hash"] = file_hash

        # Split into parent chunks
        parent_docs = self.retriever.parent_splitter.split_documents(docs)

        # Propagate hash to split chunks
        for pd in parent_docs:
            pd.metadata["source"] = norm_path
            if file_hash:
                pd.metadata["file_hash"] = file_hash

        # Extract TOC
        toc_content = self._extract_toc(pdf_path)
        if toc_content:
            logger.info("TOC found. Injecting as specialized chunk.")
            toc_doc = Document(
                page_content=f"MASTER TABLE OF CONTENTS (INHALTSVERZEICHNIS)\n\n{toc_content}",
                metadata={
                    "source": norm_path,
                    "is_toc": True,
                    "document_title": os.path.basename(norm_path),
                    "file_hash": file_hash or "",
                },
            )
            parent_docs.insert(0, toc_doc)

        # Generate consistent IDs
        import uuid

        ids = [str(uuid.uuid4()) for _ in range(len(parent_docs))]

        # Save to vectorstore + in-memory store
        self.retriever.add_documents(parent_docs, ids=ids)

        # Persist to disk
        self._persist_to_disk(parent_docs, ids)
        logger.info(f"Successfully ingested {pdf_path}")
        return None

    def _extract_url_toc(self, url: str) -> Optional[str]:
        """Attempt to extract Table of Contents from a URL using HTML headings."""
        try:
            import requests
            from bs4 import BeautifulSoup

            # Add a generic user agent to prevent 403 Forbidden errors on some sites
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all headings h1-h4
            headings = soup.find_all(["h1", "h2", "h3", "h4"])
            if not headings:
                return None

            toc_lines = ["## Table of Contents (Extracted HTML Headings)"]
            seen_texts = set()

            for h in headings:
                level = int(h.name[1])  # 'h2' -> 2
                text = h.get_text(strip=True)
                # Skip empty headings or duplicates
                if text and len(text) > 2 and text not in seen_texts:
                    seen_texts.add(text)
                    indent = "  " * (level - 1)
                    toc_lines.append(f"{indent}- {text}")

            if len(toc_lines) > 1:
                return "\n".join(toc_lines)
            return None
        except Exception as e:
            logger.warning(f"Failed to extract TOC from URL {url}: {e}")
            return None

    def ingest_url(self, url: str):
        """Parse and add a Web URL to the library using Parent-Child strategy."""

        # Idempotency check: Check if this URL is already in the library
        existing_sources = {
            doc.metadata["source"]
            for key in self.store.yield_keys()
            if (doc := self.store.mget([key])[0]) and "source" in doc.metadata
        }

        if url in existing_sources:
            logger.info(f"Skipping ingestion: {url} is already in the library.")
            return

        logger.info(f"Ingesting URL: {url}")
        try:
            from langchain_community.document_loaders import WebBaseLoader

            loader = WebBaseLoader(url)
            docs = list(loader.load())
        except Exception as e:
            logger.error(f"Failed to load URL {url}: {e}")
            return

        # Add metadata for tracking
        for doc in docs:
            doc.metadata["source"] = url
            if "title" in doc.metadata:
                doc.metadata["document_title"] = doc.metadata["title"]
            else:
                doc.metadata["document_title"] = url

        # Split into parent chunks first to ensure we have the correct count for IDs
        parent_docs = self.retriever.parent_splitter.split_documents(docs)

        # Execute TOC logic for URLs
        toc_content = self._extract_url_toc(url)
        if toc_content:
            logger.info("Deterministic HTML TOC found. Injecting as specialized chunk.")
            # Build a dedicated Langchain Document just for the TOC layout
            toc_doc = Document(
                page_content=f"MASTER TABLE OF CONTENTS (INHALTSVERZEICHNIS)\n\n{toc_content}",
                metadata={
                    "source": url,
                    "is_toc": True,
                    "document_title": docs[0].metadata.get("title", url)
                    if docs
                    else url,
                },
            )
            # Inject it at the very beginning of the parent_docs for vector store indexing
            parent_docs.insert(0, toc_doc)

        # Generate consistent IDs for both retriever (vectorstore/RAM) and disk persistence
        import uuid

        ids = [str(uuid.uuid4()) for _ in range(len(parent_docs))]

        # This will save to vectorstore and populate the IN-MEMORY RAM store
        self.retriever.add_documents(parent_docs, ids=ids)

        # Persist new documents to disk using the SAME IDs so they can be re-hydrated next session
        self._persist_to_disk(parent_docs, ids)
        logger.info(f"Successfully ingested {url}")

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


@tool
def get_ebook_toc(document_name: str) -> str:
    """
    Retrieves the deterministic Table of Contents for a specific document in the library.
    Use this to get an exact outline of an ebook before searching.
    Supply the document name or a fuzzy match of its title (e.g., 'Russell').
    """
    rag = get_rag()
    toc_content = rag.get_toc(document_name)

    if toc_content:
        return toc_content
    return f"No Table of Contents found for document matching '{document_name}'."


if __name__ == "__main__":
    # Self-test if run directly
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        rag = get_rag()

        if command == "ingest" and len(sys.argv) > 2:
            path_or_url = sys.argv[2]
            if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
                rag.ingest_url(path_or_url)
            else:
                rag.ingest_ebook(path_or_url)
        elif command == "query" and len(sys.argv) > 2:
            print(search_ebook_library.run(sys.argv[2]))
        else:
            print(
                "Usage: python rag_optimized.py [ingest <pdf_path_or_url> | query <question>]"
            )
