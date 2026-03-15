import os
import json
import sys
from pathlib import Path


def get_root():
    return Path(__file__).parent.parent.parent


def verify_phase_4():
    root = get_root()
    spec_path = root / "docs" / "architecture" / "sdlc-architecture-spec.json"
    config_path = root / ".agent" / "config" / "stack-configurations.json"

    if not spec_path.exists():
        print(f"Error: SDLC spec not found at {spec_path}")
        return False

    with open(spec_path, "r") as f:
        spec = json.load(f)

    active_stack = spec.get("active_stack")
    print(f"Verifying Phase 4 (Build) for stack: {active_stack}")

    # Check walkthrough
    walkthrough_path = root / "knowledge" / "walkthrough.md"
    if not walkthrough_path.exists():
        print("Error: Gate Artifact 'knowledge/walkthrough.md' is missing.")
        return False

    print("Success: Phase 4 Build artifacts verified.")
    return True


if __name__ == "__main__":
    if verify_phase_4():
        sys.exit(0)
    else:
        sys.exit(1)
