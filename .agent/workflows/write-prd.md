---
agents:
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for write-prd. Standardized for IDX Visual Editor.
domain: universal
name: write-prd
steps:
- actions:
  - '**Actions**:'
  - Load `knowledge/prototype-brief.md`.
  - Trigger `.agent/skills/requirements/writing-prd/SKILL.md`.
  - Write to `knowledge/prd.md` using `knowledge/templates/prd.md`.
  agents:
  - project-operations-specialist
  goal: Transform an approved Prototype Brief into a formal, structured PRD.
  name: PRD Generation
  skills:
  - writing-prd
  tools:
  - write_to_file
- actions:
  - '**Actions**:'
  - Trigger `.agent/skills/requirements/slicing-stories/SKILL.md`.
  - Prompt user to run `/eliciting-nfr` to complete technical requirements.
  - Triggered by user context or meta-orchestrator.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Ensure user stories are vertically sliced and ready for development.
  name: Story Slicing
  skills:
  - slicing-stories
  tools:
  - replace_file_content
tags: []
type: sequential
version: 1.0.0
---

# /writing-prd Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for generating formal PRDs from prototype briefs and slicing user stories for development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Approved Prototype Brief ready for formalization.
- Requirement for breaking down a feature into verifiable user stories.
- User request: `/writing-prd`.

**Trigger Examples:**
- "Generate a PRD for the 'Multi-Agent Debate Protocol' based on the approved brief."
- "Slice user stories for the 'Agentic CI/CD Pipeline' feature."

## Phases

### 1. PRD Generation
- **Goal**: Transform an approved Prototype Brief into a formal, structured PRD.
- **Agents**: `project-operations-specialist`
- **Skills**: writing-prd
- **Tools**: write_to_file
- **Actions**:
- Load `knowledge/prototype-brief.md`.
- Trigger `.agent/skills/requirements/writing-prd/SKILL.md`.
- Write to `knowledge/prd.md` using `knowledge/templates/prd.md`.

### 2. Story Slicing
- **Goal**: Ensure user stories are vertically sliced and ready for development.
- **Agents**: `project-operations-specialist`
- **Skills**: slicing-stories
- **Tools**: replace_file_content
- **Actions**:
- Trigger `.agent/skills/requirements/slicing-stories/SKILL.md`.
- Prompt user to run `/eliciting-nfr` to complete technical requirements.
- Triggered by user context or meta-orchestrator.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
