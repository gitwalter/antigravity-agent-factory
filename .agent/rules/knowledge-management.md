---
trigger: always_on
---

# Rule: Knowledge Management

## Context
Governs the creation, naming, and maintenance of Knowledge Items (KIs) in `.agent/knowledge/`.

## Requirements
- **Schema Validation**: All KIs MUST adhere to `schemas/knowledge-file.schema.json`.
- **Naming Convention**: `[topic]-patterns.json` or `[technology]-idioms.json`.
- **Mandatory Content**:
    - `id`: MUST match the filename (without extension).
    - `name`, `version`, `category`, `description`: Required top-level fields.
    - `patterns`: MUST be a non-empty object of successful implementation examples.
    - `best_practices`: Recommended approaches.
    - `anti_patterns`: Pitfalls to avoid.
- **Traceability**: All knowledge must trace back to Axiom A1 (Verifiability).

## Lifecycle
- **Creation**: Research topic -> Extract patterns -> Validate against schema -> Update `knowledge-manifest.json`.
- **Proactive Synthesis**: During Phase 7 (Monitor), agents MUST run `proactive_synthesis.py` to check for missing KIs from recently completed work.
- **Validation**: Run `pytest tests/knowledge/test_system_structure.py` to ensure schema compliance.
- **Updating**: Add new findings from conversation logs or project evolution.
- **Correction**: If knowledge is found to be incorrect or outdated, update immediately.

## Tooling
- ALWAYS check KI summaries at the start of a task (as per global rules).
- **Grounding**: ALWAYS search the `memory` MCP graph and relevant context MCPs (Drive, Gmail) before creating or updating Knowledge Items.
- Use `grep_search` to find related knowledge before creating duplicates.
