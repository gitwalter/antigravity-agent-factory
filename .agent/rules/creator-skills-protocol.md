# Rule: Creator Skills Protocol

## Context
This rule governs the creation and maintenance of core factory artifacts (Agents, Skills, Knowledge, Workflows) by mandating the use of specialized "creator" skills.

## Requirements
1.  **Mandatory Creator Usage**: ALWAYS use the designated "creator" skill when generating or modifying factory-level artifacts:
    - **Agents**: Use `agent-creator`.
    - **Skills**: Use `skill-creator`.
    - **Knowledge**: Use `knowledge-creator`.
    - **Workflows**: Use `workflow-creator` (if available) or follow `workflow-standard.md`.
2.  **Consistency**: All "creator" skills MUST follow a consistent structure:
    - Include a **Validation Phase** in the `Process`.
    - Adhere to the `axioms` in frontmatter.
    - Leverage templates from `.agent/templates/`.
3.  **Validation Enforcement**: No artifact is considered "Factory Ready" until it passes its respective structural validation:
    - **Knowledge**: `pytest tests/knowledge/test_system_structure.py` and `python scripts/validation/verify_structures.py`.
    - **Workflows**: `pytest tests/validation/test_workflow_structure.py`.
    - **Skills**: `pytest tests/unit/test_skill_structure.py` (if available) and schema validation.
4.  **Naming Convention**: All "creator" skills follow the `[asset]-creator` pattern for easy discovery.

## Workflow Alignment
- When a task requires a new asset, search for the `[asset]-creator` skill first.
- If a creator skill is found, follow its `SKILL.md` strictly.
- If it doesn't exist, use `skill-creator` to build it first.

---
**Axiom Alignment**: A1 (Verifiability), A5 (Consistency).
