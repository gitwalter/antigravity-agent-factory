---
description: Optimize AI/LLM costs through intelligent routing, caching, batching,
  and usage analytics
name: ai-cost-optimization
type: skill
---
# Ai Cost Optimization

Optimize AI/LLM costs through intelligent routing, caching, batching, and usage analytics

Optimize AI and LLM costs through intelligent model routing, semantic caching, prompt optimization, and usage analytics.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Token Usage Tracking and Analytics

```python
# token_tracking.py
import tiktoken
from typing import Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class TokenUsage:
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    task_type: str

class TokenTracker:
    """Track and analyze token usage."""
    
    def __init__(self):
        self.usage_history: List[TokenUsage] = []
        self.encodings = {}  # Cache encodings
    
    def _get_encoding(self, model: str):
        """Get tokenizer encoding for model."""
        if model not in self.encodings:
            if "gpt-4" in model or "gpt-3.5" in model:
                self.encodings[model] = tiktoken.encoding_for_model(model)
            else:
                # Fallback to cl100k_base for most OpenAI models
                self.encodings[model] = tiktoken.get_encoding("cl100k_base")
        return self.encodings[model]
    
    def count_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """Count tokens in text."""
        encoding = self._get_encoding(model)
        return len(encoding.encode(text))
    
    def record_usage(
        self,
        model: str,
        prompt: str,
        completion: str,
        task_type: str = "unknown",
    ):
        """Record token usage."""
        prompt_tokens = self.count_tokens(prompt, model)
        completion_tokens = self.count_tokens(completion, model)
        cost = self._calculate_cost(model, prompt_tokens, completion_tokens)
        
        usage = TokenUsage(
            timestamp=datetime.now(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost,
            task_type=task_type,
        )
        
        self.usage_history.append(usage)
        return usage
    
    def _calculate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        """Calculate cost based on model pricing."""
        # Pricing per 1M tokens (as of 2024)
        pricing = {
            "gpt-4": {"input": 30.0, "output": 60.0},
            "gpt-4-turbo": {"input": 10.0, "output": 30.0},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
            "claude-3-opus": {"input": 15.0, "output": 75.0},
            "claude-3-sonnet": {"input": 3.0, "output": 15.0},
            "claude-3-haiku": {"input": 0.25, "output": 1.25},
        }
        
        model_pricing = pricing.get(model, {"input": 1.0, "output": 1.0})
        
        cost = (
            (prompt_tokens / 1_000_000) * model_pricing["input"] +
            (completion_tokens / 1_000_000) * model_pricing["output"]
        )
        
        return cost
    
    def get_cost_analytics(self, days: int = 7) -> Dict:
        """Get cost analytics."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [u for u in self.usage_history if u.timestamp >= cutoff]
        
        if not recent:
            return {}
        
        total_cost = sum(u.cost_usd for u in recent)
        total_tokens = sum(u.prompt_tokens + u.completion_tokens for u in recent)
        
        # Cost by model
        cost_by_model = {}
        for usage in recent:
            cost_by_model[usage.model] = cost_by_model.get(usage.model, 0) + usage.cost_usd
        
        # Cost by task type
        cost_by_task = {}
        for usage in recent:
            cost_by_task[usage.task_type] = cost_by_task.get(usage.task_type, 0) + usage.cost_usd
        
        # Average cost per request
        avg_cost_per_request = total_cost / len(recent)
        
        return {
            "total_cost_usd": total_cost,
            "total_tokens": total_tokens,
            "total_requests": len(recent),
            "avg_cost_per_request": avg_cost_per_request,
            "cost_by_model": cost_by_model,
            "cost_by_task": cost_by_task,
            "daily_average": total_cost / days,
        }
```

### Step 2: Intelligent Model Routing

```python
# model_router.py
from typing import Dict, Optional
from enum import Enum
import re

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"

class ModelRouter:
    """Route requests to appropriate model based on complexity."""
    
    def __init__(self):
        self.model_mapping = {
            TaskComplexity.SIMPLE: "gpt-3.5-turbo",
            TaskComplexity.MEDIUM: "gpt-4-turbo",
            TaskComplexity.COMPLEX: "gpt-4",
        }
        
        # Cost per 1M tokens
        self.cost_per_million = {
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
            "gpt-4-turbo": {"input": 10.0, "output": 30.0},
            "gpt-4": {"input": 30.0, "output": 60.0},
        }
    
    def assess_complexity(self, prompt: str, task_type: str = None) -> TaskComplexity:
        """Assess task complexity."""
        prompt_lower = prompt.lower()
        prompt_length = len(prompt)
        
        # Simple heuristics
        complexity_score = 0
        
        # Length-based
        if prompt_length > 2000:
            complexity_score += 2
        elif prompt_length > 1000:
            complexity_score += 1
        
        # Keyword-based complexity indicators
        complex_keywords = [
            "analyze", "compare", "evaluate", "synthesize",
            "reason", "logic", "mathematical", "code",
        ]
        simple_keywords = [
            "summarize", "translate", "rewrite", "format",
        ]
        
        for keyword in complex_keywords:
            if keyword in prompt_lower:
                complexity_score += 1
        
        for keyword in simple_keywords:
            if keyword in prompt_lower:
                complexity_score -= 1
        
        # Task type hints
        if task_type:
            if task_type in ["code_generation", "analysis", "reasoning"]:
                complexity_score += 2
            elif task_type in ["translation", "summarization", "formatting"]:
                complexity_score -= 1
        
        # Determine complexity
        if complexity_score >= 3:
            return TaskComplexity.COMPLEX
        elif complexity_score >= 1:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def select_model(
        self,
        prompt: str,
        task_type: str = None,
        force_model: Optional[str] = None,
    ) -> str:
        """Select appropriate model."""
        if force_model:
            return force_model
        
        complexity = self.assess_complexity(prompt, task_type)
        return self.model_mapping[complexity]
    
    def estimate_cost(
        self,
        model: str,
        prompt_tokens: int,
        estimated_completion_tokens: int = 500,
    ) -> float:
        """Estimate cost for request."""
        pricing = self.cost_per_million.get(model, {"input": 1.0, "output": 1.0})
        
        cost = (
            (prompt_tokens / 1_000_000) * pricing["input"] +
            (estimated_completion_tokens / 1_000_000) * pricing["output"]
        )
        
        return cost

# Usage
router = ModelRouter()
model = router.select_model("Translate this text to French", task_type="translation")
# Returns: "gpt-3.5-turbo" (simple task)

model = router.select_model("Analyze this code and suggest optimizations", task_type="code_analysis")
# Returns: "gpt-4" (complex task)
```

### Step 3: Semantic Caching with Redis

```python
# semantic_cache.py
import redis
import hashlib
import json
from typing import Optional, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticCache:
    """Semantic cache for LLM responses using embeddings."""
    
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        similarity_threshold: float = 0.95,
    ):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True,
        )
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.similarity_threshold = similarity_threshold
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text."""
        return self.encoder.encode(text, normalize=True)
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity."""
        return np.dot(a, b)
    
    def _get_cache_key(self, embedding: np.ndarray) -> str:
        """Generate cache key from embedding."""
        # Use first few dimensions for key (approximate)
        key_hash = hashlib.md5(embedding[:16].tobytes()).hexdigest()
        return f"semantic_cache:{key_hash}"
    
    def get(
        self,
        prompt: str,
    ) -> Optional[Tuple[str, float]]:
        """Get cached response if similar prompt exists."""
        prompt_embedding = self._get_embedding(prompt)
        
        # Search for similar embeddings
        # In production, use vector database (Redis Vector, Pinecone, etc.)
        # Here's a simplified version using Redis sets
        
        # Get all cache keys
        cache_keys = self.redis_client.keys("semantic_cache:*")
        
        best_match = None
        best_similarity = 0.0
        
        for key in cache_keys:
            # Get stored embedding and response
            cached_data = self.redis_client.hgetall(key)
            
            if not cached_data:
                continue
            
            cached_embedding = np.frombuffer(
                bytes.fromhex(cached_data["embedding"]),
                dtype=np.float32,
            )
            
            similarity = self._cosine_similarity(prompt_embedding, cached_embedding)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = cached_data["response"]
        
        if best_similarity >= self.similarity_threshold:
            return (best_match, best_similarity)
        
        return None
    
    def set(
        self,
        prompt: str,
        response: str,
        ttl: int = 86400,  # 24 hours
    ):
        """Cache prompt-response pair."""
        prompt_embedding = self._get_embedding(prompt)
        cache_key = self._get_cache_key(prompt_embedding)
        
        # Store embedding (as hex) and response
        self.redis_client.hset(
            cache_key,
            mapping={
                "embedding": prompt_embedding.tobytes().hex(),
                "response": response,
                "prompt": prompt,
            },
        )
        self.redis_client.expire(cache_key, ttl)

# Usage with LLM call
def generate_with_cache(
    prompt: str,
    llm_call,
    cache: SemanticCache,
) -> str:
    """Generate with semantic caching."""
    # Check cache
    cached = cache.get(prompt)
    if cached:
        response, similarity = cached
        print(f"Cache hit! Similarity: {similarity:.3f}")
        return response
    
    # Generate from LLM
    response = llm_call(prompt)
    
    # Cache result
    cache.set(prompt, response)
    
    return response
```

### Step 4: Prompt Caching (Anthropic/OpenAI)

```python
# prompt_caching.py
from typing import Dict, List, Optional
import hashlib
import json

class PromptCache:
    """Cache for prompt prefixes (Anthropic/OpenAI style)."""
    
    def __init__(self):
        self.cache: Dict[str, str] = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def _hash_prompt(self, prompt: str) -> str:
        """Hash prompt for cache key."""
        return hashlib.sha256(prompt.encode()).hexdigest()
    
    def get_cached_prefix(self, messages: List[Dict]) -> Optional[str]:
        """Get cached prefix if available."""
        # Find longest common prefix
        if not messages:
            return None
        
        # Build prefix hash
        prefix_parts = []
        for msg in messages[:-1]:  # All but last message
            prefix_parts.append(json.dumps(msg, sort_keys=True))
        
        prefix_str = "|".join(prefix_parts)
        prefix_hash = self._hash_prompt(prefix_str)
        
        if prefix_hash in self.cache:
            self.cache_hits += 1
            return self.cache[prefix_hash]
        
        self.cache_misses += 1
        return None
    
    def cache_prefix(self, messages: List[Dict], cache_id: str):
        """Cache prefix for future use."""
        prefix_parts = []
        for msg in messages[:-1]:
            prefix_parts.append(json.dumps(msg, sort_keys=True))
        
        prefix_str = "|".join(prefix_parts)
        prefix_hash = self._hash_prompt(prefix_str)
        
        self.cache[prefix_hash] = cache_id
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        total = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total if total > 0 else 0.0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate,
            "cached_prefixes": len(self.cache),
        }

# Usage with OpenAI API
import openai

prompt_cache = PromptCache()

def chat_completion_with_cache(
    messages: List[Dict],
    model: str = "gpt-3.5-turbo",
) -> str:
    """Chat completion with prompt caching."""
    
    # Check for cached prefix
    cached_id = prompt_cache.get_cached_prefix(messages)
    
    if cached_id:
        # Use cached prefix
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            extra_headers={
                "OpenAI-Beta": "assistants=v2",
            },
            # In OpenAI API, you'd use cache_control
        )
    else:
        # Regular call
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        
        # Cache the prefix for future use
        cache_id = response.get("cache_id")
        if cache_id:
            prompt_cache.cache_prefix(messages, cache_id)
    
    return response.choices[0].message.content
```

### Step 5: Batching Strategies for Embeddings

```python
# embedding_batching.py
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingBatcher:
    """Batch embedding requests for efficiency."""
    
    def __init__(self, batch_size: int = 32):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.batch_size = batch_size
        self.pending_texts: List[str] = []
        self.pending_futures: List = []
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encode batch of texts."""
        # Batch encoding is more efficient
        embeddings = self.encoder.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode single text (less efficient)."""
        return self.encoder.encode([text])[0]

# Cost comparison
def compare_batching_costs():
    """Compare costs of batched vs individual calls."""
    texts = [f"Text {i}" for i in range(100)]
    
    batcher = EmbeddingBatcher(batch_size=32)
    
    # Batched approach
    batched_embeddings = batcher.encode_batch(texts)
    # Single API call (if using API)
    
    # Individual approach
    individual_embeddings = [batcher.encode_single(text) for text in texts]
    # 100 API calls
    
    # Batched is ~10-100x more cost-effective
```

### Step 6: Cost-Per-Task Metrics

```python
# cost_per_task.py
from typing import Dict
from datetime import datetime, timedelta

class CostPerTaskTracker:
    """Track cost per task type."""
    
    def __init__(self):
        self.task_costs: Dict[str, List[float]] = {}
        self.task_counts: Dict[str, int] = {}
    
    def record_task(
        self,
        task_type: str,
        cost: float,
    ):
        """Record task cost."""
        if task_type not in self.task_costs:
            self.task_costs[task_type] = []
            self.task_counts[task_type] = 0
        
        self.task_costs[task_type].append(cost)
        self.task_counts[task_type] += 1
    
    def get_cost_per_task(self, task_type: str) -> Dict:
        """Get cost metrics for task type."""
        if task_type not in self.task_costs:
            return {}
        
        costs = self.task_costs[task_type]
        
        return {
            "task_type": task_type,
            "total_cost": sum(costs),
            "avg_cost": sum(costs) / len(costs),
            "min_cost": min(costs),
            "max_cost": max(costs),
            "total_tasks": self.task_counts[task_type],
        }
    
    def get_all_task_costs(self) -> Dict[str, Dict]:
        """Get cost metrics for all task types."""
        return {
            task_type: self.get_cost_per_task(task_type)
            for task_type in self.task_costs.keys()
        }
    
    def identify_expensive_tasks(self, threshold: float = 1.0) -> List[str]:
        """Identify tasks exceeding cost threshold."""
        expensive = []
        
        for task_type, metrics in self.get_all_task_costs().items():
            if metrics["avg_cost"] > threshold:
                expensive.append(task_type)
        
        return expensive

# Usage
tracker = CostPerTaskTracker()
tracker.record_task("translation", cost=0.05)
tracker.record_task("code_generation", cost=0.50)
tracker.record_task("analysis", cost=1.20)

metrics = tracker.get_cost_per_task("code_generation")
expensive = tracker.identify_expensive_tasks(threshold=0.50)
```

### Step 7: Budget Alerts

```python
# budget_alerts.py
from typing import Callable, Optional
from datetime import datetime, timedelta

class BudgetManager:
    """Manage budget and alerts."""
    
    def __init__(self, daily_budget: float):
        self.daily_budget = daily_budget
        self.alert_callbacks: List[Callable] = []
        self.spending_history = []
    
    def add_alert_callback(self, callback: Callable[[float, float], None]):
        """Add callback for budget alerts."""
        self.alert_callbacks.append(callback)
    
    def check_budget(
        self,
        current_spending: float,
        period: str = "daily",
    ) -> Dict:
        """Check budget status."""
        if period == "daily":
            budget = self.daily_budget
        else:
            budget = self.daily_budget * 30  # Monthly
        
        remaining = budget - current_spending
        percentage_used = (current_spending / budget) * 100
        
        status = {
            "budget": budget,
            "spent": current_spending,
            "remaining": remaining,
            "percentage_used": percentage_used,
            "status": "ok",
        }
        
        # Alert thresholds
        if percentage_used >= 100:
            status["status"] = "exceeded"
            self._trigger_alerts(current_spending, budget)
        elif percentage_used >= 90:
            status["status"] = "warning"
            self._trigger_alerts(current_spending, budget)
        elif percentage_used >= 75:
            status["status"] = "caution"
        
        return status
    
    def _trigger_alerts(self, spent: float, budget: float):
        """Trigger alert callbacks."""
        for callback in self.alert_callbacks:
            try:
                callback(spent, budget)
            except Exception as e:
                print(f"Error in alert callback: {e}")

# Usage
def send_budget_alert(spent: float, budget: float):
    """Send budget alert."""
    print(f"ALERT: Budget exceeded! Spent: ${spent:.2f} / Budget: ${budget:.2f}")

budget_manager = BudgetManager(daily_budget=100.0)
budget_manager.add_alert_callback(send_budget_alert)

# Check budget
status = budget_manager.check_budget(current_spending=95.0)
# Returns: {"status": "warning", "percentage_used": 95.0, ...}
```

## Output

- Token usage analytics and reports
- Intelligent model routing system
- Semantic caching implementation
- Cost-per-task metrics
- Budget monitoring and alerts

## Best Practices

- Route simple tasks to cheaper models (GPT-3.5)
- Use semantic caching for similar prompts
- Enable prompt caching for repeated prefixes
- Batch embedding requests
- Track cost per task type
- Set up budget alerts at 75%, 90%, 100%
- Monitor token usage patterns
- Compare provider pricing regularly

## Related

- Skill: `ml-monitoring`
- Skill: `model-serving`
- Skill: `ai-system-design`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
