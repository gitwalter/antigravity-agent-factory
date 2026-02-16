import sys


def estimate_tokens(text):
    # Simple heuristic: 1 token ~= 4 chars for English
    return len(text) // 4


if __name__ == "__main__":
    # Heuristic check for SKILL.md length
    import os

    skill_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_md = os.path.join(skill_path, "SKILL.md")

    if os.path.exists(skill_md):
        with open(skill_md, "r") as f:
            tokens = estimate_tokens(f.read())
            print(f"SKILL.md size: ~{tokens} tokens")
            if tokens > 500:
                print(
                    "WARNING: Skill exceeds optimal token target (500). Consider moving logic to scripts/."
                )
    else:
        print("SKILL.md not found.")
