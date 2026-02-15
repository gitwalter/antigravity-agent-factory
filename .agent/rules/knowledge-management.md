# Rule: Knowledge Management

## Context
Governs the creation, naming, and maintenance of Knowledge Items (KIs) in `.agent/knowledge/`.

## Requirements
- **Schema Validation**: All KIs MUST adhere to `schemas/knowledge-file.schema.json`.
- **Naming Convention**: `[topic]-patterns.json` or `[technology]-idioms.json`.
- **Mandatory Content**:
    - `patterns`: Successful implementation examples.
    - `best_practices`: Recommended approaches.
    - `anti_patterns`: Pitfalls to avoid.
- **Traceability**: All knowledge must trace back to Axiom A1 (Verifiability).

## Lifecycle
- **Creation**: Research topic -> Extract patterns -> Validate against schema -> Update `knowledge-manifest.json`.
- **Updating**: Add new findings from conversation logs or project evolution.
- **Correction**: If knowledge is found to be incorrect or outdated, update immediately.

## Tooling
- ALWAYS check KI summaries at the start of a task (as per global rules).
- Use `grep_search` to find related knowledge before creating duplicates.
