import os
import sys
import logging
import time

# Ensure project root is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.ai.rag.rag_optimized import OptimizedRAG, get_rag

# Configure logging to be very verbose for diagnostics
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("RepairLibrary")


def repair():
    logger.info("Starting Ebook Library Repair/Rebuild Process...")

    try:
        # Initialize RAG without automatic warmup to control the steps
        rag = OptimizedRAG(warmup=False)

        # 1. Check Paths
        logger.info(f"Parent store path: {rag.parent_store_path}")
        if not os.path.exists(rag.parent_store_path):
            logger.error(
                f"CRITICAL: Parent store path does not exist: {rag.parent_store_path}"
            )
            return

        # 2. Force Hydration & Initialization
        logger.info("Initializing RAG components and forcing hydration...")
        # Delete cache to force fresh reload from raw files
        cache_path = os.path.join(
            os.path.dirname(rag.parent_store_path), "parent_store_cache.json"
        )
        if os.path.exists(cache_path):
            logger.info(f"Removing old cache: {cache_path}")
            os.remove(cache_path)

        # ensure_ready() triggers:
        # 1. retriever property (initializes splitters, store, vectorstore)
        # 2. _hydrate_store() (via store initialization)
        # 3. _sync_vectors() (the actual repair logic)
        # 4. _warmup()
        rag.ensure_ready()

        keys = list(rag.store.yield_keys())
        logger.info(f"Loaded {len(keys)} documents into memory.")

        if len(keys) == 0:
            logger.error(
                "CRITICAL: No documents found to index. Hydration failed or store is empty."
            )
            return

        # 3. Check Qdrant State
        from scripts.ai.rag.rag_optimized import COLLECTION_NAME

        count = rag.client.count(collection_name=COLLECTION_NAME).count
        logger.info(f"Final document count in '{COLLECTION_NAME}': {count}")

        if count > 0:
            logger.info("✅ SUCCESS: Ebook Library has been repopulated.")
        else:
            logger.warning(
                "⚠️ REPAIR FINISHED but document count is still 0. Check logs for errors."
            )

    except Exception as e:
        logger.exception(f"❌ Repair failed with error: {e}")


if __name__ == "__main__":
    repair()
