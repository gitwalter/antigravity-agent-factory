import sys
import os
import logging

# Setup logging to stderr
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, PROJECT_ROOT)


def test_agentic_rag():
    from scripts.ai.rag.agentic_rag import AgenticRAG

    print("Initializing AgenticRAG...", file=sys.stderr)
    rag = AgenticRAG()

    print("Querying...", file=sys.stderr)
    # Use a query that should return results
    res = rag.query("agent building guide")

    gen = res.get("generation", "")
    print(f"Result Length: {len(gen)}", file=sys.stderr)
    if not gen:
        print("ERROR: No generation returned.", file=sys.stderr)
        sys.exit(1)

    print("SUCCESS: AgenticRAG worked.", file=sys.stderr)


if __name__ == "__main__":
    test_agentic_rag()
