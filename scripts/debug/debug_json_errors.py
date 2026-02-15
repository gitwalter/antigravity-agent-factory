import json
import os
from pathlib import Path

def debug_json(f_path):
    print(f"Checking {f_path}...")
    try:
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  Length: {len(content)}")
            data = json.loads(content)
            print("  JSON is valid")
    except json.JSONDecodeError as e:
        print(f"  JSON Error at {e.pos} (line {e.lineno}, col {e.colno}): {e.msg}")
        start = max(0, e.pos - 50)
        end = min(len(content), e.pos + 50)
        context = content[start:end]
        print(f"  Context: {repr(context)}")
        # Highlight the exact position
        relative_pos = e.pos - start
        print(" " * (relative_pos + 11) + "^")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    knowledge_dir = Path(".agent/knowledge")
    for f in knowledge_dir.glob("*.json"):
        debug_json(f)
