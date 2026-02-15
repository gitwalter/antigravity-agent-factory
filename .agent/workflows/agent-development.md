---
## Overview

description: Multi-step workflow for developing AI agents from design through deployment.
---

# Agent Development (Enriched)

This workflow defines the process for creating, refining, and deploying specialized AI agents. It ensures that every agent has a distinct mission, a robust set of axioms, and high-quality tool bindings.

**Version:** 1.1.0
**Owner:** AgentDevelopmentSpecialist (ADS)
**Skill Set:** `agent-generation`, `skill-generation`, `agent-testing`

## Trigger Conditions

This workflow is activated when:
- A new persona or specialization is identified as missing.
- An existing agent's backstory or toolkit needs refinement.
- MSO identifies a gap in operational intelligence.

**Trigger Examples:**
- "Develop an agent specializing in SAP RAP development."
- "Refine the CognitiveCycleEngineer's persona and tool bindings."
- "Spawn a sub-agent for repository auditing."

## Phases

### 1. Mission & Persona Design
Define the agent's core identity, mission, and the specific problem it solves.
- **Agent**: `PersonaDesigner` (sub-role of ADS)
- **Input**: User request / MSO gap analysis
- **Output**: Agent backstory, mission statement, and core axioms.

### 2. Capability Architecture
Design the intelligence profile and tool bindings for the agent.
- **Skill**: `agent-generation`
- **Output**: Draft of `agent-name.md` with purpose, philosophy, and skill mapping.

### 3. Tactical Tool Binding
Identify and bind the specific skills (Tactical capabilities) the agent requires.
- **Skill**: `skill-generation`, `tool-usage`
- **Process**: Map skills from the `.agent/skills` catalog to the agent's skillset.

### 4. Axiom Aligned Verification
Test the agent's behavior against its mission and system-wide axioms.
- **Skill**: `agent-testing`
- **Check**: Verify compliance with `axiom-zero-love-truth-beauty.json`.
- **Output**: Test results and behavioral audit report.

### 5. Deployment & Registration
Register the agent in the system catalog and make it available for orchestration.
- **Skill**: `system-registration`
- **Output**: Updated `agent-catalog.json`.

## Decision Points

- **Insufficient Tools**: If needed skills don't exist, pivot to the **Skill Enrichment** workflow.
- **Persona Ambiguity**: If mission overlaps too much with existing agents, consolidate instead of spawning.

## Fallback Procedures

1. **Prompt Refining**: If agent fails tests, use `prompt-optimization` to refine its core instructions.
2. **Backstory Pivot**: If persona is ineffective, redefine the mission based on successful interaction patterns.


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
