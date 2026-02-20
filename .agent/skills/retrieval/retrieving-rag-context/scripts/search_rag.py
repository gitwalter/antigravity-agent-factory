import asyncio
import argparse
import sys
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_URL = "http://127.0.0.1:8000/sse"


async def invoke_search(query: str):
    try:
        # Force stdout to UTF-8 to prevent Windows cp1252 console crashes
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")

        # Connect to the background MCP server over HTTP SSE
        client = MultiServerMCPClient(
            connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
        )

        tools = await client.get_tools()
        search_tool = next((t for t in tools if t.name == "search_library"), None)

        if search_tool:
            result = await search_tool.ainvoke({"query": query})

            import json

            # Print as compliant JSON string natively back to the Antigravity agent process
            output = (
                result if isinstance(result, (dict, list)) else {"text": str(result)}
            )
            print(json.dumps(output))
        else:
            print("Error: 'search_library' tool not found on server.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error connecting to RAG MCP Client: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the Antigravity RAG MCP Server")
    parser.add_argument("query", type=str, help="Search query for the RAG library")

    args = parser.parse_args()
    asyncio.run(invoke_search(args.query))
