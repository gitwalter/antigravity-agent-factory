import os
import json
import sys
from pathlib import Path


def get_root():
    return Path(__file__).parent.parent.parent


def verify_phase_5():
    root = get_root()
    spec_path = root / "docs" / "architecture" / "sdlc-architecture-spec.json"

    if not spec_path.exists():
        print(f"Error: SDLC spec not found at {spec_path}")
        return False

    with open(spec_path, "r") as f:
        spec = json.load(f)

    print(f"Verifying Phase 5 (Test & Eval) for stack: {spec.get('active_stack')}")

    # Check evaluation report
    eval_path = root / "knowledge" / "eval-report.md"
    if not eval_path.exists():
        print("Error: Gate Artifact 'knowledge/eval-report.md' is missing.")
        return False

    print("Success: Phase 5 Test & Eval artifacts verified.")
    return True


if __name__ == "__main__":
    if verify_phase_5():
        sys.exit(0)
    else:
        sys.exit(1)
