---
agents:
- project-operations-specialist
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for brief-prototype. Standardized for IDX Visual
  Editor.
domain: universal
name: brief-prototype
steps:
- actions:
  - '**Actions**:'
  - Load `knowledge/opportunities.md`.
  - Trigger `.agent/skills/ideation/briefing-prototypes/SKILL.md`.
  - Write to `knowledge/prototype-brief.md` using `knowledge/templates/prototype-brief.md`.
  - Triggered by user context or meta-orchestrator.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Research potential opportunities and formalize the one with the highest ROI.
  name: Prototype Brief Extraction
  skills:
  - brainstorming-ideas
  - researching-first
  tools:
  - search_web
  - deepwiki
- actions: []
  agents:
  - '@Architect'
  goal: Verify the results of the workflow.
  name: Verification
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Prototype Briefing

**Version:** 1.0.0

## Overview
Antigravity workflow for prototype brief extraction. Standardized for IDX Visual Editor.

## Trigger Conditions
- New opportunity identified in `knowledge/opportunities.md`.
- Strategic decision to prototype a new system component.
- User request: `/brief-prototype`.

**Trigger Examples:**
- "Brief a prototype for the new API layer."
- "Extract a brief from the latest opportunity."

## Phases

### 1. Prototype Brief Extraction
- **Goal**: Research potential opportunities and formalize the one with the highest ROI.
- **Agents**: `project-operations-specialist`
- **Skills**: brainstorming-ideas, researching-first
- **Tools**: search_web, deepwiki
- **Actions**:
- Load `knowledge/opportunities.md`.
- Trigger `.agent/skills/ideation/briefing-prototypes/SKILL.md`.
- Write to `knowledge/prototype-brief.md` using `knowledge/templates/prototype-brief.md`.
- Triggered by user context or meta-orchestrator.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

### 2. Verification
- **Goal**: Verify the results of the workflow.
- **Agents**: `@Architect`
