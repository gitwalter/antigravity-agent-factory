import os
import sys
import logging
from typing import List, Dict, Any, Optional

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from scripts.ai.rag.rag_optimized import get_rag, OptimizedRAG

logger = logging.getLogger(__name__)


class RAGManager:
    """
    Standalone RAGManager for Knowledge Explorer.
    """

    def __init__(self):
        self.rag: OptimizedRAG = get_rag(warmup=False)

    def get_catalog(self) -> List[Dict[str, str]]:
        try:
            client = self.rag.client
            points_result = client.scroll(
                collection_name="ebook_library", limit=1000, with_payload=True
            )
            points = points_result[0]

            sources = {}
            for p in points:
                if p.payload and "metadata" in p.payload:
                    source_path = p.payload["metadata"].get("source", "")
                    if source_path:
                        name = os.path.basename(source_path)
                        if name not in sources:
                            sources[name] = {
                                "name": name,
                                "path": source_path,
                                "title": p.payload["metadata"].get(
                                    "document_title", name
                                ),
                            }
            return sorted(list(sources.values()), key=lambda x: x["name"])
        except Exception as e:
            logger.error(f"Error fetching RAG catalog: {e}")
            return []

    def semantic_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            docs = self.rag.query(query)
            embeddings = self.rag.embeddings
            import numpy as np

            query_emb = embeddings.embed_query(query)

            results = []
            for doc in docs:
                doc_emb = embeddings.embed_documents([doc.page_content])[0]
                q_vec = np.array(query_emb)
                d_vec = np.array(doc_emb)
                similarity = np.dot(q_vec, d_vec) / (
                    np.linalg.norm(q_vec) * np.linalg.norm(d_vec) + 1e-10
                )

                results.append(
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "source": os.path.basename(
                            doc.metadata.get("source", "Unknown")
                        ),
                        "relevance_score": float(similarity),
                        "is_relevant": similarity >= 0.25,
                    }
                )
            return sorted(results, key=lambda x: x["relevance_score"], reverse=True)[
                :limit
            ]
        except Exception as e:
            logger.error(f"Error in RAG semantic search: {e}")
            return []

    def get_document_toc(self, document_name: str) -> Optional[str]:
        return self.rag.get_toc(document_name)

    def get_document_chunks(self, source_name: str, limit: int = 50) -> List[str]:
        try:
            catalog = self.get_catalog()
            source_path = next(
                (
                    d["path"]
                    for d in catalog
                    if d["name"].lower() == source_name.lower()
                ),
                None,
            )
            if not source_path:
                return []

            from qdrant_client.http.models import Filter, FieldCondition, MatchValue

            f = Filter(
                must=[
                    FieldCondition(
                        key="metadata.source", match=MatchValue(value=source_path)
                    )
                ]
            )
            result = self.rag.client.scroll(
                collection_name="ebook_library",
                limit=limit,
                with_payload=True,
                scroll_filter=f,
            )
            return [
                p.payload.get("page_content", "").strip()[:1000]
                for p in result[0]
                if p.payload
            ]
        except Exception as e:
            logger.error(f"Error getting chunks: {e}")
            return []

    def scan_library(self, directory: str) -> Dict[str, Any]:
        try:
            directory = os.path.abspath(directory)
            if not os.path.isdir(directory):
                return {"error": f"Not a directory: {directory}"}
            local_pdfs = []
            for root, _, files in os.walk(directory):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        local_pdfs.append(os.path.abspath(os.path.join(root, f)))
            catalog = self.get_catalog()
            indexed_paths = {
                os.path.normcase(os.path.normpath(d["path"])) for d in catalog
            }
            missing = []
            present = []
            for pdf in local_pdfs:
                norm = os.path.normcase(os.path.normpath(pdf))
                if norm in indexed_paths:
                    present.append({"name": os.path.basename(pdf), "path": pdf})
                else:
                    missing.append(
                        {
                            "name": os.path.basename(pdf),
                            "path": pdf,
                            "size_mb": os.path.getsize(pdf) / (1024 * 1024),
                        }
                    )
            return {
                "total": len(local_pdfs),
                "indexed_count": len(present),
                "missing_count": len(missing),
                "missing": missing,
            }
        except Exception as e:
            logger.error(f"Error scanning: {e}")
            return {"error": str(e)}

    def ingest_document(self, file_path: str) -> bool:
        try:
            self.rag.ingest_ebook(file_path)
            return True
        except Exception as e:
            logger.error(f"Error ingesting: {e}")
            return False

    def ingest_url(self, url: str) -> bool:
        try:
            self.rag.ingest_url(url)
            return True
        except Exception as e:
            logger.error(f"Error ingesting URL: {e}")
            return False

    def check_service_status(self) -> Dict[str, Any]:
        status = {"qdrant": False, "count": 0}
        try:
            client = self.rag.client
            collection_info = client.get_collection("ebook_library")
            status["qdrant"] = True
            status["count"] = collection_info.points_count
        except Exception:
            pass
        return status

    def synthesize_answer(
        self, question: str, contexts: List[str], ai_manager: Any
    ) -> str:
        if not contexts:
            return "No local context available."
        context_block = "\n\n".join(
            [f"[Context {i+1}]: {ctx}" for i, ctx in enumerate(contexts)]
        )
        system_prompt = "You are an AI research assistant. Answer based STRICTLY on provided context. Use [1], [2] citations."
        user_prompt = f"### Question: {question}\n\n### Context:\n{context_block}"
        try:
            from langchain_core.messages import HumanMessage, SystemMessage

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = ai_manager.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error in RAG synthesis: {e}")
            return f"Error: {str(e)}"
