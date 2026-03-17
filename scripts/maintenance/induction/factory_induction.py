import os
import argparse
import logging
from pathlib import Path
from drafting_engine import DraftingEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FactoryInductor:
    """
    Orchestrator for Universal Factory Induction.
    Supports induction of Skills, Agents, Workflows, and KIs.
    """

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.templates_dir = (
            self.root_dir / "scripts" / "maintenance" / "induction" / "templates"
        )
        self.engine = DraftingEngine(str(self.templates_dir))

    def induce_asset(
        self,
        type: str,
        name: str,
        category: str,
        intent: str = None,
        task_id: str = None,
    ):
        """
        Main induction logic.
        """
        logger.info(f"Starting induction for {type}: {name}")

        # 1. Fetch context (if task_id provided, here we'd call Plane API)
        context = {
            "name": name,
            "category": category,
            "description": intent if intent else f"Autonomous induction for {name}.",
            # Add placeholders for complex structure
            "skills": ["none"],
            "knowledge": ["none"],
            "tools": ["none"],
            "workflows": ["none"],
            "blueprints": ["universal"],
            "domain": "universal",
            "process": [
                {
                    "name": "Standard Initiation",
                    "steps": ["Define mission", "Execute steps"],
                }
            ],
            "axiom_alignment": {},
            "patterns": {},
            "related_skills": ["none"],
            "related_knowledge": ["none"],
        }

        # 2. Draft content
        content = self.engine.draft_asset(type, context)

        # 3. Create structure
        asset_path = self.get_asset_path(type, name, category)
        asset_path.parent.mkdir(parents=True, exist_ok=True)

        # Specific handling for Skill bundles (Level 3)
        if type == "skill":
            asset_path.mkdir(parents=True, exist_ok=True)
            for sub in ["scripts", "references", "assets"]:
                (asset_path / sub).mkdir(exist_ok=True)
            target_file = asset_path / "SKILL.md"
        else:
            target_file = (
                asset_path if type != "knowledge" else asset_path.with_suffix(".json")
            )
            target_file.parent.mkdir(parents=True, exist_ok=True)

        # 4. Write content
        target_file.write_text(content, encoding="utf-8")
        logger.info(f"Successfully induced {type} at {target_file}")

    def get_asset_path(self, type: str, name: str, category: str) -> Path:
        """
        Resolve correct factory path for the asset type.
        """
        base = self.root_dir / ".agent"
        if type == "skill":
            return base / "skills" / category / name
        elif type == "agent":
            return base / "agents" / category / f"{name}.md"
        elif type == "workflow":
            return base / "workflows" / f"{name}.md"
        elif type == "knowledge":
            return base / "knowledge" / f"{name}.json"
        else:
            raise ValueError(f"Unknown asset type: {type}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Universal Factory Induction Orchestrator"
    )
    parser.add_argument(
        "--type", required=True, choices=["skill", "agent", "workflow", "knowledge"]
    )
    parser.add_argument("--name", required=True)
    parser.add_argument("--category", default="parallel")
    parser.add_argument("--intent", help="Natural language intent for the asset")
    parser.add_argument("--task-id", help="Plane Task ID for requirements induction")

    args = parser.parse_args()

    # Resolve project root relative to script position
    project_root = Path(__file__).resolve().parent.parent.parent.parent

    inductor = FactoryInductor(str(project_root))
    inductor.induce_asset(
        args.type, args.name, args.category, args.intent, args.task_id
    )
