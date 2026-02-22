---
agents:
- python-ai-specialist
- ai-app-developer
- master-system-orchestrator
category: management
description: Master skill for orchestrating and utilizing the full MCP ecosystem (Tavily,
  RAG, Memory, Sequential Thinking)
name: orchestrating-mcp
related_skills:
- skill-creator
- retrieving-rag-context
tools:
- tavily_*
- mcp_rag_*
- mcp_memory_*
- mcp_sequential-thinking_*
- mcp_google-contacts_*
- mcp_doc-tools_*
type: skill
version: 1.1.0
---

# MCP Orchestration

This skill governs the strategic selection and execution of MCP tools across the entire factory ecosystem. It ensures that agents use the most efficient communication and retrieval patterns for the task at hand.

## Process

Follow these procedures to implement the capability:

## When to Use

This skill should be used when completing tasks related to orchestrating mcp.

## Master Tool Reference (Fully Grounded)

### 1. Web Intelligence (Tavily)
- **Search**: `mcp_tavily_tavily_search(query, search_depth, max_results)` - Semantic web search.
- **Research**: `mcp_tavily_tavily_research(input)` - Multi-step research.
- **Extract**: `mcp_tavily_tavily_extract(urls, query)` - Clean markdown extraction.
- **Map**: `mcp_tavily_tavily_map(url)` - Domain sub-page discovery.
- **Crawl**: `mcp_tavily_tavily_crawl(url)` - Mass data harvesting.

### 2. Browser Automation (Playwright)
- **Navigation**: `mcp_playwright_browser_navigate(url)`, `mcp_playwright_browser_wait_for(text, time)`
- **Interaction**: `mcp_playwright_browser_click(ref)`, `mcp_playwright_browser_type(ref, text)`, `mcp_playwright_browser_drag(startRef, endRef)`, `mcp_playwright_browser_hover(ref)`
- **Forms**: `mcp_playwright_browser_fill_form(fields)`, `mcp_playwright_browser_select_option(ref, values)`, `mcp_playwright_browser_file_upload(paths)`
- **State**: `mcp_playwright_browser_snapshot()` (Accessibility tree), `mcp_playwright_browser_take_screenshot(type)`
- **Analysis**: `mcp_playwright_browser_evaluate(function)`, `mcp_playwright_browser_network_requests(includeStatic)`, `mcp_playwright_browser_console_messages(level)`
- **Tabs**: `mcp_playwright_browser_tabs(action, index)`

### 3. State & Knowledge (Memory & RAG)
- **Memory Graph**: `mcp_memory_read_graph()`, `mcp_memory_create_entities(entities)`, `mcp_memory_create_relations(relations)`, `mcp_memory_add_observations(observations)`, `mcp_memory_search_nodes(query)`, `mcp_memory_open_nodes(names)`
- **Ebook Library (RAG)**: `mcp_rag_search_library(query)`, `mcp_rag_get_ebook_toc(document_name)`, `mcp_rag_ingest_document(file_path)`, `mcp_rag_list_library_sources()`
- **Repo Intelligence**: `mcp_deepwiki_ask_question(repoName, question)`, `mcp_deepwiki_read_wiki_structure(repoName)`, `mcp_deepwiki_read_wiki_contents(repoName)`
- **Framework Docs**: `mcp_docs-langchain_SearchDocsByLangChain(query)`

### 4. Utilities (Fetch & Sequential Thinking)
- **Fetch**: `mcp_fetch_fetch(url, raw, max_length)` - Stateless HTTP retrieval.
- **Reasoning**: `mcp_sequential-thinking_sequentialthinking(thought, thoughtNumber, totalThoughts, nextThoughtNeeded)` - Structured problem solving.

---

## Workspace & Productivity Tools (Platform Specific)

### 5. Google Workspace (Gmail, Calendar, Contacts)
- **Gmail**: `mcp_gmail_list_messages(query, max_results)`, `mcp_gmail_get_message(message_id)`, `mcp_gmail_create_draft(to, subject, body)`, `mcp_gmail_send_message(to, subject, body)`
- **Calendar**: `mcp_google-calendar_calendar_list()`, `mcp_google-calendar_calendar_get_events(calendar_id, time_min, time_max)`, `mcp_google-calendar_calendar_create_event(calendar_id, summary, start, end)`
- **Contacts**: `mcp_google-contacts_list_contacts(name_filter)`, `mcp_google-contacts_search_contacts(query)`, `mcp_google-contacts_get_contact(identifier)`, `mcp_google-contacts_create_contact(given_name, family_name, email, phone)`

### 6. Document & Professional Tools
- **Doc Tools (Word)**: `mcp_doc-tools_create_document(filename, content)`, `mcp_doc-tools_edit_document(filename, actions)`, `mcp_doc-tools_read_document(filename)`
- **GDrive**: `mcp_gdrive_list_files(query)`, `mcp_gdrive_get_file_content(file_id)`
- **Excel**: `mcp_excel_write_data_to_excel(filepath, sheet_name, data)`, `mcp_excel_read_data_from_excel(filepath, sheet_name)`
- **LangSmith**: `mcp_langsmith_list_projects()`, `mcp_langsmith_fetch_runs(project_name, limit, page_number)`

## Best Practices
- **Grounding Priority**: Memory > RAG > Workspace (if applicable) > Tavily/Fetch.
- **Reasoning Integrity**: Always use `mcp_sequential-thinking_sequentialthinking` before complex multi-agent handoffs.
- **Cleanup**: Delete temporary files and drafts after use.


## Prerequisites

- Access to relevant project documentation
- Environmental awareness of the target stack
