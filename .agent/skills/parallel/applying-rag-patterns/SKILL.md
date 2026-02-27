---
agents:
- none
category: parallel
description: Document chunking strategies, hybrid retrieval (semantic + keyword),
  reranking patterns, and citation/attribution
knowledge:
- none
name: applying-rag-patterns
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Rag Patterns

Document chunking strategies, hybrid retrieval (semantic + keyword), reranking patterns, and citation/attribution

Implement Retrieval-Augmented Generation with effective chunking, hybrid retrieval, reranking, and proper citation.

## Process

1. **Chunk documents** — Use recursive chunking for most docs (character, token, semantic, header-based).
2. **Set up retrieval** — Prefer hybrid search (semantic + keyword); single pass is acceptable for simple use cases.
3. **Rerank results** — Add cross-encoder or Cohere reranking for better relevance.
4. **Enable citations** — Format context with `[1]`, `[2]` markers and include source metadata.
5. **Wire pipeline** — Connect chunker → embeddings → retriever → reranker → prompt with context.


## Chunking Strategies Comparison

| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| Character-based | Simple text | Fast, predictable | Ignores structure |
| Recursive | General documents | Respects structure | May split sentences |
| Token-based | LLM context | Accurate sizing | Requires tokenizer |
| Semantic | Related content | Groups concepts | Slower, needs embeddings |
| Header-based | Markdown | Preserves hierarchy | Markdown only |

## Best Practices

- Use recursive chunking for most documents
- Overlap chunks by 10–20% to preserve context
- Chunk size: 500–1000 chars for general use; adjust for model context
- Use semantic chunking for conceptual grouping
- Combine multiple retrieval methods (hybrid search)
- Rerank results for better relevance
- Always include source citations
- Store metadata (source, page, timestamp) with chunks

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No chunk overlap | Use 10–20% overlap |
| Too large chunks | Keep under model context limit |
| Ignoring document structure | Use header-aware chunking |
| Single retrieval method | Use hybrid search |
| No reranking | Add reranking step |
| Missing citations | Always include source metadata |
| No metadata preservation | Pass metadata through pipeline |

## Resources

- **TROUBLESHOOTING.md** — Common issues (poor retrieval, slow indexing, hallucination, OOM, empty results)
- **scripts/verify.py** — Run `python scripts/verify.py --project-dir .` to check RAG best practices
- **scripts/analyze.py** — Run `python scripts/analyze.py --file doc.txt --chunk-size 1000 --overlap 200` for chunk analysis
- **examples/basic_retriever/** — Minimal RAG with ChromaDB
- Related: `retrieving-advanced`, `knowledge-graphs`, `memory-management`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
