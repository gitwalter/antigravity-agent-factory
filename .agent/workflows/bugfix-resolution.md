---
description: Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow en...
version: 1.0.0
---

# Bugfix Resolution

Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow ensures thorough root cause analysis, proper fix implementation, and comprehensive testing.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** workflow-quality-specialist

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

### Phase 0: Issue Creation & Ticket Details
**Agent**: `project-operations-specialist`
All bugs MUST have a corresponding Plane issue before work begins. Use the `managing-plane-tasks` skill.
1. Check if an issue exists.
2. If not, create an issue in Plane ensuring strict schema compliance (must be assigned to a module and a cycle).
3. Ensure the issue has a `BUG` label and is set to "In Progress" when work starts.
Use the MCP server tools (`mcp_plane_create_issue`, `mcp_plane_update_issue`) and NOT the legacy `manager.py` script.

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
**Agent**: `python-ai-specialist`
Implement the technical solution in the codebase safely.

### Verify Fix Locally

### Run Full Test Suite
**Agent**: `workflow-quality-specialist`
Execute `pytest` to ensure no regressions and verify the primary fix.

### Code Review

### Update Ticket
Update the status in Plane using the MCP server tools. Use the `mcp_plane_update_issue` tool with the correct state ID for 'Done'.

### Phase Final: High-Fidelity Closure (Memory Induction)
**Agent**: `project-operations-specialist`
Close the issue using the strict methodology defined in the `managing-plane-tasks` skill.
1. Create a detailed `solution.json` file containing `summary`, `architectural_decisions`, `files_affected`, `verification`, and `evolution`.
2. **Documentation**: Invoke the `/documentation-workflow` to generate or update the `walkthrough.md` and related technical docs.
3. Run the `post_solution.py` script (`python .agent/skills/routing/managing-plane-tasks/scripts/post_solution.py --issue <ISSUE_ID> --json <JSON_PATH> --close`) to formulate the high-fidelity comment and close the ticket in Plane. This serves as the Tier 4 Memory Proposal.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
