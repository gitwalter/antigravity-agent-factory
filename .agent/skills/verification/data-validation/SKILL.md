---
name: data-validation
version: 1.0.0
type: skill
description: Skills for validating data integrity, schema compliance, and lineage in data pipelines.
category: verification
agents:
- data-architect-specialist
knowledge:
- data-patterns.json
tools:
- name: validate_schema
  type: factory
  description: Validates a dataset against a defined schema.
---

# Data Validation Skill

## When to Use
Use this skill when you need to verify the integrity, type compliance, and business logic of data at any stage of the SDLC, particularly within ETL/ELT pipelines.

## Prerequisites
- Defined schema (JSON Schema, SQL DDL, or Pydantic models).
- Access to the target data source or artifacts.
- Validated `data-patterns.json` Knowledge Item.

## Process
1. **Identify Schema**: Select the target schema or definition to validate against.
2. **Execute Validation**: Use the `validate_schema` tool to run the check.
3. **Report Failures**: Generate a summary of violations and their impact.
4. **Remediate**: Fix the data or update the schema if it's outdated.

## Best Practices
- **Early Validation**: Run validation as close to the source as possible.
- **Automate**: Integrate validation checks into CI/CD pipelines.
- **Version Schemas**: Always use versioned schemas to avoid regression.
