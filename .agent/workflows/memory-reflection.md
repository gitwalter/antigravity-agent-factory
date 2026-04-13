---
description: Trigger the Cognitive Reflection Engine to synthesize new insights from episodic logs.
version: "1.0.0"
---
# Memory Reflection Workflow (`/memory-reflection`)

> **Version:** 1.0.0 | **Trigger Workflow:** `/memory-reflection`

This workflow initiates the automated distillation pipeline. It parses recent session logs, distills observations into cognitive insights, and prunes decayed memory from the vector index.

## Trigger Conditions

Use this workflow when:
- A session has ended and new episodic logs exist in `logs/memory/` or `.gemini/extensions`.
- You want to promote distilled session insights into the `memory_semantic` collection.
- Knowledge base feels stale or an upcoming task would benefit from remembered patterns.
- Running the `/knowledge-bridge-workflow` after significant implementation work.

**Trigger Examples:**
- `/memory-reflection` — after completing a multi-step implementation session.
- `/memory-reflection` — before starting a new sprint to prime semantic context.


## Prerequisites

- The memory backend (Qdrant Docker and SQLite) must be running.
- Recent IDE sessions must have logged episodic events to the `.gemini/extensions` hooks or `logs/memory/`.

## Steps

### Step 1: Collect Experience Logs
We first read unstructured IDE hook JSONL output and transform it into Exact SQLite memory + Synthesized Summaries.

// turbo
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python "scripts/memory/memory_cli.py" run collect
```

### Step 2: Trigger Reflection Engine
We execute the multi-document pattern matching to identify structural insights and promote them to Semantic Knowledge. This also clears out decayed nodes.

// turbo
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python "scripts/memory/memory_cli.py" run reflect
```

### Step 3: Reindex Procedural Memory (Optional)
If new workflows or skills were discovered during the reflection, re-index them back into the `COLLECTION_PROCEDURAL` mapping.

// turbo
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python "scripts/memory/memory_cli.py" run index
```

## Review
Review the output to ensure the memory DB was updated successfully. You can run manual checks via the CLI:
```powershell
# E.g. search the latest semantic entries
conda run -p D:\Anaconda\envs\cursor-factory python "scripts/memory/memory_cli.py" vector memory_semantic "What did we learn today?"
```
