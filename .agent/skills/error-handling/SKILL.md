---
description: Retry strategies with tenacity, fallback patterns, circuit breakers,
  graceful degradation
name: error-handling
type: skill
---

# Error Handling

Retry strategies with tenacity, fallback patterns, circuit breakers, graceful degradation

## 
# Error Handling Skill

Implement robust error handling patterns - retry strategies, fallbacks, circuit breakers, and graceful degradation for resilient agent systems.

## 
# Error Handling Skill

Implement robust error handling patterns - retry strategies, fallbacks, circuit breakers, and graceful degradation for resilient agent systems.

## Process
### Step 1: Basic Retry with Tenacity

Implement retry logic for transient failures:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
import logging
from langchain_openai import ChatOpenAI
import httpx

logger = logging.getLogger(__name__)

# Basic retry decorator
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)
async def unreliable_api_call(endpoint: str) -> str:
    """API call with automatic retry."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.text

# Retry with specific exceptions
from httpx import HTTPStatusError, TimeoutException

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=1, max=60),
    retry=retry_if_exception_type((HTTPStatusError, TimeoutException)),
    reraise=True
)
async def robust_api_call(url: str) -> dict:
    """Retry on specific exceptions only."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Retry LLM calls
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception)
)
async def retryable_llm_call(prompt: str) -> str:
    """LLM call with retry."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = await llm.ainvoke(prompt)
    return response.content
```

### Step 2: Advanced Retry Strategies

Custom retry conditions and backoff strategies:

```python
from tenacity import (
    retry,
    stop_after_delay,
    wait_fixed,
    wait_random,
    wait_chain,
    retry_if_result,
    retry_if_exception_message
)

# Retry until timeout
@retry(
    stop=stop_after_delay(30),  # Stop after 30 seconds
    wait=wait_fixed(2)
)
async def retry_until_timeout():
    """Retry until time limit."""
    # Implementation
    pass

# Random wait between retries
@retry(
    stop=stop_after_attempt(5),
    wait=wait_random(min=1, max=5)  # Random 1-5 seconds
)
async def retry_with_random_wait():
    """Retry with random wait."""
    pass

# Chained wait strategy
@retry(
    stop=stop_after_attempt(5),
    wait=wait_chain(
        wait_fixed(1) * 3,  # Wait 1s for first 3 attempts
        wait_exponential(multiplier=2, min=2, max=10)  # Then exponential
    )
)
async def retry_with_chained_wait():
    """Retry with chained wait strategy."""
    pass

# Retry based on result
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_result(lambda result: result is None or result == "")
)
async def retry_on_empty_result():
    """Retry if result is empty."""
    result = await some_operation()
    return result

# Retry based on exception message
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_message(match=".*rate limit.*")
)
async def retry_on_rate_limit():
    """Retry only on rate limit errors."""
    # Implementation
    pass
```

### Step 3: Fallback Patterns

Implement fallback mechanisms:

```python
from typing import Callable, List, Any
import asyncio

class FallbackChain:
    """Execute functions in order until one succeeds."""
    
    def __init__(self, fallbacks: List[Callable]):
        self.fallbacks = fallbacks
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute fallbacks in order."""
        last_error = None
        
        for i, fallback in enumerate(self.fallbacks):
            try:
                if asyncio.iscoroutinefunction(fallback):
                    result = await fallback(*args, **kwargs)
                else:
                    result = fallback(*args, **kwargs)
                
                # Success - return result
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"Fallback {i} failed: {e}")
                continue
        
        # All fallbacks failed
        raise Exception(f"All fallbacks failed. Last error: {last_error}")

# Usage with multiple LLM providers
async def primary_llm(prompt: str) -> str:
    """Primary LLM provider."""
    llm = ChatOpenAI(model="gpt-4")
    response = await llm.ainvoke(prompt)
    return response.content

async def fallback_llm(prompt: str) -> str:
    """Fallback LLM provider."""
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(model="claude-3-5-sonnet")
    response = await llm.ainvoke(prompt)
    return response.content

async def local_fallback(prompt: str) -> str:
    """Local fallback (e.g., cached response)."""
    return "Default response from cache"

# Create fallback chain
llm_chain = FallbackChain([primary_llm, fallback_llm, local_fallback])

# Use fallback chain
try:
    result = await llm_chain.execute("What is Python?")
except Exception as e:
    logger.error(f"All LLM providers failed: {e}")

# Fallback with default value
async def safe_llm_call(prompt: str, default: str = "Unable to generate response") -> str:
    """LLM call with default fallback."""
    try:
        llm = ChatOpenAI(model="gpt-4")
        response = await llm.ainvoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return default
```

### Step 4: Circuit Breaker Pattern

Implement circuit breaker to prevent cascading failures:

```python
from enum import Enum
from datetime import datetime
from typing import Callable, Optional
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.failure_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        # Execute function
        try:
            if asyncio.iscoroutinefunction(func):
                result = asyncio.run(func(*args, **kwargs))
            else:
                result = func(*args, **kwargs)
            
            # Success - reset if half-open
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise e
    
    async def acall(self, func: Callable, *args, **kwargs):
        """Async version of call."""
        if self.state == CircuitState.OPEN:
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.failure_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise e

# Usage
circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    expected_exception=Exception
)

async def protected_api_call(url: str) -> dict:
    """API call protected by circuit breaker."""
    async def _call():
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    
    return await circuit_breaker.acall(_call)
```

### Step 5: Graceful Degradation

Implement graceful degradation for partial failures:

```python
from typing import Dict, List
from pydantic import BaseModel

class DegradedResponse(BaseModel):
    """Response with degradation metadata."""
    data: Dict
    degraded_features: List[str]
    full_response: bool

class GracefulDegradation:
    """Implement graceful degradation patterns."""
    
    async def get_user_profile(self, user_id: str) -> DegradedResponse:
        """Get user profile with graceful degradation."""
        degraded_features = []
        profile = {}
        
        # Try to get full profile
        try:
            full_profile = await self._fetch_full_profile(user_id)
            return DegradedResponse(
                data=full_profile,
                degraded_features=[],
                full_response=True
            )
        except Exception as e:
            logger.warning(f"Full profile fetch failed: {e}")
        
        # Degrade to cached profile
        try:
            cached_profile = await self._get_cached_profile(user_id)
            degraded_features.append("real_time_data")
            profile.update(cached_profile)
        except Exception as e:
            logger.warning(f"Cached profile fetch failed: {e}")
            degraded_features.append("cached_data")
        
        # Degrade to minimal profile
        try:
            minimal_profile = await self._get_minimal_profile(user_id)
            profile.update(minimal_profile)
        except Exception as e:
            logger.error(f"Minimal profile fetch failed: {e}")
            # Return empty profile as last resort
            profile = {"user_id": user_id, "status": "degraded"}
        
        return DegradedResponse(
            data=profile,
            degraded_features=degraded_features,
            full_response=False
        )
    
    async def _fetch_full_profile(self, user_id: str) -> Dict:
        """Fetch full profile from primary source."""
        # Implementation
        pass
    
    async def _get_cached_profile(self, user_id: str) -> Dict:
        """Get cached profile."""
        # Implementation
        pass
    
    async def _get_minimal_profile(self, user_id: str) -> Dict:
        """Get minimal profile from fallback."""
        # Implementation
        pass

# Graceful degradation for LLM features
class LLMDegradation:
    """Graceful degradation for LLM features."""
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response with feature degradation."""
        # Try full-featured generation
        try:
            return await self._full_generation(prompt)
        except Exception as e:
            logger.warning(f"Full generation failed: {e}")
        
        # Degrade to simpler model
        try:
            return await self._simple_generation(prompt)
        except Exception as e:
            logger.warning(f"Simple generation failed: {e}")
        
        # Degrade to template-based response
        return self._template_response(prompt)
    
    async def _full_generation(self, prompt: str) -> str:
        """Full-featured generation."""
        llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        response = await llm.ainvoke(prompt)
        return response.content
    
    async def _simple_generation(self, prompt: str) -> str:
        """Simpler model generation."""
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        response = await llm.ainvoke(prompt)
        return response.content
    
    def _template_response(self, prompt: str) -> str:
        """Template-based fallback."""
        return f"I apologize, but I'm experiencing technical difficulties. Your query was: {prompt[:50]}..."
```

### Step 6: Error Recovery and Compensation

Implement recovery and compensation patterns:

```python
from typing import Callable, List

class CompensationAction:
    """Represents a compensation action for rollback."""
    
    def __init__(self, action: Callable, *args, **kwargs):
        self.action = action
        self.args = args
        self.kwargs = kwargs
    
    async def execute(self):
        """Execute compensation."""
        if asyncio.iscoroutinefunction(self.action):
            await self.action(*self.args, **self.kwargs)
        else:
            self.action(*self.args, **self.kwargs)

class TransactionalOperation:
    """Transactional operation with compensation."""
    
    def __init__(self):
        self.actions: List[Callable] = []
        self.compensations: List[CompensationAction] = []
    
    def add_action(self, action: Callable, compensation: Callable = None, *args, **kwargs):
        """Add action with optional compensation."""
        self.actions.append(action)
        if compensation:
            self.compensations.append(CompensationAction(compensation, *args, **kwargs))
    
    async def execute(self) -> bool:
        """Execute all actions, compensating on failure."""
        executed = []
        
        try:
            for i, action in enumerate(self.actions):
                if asyncio.iscoroutinefunction(action):
                    await action()
                else:
                    action()
                executed.append(i)
            
            return True
        
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            # Compensate in reverse order
            for i in reversed(executed):
                if i < len(self.compensations):
                    try:
                        await self.compensations[i].execute()
                    except Exception as comp_error:
                        logger.error(f"Compensation failed: {comp_error}")
            
            return False

# Usage
async def create_user_profile(user_id: str, data: dict):
    """Create user profile."""
    # Implementation
    pass

async def delete_user_profile(user_id: str):
    """Delete user profile (compensation)."""
    # Implementation
    pass

transaction = TransactionalOperation()
transaction.add_action(
    lambda: create_user_profile("user_123", {}),
    compensation=lambda: delete_user_profile("user_123")
)

success = await transaction.execute()
```

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
import logging
from langchain_openai import ChatOpenAI
import httpx

logger = logging.getLogger(__name__)

# Basic retry decorator
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)
async def unreliable_api_call(endpoint: str) -> str:
    """API call with automatic retry."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.text

# Retry with specific exceptions
from httpx import HTTPStatusError, TimeoutException

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=1, max=60),
    retry=retry_if_exception_type((HTTPStatusError, TimeoutException)),
    reraise=True
)
async def robust_api_call(url: str) -> dict:
    """Retry on specific exceptions only."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Retry LLM calls
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception)
)
async def retryable_llm_call(prompt: str) -> str:
    """LLM call with retry."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = await llm.ainvoke(prompt)
    return response.content
```

```python
from tenacity import (
    retry,
    stop_after_delay,
    wait_fixed,
    wait_random,
    wait_chain,
    retry_if_result,
    retry_if_exception_message
)

# Retry until timeout
@retry(
    stop=stop_after_delay(30),  # Stop after 30 seconds
    wait=wait_fixed(2)
)
async def retry_until_timeout():
    """Retry until time limit."""
    # Implementation
    pass

# Random wait between retries
@retry(
    stop=stop_after_attempt(5),
    wait=wait_random(min=1, max=5)  # Random 1-5 seconds
)
async def retry_with_random_wait():
    """Retry with random wait."""
    pass

# Chained wait strategy
@retry(
    stop=stop_after_attempt(5),
    wait=wait_chain(
        wait_fixed(1) * 3,  # Wait 1s for first 3 attempts
        wait_exponential(multiplier=2, min=2, max=10)  # Then exponential
    )
)
async def retry_with_chained_wait():
    """Retry with chained wait strategy."""
    pass

# Retry based on result
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_result(lambda result: result is None or result == "")
)
async def retry_on_empty_result():
    """Retry if result is empty."""
    result = await some_operation()
    return result

# Retry based on exception message
@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_message(match=".*rate limit.*")
)
async def retry_on_rate_limit():
    """Retry only on rate limit errors."""
    # Implementation
    pass
```

```python
from typing import Callable, List, Any
import asyncio

class FallbackChain:
    """Execute functions in order until one succeeds."""
    
    def __init__(self, fallbacks: List[Callable]):
        self.fallbacks = fallbacks
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute fallbacks in order."""
        last_error = None
        
        for i, fallback in enumerate(self.fallbacks):
            try:
                if asyncio.iscoroutinefunction(fallback):
                    result = await fallback(*args, **kwargs)
                else:
                    result = fallback(*args, **kwargs)
                
                # Success - return result
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"Fallback {i} failed: {e}")
                continue
        
        # All fallbacks failed
        raise Exception(f"All fallbacks failed. Last error: {last_error}")

# Usage with multiple LLM providers
async def primary_llm(prompt: str) -> str:
    """Primary LLM provider."""
    llm = ChatOpenAI(model="gpt-4")
    response = await llm.ainvoke(prompt)
    return response.content

async def fallback_llm(prompt: str) -> str:
    """Fallback LLM provider."""
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(model="claude-3-5-sonnet")
    response = await llm.ainvoke(prompt)
    return response.content

async def local_fallback(prompt: str) -> str:
    """Local fallback (e.g., cached response)."""
    return "Default response from cache"

# Create fallback chain
llm_chain = FallbackChain([primary_llm, fallback_llm, local_fallback])

# Use fallback chain
try:
    result = await llm_chain.execute("What is Python?")
except Exception as e:
    logger.error(f"All LLM providers failed: {e}")

# Fallback with default value
async def safe_llm_call(prompt: str, default: str = "Unable to generate response") -> str:
    """LLM call with default fallback."""
    try:
        llm = ChatOpenAI(model="gpt-4")
        response = await llm.ainvoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return default
```

```python
from enum import Enum
from datetime import datetime
from typing import Callable, Optional
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.failure_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        # Execute function
        try:
            if asyncio.iscoroutinefunction(func):
                result = asyncio.run(func(*args, **kwargs))
            else:
                result = func(*args, **kwargs)
            
            # Success - reset if half-open
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise e
    
    async def acall(self, func: Callable, *args, **kwargs):
        """Async version of call."""
        if self.state == CircuitState.OPEN:
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.failure_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise e

# Usage
circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    expected_exception=Exception
)

async def protected_api_call(url: str) -> dict:
    """API call protected by circuit breaker."""
    async def _call():
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    
    return await circuit_breaker.acall(_call)
```

```python
from typing import Dict, List
from pydantic import BaseModel

class DegradedResponse(BaseModel):
    """Response with degradation metadata."""
    data: Dict
    degraded_features: List[str]
    full_response: bool

class GracefulDegradation:
    """Implement graceful degradation patterns."""
    
    async def get_user_profile(self, user_id: str) -> DegradedResponse:
        """Get user profile with graceful degradation."""
        degraded_features = []
        profile = {}
        
        # Try to get full profile
        try:
            full_profile = await self._fetch_full_profile(user_id)
            return DegradedResponse(
                data=full_profile,
                degraded_features=[],
                full_response=True
            )
        except Exception as e:
            logger.warning(f"Full profile fetch failed: {e}")
        
        # Degrade to cached profile
        try:
            cached_profile = await self._get_cached_profile(user_id)
            degraded_features.append("real_time_data")
            profile.update(cached_profile)
        except Exception as e:
            logger.warning(f"Cached profile fetch failed: {e}")
            degraded_features.append("cached_data")
        
        # Degrade to minimal profile
        try:
            minimal_profile = await self._get_minimal_profile(user_id)
            profile.update(minimal_profile)
        except Exception as e:
            logger.error(f"Minimal profile fetch failed: {e}")
            # Return empty profile as last resort
            profile = {"user_id": user_id, "status": "degraded"}
        
        return DegradedResponse(
            data=profile,
            degraded_features=degraded_features,
            full_response=False
        )
    
    async def _fetch_full_profile(self, user_id: str) -> Dict:
        """Fetch full profile from primary source."""
        # Implementation
        pass
    
    async def _get_cached_profile(self, user_id: str) -> Dict:
        """Get cached profile."""
        # Implementation
        pass
    
    async def _get_minimal_profile(self, user_id: str) -> Dict:
        """Get minimal profile from fallback."""
        # Implementation
        pass

# Graceful degradation for LLM features
class LLMDegradation:
    """Graceful degradation for LLM features."""
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response with feature degradation."""
        # Try full-featured generation
        try:
            return await self._full_generation(prompt)
        except Exception as e:
            logger.warning(f"Full generation failed: {e}")
        
        # Degrade to simpler model
        try:
            return await self._simple_generation(prompt)
        except Exception as e:
            logger.warning(f"Simple generation failed: {e}")
        
        # Degrade to template-based response
        return self._template_response(prompt)
    
    async def _full_generation(self, prompt: str) -> str:
        """Full-featured generation."""
        llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        response = await llm.ainvoke(prompt)
        return response.content
    
    async def _simple_generation(self, prompt: str) -> str:
        """Simpler model generation."""
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        response = await llm.ainvoke(prompt)
        return response.content
    
    def _template_response(self, prompt: str) -> str:
        """Template-based fallback."""
        return f"I apologize, but I'm experiencing technical difficulties. Your query was: {prompt[:50]}..."
```

```python
from typing import Callable, List

class CompensationAction:
    """Represents a compensation action for rollback."""
    
    def __init__(self, action: Callable, *args, **kwargs):
        self.action = action
        self.args = args
        self.kwargs = kwargs
    
    async def execute(self):
        """Execute compensation."""
        if asyncio.iscoroutinefunction(self.action):
            await self.action(*self.args, **self.kwargs)
        else:
            self.action(*self.args, **self.kwargs)

class TransactionalOperation:
    """Transactional operation with compensation."""
    
    def __init__(self):
        self.actions: List[Callable] = []
        self.compensations: List[CompensationAction] = []
    
    def add_action(self, action: Callable, compensation: Callable = None, *args, **kwargs):
        """Add action with optional compensation."""
        self.actions.append(action)
        if compensation:
            self.compensations.append(CompensationAction(compensation, *args, **kwargs))
    
    async def execute(self) -> bool:
        """Execute all actions, compensating on failure."""
        executed = []
        
        try:
            for i, action in enumerate(self.actions):
                if asyncio.iscoroutinefunction(action):
                    await action()
                else:
                    action()
                executed.append(i)
            
            return True
        
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            # Compensate in reverse order
            for i in reversed(executed):
                if i < len(self.compensations):
                    try:
                        await self.compensations[i].execute()
                    except Exception as comp_error:
                        logger.error(f"Compensation failed: {comp_error}")
            
            return False

# Usage
async def create_user_profile(user_id: str, data: dict):
    """Create user profile."""
    # Implementation
    pass

async def delete_user_profile(user_id: str):
    """Delete user profile (compensation)."""
    # Implementation
    pass

transaction = TransactionalOperation()
transaction.add_action(
    lambda: create_user_profile("user_123", {}),
    compensation=lambda: delete_user_profile("user_123")
)

success = await transaction.execute()
```

## Error Handling Patterns
| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| **Retry** | Transient failures | Tenacity decorators |
| **Fallback** | Service unavailability | FallbackChain |
| **Circuit Breaker** | Cascading failures | CircuitBreaker class |
| **Graceful Degradation** | Partial failures | Feature degradation |
| **Compensation** | Transaction rollback | Compensation actions |
| **Timeout** | Long-running operations | asyncio.timeout |

## Best Practices
- Use exponential backoff for retries
- Set appropriate retry limits
- Implement circuit breakers for external services
- Provide meaningful fallbacks
- Log all errors for debugging
- Monitor error rates
- Use timeouts for all I/O operations
- Implement graceful degradation
- Test error scenarios
- Document error handling strategies

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Infinite retries | Set retry limits |
| No backoff | Use exponential backoff |
| Ignoring errors | Handle and log all errors |
| No timeouts | Set timeouts for I/O |
| No fallbacks | Implement fallback chains |
| Retrying non-retryable errors | Check error types |
| No circuit breakers | Add circuit breakers |
| Silent failures | Log and report errors |
| No compensation | Implement rollback logic |
| Ignoring rate limits | Handle rate limit errors |

## Related
- Skill: `caching-optimization`
- Skill: `tool-usage`
- Skill: `langchain-usage`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: tenacity, langchain-core, langchain-openai, httpx
