---
agents:
- none
category: chain
description: LangGraph state schemas, reducers, checkpointing, and persistence
knowledge:
- none
name: managing-state
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# State Management

LangGraph state schemas, reducers, checkpointing, and persistence

Manage agent state in LangGraph workflows - schemas, reducers, and persistence.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Define State Schema

```python
from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """State schema for the agent."""
    # Messages with reducer (accumulates)
    messages: Annotated[list, add_messages]

    # Simple fields (overwrite on update)
    current_step: str
    iteration: int

    # Complex nested state
    context: dict
    results: list
```

### Step 2: Custom Reducers

```python
from operator import add
from typing import Annotated

def merge_dicts(left: dict, right: dict) -> dict:
    """Merge two dictionaries, right overwrites left."""
    return {**left, **right}

def append_unique(left: list, right: list) -> list:
    """Append only unique items."""
    return list(set(left + right))

class AdvancedState(TypedDict):
    # Accumulate messages
    messages: Annotated[list, add_messages]

    # Accumulate numeric values
    token_count: Annotated[int, add]

    # Merge dictionaries
    metadata: Annotated[dict, merge_dicts]

    # Unique list items
    visited_nodes: Annotated[list[str], append_unique]

    # Simple overwrite
    status: str
```

### Step 3: State Updates in Nodes

```python
from langgraph.graph import StateGraph

async def process_node(state: AgentState) -> dict:
    """Node that updates state."""
    # Return only the fields to update
    return {
        "current_step": "processing",
        "iteration": state["iteration"] + 1,
        "context": {**state["context"], "processed": True}
    }

async def accumulate_node(state: AdvancedState) -> dict:
    """Node using reducers."""
    return {
        "token_count": 150,  # Will be added to existing
        "metadata": {"source": "api"},  # Will be merged
        "visited_nodes": ["accumulate"],  # Will be appended uniquely
    }
```

### Step 4: Checkpointing with MemorySaver

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

# Create checkpointer
checkpointer = MemorySaver()

# Build graph
graph = StateGraph(AgentState)
graph.add_node("process", process_node)
graph.add_node("decide", decide_node)
graph.set_entry_point("process")
graph.add_edge("process", "decide")
graph.add_conditional_edges("decide", route_function, {"continue": "process", "end": END})

# Compile with checkpointing
app = graph.compile(checkpointer=checkpointer)

# Run with thread ID for persistence
config = {"configurable": {"thread_id": "task_001"}}
result = await app.ainvoke(initial_state, config)

# Resume later with same thread ID
resumed_result = await app.ainvoke(None, config)
```

### Step 5: Redis Checkpointer

```python
from langgraph.checkpoint.base import BaseCheckpointSaver
import redis
import json
from datetime import datetime

class RedisCheckpointer(BaseCheckpointSaver):
    """Redis-backed checkpointer for distributed systems."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
        self.ttl = 86400 * 7  # 7 days

    def _key(self, thread_id: str, checkpoint_id: str) -> str:
        return f"checkpoint:{thread_id}:{checkpoint_id}"

    def get(self, config: dict) -> dict | None:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = config["configurable"].get("checkpoint_id", "latest")

        if checkpoint_id == "latest":
            # Get most recent
            keys = self.client.keys(f"checkpoint:{thread_id}:*")
            if not keys:
                return None
            latest_key = sorted(keys)[-1]
            data = self.client.get(latest_key)
        else:
            data = self.client.get(self._key(thread_id, checkpoint_id))

        return json.loads(data) if data else None

    def put(self, config: dict, checkpoint: dict) -> dict:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = datetime.now().isoformat()

        key = self._key(thread_id, checkpoint_id)
        self.client.setex(key, self.ttl, json.dumps(checkpoint))

        return {"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}}

# Use Redis checkpointer
redis_checkpointer = RedisCheckpointer()
app = graph.compile(checkpointer=redis_checkpointer)
```

### Step 6: PostgreSQL Checkpointer

```python
from langgraph.checkpoint.postgres import PostgresSaver
import asyncpg

# Async PostgreSQL checkpointer
async def create_postgres_checkpointer():
    conn = await asyncpg.connect("postgresql://user:pass@localhost/db")

    # Create table if not exists
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            thread_id TEXT,
            checkpoint_id TEXT,
            state JSONB,
            created_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (thread_id, checkpoint_id)
        )
    """)

    return PostgresSaver(conn)

# Use
checkpointer = await create_postgres_checkpointer()
app = graph.compile(checkpointer=checkpointer)
```

### Step 7: State Visualization

```python
def visualize_state(state: AgentState) -> str:
    """Create visual representation of state."""
    lines = [
        "┌─ Agent State ─────────────────┐",
        f"│ Step: {state['current_step']:<22} │",
        f"│ Iteration: {state['iteration']:<17} │",
        f"│ Messages: {len(state['messages']):<18} │",
        "├───────────────────────────────┤",
    ]

    for key, value in state.get('context', {}).items():
        lines.append(f"│ {key}: {str(value)[:20]:<20} │")

    lines.append("└───────────────────────────────┘")
    return "\n".join(lines)

# In node
async def debug_node(state: AgentState) -> dict:
    print(visualize_state(state))
    return {}
```

## State Patterns

| Pattern | Use Case |
|---------|----------|
| Message Accumulation | Chat history |
| Counter Reducer | Token counting, iterations |
| Dict Merge | Metadata aggregation |
| Set Reducer | Unique items tracking |
| Overwrite | Current status, step |

## Checkpointer Comparison

| Backend | Use Case | Pros | Cons |
|---------|----------|------|------|
| MemorySaver | Development | Fast, simple | Not persistent |
| Redis | Distributed | Fast, TTL | Memory-bound |
| PostgreSQL | Production | Durable, queryable | Slower |
| SQLite | Local prod | Durable, simple | Single node |

## Best Practices

- Define clear state schemas with TypedDict
- Use appropriate reducers for each field
- Implement checkpointing for production
- Use thread IDs for multi-user scenarios
- Clean up old checkpoints periodically
- Validate state transitions

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Mutable state | Return new state dict |
| No checkpointing | Add MemorySaver minimum |
| Unbounded state | Compress/prune old data |
| No schema | Use TypedDict |

## Related

- Knowledge: `{directories.knowledge}/state-patterns.json`
- Skill: `langgraph-agent-building`
- Skill: `memory-management`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
