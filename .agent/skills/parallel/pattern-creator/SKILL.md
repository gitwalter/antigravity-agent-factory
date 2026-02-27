---
name: pattern-creator
description: Standardized agent pattern creation and validation
type: skill
version: 1.0.0
category: factory
agents:
  - analyzer
  - comparator
  - grader
knowledge:
  - agent-pattern.json
tools:
  - none
related_skills:
  - skill-creator
  - agent-creator
templates:
  - none
---

# Pattern Creator

The **Pattern Creator** skill manages the generation and validation of agent patterns. Patterns are meta-definitions used to generate specific agent instances. They reside in `{directories.patterns}/`.

## Standard Structure

Patterns are JSON files that follow the complex schema defined in `agent-pattern.json`. Key sections include:
- `metadata`: Pattern identity (ID, name, category).
- `frontmatter`: Blueprint for the generated agent's metadata.
- `sections`: Blueprint for the agent's markdown content (purpose, workflow, rules).
- `variables`: Parameters to be replaced during generation.

## Process

1.  **Abstraction**: Identify a reusable agent architectural pattern.
2.  **Draft JSON**: Build the pattern object.
3.  **Validate**: Run `scripts/quick_validate.py` (which uses `agent-pattern.json` as its schema).

## When to Use

- When creating a new pattern from scratch
- When improving or refactoring an existing pattern
- When standardizing an pattern to adhere to Factory schemas
- When another skill or agent requests a compliant pattern

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
