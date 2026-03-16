---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for fiori-app-development. Standardized for IDX
  Visual Editor.
domain: universal
name: fiori-app-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Verify Interface (I_) and Consumption (C_) views.
  - Create Service Definition and Binding.
  agents:
  - python-ai-specialist
  goal: Verify backend CDS views and expose them via Service Definition and Binding.
  name: Service Preparation & Exposure
  skills:
  - developing-rap-objects
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Configure List Report and Object Page annotations.
  - Configure Value Helps and custom actions.
  agents:
  - python-ai-specialist
  goal: Define the UI layout (List Report, Object Page) using CDS annotations or Metadata
    Extensions.
  name: UI Annotation Configuration
  skills:
  - developing-fiori-apps
  tools:
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Create Fiori Elements project.
  - Configure app manifest and page map.
  agents:
  - project-operations-specialist
  goal: Use Fiori Tools to generate the project and configure manifest/page map.
  name: Project Generation & Configuration
  skills:
  - developing-fiori-apps
  tools:
  - fiori-tools-cli
- actions:
  - '**Agents**: `project-operations-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Perform local testing-agents.
  - Register app in Launchpad and transport/deploy.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  - workflow-quality-specialist
  goal: Register the app in Fiori Launchpad and deploy to the target system.
  name: Testing & Deployment
  skills:
  - committing-releases
  - verifying-artifact-structures
  tools:
  - safe_release.py
tags: []
type: sequential
version: 1.0.0
---

# Fiori App Development

**Version:** 1.0.0

## Overview
Antigravity workflow for SAP Fiori App development using Fiori Elements. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for a new SAP Fiori application based on backend CDS views.
- Need to configure List Report or Object Page layouts using annotations.
- User request: `/fiori-app-development`.

**Trigger Examples:**
- "Develop a Fiori List Report for monitoring warehouse tasks."
- "Configure the Object Page for the 'Equipment Maintenance' application."

## Phases

### 1. Service Preparation & Exposure
- **Goal**: Verify backend CDS views and expose them via Service Definition and Binding.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Verify Interface (I_) and Consumption (C_) views.
- Create Service Definition and Binding.

### 2. UI Annotation Configuration
- **Goal**: Define the UI layout (List Report, Object Page) using CDS annotations or Metadata Extensions.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-fiori-apps
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Configure List Report and Object Page annotations.
- Configure Value Helps and custom actions.

### 3. Project Generation & Configuration
- **Goal**: Use Fiori Tools to generate the project and configure manifest/page map.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-fiori-apps
- **Tools**: fiori-tools-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Create Fiori Elements project.
- Configure app manifest and page map.

### 4. Testing & Deployment
- **Goal**: Register the app in Fiori Launchpad and deploy to the target system.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: committing-releases, verifying-artifact-structures
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Actions**:
- Perform local testing-agents.
- Register app in Launchpad and transport/deploy.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
