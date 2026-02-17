import os
import logging
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAgent:
    """Agentic RAG implementation using local FAISS and HuggingFace embeddings for high performance."""

    def __init__(
        self,
        index_path: str = "./.vector_store",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        # Use local embeddings to avoid latency and API keys
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

        # Load Vector Store
        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}. Run ingestion first."
            )

        # Standardized FAISS loading
        self.vector_store = FAISS.load_local(
            index_path,
            self.embeddings,
            index_name="index",
            allow_dangerous_deserialization=True,
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})

        # Define Prompt
        self.prompt = ChatPromptTemplate.from_template("""
        Answer the question based only on the following context:
        {context}

        Question: {question}
        """)

    def get_chain(self):
        """Construct the LCEL RAG chain."""

        def format_docs(docs):
            return "\n\n".join(
                f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
                for doc in docs
            )

        return (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | StrOutputParser()
        )

    def query_context(self, question: str) -> List:
        """Retrieve relevant context documents directly."""
        return self.retriever.invoke(question)


if __name__ == "__main__":
    # Example usage
    try:
        agent = RAGAgent()
        results = agent.query_context("main topics of Stuart Russell book")
        for i, res in enumerate(results, 1):
            print(f"\n{i}. Source: {res.metadata.get('source')}")
            print(f"Content: {res.page_content[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
