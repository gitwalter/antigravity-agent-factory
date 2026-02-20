import asyncio
import sys
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_URL = "http://127.0.0.1:8000/sse"


async def invoke_list_sources():
    try:
        # Force stdout to UTF-8 to prevent Windows cp1252 console crashes
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")

        # Connect to the background MCP server over HTTP SSE
        client = MultiServerMCPClient(
            connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
        )

        tools = await client.get_tools()
        list_tool = next((t for t in tools if t.name == "list_library_sources"), None)

        if list_tool:
            # Silence internal LangChain stdout print artifacts
            sources_result = await list_tool.ainvoke({})

            import json

            # Print as compliant JSON string natively back to the Antigravity agent process
            output = (
                sources_result
                if isinstance(sources_result, (dict, list))
                else {"catalog": str(sources_result)}
            )
            print(json.dumps(output))

        else:
            print(
                "Error: 'list_library_sources' tool not found on server.",
                file=sys.stderr,
            )
            sys.exit(1)

    except Exception as e:
        print(f"Error connecting to RAG MCP Client: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(invoke_list_sources())
