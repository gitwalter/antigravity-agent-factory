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
        }

        payload = {
            "entity_name": f"Dashboard Project: {project.name}",
            "entity_type": "Data Science Project",
            "observations": observations,
            "synced_at": datetime.now().isoformat(),
            "source": "Statistical Dashboard Project Center",
        }

        filename = f"sync_{project.id}.json"
        path = os.path.join(self.sync_dir, filename)
        with open(path, "w") as f:
            json.dump(payload, f, indent=4)
        return path
