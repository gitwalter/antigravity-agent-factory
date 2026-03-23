"""
Immutable Episodic Logger for Antigravity Agent Factory
Ensures every agent observation and state is recorded in an append-only
local log (Git-excluded) for reconstruction and transparency.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class EpisodicLogger:
    """
    Manages the Immutable Episodic Log (local-only).

    Attributes:
        log_dir: Directory where logs are stored.
        current_log_file: Path to the current session's log file.
    """

    def __init__(self, log_dir: str = "logs/memory"):
        self.log_dir = Path(log_dir)
        self._ensure_log_dir()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = self.log_dir / f"episodic_{self.session_id}.jsonl"

    def _ensure_log_dir(self):
        """Ensure the log directory exists."""
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_observation(self, observation: Dict[str, Any]):
        """
        Record a raw observation to the immutable log.

        Args:
            observation: Dictionary containing the observation data.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "observation",
            "data": observation,
        }
        self._append_to_log(entry)

    def log_agent_state(self, state: Dict[str, Any]):
        """
        Record the agent's internal state for later reconstruction.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_state",
            "data": state,
        }
        self._append_to_log(entry)

    def _append_to_log(self, entry: Dict[str, Any]):
        """Append a JSON entry to the current log file."""
        try:
            with open(self.current_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write to episodic log: {e}")


# Singleton instance
_instance = None


def get_episodic_logger(log_dir: str = "logs/memory") -> EpisodicLogger:
    global _instance
    if _instance is None or Path(_instance.log_dir) != Path(log_dir):
        _instance = EpisodicLogger(log_dir)
    return _instance
