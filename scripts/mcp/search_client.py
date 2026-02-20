import asyncio
import sys
import argparse
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main(query: str):
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

        search_tool = next((t for t in tools if t.name == "search_library"), None)

        if search_tool:
            print(f"Executing search for: '{query}'...")
            # invocations in LangChain are async
            result = await search_tool.ainvoke({"query": query})
            print("\n--- Search Results ---")
            print(result)
            print("----------------------")
        else:
            print("Error: 'search_library' tool not found.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search RAG library via MCP.")
    parser.add_argument("query", help="Search query string")
    args = parser.parse_args()

    asyncio.run(main(args.query))
