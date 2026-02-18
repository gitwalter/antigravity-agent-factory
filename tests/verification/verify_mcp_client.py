import asyncio
import os
# Make sure we can find the mcp package if it's in the environment
# Assuming mcp is installed in the conda env we rely on

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run():
    # Set up server parameters
    # Point to the RAG MCP server script
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    script_path = os.path.join(
        project_root, "scripts/mcp/servers/rag/rag_mcp_server.py"
    )

    # Use the same python/conda environment
    # We use 'python' directly if we are running INSIDE the conda env,
    # or 'conda run' if outside.
    # Since run_command uses 'conda run', we can try invoking python directly assuming
    # we point to the right executable, OR just use the command string logic.

    # Let's try to use the absolute path to the python executable in the conda env if possible,
    # or just 'python' if we trust the environment.
    # Given the user rules: D:\Anaconda\envs\cursor-factory
    python_exe = r"D:\Anaconda\envs\cursor-factory\python.exe"

    print(f"Connecting to MCP Server at: {script_path} using {python_exe}")

    server_params = StdioServerParameters(
        command=python_exe,
        args=[script_path],
        env=os.environ.copy(),  # Inherit env vars including PYTHONPATH if any
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("Initializing...")
                await session.initialize()

                print("Listing tools...")
                tools = await session.list_tools()
                tool_names = [t.name for t in tools.tools]
                print(f"Tools found: {tool_names}")

                if "search_library" not in tool_names:
                    print("ERROR: search_library tool not found!")
                    return

                print("Calling search_library('agent concepts')...")
                # This is the moment of truth - will it crash?
                result = await session.call_tool(
                    "search_library", arguments={"query": "agent concepts"}
                )

                print("Result received!")
                if result.content and len(result.content) > 0:
                    print(f"Preview: {result.content[0].text[:500]}...")
                else:
                    print(f"Result empty or unexpected format: {result}")

    except Exception as e:
        print(f"\nCRASH/ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run())
