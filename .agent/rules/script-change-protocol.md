---
title: Script Change Protocol
scope: all agents modifying CLI scripts
axioms: [A1, A3, A5]
---

# Script Change Protocol

**When**: After modifying any script's CLI interface (adding/changing/removing commands, parameters, or flags).

**What to do**:

1. **Run sync_script_registry.py** to update Memory MCP with the new interface:
   ```powershell
   conda run -p D:\Anaconda\envs\cursor-factory python scripts/maintenance/sync_script_registry.py
   ```

2. **Update relevant skills** if the change affects WHEN or WHY a command is used
   - Skills describe **WHAT** to do and **WHEN** to use it
   - Memory MCP stores **HOW** (exact syntax, parameters, examples)
   - Skills should include: *"Query memory MCP for current command syntax before running"*

3. **Update knowledge catalogs** if the change adds new capabilities
   - e.g., `rag-knowledge-catalog.json` for RAG script changes

## Separation of Concerns

| Layer | Stores | Example |
|-------|--------|---------|
| **Skill** | Intent (WHAT/WHEN) | "Use when ingesting PDFs into RAG" |
| **Memory MCP** | Execution (HOW) | "ingest <file> [--force]" |
| **Knowledge** | Context (WHY) | "Hash dedup prevents wasted compute" |
