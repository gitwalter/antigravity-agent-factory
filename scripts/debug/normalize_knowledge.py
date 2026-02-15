import json
import os
from pathlib import Path

def normalize_and_validate():
    knowledge_dir = Path(".agent/knowledge")
    updated = 0
    errors = 0
    
    for f_path in knowledge_dir.glob("*.json"):
        try:
            content = f_path.read_text(encoding='utf-8')
            # Normalize field name
            if '"solution":' in content:
                content = content.replace('"solution":', '"fix":')
                f_path.write_text(content, encoding='utf-8')
                updated += 1
            
            # Validate JSON
            json.loads(content)
        except json.JSONDecodeError as e:
            print(f"ERROR in {f_path} at {e.pos}: {e.msg}")
            errors += 1
        except Exception as e:
            print(f"ERROR reading {f_path}: {e}")
            errors += 1
            
    print(f"Summary: Updated {updated} files. Found {errors} JSON errors.")
    return errors == 0

if __name__ == "__main__":
    if normalize_and_validate():
        print("All JSON files are structurally sound.")
    else:
        exit(1)
