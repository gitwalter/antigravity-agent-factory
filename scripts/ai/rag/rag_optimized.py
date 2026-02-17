import os
import logging
from typing import List, Optional

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_classic.storage import LocalFileStore, create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
QDRANT_PATH = "data/rag/qdrant_workspace"
PARENT_STORE_PATH = "data/rag/parent_store"
COLLECTION_NAME = "ebook_library"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE = 384


class OptimizedRAG:
    """Highly optimized Parent-Child RAG architecture for PDF ebooks."""

    def __init__(self):
        # 1. Initialize Embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        # 2. Initialize Qdrant Client and Collection
        self.client = QdrantClient(path=QDRANT_PATH)

        # Ensure collection exists
        collections = self.client.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)

        if not exists:
            logger.info(f"Creating Qdrant collection: {COLLECTION_NAME}")
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )

        # Connect to LangChain's Qdrant Vector Store
        self.vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding=self.embeddings,
        )

        # 3. Initialize Parent Store
        fs = LocalFileStore(root_path=PARENT_STORE_PATH)
        self.store = create_kv_docstore(fs)

        # 4. Text Splitters
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=200
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400, chunk_overlap=50
        )

        # 5. Initialize ParentDocumentRetriever
        self.retriever = ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
        )

    def ingest_ebook(self, pdf_path: str):
        """Parse and add a PDF to the library using Parent-Child strategy."""
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            return

        logger.info(f"Ingesting ebook: {pdf_path}")
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()

        # Add metadata for tracking
        for doc in docs:
            doc.metadata["source"] = os.path.normpath(pdf_path)

        self.retriever.add_documents(docs, ids=None)
        logger.info(f"Successfully ingested {pdf_path}")

    def query(self, question: str, k: int = 5):
        """Perform semantic search and return relevant parent chunks."""
        return self.retriever.invoke(question)


# Initialize global instance for the tool
_rag_instance: Optional[OptimizedRAG] = None


def get_rag():
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = OptimizedRAG()
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
