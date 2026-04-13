import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    try:
        # Configuration for the RAG server
        server_config = {
            "rag_server": {
                "url": "http://127.0.0.1:8000/sse",
                "transport": "sse",
            }
        }

        # Initialize MultiServerMCPClient with the configuration
        client = MultiServerMCPClient(connections=server_config)

        # List tools to verify connection and find the correct tool
        tools = await client.get_tools()

        list_tool = next((t for t in tools if t.name == "list_library_sources"), None)

        if list_tool:
            # invocations in LangChain are async
            result = await list_tool.ainvoke({})
            print(result)
        else:
            print("Error: 'list_library_sources' tool not found.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
