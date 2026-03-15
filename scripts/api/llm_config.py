"""
LLM Configuration for Antigravity IDX.
Uses aisuite for provider abstraction and LangChain for traced chains.
"""

import os
import json
import logging
import aisuite as ai
from langchain_google_genai import ChatGoogleGenerativeAI


def get_gemini_api_key() -> str:
    """Get Gemini API key from environment."""
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    return key


def get_aisuite_client() -> ai.Client:
    """Get an aisuite client configured for Gemini."""
    return ai.Client()


def log_thought(
    name: str, run_type: str, status: str, error: str = None, latency_ms: int = None
):
    """Log a thought to the local thoughts.log for the IDX sidebar fallback."""
    try:
        from workflow_service import PROJECT_ROOT

        log_path = PROJECT_ROOT / "thoughts.log"

        entry = {
            "type": "trace",
            "id": f"thought_{os.urandom(4).hex()}",
            "name": name,
            "run_type": run_type,
            "status": status,
            "error": error,
            "latency_ms": latency_ms,
        }

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logging.error(f"Failed to log thought: {e}")


def get_langchain_llm(
    model: str = "gemini-2.5-flash-lite",
    temperature: float = 0,
) -> ChatGoogleGenerativeAI:
    """Get a LangChain-compatible LLM with LangSmith tracing enabled."""
    # Enable LangSmith tracing
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", "antigravity-idx")

    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=get_gemini_api_key(),
        temperature=temperature,
        convert_system_message_to_human=True,
    )


def chat_with_aisuite(
    messages: list[dict],
    model: str = "google:gemini-2.5-flash-lite",
    tools: list | None = None,
    max_turns: int = 5,
) -> dict:
    """Send a chat completion via aisuite (provider-abstracted)."""
    client = get_aisuite_client()
    kwargs = {
        "model": model,
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["max_turns"] = max_turns

    # Register the start of the thought
    log_thought(messages[-1]["content"][:30], "chat", "running")

    try:
        import time

        start_time = time.time()
        response = client.chat.completions.create(**kwargs)
        latency = int((time.time() - start_time) * 1000)

        content = response.choices[0].message.content
        log_thought(messages[-1]["content"][:30], "chat", "success", latency_ms=latency)

        return {
            "content": content,
            "model": model,
        }
    except Exception as e:
        log_thought(messages[-1]["content"][:30], "chat", "error", error=str(e))
        raise e
