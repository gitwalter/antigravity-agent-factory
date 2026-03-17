import os
import yaml
import json
import shutil
from typing import Dict, List, Any, Optional
from pathlib import Path

# Path configuration
LOCAL_WORKFLOWS_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent / ".agent" / "workflows"
)
# Global workflows are in the user's .gemini directory
GLOBAL_WORKFLOWS_DIR = Path.home() / ".gemini" / "antigravity" / "global_workflows"
STANDARD_RULE_PATH = LOCAL_WORKFLOWS_DIR.parent / "rules" / "workflow-standard.md"


class WorkflowManager:
    def __init__(self, local_dir: str, global_dir: str):
        self.local_dir = local_dir
        self.global_dir = global_dir
        self.local_workflows = {}
        self.global_workflows = {}

    def load_all(self):
        self.local_workflows = self._load_dir(self.local_dir)
        self.global_workflows = self._load_dir(self.global_dir)

    def _load_dir(self, directory: str) -> Dict[str, Dict[str, Any]]:
        workflows = {}
        if not os.path.exists(directory):
            print(f"Warning: Directory {directory} does not exist.")
            return workflows

        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                file_path = os.path.join(directory, filename)
                workflow_data = self._parse_workflow(file_path)
                workflows[filename] = workflow_data
        return workflows

    def _parse_workflow(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter = {}
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                except Exception as e:
                    print(f"Error parsing YAML in {file_path}: {e}")

        return {
            "path": file_path,
            "filename": os.path.basename(file_path),
            "frontmatter": frontmatter,
            "body": body,
            "version": frontmatter.get("version", "0.0.0"),
            "description": frontmatter.get("description", ""),
            "tags": frontmatter.get("tags", []),
            "author": frontmatter.get("author", ""),
        }

    def audit_workflow(self, workflow: Dict[str, Any]) -> List[str]:
        issues = []
        fm = workflow["frontmatter"]
        body = workflow["body"]

        # Check Frontmatter
        if not fm.get("description"):
            issues.append("Missing 'description'")
        if not fm.get("version"):
            issues.append("Missing 'version'")
        if not fm.get("tags"):
            issues.append("Missing 'tags'")

        # Check Structure
        if "## Trigger Conditions" not in body:
            issues.append("Missing '## Trigger Conditions'")
        if "## Trigger Examples" not in body:
            issues.append("Missing '## Trigger Examples'")
        if "## Phases" not in body and "## Steps" not in body:
            issues.append("Missing '## Phases' or '## Steps'")
        if "## Best Practices" not in body:
            issues.append("Missing '## Best Practices'")

        return issues

    def standardize_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically fix structural issues and add missing sections."""
        fm = workflow["frontmatter"]
        body = workflow["body"]

        # Ensure Frontmatter properties
        if not fm.get("version") or fm.get("version") == "0.0.0":
            fm["version"] = "2.0.0"

        if not fm.get("description"):
            # Try to extract from H1 or first paragraph
            fm["description"] = "Standardized factory workflow."

        if not fm.get("tags"):
            name_parts = workflow["filename"].replace(".md", "").split("-")
            fm["tags"] = name_parts + ["standardized"]

        # Ensure Sections in Body
        if "## Trigger Conditions" not in body:
            body = body.replace(
                "# ",
                "# Workflow\n\n## Trigger Conditions\n- User requests activation.\n\n# ",
                1,
            )

        if "## Trigger Examples" not in body:
            body += (
                '\n\n## Trigger Examples\n- "Execute ' + workflow["filename"] + '"\n'
            )

        if "## Best Practices" not in body:
            body += "\n\n## Best Practices\n- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.\n- **Memory First**: Check context before execution.\n- **Verifiability**: Document every step.\n"

        if "## Related" not in body:
            body += "\n\n## Related\n- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)\n"

        workflow["frontmatter"] = fm
        workflow["body"] = body
        return workflow

    def write_workflow(self, workflow: Dict[str, Any], directory: str):
        file_path = os.path.join(directory, workflow["filename"])
        fm_content = yaml.dump(workflow["frontmatter"], sort_keys=False)
        content = f"---\n{fm_content}---\n{workflow['body']}"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {file_path}")

    def run_audit(self, fix=False):
        print("\n--- Workflow Audit & Standardization ---")
        issues_found = 0
        for filename, wf in self.local_workflows.items():
            issues = self.audit_workflow(wf)
            if issues:
                issues_found += 1
                if fix:
                    print(f"[FIX] Standardizing {filename}...")
                    standardized_wf = self.standardize_workflow(wf)
                    self.write_workflow(standardized_wf, self.local_dir)
                else:
                    print(f"[ISSUE] {filename}: {', '.join(issues)}")

        print(
            f"\nAudit completed. Checked {len(self.local_workflows)}, Issues: {issues_found}, Fixed: {fix}"
        )

    def sync(self, dry_run=True):
        print(f"\n--- Synchronization Process (Dry Run: {dry_run}) ---")

        # Refresh state
        self.load_all()

        # All unique filenames
        all_filenames = set(self.local_workflows.keys()) | set(
            self.global_workflows.keys()
        )

        for filename in sorted(all_filenames):
            local_wf = self.local_workflows.get(filename)
            global_wf = self.global_workflows.get(filename)

            if local_wf and not global_wf:
                print(f"[NEW] Local -> Global: {filename}")
                if not dry_run:
                    shutil.copy2(
                        local_wf["path"], os.path.join(self.global_dir, filename)
                    )

            elif global_wf and not local_wf:
                print(f"[NEW] Global -> Local: {filename}")
                if not dry_run:
                    shutil.copy2(
                        global_wf["path"], os.path.join(self.local_dir, filename)
                    )

            elif local_wf and global_wf:
                # Version comparison logic
                v_local = local_wf["version"]
                v_global = global_wf["version"]

                if v_local > v_global:
                    print(
                        f"[UPDATE] Local -> Global: {filename} ({v_local} > {v_global})"
                    )
                    if not dry_run:
                        shutil.copy2(local_wf["path"], global_wf["path"])
                elif v_global > v_local:
                    print(
                        f"[UPDATE] Global -> Local: {filename} ({v_global} > {v_local})"
                    )
                    if not dry_run:
                        shutil.copy2(global_wf["path"], local_wf["path"])
                else:
                    # Same version, check detail (length)
                    if len(local_wf["body"]) > len(global_wf["body"]) + 50:
                        print(
                            f"[HEURISTIC] Local -> Global: {filename} (Local is more detailed)"
                        )
                        if not dry_run:
                            shutil.copy2(local_wf["path"], global_wf["path"])
                    elif len(global_wf["body"]) > len(local_wf["body"]) + 50:
                        print(
                            f"[HEURISTIC] Global -> Local: {filename} (Global is more detailed)"
                        )
                        if not dry_run:
                            shutil.copy2(global_wf["path"], local_wf["path"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sync and Standardize Workflows")
    parser.add_argument("--fix", action="store_true", help="Auto-fix structural issues")
    parser.add_argument("--sync", action="store_true", help="Run synchronization")
    parser.add_argument(
        "--commit", action="store_true", help="Actually write changes (not dry run)"
    )
    args = parser.parse_args()

    manager = WorkflowManager(LOCAL_WORKFLOWS_DIR, GLOBAL_WORKFLOWS_DIR)
    manager.load_all()

    if args.fix:
        manager.run_audit(fix=args.commit)

    if args.sync:
        manager.sync(dry_run=not args.commit)
