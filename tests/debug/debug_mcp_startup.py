import sys
import os
import logging
import time

# Setup logging to stderr
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("debug_mcp")

# Add project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, PROJECT_ROOT)


def test_startup():
    logger.info("Starting MCP Server Simulation...")
    t0 = time.time()

    try:
        from scripts.ai.rag.rag_optimized import get_rag

        logger.info(f"Imported get_rag in {time.time()-t0:.2f}s")

        logger.info("Calling get_rag(warmup=True)...")
        rag = get_rag(warmup=True)

        logger.info(f"RAG Initialized in {time.time()-t0:.2f}s")

        logger.info("Running test query...")
        res = rag.query("test")
        logger.info(f"Query Result: {res.keys()}")

    except Exception as e:
        logger.error(f"Startup Failed: {e}", exc_info=True)


if __name__ == "__main__":
    test_startup()
