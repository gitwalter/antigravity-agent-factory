import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from scripts.core.template_engine import create_engine


def verify_skill():
    # Detect factory root
    factory_root = Path(__file__).parent.parent.parent
    print(f"Factory root: {factory_root}")

    try:
        engine = create_engine(factory_root)

        # Simulating context that generate_project.py would provide
        skill_id = "developing-ai-agents"
        skill_name = "developing-ai-agents"
        skill_description = "AI Agent Development with LangChain and LangGraph"
        skill_title = "AI Agent Development Skill"
        skill_summary = "This skill provides expertise in building AI agents using modern frameworks like LangChain, LangGraph, CrewAI, and AutoGen."

        project_name = "Test Project"

        context = {
            "skill_name": skill_name,
            "skill_description": skill_description,
            "skill_title": skill_title,
            "skill_summary": skill_summary,
            "project_name": project_name,
            "frameworks": ["langchain", "langgraph"],
        }

        # Template path relative to templates dir
        template_path = f"skills/{skill_id}/SKILL.md.j2"

        print(f"Rendering {template_path}...")
        output = engine.render(template_path, context)

        print("\n--- RENDERED OUTPUT START ---\n")
        print(output)
        print("\n--- RENDERED OUTPUT END ---\n")

        # Basic validation
        assert "AI Agent Development with LangChain and LangGraph" in output
        assert "# AI Agent Development Skill" in output
        assert "## Core Capabilities" in output
        assert "## Usage in Test Project" in output
        assert "## Troubleshooting" in output

        print("\nVERIFICATION SUCCESSFUL")

    except Exception as e:
        print(f"FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    verify_skill()
