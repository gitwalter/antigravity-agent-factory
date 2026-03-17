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

    try:
        import time

        start_time = time.time()
        response = client.chat.completions.create(**kwargs)
        latency = int((time.time() - start_time) * 1000)

        content = response.choices[0].message.content

        return {
            "content": content,
            "model": model,
        }
    except Exception as e:
        raise e
