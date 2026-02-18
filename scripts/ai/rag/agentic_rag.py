import os
import sys
import logging
from typing import List
from typing_extensions import TypedDict
import re
import numpy as np

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Only import what we use
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START

from scripts.ai.rag.rag_optimized import get_rag

logger = logging.getLogger(__name__)

# --- State Definition ---


class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """

    question: str
    generation: str
    documents: List[str]
    web_search: str  # "yes" or "no"


# --- Nodes ---


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


def retrieve(state):
    """
    Retrieve documents
    """
    logger.info("---RETRIEVE---")
    question = state["question"]
    rag = get_rag()
    documents = rag.query(question)
    logger.info(f"---RETRIEVED {len(documents)} DOCUMENTS---")
    for i, doc in enumerate(documents):
        # Log minimal snippet to avoid spamming logs
        logger.debug(f"Doc {i} Snippet: {doc.page_content[:100]}...")
    return {"documents": documents, "question": question}


def normalize_text(text: str) -> str:
    """Normalize text for more robust comparison."""
    # Replace common umlauts
    text = text.lower()
    text = (
        text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    )
    # Remove non-alphanumeric (except spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    using embedding-based semantic similarity.
    """
    logger.info("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    documents = state["documents"]
    question = state["question"]

    if not documents:
        logger.info("---NO DOCUMENTS RETRIEVED, ROUTING TO WEB SEARCH---")
        return {
            "web_search": "yes",
            "question": question,
            "documents": documents,
        }

    try:
        rag = get_rag()
        embeddings = rag.embeddings

        # Embed query and documents
        query_emb = embeddings.embed_query(question)
        doc_texts = [doc.page_content for doc in documents]
        doc_embs = embeddings.embed_documents(doc_texts)

        # Cosine similarity
        query_vec = np.array(query_emb)
        relevant_docs = []
        threshold = 0.25  # MiniLM cosine similarity threshold

        for doc, doc_emb in zip(documents, doc_embs):
            doc_vec = np.array(doc_emb)
            similarity = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec) + 1e-10
            )
            if similarity >= threshold:
                relevant_docs.append(doc)
                logger.debug(f"---DOCUMENT RELEVANT (similarity={similarity:.3f})---")
            else:
                logger.debug(
                    f"---DOCUMENT FILTERED (similarity={similarity:.3f} < {threshold})---"
                )

        if not relevant_docs:
            logger.info("---ALL DOCUMENTS BELOW THRESHOLD, ROUTING TO WEB SEARCH---")
            return {
                "web_search": "yes",
                "question": question,
                "documents": documents,  # still pass them for fallback generation
            }

        logger.info(
            f"---{len(relevant_docs)}/{len(documents)} DOCUMENTS PASSED RELEVANCE---"
        )
        return {"web_search": "no", "question": question, "documents": relevant_docs}

    except Exception as e:
        # If embedding grading fails, trust the vector store results
        logger.error(f"---GRADING ERROR: {e}, TRUSTING VECTOR STORE---")
        return {"web_search": "no", "question": question, "documents": documents}


def generate(state):
    """
    Generate answer/format results
    """
    logger.info("---FORMAT RESULTS---")
    documents = state["documents"]

    if not documents:
        return {
            "generation": "No relevant local or web information found.",
            "question": state["question"],
            "documents": documents,
        }

    formatted_results = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content
        formatted_results.append(f"### Result {i} (Source: {source})\n{content}\n")

    return {
        "generation": "\n".join(formatted_results),
        "question": state["question"],
        "documents": documents,
    }


def web_search(state):
    """
    Web search fallback placeholder
    """
    logger.info("---WEB SEARCH REQUESTED---")
    return {"documents": [], "question": state["question"], "web_search": "yes"}


# --- Build Graph ---


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-route to web search.
    """
    logger.info("---ASSESS GRADED DOCUMENTS---")
    if state.get("web_search") == "yes":
        return "web_search"
    else:
        return "generate"


def build_graph():
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("web_search", web_search)

    # Build graph
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "web_search": "web_search",
            "generate": "generate",
        },
    )
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)

    # Compile
    app = workflow.compile()
    return app


class AgenticRAG:
    """Orchestrates the Agentic RAG workflow via LangGraph."""

    def __init__(self):
        self.app = build_graph()

    def query(self, question: str) -> dict:
        config = {"configurable": {"thread_id": "1"}}
        inputs = {"question": question}
        return self.app.invoke(inputs, config)
