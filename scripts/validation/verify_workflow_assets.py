import os
import yaml
import re
from pathlib import Path
from typing import List, Dict, Set

# --- Configuration ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if not (ROOT_DIR / ".agentrules").exists():
    ROOT_DIR = Path.cwd()
WORKFLOWS_DIR = ROOT_DIR / ".agent" / "workflows"
AGENTS_DIR = ROOT_DIR / ".agent" / "agents"
SKILLS_DIR = ROOT_DIR / ".agent" / "skills"
SCRIPTS_DIR = ROOT_DIR / "scripts"

# Specialist Codes from AGENTS.md
SPECIALIST_CODES = {
    "SYARCH",
    "WQSS",
    "KNOPS",
    "PROPS",
    "MOBEX",
    "DATAARC",
    "W3GURU",
    "GURU",
    "SYSOPS",
    "PROJEX",
    "CODEWIZ",
    "QABOT",
}


class AssetValidator:
    def __init__(self):
        self.valid_agents = self._scan_agents()
        self.valid_skills = self._scan_skills()
        self.valid_scripts = self._scan_scripts()
        self.errors = []

    def _scan_agents(self) -> Set[str]:
        """Scan .agent/agents/ and subdirs for agent names and codes."""
        agents = set(SPECIALIST_CODES)
        if not AGENTS_DIR.exists():
            return agents
        for p in AGENTS_DIR.rglob("*.md"):
            agents.add(p.stem)  # system-architecture-specialist
            # Also try to load the 'name' from frontmatter if possible
            try:
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.startswith("---"):
                        fm = yaml.safe_load(content.split("---")[1])
                        if fm and "name" in fm:
                            agents.add(fm["name"])
            except Exception:
                pass
        return agents

    def _scan_skills(self) -> Set[str]:
        """Scan .agent/skills/ for skill names (directory or .md)."""
        skills = set()
        if not SKILLS_DIR.exists():
            return skills
        # Common skill patterns
        for p in SKILLS_DIR.rglob("SKILL.md"):
            skills.add(p.parent.name)
        for p in SKILLS_DIR.rglob("*.md"):
            if p.name != "SKILL.md":
                skills.add(p.stem)
        return skills

    def _scan_scripts(self) -> Set[str]:
        """Scan scripts/ for valid python/bash files."""
        scripts = set()
        if not SCRIPTS_DIR.exists():
            return scripts
        for p in SCRIPTS_DIR.rglob("*.*"):
            if p.suffix in [".py", ".sh", ".bat", ".ps1"]:
                # Store relative to ROOT_DIR or just the path format in workflows
                rel_path = p.relative_to(ROOT_DIR).as_posix()
                scripts.add(rel_path)
                scripts.add(p.name)  # Also check by name
        return scripts

    def verify_workflow(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for Agent references (Strict: word boundaries, no lower case words like 'I')
        agent_matches = re.findall(
            r"\b(?:Agent|agent|@persona):\s*[`]?([A-Z][A-Z0-9_\-]+)\b", content
        )
        for agent in agent_matches:
            if agent not in self.valid_agents:
                self.errors.append(
                    f"{file_path.name}: Invalid Agent reference '{agent}'"
                )

        # 2. Check for Skill references (Require explicit 'Skill:' or '[[]]')
        skill_matches = re.findall(
            r"(?:Skill|skill|uses):\s*[`]?([a-z0-9_\-]+)[`]?", content
        )
        skill_matches += re.findall(r"\[\[([a-z0-9_\-]+)\]\]", content)

        for skill in set(skill_matches):
            if skill not in self.valid_skills:
                if skill not in ["name", "skill", "none", "patterns"]:
                    self.errors.append(
                        f"{file_path.name}: Invalid Skill reference '{skill}'"
                    )

        # 3. Check for Script references (Look for path strings and legacy redirects)
        script_matches = re.findall(r"[`](scripts/[^`]+)[`]", content)
        for script in script_matches:
            # Clean possible line numbers or args
            clean_script = script.split(":")[0].split(" ")[0].strip()
            if clean_script not in self.valid_scripts:
                # Try legacy redirect
                legacy_script = clean_script.replace("scripts/", "scripts/legacy/")
                if legacy_script in self.valid_scripts:
                    # Optional: flag as legacy but valid
                    # print(f"[INFO] {file_path.name}: Using legacy script {legacy_script}")
                    pass
                else:
                    self.errors.append(
                        f"{file_path.name}: Invalid Script reference '{clean_script}' (Legacy path also not found)"
                    )

    def run(self):
        print(
            f"--- Asset Verification (Agents: {len(self.valid_agents)}, Skills: {len(self.valid_skills)}, Scripts: {len(self.valid_scripts)}) ---"
        )

        workflows = list(WORKFLOWS_DIR.glob("*.md"))
        for wf_path in workflows:
            self.verify_workflow(wf_path)

        if not self.errors:
            print(f"All {len(workflows)} workflows have valid asset references!")
        else:
            print(
                f"Found {len(self.errors)} reference errors in {len(workflows)} workflows:"
            )
            for err in self.errors:
                print(f"  [!] {err}")


if __name__ == "__main__":
    validator = AssetValidator()
    validator.run()
