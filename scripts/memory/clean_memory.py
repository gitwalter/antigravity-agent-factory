"""
Clean Memory Utility
Use this script to completely wipe all SQLite exact-match memory databases and
all Qdrant semantic memory collections before a test run.
"""

import os
import logging
from qdrant_client import QdrantClient

from scripts.memory.memory_config import (
    SQLITE_DB_PATH,
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_SEMANTIC,
    COLLECTION_PROCEDURAL,
    COLLECTION_TOOLBOX,
    COLLECTION_ENTITY,
    COLLECTION_SUMMARY,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memory_cleaner")


def clean_state():
    # 1. Wipe SQLite
    logger.info("Checking SQLite Database...")
    if os.path.exists(SQLITE_DB_PATH):
        try:
            os.remove(SQLITE_DB_PATH)
            logger.info(f"Deleted SQLite exact-match database at {SQLITE_DB_PATH}")
        except Exception as e:
            logger.error(f"Failed to delete SQLite database: {e}")
    else:
        logger.info("SQLite database does not exist. (Already clean)")

    # 2. Wipe Qdrant Collections
    logger.info("Checking Qdrant Vector Data...")
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        collections_to_clean = [
            COLLECTION_SEMANTIC,
            COLLECTION_PROCEDURAL,
            COLLECTION_TOOLBOX,
            COLLECTION_ENTITY,
            COLLECTION_SUMMARY,
            "semantic",  # legacy
            "episodic",  # legacy
            "pending",  # legacy
        ]

        for col_name in collections_to_clean:
            # We don't check if it exists first, just try dropping - qdrant handles it gracefully if you catch the error
            try:
                # To be safe, let's explicitly check or just delete
                if client.collection_exists(col_name):
                    client.delete_collection(col_name)
                    logger.info(f"Dropped Qdrant collection: {col_name}")
                else:
                    logger.info(f"Qdrant collection {col_name} does not exist. (Clean)")
            except Exception as inner_e:
                logger.warning(f"Could not drop {col_name}: {inner_e}")

    except Exception as e:
        logger.error(f"Failed to connect to or clean Qdrant: {e}")

    logger.info("Memory Wipe Complete. You are starting with a clean state.")


if __name__ == "__main__":
    clean_state()
