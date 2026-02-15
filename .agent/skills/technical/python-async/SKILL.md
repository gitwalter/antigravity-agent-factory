---
description: Tactical Blueprint for high-performance Python Asyncio. Focuses on structured
  concurrency, resource safety, and resilient background processing.
name: python-async
type: skill
---
# Capability Manifest: Python Async Mastery

This blueprint provides the **procedural truth** for engineering high-performance, non-blocking systems using Python's `asyncio` ecosystem.

## When to Use

This skill should be used when completing tasks related to python async.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Structured Concurrency (Python 3.11+)
1.  **Prefer `TaskGroup`**: Always use `asyncio.TaskGroup()` for managing multiple tasks. It ensures that if one task fails, all others are cancelled, preventing "zombie" tasks.
2.  **Explicit Timeouts**: Wrap every network or I/O operation in `asyncio.wait_for(coro, timeout=X)`.
3.  **Shielding**: Use `asyncio.shield()` only when a task *must* complete even if the parent is cancelled (e.g., critical DB writes).

### Procedure 2: Resource Safety (Context Managers)
1.  **Async with Everything**: Use `async with` for every resource that supports it (Sessions, Files, Connections).
2.  **Manual Cleanup**: If a resource doesn't support `async with`, implement a `try...finally` block to ensure `await resource.close()` is called.
3.  **Connection Pooling**: Never create a new `aiohttp.ClientSession` for every request. Implement a singleton or lifespan-managed session pool.

### Procedure 3: Resilient Background Processing
1.  **Producer-Consumer (Queue)**: Use `asyncio.Queue` for local background processing. Implement 3+ workers to ensure throughput.
2.  **Graceful Shutdown**: Implement a signal handler that waits for the queue to empty (`await queue.join()`) before terminating the process.
3.  **Offloading Blockers**: Use `asyncio.to_thread()` to run CPU-bound or blocking I/O (e.g., legacy libs) in a separate thread without blocking the event loop.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Event Loop Lag** | Blocking I/O (e.g., `requests.get`) called in async code. | Identify the blocker via `loop.set_debug(True)`; replace with `aiohttp` or wrap in `to_thread()`. |
| **Silent Task Failure** | Background task raised an exception that wasn't awaited. | Attach a callback via `task.add_done_callback()` to log errors; use `TaskGroup` to ensure exceptions bubble up. |
| **Memory Leak (Zombie Tasks)** | `asyncio.create_task()` called without tracking the task or using a TaskGroup. | Move tasks into a managed list or use a TaskGroup context manager. |

## Idiomatic Code Patterns (The Gold Standard)

### The "Resilient" Worker Pattern
```python
async def worker(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()
        try:
            await process_item(item)
        except Exception as e:
            logger.error(f"Worker {worker_id} failed: {e}")
        finally:
            queue.task_done()
```

### The "FastAPI Lifespan" Session
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: Create global session
    app.state.http_client = aiohttp.ClientSession()
    yield
    # Teardown: Close global session
    await app.state.http_client.close()
```

## Prerequisites

| Action | Command / Tool |
| :--- | :--- |
| Debug Loop | `asyncio.run(main(), debug=True)` |
| Profile Async | `py-spy record -o profile.svg --pid <PID>` |
| Test Async | `pytest-asyncio` |

## Best Practices
Before finalized any async implementation:
- [ ] No blocking I/O (requests, time.sleep) in the event loop.
- [ ] All resources managed via `async with` or `lifespan`.
- [ ] Concurrency managed via `TaskGroup` or `Semaphore` (to prevent DDOSing backends).
- [ ] Graceful shutdown logic handles pending tasks.
