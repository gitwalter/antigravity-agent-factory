---
name: verifying-artifact-structures
description: Verifying the structural integrity of knowledge JSON and workflow markdown files.
type: skill
version: 1.0.0
category: verification
agents:
- workflow-quality-specialist
- integrity-guardian
tools:
- verify_structures.py
- run_command
---

# Verifying Artifact Structures

This skill provides the standard procedure for ensuring that all documentation artifacts (knowledge JSONs and workflow markdowns) meet the factory's structural requirements.

## When to Use
- After creating or modifying a knowledge file or workflow.
- During CI/CD quality gate checks.
- Before a major release or version bump.

## Prerequisites
- **Python Environment**: Conda environment `D:\Anaconda\envs\cursor-factory` must be active.
- **Validation Script**: `scripts/validation/verify_structures.py` must exist.
- **Project Structure**: Artifacts must be located in `.agent/knowledge` or `.agent/workflows`.

## Process
To maintain artifact integrity, follow this systematic verification sequence to identify and fix structural drift.

### 1. Run Automated Verification
Execute the verification script to identify structural deficiencies:
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/verify_structures.py
```

### 2. Remediate Failures
For each failure:
- **Knowledge JSON**: Ensure `id`, `name`, `version`, `category`, `description` are present. Add `patterns`, `best_practices`, and `anti_patterns`.
- **Workflow MD**: Ensure an H1 title, `## Overview`, `## Trigger Conditions`, and `Version:` declarations are present.

### 3. Synchronize Manifests
After structural fixes, update the system counts:
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/sync_knowledge_counts.py --sync
conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/sync_artifacts.py --sync
```

## Best Practices
- **Verify early**: Run structural checks immediately after file creation.
- **JSON Precision**: Always match the `id` field to the filename (without extension).
- **Trigger Clarity**: Ensure workflows have at least 2 clear trigger examples.
