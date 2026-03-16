---
description: Comprehensive guide to the Antigravity Automated SDLC.
version: 1.0.0
---

# Antigravity SDLC Usage Guide

**Version:** 1.0.0

## Overview
This guide describes the 7 phases of the Automated Software Development Life Cycle (SDLC) used in the Antigravity Agent Factory. Every phase is enforced by a specific workflow and requires a formal "Phase Gate" artifact before proceeding.

## Trigger Conditions
- Completion of a technical task or feature request.
- Start of a new project or module.
- Periodic repository audit.

**Trigger Examples:**
- /sdlc-meta-orchestrator
- "Follow the SDLC for this new feature."
- "Execute the factory building workflow."

## Phases

### Phase 1: Ideation (`/briefing-prototypes`)
- **Goal**: Research potential opportunities and formalize the one with the highest ROI.
- **Agents**: `project-operations-specialist`
- **Skills**: brainstorming-ideas, researching-first
- **Tools**: search_web, deepwiki
- **Actions**:
    - Identify a high-value opportunity.
    - Create a [Prototype Brief](file:///knowledge/prototype-brief.md).

### Phase 2: Requirements (`/writing-prd`)
- **Goal**: Breakdown the Brief into functional requirements and user stories.
- **Agents**: `project-operations-specialist`
- **Skills**: generating-documentation
- **Tools**: write_to_file
- **Actions**:
    - Create the [PRD](file:///knowledge/prd.md).
    - Run `/eliciting-nfr` for technical constraints.

### Phase 3: Architecture (`/ai-designing-ai-systems`)
- **Goal**: Design the system architecture based on the PRD.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems
- **Tools**: view_file, write_to_file
- **Actions**:
    - Create the [AI Design Document](file:///knowledge/ai-design.md) with C4 diagrams.

### Phase 4: Build (`/developing-ai-agents`)
- **Goal**: Axiomatic implementation of the feature.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, analyzing-code
- **Tools**: run_command, replace_file_content
- **Actions**:
    - Implement the feature using builder agents and TDD.
    - Generate [Walkthrough](file:///knowledge/walkthrough.md).

### Phase 5: Test & Eval (`/agent-testing-agents`)
- **Goal**: Verify correctness and quality.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: pytest
- **Actions**:
    - Run unit, integration, and LLM evaluations.
    - Produce [Evaluation Report](file:///knowledge/eval-report.md).

### Phase 6: Deploy (`/committing-releases`)
- **Goal**: Version control and formal release.
- **Agents**: `project-operations-specialist`
- **Skills**: governing-repositories
- **Tools**: git, committing-releases
- **Actions**:
    - Merge, tag, and update `CHANGELOG.md`.

### Phase 7: Monitor (`/logging-and-monitoring`)
- **Goal**: Close the feedback loop.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: log_analysis
- **Actions**:
    - Gather production metrics.
    - Generate [Monitor Report](file:///knowledge/monitor-report.md).

---

## Detailed SDLC Phase Mapping

| Phase | Goal | Primary Workflow | Gate Artifact |
| :--- | :--- | :--- | :--- |
| **Phase 1: Ideation** | Transform opportunities into formal, approvable briefs. | `/briefing-prototypes` | `knowledge/prototype-brief.md` |
| **Phase 2: Requirements** | Transform briefs into structured PRDs with functional requirements. | `/writing-prd` | `knowledge/prd.md` |
| **Phase 3: Architecture** | Design robust, scalable, and cost-effective system architectures. | `/ai-designing-ai-systems` | `knowledge/ai-design.md` |
| **Phase 4: Build** | Safe, axiomatic implementation with automated walkthroughs. | `/developing-ai-agents` | `knowledge/walkthrough.md` |
| **Phase 5: Test & Eval** | Verification against requirements via rigorous testing-agents and evaluation. | `/agent-testing-agents` | `knowledge/eval-report.md` |
| **Phase 6: Deploy** | Coordinate deployment, versioning, and formal release notes. | `/committing-releases` | `knowledge/release-notes.md` |
| **Phase 7: Monitor** | Track production health and feed insights back to Ideation. | `/logging-and-monitoring` | `knowledge/monitor-report.md` |

---

## How to use the Documentation Workflow
If at any point you need to synchronize documentation or generate missing artifacts, use:
`@[/generating-documentation]`

This workflow will:
1. Discover the current SDLC state.
2. Draft missing artifacts.
3. Validate links using `link_checker.py`.
4. Sync documentation to the PMS (Plane) and global stores.

---
**Standard**: "No Code without a Gate. No Release without a Note."
