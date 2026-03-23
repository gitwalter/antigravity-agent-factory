---
name: workflow-creator
description: 'Standardized workflow creation and evaluation with mandatory schema
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
- workflow.schema.json
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

# Workflow Creator

The **Workflow Creator** skill is designed for the generation and validation of standardized workflow files. Workflows in the Factory are multi-step processes described in markdown files within `{directories.workflows}/`.

## Standard Structure

Workflows follow this markdown format:

1.  **YAML Frontmatter**: Includes `description` and optional `category`.
2.  **Instructional Content**: A numbered list of steps.
3.  **Turbo Annotations**: Use `// turbo` or `// turbo-all` for automated command execution.

## Validation

All workflows MUST pass `schemas/workflow.schema.json` validation. This ensures they are properly formatted and can be parsed by the orchestrator.

## Process

1.  **TDD Phase (RED)**:
    - Write a failing verification test in `tests/workflows/` (e.g., `test_my_new_workflow_validity`).
    - **Verify RED**: Run the test and confirm failure via `conda run -p D:\Anaconda\envs\cursor-factory pytest <test_path>`.
2.  **Implementation Phase (GREEN)**:
    - Draft the `.md` file in the appropriate domain subdirectory.
    - Write the minimal content needed to pass the test.
3.  **Validation Phase**:
    - Run `scripts/quick_validate.py` to ensure schema compliance.
    - **Verify GREEN**: Run the verification test again to confirm it passes.
4.  **REFACTOR & Sync**:
    - Clean up the workflow instructions.
    - **Mandatory Sync**: Run `conda run -p D:\Anaconda\envs\cursor-factory python scripts/sync_global_workflows.py`.

## When to Use

- When creating a new workflow from scratch
- When improving or refactoring an existing workflow
- When standardizing an workflow to adhere to Factory schemas
- When another skill or agent requests a compliant workflow

## Prerequisites

- Access to the Factory schemas in `schemas/`
- Understanding of the artifact structure defined in this skill
- The `quick_validate.py` script must be available for schema validation

## Best Practices

- Always validate against the schema before finalizing
- Keep the artifact focused and non-redundant with existing ones
- Follow the naming conventions defined in the Factory standards
- Document the artifact's purpose clearly in the description field
- Link related artifacts in the `related_skills` or `related_knowledge` fields
