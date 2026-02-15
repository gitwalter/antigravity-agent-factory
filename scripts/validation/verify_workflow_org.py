import json
import os
from pathlib import Path

def verify_implementation():
    root = Path(r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory")
    
    # Files to check
    files_to_verify = [
        root / ".agentrules",
        root / ".agent" / "workflows" / "organization" / "blueprint_organization_paths.md",
        root / ".agent" / "config" / "dependency_structure.json"
    ]
    
    print("--- Verifying File Existence ---")
    all_exist = True
    for f in files_to_verify:
        if f.exists():
            print(f"OK: {f.relative_to(root)}")
        else:
            print(f"MISSING: {f.relative_to(root)}")
            all_exist = False
            
    if not all_exist:
        return

    print("\n--- Verifying .agentrules Content ---")
    with open(root / ".agentrules", "r", encoding="utf-8") as f:
        content = f.read()
        if "### Workflow-Centric Organization (REQUIRED)" in content:
            print("OK: Workflow principles found in .agentrules")
        else:
            print("FAIL: Workflow principles NOT found in .agentrules")
            
    print("\n--- Verifying JSON Structure ---")
    try:
        with open(root / ".agent" / "config" / "dependency_structure.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if "orchestration_styles" in data and "Workflow" in data["dependency_map"]["tier_hierarchy"]:
                print("OK: dependency_structure.json has orchestration_styles and updated tier_hierarchy")
            else:
                print("FAIL: dependency_structure.json is missing required methodology keys")
    except Exception as e:
        print(f"FAIL: Error reading JSON: {e}")

if __name__ == "__main__":
    verify_implementation()
