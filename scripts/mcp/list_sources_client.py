import asyncio
import sys
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


async def main():
    try:
        async with sse_client("http://127.0.0.1:8000/sse") as transport:
            async with ClientSession(transport[0], transport[1]) as session:
                await session.initialize()
                # list_library_sources does not take arguments
                result = await session.call_tool("list_library_sources", {})
                print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
