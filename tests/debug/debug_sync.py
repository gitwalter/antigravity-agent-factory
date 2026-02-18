import sys
import os
import logging

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, PROJECT_ROOT)

from scripts.ai.rag.rag_optimized import get_rag

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debug_sync")


def test_sync_state():
    rag = get_rag(warmup=False)

    # 1. Check Store (should trigger hydration)
    logger.info("Checking Store...")
    keys = list(rag.store.yield_keys())
    logger.info(f"Store Keys: {len(keys)}")

    if len(keys) == 0:
        logger.error("Store is empty! Hydration failed?")

    # 2. Check Qdrant
    logger.info("Checking Qdrant...")
    try:
        count = rag.client.count(collection_name="ebook_library").count
        logger.info(f"Qdrant Count: {count}")
    except Exception as e:
        logger.error(f"Qdrant Check Failed: {e}")

    # 3. Check Condition & Sync
    if count == 0 and len(keys) > 0:
        logger.info("CONDITION MET: Calling ensure_ready() to trigger sync...")
        rag.ensure_ready()
    else:
        logger.info("CONDITION NOT MET.")


if __name__ == "__main__":
    test_sync_state()
