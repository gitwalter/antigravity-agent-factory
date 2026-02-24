import streamlit as st
import os
import sys
import logging

# Set page config FIRST
st.set_page_config(page_title="🧠 Knowledge Explorer", page_icon="🧠", layout="wide")

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from projects.rag_knowledge_explorer.core.rag_manager import RAGManager
from projects.rag_knowledge_explorer.core.ai_manager import AIManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize Managers
@st.cache_resource
def get_managers():
    return RAGManager(), AIManager()


rag_manager, ai_manager = get_managers()


def main():
    st.title("🧠 Antigravity Knowledge Explorer")
    st.markdown(
        "Semantic search and document intelligence over the factory RAG library."
    )

    # Service Status in Sidebar
    status = rag_manager.check_service_status()
    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 RAG Service Health")
    if status["qdrant"]:
        st.sidebar.success(f"Qdrant: Online ({status['count']} chunks)")
    else:
        st.sidebar.error("Qdrant: Offline")
        st.error(
            "⚠️ **RAG Backend Unreachable.** Please ensure the Qdrant Docker container is running."
        )

    if status["qdrant"]:
        search_tab, library_tab, ingest_tab = st.tabs(
            ["🔍 Semantic Search", "📁 Library Browser", "📥 Ingestion"]
        )

        with search_tab:
            st.subheader("Semantic Discovery")
            st.info(
                "💡 **Pattern:** Uses local `FastEmbed` embeddings (Cost: Free) with Parent-Child retrieval."
            )

            q_col1, q_col2 = st.columns([4, 1])
            with q_col1:
                search_query = st.text_input(
                    "Enter question or concept",
                    placeholder="e.g., How does the landing page design align with user engagement?",
                    label_visibility="collapsed",
                )
            with q_col2:
                search_limit = st.selectbox("Top K", [3, 5, 10, 20], index=1)

            use_ai = st.toggle(
                "🧠 **Generate AI Answer** (Requires LLM Call)",
                value=False,
                help="Uses Gemini to synthesize an answer from the retrieved context. Cost: approx. $0.001 per call.",
            )

            if search_query:
                with st.spinner("Retrieving knowledge fragments..."):
                    results = rag_manager.semantic_search(
                        search_query, limit=search_limit
                    )

                    if results:
                        st.success(f"Found {len(results)} relevant context blocks.")

                        # Process AI Answer if requested
                        if use_ai:
                            with st.status(
                                "🧠 Synthesizing with Gemini...", expanded=True
                            ) as status_ui:
                                contexts = [
                                    r["content"] for r in results if r["is_relevant"]
                                ]
                                answer = rag_manager.synthesize_answer(
                                    search_query, contexts, ai_manager
                                )
                                st.markdown("### 🤖 AI Insight")
                                st.markdown(answer)
                                status_ui.update(
                                    label="AI Synthesis Complete", state="complete"
                                )

                        st.markdown("### 🔍 Retrieved Contexts")
                        for i, res in enumerate(results):
                            with st.container():
                                c1, c2 = st.columns([3, 1])
                                with c1:
                                    st.markdown(
                                        f"#### [{i+1}] Source: `{res['source']}`"
                                    )
                                with c2:
                                    # Relevance Grade
                                    color = "green" if res["is_relevant"] else "orange"
                                    st.markdown(
                                        f"<p style='color:{color}; font-weight:bold; text-align:right;'>Relevance: {res['relevance_score']:.2f}</p>",
                                        unsafe_allow_html=True,
                                    )

                                st.markdown(res["content"])
                                st.divider()
                    else:
                        st.warning("No relevant information found in the library.")

        with library_tab:
            st.subheader("Indexed Documents")
            catalog = rag_manager.get_catalog()
            if catalog:
                selected_doc = st.selectbox(
                    "Select document to inspect", [d["name"] for d in catalog]
                )
                doc_info = next(d for d in catalog if d["name"] == selected_doc)

                l_col1, l_col2 = st.columns([2, 1])
                with l_col1:
                    st.markdown(f"**Title:** {doc_info['title']}")
                    st.markdown(f"**Path:** `{doc_info['path']}`")

                with l_col2:
                    st.info(
                        "💡 **Pattern:** Documents are stored using a Parent-Child strategy for high-context retrieval."
                    )

                b_tab1, b_tab2 = st.tabs(["🧩 Browse Fragments", "�️ TOC Recon"])
                with b_tab1:
                    if st.button("🔄 Fetch Sample Chunks"):
                        chunks = rag_manager.get_document_chunks(selected_doc, limit=10)
                        if chunks:
                            for idx, chunk in enumerate(chunks):
                                st.text_area(f"Chunk {idx+1}", chunk, height=150)
                        else:
                            st.info("No fragments retrieved for this document.")
                with b_tab2:
                    if st.button("🗺️ Load TOC Structure"):
                        toc = rag_manager.get_document_toc(selected_doc)
                        if toc:
                            st.markdown("### 📋 Table of Contents")
                            st.markdown(toc)
                        else:
                            st.info("No deterministic TOC found for this document.")
            else:
                st.info("The RAG library is currently empty.")

        with ingest_tab:
            st.subheader("Factory Ingestion Pipeline")
            st.write(
                "Add new PDF documents or websites to the permanent knowledge base."
            )

            i_tab1, i_tab2, i_tab3 = st.tabs(
                ["📥 Single PDF", "🔍 Library Scan", "🌐 Web URL"]
            )

            with i_tab1:
                pdf_path = st.text_input(
                    "Absolute Path to PDF",
                    placeholder="D:/ebooks/technical_manual.pdf",
                    key="single_pdf",
                )
                if st.button("🚀 Start Ingestion", key="btn_ingest"):
                    if (
                        pdf_path
                        and pdf_path.lower().endswith(".pdf")
                        and os.path.exists(pdf_path)
                    ):
                        with st.spinner("Processing Parent-Child chunks..."):
                            if rag_manager.ingest_document(pdf_path):
                                st.balloons()
                                st.success(
                                    "Document ingested and synchronized with Qdrant."
                                )
                            else:
                                st.error("Ingestion failed. Consult terminal logs.")
                    else:
                        st.error("Please provide a valid absolute path to a PDF file.")

            with i_tab3:
                web_url = st.text_input(
                    "Website URL",
                    placeholder="https://docs.langchain.com/...",
                    key="single_url",
                )
                if st.button("🚀 Ingest URL", key="btn_ingest_url"):
                    if web_url and (
                        web_url.startswith("http://") or web_url.startswith("https://")
                    ):
                        with st.spinner("Fetching and chunking website content..."):
                            if rag_manager.ingest_url(web_url):
                                st.balloons()
                                st.success(
                                    f"Website '{web_url}' ingested and synchronized with Qdrant."
                                )
                            else:
                                st.error("Ingestion failed. Consult terminal logs.")
                    else:
                        st.error("Please provide a valid HTTP/HTTPS URL.")

            with i_tab2:
                scan_dir = st.text_input(
                    "Directory to Scan", value="D:/ebooks", placeholder="D:/ebooks"
                )
                if st.button("🔍 Scan for New Knowledge"):
                    with st.spinner("Comparing local files with Qdrant index..."):
                        report = rag_manager.scan_library(scan_dir)
                        if "error" in report:
                            st.error(report["error"])
                        else:
                            st.metric("Total PDFs Found", report["total"])
                            c1, c2 = st.columns(2)
                            c1.metric("Already Indexed", report["indexed_count"])
                            c2.metric("Missing Knowledge", report["missing_count"])

                            if report["missing"]:
                                st.subheader("🆕 Missing from RAG")
                                for m in report["missing"]:
                                    col_m1, col_m2 = st.columns([4, 1])
                                    col_m1.write(
                                        f"📄 {m['name']} ({m['size_mb']:.1f} MB)"
                                    )
                                    if col_m2.button(
                                        "Ingest", key=f"ingest_{m['name']}"
                                    ):
                                        with st.spinner(f"Ingesting {m['name']}..."):
                                            if rag_manager.ingest_document(m["path"]):
                                                st.success(f"Ingested {m['name']}")
                            else:
                                st.success(
                                    "Everything in this directory is already indexed!"
                                )


if __name__ == "__main__":
    main()
