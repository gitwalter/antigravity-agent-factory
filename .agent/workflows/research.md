---
description: Multi-source research workflow using RAG, web search, docs, and GitHub
---

# /research — Multi-Source Research Workflow

Route knowledge questions to the right MCP tool and skill based on the type of query.

**Version:** 1.0.0

## Trigger Conditions

This workflow is activated when:
- A research or knowledge question is asked.
- The user needs to find information from RAG, web, docs, or code repos.
- User requests "research", "look up", "find out", or "what do we know about".

**Trigger Examples:**
- "What's in our RAG library?"
- "Research best practices for prompt engineering"
- "Look up the LangChain docs for retrieval chains"
- "What do we know about multi-agent orchestration?"

## Decision Matrix

| Question Type | Skill | MCP Server | Tool |
|---|---|---|---|
| "What's in our RAG/library?" | `inspecting-rag-catalog` | `antigravity-rag` | `list_library_sources` |
| Domain/ebook question | `retrieving-rag-context` | `antigravity-rag` | `search_library` |
| Current events / web topic | *(direct)* | `tavily` | `tavily-search` |
| Library/framework docs | *(direct)* | `deepwiki` or `docs-langchain` | `read_wiki_contents` |
| Read a specific URL | *(direct)* | `fetch` | `fetch` |
| Code/repo exploration | `operating-github` | GitHub MCP | repo tools |
| Complex multi-source | `researching-first` | multiple | cascading |

## Steps

### 1. Classify the Query
Determine which source is most appropriate:
- **Catalog query** ("what do we have?", "list sources") → Step 2a
- **Ingested content query** (topics matching RAG library) → Step 2b
- **Web/current topic** (news, trends, general knowledge) → Step 2c
- **Library/framework docs** ("how does X work in LangChain?") → Step 2d
- **Code/repo** ("what's in repo X?") → Step 2e
- **Complex/multi-source** (needs research methodology) → Step 2f

### 2a. Inspect RAG Catalog
// turbo
Use the `inspecting-rag-catalog` skill:
```
@tool mcp_antigravity-rag_list_library_sources
```

### 2b. Query RAG Library
Use the `retrieving-rag-context` skill:
```
@tool mcp_antigravity-rag_search_library query="<semantic query>"
```
The Agentic RAG system will grade relevance and fallback to web search if needed.

### 2c. Web Research
Use Tavily MCP for web search:
```
@tool mcp_tavily_tavily-search query="<search query>"
```
Optionally extract full content from results:
```
@tool mcp_tavily_tavily-extract urls=["<url>"]
```

### 2d. Documentation Lookup
For framework/library docs, try in order:
1. **LangChain docs** (if LangChain-related):
   ```
   @tool mcp_docs-langchain (if enabled)
   ```
2. **DeepWiki** (for any open-source library):
   ```
   @tool mcp_deepwiki_read_wiki_contents (if enabled)
   ```
3. **Fetch** (fallback — read any URL directly):
   ```
   @tool mcp_fetch_fetch url="<docs-url>"
   ```

### 2e. GitHub / Code Research
Use the `operating-github` skill for repository exploration and code search.

### 2f. Full Research Pipeline
Invoke the `researching-first` skill for complex topics requiring multiple sources:
1. **Local first**: Search RAG via `search_library`
2. **Grade relevance**: If insufficient, expand to web
3. **Web search**: Tavily for current information
4. **Docs**: DeepWiki/LangChain docs for technical depth
5. **Document findings**: Create knowledge file
6. **Synthesize**: Combine all sources with citations

## Notes
- Always try **local RAG first** for domain topics before escalating to web.
- `docs-langchain` and `deepwiki` are currently disabled in MCP config. Enable them in `mcp_config.json` when needed.
- For the full research pipeline, time-box to avoid analysis paralysis.
