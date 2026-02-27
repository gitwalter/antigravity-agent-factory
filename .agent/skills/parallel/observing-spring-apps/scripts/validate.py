import os
import sys


def validate():
    skill_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Check for core components
    missing = []
    for d in ["references", "scripts", "assets"]:
        if not os.path.exists(os.path.join(skill_path, d)):
            missing.append(d)

    if "SKILL.md" not in os.listdir(skill_path):
        missing.append("SKILL.md")

    if missing:
        print(f"Validation FAILED: Missing {', '.join(missing)}")
        return False

    print("Validation PASSED: Level 1-3 structural integrity verified.")
    return True


if __name__ == "__main__":
    sys.exit(0 if validate() else 1)
