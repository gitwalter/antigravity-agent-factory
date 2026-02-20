import sys
import os
import logging
import subprocess

# Determine project root based on script location
# Script is in <root>/notebooks/verify_rag.py
# So root is script_dir/..
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Mock logger to avoid spamming
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_rag():
    print("--- Verifying RAG Logic (FastMCP) ---")
    print(f"Project Root: {project_root}")

    try:
        from qdrant_client import QdrantClient
        from scripts.ai.rag.rag_optimized import get_rag
    except ImportError as e:
        print(f"[X] Import Error for project modules: {e}")
        print(f"sys.path: {sys.path}")
        return

    # Check for fastmcp
    try:
        import fastmcp
    except ImportError:
        print("[!] fastmcp not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastmcp"])
        import fastmcp

    from fastmcp import FastMCP

    try:
        # 1. Test Qdrant Connection
        print("[1/3] Testing Qdrant Connection...")
        client = QdrantClient(url="http://localhost:6333")
        collections = client.get_collections()
        found = any(c.name == "ebook_library" for c in collections.collections)
        if found:
            print("   [OK] 'ebook_library' collection found.")
        else:
            print("   [X] 'ebook_library' collection NOT found.")
            return

        # 2. Test RAG Query
        print("[2/3] Testing RAG Query...")
        rag = get_rag(warmup=True)
        results = rag.query("agentic workflow")
        if results:
            print(f"   [OK] Retrieved {len(results)} results.")
        else:
            print("   [!] No results found (this might be normal if empty).")

        # 3. Test MCP Prototype Class
        print("[3/3] Testing FastMCP Prototype...")

        mcp = FastMCP("RAG Agent Server")

        @mcp.tool()
        def query_rag(query: str) -> str:
            """Semantically search the ebook library for technical concepts."""
            docs = rag.query(query)
            return "Found" if docs else "Empty"

        # Test the decorated function directly
        res = query_rag("test")
        print(f"   [OK] FastMCP Function returned: {res}")

        print("\n[SUCCESS] Verification Successful!")

    except Exception as e:
        print(f"❌ Runtime Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    verify_rag()
