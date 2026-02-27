---
name: template-creator
description: Standardized template creation and validation with mandatory schema validation
type: skill
version: 1.0.0
category: factory
agents:
  - analyzer
  - comparator
  - grader
knowledge:
  - template.schema.json
tools:
  - none
related_skills:
  - skill-creator
  - agent-creator
templates:
  - none
---

# Template Creator

The **Template Creator** skill manages the generation and validation of templates (`.j2`, `.tmpl`) used by Factory agents to generate code or documentation. Templates reside in `{directories.templates}/`.

## Standard Structure

Templates follow `schemas/template.schema.json`. They must include a header or sidecar metadata that defines:
- `name`: Template identifier.
- `description`: What it generates.
- `type`: Category (code, doc, script).
- `variables`: List of variables required by the template.

## Process

1.  **Requirement**: Identify the repetitive structure to be templated.
2.  **Draft Template**: Create the Jinja2 file.
3.  **Define Metadata**: Ensure metadata complies with the schema.
4.  **Validate**: Run `scripts/quick_validate.py`.

## When to Use

- When creating a new template from scratch
- When improving or refactoring an existing template
- When standardizing an template to adhere to Factory schemas
- When another skill or agent requests a compliant template

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
