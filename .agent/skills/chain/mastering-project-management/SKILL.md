---
description: Tactical Blueprint for Modern Project Management (Scrum/Kanban) and Reporting.
  Focuses on procedural truth for backlog health, sprint flow, and metrics.
name: mastering-project-management
type: skill
---
# Capability Manifest: Project Management Mastery

This blueprint provides the **procedural truth** for orchestrating high-fidelity software delivery within the Antigravity Agent Factory.

## When to Use

This skill should be used when completing tasks related to project management mastery.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Backlog Excellence (Refinement)
1.  **Definition of Ready (DoR)**: A story is only ready when it has:
    - Persona-based Description.
    - 3+ Clear Acceptance Criteria (AC).
    - Link to a parent Epic.
    - Estimation (Points/Hours).
2.  **MoSCoW Prioritization**: Mandatory tags for every story:
    - `Must`: Essential for the next release.
    - `Should`: Important but not critical.
    - `Could`: Nice to have.
    - `Won't`: Deferred.

### Procedure 2: Sprint Orchestration (Flow)
1.  **Capacity Gate**: Before starting a sprint, run `pm.calculateVelocity()` and verify against the proposed total points.
2.  **State Transitions**: Enforce strict flow: `To Do` -> `In Progress` -> `In Review` -> `Verification` -> `Done`.
3.  **Blocker Management**: Any item in `In Progress` for >40% of sprint length must be flagged as `AT_RISK` and requires a mitigation comment.

### Procedure 3: Reporting & Observability
1.  **Automated Changelog**: Pull all `Done` stories since the last release tag and generate grouped release notes.
2.  **Velocity Tracking**: Generate a CSV/JSON of points completed per sprint to build the "Historical Truth" for planning.
3.  **Stakeholder Sync**: Weekly automated summary of `Must/Should` progress and identified risks.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Silent Sprint Fail** | Scope creep or hidden blockers. | Run a "Sprint Audit" to compare mid-sprint state vs. initial commitment; move non-critical items back to backlog. |
| **Metric Inaccuracy** | Stale status in the PM backend. | Trigger a "Status Refresh" nudge to all active agents; run `pm.syncFromBackend()`. |
| **Story Rejection** | Vague ACs leading to incorrect implementation. | Reject the story; conduct a "Hard Refinement" session to redefine ACs with the developer agent. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Create Story | `pm.create_item()` |
| List Backlog | `pm.list_backlog()` |
| Generate Report | `pm.generate_status_report()` |
| Update Config | `pm-configuration` |

## Best Practices
Before starting a sprint:
- [ ] Every item meets the Definition of Ready.
- [ ] Total points < 105% of historical velocity.
- [ ] Dependencies map is clear (No circular blocks).
- [ ] Release target is identified and dated.
