import os
import yaml
from typing import List, Dict


class WorkflowManager:
    """Manages discovery and reading of factory workflows."""

    def __init__(self, workflows_dir: str = ".agent/workflows"):
        self.workflows_dir = workflows_dir

    def list_workflows(self) -> List[Dict]:
        """Returns a list of workflow metadata (name, description, path)."""
        workflows = []
        if not os.path.exists(self.workflows_dir):
            return []

        for filename in os.listdir(self.workflows_dir):
            if filename.endswith(".md"):
                path = os.path.join(self.workflows_dir, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if content.startswith("---"):
                            _, frontmatter, _ = content.split("---", 2)
                            data = yaml.safe_load(frontmatter)
                            workflows.append(
                                {
                                    "id": filename,
                                    "name": filename.replace(".md", "")
                                    .replace("-", " ")
                                    .title(),
                                    "description": data.get(
                                        "description", "No description available."
                                    ),
                                    "path": path,
                                }
                            )
                except Exception as e:
                    print(f"Error reading workflow {filename}: {e}")

        return sorted(workflows, key=lambda x: x["name"])

    def get_workflow_content(self, filename: str) -> str:
        """Returns the full content of a workflow file."""
        path = os.path.join(self.workflows_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
