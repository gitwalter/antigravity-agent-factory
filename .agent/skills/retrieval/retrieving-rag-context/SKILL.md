---
name: retrieving-rag-context
description: Specialized skill for retrieving rag context
type: skill
version: 1.0.0
category: retrieval
agents: [python-ai-specialist, ai-app-developer]
knowledge: [best-practices.json]
tools: ["local-faiss", "local-faiss-mcp"]
related_skills: [skill-generation]
templates: ["none"]
---
# Retrieving Rag Context

Process for querying the Qdrant vector store to provide rich context for AI responses using Parent-Child retrieval.

## Prerequisites
- Active Qdrant vector store with indexed documents.
- `antigravity-rag` MCP server active.
- Knowledge of the target ebook library structure.

## When to Use
- When answering complex technical or domain-specific questions.
- When grounding responses in project-specific documentation or ingested ebooks.

## Process
1.  **Formulate Query**: Create a descriptive query for semantic search.
2.  **Execute Search**: Call `@tool mcp_antigravity-rag_search_library`.
3.  **Synthesize**: Use the returned parent chunks (which provide full paragraphs/sections) to ground the answer.

## Important Rules
- **Tool Primacy**: Always use the `@tool mcp_antigravity-rag_search_library` for queries.
- **Context Integrity**: Respect the narrative context provided by the parent chunks.
- **No External LLM for Retrieval**: The retrieval is performed natively on CPU using FastEmbed and Qdrant.

## Best Practices
- **Parent Retrieval**: Always retrieve parent chunks rather than small segments for better LLM grounding.
- **Thresholding**: Set a similarity threshold of 0.7 to avoid hallucinating from irrelevant noise.
- **Keyword Integration**: Combine semantic search with keyword filtering for highly technical queries.
