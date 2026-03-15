"""
Workflow Service for Antigravity IDX.
Handles CRUD operations on .agent/workflows/*.md files
and generation/execution of LangGraph/CrewAI agent workflows.
"""

import os
import re
import yaml
import json
import glob
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# Root of the antigravity-agent-factory project
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
GLOBAL_WORKFLOWS_DIR = Path(r"C:\Users\wpoga\.gemini\antigravity\global_workflows")
WORKFLOWS_DIR = PROJECT_ROOT / ".agent" / "workflows"
AGENTS_DIR = PROJECT_ROOT / ".agent" / "agents"
SKILLS_DIR = PROJECT_ROOT / ".agent" / "skills"
RULES_DIR = PROJECT_ROOT / ".agent" / "rules"
BLUEPRINTS_DIR = PROJECT_ROOT / ".agent" / "blueprints"
KNOWLEDGE_DIR = PROJECT_ROOT / ".agent" / "knowledge"
ROOT_KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
PATTERNS_DIR = PROJECT_ROOT / ".agent" / "patterns"


class WorkflowPhase(BaseModel):
    """A single phase/step within a workflow."""

    name: str
    goal: str = ""
    actions: List[str] = Field(default_factory=list)
    agent: str = ""
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)


class Workflow(BaseModel):
    """Represents an Antigravity workflow (.md file)."""

    filename: str
    description: str = ""
    tags: List[str] = Field(default_factory=list)
    version: str = "1.0.0"
    title: str = ""
    phases: List[WorkflowPhase] = Field(default_factory=list)
    raw_body: str = ""
    workflow_type: str = "antigravity"  # antigravity | langgraph | crewai


def parse_workflow(filepath: Path) -> Workflow:
    """Parse a workflow .md file into a Workflow object."""
    content = filepath.read_text(encoding="utf-8")
    filename = filepath.stem

    # Split YAML frontmatter from body
    frontmatter = {}
    body = content
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
        body = fm_match.group(2)

    # Extract title from first H1
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename

    # Extract phases using a more robust block-splitting approach
    phases = []

    # Identify phase headers (## or ### followed by optional "Phase" and a number)
    # This split preserves the headers
    header_pattern = re.compile(
        r"(\n#{2,3}\s+(?:Phase\s+)?\d+[\.:]\s*.+)", re.MULTILINE
    )
    blocks = header_pattern.split(body)

    # The first element is content before any phase
    # The rest are pairs of [Header, Content]
    for i in range(1, len(blocks), 2):
        header = blocks[i]
        content_block = blocks[i + 1] if i + 1 < len(blocks) else ""

        # Parse phase name from header
        name_match = re.search(r"#{2,3}\s+(?:Phase\s+)?\d+[\.:]\s*(.+)", header)
        phase_name = name_match.group(1).strip() if name_match else "Unnamed Phase"

        # Initialize phase fields
        goal = ""
        agent = ""
        skills = []
        tools = []
        actions = []

        # Parse metadata lines (Goal, Agent, Skills, Tools)
        # We look for "- **Field**: Value" or "**Field**: Value"
        full_block = header + "\n" + content_block

        goal_match = re.search(
            r"^\s*[-*]?\s*\*\*Goal\*\*[:\s]+(.+)$",
            full_block,
            re.MULTILINE | re.IGNORECASE,
        )
        if goal_match:
            goal = goal_match.group(1).strip()

        agent_match = re.search(
            r"^\s*[-*]?\s*\*\*Agent\*\*[:\s]+`?([^`\n]+)`?$",
            full_block,
            re.MULTILINE | re.IGNORECASE,
        )
        if agent_match:
            agent = agent_match.group(1).strip()

        skills_match = re.search(
            r"^\s*[-*]?\s*\*\*Skills\*\*[:\s]+(.+)$",
            full_block,
            re.MULTILINE | re.IGNORECASE,
        )
        if skills_match:
            skills = [s.strip() for s in skills_match.group(1).split(",") if s.strip()]

        tools_match = re.search(
            r"^\s*[-*]?\s*\*\*Tools\*\*[:\s]+(.+)$",
            full_block,
            re.MULTILINE | re.IGNORECASE,
        )
        if tools_match:
            tools = [t.strip() for t in tools_match.group(1).split(",") if t.strip()]

        # Parse actions (any bullet/numbered list items not identified as metadata)
        # This is more inclusive: it looks for lines starting with - or 1.
        action_lines = re.findall(
            r"^\s*[-*]\s+(?!\*\*Goal\*\*|\*\*Agent\*\*|\*\*Skills\*\*|\*\*Tools\*\*|\*\*Action\*\*)(.+)$",
            content_block,
            re.MULTILINE | re.IGNORECASE,
        )
        actions.extend([a.strip() for a in action_lines if a.strip()])

        # Also look for explicit **Action**: lines (legacy support)
        legacy_actions = re.findall(
            r"^\s*[-*]?\s*\*\*Action\*\*[:\s]+(.+)$",
            full_block,
            re.MULTILINE | re.IGNORECASE,
        )
        actions.extend([a.strip() for a in legacy_actions if a.strip()])

        phases.append(
            WorkflowPhase(
                name=phase_name,
                goal=goal,
                agent=agent,
                skills=skills,
                tools=tools,
                actions=actions,
            )
        )

    return Workflow(
        filename=filename,
        description=frontmatter.get("description", ""),
        tags=frontmatter.get("tags", []),
        version=str(frontmatter.get("version", "1.0.0")),
        title=title,
        phases=phases,
        raw_body=body,
    )


def list_workflows() -> list[dict]:
    """List all workflows from both project and global directories."""
    wf_map = {}

    dirs = [("project", WORKFLOWS_DIR), ("global", GLOBAL_WORKFLOWS_DIR)]

    for source, wf_dir in dirs:
        if not wf_dir.exists():
            continue
        for md_file in wf_dir.glob("*.md"):
            name = md_file.stem
            try:
                wf = parse_workflow(md_file)
                entry = {
                    **wf.model_dump(),
                    "phase_count": len(wf.phases),
                    "sources": [source],
                }
                if name in wf_map:
                    wf_map[name]["sources"].append(source)
                else:
                    wf_map[name] = entry
            except Exception as e:
                entry = {
                    "filename": name,
                    "title": name,
                    "description": f"Error parsing ({source}): {e}",
                    "tags": [],
                    "version": "?",
                    "phase_count": 0,
                    "phases": [],
                    "sources": [source],
                }
                if name in wf_map:
                    wf_map[name]["sources"].append(source)
                else:
                    wf_map[name] = entry

    return sorted(wf_map.values(), key=lambda x: x["filename"])


def get_workflow(filename: str) -> dict:
    """Get a single workflow by filename. Checks project then global."""
    filepath = WORKFLOWS_DIR / f"{filename}.md"
    source = "project"
    if not filepath.exists():
        filepath = GLOBAL_WORKFLOWS_DIR / f"{filename}.md"
        source = "global"

    if not filepath.exists():
        return {"error": f"Workflow {filename} not found"}

    wf = parse_workflow(filepath)
    res = wf.model_dump()
    res["source"] = source
    return res


def save_workflow(filename: str, data: dict) -> dict:
    """Save a workflow with symmetric sync to both project and global dirs."""
    prj_path = WORKFLOWS_DIR / f"{filename}.md"
    glb_path = GLOBAL_WORKFLOWS_DIR / f"{filename}.md"

    # Check where it exists to decide on sync
    exists_prj = prj_path.exists()
    exists_glb = glb_path.exists()

    raw_body = data.get("raw_body")
    content = ""

    if raw_body:
        content = raw_body
    else:
        # Build YAML frontmatter from phases/metadata if no raw_body
        frontmatter = {
            "description": data.get("description", ""),
            "tags": data.get("tags", []),
            "version": data.get("version", "1.0.0"),
        }

        # Build markdown body
        title = data.get("title", filename)
        body_lines = [f"# {title}\n"]

        phases = data.get("phases", [])
        for i, phase in enumerate(phases):
            # We'll use level 3 (###) for saving to maintain standard
            body_lines.append(f"### {i+1}. {phase.get('name', 'Unnamed')}")
            if phase.get("goal"):
                body_lines.append(f"- **Goal**: {phase['goal']}")
            if phase.get("agent"):
                agent_name = phase["agent"]
                if not agent_name.startswith("`"):
                    agent_name = f"`{agent_name}`"
                body_lines.append(f"- **Agent**: {agent_name}")
            if phase.get("skills"):
                body_lines.append(f"- **Skills**: {', '.join(phase['skills'])}")
            if phase.get("tools"):
                body_lines.append(f"- **Tools**: {', '.join(phase['tools'])}")

            # Simplified actions (cleaner list)
            for action in phase.get("actions", []):
                body_lines.append(f"- {action}")
            body_lines.append("")

        content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n"
        content += "\n".join(body_lines)

    # Symmetry Sync: Write to both if they exist or if requested to sync
    write_paths = []
    if WORKFLOWS_DIR.exists():
        write_paths.append(prj_path)
    if GLOBAL_WORKFLOWS_DIR.exists():
        write_paths.append(glb_path)

    for p in write_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    return {"status": "saved", "filename": filename, "synced": len(write_paths) > 1}


def list_agents() -> list[dict]:
    """List all agent definitions."""
    agents = []
    for pattern_dir in sorted(AGENTS_DIR.iterdir()):
        if not pattern_dir.is_dir():
            continue
        for agent_file in sorted(pattern_dir.glob("*.md")):
            content = agent_file.read_text(encoding="utf-8")
            fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            meta = {}
            if fm_match:
                try:
                    meta = yaml.safe_load(fm_match.group(1)) or {}
                except yaml.YAMLError:
                    pass
            agents.append(
                {
                    "name": agent_file.stem,
                    "pattern": pattern_dir.name,
                    "description": meta.get("description", ""),
                    "path": str(agent_file.relative_to(PROJECT_ROOT)),
                }
            )
    return agents


def list_skills() -> list[dict]:
    """List all skill definitions."""
    skills = []
    for pattern_dir in sorted(SKILLS_DIR.iterdir()):
        if not pattern_dir.is_dir():
            continue
        for skill_dir in sorted(pattern_dir.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            content = skill_file.read_text(encoding="utf-8")
            fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            meta = {}
            if fm_match:
                try:
                    meta = yaml.safe_load(fm_match.group(1)) or {}
                except yaml.YAMLError:
                    pass
            skills.append(
                {
                    "name": meta.get("name", skill_dir.name),
                    "pattern": pattern_dir.name,
                    "description": meta.get("description", ""),
                    "tools": meta.get("tools", []),
                    "path": str(skill_file.relative_to(PROJECT_ROOT)),
                }
            )
    return skills


def list_scripts() -> list[dict]:
    """List all Python scripts in the scripts directory, including deep subdirectories."""
    scripts = []
    if not SCRIPTS_DIR.exists():
        return []

    for py_file in sorted(SCRIPTS_DIR.rglob("*.py")):
        if (
            "__pycache__" in str(py_file)
            or "site-packages" in str(py_file)
            or ".venv" in str(py_file)
        ):
            continue

        # Extract docstring
        try:
            content = py_file.read_text(encoding="utf-8")
            doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            docstring = doc_match.group(1).strip() if doc_match else ""
        except Exception:
            docstring = ""

        rel_path = str(py_file.relative_to(PROJECT_ROOT)).replace("\\", "/")
        category = "root"
        try:
            category = py_file.parent.relative_to(SCRIPTS_DIR).parts[0]
        except (IndexError, ValueError):
            pass

        scripts.append(
            {
                "name": py_file.stem,
                "path": rel_path,
                "docstring": docstring[:200],
                "category": category,
            }
        )
    return sorted(scripts, key=lambda x: x["path"])


def list_rules() -> list[dict]:
    """List all rules."""
    return list_simple_artifacts(RULES_DIR, "*.md")


def list_blueprints() -> list[dict]:
    """List all blueprints."""
    # Blueprints are folders with a blueprint.json inside
    return list_simple_artifacts(
        BLUEPRINTS_DIR, "**/blueprint.json", artifact_type="blueprint"
    )


def list_knowledge_files() -> list[dict]:
    """List all knowledge files (local and root)."""
    local = list_simple_artifacts(KNOWLEDGE_DIR, "**/*.json")
    root_knowledge = list_simple_artifacts(ROOT_KNOWLEDGE_DIR, "**/*.md")
    return local + root_knowledge


def list_patterns() -> list[dict]:
    """List all patterns."""
    return list_simple_artifacts(PATTERNS_DIR, "**/*.json")


def get_agent_config() -> dict:
    """Read .agent configuration/metadata."""
    config_file = PROJECT_ROOT / ".agent" / "config" / "settings.json"
    if config_file.exists():
        try:
            return json.loads(config_file.read_text(encoding="utf-8"))
        except Exception:
            return {"error": "Failed to parse settings.json"}
    return {"status": "default", "path": str(PROJECT_ROOT / ".agent")}


def save_agent_config(data: dict) -> dict:
    """Save .agent configuration."""
    config_file = PROJECT_ROOT / ".agent" / "config" / "settings.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"status": "saved"}


def list_simple_artifacts(
    directory: Path, glob_pattern: str = "*.md", artifact_type: str = "generic"
) -> list[dict]:
    """Generic list for simple markdown/JSON artifacts."""
    artifacts = []
    if not directory.exists():
        return []

    try:
        # Path.glob already supports ** patterns
        files = sorted(directory.glob(glob_pattern))
    except Exception:
        return []

    for art_file in files:
        try:
            content = art_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Try to extract frontmatter if md
        meta = {}
        if art_file.suffix == ".md":
            fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if fm_match:
                try:
                    meta = yaml.safe_load(fm_match.group(1)) or {}
                except yaml.YAMLError:
                    pass
        elif art_file.suffix == ".json":
            try:
                meta = json.loads(content)
            except json.JSONDecodeError:
                pass

        name = art_file.stem
        if name == "blueprint" and art_file.suffix == ".json":
            name = art_file.parent.name

        title = meta.get("title", meta.get("name", name))
        description = meta.get("description", "")

        if artifact_type == "blueprint" and "metadata" in meta:
            # Special handling for blueprint.json structure
            blueprint_meta = meta["metadata"]
            name = blueprint_meta.get("blueprintId", art_file.parent.name)
            title = blueprint_meta.get("blueprintName", name)
            description = blueprint_meta.get("description", "")

        artifacts.append(
            {
                "name": name,
                "path": str(art_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                "description": description,
                "title": title,
            }
        )
    return artifacts


# --- Entity Details & Saving ---


def get_agent(name: str) -> dict:
    """Find and return agent metadata and content."""
    for agent_file in AGENTS_DIR.rglob(f"{name}.md"):
        content = agent_file.read_text(encoding="utf-8")
        return {
            "name": name,
            "path": str(agent_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "content": content,
        }
    return {"error": f"Agent {name} not found"}


def save_agent(path: str, content: str) -> dict:
    """Save agent content."""
    fullpath = PROJECT_ROOT / path
    if not fullpath.exists():
        return {"error": f"File {path} not found"}
    fullpath.write_text(content, encoding="utf-8")
    return {"status": "saved", "path": path}


def get_skill(name: str) -> dict:
    """Find and return skill metadata and content."""
    for skill_file in SKILLS_DIR.rglob("SKILL.md"):
        if skill_file.parent.name == name:
            content = skill_file.read_text(encoding="utf-8")
            return {
                "name": name,
                "path": str(skill_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                "content": content,
            }
    return {"error": f"Skill {name} not found"}


def save_skill(path: str, content: str) -> dict:
    """Save skill content."""
    fullpath = PROJECT_ROOT / path
    if not fullpath.exists():
        return {"error": f"File {path} not found"}
    fullpath.write_text(content, encoding="utf-8")
    return {"status": "saved", "path": path}


def get_script(path: str) -> dict:
    """Return script content."""
    fullpath = PROJECT_ROOT / path
    if not fullpath.exists():
        return {"error": f"Script {path} not found"}
    content = fullpath.read_text(encoding="utf-8")
    return {"name": Path(path).stem, "path": path, "content": content}


def save_script(path: str, content: str) -> dict:
    """Save script content."""
    fullpath = PROJECT_ROOT / path
    if not fullpath.exists():
        return {"error": f"File {path} not found"}
    fullpath.write_text(content, encoding="utf-8")
    return {"status": "saved", "path": path}


def get_generic_artifact(path: str) -> dict:
    """Find and return generic artifact content."""
    fullpath = PROJECT_ROOT / path
    if not fullpath.exists():
        return {"error": f"Artifact {path} not found"}
    content = fullpath.read_text(encoding="utf-8")
    return {"name": Path(path).stem, "path": path, "content": content}


def save_generic_artifact(path: str, content: str) -> dict:
    """Save generic artifact content."""
    fullpath = PROJECT_ROOT / path
    # For safety, ensure it's within .agent or root knowledge
    if not (path.startswith(".agent") or path.startswith("knowledge")):
        return {"error": f"Access denied to path: {path}"}
    fullpath.parent.mkdir(parents=True, exist_ok=True)
    fullpath.write_text(content, encoding="utf-8")
    return {"status": "saved", "path": path}
