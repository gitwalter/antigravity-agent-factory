from pathlib import Path


def diagnose():
    print("=== Diagnosing Knowledge Files ===")
    knowledge_root = Path(".agent/knowledge")
    print(f"Knowledge Root Absolute: {knowledge_root.absolute()}")
    print(f"Exists: {knowledge_root.exists()}")
    files = list(knowledge_root.glob("*.json"))
    print(f"Found {len(files)} JSON files via glob *.json")
    if len(files) > 0:
        print(f"First 5: {[f.name for f in files[:5]]}")
    else:
        # List dir manually
        try:
            print(f"Dir listing: {[x.name for x in knowledge_root.iterdir()]}")
        except Exception as e:
            print(f"Error listing dir: {e}")

    print("\n=== Diagnosing Skill Directories ===")
    skills_root = Path(".agent/skills")
    print(f"Skills Root Absolute: {skills_root.absolute()}")
    print(f"Exists: {skills_root.exists()}")
    non_kebab = []
    for d in skills_root.iterdir():
        if d.is_dir():
            if d.name != d.name.lower() or "_" in d.name or " " in d.name:
                non_kebab.append(d.name)

    print(f"Non-kebab directories ({len(non_kebab)}): {non_kebab}")

    print("\n=== Diagnosing Templates ===")
    templates_root = Path(".agent/templates")
    print(f"Templates Root Absolute: {templates_root.absolute()}")
    from jinja2 import Environment

    env = Environment()

    for f in templates_root.rglob("*.j2"):
        try:
            env.parse(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Syntax Error in {f.relative_to(templates_root)}: {e}")


if __name__ == "__main__":
    diagnose()
