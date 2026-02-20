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
- Active Qdrant vector store with indexed documents (running via Docker).
- FastMCP RAG Server must be actively running via `scripts/mcp/servers/rag/start_rag_server.bat` (exposing SSE on port 8000).
- Knowledge of the target ebook library structure.

## When to Use
- When answering complex technical or domain-specific questions.
- When grounding responses in project-specific documentation or ingested ebooks.

## Process
0.  **Initialize State**:
    - Before beginning, create an internal memory buffer (`rag_search_state`) to accumulate all relevant retrieved information.
1.  **Retrieve (Formulate Query & Search)**:
    - Formulate a precise, domain-specific search query based on the user's need.
    - **TOC Reconnaissance (Optional but Recommended)**: Every ingested eBook has a deterministic outline injected into the vector store. If you need to understand the broad structure of the book before deep diving, execute the TOC retrieval script: `python "scripts/get_rag_toc.py" "keyword or title"` (e.g. "Russell"). This returns a clean map of the book.
    - Execute the native retrieval script: `python "scripts/search_rag.py" "your precise query"`.
    - Wait for the JSON response containing the retrieved contextual chunks.
2.  **Grade (Evaluate Relevance)**:
    - Critically analyze the returned text chunks. Do they actually contain the factual information needed to answer the user's question?
    - If a chunk is **highly relevant**, append its contents to your `rag_search_state`.
    - If the context is **irrelevant or missing**, discard it.
3.  **Adapt (Rewrite or Fallback)**:
    - If the first query failed or only partially answered the larger question, reformulate the query using different keywords, synonyms, or a broader concept.
    - Run the retrieval script again with the new query and repeat steps 1 & 2 to build the state.
    - If multiple local retrieval attempts fail to find the answer, you **must fallback** to a standard web search (e.g., using Tavily or direct web tools) to find the answer externally, appending that to the state.
4.  **Synthesize**:
    - Once your `rag_search_state` contains sufficient information to fully address the user prompt, stop searching.
    - Ground your final answer strictly in the accumulated facts provided by the state.

## Level 3 Resources

### Scripts
- `scripts/search_rag.py`: Primary CLI utility to query the RAG via the active SSE endpoint.
  - Usage: `python "scripts/search_rag.py" "your question"`
  - Note: This streams raw JSON natively to standard out using UTF-8, making it safe and easy for you to parse.
- `scripts/get_rag_toc.py`: Secondary CLI utility to directly fetch the Table of Contents of a specific book.
  - Usage: `python "scripts/get_rag_toc.py" "book title or keyword"`

### References
- `references/agentic-logic.md`: Breakdown of the Retrieve -> Grade -> Adapt decision tree.

## Important Rules
- **Maintain Accumulative State**: Do not overwrite previous contextual discoveries. You are the orchestrator. You MUST accumulate relevant information across multiple searches before attempting to answer complex queries.
- **Agentic Loop is Mandatory**: You MUST grade the results yourself and adapt if the search fails. Do not blindly return bad context.
- **Context Integrity**: Respect the narrative context provided by the chunks. Do not hallucinate outside the given text unless explicitly falling back to web search.

## Best Practices
- **Parent Retrieval**: Always retrieve parent chunks rather than small segments for better LLM grounding.
- **Thresholding**: The `AgenticRAG` system uses normalized keyword matching for relevance grading.
- **Query Refinement**: If results are poor, refine the query to be more specific to the domain terms found in the library.
