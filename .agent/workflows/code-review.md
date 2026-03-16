---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for code-review. Standardized for IDX Visual Editor.
domain: universal
name: code-review
steps:
- actions:
  - '**Tool**: `git diff` via `run_command` and `mcp_plane_retrieve_work_item`.'
  - Fetch the diff and linked Plane issue (e.g., [AGENT-133](https://app.plane.so/agent-factory/browse/AGENT-133/)).
  agents:
  - '@Architect'
  goal: Understand the scope and intent of the changes.
  name: Context Acquisition
  skills: []
  tools: []
- actions:
  - '**Tool**: `ruff`, `mypy`, or `eslint` via `run_command`.'
  - '**Reference**: Verify against `.agentrules` Layer 3 and 4.'
  - Run linters and type checkers.
  agents:
  - '@Architect'
  goal: Ensure code adheres to factory standards.
  name: Static Analysis & Compliance
  skills: []
  tools: []
- actions:
  - '**Tool**: Use `python-ai-specialist` for deep code analysis.'
  - Perform manual/AI-assisted review of logic, error handling, and security patterns.
  agents:
  - '@Architect'
  goal: Identify bugs, vulnerabilities, and architectural mismatches.
  name: Logic & Security Audit
  skills: []
  tools: []
- actions:
  - '**Tool**: `pytest` or `npm test` via `run_command`.'
  - Run the unit/integration tests included with the PR.
  agents:
  - '@Architect'
  goal: Validate that the code works as intended.
  name: Verification & Feedback
  skills: []
  tools: []
- actions:
  - '**Tool**: Invoke `/generating-documentation` to format the review comment.'
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  - Generate a summary report with severity ratings.
  agents:
  - '@Architect'
  goal: Communicate findings clearly.
  name: Review Reporting
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Code Review

**Version:** 1.0.0

## Overview
Antigravity workflow for code-review. Standardized for IDX Visual Editor.

## Trigger Conditions
- Pull Request created and ready for review.
- Manual triggers for code quality audits.
- User request: `/code-review`.

**Trigger Examples:**
- "Review the changes in PR #42."
- "Audit the code quality of the recent commit."

## Phases

### 1. Context Acquisition
- **Goal**: Understand the scope and intent of the changes.
- **Agents**: `@Architect`
- **Tool**: `git diff` via `run_command` and `mcp_plane_retrieve_work_item`.
- Fetch the diff and linked Plane issue (e.g., [AGENT-133](https://app.plane.so/agent-factory/browse/AGENT-133/)).

### 2. Static Analysis & Compliance
- **Goal**: Ensure code adheres to factory standards.
- **Agents**: `@Architect`
- **Tool**: `ruff`, `mypy`, or `eslint` via `run_command`.
- **Reference**: Verify against `.agentrules` Layer 3 and 4.
- Run linters and type checkers.

### 3. Logic & Security Audit
- **Goal**: Identify bugs, vulnerabilities, and architectural mismatches.
- **Agents**: `@Architect`
- **Tool**: Use `python-ai-specialist` for deep code analysis.
- Perform manual/AI-assisted review of logic, error handling, and security patterns.

### 4. Verification & Feedback
- **Goal**: Validate that the code works as intended.
- **Agents**: `@Architect`
- **Tool**: `pytest` or `npm test` via `run_command`.
- Run the unit/integration tests included with the PR.

### 5. Review Reporting
- **Goal**: Communicate findings clearly.
- **Agents**: `@Architect`
- **Tool**: Invoke `/generating-documentation` to format the review comment.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
- Generate a summary report with severity ratings.
