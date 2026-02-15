import json
from pathlib import Path


def fix_knowledge():
    root = Path(".agent/knowledge")
    if not root.exists():
        print(f"Knowledge root {root} does not exist!")
        return

    print(f"Fixing knowledge files in {root}...\n")

    fixed_count = 0

    for knowledge_file in root.glob("*.json"):
        try:
            content = knowledge_file.read_text(encoding="utf-8")
            if not content.strip():
                print(f"[EMPTY] {knowledge_file.name}: File is empty")
                # Initialize with minimal structure
                data = {}
            else:
                data = json.loads(content)
        except json.JSONDecodeError:
            print(f"[INVALID JSON] {knowledge_file.name}")
            data = {}

        modified = False
        file_id = knowledge_file.stem

        # Fix required fields
        if "id" not in data or data["id"] != file_id:
            data["id"] = file_id
            modified = True

        if "name" not in data:
            data["name"] = file_id.replace("-", " ").title()
            modified = True

        if "version" not in data:
            data["version"] = "1.0.0"
            modified = True

        if "category" not in data:
            data["category"] = "patterns"  # Default category
            modified = True

        if "description" not in data:
            data["description"] = f"Knowledge patterns for {file_id.replace('-', ' ')}."
            modified = True

        # Fix structures
        if "patterns" not in data:
            data["patterns"] = {}
            modified = True

        # Fix best_practices type
        if "best_practices" not in data:
            data["best_practices"] = []
            modified = True
        elif isinstance(data["best_practices"], dict):
            print(f"  Converting best_practices dict to list in {knowledge_file.name}")
            new_bp = []
            for k, v in data["best_practices"].items():
                if isinstance(v, dict):
                    item = {"name": k}
                    item.update(v)
                    new_bp.append(item)
                elif isinstance(v, list):
                    # Handle case where dict values are lists (e.g. categorized best practices)
                    for item in v:
                        if isinstance(item, str):
                            new_bp.append(item)
                        else:
                            new_bp.append({"category": k, "content": str(item)})
                else:
                    new_bp.append({"name": k, "description": str(v)})
            data["best_practices"] = new_bp
            modified = True

        # Fix anti_patterns type
        if "anti_patterns" not in data:
            data["anti_patterns"] = []
            modified = True
        elif isinstance(data["anti_patterns"], dict):
            print(f"  Converting anti_patterns dict to list in {knowledge_file.name}")
            new_ap = []
            for k, v in data["anti_patterns"].items():
                if isinstance(v, dict):
                    item = {"name": k}
                    item.update(v)
                    new_ap.append(item)
                else:
                    new_ap.append({"name": k, "description": str(v)})
            data["anti_patterns"] = new_ap
            modified = True

        if modified:
            knowledge_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"[FIXED] {knowledge_file.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} knowledge files.")


if __name__ == "__main__":
    fix_knowledge()
