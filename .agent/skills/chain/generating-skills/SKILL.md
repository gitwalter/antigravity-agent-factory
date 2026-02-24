---
description: Skill definition file generation with mandatory schema validation against
  schemas/skill.schema.json
name: generating-skills
type: skill
---
# Skill Generation

Skill definition file generation with mandatory schema validation against schemas/skill.schema.json

Generates skill definition files from patterns with mandatory schema validation.

## Canonical Schema Reference

All generated skills MUST validate against `schemas/skill.schema.json`:

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string | Pattern: `^[a-z0-9-]+(/[a-z0-9-]+)*$`, min 3 chars, matches directory name |
| `description` | string | Min 20 chars |
| `type` | const | Must be `"skill"` |
| `version` | string | Semantic version `^\d+\.\d+\.\d+$` |
| `category` | enum | ONLY: core, rag, agent-patterns, integration, observability, specialized, workflow, optimization, security, testing, ai-ml, trading, sap, dotnet, java, web, devops, onboarding, factory |
| `agents` | array | Min 1 item, each `^[a-z0-9-]+$` |
| `knowledge` | array | Min 1 item, each `^[a-z0-9-]+\.json$` (NO path prefixes) |
| `tools` | array | Min 1 item (use `["none"]`) |
| `related_skills` | array | Min 1 item, each `^[a-z0-9-]+$` |
| `templates` | array | Min 1 item (use `["none"]`) |

**Category mapping:**

| Natural Category | Use Instead |
|-----------------|-------------|
| data-science | `ai-ml` |
| meta | `factory` |
| general | `specialized` |

## Validation Checklist (Before Write)

1. Ensure `name` matches skill directory (e.g. `pm/close-sprint` → `pm/close-sprint/`)
2. Confirm `knowledge` entries are bare filenames only (e.g. `best-practices.json`, NOT `knowledge/best-practices.json`)
3. Verify `category` is in the allowed enum; map natural categories per table above
4. Assert `tools` and `templates` have at least one item; use `["none"]` when no specific resources
5. Run `schema_validator.py --type skill` on the generated file before committing
6. **New Requirement**: Run `verify_structures.py` to ensure all mandatory markdown sections exist (H1, When to Use, Prerequisites, Process, Best Practices).

## Process
The generation and verification process must be followed sequentially to ensure all structural requirements are met.

### 1. Run Automated Verification

## Common Schema Violations

| Violation | Fix |
|-----------|-----|
| `knowledge: [knowledge/best-practices.json]` | Use `[best-practices.json]` (no path prefix) |
| `category: data-science` | Use `ai-ml` |
| `related_skills: []` | Add at least one related skill |
| `tools` omitted | Add `tools: ["none"]` |
| `version: 1.0` | Use semantic version `1.0.0` |

1. Review the task requirements.
2. Apply the skill's methodology.
3. **Mandatory Quality Gate Sequence**:
   - **Step 1: Header Verification**: Every skill MUST have a unique H1 title.
   - **Step 2: Section Enforcement**: Every skill MUST have: `When to Use`, `Prerequisites`, `Process`, and `Best Practices`.
   - **Step 3: Content Depth**: Every section MUST have at least 20 words of descriptive content (no empty headers).
   - **Step 4: Tool Validation**: Run `verify_structures.py` to assert compliance.
4. Validate the output against the defined criteria.
### Step 1: Load Skill Pattern
1. Load pattern from `{directories.patterns}/skills/{skill-id}.json`
2. Parse metadata, frontmatter, and sections

### Step 2: Apply Customizations
Override frontmatter, knowledge references, and MCP tool references as specified.

### Step 3: Render Markdown (Schema-First)
Convert pattern to markdown. **Ensure frontmatter satisfies all schema constraints** before writing.

### Step 4: Validate Before Write
71. Run `python scripts/validation/schema_validator.py --type skill` on the generated YAML frontmatter (or full SKILL.md). Fix any errors before committing.
72. Run `python scripts/validation/verify_structures.py` to ensure markdown section compliance.

### Step 5: Create Skill Directory
```
{TARGET}/{directories.skills}/{skill-name}/
├── SKILL.md
└── references/        # Optional
```

### Step 6: Post-Creation Sync (Factory Only)

When adding skills to the Cursor Agent Factory:

```powershell
python scripts/validation/schema_validator.py --type skill
python scripts/build_knowledge_crossref.py
88. python scripts/validation/validate_readme_structure.py --update
89. python scripts/validation/verify_structures.py
```

## Standard Skill Template

```markdown
---
name: {name}
description: {description}
type: skill
version: 1.0.0
category: {category}
knowledge: [best-practices.json]
tools: ["none"]
related_skills: [agent-generation]
templates: ["none"]
agents: [ai-app-developer]
---

# {title}

{introduction}

## When to Use

{mandatory details}

## Prerequisites

{mandatory details}

## Process

{process steps}

## Best Practices

{rules}
```

## Important Rules

1. **Schema-first** — Always validate against `schemas/skill.schema.json` before writing. Never skip validation.
2. **No path prefixes in knowledge** — Use `best-practices.json`, never `knowledge/best-practices.json`.
3. **Use `{directories.XXX}` path variables** — Never hardcode paths in generated content.
4. **Lowercase kebab-case** — Skill directories and `name` must use `^[a-z0-9-]+(/[a-z0-9-]+)*$`.
5. Run all post-creation sync commands when adding skills to the factory.

## Fallback Procedures
- **If pattern not found:** Report error, skip skill
- **If validation fails:** Fix schema violations before writing; do not commit invalid frontmatter
- **If customization fails:** Use default pattern values; ensure defaults pass schema validation

## Best Practices
- **Verify early**: Run structural checks immediately after file creation.
- **JSON Precision**: Always match the `id` field to the filename (without extension).
- **Trigger Clarity**: Ensure workflows have at least 2 clear trigger examples.
- **Process Depth**: Ensure every step has a clear description, not just a title.

## References

- `schemas/skill.schema.json`
- `{directories.patterns}/skills/*.json`
- `scripts/validation/schema_validator.py`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.
