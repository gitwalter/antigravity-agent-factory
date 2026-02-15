"""
PABP Renderers — converts PABP JSON to Antigravity-native Markdown.

Provides rendering functions used by platform adapters and the PABPClient
to convert structured PABP JSON back into proper Antigravity Markdown
format matching the conventions in `.agent/agents/`, `.agent/skills/`,
and `.agent/workflows/`.

Antigravity agent format reference (from existing project files):
  # agent-name
  Description
  - **Role**: Agent
  - **Model**: default
  ## Purpose
  ## Philosophy
  ## Activation
  ## Skills        ← uses [[wiki-link]] refs
  ## Knowledge     ← uses **name** links
  ## Tooling

Antigravity skill format reference:
  ---
  description: ...
  ---
  # Skill Name
  ## Process / sections with code blocks

Antigravity workflow format reference:
  ---
  description: ...
  ---
  # Title
  ## sections

SDG - Love - Truth - Beauty
"""

import re
from typing import Dict


def _apply_rewrites(
    text: str,
    path_rewrites: Dict[str, str] = None,
    term_rewrites: Dict[str, str] = None,
) -> str:
    """Apply path and term rewrites to text content."""
    if path_rewrites:
        for pattern, replacement in path_rewrites.items():
            text = re.sub(pattern, replacement, text)
    if term_rewrites:
        for old, new in term_rewrites.items():
            text = text.replace(old, new)
    return text


def _content_has_code_blocks(content: str) -> bool:
    """Check if a content string already contains fenced code blocks."""
    return bool(re.search(r"```\w*\n", content))


def render_skill_markdown(
    pabp_data: dict,
    *,
    path_rewrites: Dict[str, str] = None,
    term_rewrites: Dict[str, str] = None,
) -> str:
    """Render PABP Skill JSON to Antigravity SKILL.md format.

    Antigravity format:
        ---
        description: <one-liner>
        ---

        # <Title>

        <description>

        ## Process / sections with code blocks
    """
    name = pabp_data.get("name", "unknown")
    description = pabp_data.get("description", "")
    sections = pabp_data.get("sections", [])

    lines = []

    # YAML frontmatter — Antigravity only uses 'description'
    lines.append("---")
    lines.append(f"description: {description}")
    lines.append("---")
    lines.append("")

    # Title
    title = name.replace("-", " ").title()
    lines.append(f"# {title}")
    lines.append("")

    # Description
    if description:
        lines.append(description)
        lines.append("")

    # Sections
    seen_content = set()  # Track emitted content to avoid duplicates
    for section in sections:
        sec_title = section.get("title", "")
        content = section.get("content", "")
        code_blocks = section.get("code_blocks", [])

        # Skip sections with empty titles that just repeat the description
        if not sec_title:
            # Only include if content adds new info beyond the description
            if content and content.strip() != description.strip():
                # Strip leading "# Title\n\n" from content if present
                cleaned = re.sub(r"^#\s+.*?\n\n", "", content.strip())
                if cleaned and cleaned != description:
                    # Skip if we already emitted this exact content
                    content_hash = hash(cleaned)
                    if content_hash in seen_content:
                        continue
                    seen_content.add(content_hash)
                    lines.append(cleaned)
                    lines.append("")
            continue

        lines.append(f"## {sec_title}")
        lines.append("")

        if content:
            # If content already contains fenced code blocks, use it as-is
            # and skip the separate code_blocks to avoid duplication
            if _content_has_code_blocks(content):
                lines.append(content)
                lines.append("")
                continue
            else:
                lines.append(content)
                lines.append("")

        # Only render separate code_blocks if content didn't already have them
        for cb in code_blocks:
            lang = cb.get("language", "")
            code = cb.get("code", "")
            desc = cb.get("description", "")
            if desc:
                lines.append(f"*{desc}*")
                lines.append("")
            lines.append(f"```{lang}")
            lines.append(code)
            lines.append("```")
            lines.append("")

    result = "\n".join(lines)
    return _apply_rewrites(result, path_rewrites, term_rewrites)


def render_agent_markdown(
    pabp_data: dict,
    *,
    path_rewrites: Dict[str, str] = None,
    term_rewrites: Dict[str, str] = None,
) -> str:
    """Render PABP Agent JSON to Antigravity agent Markdown format.

    Antigravity format:
        # agent-name

        Description

        - **Role**: Agent
        - **Model**: default

        ## Purpose
        ## Philosophy
        ## Activation
        ## Skills          ← [[wiki-link]] format
        ## Knowledge       ← **name** links
        ## Tooling         ← MCP servers, scripts, CLI tools
    """
    name = pabp_data.get("name", "unknown")
    description = pabp_data.get("description", "")
    purpose = pabp_data.get("purpose", "")
    philosophy = pabp_data.get("philosophy", "")
    skills = pabp_data.get("skills", [])
    knowledge = pabp_data.get("knowledge", [])
    activation = pabp_data.get("activation", {})
    constraints = pabp_data.get("constraints", [])
    system_instructions = pabp_data.get("system_instructions", "")
    tooling = pabp_data.get("tooling", {})

    lines = []

    # Title — use kebab-case name (Antigravity convention)
    lines.append(f"# {name}")
    lines.append("")

    # Description
    if description:
        lines.append(description)
        lines.append("")

    # Role and Model metadata
    lines.append(f"- **Role**: {pabp_data.get('role', 'Agent')}")
    lines.append(f"- **Model**: {pabp_data.get('model', 'default')}")
    lines.append("")

    # Purpose
    if purpose:
        lines.append("## Purpose")
        lines.append(purpose)
        lines.append("")

    # Philosophy
    if philosophy:
        lines.append("## Philosophy")
        lines.append(philosophy)
        lines.append("")

    # Activation — placed BEFORE Skills/Knowledge (Antigravity convention)
    if activation:
        triggers = activation.get("triggers", [])
        contexts = activation.get("contexts", [])
        if triggers or contexts:
            lines.append("## Activation")
            if triggers:
                lines.append("**Triggers:**")
                for t in triggers:
                    lines.append(f"- {t}")
                lines.append("")
            if contexts:
                lines.append("**Contexts:**")
                for c in contexts:
                    lines.append(f"- {c}")
                lines.append("")

    # Skills — use [[wiki-link]] format (Antigravity convention)
    if skills:
        lines.append("## Skills")
        for s in skills:
            lines.append(f"- [[{s}]]")
        lines.append("")

    # Knowledge — use **name** format (Antigravity convention - sibling dir)
    if knowledge:
        lines.append("## Knowledge")
        for k in knowledge:
            # Build relative path from .agent/agents/ to .agent/knowledge/
            if k.endswith(".json"):
                lines.append(f"- **{k}**")
            elif k.endswith(".md"):
                display = k.replace(".json", "").replace("-", " ").title()
                lines.append(f"- **{display}**")
            else:
                lines.append(f"- **{k}**")
        lines.append("")

    # Tooling — MCP servers, scripts, CLI tools (Antigravity convention)
    if tooling:
        mcp_servers = tooling.get("mcp_servers", [])
        scripts = tooling.get("scripts", [])
        cli_tools = tooling.get("cli_tools", [])
        apis = tooling.get("apis", [])

        if mcp_servers or scripts or cli_tools or apis:
            lines.append("## Tooling")
            if mcp_servers:
                lines.append("**MCP Servers:**")
                for srv in mcp_servers:
                    if isinstance(srv, dict):
                        srv_name = srv.get("name", "unknown")
                        required = srv.get("required", True)
                        req_label = "Required" if required else "Optional"
                        lines.append(f"- **{srv_name}** ({req_label})")
                    else:
                        lines.append(f"- **{srv}** (Required)")
                lines.append("")
            if scripts:
                lines.append("**Scripts:**")
                for script in scripts:
                    ref = (
                        script.get("ref", "unknown")
                        if isinstance(script, dict)
                        else str(script)
                    )
                    lines.append(f"- `{ref}`")
                lines.append("")
            if cli_tools:
                lines.append("**CLI Tools:**")
                for tool in cli_tools:
                    tool_name = (
                        tool.get("name", "unknown")
                        if isinstance(tool, dict)
                        else str(tool)
                    )
                    lines.append(f"- `{tool_name}`")
                lines.append("")
            if apis:
                lines.append("**APIs:**")
                for api in apis:
                    api_name = (
                        api.get("name", "unknown")
                        if isinstance(api, dict)
                        else str(api)
                    )
                    lines.append(f"- `{api_name}`")
                lines.append("")

    # Constraints
    if constraints:
        lines.append("## Constraints")
        for c in constraints:
            lines.append(f"- {c}")
        lines.append("")

    # System Instructions
    if system_instructions:
        lines.append("## System Instructions")
        lines.append(system_instructions)
        lines.append("")

    result = "\n".join(lines)
    return _apply_rewrites(result, path_rewrites, term_rewrites)


def render_workflow_markdown(
    pabp_data: dict,
    *,
    path_rewrites: Dict[str, str] = None,
    term_rewrites: Dict[str, str] = None,
) -> str:
    """Render PABP Workflow JSON to Antigravity workflow Markdown format.

    Antigravity format:
        ---
        description: <one-liner>
        ---
        # Title
        ## Overview / steps
    """
    name = pabp_data.get("name", "unknown")
    description = pabp_data.get("description", "")
    trigger = pabp_data.get("trigger", "")
    steps = pabp_data.get("steps", [])

    # Clean the title
    raw_name = name.strip()
    if raw_name.endswith("_workflow"):
        raw_name = raw_name[: -len("_workflow")]
    title = raw_name.replace("-", " ").replace("_", " ").title()

    # Short description for frontmatter
    short_desc = description.split("\n")[0].strip() if description else title
    if len(short_desc) > 120:
        short_desc = short_desc[:117] + "..."

    lines = []

    # YAML frontmatter (Antigravity convention)
    lines.append("---")
    lines.append(f"description: {short_desc}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")

    if description:
        lines.append(description)
        lines.append("")

    if trigger:
        lines.append("## Trigger Conditions")
        lines.append("")
        lines.append(trigger)
        lines.append("")

    if steps:
        lines.append("## Steps")
        lines.append("")
        for step in steps:
            action = step.get("action", step.get("id", "Step"))
            desc = step.get("description", "")
            lines.append(f"### {action}")
            lines.append("")
            if desc:
                lines.append(desc)
                lines.append("")

    result = "\n".join(lines)
    return _apply_rewrites(result, path_rewrites, term_rewrites)


def render_agent_crewai_yaml(pabp_data: dict, **kwargs) -> str:
    """Render Agent as CrewAI YAML format."""
    name = pabp_data.get("name", "unknown")
    desc = pabp_data.get("description", "")
    purpose = pabp_data.get("purpose", "")
    skills = pabp_data.get("skills", [])

    lines = [
        f"name: {name}",
        f"role: {purpose or desc}",
        f"goal: {purpose}",
        f"backstory: {desc}",
    ]
    if skills:
        lines.append("tools:")
        for s in skills:
            lines.append(f"  - {s}")
    return "\n".join(lines)


def render_agent_langchain_py(pabp_data: dict, **kwargs) -> str:
    """Render Agent as LangChain Python format."""
    name = pabp_data.get("name", "unknown")
    desc = pabp_data.get("description", "")
    purpose = pabp_data.get("purpose", "")

    return f'''"""
Agent: {name}
{desc}
"""
from langchain.agents import AgentExecutor

AGENT_NAME = "{name}"
AGENT_PURPOSE = """{purpose}"""
AGENT_DESCRIPTION = """{desc}"""
'''
