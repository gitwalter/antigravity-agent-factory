#!/usr/bin/env python3
"""
Antigravity Agent Factory - Automated PRD to Code Bridge

Transforms a verified Agentic PRD (knowledge/prd.md) into structured project scaffolding and core implementation logic.
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core.generate_project import ProjectConfig, ProjectGenerator


class PRDBridge:
    """Orchestrates the transformation of PRD requirements into code."""

    def __init__(self, prd_path: str, target_dir: str):
        self.prd_path = Path(prd_path)
        self.target_dir = Path(target_dir)
        self.prd_content = ""
        self.config_data = {}

    def load_prd(self) -> bool:
        """Loads and reads the PRD file."""
        if not self.prd_path.exists():
            print(f"[ERROR] PRD not found at {self.prd_path}")
            return False

        with open(self.prd_path, "r", encoding="utf-8") as f:
            self.prd_content = f.read()
        return True

    def parse_prd(self) -> Dict[str, Any]:
        """Parses the PRD to extract structured data."""
        # Extract Project Name from H1
        project_name_match = re.search(
            r"^# PRD\s*—\s*(.+)$", self.prd_content, re.MULTILINE
        )
        if not project_name_match:
            project_name_match = re.search(
                r"^# Product Requirements Document \(PRD\):\s*(.+)$",
                self.prd_content,
                re.MULTILINE,
            )

        project_name = (
            project_name_match.group(1).strip()
            if project_name_match
            else "automated-project"
        )

        # Extract Description from Executive Summary
        description_match = re.search(
            r"## 1\. Executive Summary\n(.+?)(?=\n##)", self.prd_content, re.DOTALL
        )
        project_description = (
            description_match.group(1).strip() if description_match else ""
        )

        # Extract JSON blocks (Stories/Acceptance Criteria)
        stories = []
        json_blocks = re.findall(r"```json\n(.*?)\n```", self.prd_content, re.DOTALL)
        for block in json_blocks:
            try:
                story_data = json.loads(block)
                if "story_id" in story_data:
                    stories.append(story_data)
            except json.JSONDecodeError:
                print(f"[WARNING] Failed to parse JSON block: {block[:50]}...")

        # Extract Agents and Skills mentioned in Section 5 or Metadata
        agents = []
        skills = []

        # Look for agents in metadata section
        agents_match = re.findall(r"- agents: `(.+?)`", self.prd_content, re.IGNORECASE)
        for agent_list in agents_match:
            agents.extend([a.strip() for a in agent_list.split(",")])

        # De-duplicate
        agents = list(set(agents))

        return {
            "project_name": project_name,
            "project_description": project_description,
            "stories": stories,
            "agents": agents,
            "skills": skills,  # To be refined
        }

    def execute(self):
        """Runs the bridge execution."""
        if not self.load_prd():
            return False

        print(f"Parsing PRD: {self.prd_path}...")
        parsed_data = self.parse_prd()

        print(f"Project Name: {parsed_data['project_name']}")

        # Create ProjectConfig
        config = ProjectConfig(
            project_name=parsed_data["project_name"],
            project_description=parsed_data["project_description"],
            agents=parsed_data["agents"],
            skills=["bugfix-workflow", "tdd"],  # Default starter skills
        )

        # Initialize ProjectGenerator
        generator = ProjectGenerator(config, str(self.target_dir))

        print("Starting core structure generation...")
        result = generator.generate()

        if result["success"]:
            print("[SUCCESS] Core structure generated.")
            self._generate_implementation_logic(parsed_data["stories"])
            return True
        else:
            print(f"[ERROR] Generation failed: {result['errors']}")
            return False

    def _generate_implementation_logic(self, stories: List[Dict[str, Any]]):
        """
        Placeholder for logic that triggers builder agents to implement
        files based on extracted stories.
        In this version, we create stub files for each story.
        """
        src_dir = self.target_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)

        for story in stories:
            story_id = story.get("story_id", "unknown")
            file_name = f"{story_id.lower().replace('-', '_')}_impl.py"
            file_path = src_dir / file_name

            content = f'"""\nImplementation for Story {story_id}\n\n'
            content += "Acceptance Criteria:\n"
            for ac in story.get("acceptance", []):
                content += f'- {ac.get("expr", "N/A")}\n'
            content += '"""\n\n'
            content += "def run():\n    # TODO: Implement logic according to acceptance criteria\n    pass\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Generated implementation stub: {file_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated PRD to Code Bridge")
    parser.add_argument(
        "--prd", type=str, default="knowledge/prd.md", help="Path to the PRD file"
    )
    parser.add_argument("--out", type=str, default=".", help="Target output directory")

    args = parser.parse_args()

    bridge = PRDBridge(args.prd, args.out)
    bridge.execute()
