import time
import sys
import os


def profile_imports():
    print("--- Import Profiling ---")

    start = time.perf_counter()
    import torch

    print(f"import torch: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    import sentence_transformers

    print(f"import sentence_transformers: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    import qdrant_client

    print(f"import qdrant_client: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    import scripts.memory.memory_store

    print(f"import scripts.memory.memory_store: {time.perf_counter() - start:.4f}s")


def profile_services():
    print("\n--- Service Initialization Profiling ---")

    # We need to add the project root to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.append(project_root)

    from scripts.memory.embedding_service import EmbeddingService
    from scripts.memory.memory_store import MemoryStore

    start = time.perf_counter()
    # Test lazy loading first
    embed_service = EmbeddingService(lazy_load=True)
    print(f"EmbeddingService(lazy_load=True) init: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    embed_service._load_model()
    print(
        f"EmbeddingService._load_model(): {time.perf_counter() - start:.4f}s (Actual warmup)"
    )

    start = time.perf_counter()
    store = MemoryStore()
    print(f"MemoryStore() init: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    # This might trigger qdrant connection
    _ = store.client
    print(f"MemoryStore.client access: {time.perf_counter() - start:.4f}s")


if __name__ == "__main__":
    profile_imports()
    profile_services()
