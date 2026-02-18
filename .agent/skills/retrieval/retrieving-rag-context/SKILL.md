---
name: retrieving-rag-context
description: Specialized skill for retrieving rag context
type: skill
version: 1.1.0
category: retrieval
agents: [python-ai-specialist, ai-app-developer]
knowledge: [best-practices.json]
tools: ["antigravity-rag"]
related_skills: [ingesting-rag-content, inspecting-rag-catalog, skill-creator]
templates: ["none"]
---

# Retrieving RAG Context

Process for querying the Qdrant vector store to provide rich context for AI responses using an **Agentic RAG** approach (Retrieve -> Grade -> Adapt).

## Prerequisites
- Active Qdrant vector store with indexed documents.
- `antigravity-rag` MCP server active (configured in `c:\Users\wpoga\.gemini\antigravity\mcp_config.json`).
- Knowledge of the target ebook library structure.

## When to Use
- When answering complex technical or domain-specific questions.
- When grounding responses in project-specific documentation or ingested ebooks.

## Process
1.  **Formulate Query**: Create a descriptive query for semantic search.
2.  **Execute Agentic Search**: Call `@tool mcp_antigravity-rag_search_library`.
3.  **Handle Fallback**: The server will automatically use the `AgenticRAG` loop (LangGraph) to grade relevance and fallback to web search (Tavily) if local context is insufficient.
4.  **Synthesize**: Use the returned parent chunks (which provide full paragraphs/sections) to ground the answer.

## Level 3 Resources

### Scripts
- **NONE**: This skill relies exclusively on the `antigravity-rag` MCP server.
- `scripts/ai/rag/agentic_rag.py`: The system-wide orchestration logic for relevance grading (backend use only).

### References
- `references/agentic-logic.md`: Breakdown of the Retrieve -> Grade -> Adapt decision tree.

## Important Rules
- **Agentic Priority**: Prefer `@tool mcp_antigravity-rag_search_library` over lower-level semantic search as it includes relevance grading.
- **Context Integrity**: Respect the narrative context provided by the parent chunks.
- **Local vs Web**: Pay attention to the "NOTE" in the tool output if web search was triggered.

## Best Practices
- **Parent Retrieval**: Always retrieve parent chunks rather than small segments for better LLM grounding.
- **Thresholding**: The `AgenticRAG` system uses normalized keyword matching for relevance grading.
- **Query Refinement**: If results are poor, refine the query to be more specific to the domain terms found in the library.
