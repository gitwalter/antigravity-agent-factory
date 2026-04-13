import pytest
import time
import subprocess
import os
import sys

# Targets from implementation plan
TARGET_STARTUP_LIST_TOOLS = 2.0  # Seconds
TARGET_WARMUP_READY = 30.0  # Seconds
TARGET_READ_LATENCY = 0.200  # 200ms
TARGET_WRITE_LATENCY = 0.500  # 500ms


def test_import_speed():
    """Verify that importing our core services is fast (due to lazy loading)."""
    # Use a separate process to avoid cached imports
    code = """
import sys
import os
sys.path.append(os.getcwd())
import time
start = time.perf_counter()
from scripts.memory.memory_store import MemoryStore
print(time.perf_counter() - start)
"""
    try:
        # Use sys.executable to run with the current environment's python directly
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            check=True,
            cwd=os.getcwd(),
        )
    except subprocess.CalledProcessError as e:
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise
    import_time = float(result.stdout.strip())
    print(f"MemoryStore import time: {import_time:.4f}s")
    assert (
        import_time < TARGET_STARTUP_LIST_TOOLS
    ), f"Import took too long: {import_time}s"


@pytest.mark.benchmark
def test_read_write_latency():
    """Benchmark raw MemoryStore operations."""
    from scripts.memory.memory_store import MemoryStore

    store = MemoryStore()

    # Warmup - ensure model is loaded into memory
    _ = store.embedding_service.embed_single("warmup")
    store.search("warmup", memory_type="semantic", k=1)

    # Write Latency
    start = time.perf_counter()
    store.add_memory(
        content=f"Performance test entry {time.time()}",
        metadata={"test": "performance"},
        memory_type="episodic",
    )
    write_time = time.perf_counter() - start
    print(f"Write latency: {write_time:.4f}s")

    # Read Latency
    start = time.perf_counter()
    store.search("performance test entry", memory_type="episodic", k=5)
    read_time = time.perf_counter() - start
    print(f"Read latency: {read_time:.4f}s")

    assert write_time < TARGET_WRITE_LATENCY
    assert read_time < TARGET_READ_LATENCY
