---
agents:
- workflow-quality-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for rap-with-draft. Standardized for IDX Visual
  Editor.
domain: universal
name: rap-with-draft
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Create database and draft tables.
  - Create CDS Interface and Projection views.
  agents:
  - python-ai-specialist
  goal: Define the persistent and draft tables and the initial CDS views.
  name: Data Model & Draft Configuration
  skills:
  - developing-rap-objects
  - developing-rap-objects
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Create Behavior Definition with `with draft`.
  - Configure Draft Indicator and Draft Actions.
  agents:
  - python-ai-specialist
  goal: Configure the Behavior Definition to support draft handling and ETag.
  name: Behavior Definition with Draft
  skills:
  - developing-rap-objects
  tools:
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement Submit and other custom actions.
  - Configure instance authorization and DCL rules.
  agents:
  - python-ai-specialist
  goal: Implement logic for draft activation, custom actions, and instance-based authorization.
  name: Implementation of Actions & Authorization
  skills:
  - developing-rap-objects
  - securing-ai-systems
  tools:
  - replace_file_content
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test draft creation, activation, and resume.
  - Verify ETag handling and action logic.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  goal: Rigorously test draft lifecycle (Create, Activate, Resume, ETag).
  name: Verification & Testing
  skills:
  - testing-agents
  tools:
  - run_tests.py
tags: []
type: sequential
version: 1.0.0
---

# RESTful ABAP Programming (RAP) with Draft Handling

**Version:** 1.0.0

## Overview
Antigravity workflow for developing SAP RAP objects with draft handling capabilities. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for building transactional SAP applications with draft support (save-and-resume).
- Need to implement complex business logic with intermediate states.
- User request: `/rap-with-draft`.

**Trigger Examples:**
- "Implement a RAP business object for 'Travel Requests' with draft enabled."
- "Add draft support to the existing 'Employee Onboarding' RAP service."

## Phases

### 1. Data Model & Draft Configuration
- **Goal**: Define the persistent and draft tables and the initial CDS views.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects, developing-rap-objects
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Create database and draft tables.
- Create CDS Interface and Projection views.

### 2. Behavior Definition with Draft
- **Goal**: Configure the Behavior Definition to support draft handling and ETag.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Create Behavior Definition with `with draft`.
- Configure Draft Indicator and Draft Actions.

### 3. Implementation of Actions & Authorization
- **Goal**: Implement logic for draft activation, custom actions, and instance-based authorization.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects, securing-ai-systems
- **Tools**: replace_file_content
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement Submit and other custom actions.
- Configure instance authorization and DCL rules.

### 4. Verification & Testing
- **Goal**: Rigorously test draft lifecycle (Create, Activate, Resume, ETag).
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test draft creation, activation, and resume.
- Verify ETag handling and action logic.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
