# Rule: Skill Development

## Context
Enforces consistency and quality in skill creation within the `.agent/skills/` directory.

## Requirements
- **Schema Validation**: All skills MUST adhere to `schemas/skill.schema.json`.
- **File Structure**: Skills are folders containing `SKILL.md`.
- **Required Sections**: `SKILL.md` MUST include:
    - `When to Use`
    - `Prerequisites`
    - `Process` (Step-by-step instructions)
    - `Best Practices`
- **Axiom Alignment**: Frontmatter MUST include an `axioms` block linking back to `.agentrules` (A1-A6).
- **MCP Integration**:
    - Skills that require external data or complex logic MUST specify the required MCP tools in their `Prerequisites`.

## Directory Organization
- `operational/`: Process-oriented skills (e.g., project management, workflows).
- `technical/`: Technical implementations (e.g., coding patterns, API integrations).
- `integrations/`: MCP and external system connectors.

## Workflow
1. Use `view_file` on `schemas/skill.schema.json` before starting.
2. Draft `SKILL.md` with appropriate frontmatter.
3. Update `skill-catalog.json` with the new skill metadata.
