# Parent-Child RAG Architecture

The Antigravity RAG system uses a **Parent-Child** strategy to balance retrieval granularity with context richness.

## Core Concepts

1.  **Parent Chunks**: Multi-paragraph sections (approx. 2000 characters) that provide sufficient narrative context for the LLM.
2.  **Child Chunks**: Small segments (approx. 400 characters) created from parents. These are embedded and stored in the vector database.
3.  **Retrieval Loop**:
    *   The system searches for relevant **Child Chunks**.
    *   It resolves the found children to their **Parent Chunks** using a persistent docstore.
    *   The LLM receives the **Parent Chunks** as ground truth.

## Why it matters
- **High Recall**: Small chunks are easier to match semantically.
- **Narrative Integrity**: Large parent chunks prevent the "silo" effect where the LLM only sees a single sentence without context.
- **Efficiency**: Only child embeddings are stored in the vector index, keeping the search space optimized.

## Qdrant Integration
- **Collection Name**: `ebook_library`
- **Metadata**: Stores absolute paths and page numbers for traceability.
