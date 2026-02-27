---
name: knowledge-creator
description: Standardized knowledge file creation and validation with mandatory schema validation
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
---

# Knowledge Creator

The **Knowledge Creator** skill manages the generation and validation of structured knowledge files (`.json`) used by the Factory agents. These files reside in `{directories.knowledge}/`.

## Standard Structure

Knowledge files are JSON objects that follow `schemas/knowledge-file.schema.json`. They typically include:
- `title`: Name of the knowledge set.
- `description`: Purpose.
- `version`: Semver versioning.
- `category`: Classification.
- `content`: The actual structured data (e.g., lists of tools, patterns, or facts).

## Process

1.  **Gather Information**: Identify the facts or data to be structured.
2.  **Draft JSON**: Build the object structure.
3.  **Validate**: Run `scripts/quick_validate.py` against the `.json` file.
4.  **Sync**: Run `build_knowledge_crossref.py` to update the global registry.

## When to Use

- When creating a new knowledge file from scratch
- When improving or refactoring an existing knowledge file
- When standardizing an knowledge file to adhere to Factory schemas
- When another skill or agent requests a compliant knowledge file

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
