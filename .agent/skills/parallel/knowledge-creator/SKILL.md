---
name: knowledge-creator
description: 'Standardized knowledge file creation and validation with mandatory schema
  validation

  '
type: skill
version: 1.0.0
category: factory
agents:
- analyzer
- comparator
- grader
knowledge:
- knowledge-file.schema.json
tools:
- none
related_skills:
- skill-creator
- agent-creator
templates:
- none
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Knowledge Creator

The **Knowledge Creator** skill manages the generation and validation of structured knowledge files (`.json`) used by the Factory agents. These files reside in `{directories.knowledge}/`.

## Standard Structure

Knowledge files are JSON objects that follow `schemas/knowledge-file.schema.json`. They typically include:
- `description`: Purpose.
- `version`: Semver versioning.
- `category`: Classification.
- `content`: The actual structured data (e.g., lists of tools, patterns, or facts).
- **Validation**: Every knowledge file MUST pass `tests/knowledge/test_system_structure.py`.

## Process

1.  **TDD Phase (RED)**:
    - Write a failing test in `tests/knowledge/` representing the new data structure requirements.
    - **Verify RED**: Run `conda run -p D:\Anaconda\envs\cursor-factory pytest tests/knowledge/test_system_structure.py` and confirm failure.
2.  **Implementation Phase (GREEN)**:
    - Draft the JSON object structure following `schemas/knowledge-file.schema.json`.
3.  **Validation Phase**:
    - **Verify GREEN**: Run structural tests and confirm pass.
    - Run structural verification: `conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/verify_structures.py`.
4.  **Sync**:
    - Update registries: `conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/sync_artifacts.py`.
    - **Mandatory Global Sync**: Run `conda run -p D:\Anaconda\envs\cursor-factory python scripts/sync_global_workflows.py`.

## When to Use

- When creating a new knowledge file from scratch
- When improving or refactoring an existing knowledge file
- When standardizing an knowledge file to adhere to Factory schemas
- When another skill or agent requests a compliant knowledge file

## Prerequisites

- Access to the Factory schemas in `schemas/`
- Understanding of the artifact structure defined in this skill
- `scripts/validation/verify_structures.py` must be available for structural checks

## Best Practices

- Always validate against the schema before finalizing
- Keep the artifact focused and non-redundant with existing ones
- Follow the naming conventions defined in the Factory standards
- Document the artifact's purpose clearly in the description field
- Link related artifacts in the `related_skills` or `related_knowledge` fields
