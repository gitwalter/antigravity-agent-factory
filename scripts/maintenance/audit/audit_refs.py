import os

SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)


def audit_references():
    empty_refs = []
    total_skills = 0

    for root, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            total_skills += 1
            refs_path = os.path.join(root, "references")
            if not os.path.exists(refs_path):
                empty_refs.append(root)
            else:
                ref_files = [
                    f
                    for f in os.listdir(refs_path)
                    if f != "metadata.json" and not f.startswith(".")
                ]
                if not ref_files:
                    empty_refs.append(root)

    print(f"Total Skills: {total_skills}")
    print(f"Skills with empty references: {len(empty_refs)}")
    for s in empty_refs:
        print(f"EMPTY_REF: {s.replace(SKILLS_ROOT, '')}")


if __name__ == "__main__":
    audit_references()
