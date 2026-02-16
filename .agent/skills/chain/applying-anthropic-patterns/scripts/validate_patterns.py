import json
import os
import sys


def validate_skill_logic(skill_path):
    """
    Validates that the skill's logic (in SKILL.md) aligns with Anthropic standards.
    Checks for presence of Pattern identifiers in the process description.
    """
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return False, "SKILL.md missing"

    with open(skill_md, "r") as f:
        content = f.read().lower()

    patterns = ["chain", "parallel", "routing", "evaluator", "orchestrator", "worker"]
    found = [p for p in patterns if p in content]

    if not found:
        return False, "No recognized Anthropic pattern keywords found in SKILL.md"

    return True, f"Found patterns: {', '.join(found)}"


if __name__ == "__main__":
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    success, msg = validate_skill_logic(skill_root)
    print(f"Pattern Alignment: {'PASS' if success else 'FAIL'} - {msg}")
    sys.exit(0 if success else 1)
