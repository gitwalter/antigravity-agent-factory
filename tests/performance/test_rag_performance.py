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


def main():
    print("=== RAG Performance Test ===")

    # Measure Initialization
    rag, init_time = measure_initialization()

    # Test Queries based on actual library content
    test_queries = [
        "What are the core principles of AI agent governance?",  # From WEF/Practices docs
        "Explain the concept of Agentic RAG and how it differs from standard RAG.",  # From BSA blog
        "What initiates the action in an intelligent agent?",  # From Woodridge
        "Summary of Claude's constitution",  # From Claude's constitution
        "How to build effective AI agents?",  # From Practical Guide
    ]

    # 1. First query (might be slower if lazy loading happens, though warmup should handle it)
    first_query_start = time.time()
    rag.query("warmup query")
    first_query_time = time.time() - first_query_start
    print(f"First query (after init): {first_query_time:.4f}s")

    # 2. Warm queries
    warm_times = measure_queries(rag, test_queries, warm=True)

    print("\n=== Summary Results ===")
    print(f"Initialization: {init_time:.4f}s")
    print(f"Avg Warm Query: {statistics.mean(warm_times):.4f}s")
    print(f"Throughput: {1/statistics.mean(warm_times):.2f} queries/sec")


if __name__ == "__main__":
    main()
