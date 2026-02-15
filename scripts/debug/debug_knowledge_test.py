import json
from pathlib import Path


def test_debug_knowledge():
    root = Path(__file__).parent.parent
    knowledge_dir = root / ".agent" / "knowledge"
    print(f"Knowledge Dir: {knowledge_dir.absolute()}")

    files = list(knowledge_dir.glob("*.json"))
    print(f"Found {len(files)} files")

    errors = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if "patterns" not in data:
                errors.append(f"{f.name}: Missing patterns")
            elif not isinstance(data["patterns"], dict):
                errors.append(f"{f.name}: Patterns not dict")
            elif len(data["patterns"]) == 0:
                print(f"[WARN] {f.name}: Patterns empty")
        except Exception as e:
            errors.append(f"{f.name}: {e}")

    if errors:
        print(f"ERRORS: {errors[:5]}...")
    else:
        print("No errors found (ignoring empty patterns for now)")


if __name__ == "__main__":
    test_debug_knowledge()
