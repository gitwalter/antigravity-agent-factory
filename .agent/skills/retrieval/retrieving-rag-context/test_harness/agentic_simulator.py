import os
import sys
import json
import subprocess
import time


def simulate_agentic_rag():
    print("ANTIGRAVITY AGENT SIMULATOR: Starting Agentic RAG Skill...")

    # [Step 0] Initialize State Buffer as per SKILL.md
    rag_search_state = []

    # Define iterative queries the agent might formulate to answer "What is the LAMA planner?"
    search_queries = ["LAMA planner details", "Richter Westphal optimal planning"]

    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../scripts/search_rag.py")
    )

    for i, query in enumerate(search_queries, 1):
        print(f"\n[Step 1] Retrieving -> Executing native script for query: '{query}'")

        try:
            # The agent executes the new JSON-emitting script sub-process
            # (Note: running with utf-8 encoding as we designed)
            result = subprocess.run(
                [sys.executable, script_path, query],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.returncode != 0:
                print(f"❌ Script error: {result.stderr}")
                continue

            # Agent parses the raw JSON from stdout
            raw_json_str = result.stdout.strip()
            data = json.loads(raw_json_str)

            # The structure we designed returns a list of dictionaries if it's from LangChain Content blocks
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                retrieved_text = data[0].get("text", str(data))
            elif isinstance(data, dict):
                retrieved_text = data.get("text", str(data))
            else:
                retrieved_text = str(data)

            print(
                f"[Step 2] Grading -> Agent evaluates {len(retrieved_text)} chars of context..."
            )
            time.sleep(1)  # Simulating LLM grading latency

            # Mocking the semantic grading decision
            # Mocking the semantic grading decision
            if "Richter" in retrieved_text or "LAMA" in retrieved_text:
                print(
                    "   [APPROVE] Highly relevant chunk found! Appending to State Buffer."
                )
                rag_search_state.append(
                    f"--- Context from Query: {query} ---\n{retrieved_text[:150]}...\n"
                )
            else:
                print("   [REJECT] Chunk irrelevant. Discarding.")
                print("[Step 3] Adapting -> Adjusting query strategy...")

        except Exception as e:
            print(f"Error during agentic loop: {e}")

    print("\n[Step 4] Synthesizing -> Final Answer from accumulated State Buffer:")
    print("==================================================================")
    print("\n".join(rag_search_state))
    print("==================================================================")
    print(
        "Agent: 'Based on the retrieved context, the LAMA planner was introduced by Richter and Westphal...'"
    )


if __name__ == "__main__":
    simulate_agentic_rag()
