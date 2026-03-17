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
from typing import Optional, List, Dict, Any, Union


# Root of the antigravity-agent-factory project
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
GLOBAL_WORKFLOWS_DIR = Path.home() / ".gemini" / "antigravity" / "global_workflows"
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
    agents: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)

    @property
    def agent(self) -> str:
        """Backward compatibility for 'agent' attribute."""
        return self.agents[0] if self.agents else ""

    @agent.setter
    def agent(self, value: str):
        """Backward compatibility for setting 'agent'."""
        if value:
            self.agents = [value]
        else:
            self.agents = []


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


def parse_workflow(filename: Union[str, Path]) -> Workflow:
    """Parse a workflow .md file into a Workflow object."""
    filename_str = str(filename)

    # Determine the directory relative to the current file
    current_dir = Path(__file__).parent.parent.parent
    workflows_path = current_dir / ".agent" / "workflows"

    if os.path.isabs(filename_str):
        filepath = Path(filename_str)
    else:
        filepath = workflows_path / filename_str

    if not filepath.exists():
        raise FileNotFoundError(f"Workflow file {filename} not found at {filepath}")

    content = filepath.read_text(encoding="utf-8")
    # filename already provided as str

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

    # Identify phases
    phases = []

    # Strategy: Frontmatter-First
    # If the frontmatter has a 'steps' array, it is the primary source of truth for the UI
    fm_steps = frontmatter.get("steps", [])
    if isinstance(fm_steps, list) and len(fm_steps) > 0:
        for idx, step in enumerate(fm_steps):
            if isinstance(step, dict):
                phase_name = step.get("name", f"Step {idx+1}")
                # Map schema-defined 'agents' (list) or 'agent' (string legacy)
                agents = step.get("agents", [])
                if not agents and "agent" in step:
                    agents = [step["agent"]]

                phases.append(
                    WorkflowPhase(
                        name=phase_name,
                        goal=step.get("goal", step.get("description", "")),
                        agents=agents,
                        skills=step.get("skills", []),
                        tools=step.get("tools", []),
                        actions=step.get("actions", []),
                    )
                )

    # If no phases from frontmatter, fall back to parsing the Markdown body (Legacy Support)
    if not phases:
        # Identify phase headers (## or ### followed by optional "Phase" or "Step" and a number)
        # This split preserves the headers
        header_pattern = re.compile(
            r"(^#{2,3}\s+(?:Phase|Step)?\s*\d+[\.:]\s*.+)", re.MULTILINE | re.IGNORECASE
        )
        blocks = header_pattern.split(body)

        # The first element is content before any phase
        # The rest are pairs of [Header, Content]
        for i in range(1, len(blocks), 2):
            header = blocks[i]
            content_block = blocks[i + 1] if i + 1 < len(blocks) else ""

            # Parse phase name from header
            name_match = re.search(
                r"#{2,3}\s+(?:Phase|Step)?\s*\d+[\.:]\s*(.+)", header, re.IGNORECASE
            )
            phase_name = name_match.group(1).strip() if name_match else "Unnamed Phase"

            # Initialize phase fields
            goal = ""
            agents = []
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
                r"^\s*[-*]?\s*\*\*Agents?\*\*[:\s]+(.+)$",
                full_block,
                re.MULTILINE | re.IGNORECASE,
            )
            if agent_match:
                agents = [
                    a.strip().replace("`", "")
                    for a in agent_match.group(1).split(",")
                    if a.strip()
                ]

            skills_match = re.search(
                r"^\s*[-*]?\s*\*\*Skills\*\*[:\s]+(.+)$",
                full_block,
                re.MULTILINE | re.IGNORECASE,
            )
            if skills_match:
                skills = [
                    s.strip() for s in skills_match.group(1).split(",") if s.strip()
                ]

            tools_match = re.search(
                r"^\s*[-*]?\s*\*\*Tools\*\*[:\s]+(.+)$",
                full_block,
                re.MULTILINE | re.IGNORECASE,
            )
            if tools_match:
                tools = [
                    t.strip() for t in tools_match.group(1).split(",") if t.strip()
                ]

            # Parse actions (any bullet/numbered list items not identified as metadata)
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
                    agents=agents,
                    skills=skills,
                    tools=tools,
                    actions=actions,
                )
            )

    return Workflow(
        filename=Path(filename_str).name,
        description=frontmatter.get("description", ""),
        tags=frontmatter.get("tags", []),
        version=str(frontmatter.get("version", "1.0.0")),
        title=title,
        phases=phases,
        raw_body=body,
    )


def list_workflows() -> list[dict]:
    """List all workflows from the project directory."""
    workflows = []
    if not WORKFLOWS_DIR.exists():
        return []

    for md_file in WORKFLOWS_DIR.rglob("*.md"):
        # Calculate filename relative to WORKFLOWS_DIR (e.g. "research.md" or "org/paths.md")
        try:
            rel_path = md_file.relative_to(WORKFLOWS_DIR)
            filename = str(rel_path).replace("\\", "/")
            name = md_file.stem

            wf = parse_workflow(filename)
            entry = {
                **wf.model_dump(),
                "phase_count": len(wf.phases),
                "source": "project",
            }
            workflows.append(entry)
        except Exception as e:
            workflows.append(
                {
                    "filename": str(md_file.relative_to(WORKFLOWS_DIR)).replace(
                        "\\", "/"
                    ),
                    "title": md_file.stem,
                    "description": f"Error parsing: {e}",
                    "tags": [],
                    "version": "?",
                    "phase_count": 0,
                    "phases": [],
                    "source": "project",
                }
            )

    return sorted(workflows, key=lambda x: x["filename"])


def get_workflow(filename: str) -> dict:
    """Get a single workflow by filename. Only checks project directory."""
    # Robustly handle extensions
    clean_filename = filename
    if clean_filename.lower().endswith(".md"):
        clean_filename = clean_filename[:-3]

    filepath = WORKFLOWS_DIR / f"{clean_filename}.md"
    if not filepath.exists():
        return {"error": f"Workflow {filename} not found"}

    wf = parse_workflow(str(filepath))
    res = wf.model_dump()
    res["source"] = "project"
    return res


def save_workflow(
    filename: str, data: Union[dict, Workflow], raw_body: str = None
) -> dict:
    """Save a workflow to the project workflows directory."""
    # Robustly handle extensions
    clean_filename = filename
    if clean_filename.lower().endswith(".md"):
        clean_filename = clean_filename[:-3]

    prj_path = WORKFLOWS_DIR / f"{clean_filename}.md"

    if isinstance(data, Workflow):
        data = data.model_dump()

    # Check where it exists to decide on sync
    exists_prj = prj_path.exists()

    content = ""

    if raw_body:
        content = raw_body
    else:
        # Build Markdown and Sync Frontmatter
        phases_data = data.get("phases", [])

        # Convert Pydantic models to dicts if necessary
        clean_phases = []
        for p in phases_data:
            if hasattr(p, "model_dump"):
                clean_phases.append(p.model_dump())
            elif isinstance(p, dict):
                clean_phases.append(p)

        # Build frontmatter steps array for schema compliance
        fm_steps = []
        for idx, p in enumerate(clean_phases):
            step_agents = p.get("agents", [])
            if not step_agents and p.get("agent"):
                step_agents = [p["agent"]]
            if not step_agents:
                step_agents = ["@Architect"]

            fm_steps.append(
                {
                    "name": p.get("name", f"Step {idx+1}"),
                    "goal": p.get(
                        "goal", p.get("description", "Execute step actions.")
                    ),
                    "agents": step_agents,
                    "skills": p.get("skills", []),
                    "tools": p.get("tools", []),
                    "actions": p.get("actions", []),
                }
            )

        # Ensure schema compliance for mandatory fields
        wf_name = filename
        wf_desc = data.get("description", "")
        if len(wf_desc) < 20:
            wf_desc = f"Antigravity workflow for {filename}. Standardized for IDX Visual Editor."

        wf_agents = data.get("agents", [])
        if not wf_agents:
            # Aggregate agents from phases
            wf_agents = list(
                set([a for p in clean_phases for a in p.get("agents", [])])
            )
        if not wf_agents:
            wf_agents = ["@Architect"]

        # Ensure min 2 steps for schema compliance
        if len(fm_steps) == 0:
            fm_steps = [
                {
                    "name": "Initialization",
                    "goal": "Initialize the workflow context.",
                    "agents": ["@Architect"],
                },
                {
                    "name": "Verification",
                    "goal": "Verify the results of the workflow.",
                    "agents": ["@Architect"],
                },
            ]
        elif len(fm_steps) == 1:
            fm_steps.append(
                {
                    "name": "Verification",
                    "goal": "Verify the results of the workflow.",
                    "agents": ["@Architect"],
                }
            )

        frontmatter = {
            "name": wf_name,
            "description": wf_desc,
            "version": data.get("version", "1.0.0"),
            "type": data.get("type", "sequential"),
            "domain": data.get("domain", "universal"),
            "agents": wf_agents,
            "blueprints": data.get("blueprints", ["universal"]),
            "tags": data.get("tags", []),
            "steps": fm_steps,
        }

        # Build markdown body
        title = data.get("title", filename)
        body_lines = [f"# {title}\n"]

        for i, phase in enumerate(clean_phases):
            # We'll use level 3 (###) for saving to maintain standard
            body_lines.append(f"### {i+1}. {phase.get('name', 'Unnamed')}")
            if phase.get("goal"):
                body_lines.append(f"- **Goal**: {phase['goal']}")

            agents = phase.get("agents", [])
            if agents:
                formatted_agents = [
                    f"`{a}`" if not a.startswith("`") else a for a in agents if a
                ]
                if formatted_agents:
                    body_lines.append(f"- **Agents**: {', '.join(formatted_agents)}")

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

    # Write to project workflows directory
    prj_path.parent.mkdir(parents=True, exist_ok=True)
    prj_path.write_text(content, encoding="utf-8")

    return {"status": "saved", "filename": filename, "synced": False}


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
                    "id": agent_file.stem,
                    "name": agent_file.stem,
                    "pattern": pattern_dir.name,
                    "description": meta.get("description", ""),
                    "path": str(agent_file.relative_to(PROJECT_ROOT)).replace(
                        "\\", "/"
                    ),
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
                    "id": f"{pattern_dir.name}/{skill_dir.name}",
                    "name": meta.get("name", skill_dir.name),
                    "pattern": pattern_dir.name,
                    "description": meta.get("description", ""),
                    "tools": meta.get("tools", []),
                    "path": str(skill_file.relative_to(PROJECT_ROOT)).replace(
                        "\\", "/"
                    ),
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
    """List all governance rules with structured metadata."""
    return list_simple_artifacts(RULES_DIR, "*.md", artifact_type="rule")


def parse_rule(filepath: Path) -> dict:
    """Parse a rule .md file into a structured dictionary."""
    content = filepath.read_text(encoding="utf-8")
    name = filepath.stem

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

    # Extract sections from markdown
    # Rules often have H1 title, H2 Context, H2 Requirements, H2 Process
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else name

    # Context
    context_match = re.search(
        r"##\s+Context\n(.*?)(?=\n##|$)", body, re.DOTALL | re.IGNORECASE
    )
    context = context_match.group(1).strip() if context_match else ""

    # Requirements (List)
    req_match = re.search(
        r"##\s+Requirements\n(.*?)(?=\n##|$)", body, re.DOTALL | re.IGNORECASE
    )
    requirements = []
    if req_match:
        requirements = [
            r.strip().replace("- ", "").replace("* ", "")
            for r in req_match.group(1).split("\n")
            if r.strip().startswith(("- ", "* "))
        ]

    # Process (List)
    proc_match = re.search(
        r"##\s+Process\n(.*?)(?=\n##|$)", body, re.DOTALL | re.IGNORECASE
    )
    process = []
    if proc_match:
        process = [
            p.strip().replace("- ", "").replace("* ", "")
            for p in proc_match.group(1).split("\n")
            if p.strip().startswith(("- ", "* "))
        ]

    return {
        "name": name,
        "title": title,
        "trigger": frontmatter.get("trigger", "manual"),
        "context": context,
        "requirements": requirements,
        "process": process,
        "path": str(filepath.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "content": content,
    }


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
        if artifact_type == "rule" and art_file.suffix == ".md":
            try:
                rule_data = parse_rule(art_file)
                artifacts.append(
                    {
                        "name": rule_data["name"],
                        "path": rule_data["path"],
                        "description": rule_data["context"][:200],
                        "title": rule_data["title"],
                        "type": "rule",
                    }
                )
                continue
            except Exception:
                pass

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
