import os
import sys
import json

# Add project root to sys.path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../../")
)
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.ai.rag.agentic_rag import AgenticRAG


def test_retrieval(query: str):
    """Test the Agentic RAG retrieval loop."""
    print(f"Testing retrieval for: {query}")
    rag = AgenticRAG()
    result = rag.query(query)

    print("\n--- RESULTS ---")
    print(f"Status: {result.get('web_search', 'unknown')}")
    print(f"Generation snippet: {result.get('generation', '')[:500]}...")

    # Save results for inspection
    with open("retrieval_test_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("\nFull output saved to retrieval_test_output.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python test_retrieval.py "your query"')
        sys.exit(1)

    test_retrieval(sys.argv[1])
