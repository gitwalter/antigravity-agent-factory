---
description: Proof-of-Concept for the Unified Orchestration Engine demonstrating end-to-end integration.
---

# /poc-orchestration — System Integration POC

This workflow demonstrates the **Unified Organizational Model** (AGENT-15). It validates the hard-linking between roles, tools, and rules.

**Version:** 1.0.0
**Owner:** SystemArchitectSteward (SYARCH)

## Trigger Conditions

- Project initialization or structural verification request.
- Explicit command: "/run poc-orchestration".
- Verification phase of AGENT-15.

**Trigger Examples:**
- `User: /run poc-orchestration - Validate the new RAG ingestion path.`
- `User: Please run the system integration POC to verify PAIS tool access.`
- `MSO: Detected structural change in agents. Triggering /poc-orchestration for validation.`

## Phases

### 1. Strategic Decomposition
Define the mission and identify required specialists.
- **Lead Agent**: `SYARCH`
- **Rule**: `agent-definition.md`
- **Action**: Read `agent-staffing.json` to authorize tool access.
- **Exit Criteria**: `requirements.json` generated and specialists assigned.

### 2. Contextual Harvesting
Gather domain context using the cascaded routing strategy.
- **Lead Agent**: `KNOPS`
- **Logic**: Consult `orchestration-engine.json` for RAG vs. Graph priority.
- **Tool**: `@mcp_antigravity-rag_search_library` or `@mcp_memory_read_graph`.
- **Exit Criteria**: Context injected into the agent's scratchpad.

### 3. Operational Implementation
Execute technical tasks within the authorized toolset.
- **Lead Agent**: `PAIS` (for Python) / `FSWS` (for Web)
- **Constraint**: Must only use tools listed in `authorized_mcp_servers` for the role.
- **Gate**: Check `technical-standards.md` before commit.
- **Exit Criteria**: Implementation artifacts (code/docs) created.

### 4. Integrity Verification & Promotion
Validate results and 'promote' findings to long-term memory.
- **Lead Agent**: `WQSS`
- **Constraint**: Must verify `required_output_artifact` presence as per `workflow-catalog.json`.
- **Promotion**: Follow `memory_promotion_protocols` in `orchestration-engine.json`.
- **Exit Criteria**: Walkthrough finalized and session promoted.

## Success Metrics

1. **Rule Compliance**: 0 Axiom violations during execution.
2. **Registry Alignment**: Lead Agents always match the Phase definitions.
3. **Traceability**: All output artifacts correctly linked in the walkthrough.

## Example Session

User: /run poc-orchestration
Agent: Routing to SYARCH for Strategic Decomposition...
Agent [SYARCH]: Authorized tools (filesystem, git, sequentialthinking) verified. Starting decomposition...
