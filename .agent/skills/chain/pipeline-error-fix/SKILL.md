---
description: Systematic detection and fixing of CI/CD pipeline failures.
name: pipeline-error-fix
type: skill
---

# Pipeline Error Fix

## Overview
This skill provides a systematic approach to identifying and resolving failures in automated pipelines (GitHub Actions, Jenkins, etc.).

## When to Use
- When a CI/CD build or test run fails.
- When deployment pipelines encounter environment-specific errors.
- When structural regressions are detected during a build process.

## Prerequisites
- Access to the pipeline logs.
- `conda` environment `cursor-factory` active.
- Understanding of the `debug-pipeline` workflow.
- Basic knowledge of the target pipeline's configuration (e.g., `.github/workflows/`).

## Process
1. **Analyze Logs**: Use `grep` or specialist agents to identify the first failing step.
2. **Decompose Strategy**: Determine if the failure is code-related (tests), configuration-related (paths), or infrastructure-related (timeouts).
3. **Execute Workflow**: Trigger the `/debug-pipeline` workflow or follow the manual steps in `.agent/workflows/debug-pipeline.md`.
4. **Apply Fix**: Implement the targeted fix.
5. **Verify**: Re-run the local verification suite (e.g., `pytest`) before pushing.

## Best Practices
- **Isolation**: Fix one failure at a time to avoid complex regressions.
- **Verification**: Always run `pytest` locally before letting the CI handle it.
- **Root Cause**: Don't just patch the symptom; use the "5 Whys" to find the root cause.
- **Documentation**: Document the fix and any learned patterns in a Knowledge Item or the `references/` directory.
