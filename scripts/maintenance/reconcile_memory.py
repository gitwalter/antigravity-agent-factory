"""
Memory Reconciliation Utility (SSGM Framework)
Periodically realigns the active memory graph with the episodic log.
Performs summarization-based consolidation of raw observations.
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any
from scripts.memory.episodic_logger import get_episodic_logger
from scripts.api.llm_config import chat_with_aisuite

logger = logging.getLogger(__name__)


class MemoryReconciler:
    """
    Consolidates episodic logs into semantic patterns.
    """

    def __init__(self, log_dir: str = "logs/memory"):
        self.log_dir = Path(log_dir)

    def get_all_logs(self) -> List[Dict[str, Any]]:
        """Reads all entries from all episodic log files."""
        all_entries = []
        for log_file in self.log_dir.glob("episodic_*.jsonl"):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        all_entries.append(json.loads(line))
            except Exception as e:
                logger.error(f"Error reading log file {log_file}: {e}")
        return all_entries

    def identify_patterns(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Uses LLM to synthesize clusters of observations into semantic facts.
        """
        if not entries:
            return []

        # 1. Filter and group observations (Simple clustering by content similarity placeholder)
        observations = [e["data"] for e in entries if e.get("type") == "observation"]
        if len(observations) < 3:
            return []

        # 2. LLM Synthesis Pass
        try:
            obs_text = "\n".join(
                [f"- {o.get('content')}" for o in observations[:20]]
            )  # Limit batch size
            prompt = f"""
            You are the Antigravity Memory Reconciler.
            Below are raw episodic observations from recent agent sessions:

            {obs_text}

            Your task is to:
            1. Identify repeating patterns or overlapping "facts."
            2. Synthesize these raw traces into a single, high-fidelity semantic memory.
            3. Exclude temporary state, noise, or one-off errors.

            Output a JSON list of synthesized facts. Format:
            [ {{"content": "Definition of the fact", "category": "architecture/user/logic", "confidence": 0.0-1.0}} ]
            """

            response = chat_with_aisuite([{"role": "user", "content": prompt}])
            # Basic JSON extraction (assuming LLM returns clean JSON or Markdown block)
            content = response["content"]
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()

            synthesized = json.loads(content)
            return synthesized
        except Exception as e:
            logger.error(f"Semantic Reconciliation failed: {e}")
            return []

    def reconcile(self):
        """Perform the reconciliation loop."""
        entries = self.get_all_logs()
        patterns = self.identify_patterns(entries)

        for pattern in patterns:
            logger.info(f"Reconciliation found pattern: {pattern['summary']}")
            # In a real run, we would call InductionEngine.propose_memory() here


if __name__ == "__main__":
    reconciler = MemoryReconciler()
    reconciler.reconcile()
