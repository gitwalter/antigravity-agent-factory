import os
import sys
import json
import asyncio
from typing import Any, Dict, List, Optional
from IPython.display import display, Markdown

# Ensure we can import from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage

# Local RAG Server URL from `start_rag_server.bat`
SERVER_URL = "http://127.0.0.1:8000/sse"


def _remove_additional_properties(schema: Dict[str, Any]) -> None:
    """Recursively removes 'additionalProperties' from a JSON schema to appease Gemini API."""
    if not isinstance(schema, dict):
        return
    if "additionalProperties" in schema:
        del schema["additionalProperties"]
    for key, value in list(schema.items()):
        if isinstance(value, dict):
            _remove_additional_properties(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _remove_additional_properties(item)


def patch_tool_schema(tool: BaseTool) -> BaseTool:
    """Patch a LangChain tool to remove additionalProperties from its Pydantic schema representation."""
    if hasattr(tool, "args_schema") and tool.args_schema:
        # Some Langchain tools return a raw dict for args_schema, others a Pydantic BaseModel
        if isinstance(tool.args_schema, dict):
            _remove_additional_properties(tool.args_schema)
        else:
            old_schema = tool.args_schema.schema

            def custom_schema(*args, **kwargs):
                s = old_schema(*args, **kwargs)
                _remove_additional_properties(s)
                return s

            tool.args_schema.schema = custom_schema
    return tool


async def build_rag_agent(llm=None):
    """
    Connects to the RAG MCP Server, fetches tools, patches them, and builds a standard LangChain agent.
    """
    if llm is None:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.environ.get("GEMINI_API_KEY", ""),
            temperature=0,
            convert_system_message_to_human=True,
        )

    # Note: We must hold the client open while the agent executes,
    # so we return both the executor and the async client session.
    client = MultiServerMCPClient(
        connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
    )

    # Needs to be called within an async context
    raw_tools = await client.get_tools()

    # Patch the tools to remove 'additionalProperties' to fix the Gemini warnings
    tools = [patch_tool_schema(t) for t in raw_tools]
    print(f"Retrieved {len(tools)} tools from MCP: {[t.name for t in tools]}")

    # Bind tools using langgraph's modern create_react_agent
    agent = create_react_agent(llm, tools=tools)

    return agent, client


async def run_agentic_rag(query: str):
    """
    End-to-end execution of a query using the RAG MCP Agent.
    """
    print("Initiating Agentic RAG via local MCP...")
    agent, client = await build_rag_agent()

    try:
        # We process the query using the LangGraph agent's astream
        async for chunk in agent.astream(
            {"messages": [HumanMessage(content=query)]}, stream_mode="updates"
        ):
            for node, values in chunk.items():
                for message in values.get("messages", []):
                    # 1. Print out Tool Calls dispatched by the AI
                    if hasattr(message, "tool_calls") and message.tool_calls:
                        for tool_call in message.tool_calls:
                            print(
                                f"\n⚒️ Calling tool '{tool_call['name']}' with args: {tool_call['args']}"
                            )
                            print("⏳ Waiting for response...\n")

                    # 2. Print out the tool resolution contents (the MCP server response)
                    elif message.type == "tool":
                        print(
                            f"✅ Tool '{message.name}' resolved (Content length: {len(message.content)} chars)."
                        )
                        snippet = message.content[:200] + (
                            "..." if len(message.content) > 200 else ""
                        )
                        print(f"   Preview: {snippet}\n")

                    # 3. Print out standard AI text that isn't a tool call
                    elif (
                        message.type == "ai"
                        and message.content
                        and not getattr(message, "tool_calls", None)
                    ):
                        print("\n--- Final Answer ---")
                        print(message.content)
                        print("--------------------\n")

        return True
    except Exception as e:
        print(f"Error executing agent: {e}")
    finally:
        # Important: MultiServerMCPClient contexts must eventually be closed
        # (Though current Langchain adapters don't mandate an explicit .close() yet, it's good practice)
        pass


if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        print("Please set GEMINI_API_KEY environment variable.")
    else:
        query = "List all the available documents in the library. Then, search for Stuart Russell and summarize what the book says about the Turing Test limit."
        asyncio.run(run_agentic_rag(query))
