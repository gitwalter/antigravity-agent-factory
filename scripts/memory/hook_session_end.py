"""
Session End Hook
Invoked by the Gemini IDE extension at `sessionEnd`.
Reads the context JSON from STDIN, tracking the final session state, chat history,
and tool usage into the Immutable Episodic Log for later cognitive distillation.
"""

import sys
import json
import logging
from typing import Dict, Any

from scripts.memory.episodic_logger import get_episodic_logger

logger = logging.getLogger("memory_hook_end")
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)


def process_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    session_id = context.get("sessionId", "unknown_session")
    history = context.get("history", [])

    # We log the history to the episodic logger
    # The Experience Collector will index this asynchronously to avoid blocking the IDE
    episodic_log = get_episodic_logger()

    # We create a single observation for the session dump
    episodic_log.log_observation(
        {
            "type": "session_dump",
            "content": "Automated IDE session history export",
            "session_id": session_id,
            "history_length": len(history),
            "history": history,
        }
    )

    return {
        "message": f"Successfully committed {len(history)} events to episodic log for {session_id}."
    }


if __name__ == "__main__":
    try:
        raw_input = sys.stdin.read()
        context = json.loads(raw_input) if raw_input.strip() else {}
    except Exception as e:
        logger.error(f"Failed to parse stdin context: {e}")
        context = {}

    try:
        response = process_hook(context)
        print(json.dumps(response))
    except Exception as e:
        logger.error(f"Hook processing failed: {e}")
        print(json.dumps({"error": str(e)}))
