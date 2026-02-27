---
name: blueprint-creator
description: Standardized blueprint creation and validation with mandatory schema validation
type: skill
version: 1.0.0
category: factory
agents:
  - analyzer
  - comparator
  - grader
knowledge:
  - blueprint.schema.json
tools:
  - none
related_skills:
  - skill-creator
  - agent-creator
templates:
  - none
---

# Blueprint Creator

The **Blueprint Creator** skill ensures that all task decomposition blueprints are valid and follow the `schemas/blueprint.schema.json` format. Blueprints are the blueprints for complex task execution.

## Standard Structure

Blueprints reside in `{directories.blueprints}/*/blueprint.json` and must contain:
- `id`: Unique identifier.
- `name`: Human-readable name.
- `agents`: List of participating agents.
- `steps`: Array of execution steps.

## Process

1.  **Architecture**: Design the multi-agent orchestration.
2.  **Define steps**: Map out the sequence of activities.
3.  **Draft JSON**: Create the `blueprint.json` file.
4.  **Validate**: Run `scripts/quick_validate.py`.

## When to Use

- When creating a new blueprint from scratch
- When improving or refactoring an existing blueprint
- When standardizing an blueprint to adhere to Factory schemas
- When another skill or agent requests a compliant blueprint

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
