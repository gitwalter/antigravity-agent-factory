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
- **Pattern Categorization**: Every skill MUST reside in a behavioral pattern directory (`chain`, `parallel`, `routing`, etc.).
- **Level 3 Bundling**: Skills MUST be directory bundles with `scripts/` and `references/` subfolders for deterministic logic.
- **MCP Integration**:
    - Skills that require external data or complex logic MUST specify the required MCP tools in their `Prerequisites`.

## Directory Organization
Skills MUST be organized into behavioral patterns:
- `chain/`: Sequential process logic.
- `parallel/`: Independent auditing/transformation.
- `routing/`: Interface and system integration logic.
- `evaluator-optimizer/`: Verification and quality logic.
- `orchestrator-workers/`: Handoff and delegation logic.

## Level 3 Bundle Architecture
Every skill MUST be a directory bundle with:
- `SKILL.md`: Level 1 (Metadata/YAML) & Level 2 (Body/Process).
- `scripts/`: Level 3 Deterministic Python/Shell scripts.
- `references/`: Level 3 Detailed documentation and KIs.
- `assets/`: Level 3 Media and static resources.

## Workflow
1. Use `init_skill.py` from `skill-creator` to bootstrap the bundle.
2. Draft `SKILL.md` using gerund naming (e.g., `generating-agents`).
3. Limit `SKILL.md` body to <500 lines; move implementation details to `scripts/`.
4. Update `skill-catalog.json`.
