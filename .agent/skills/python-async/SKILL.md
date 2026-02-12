---
description: asyncio patterns for web apps, async context managers, Concurrent task
  execution (gather, TaskGroup), Async generators, Background task scheduling (APScheduler,
  Celery), Connection pool management
name: python-async
type: skill
---

# Python Async

asyncio patterns for web apps, async context managers, Concurrent task execution (gather, TaskGroup), Async generators, Background task scheduling (APScheduler, Celery), Connection pool management

## 
# Python Async Patterns Skill

Implement production-ready async patterns for Python web applications using asyncio, concurrent execution, and background tasks.

## 
# Python Async Patterns Skill

Implement production-ready async patterns for Python web applications using asyncio, concurrent execution, and background tasks.

## Process
### Step 1: Async Context Managers

Use async context managers for resource management:

```python
# src/core/async_context.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aiohttp
import aiofiles

@asynccontextmanager
async def get_http_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Async context manager for HTTP session."""
    async with aiohttp.ClientSession() as session:
        yield session

@asynccontextmanager
async def get_file_handle(filepath: str) -> AsyncGenerator[aiofiles.AsyncFileIO, None]:
    """Async context manager for file operations."""
    async with aiofiles.open(filepath, 'r') as file:
        yield file

# Usage
async def fetch_data(url: str) -> dict:
    """Fetch data using async context manager."""
    async with get_http_session() as session:
        async with session.get(url) as response:
            return await response.json()

async def read_file(filepath: str) -> str:
    """Read file using async context manager."""
    async with get_file_handle(filepath) as file:
        return await file.read()
```

### Step 2: Concurrent Task Execution

Use `asyncio.gather()` and `TaskGroup` for concurrent operations:

```python
import asyncio
from typing import List

# Using asyncio.gather()
async def fetch_multiple_urls(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch single URL."""
    async with session.get(url) as response:
        return await response.json()

# Using TaskGroup (Python 3.11+)
async def process_users_concurrently(users: List[dict]) -> List[dict]:
    """Process multiple users concurrently with TaskGroup."""
    async def process_user(user: dict) -> dict:
        # Process user data
        await asyncio.sleep(0.1)  # Simulate async operation
        return {"id": user["id"], "processed": True}
    
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_user(user)) for user in users]
    
    results = [task.result() for task in tasks]
    return results

# With error handling
async def fetch_with_error_handling(urls: List[str]) -> List[dict]:
    """Fetch URLs with proper error handling."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        successful_results = [
            r for r in results
            if not isinstance(r, Exception)
        ]
        return successful_results
```

### Step 3: Async Generators

Use async generators for streaming data:

```python
# src/core/async_generators.py
from typing import AsyncGenerator
import aiofiles

async def read_file_lines(filepath: str) -> AsyncGenerator[str, None]:
    """Read file line by line asynchronously."""
    async with aiofiles.open(filepath, 'r') as file:
        async for line in file:
            yield line.strip()

async def process_large_dataset(data_source: AsyncGenerator[dict, None]) -> AsyncGenerator[dict, None]:
    """Process large dataset using async generator."""
    async for item in data_source:
        # Process item
        processed = await process_item(item)
        yield processed

async def process_item(item: dict) -> dict:
    """Process single item."""
    await asyncio.sleep(0.01)  # Simulate processing
    return {"id": item["id"], "processed": True}

# Usage
async def main():
    async for line in read_file_lines("large_file.txt"):
        print(line)
```

### Step 4: Background Task Scheduling

Use APScheduler for periodic tasks:

```python
# src/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

scheduler = AsyncIOScheduler()

async def cleanup_old_data():
    """Cleanup old data periodically."""
    print("Cleaning up old data...")
    # Cleanup logic here
    await asyncio.sleep(1)

async def send_daily_report():
    """Send daily report."""
    print("Sending daily report...")
    # Report logic here
    await asyncio.sleep(1)

# Schedule periodic tasks
scheduler.add_job(
    cleanup_old_data,
    IntervalTrigger(hours=1),
    id='cleanup',
    replace_existing=True
)

scheduler.add_job(
    send_daily_report,
    CronTrigger(hour=9, minute=0),  # 9 AM daily
    id='daily_report',
    replace_existing=True
)

# Start scheduler
scheduler.start()

# In FastAPI lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
```

### Step 5: Celery for Distributed Tasks

Use Celery for distributed background tasks:

```python
# src/core/celery_app.py
from celery import Celery
from celery.schedules import crontab
import os

celery_app = Celery(
    "myapp",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="process_user_data")
async def process_user_data_async(user_id: int):
    """Process user data asynchronously."""
    # Async processing logic
    await asyncio.sleep(1)
    return {"user_id": user_id, "processed": True}

@celery_app.task(name="send_email")
def send_email_task(email: str, subject: str, body: str):
    """Send email task."""
    # Email sending logic
    print(f"Sending email to {email}")
    return {"status": "sent"}

# Periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-every-hour": {
        "task": "cleanup_old_data",
        "schedule": crontab(minute=0),  # Every hour
    },
    "daily-report": {
        "task": "send_daily_report",
        "schedule": crontab(hour=9, minute=0),  # 9 AM daily
    },
}

# Usage in FastAPI
from .core.celery_app import process_user_data_async, send_email_task

@router.post("/users/{user_id}/process")
async def process_user(user_id: int):
    """Trigger user processing."""
    task = process_user_data_async.delay(user_id)
    return {"task_id": task.id, "status": "processing"}
```

### Step 6: Connection Pool Management

Manage connection pools for async operations:

```python
# src/core/connection_pool.py
import aiohttp
from typing import Optional
import asyncio

class ConnectionPool:
    def __init__(self, max_connections: int = 100):
        self.max_connections = max_connections
        self._session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create session."""
        if self._session is None or self._session.closed:
            async with self._lock:
                if self._session is None or self._session.closed:
                    connector = aiohttp.TCPConnector(
                        limit=self.max_connections,
                        limit_per_host=20,
                        ttl_dns_cache=300,
                        force_close=False
                    )
                    timeout = aiohttp.ClientTimeout(
                        total=30,
                        connect=10,
                        sock_read=10
                    )
                    self._session = aiohttp.ClientSession(
                        connector=connector,
                        timeout=timeout
                    )
        return self._session
    
    async def close(self):
        """Close session."""
        if self._session and not self._session.closed:
            await self._session.close()

# Global pool instance
http_pool = ConnectionPool(max_connections=100)

# Usage
async def fetch_with_pool(url: str) -> dict:
    """Fetch using connection pool."""
    session = await http_pool.get_session()
    async with session.get(url) as response:
        return await response.json()

# Cleanup on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_pool.close()
```

### Step 7: Async Queue Patterns

Use asyncio queues for producer-consumer patterns:

```python
# src/core/async_queue.py
import asyncio
from typing import Optional
from collections.abc import AsyncIterator

class AsyncQueueProcessor:
    def __init__(self, max_workers: int = 5):
        self.queue = asyncio.Queue(maxsize=100)
        self.max_workers = max_workers
        self.workers: List[asyncio.Task] = []
    
    async def producer(self, items: List[dict]):
        """Produce items to queue."""
        for item in items:
            await self.queue.put(item)
        # Signal end
        for _ in range(self.max_workers):
            await self.queue.put(None)
    
    async def worker(self, worker_id: int):
        """Worker to process items."""
        while True:
            item = await self.queue.get()
            if item is None:
                break
            try:
                await self.process_item(item, worker_id)
            finally:
                self.queue.task_done()
    
    async def process_item(self, item: dict, worker_id: int):
        """Process single item."""
        print(f"Worker {worker_id} processing {item}")
        await asyncio.sleep(0.1)
    
    async def process(self, items: List[dict]):
        """Process items with workers."""
        # Start workers
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.max_workers)
        ]
        
        # Start producer
        await self.producer(items)
        
        # Wait for completion
        await self.queue.join()
        
        # Cancel workers
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)

# Usage
processor = AsyncQueueProcessor(max_workers=5)
items = [{"id": i} for i in range(100)]
await processor.process(items)
```

```python
# src/core/async_context.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aiohttp
import aiofiles

@asynccontextmanager
async def get_http_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Async context manager for HTTP session."""
    async with aiohttp.ClientSession() as session:
        yield session

@asynccontextmanager
async def get_file_handle(filepath: str) -> AsyncGenerator[aiofiles.AsyncFileIO, None]:
    """Async context manager for file operations."""
    async with aiofiles.open(filepath, 'r') as file:
        yield file

# Usage
async def fetch_data(url: str) -> dict:
    """Fetch data using async context manager."""
    async with get_http_session() as session:
        async with session.get(url) as response:
            return await response.json()

async def read_file(filepath: str) -> str:
    """Read file using async context manager."""
    async with get_file_handle(filepath) as file:
        return await file.read()
```

```python
import asyncio
from typing import List

# Using asyncio.gather()
async def fetch_multiple_urls(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch single URL."""
    async with session.get(url) as response:
        return await response.json()

# Using TaskGroup (Python 3.11+)
async def process_users_concurrently(users: List[dict]) -> List[dict]:
    """Process multiple users concurrently with TaskGroup."""
    async def process_user(user: dict) -> dict:
        # Process user data
        await asyncio.sleep(0.1)  # Simulate async operation
        return {"id": user["id"], "processed": True}
    
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_user(user)) for user in users]
    
    results = [task.result() for task in tasks]
    return results

# With error handling
async def fetch_with_error_handling(urls: List[str]) -> List[dict]:
    """Fetch URLs with proper error handling."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        successful_results = [
            r for r in results
            if not isinstance(r, Exception)
        ]
        return successful_results
```

```python
# src/core/async_generators.py
from typing import AsyncGenerator
import aiofiles

async def read_file_lines(filepath: str) -> AsyncGenerator[str, None]:
    """Read file line by line asynchronously."""
    async with aiofiles.open(filepath, 'r') as file:
        async for line in file:
            yield line.strip()

async def process_large_dataset(data_source: AsyncGenerator[dict, None]) -> AsyncGenerator[dict, None]:
    """Process large dataset using async generator."""
    async for item in data_source:
        # Process item
        processed = await process_item(item)
        yield processed

async def process_item(item: dict) -> dict:
    """Process single item."""
    await asyncio.sleep(0.01)  # Simulate processing
    return {"id": item["id"], "processed": True}

# Usage
async def main():
    async for line in read_file_lines("large_file.txt"):
        print(line)
```

```python
# src/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

scheduler = AsyncIOScheduler()

async def cleanup_old_data():
    """Cleanup old data periodically."""
    print("Cleaning up old data...")
    # Cleanup logic here
    await asyncio.sleep(1)

async def send_daily_report():
    """Send daily report."""
    print("Sending daily report...")
    # Report logic here
    await asyncio.sleep(1)

# Schedule periodic tasks
scheduler.add_job(
    cleanup_old_data,
    IntervalTrigger(hours=1),
    id='cleanup',
    replace_existing=True
)

scheduler.add_job(
    send_daily_report,
    CronTrigger(hour=9, minute=0),  # 9 AM daily
    id='daily_report',
    replace_existing=True
)

# Start scheduler
scheduler.start()

# In FastAPI lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
```

```python
# src/core/celery_app.py
from celery import Celery
from celery.schedules import crontab
import os

celery_app = Celery(
    "myapp",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="process_user_data")
async def process_user_data_async(user_id: int):
    """Process user data asynchronously."""
    # Async processing logic
    await asyncio.sleep(1)
    return {"user_id": user_id, "processed": True}

@celery_app.task(name="send_email")
def send_email_task(email: str, subject: str, body: str):
    """Send email task."""
    # Email sending logic
    print(f"Sending email to {email}")
    return {"status": "sent"}

# Periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-every-hour": {
        "task": "cleanup_old_data",
        "schedule": crontab(minute=0),  # Every hour
    },
    "daily-report": {
        "task": "send_daily_report",
        "schedule": crontab(hour=9, minute=0),  # 9 AM daily
    },
}

# Usage in FastAPI
from .core.celery_app import process_user_data_async, send_email_task

@router.post("/users/{user_id}/process")
async def process_user(user_id: int):
    """Trigger user processing."""
    task = process_user_data_async.delay(user_id)
    return {"task_id": task.id, "status": "processing"}
```

```python
# src/core/connection_pool.py
import aiohttp
from typing import Optional
import asyncio

class ConnectionPool:
    def __init__(self, max_connections: int = 100):
        self.max_connections = max_connections
        self._session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create session."""
        if self._session is None or self._session.closed:
            async with self._lock:
                if self._session is None or self._session.closed:
                    connector = aiohttp.TCPConnector(
                        limit=self.max_connections,
                        limit_per_host=20,
                        ttl_dns_cache=300,
                        force_close=False
                    )
                    timeout = aiohttp.ClientTimeout(
                        total=30,
                        connect=10,
                        sock_read=10
                    )
                    self._session = aiohttp.ClientSession(
                        connector=connector,
                        timeout=timeout
                    )
        return self._session
    
    async def close(self):
        """Close session."""
        if self._session and not self._session.closed:
            await self._session.close()

# Global pool instance
http_pool = ConnectionPool(max_connections=100)

# Usage
async def fetch_with_pool(url: str) -> dict:
    """Fetch using connection pool."""
    session = await http_pool.get_session()
    async with session.get(url) as response:
        return await response.json()

# Cleanup on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_pool.close()
```

```python
# src/core/async_queue.py
import asyncio
from typing import Optional
from collections.abc import AsyncIterator

class AsyncQueueProcessor:
    def __init__(self, max_workers: int = 5):
        self.queue = asyncio.Queue(maxsize=100)
        self.max_workers = max_workers
        self.workers: List[asyncio.Task] = []
    
    async def producer(self, items: List[dict]):
        """Produce items to queue."""
        for item in items:
            await self.queue.put(item)
        # Signal end
        for _ in range(self.max_workers):
            await self.queue.put(None)
    
    async def worker(self, worker_id: int):
        """Worker to process items."""
        while True:
            item = await self.queue.get()
            if item is None:
                break
            try:
                await self.process_item(item, worker_id)
            finally:
                self.queue.task_done()
    
    async def process_item(self, item: dict, worker_id: int):
        """Process single item."""
        print(f"Worker {worker_id} processing {item}")
        await asyncio.sleep(0.1)
    
    async def process(self, items: List[dict]):
        """Process items with workers."""
        # Start workers
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.max_workers)
        ]
        
        # Start producer
        await self.producer(items)
        
        # Wait for completion
        await self.queue.join()
        
        # Cancel workers
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)

# Usage
processor = AsyncQueueProcessor(max_workers=5)
items = [{"id": i} for i in range(100)]
await processor.process(items)
```

## Best Practices
- Use async context managers for resource cleanup
- Use `asyncio.gather()` for concurrent operations
- Use `TaskGroup` (Python 3.11+) for structured concurrency
- Handle exceptions in concurrent operations
- Use async generators for streaming large datasets
- Configure connection pools appropriately
- Use Celery for distributed tasks
- Use APScheduler for periodic tasks
- Always await async functions
- Use proper timeout handling
- Clean up resources on shutdown
- Monitor async task execution

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Blocking I/O in async code | Use async libraries (aiohttp, aiofiles) |
| Not awaiting async functions | Always use await |
| Missing exception handling | Wrap in try/except |
| No timeout handling | Use asyncio.wait_for with timeout |
| Resource leaks | Use async context managers |
| Too many concurrent tasks | Limit concurrency with semaphores |

## Related
- Knowledge: `knowledge/python-production-patterns.json`
- Skill: `fastapi-development` for web app integration
- Skill: `sqlalchemy-patterns` for async database access

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: asyncio, aiohttp, aiofiles, celery, apscheduler
> - Knowledge: python-production-patterns.json
