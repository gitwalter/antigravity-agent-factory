import os
import json
import logging
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DraftingEngine:
    """
    Intelligence Layer for Universal Factory Induction.
    Transforms raw intent/Plane data into high-fidelity asset data.
    """

    def __init__(self, templates_dir: str):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.templates_dir = templates_dir

    def draft_asset(self, asset_type: str, context: Dict[str, Any]) -> str:
        """
        Draft high-fidelity content for a specific asset type.
        In a real scenario, this would involve an LLM call.
        For now, we use a robust templating approach with placeholders if LLM is unavailable.
        """
        template_name = f"{asset_type}_template"
        extension = ".json.j2" if asset_type == "knowledge" else ".md.j2"

        try:
            template = self.env.get_template(template_name + extension)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            raise

    def enrich_from_plane(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich asset data using Plane task context.
        Maps Plane fields (name, description, etc.) to induction fields.
        """
        # Implementation of LLM-based enrichment would go here.
        # For this version, we perform structural mapping.
        enriched = {
            "name": task_data.get("name", "untitled-asset").lower().replace(" ", "-"),
            "description": task_data.get(
                "description_html", "No description provided."
            ),  # Strip HTML in production version
            "mission": task_data.get("name", "New Factory Asset"),
            "version": "1.0.0",
        }

        # Add default stubs for complex fields to guide the user/agent
        if "process" not in enriched:
            enriched["process"] = [
                {
                    "name": "Initialization",
                    "steps": ["Define requirements", "Bootstrap asset"],
                }
            ]

        return enriched


if __name__ == "__main__":
    # Internal test
    engine = DraftingEngine(os.path.join(os.path.dirname(__file__), "templates"))
    sample_context = {
        "name": "test-skill",
        "description": "A test skill for factory induction.",
        "category": "parallel",
        "mission": "To verify the drafting engine.",
        "when_to_use": ["During testing", "When validating templates"],
        "prerequisites": ["None"],
        "process": [{"name": "Step 1", "steps": ["First action"]}],
        "best_practices": ["Keep it simple"],
    }
    print(engine.draft_asset("skill", sample_context))
