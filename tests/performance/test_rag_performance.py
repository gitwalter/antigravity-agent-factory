import time
import statistics
import sys
import os
import logging

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag_perf_test")


def measure_initialization():
    logger.info("Measuring initialization time...")
    start_time = time.time()
    from scripts.ai.rag.rag_optimized import OptimizedRAG

    rag = OptimizedRAG(warmup=True)
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Initialization took: {duration:.4f} seconds")
    return rag, duration


def measure_queries(rag, queries, warm=False):
    durations = []
    logger.info(f"Measuring {'warm' if warm else 'cold'} queries...")

    for q in queries:
        start = time.time()
        rag.query(q)
        end = time.time()
        durations.append(end - start)

    avg = statistics.mean(durations)
    median = statistics.median(durations)
    logger.info(
        f"{'Warm' if warm else 'Cold'} queries - Avg: {avg:.4f}s, Median: {median:.4f}s"
    )
    return durations


def measure_memory_tiers():
    from scripts.mcp_infra.servers.rag.rag_mcp_server import _do_search, prepare_context

    tiers = ["memory_semantic", "memory_procedural", "memory_entity", "memory_summary"]

    print("\n--- Memory Tier Benchmarking ---")
    results = {}
    for tier in tiers:
        start = time.time()
        _do_search("test query", tier)
        duration = time.time() - start
        results[tier] = duration
        print(f"{tier:20}: {duration:.4f}s")

    start_fusion = time.time()
    prepare_context("test query")
    fusion_duration = time.time() - start_fusion
    print(f"{'prepare_context':20}: {fusion_duration:.4f}s")
    return results, fusion_duration


def main():
    print("=== RAG Performance Test ===")

    # Measure Initialization
    rag, init_time = measure_initialization()

    # Test Queries based on actual library content
    test_queries = [
        "What are the core principles of AI agent governance?",
        "Explain the concept of Agentic RAG and how it differs from standard RAG.",
        "What initiates the action in an intelligent agent?",
        "Summary of Claude's constitution",
        "How to build effective AI agents?",
    ]

    # 1. First query (might be slower if lazy loading happens)
    first_query_start = time.time()
    rag.query("warmup query")
    first_query_time = time.time() - first_query_start
    print(f"First query (after init): {first_query_time:.4f}s")

    # 2. Warm queries
    warm_times = measure_queries(rag, test_queries, warm=True)

    # 3. Memory Tiers
    memory_results, fusion_time = measure_memory_tiers()

    print("\n=== Final Performance Summary ===")
    print(f"Initialization       : {init_time:.4f}s")
    print(f"Avg Library Query    : {statistics.mean(warm_times):.4f}s")
    print(f"Prepare Context Speed: {fusion_time:.4f}s")
    print(f"Max Memory Tier Speed: {max(memory_results.values()):.4f}s")

    # Assertions for "Fast" Retrieval
    assert (
        max(memory_results.values()) < 1.0
    ), "Memory tier retrieval is too slow (>1.0s)"
    assert fusion_time < 2.5, "Context preparation is too slow (>2.5s)"
    print("\n✅ PERFORMANCE TARGETS MET")


if __name__ == "__main__":
    main()
