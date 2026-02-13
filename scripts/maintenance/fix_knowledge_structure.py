
import json
import sys
from pathlib import Path

def fix_knowledge_structure(factory_root: Path):
    knowledge_dir = factory_root / ".agent" / "knowledge"
    if not knowledge_dir.exists():
        print(f"Knowledge directory not found: {knowledge_dir}")
        return

    count = 0
    print(f"Scanning knowledge files in {knowledge_dir}")
    
    for knowledge_file in knowledge_dir.glob("*.json"):
        if knowledge_file.name == "schema.json":
            continue
            
        try:
            content = knowledge_file.read_text(encoding="utf-8")
            data = json.loads(content)
            updated = False
            
            # Fix ID mismatch
            file_id = knowledge_file.stem
            if data.get("id") != file_id:
                data["id"] = file_id
                updated = True
                print(f"Fixed ID for {knowledge_file.name}")
                
            # Ensure best_practices
            if "best_practices" not in data:
                data["best_practices"] = []
                updated = True
                
            # Ensure anti_patterns
            if "anti_patterns" not in data:
                data["anti_patterns"] = []
                updated = True

            # Ensure patterns exists (test checks for it)
            if "patterns" not in data:
                 data["patterns"] = {}
                 updated = True

            if updated:
                knowledge_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                count += 1
                print(f"Updated {knowledge_file.name}")
        except Exception as e:
            print(f"Error processing {knowledge_file.name}: {e}")

    print(f"Fixed {count} knowledge files.")

if __name__ == "__main__":
    fix_knowledge_structure(Path(__file__).parent.parent.parent)
