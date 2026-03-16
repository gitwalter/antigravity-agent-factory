---
description: Comprehensive workflow for performing structured code reviews covering
  correctness, style, design, performance, secur...
version: 1.0.0
tags:
- code
- review
- standardized
---


# Code Review

Comprehensive workflow for performing structured code reviews covering correctness, style, design, performance, security, and maintainability. Generates actionable feedback with severity ratings and clear recommendations.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** system-steward

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

## Trigger Conditions

This workflow is activated when:

- Pull request is created or updated
- User requests code review
- Pre-merge review is required
- Code audit is needed

**Trigger Examples:**
- "Review this pull request"
- "Check my code for issues"
- "Do a code review on the changes"
- "PR #123 needs review"

## Steps

## Phases

### 1. Context Acquisition
- **Goal**: Understand the scope and intent of the changes.
- **Action**: Fetch the diff and linked Plane issue (e.g., [AGENT-133](https://app.plane.so/agent-factory/browse/AGENT-133/)).
- **Tool**: `git diff` via `run_command` and `mcp_plane_retrieve_work_item`.

### 2. Static Analysis & Compliance
- **Goal**: Ensure code adheres to factory standards.
- **Action**: Run linters and type checkers.
- **Tool**: `ruff`, `mypy`, or `eslint` via `run_command`.
- **Reference**: Verify against `.agentrules` Layer 3 and 4.

### 3. Logic & Security Audit
- **Goal**: Identify bugs, vulnerabilities, and architectural mismatches.
- **Action**: Perform manual/AI-assisted review of logic, error handling, and security patterns.
- **Tool**: Use `python-ai-specialist` for deep code analysis.

### 4. Verification & Feedback
- **Goal**: Validate that the code works as intended.
- **Action**: Run the unit/integration tests included with the PR.
- **Tool**: `pytest` or `npm test` via `run_command`.

### 5. Review Reporting
- **Goal**: Communicate findings clearly.
- **Action**: Generate a summary report with severity ratings.
- **Tool**: Invoke `/generating-documentation` to format the review comment.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
