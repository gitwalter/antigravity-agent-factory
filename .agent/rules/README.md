# Agent Rules

This directory contains rule definitions for the Antigravity Agent System. 

## Format
Rules are defined in JSON or YAML format, following the `rule.schema.json` specification.

### Example
```json
{
  "$pabp": "1.0.0",
  "$type": "rule",
  "name": "always-use-kebab-case",
  "description": "Enforce kebab-case for all file names",
  "scope": "project",
  "content": "All files must be named using kebab-case.",
  "format": "markdown",
  "applies_to": ["**/*"]
}
```

## Loading
The system automatically loads all valid rule files from this directory and aggregates them.
