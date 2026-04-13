"""
Memory Cleanup Service (SSGM Temporal Decay)
Enforces the SSGM Temporal Decay principle. Iterates over active episodic/transient
memories and prunes them if they exceed a specific age threshold (e.g. 7 days).
"""

import logging
from datetime import datetime, timedelta
from typing import List

from scripts.memory.memory_store import get_memory_store

logger = logging.getLogger(__name__)


class MemoryCleaner:
    def __init__(self, days_threshold: int = 7):
        self.days_threshold = days_threshold
        self.vector_store = get_memory_store()
        self.client = self.vector_store.client

    def cleanup_episodic_memory(self) -> int:
        """
        Prunes episodic memories that are older than the threshold.
        Since qdrant doesn't support complex math expressions directly,
        we fetch the points, check their metadata locally, and batch delete them.
        """
        collection_name = "episodic"  # Note: if episodic isn't defined explicitly, it might just be the literal word
        removed_count = 0

        try:
            # First check if the collection exists
            collections = [c.name for c in self.client.get_collections().collections]
            if collection_name not in collections:
                logger.info(
                    f"Collection {collection_name} does not exist. Nothing to clean."
                )
                return 0

            # Get points
            cutoff_date = datetime.now() - timedelta(days=self.days_threshold)

            from qdrant_client.http.models import Filter, FieldCondition, Range

            # Using scroll to iterate over all entries
            offset = None
            while True:
                results, offset = self.client.scroll(
                    collection_name=collection_name,
                    limit=100,
                    with_payload=True,
                    offset=offset,
                )

                to_delete = []
                for hit in results:
                    payload = hit.payload or {}
                    created_at_str = payload.get("created_at")

                    if created_at_str:
                        try:
                            # Parse ISO string
                            created_at = datetime.fromisoformat(created_at_str)
                            if created_at < cutoff_date:
                                to_delete.append(hit.id)
                        except Exception as parse_error:
                            logger.warning(
                                f"Bad date format on memory {hit.id}: {created_at_str}"
                            )
                    else:
                        # Un-timestamped episodic memory defaults to stale
                        to_delete.append(hit.id)

                if to_delete:
                    self.client.delete(
                        collection_name=collection_name, points_selector=to_delete
                    )
                    removed_count += len(to_delete)
                    logger.debug(f"Deleted {len(to_delete)} stale episodic memories.")

                if offset is None:
                    break

        except Exception as e:
            logger.error(f"Error during memory cleanup: {e}")

        return removed_count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cleaner = MemoryCleaner(days_threshold=7)
    removed = cleaner.cleanup_episodic_memory()
    print(f"Memory Cleanup Complete: Pruned {removed} stale episodic memories.")
