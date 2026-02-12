---
description: JSON knowledge file generation skill
name: knowledge-generation
type: skill
---

# Knowledge Generation

JSON knowledge file generation skill

## 
# Knowledge Generation Skill

Generates structured JSON knowledge files for target projects.

## 
# Knowledge Generation Skill

Generates structured JSON knowledge files for target projects.

## Process
### Step 1: Determine Required Files
Based on stack, identify needed knowledge files:

| Stack | Required Files |
|-------|----------------|
| All | `naming-conventions.json` |
| All | `reference-sources.json` |
| Web | `api-patterns.json` |
| SAP | `cdhdr-object-classes.json`, `tadir-object-types.json` |

### Step 2: Generate File Structure
Each knowledge file follows this structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "{File Title}",
  "description": "{File Description}",
  "version": "1.0.0",
  "data": {
    // Queryable data
  }
}
```

### Step 3: Populate Data
Based on stack capabilities:
- Copy naming conventions from stack definition
- Add style guide rules
- Include domain-specific patterns

### Step 4: Write Files
Write to target location:
- Path: `{TARGET}/knowledge/{filename}.json`
- Encoding: UTF-8
- Validate JSON structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "{File Title}",
  "description": "{File Description}",
  "version": "1.0.0",
  "data": {
    // Queryable data
  }
}
```

## Output
Knowledge files in `knowledge/` directory:

| File | Content |
|------|---------|
| `naming-conventions.json` | Naming rules for the stack |
| `reference-sources.json` | External reference URLs |
| `best-practices.json` | Development best practices |

## Query Patterns
Design files for easy querying:

```javascript
// Access naming convention
conventions.variables // "snake_case"

// Access by key
tables['{TABLE_NAME}']

// Iterate patterns
patterns.forEach(p => ...)
```

```javascript
// Access naming convention
conventions.variables // "snake_case"

// Access by key
tables['{TABLE_NAME}']

// Iterate patterns
patterns.forEach(p => ...)
```

## Fallback Procedures
- **If stack not recognized**: Create minimal generic files
- **If data unavailable**: Leave section empty with placeholder

## Best Practices
- Always include `$schema` field for JSON validation
- Use descriptive titles and descriptions in each file
- Organize data for easy querying with consistent key naming
- Version knowledge files to track changes over time
- Validate JSON structure before committing
- Include examples in complex knowledge files
- Keep individual files focused on single domains

## References
- `knowledge/stack-capabilities.json`
- `knowledge/best-practices.json`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: stack-capabilities.json, best-practices.json
