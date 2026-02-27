---
agents:
- none
category: parallel
description: Tactical Blueprint for Retrieval-Augmented Generation (RAG) systems.
  Focuses on document ingestion, semantic retrieval, reranking, and citation truth.
knowledge:
- none
name: engineering-rag-systems
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Capability Manifest: RAG Engineering Manual

This blueprint provides the **procedural truth** for engineering high-fidelity RAG systems that prioritize retrieval precision and fact-based "Truth" in the Antigravity Agent Factory.

## Operational Environment

- **Embedding Models**: OpenAI `text-embedding-3-small` (Cost-efficient) / `large` (Precision).
- **Vector Stores**: PGVector (Enterprise), ChromaDB (Agile/Local).
- **Reranker**: Cohere Rerank / BGE-Reranker (Mandatory for high-noise contexts).

## Process

Follow these procedures to engineer high-fidelity RAG systems:

### Procedure 1: Document Ingestion (The Ingestion Truth)
Execute these steps to ensure contextual integrity:
1.  **Partitioning**: Use `Unstructured` or `LangChain` loaders with `mode="elements"` to preserve metadata (headers, page numbers, tables).
2.  **Chunking Strategy**:
    - *Default*: Recursive Character Text Splitting (1000 chars, 200 overlap).
    - *Expert*: Semantic Chunking (split by AI-detected meaning boundaries).
3.  **Indexing**: Always include a `source_id` and `timestamp` in the metadata to enable the "Chain of Truth" (Citations).

### Procedure 2: Hybrid Retrieval Logic
1.  **Step 1: Semantic Search**: Retrieve top-K candidates using Vector Similarity (Cosine).
2.  **Step 2: Keyword Search**: Retrieve top-K candidates using BM25 for precise term matching.
3.  **Step 3: Reciprocal Rank Fusion (RRF)**: Merge results to provide a balanced "Truth" candidate list.

### Procedure 3: The Reflection & Citation Gate
1.  **Retrieve**: Get candidates.
2.  **Rerank**: Use a `Cross-Encoder` to select the top 3-5 most relevant chunks.
3.  **Generate**: LLM answers *only* using the provided context.
4.  **Audit**: Mandatory check for citations. If the response makes a claim not present in the context, regenerate or flag as "Unknown."

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Lost in Middle** | Context window overflow or LLM attention dilution. | Implement "Long-Context" Reranking (Cross-Encoder); reduce top-K; use "Map-Reduce" or "Refine" chain types. |
| **Zero Retrieval** | Query-Index embedding mismatch. | Implement **Query Expansion** (HyDE or Multi-Query); lower the similarity threshold; check index metadata filters. |
| **Hallucinated Citations** | LLM using internal knowledge over context. | Tighten the System Prompt; use "No-Self-Knowledge" guardrails; implement a secondary "Citation Verification" node. |

## Idiomatic Code Patterns (The Gold Standard)

### The "Truthful" Retrieval Pipe
```python
def get_hybrid_retriever(vectorstore, documents):
    return EnsembleRetriever(
        retrievers=[
            vectorstore.as_retriever(search_kwargs={"k": 5}),
            BM25Retriever.from_documents(documents)
        ],
        weights=[0.5, 0.5]
    )
```

### The "Observable" Citation Prompt snippet
```text
CONTEXT:
---
{context}
---

INSTRUCTION:
Answer the user query ONLY using the context above.
For every claim, provide a bracketed citation pointing to the source id, e.g., [source_123].
If the context is insufficient, explicitly state "I do not have enough specific truth to answer this."
```

## Prerequisites

| Action | Command |
| :--- | :--- |
| Inspect Index | `vector_db.get(where={"source": "file_a"})` |
| Benchmarking | `ragas-evaluate` (Check Faithfulness, Relevancy) |
| Local Vector DB | `chroma run --path ./db` |

## When to Use
Use this blueprint whenever building Q&A systems over documents, semantic search engines, or any agentic system that requires "Grounding" in external data. It is the authoritative source for "How we retrieve truth" vs "What RAG is."


## Best Practices

- Follow the system axioms (A1-A5)
- Ensure all changes are verifiable
- Document complex logic for future maintenance
