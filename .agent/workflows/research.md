---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for research. Standardized for IDX Visual Editor.
domain: universal
name: research
steps:
- actions: []
  agents:
  - '@Architect'
  goal: ''
  name: Context Engineering (Memory-First)
  skills: []
  tools: []
- actions:
  - "**Structural/Context query** (\"what is X?\", \"how does X relate to Y?\") \u2192\
    \ **Always Phase 0 first**"
  - "**Catalog query** (\"what do we have?\", \"list sources\") \u2192 Step 2a"
  - "**Ingested content query** (topics matching RAG library) \u2192 Step 2b"
  - "**Web/current topic** (news, trends, general knowledge) \u2192 Step 2c"
  - "**Library/framework docs** (\"how does X work in LangChain?\") \u2192 Step 2d"
  - "**Code/repo** (\"what's in repo X?\") \u2192 Step 2e"
  - "**Complex/multi-source** (needs researching-first methodology) \u2192 Step 2f"
  - Always try **local RAG first** for domain topics before escalating to web.
  - '`docs-langchain` and `deepwiki` are currently disabled in MCP config. Enable
    them in `mcp_config.json` when needed.'
  - For the full researching-first pipeline, time-box to avoid analysis paralysis.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - '@Architect'
  goal: ''
  name: Classify the Query
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Multi-Source Research Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for deep research across multiple local and external sources. Standardized for IDX Visual Editor.

## Trigger Conditions
- Complex user query requiring extensive research or fact-finding.
- Need to synthesize information from various sources (documentation, code, web).
- User request: `/research`.

**Trigger Examples:**
- "Research the best practices for implementing multi-agent debate protocols."
- "Conduct a deep dive into the 'LangGraph' documentation for POC orchestration."

## Phases

### 1. Context Engineering (Memory-First)
- **Agents**: `@Architect`

### 2. Classify the Query
- **Agents**: `@Architect`
- **Structural/Context query** ("what is X?", "how does X relate to Y?") → **Always Phase 0 first**
- **Catalog query** ("what do we have?", "list sources") → Step 2a
- **Ingested content query** (topics matching RAG library) → Step 2b
- **Web/current topic** (news, trends, general knowledge) → Step 2c
- **Library/framework docs** ("how does X work in LangChain?") → Step 2d
- **Code/repo** ("what's in repo X?") → Step 2e
- **Complex/multi-source** (needs researching-first methodology) → Step 2f
- Always try **local RAG first** for domain topics before escalating to web.
- `docs-langchain` and `deepwiki` are currently disabled in MCP config. Enable them in `mcp_config.json` when needed.
- For the full researching-first pipeline, time-box to avoid analysis paralysis.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
