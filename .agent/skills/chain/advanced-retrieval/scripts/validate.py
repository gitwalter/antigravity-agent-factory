import os


def validate_references(skill_path):
    refs_path = os.path.join(skill_path, "references")
    if not os.path.exists(refs_path):
        return False, "No references directory found"

    files = [f for f in os.listdir(refs_path) if f.endswith(".json")]
    if not files:
        return False, "No JSON knowledge files found in references"

    return True, f"Found {len(files)} reference files"


if __name__ == "__main__":
    # Validate self
    import sys

    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    success, msg = validate_references(skill_root)
    print(f"Validation Status: {'PASS' if success else 'FAIL'} - {msg}")
    sys.exit(0 if success else 1)
