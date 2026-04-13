"""
Experience Collector
Phase 2 of the Automated Cognitive Memory System.
Reads unstructured JSONL log artifacts, routes exact-match data into the SQLite DB,
and invokes LLM distillation to extract cognitive summaries for the Vector DB.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from scripts.memory.memory_database import MemoryDatabase
from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_SUMMARY

logger = logging.getLogger(__name__)


class ExperienceCollector:
    def __init__(self, logs_dir: str = "logs/memory"):
        self.logs_dir = Path(logs_dir)
        self.sql_db = MemoryDatabase()
        self.vector_store = get_memory_store()

    def process_uncollected_logs(self) -> int:
        """
        Scan the logs directory for raw JSONL files, process them,
        and move them to an 'archived' directory to ensure we don't double-process.
        """
        if not self.logs_dir.exists():
            logger.warning(f"Log directory {self.logs_dir} not found.")
            return 0

        archive_dir = self.logs_dir / "archived"
        archive_dir.mkdir(exist_ok=True)

        parsed_count = 0
        for log_file in self.logs_dir.glob("*.jsonl"):
            # Process entire log
            self._process_file(log_file)

            # Archive
            try:
                log_file.rename(archive_dir / log_file.name)
                parsed_count += 1
            except Exception as e:
                logger.error(f"Failed to archive {log_file.name}: {e}")

        return parsed_count

    def _process_file(self, log_file: Path):
        """Parse individual log file and route data to the dual-storage tier."""
        session_id = log_file.stem.replace("episodic_", "")

        observations = []

        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry_type = entry.get("type")
                    data = entry.get("data", {})

                    if entry_type == "observation":
                        # We route this to chat history or tool logs depending on the hook's structure.
                        # Assuming the `data` holds our content
                        obs_type = data.get("type", "unknown")
                        content = data.get("content", "")

                        if obs_type == "tool_execution":
                            # Store in exact-match tool DB
                            self.sql_db.insert_tool_log(
                                thread_id=session_id,
                                tool_name=data.get("tool_name", "unknown"),
                                input_args=data.get("args", {}),
                                output_result=content,
                                status=data.get("status", "success"),
                            )
                        else:
                            # Store in exact-match chat DB
                            self.sql_db.insert_chat_message(
                                thread_id=session_id,
                                role=data.get("role", "system"),
                                content=content,
                            )

                        observations.append(content)

                except json.JSONDecodeError:
                    continue

        # Once the file is processed, if there are significant observations,
        # distill them into a single cognitive summary vector.
        if observations:
            self._distill_and_store_summary(session_id, observations)

    def _distill_and_store_summary(self, session_id: str, observations: List[str]):
        """
        Combine raw observations into a summarized episodic concept.
        (Mocks an LLM call for now, preparing the structural routing).
        """
        combined_text = "\n".join(observations)

        # TODO: Implement True LLM Summarization Pipeline (Prompt + Chain)
        # For Phase 2, we simulate the distillation:
        distilled_summary = f"[Session {session_id} Summary]: The agent engaged in problem solving and recorded {len(observations)} key events/statements."

        metadata = {
            "session_id": session_id,
            "distilled": True,
            "raw_observation_count": len(observations),
        }

        # Store in Semantic Tier
        self.vector_store.add_memory(
            content=distilled_summary, metadata=metadata, memory_type=COLLECTION_SUMMARY
        )
        logger.info(
            f"Distilled summary stored for session {session_id} in {COLLECTION_SUMMARY}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    collector = ExperienceCollector()
    count = collector.process_uncollected_logs()
    print(f"Experience Collection Complete: {count} uncollected logs processed.")
