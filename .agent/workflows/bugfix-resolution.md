---
## Overview

description: Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow en...
---

# Bugfix Resolution

Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow ensures thorough root cause analysis, proper fix implementation, and comprehensive testing.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** debug-conductor

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

## Trigger Conditions

This workflow is activated when:

- Jira, GitHub, GitLab, or Plane issue is mentioned
- User reports a bug or defect
- Error report requires investigation
- Test failure needs resolution

**Trigger Examples:**
- "Fix bug PROJ-123"
- "Resolve issue #456"
- "Fix Plane task AGENT-12"
- "The login page is throwing an error"
- "Users are reporting data not saving"

## Steps

### Fetch Ticket Details
If a Plane issue is provided, use the native `pms-management` skill:
`conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list`

### Phase 0: Context Engineering (Memory-First)
Before deep-diving into code, query the Active Consciousness to see if this bug is a known anti-pattern or if a similar fix exists.
Use the `managing-memory-bank` skill to execute `mcp_memory_search_nodes` against the Tier 0 Graph.
**Fallback (MANDATORY)**: If the Tier 0 query returns zero structural results for the domain being modified, or if the entity data relies on deprecated packages/patterns, you MUST suspend the workflow. Trigger the "Zero-Context Fallback" directly by using `notify_user` to ask for the current standard. Build the memory before executing the fix.

### Classify Bug Severity

### Ground Data Model

### Gather Code Context

### Reproduce the Bug

### Trace Error Origin

### Identify Recent Changes

### Form Hypothesis

### Create Implementation Plan

### Write Regression Test

### Implement Fix

### Verify Fix Locally

### Run Full Test Suite

### Code Review

### Update Ticket
Update the status in Plane. Use the mapping below to ensure the correct state name:
- **Completed**: use `Done` (for completions)
- **Blocked**: use `Backlog` (if work stops)

Command:
`conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update --id <SEQ_ID> --state "Done"`

### Phase Final: Memory Induction & Proposal
If the bugfix revealed a new architectural constraint, methodology flaw, or critical anti-pattern (Layer 3 or 4), you MUST capture it.
Use `managing-plane-tasks` to draft the High-Fidelity solution payload, explicitly filling the `architectural_decisions` array. This serves as the Tier 4 Memory Proposal. Do not skip this step; it is how the factory learns to prevent future bugs.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
