import sys
import asyncio
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_URL = "http://127.0.0.1:8000/sse"


async def invoke_get_toc(document_name: str):
    try:
        # Force stdout to UTF-8 to prevent Windows cp1252 console crashes
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")

        # Connect to the background MCP server over HTTP SSE
        client = MultiServerMCPClient(
            connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
        )

        tools = await client.get_tools()
        toc_tool = next((t for t in tools if t.name == "get_ebook_toc"), None)

        if toc_tool:
            # Silence internal LangChain stdout print artifacts
            result = await toc_tool.ainvoke({"document_name": document_name})

            import json

            # Print as compliant JSON string natively back to the Antigravity agent process
            output = (
                result if isinstance(result, (dict, list)) else {"toc": str(result)}
            )
            print(json.dumps(output))

        else:
            print("Error: 'get_ebook_toc' tool not found on server.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error connecting to RAG MCP Client: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            'Usage: python get_rag_toc.py "<document_name_or_keyword>"', file=sys.stderr
        )
        sys.exit(1)

    doc_name = sys.argv[1]
    asyncio.run(invoke_get_toc(doc_name))
