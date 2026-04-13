"""
Session Start Hook
Invoked by the Gemini IDE extension at `sessionStart`.
Reads the context JSON from STDIN, retrieves relevant memory via Graph-RAG/Vector,
and returns the context payload to inject into the new session.
"""

import sys
import json
import logging
from typing import Dict, Any

from scripts.memory.memory_integration import MemoryIntegration

logger = logging.getLogger("memory_hook_start")
# Redirect stdout for JSON payload, keep logs to stderr
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)


def process_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    task_description = context.get("task", "")
    session_id = context.get("sessionId", "unknown_session")

    integration = MemoryIntegration()

    # We query the engine for relevant memory based on the task prompt
    # and system context.
    memory_context = integration.get_context_for_session(
        {"intent": task_description, "session_id": session_id}
    )

    # The IDE expects a JSON response.
    # Usually: { "messages": [ { "role": "system", "content": "..." } ] }
    # or just arbitrary output that the extension handles.
    # We follow standard extension hook protocol.
    return {
        "context_injections": [{"type": "memory_bubble", "content": memory_context}],
        "message": "Memory context successfully injected.",
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
        # MUST print JSON to STDOUT
        print(json.dumps(response))
    except Exception as e:
        logger.error(f"Hook processing failed: {e}")
        print(json.dumps({"error": str(e)}))
