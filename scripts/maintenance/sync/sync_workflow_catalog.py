import os
import json
import yaml

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKFLOWS_DIR = os.path.join(ROOT_DIR, ".agent", "workflows")
CATALOG_PATH = os.path.join(ROOT_DIR, ".agent", "knowledge", "workflow-catalog.json")


def sync_workflow_catalog():
    if not os.path.exists(CATALOG_PATH):
        print(f"ERROR: Catalog not found at {CATALOG_PATH}")
        return

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    existing_workflows = {
        w.get("id"): w for w in catalog.get("content", {}).get("workflows", [])
    }
    new_workflows = []

    for filename in os.listdir(WORKFLOWS_DIR):
        if not filename.endswith(".md"):
            continue

        workflow_id = filename.replace(".md", "")
        filepath = os.path.join(WORKFLOWS_DIR, filename)

        description = "No description provided"
        sdlc_phase = "Uncategorized"

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---"):
            try:
                end_idx = content.find("---", 3)
                if end_idx != -1:
                    fm_text = content[3:end_idx]
                    fm = yaml.safe_load(fm_text) or {}
                    description = fm.get("description", description)
                    sdlc_phase = fm.get("sdlc_phase", sdlc_phase)
            except Exception as e:
                print(f"Error parsing YAML in {filename}: {e}")

        # Preserve existing manual data (like 'phases' array) if it exists
        existing_entry = existing_workflows.get(workflow_id, {})

        entry = {
            "id": workflow_id,
            "name": workflow_id.replace("-", " ").title(),
            "description": str(description).strip(),
            "location": f".agent/workflows/{filename}",
            "sdlc_phase": str(sdlc_phase).strip(),
        }

        if "phases" in existing_entry:
            entry["phases"] = existing_entry["phases"]

        new_workflows.append(entry)

    new_workflows.sort(key=lambda x: x["id"])

    if "content" not in catalog:
        catalog["content"] = {}
    catalog["content"]["workflows"] = new_workflows

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"Workflow catalog synchronized: {len(new_workflows)} workflows registered.")


if __name__ == "__main__":
    sync_workflow_catalog()
