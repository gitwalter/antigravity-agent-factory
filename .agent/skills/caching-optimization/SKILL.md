---
description: LLM response caching, semantic caching, memoization, cache invalidation
---

# Caching Optimization

LLM response caching, semantic caching, memoization, cache invalidation

## 
# Caching Optimization Skill

Implement caching strategies for LLM responses, semantic caching, memoization, and cache invalidation to reduce costs and improve performance.

## 
# Caching Optimization Skill

Implement caching strategies for LLM responses, semantic caching, memoization, and cache invalidation to reduce costs and improve performance.

## Process
### Step 1: Basic LLM Response Caching

Cache LLM responses using simple key-value storage:

```python
from langchain_openai import ChatOpenAI
from langchain_core.caches import InMemoryCache
from langchain.globals import set_llm_cache
import hashlib
import json
from typing import Optional
import time

# In-memory cache
cache = InMemoryCache()
set_llm_cache(cache)

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# LLM will automatically use cache
response1 = await llm.ainvoke("What is Python?")
response2 = await llm.ainvoke("What is Python?")  # Cached

# Custom cache implementation
class SimpleCache:
    """Simple in-memory cache for LLM responses."""
    
    def __init__(self, ttl: int = 3600):
        self.cache: dict = {}
        self.ttl = ttl
    
    def _key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate cache key."""
        content = f"{prompt}:{model}:{temperature}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Get cached response."""
        key = self._key(prompt, model, temperature)
        if key in self.cache:
            entry = self.cache[key]
            # Check TTL
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["response"]
            else:
                del self.cache[key]
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str) -> None:
        """Cache response."""
        key = self._key(prompt, model, temperature)
        self.cache[key] = {
            "response": response,
            "timestamp": time.time()
        }

# Usage
cache = SimpleCache(ttl=3600)
cached = cache.get("What is Python?", "gpt-4", 0.7)
if not cached:
    response = await llm.ainvoke("What is Python?")
    cache.set("What is Python?", "gpt-4", 0.7, response.content)
```

### Step 2: Redis-Based Caching

Use Redis for distributed caching:

```python
import redis
import json
import hashlib
from typing import Optional
from datetime import timedelta

class RedisCache:
    """Redis-backed cache for LLM responses."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", ttl: int = 3600):
        self.client = redis.from_url(redis_url)
        self.ttl = ttl
    
    def _key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate cache key."""
        content = f"{prompt}:{model}:{temperature}"
        return f"llm_cache:{hashlib.md5(content.encode()).hexdigest()}"
    
    def get(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Get cached response."""
        key = self._key(prompt, model, temperature)
        data = self.client.get(key)
        if data:
            return json.loads(data)["response"]
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str) -> None:
        """Cache response."""
        key = self._key(prompt, model, temperature)
        data = {
            "response": response,
            "model": model,
            "temperature": temperature
        }
        self.client.setex(key, self.ttl, json.dumps(data))
    
    def invalidate(self, pattern: str = None) -> None:
        """Invalidate cache entries matching pattern."""
        if pattern:
            keys = self.client.keys(f"llm_cache:*{pattern}*")
        else:
            keys = self.client.keys("llm_cache:*")
        
        if keys:
            self.client.delete(*keys)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        keys = self.client.keys("llm_cache:*")
        if keys:
            self.client.delete(*keys)

# Usage
redis_cache = RedisCache(ttl=7200)  # 2 hours

async def cached_llm_call(prompt: str, model: str = "gpt-4", temperature: float = 0.7):
    """Make cached LLM call."""
    cached = redis_cache.get(prompt, model, temperature)
    if cached:
        return cached
    
    llm = ChatOpenAI(model=model, temperature=temperature)
    response = await llm.ainvoke(prompt)
    redis_cache.set(prompt, model, temperature, response.content)
    return response.content
```

### Step 3: Semantic Caching

Cache based on semantic similarity, not exact matches:

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple, Optional
import chromadb
import hashlib

class SemanticCache:
    """Semantic similarity-based cache."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = similarity_threshold
        self.cache: List[dict] = []
    
    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        """Normalize vector for cosine similarity."""
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector
    
    def add(self, prompt: str, response: str) -> None:
        """Add prompt-response pair to cache."""
        embedding = self.embedder.encode(prompt)
        embedding = self._normalize(embedding)
        
        self.cache.append({
            "prompt": prompt,
            "response": response,
            "embedding": embedding
        })
    
    def get(self, prompt: str) -> Tuple[Optional[str], float]:
        """Get cached response if semantically similar."""
        if len(self.cache) == 0:
            return None, 0.0
        
        query_embedding = self.embedder.encode(prompt)
        query_embedding = self._normalize(query_embedding)
        
        # Find most similar
        best_similarity = 0.0
        best_response = None
        
        for entry in self.cache:
            similarity = np.dot(query_embedding, entry["embedding"])
            if similarity > best_similarity:
                best_similarity = similarity
                best_response = entry["response"]
        
        if best_similarity >= self.threshold:
            return best_response, best_similarity
        
        return None, best_similarity
    
    def clear(self) -> None:
        """Clear cache."""
        self.cache = []

# Usage with ChromaDB (alternative)
class ChromaSemanticCache:
    """Semantic cache using ChromaDB."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("semantic_cache")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = similarity_threshold
    
    def get(self, prompt: str) -> Optional[str]:
        """Get semantically similar cached response."""
        query_embedding = self.embedder.encode(prompt).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        
        if results["distances"] and results["distances"][0][0] <= (1 - self.threshold):
            # ChromaDB returns distance, convert to similarity
            return results["documents"][0][0]
        
        return None
    
    def add(self, prompt: str, response: str) -> None:
        """Add to semantic cache."""
        embedding = self.embedder.encode(prompt).tolist()
        
        self.collection.add(
            ids=[hashlib.md5(prompt.encode()).hexdigest()],
            embeddings=[embedding],
            documents=[response]
        )

# Usage
semantic_cache = SemanticCache(similarity_threshold=0.85)

async def semantically_cached_llm(prompt: str):
    """LLM call with semantic caching."""
    cached, similarity = semantic_cache.get(prompt)
    if cached:
        return cached
    
    llm = ChatOpenAI(model="gpt-4")
    response = await llm.ainvoke(prompt)
    semantic_cache.add(prompt, response.content)
    return response.content
```

### Step 4: Function Memoization

Memoize expensive function calls:

```python
from functools import wraps
import hashlib
import pickle
from typing import Callable, Any
import asyncio

def memoize(ttl: int = 3600, cache_backend: str = "memory"):
    """Decorator for memoizing function results."""
    
    if cache_backend == "memory":
        cache = {}
    elif cache_backend == "redis":
        cache = redis.from_url("redis://localhost:6379")
    else:
        cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            key_data = {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            }
            key = hashlib.md5(pickle.dumps(key_data)).hexdigest()
            cache_key = f"memoize:{func.__name__}:{key}"
            
            # Check cache
            if cache_backend == "redis":
                cached = cache.get(cache_key)
                if cached:
                    return pickle.loads(cached)
            else:
                if cache_key in cache:
                    entry = cache[cache_key]
                    if time.time() - entry["timestamp"] < ttl:
                        return entry["value"]
                    else:
                        del cache[cache_key]
            
            # Execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Cache result
            if cache_backend == "redis":
                cache.setex(cache_key, ttl, pickle.dumps(result))
            else:
                cache[cache_key] = {
                    "value": result,
                    "timestamp": time.time()
                }
            
            return result
        
        return async_wrapper
    return decorator

# Usage
@memoize(ttl=1800)  # 30 minutes
async def expensive_computation(data: str) -> str:
    """Expensive computation that should be cached."""
    # Simulate expensive operation
    await asyncio.sleep(2)
    llm = ChatOpenAI(model="gpt-4")
    response = await llm.ainvoke(f"Process: {data}")
    return response.content

# First call - executes
result1 = await expensive_computation("test data")

# Second call - cached
result2 = await expensive_computation("test data")  # Returns immediately
```

### Step 5: Cache Invalidation Strategies

Implement various cache invalidation patterns:

```python
from datetime import datetime
from typing import List, Callable

class CacheManager:
    """Advanced cache management with invalidation strategies."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
        self.invalidation_callbacks: List[Callable] = []
    
    def add_invalidation_callback(self, callback: Callable) -> None:
        """Add callback to execute on cache invalidation."""
        self.invalidation_callbacks.append(callback)
    
    def invalidate_by_pattern(self, pattern: str) -> int:
        """Invalidate entries matching pattern."""
        keys = self.client.keys(f"*{pattern}*")
        if keys:
            count = self.client.delete(*keys)
            self._trigger_callbacks(pattern)
            return count
        return 0
    
    def invalidate_by_ttl(self, max_age: int) -> int:
        """Invalidate entries older than max_age seconds."""
        keys = self.client.keys("*")
        count = 0
        
        for key in keys:
            ttl = self.client.ttl(key)
            if ttl == -1:  # No expiration
                # Check if key has timestamp metadata
                data = self.client.get(key)
                if data:
                    try:
                        entry = json.loads(data)
                        if "timestamp" in entry:
                            age = datetime.now().timestamp() - entry["timestamp"]
                            if age > max_age:
                                self.client.delete(key)
                                count += 1
                    except:
                        pass
            elif ttl > max_age:
                # Set new TTL
                self.client.expire(key, max_age)
        
        return count
    
    def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate entries tagged with specific tag."""
        tag_key = f"tag:{tag}"
        keys = self.client.smembers(tag_key)
        
        if keys:
            count = self.client.delete(*keys)
            self.client.delete(tag_key)
            self._trigger_callbacks(f"tag:{tag}")
            return count
        return 0
    
    def tag_entry(self, key: str, tags: List[str]) -> None:
        """Tag cache entry for later invalidation."""
        for tag in tags:
            tag_key = f"tag:{tag}"
            self.client.sadd(tag_key, key)
    
    def _trigger_callbacks(self, pattern: str) -> None:
        """Trigger invalidation callbacks."""
        for callback in self.invalidation_callbacks:
            try:
                callback(pattern)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def clear_all(self) -> None:
        """Clear all cache entries."""
        keys = self.client.keys("*")
        if keys:
            self.client.delete(*keys)
        self._trigger_callbacks("all")

# Usage with tagging
cache_manager = CacheManager()

def cache_with_tags(key: str, value: str, tags: List[str], ttl: int = 3600):
    """Cache entry with tags."""
    cache_manager.client.setex(key, ttl, value)
    cache_manager.tag_entry(key, tags)

# Invalidate all entries with specific tag
cache_manager.invalidate_by_tag("user_data")  # Invalidates all user-related cache
```

### Step 6: LangChain Cache Integration

Use LangChain's built-in caching:

```python
from langchain.globals import set_llm_cache, get_llm_cache
from langchain.cache import RedisCache, InMemoryCache
from langchain_openai import ChatOpenAI

# Set global cache
set_llm_cache(RedisCache(redis_url="redis://localhost:6379"))

# Or use in-memory cache
set_llm_cache(InMemoryCache())

# LLMs will automatically use cache
llm = ChatOpenAI(model="gpt-4")

# First call - not cached
response1 = await llm.ainvoke("What is Python?")

# Second call - cached
response2 = await llm.ainvoke("What is Python?")

# Clear cache
cache = get_llm_cache()
if isinstance(cache, RedisCache):
    cache.client.flushdb()

# Custom cache with TTL
class TTLCache(InMemoryCache):
    """In-memory cache with TTL."""
    
    def __init__(self, ttl: int = 3600):
        super().__init__()
        self.ttl = ttl
        self.timestamps = {}
    
    def lookup(self, prompt: str, llm_string: str) -> Optional[str]:
        """Lookup with TTL check."""
        key = self._generate_key(prompt, llm_string)
        
        if key in self.cache:
            if time.time() - self.timestamps.get(key, 0) < self.ttl:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        
        return None
    
    def update(self, prompt: str, llm_string: str, return_val: str) -> None:
        """Update cache with timestamp."""
        key = self._generate_key(prompt, llm_string)
        self.cache[key] = return_val
        self.timestamps[key] = time.time()

# Use custom cache
set_llm_cache(TTLCache(ttl=1800))  # 30 minutes
```

```python
from langchain_openai import ChatOpenAI
from langchain_core.caches import InMemoryCache
from langchain.globals import set_llm_cache
import hashlib
import json
from typing import Optional
import time

# In-memory cache
cache = InMemoryCache()
set_llm_cache(cache)

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# LLM will automatically use cache
response1 = await llm.ainvoke("What is Python?")
response2 = await llm.ainvoke("What is Python?")  # Cached

# Custom cache implementation
class SimpleCache:
    """Simple in-memory cache for LLM responses."""
    
    def __init__(self, ttl: int = 3600):
        self.cache: dict = {}
        self.ttl = ttl
    
    def _key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate cache key."""
        content = f"{prompt}:{model}:{temperature}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Get cached response."""
        key = self._key(prompt, model, temperature)
        if key in self.cache:
            entry = self.cache[key]
            # Check TTL
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["response"]
            else:
                del self.cache[key]
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str) -> None:
        """Cache response."""
        key = self._key(prompt, model, temperature)
        self.cache[key] = {
            "response": response,
            "timestamp": time.time()
        }

# Usage
cache = SimpleCache(ttl=3600)
cached = cache.get("What is Python?", "gpt-4", 0.7)
if not cached:
    response = await llm.ainvoke("What is Python?")
    cache.set("What is Python?", "gpt-4", 0.7, response.content)
```

```python
import redis
import json
import hashlib
from typing import Optional
from datetime import timedelta

class RedisCache:
    """Redis-backed cache for LLM responses."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", ttl: int = 3600):
        self.client = redis.from_url(redis_url)
        self.ttl = ttl
    
    def _key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate cache key."""
        content = f"{prompt}:{model}:{temperature}"
        return f"llm_cache:{hashlib.md5(content.encode()).hexdigest()}"
    
    def get(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Get cached response."""
        key = self._key(prompt, model, temperature)
        data = self.client.get(key)
        if data:
            return json.loads(data)["response"]
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str) -> None:
        """Cache response."""
        key = self._key(prompt, model, temperature)
        data = {
            "response": response,
            "model": model,
            "temperature": temperature
        }
        self.client.setex(key, self.ttl, json.dumps(data))
    
    def invalidate(self, pattern: str = None) -> None:
        """Invalidate cache entries matching pattern."""
        if pattern:
            keys = self.client.keys(f"llm_cache:*{pattern}*")
        else:
            keys = self.client.keys("llm_cache:*")
        
        if keys:
            self.client.delete(*keys)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        keys = self.client.keys("llm_cache:*")
        if keys:
            self.client.delete(*keys)

# Usage
redis_cache = RedisCache(ttl=7200)  # 2 hours

async def cached_llm_call(prompt: str, model: str = "gpt-4", temperature: float = 0.7):
    """Make cached LLM call."""
    cached = redis_cache.get(prompt, model, temperature)
    if cached:
        return cached
    
    llm = ChatOpenAI(model=model, temperature=temperature)
    response = await llm.ainvoke(prompt)
    redis_cache.set(prompt, model, temperature, response.content)
    return response.content
```

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple, Optional
import chromadb
import hashlib

class SemanticCache:
    """Semantic similarity-based cache."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = similarity_threshold
        self.cache: List[dict] = []
    
    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        """Normalize vector for cosine similarity."""
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector
    
    def add(self, prompt: str, response: str) -> None:
        """Add prompt-response pair to cache."""
        embedding = self.embedder.encode(prompt)
        embedding = self._normalize(embedding)
        
        self.cache.append({
            "prompt": prompt,
            "response": response,
            "embedding": embedding
        })
    
    def get(self, prompt: str) -> Tuple[Optional[str], float]:
        """Get cached response if semantically similar."""
        if len(self.cache) == 0:
            return None, 0.0
        
        query_embedding = self.embedder.encode(prompt)
        query_embedding = self._normalize(query_embedding)
        
        # Find most similar
        best_similarity = 0.0
        best_response = None
        
        for entry in self.cache:
            similarity = np.dot(query_embedding, entry["embedding"])
            if similarity > best_similarity:
                best_similarity = similarity
                best_response = entry["response"]
        
        if best_similarity >= self.threshold:
            return best_response, best_similarity
        
        return None, best_similarity
    
    def clear(self) -> None:
        """Clear cache."""
        self.cache = []

# Usage with ChromaDB (alternative)
class ChromaSemanticCache:
    """Semantic cache using ChromaDB."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("semantic_cache")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = similarity_threshold
    
    def get(self, prompt: str) -> Optional[str]:
        """Get semantically similar cached response."""
        query_embedding = self.embedder.encode(prompt).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        
        if results["distances"] and results["distances"][0][0] <= (1 - self.threshold):
            # ChromaDB returns distance, convert to similarity
            return results["documents"][0][0]
        
        return None
    
    def add(self, prompt: str, response: str) -> None:
        """Add to semantic cache."""
        embedding = self.embedder.encode(prompt).tolist()
        
        self.collection.add(
            ids=[hashlib.md5(prompt.encode()).hexdigest()],
            embeddings=[embedding],
            documents=[response]
        )

# Usage
semantic_cache = SemanticCache(similarity_threshold=0.85)

async def semantically_cached_llm(prompt: str):
    """LLM call with semantic caching."""
    cached, similarity = semantic_cache.get(prompt)
    if cached:
        return cached
    
    llm = ChatOpenAI(model="gpt-4")
    response = await llm.ainvoke(prompt)
    semantic_cache.add(prompt, response.content)
    return response.content
```

```python
from functools import wraps
import hashlib
import pickle
from typing import Callable, Any
import asyncio

def memoize(ttl: int = 3600, cache_backend: str = "memory"):
    """Decorator for memoizing function results."""
    
    if cache_backend == "memory":
        cache = {}
    elif cache_backend == "redis":
        cache = redis.from_url("redis://localhost:6379")
    else:
        cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            key_data = {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            }
            key = hashlib.md5(pickle.dumps(key_data)).hexdigest()
            cache_key = f"memoize:{func.__name__}:{key}"
            
            # Check cache
            if cache_backend == "redis":
                cached = cache.get(cache_key)
                if cached:
                    return pickle.loads(cached)
            else:
                if cache_key in cache:
                    entry = cache[cache_key]
                    if time.time() - entry["timestamp"] < ttl:
                        return entry["value"]
                    else:
                        del cache[cache_key]
            
            # Execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Cache result
            if cache_backend == "redis":
                cache.setex(cache_key, ttl, pickle.dumps(result))
            else:
                cache[cache_key] = {
                    "value": result,
                    "timestamp": time.time()
                }
            
            return result
        
        return async_wrapper
    return decorator

# Usage
@memoize(ttl=1800)  # 30 minutes
async def expensive_computation(data: str) -> str:
    """Expensive computation that should be cached."""
    # Simulate expensive operation
    await asyncio.sleep(2)
    llm = ChatOpenAI(model="gpt-4")
    response = await llm.ainvoke(f"Process: {data}")
    return response.content

# First call - executes
result1 = await expensive_computation("test data")

# Second call - cached
result2 = await expensive_computation("test data")  # Returns immediately
```

```python
from datetime import datetime
from typing import List, Callable

class CacheManager:
    """Advanced cache management with invalidation strategies."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
        self.invalidation_callbacks: List[Callable] = []
    
    def add_invalidation_callback(self, callback: Callable) -> None:
        """Add callback to execute on cache invalidation."""
        self.invalidation_callbacks.append(callback)
    
    def invalidate_by_pattern(self, pattern: str) -> int:
        """Invalidate entries matching pattern."""
        keys = self.client.keys(f"*{pattern}*")
        if keys:
            count = self.client.delete(*keys)
            self._trigger_callbacks(pattern)
            return count
        return 0
    
    def invalidate_by_ttl(self, max_age: int) -> int:
        """Invalidate entries older than max_age seconds."""
        keys = self.client.keys("*")
        count = 0
        
        for key in keys:
            ttl = self.client.ttl(key)
            if ttl == -1:  # No expiration
                # Check if key has timestamp metadata
                data = self.client.get(key)
                if data:
                    try:
                        entry = json.loads(data)
                        if "timestamp" in entry:
                            age = datetime.now().timestamp() - entry["timestamp"]
                            if age > max_age:
                                self.client.delete(key)
                                count += 1
                    except:
                        pass
            elif ttl > max_age:
                # Set new TTL
                self.client.expire(key, max_age)
        
        return count
    
    def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate entries tagged with specific tag."""
        tag_key = f"tag:{tag}"
        keys = self.client.smembers(tag_key)
        
        if keys:
            count = self.client.delete(*keys)
            self.client.delete(tag_key)
            self._trigger_callbacks(f"tag:{tag}")
            return count
        return 0
    
    def tag_entry(self, key: str, tags: List[str]) -> None:
        """Tag cache entry for later invalidation."""
        for tag in tags:
            tag_key = f"tag:{tag}"
            self.client.sadd(tag_key, key)
    
    def _trigger_callbacks(self, pattern: str) -> None:
        """Trigger invalidation callbacks."""
        for callback in self.invalidation_callbacks:
            try:
                callback(pattern)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def clear_all(self) -> None:
        """Clear all cache entries."""
        keys = self.client.keys("*")
        if keys:
            self.client.delete(*keys)
        self._trigger_callbacks("all")

# Usage with tagging
cache_manager = CacheManager()

def cache_with_tags(key: str, value: str, tags: List[str], ttl: int = 3600):
    """Cache entry with tags."""
    cache_manager.client.setex(key, ttl, value)
    cache_manager.tag_entry(key, tags)

# Invalidate all entries with specific tag
cache_manager.invalidate_by_tag("user_data")  # Invalidates all user-related cache
```

```python
from langchain.globals import set_llm_cache, get_llm_cache
from langchain.cache import RedisCache, InMemoryCache
from langchain_openai import ChatOpenAI

# Set global cache
set_llm_cache(RedisCache(redis_url="redis://localhost:6379"))

# Or use in-memory cache
set_llm_cache(InMemoryCache())

# LLMs will automatically use cache
llm = ChatOpenAI(model="gpt-4")

# First call - not cached
response1 = await llm.ainvoke("What is Python?")

# Second call - cached
response2 = await llm.ainvoke("What is Python?")

# Clear cache
cache = get_llm_cache()
if isinstance(cache, RedisCache):
    cache.client.flushdb()

# Custom cache with TTL
class TTLCache(InMemoryCache):
    """In-memory cache with TTL."""
    
    def __init__(self, ttl: int = 3600):
        super().__init__()
        self.ttl = ttl
        self.timestamps = {}
    
    def lookup(self, prompt: str, llm_string: str) -> Optional[str]:
        """Lookup with TTL check."""
        key = self._generate_key(prompt, llm_string)
        
        if key in self.cache:
            if time.time() - self.timestamps.get(key, 0) < self.ttl:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        
        return None
    
    def update(self, prompt: str, llm_string: str, return_val: str) -> None:
        """Update cache with timestamp."""
        key = self._generate_key(prompt, llm_string)
        self.cache[key] = return_val
        self.timestamps[key] = time.time()

# Use custom cache
set_llm_cache(TTLCache(ttl=1800))  # 30 minutes
```

## Caching Strategies
| Strategy | Use Case | Pros | Cons |
|----------|----------|------|------|
| **Exact Match** | Identical queries | Simple, fast | Misses similar queries |
| **Semantic** | Similar queries | Higher hit rate | More complex, slower |
| **TTL-based** | Time-sensitive data | Automatic expiry | May expire too early/late |
| **Tag-based** | Related data | Precise invalidation | Requires tagging |
| **LRU** | Memory-limited | Efficient memory use | Complex implementation |

## Best Practices
- Use semantic caching for similar queries
- Set appropriate TTLs based on data freshness needs
- Implement cache warming for critical paths
- Monitor cache hit rates
- Use Redis for distributed systems
- Tag cache entries for precise invalidation
- Implement cache fallbacks for failures
- Set memory limits for in-memory caches
- Log cache misses for optimization
- Use compression for large cached values

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| No TTL | Set appropriate expiration times |
| Caching everything | Cache only expensive operations |
| No invalidation | Implement invalidation strategies |
| Exact match only | Use semantic caching |
| No monitoring | Track hit rates and performance |
| Synchronous cache | Use async cache operations |
| No error handling | Handle cache failures gracefully |
| Stale data | Implement proper invalidation |
| Memory leaks | Set size limits and eviction policies |
| No compression | Compress large cached values |

## Related
- Skill: `memory-management`
- Skill: `error-handling`
- Skill: `langchain-usage`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: langchain-core, langchain, langchain-openai, redis, sentence-transformers
