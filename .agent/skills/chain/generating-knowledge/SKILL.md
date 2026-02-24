---
description: JSON knowledge file generation with mandatory schema validation against
  schemas/knowledge-file.schema.json
name: generating-knowledge
type: skill
---
# Knowledge Generation

JSON knowledge file generation with mandatory schema validation against schemas/knowledge-file.schema.json

Generates structured JSON knowledge files for target projects with mandatory schema validation against `schemas/knowledge-file.schema.json`.

## Canonical Schema Reference

All knowledge files MUST validate against `schemas/knowledge-file.schema.json`. Required fields:

| Field | Type | Constraints |
|-------|------|-------------|
| `$schema` | const | Must be `"http://json-schema.org/draft-07/schema#"` |
| `id` | string | Pattern: `^[a-z0-9-]+$`, min 3 chars, matches filename without .json |
| `title` | string | Min 10 chars |
| `description` | string | Min 20 chars |
| `version` | string | Semantic version |
| `category` | enum | ONLY: core, rag, agent-patterns, integration, observability, specialized, workflow, optimization, security, testing, ai-ml, trading, sap, dotnet, java, web |
| `axiomAlignment` | object | Required keys: A1_verifiability, A2_user_primacy, A3_transparency, A4_non_harm, A5_consistency (each min 10 chars) |
| `patterns` | object | Min 1 property. Each entry MUST have: description (min 20), use_when (min 10), code_example (min 20), best_practices (array, min 2 items each min 10 chars) |
| `best_practices` | array | Min 2 concrete items (min 15 chars) - **MANDATORY** |
| `anti_patterns` | array | Min 2 concrete items (min 15 chars) - **MANDATORY** |
| `related_skills` | array | Min 1 item, each `^[a-z0-9-]+$` |
| `related_knowledge` | array | Min 1 item, each `^[a-z0-9-]+\\.json$` |

**Category mapping:** data-science → `ai-ml`, general → `specialized`, devops → `integration`, meta → `core`

**CRITICAL:** `patterns` must be an OBJECT (not array), with entries containing `description`, `use_when`, `code_example`, and `best_practices`.

## Correct Knowledge File Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "id": "my-patterns",
  "title": "My Domain Patterns for Reference",
  "description": "Patterns for handling domain-specific integrations and workflows.",
  "version": "1.0.0",
  "category": "integration",
  "axiomAlignment": {
    "A1_verifiability": "Patterns include verifiable assertions.",
    "A2_user_primacy": "User intent guides pattern selection.",
    "A3_transparency": "Pattern logic is documented.",
    "A4_non_harm": "Patterns avoid harmful side effects.",
    "A5_consistency": "Patterns align with project conventions."
  },
  "patterns": {
    "pattern-key": {
      "description": "When to use this pattern with sufficient detail.",
      "use_when": "Integration with external API required.",
      "code_example": "// Example code snippet here...",
      "best_practices": [
        "First best practice with enough detail.",
        "Second best practice requirement."
      ]
    }
  },
  "related_skills": ["api-design", "integration"],
  "related_knowledge": ["api-patterns.json"],
  "best_practices": ["First best practice", "Second best practice"],
  "anti_patterns": ["First anti-pattern", "Second anti-pattern"]
}
```

## Common Violations

| Violation | Fix |
|-----------|-----|
| `patterns` is array | Use object with named keys |
| Missing `axiomAlignment` | Add all 5 required axiom keys |
| Invalid category | Map to allowed enum or use mapping table |
| `id` doesn't match filename | Ensure `id` equals filename without `.json` |
| Short descriptions | Min 10 chars title, 20 chars description |
| `best_practices` has &lt; 2 items | Add at least 2 practices |
| `related_knowledge` empty | Add at least 1 `.json` filename |
| Missing `best_practices`/`anti_patterns` | Add both mandatory lists with at least 2 items each |

## Process

1. **Determine required files** — Based on stack, identify needed knowledge files (e.g. naming-conventions, api-patterns).
2. **Map category** — Use schema-allowed categories; apply mapping for legacy values (data-science→ai-ml, etc.).
3. **Build structure** — Populate all required fields per schema; ensure `patterns` is object with complete entries and `best_practices`/`anti_patterns` are provided.
4. **Validate** — Run schema validation and `verify_structures.py` before committing.

## Post-Creation Sync

After creating or updating knowledge files, run:

```bash
91. python scripts/build_knowledge_crossref.py
92. python scripts/validation/verify_structures.py
```

Then run `repo-sync` skill to validate artifact consistency.

## Important Rules

1. **Use `{directories.XXX}` path variables** — NEVER hardcode directory paths. See `{directories.config}/settings.json` for the full mapping.
2. **Lowercase kebab-case filenames** — All knowledge files must use lowercase kebab-case (e.g. `best-practices.json`).
3. **Validate against schema** — Always run validation before committing. Use `schemas/knowledge-file.schema.json`.

## References

- `{directories.knowledge}/stack-capabilities.json`
- `{directories.knowledge}/best-practices.json`
- `{directories.knowledge}/knowledge-cross-reference.json`
- `schemas/knowledge-file.schema.json`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.
