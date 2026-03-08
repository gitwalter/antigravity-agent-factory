---
name: mastering-project-management
description: >
  Procedural truth for orchestrating high-fidelity software delivery via Plane MCP server.
type: skill
version: 2.0.0
category: chain
---

# Capability Manifest: Project Management Mastery

This blueprint provides the **procedural truth** for orchestrating high-fidelity software delivery. The key is to use the **Plane MCP server** for all remote operations (Issue creation, label management, state updates) and standardized naming conventions to ensure the project remains high-fidelity and machine-readable.

## When to Use

This skill should be used when completing tasks related to project management mastery.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Backlog Excellence (Refinement)
1.  **Definition of Ready (DoR)**: A story is only ready when it has:
    - **Persona-based Description**: Clear "As a... I want... So that..." or structured **# Goal** header.
    - **3+ Clear Acceptance Criteria (AC)**: Explicit validation steps.
    - **Link to a parent Epic**: Or appropriate Module/Cycle categorization.
    - **Estimation (Points/Hours)**: Every task must have an estimate.
    - **Technical Context**: Implementation notes to guide the developer agent.
2.  **MoSCoW Prioritization**: Mandatory tags for every story:
    - `Must`: Essential for the next release.
    - `Should`: Important but not critical.
    - `Could`: Nice to have.
    - `Won't`: Deferred.

### Procedure 2: Sprint Orchestration (Flow)
1.  **Capacity Gate**: Before starting a sprint, manually verify the proposed total points against the team's historical velocity (visible in Plane insights).
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
| **Metric Inaccuracy** | Stale status in the PM backend. | Trigger a "Status Refresh" nudge to all active agents; manually audit item statuses in Plane to ensure alignment with reality. |
| **Story Rejection** | Vague ACs leading to incorrect implementation. | Reject the story; conduct a "Hard Refinement" session to redefine ACs with the developer agent. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Create Work Item | `mcp_plane_create_work_item` |
| List Work Items | `mcp_plane_list_work_items` |
| Retrieve Item | `mcp_plane_retrieve_work_item` |
| Update Item | `mcp_plane_update_work_item` |
| Search Items | `mcp_plane_search_work_items` |

## Label Governance (Source of Truth)


Every work item MUST be tagged with at least one label from this synchronized set. For **Remote Plane** operations, always use the `mcp_plane` tools (`create_label`, `update_label`, `list_labels`) to maintain this synchronization. Do NOT use local management scripts for remote label administration.

| Label | Description | UUID |
| :--- | :--- | :--- |
| `BUG` | Defect or unexpected behavior. | `86386dc5-0402-4294-983d-5d0a8043a5fe` |
| `CORE` | Core system infrastructure and logic. | `5b807a8c-09c4-49d5-ac0d-290568780564` |
| `DATA` | Data models, migrations, and pipelines. | `70f46984-9401-44cd-a489-8aaad7fa8f4a` |
| `DOCU` | Documentation and knowledge items. | `ffa3d5a6-91dd-4564-991f-77a7566657aa` |
| `FEATURE` | New functional capabilities. | `57a1da51-90c6-46db-9340-6c88ac9b1ed0` |
| `TEST` | Testing infrastructure and test cases. | `740d9fb4-20e8-4184-a967-8c9110d97911` |
| `UI` | User interface and experience. | `a01878b6-eb15-4ba5-a686-218206d2c0b5` |
| `ORCHESTRATION` | Agent coordination, loops, and supervisor logic. | `c1753b7b-68e8-4474-91dd-52e10842f17d` |
| `GROUNDING` | RAG patterns, knowledge retrieval, and memory management. | `d688fff1-22e0-41be-b7cc-60e4af471016` |
| `INTEGRATION` | MCP server connections and external API logic. | `78c78433-4e9e-4a44-a6ce-4017d3c51b60` |
| `INFRA` | Environment setup, Conda, and shell platform management. | `6ecab990-939b-4353-a608-7d998b1ec8b3` |
| `SKILL` | Development and refinement of agent skills. | `10becfa5-dc59-4ab1-a780-ad9852237c57` |

## Best Practices
Before starting a sprint:
- [ ] Every item meets the Definition of Ready.
- [ ] Total points < 105% of historical velocity.
- [ ] Dependencies map is clear (No circular blocks).
- [ ] Release target is identified and dated.

## Example Library (Recipes)

To ensure excellence, use these copy-pasteable patterns for common scenarios.

### 1. Creating a Standardized Feature
```json
// Tool: mcp_plane_create_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "name": "FEATURE: Implement OIDC Authentication Support",
  "priority": "high",
  "description_html": "<div>Develop and integrate OIDC auth flow...</div>",
  "labels": ["5248c180-2056-495c-859c-82747b5d1d52", "5b807a8c-09c4-49d5-ac0d-290568780564"], // FEATURE, CORE
  "scripts": ["scripts/validation/sync_manifest_versions.py"]
}
```


## Troubleshooting & Fail-State
| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **MCP Server Unavailable** | Plane MCP server connection lost. | Verify MCP server config in `mcp_config.json`; check cloud Plane instance status. |
| **UUID Resolution Failure** | Invalid label/state/cycle ID. | Re-query with `mcp_plane_list_labels` / `mcp_plane_list_states` to get current UUIDs. |
| **Duplicate Work Item** | Issue with same name already exists. | Use `mcp_plane_search_work_items` to find existing item before creating. |
| **Label Governance Violation** | Label not in the synchronized set. | Use only labels from the Label Governance table above. Verify with `mcp_plane_list_labels`. |

---
*Operational maturity is the foundation of high-velocity agency.*
