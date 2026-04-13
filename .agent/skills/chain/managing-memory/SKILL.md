---
agents:
- python-ai-specialist
category: chain
description: 'Manage the Antigravity Dual-Storage Memory system (SQL + Vector) and implement cognitive lifecycle hooks.'
knowledge:
- cognitive-memory-patterns.json
name: managing-memory
related_skills:
- None
templates:
- none
tools:
- search_memory_entity
- search_memory_semantic
- search_memory_procedural
- search_memory_summary
- prepare_context
- add_memory_entity
- add_memory_summary
- add_memory_episodic
- propose_memory_semantic
- propose_memory_procedural
- propose_memory_toolbox
type: skill
version: 2.0.0
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---
# Managing Memory (Antigravity Architecture)

Automated Cognitive Memory System - Conversation, Long-term, and Episodic backend implementations inside the framework.

Implement memory systems for agents using the standard Dual-Storage approach:
- SQL Storage (SQLite) for exact-match sequences.
- Vector Storage (Qdrant Docker) for semantic, probabilistic patterns.

## Process

1. Establish memory schema mapping (Semantic, Procedural, Toolbox, Entity, Summary).
2. Wire up the IDE hooks (`sessionStart`, `sessionEnd`).
3. Leverage background reflection engines.

### Step 1: Querying SQL Database (Episodic Chat/Tool Logs)

```python
from scripts.memory.memory_database import MemoryDatabase

db = MemoryDatabase()

# Fetch history
history = db.get_chat_history(thread_id="session_123", limit=10)
for msg in history:
    print(f"[{msg['role']}] {msg['content']}")

# Fetch tool logs
tools = db.get_tool_logs(thread_id="session_123", limit=5)
```

### Step 2: Querying Semantic Memory (Vector Database)

```python
from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_SEMANTIC

store = get_memory_store()

# Retrieve distilled knowledge
results = store.search("architecture patterns", memory_type=COLLECTION_SEMANTIC, k=3)
for result in results:
    print(result.content)
```

### Step 3: Extracting Entities

```python
from scripts.memory.entity_store import get_entity_store

entity_store = get_entity_store()

# Extract and persist mentions
entity_store.extract_and_store_entities(
    text="The user deployed to the AWS staging cluster.",
    source_context="Deploy script discussion"
)
```

### Step 4: Indexing Procedural Memory

To ensure agents have access to workflows and skills, trigger the parent-child chunk indexer:

```python
from scripts.memory.procedural_indexer import ProceduralIndexer

indexer = ProceduralIndexer()
indexer.index_all() # Indexes .agent/workflows and .agent/skills
```

### Step 5: Using RAG MCP Tools (Recommended for Agents)

While direct Python imports are available for infrastructure scripts, **Agents should prioritize the `qdrant-rag` MCP tools** for better isolation and observability.

#### Instant Persistence (Entity/Summary/Episodic)
Use `add_memory_*` tools for facts that are verified and don't require structural induction.
```python
# Example Tool Call (Logical)
add_memory_entity(content="User preferred OS: Windows", metadata={"priority": "high"})
```

#### Induction Proposals (Semantic/Procedural/Toolbox)
Use `propose_memory_*` for new rules, workflows, or scripts. These go into a "Pending" queue for user approval (A2).
```python
# Example Tool Call (Logical)
propose_memory_semantic(
    content="Always use 'mcp_infra' for local mcp servers to avoid shadowing.",
    reasoning="Prevents ImportError conflicts with the official mcp library."
)
```

#### Unified Context Retrieval
Use `prepare_context` to fetch a fused view of all memory tiers for a given query.
```python
# Example Tool Call (Logical)
context = prepare_context(query="how to debug mcp servers")
```

## Memory Types

| Type | Human Analogy | Storage | Retrieval |
|--|--|--|--|
| Conversational | Short-term memory | SQL (`chat_history`) | Exact Match |
| Tool Log | Audit trail | SQL (`tool_logs`) | Exact Match |
| Semantic | Long-term facts | Vector DB (`memory_semantic`) | Semantic Search |
| Procedural | Learned paths | Vector DB (`memory_procedural`) | Semantic Search |
| Toolbox | Capabilities | Vector DB (`memory_toolbox`) | Semantic Search |
| Entity | Episodic entities | Vector DB (`memory_entity`) | Semantic Search |
| Summary | Condensed session | Vector DB (`memory_summary`) | Semantic Search |

## Relational Lifecycle

1. **Extraction (SessionEnd)**: Raw logs go to SQLite exact tiers. A distilled summary is pushed to `memory_summary`.
2. **Consolidation**: `ReflectionEngine` evaluates multiple summaries, finding structural trends and converting them to `memory_semantic`.
3. **Decay**: Outdated or irrelevant summaries are pruned (Weibull decay) via `GovernanceGates`.

## When to Use
This skill should be used when interfacing with the dual-storage cognitive database.

## Prerequisites
- The environment must have Qdrant running on Docker port 6333.
- Access to the Python scripting environments in `/scripts/memory`.

## Best Practices
- **Always use full collection names**: Use `COLLECTION_SEMANTIC`, `COLLECTION_PROCEDURAL` etc. from `memory_config.py` instead of short aliases.
- **Require user approval**: Never store observations to semantic memory without a user-validated proposal (A2: User Primacy).
- **Close clients**: Always call `store.close()` after test usage to release Windows file handles.
- **Isolate test state**: Clear Qdrant collections before each test to prevent cross-test pollution.
- **Check dedup gate**: The 0.95 similarity threshold prevents duplicate semantic memories — avoid storing nearly identical content.
- **Prevent Namespace Shadowing**: Never name local directories using common library names (e.g., `mcp`, `json`, `path`) if the project root is in `sys.path`. Use suffixes like `_infra` or `_custom` to prevent `ImportError` collisions.
- **Warmup Waiting**: When using the RAG server in tests, wait for the `_store_ready` event or provide a sufficient timeout to allow the embedding models to load in the background.
