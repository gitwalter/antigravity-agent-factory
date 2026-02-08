---
name: memory-management
description: Agent memory patterns - conversation, long-term, and backend implementations
type: skill
agents: [code-reviewer, test-generator]
knowledge: [memory-patterns.json]
---

# Memory Management Skill

Implement memory systems for agents - conversation history, long-term storage, and retrieval.

## When to Use

- Building conversational agents
- Maintaining context across sessions
- Storing and retrieving knowledge
- Implementing user preferences
- Building personalized experiences

## Prerequisites

```bash
pip install langchain-core redis chromadb
```

## Process

### Step 1: Conversation Memory (Short-term)

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# Simple in-memory history
history = InMemoryChatMessageHistory()
history.add_user_message("Hello, I'm Alice")
history.add_ai_message("Hi Alice! How can I help?")

# Access messages
messages = history.messages
```

### Step 2: Session-Based Memory

```python
from langchain_core.runnables.history import RunnableWithMessageHistory

# Session store
session_store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

# Wrap chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Use with session
result = await chain_with_memory.ainvoke(
    {"input": "Remember my name is Bob"},
    config={"configurable": {"session_id": "user_123"}}
)
```

### Step 3: Redis Memory Backend

```python
import redis
import json
from langchain_core.messages import messages_from_dict, messages_to_dict

class RedisMemory:
    """Redis-backed conversation memory."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
        self.ttl = 86400 * 7  # 7 days
    
    def _key(self, session_id: str) -> str:
        return f"memory:{session_id}"
    
    def add_messages(self, session_id: str, messages: list) -> None:
        key = self._key(session_id)
        existing = self.get_messages(session_id)
        all_messages = existing + messages
        
        self.client.setex(
            key,
            self.ttl,
            json.dumps(messages_to_dict(all_messages))
        )
    
    def get_messages(self, session_id: str) -> list:
        key = self._key(session_id)
        data = self.client.get(key)
        if data:
            return messages_from_dict(json.loads(data))
        return []
    
    def clear(self, session_id: str) -> None:
        self.client.delete(self._key(session_id))

# Use with RunnableWithMessageHistory
redis_memory = RedisMemory()

def get_redis_history(session_id: str):
    class RedisHistory:
        def __init__(self, session_id):
            self.session_id = session_id
        
        @property
        def messages(self):
            return redis_memory.get_messages(self.session_id)
        
        def add_messages(self, messages):
            redis_memory.add_messages(self.session_id, messages)
    
    return RedisHistory(session_id)
```

### Step 4: Long-Term Memory with Vector Store

```python
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime

class LongTermMemory:
    """Vector-based long-term memory for semantic retrieval."""
    
    def __init__(self, collection_name: str = "memories"):
        self.client = chromadb.PersistentClient(path="./memory_db")
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def store(self, user_id: str, content: str, metadata: dict = None) -> str:
        """Store a memory with semantic embedding."""
        memory_id = f"{user_id}_{datetime.now().isoformat()}"
        embedding = self.embedder.encode(content).tolist()
        
        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[{
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            }]
        )
        return memory_id
    
    def retrieve(self, user_id: str, query: str, n_results: int = 5) -> list[str]:
        """Retrieve relevant memories."""
        query_embedding = self.embedder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"user_id": user_id}
        )
        
        return results["documents"][0] if results["documents"] else []
    
    def forget(self, memory_id: str) -> None:
        """Delete a specific memory."""
        self.collection.delete(ids=[memory_id])

# Usage
ltm = LongTermMemory()
ltm.store("user_123", "User prefers Python over JavaScript")
ltm.store("user_123", "User works in fintech")

relevant = ltm.retrieve("user_123", "What programming language?")
```

### Step 5: Memory Compression

```python
from langchain_core.messages import SystemMessage

class MemoryCompressor:
    """Compress conversation history to fit context windows."""
    
    def __init__(self, llm, max_messages: int = 20):
        self.llm = llm
        self.max_messages = max_messages
    
    async def compress(self, messages: list) -> list:
        """Compress old messages into a summary."""
        if len(messages) <= self.max_messages:
            return messages
        
        # Split into old and recent
        cutoff = len(messages) - self.max_messages // 2
        old_messages = messages[:cutoff]
        recent_messages = messages[cutoff:]
        
        # Summarize old messages
        summary_prompt = f"""Summarize the key points from this conversation:
        
{self._format_messages(old_messages)}

Provide a concise summary capturing important context, user preferences, and decisions."""
        
        summary = await self.llm.ainvoke(summary_prompt)
        
        # Return compressed history
        return [
            SystemMessage(content=f"Previous conversation summary: {summary.content}"),
            *recent_messages
        ]
    
    def _format_messages(self, messages) -> str:
        return "\n".join(f"{m.type}: {m.content}" for m in messages)
```

### Step 6: Structured User Memory

```python
from pydantic import BaseModel
from typing import Optional
import json

class UserProfile(BaseModel):
    """Structured user profile for personalization."""
    user_id: str
    name: Optional[str] = None
    preferences: dict = {}
    facts: list[str] = []
    last_interaction: Optional[str] = None

class UserMemoryStore:
    """Store and retrieve structured user profiles."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def _key(self, user_id: str) -> str:
        return f"user_profile:{user_id}"
    
    def get(self, user_id: str) -> UserProfile:
        data = self.redis.get(self._key(user_id))
        if data:
            return UserProfile(**json.loads(data))
        return UserProfile(user_id=user_id)
    
    def save(self, profile: UserProfile) -> None:
        self.redis.set(self._key(profile.user_id), profile.model_dump_json())
    
    def update_preference(self, user_id: str, key: str, value) -> None:
        profile = self.get(user_id)
        profile.preferences[key] = value
        self.save(profile)
    
    def add_fact(self, user_id: str, fact: str) -> None:
        profile = self.get(user_id)
        if fact not in profile.facts:
            profile.facts.append(fact)
        self.save(profile)
```

## Memory Types

| Type | Use Case | Backend |
|------|----------|---------|
| Conversation | Recent context | In-memory, Redis |
| Session | Multi-turn dialogs | Redis, PostgreSQL |
| Long-term | Knowledge storage | Vector DB |
| User Profile | Preferences | Redis, PostgreSQL |
| Entity | Facts about entities | Knowledge Graph |

## Best Practices

- Use TTL for conversation memory to manage storage
- Compress old messages to fit context windows
- Separate short-term and long-term memory
- Index memories for semantic retrieval
- Store structured data when possible
- Implement memory forgetting for privacy

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Unbounded history | Set max messages, compress |
| No persistence | Use Redis/PostgreSQL |
| No semantic search | Add vector embeddings |
| Single memory type | Layer memory systems |

## Related

- Knowledge: `knowledge/memory-patterns.json`
- Skill: `state-management`
- Skill: `rag-patterns`
