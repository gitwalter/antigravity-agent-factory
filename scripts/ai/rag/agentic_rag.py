import os
import sys
import logging
from typing import List, Annotated, Union
from typing_extensions import TypedDict

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_classic.storage import LocalFileStore, create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from qdrant_client import QdrantClient
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import END, StateGraph, START

from scripts.ai.rag.rag_optimized import get_rag

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
    print("---RETRIEVE---")
    question = state["question"]
    rag = get_rag()
    documents = rag.query(question)
    print(f"---RETRIEVED {len(documents)} DOCUMENTS---")
    for i, doc in enumerate(documents):
        print(f"Doc {i} Snippet: {doc.page_content[:100]}...")
    return {"documents": documents, "question": question}


def normalize_text(text: str) -> str:
    """Normalize text for more robust comparison."""
    import re

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
    Determines whether the retrieved documents are relevant to the question.
    """
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = normalize_text(state["question"])
    documents = state["documents"]

    if not documents:
        return {
            "web_search": "yes",
            "question": state["question"],
            "documents": documents,
        }

    # Heuristic: Check if normalized keywords from question appear in normalized snippets
    keywords = [w for w in question.split() if len(w) > 3]
    relevant_count = 0
    for doc in documents:
        content = normalize_text(doc.page_content)
        if any(kw in content for kw in keywords):
            relevant_count += 1
            print("---DOCUMENT GRADED RELEVANT (Keyword match)---")

    if relevant_count == 0:
        print("---NO DOCUMENTS GRADED RELEVANT---")
        return {
            "web_search": "yes",
            "question": state["question"],
            "documents": documents,
        }

    return {"web_search": "no", "question": state["question"], "documents": documents}


def generate(state):
    """
    Generate answer/format results
    """
    print("---FORMAT RESULTS---")
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
    print("---WEB SEARCH REQUESTED---")
    return {"documents": [], "question": state["question"], "web_search": "yes"}


# --- Build Graph ---


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-route to web search.
    """
    print("---ASSESS GRADED DOCUMENTS---")
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


if __name__ == "__main__":
    agentic_rag = AgenticRAG()
    # Test query
    result = agentic_rag.query("Was ist Wissensrepräsentation?")
    print(f"Status: {result.get('web_search')}")
    print(f"Generation: {result.get('generation', '')[:200]}...")
