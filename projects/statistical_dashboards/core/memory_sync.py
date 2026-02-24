import json
import os
from datetime import datetime


class MemorySyncManager:
    """Manages the preparation of dashboard project data for the Antigravity Memory MCP."""

    def __init__(self, sync_dir="projects/statistical_dashboards/data/sync"):
        self.sync_dir = sync_dir
        if not os.path.exists(self.sync_dir):
            os.makedirs(self.sync_dir)

    def prepare_sync_payload(self, project, artifact_links=None):
        """
        Creates a JSON payload for the agent to ingest via Memory MCP.
        This fulfills the synchronization hook requirement.
        """
        observations = [
            f"Description: {project.description}",
        ]

        # Add dataset summary
        if project.datasets:
            observations.append(
                f"Datasets Attached: {', '.join([d.filename for d in project.datasets])}"
            )
            observations.append(
                f"Total Combined Data Rows: {sum(d.row_count for d in project.datasets)}"
            )

        # Add links to artifacts (if any provided)
        if artifact_links:
            for link in artifact_links:
                observations.append(f"Data Artifact: {link}")

        payload = {
            "entity_name": f"Dashboard Project: {project.name}",
            "entity_type": "Data Science Project",
            "observations": observations,
            "synced_at": datetime.now().isoformat(),
            "source": "Statistical Dashboard Project Center",
            "project_id": project.id,
        }

        filename = f"sync_{project.id}.json"
        path = os.path.join(self.sync_dir, filename)
        with open(path, "w") as f:
            json.dump(payload, f, indent=4)
        return path

    def post_report_to_plane(self, project, summary_html):
        """
        Directly posts a statistical summary to the associated Plane issue.
        Uses the native manager.py for reliable injection.
        """
        manager_script = "scripts/pms/manager.py"
        conda_exec = "conda run -p D:\\Anaconda\\envs\\cursor-factory"

        # Map project to issue ID (assuming AGENT-1 for now or project metadata)
        # In a real scenario, the project object would have an external_id or similar.
        issue_id = getattr(project, "external_id", "AGENT-1")

        import subprocess

        # Prepare safe description for shell
        # On Windows, we need to wrap in double quotes and escape internal ones
        safe_description = summary_html.replace('"', '\\"')

        cmd = [
            "python",
            manager_script,
            "update",
            "--id",
            issue_id,
            "--description",
            f'"{safe_description}"',
        ]

        full_cmd = f"{conda_exec} {' '.join(cmd)}"
        try:
            result = subprocess.run(
                full_cmd, shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                return False, result.stderr or result.stdout
            return True, result.stdout
        except Exception as e:
            return False, str(e)
