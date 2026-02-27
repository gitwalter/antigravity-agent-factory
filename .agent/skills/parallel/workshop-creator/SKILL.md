---
name: workshop-creator
description: Standardized workshop creation and validation
type: skill
version: 1.0.0
category: factory
agents:
  - analyzer
  - comparator
  - grader
knowledge:
  - none
tools:
  - none
related_skills:
  - skill-creator
templates:
  - none
---

# Workshop Creator

The **Workshop Creator** skill manages the creation of training workshops for the Factory. Workshops are comprehensive guides that teach specific concepts, technologies, or workflows. They reside in `docs/workshops/`.

## Standard Structure

Workshops are Markdown files following a specific naming convention (`LX_name.md`) and containing:
1.  **Level (LX)**: Incremental difficulty.
2.  **Learning Objectives**: What the user will learn.
3.  **Core Content**: Detailed instructions and code examples.
4.  **Practice**: Hands-on exercises.

## Process

1.  **Syllabus**: Define the learning path.
2.  **Draft**: Write the workshop in Markdown.
3.  **Validate**: Run `scripts/quick_validate.py` to ensure naming and section compliance.

## When to Use

- When creating a new workshop from scratch
- When improving or refactoring an existing workshop
- When standardizing an workshop to adhere to Factory schemas
- When another skill or agent requests a compliant workshop

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
