---
description: End-to-end workflow for developing Fiori Elements applications in SAP
  S/4HANA. Covers CDS data modeling, service defi...
version: 1.0.0
tags:
- fiori
- app
- development
- standardized
---


# Fiori App Development

End-to-end workflow for developing Fiori Elements applications in SAP S/4HANA. Covers CDS data modeling, service definition, UI annotations, app generation, testing-agents, and deployment.

**Version:** 1.0.0
**Created:** 2026-02-09
**Applies To:** sap-systems-specialist, fiori-development

## Trigger Conditions

This workflow is activated when:

- New Fiori Elements app required
- List Report or Object Page app needed
- Fiori app for existing RAP BO
- UI customization for business users

**Trigger Examples:**
- "Create a Fiori Elements app for travel bookings"
- "Build List Report for purchase orders"
- "Develop Object Page for sales orders"
- "Generate Fiori app from CDS view"

## Phases

### Phase 1: Service Preparation & Exposure
- **Goal**: Verify backend CDS views and expose them via Service Definition and Binding.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-rap-objects
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Verify Interface (I_) and Consumption (C_) views.
    - Create Service Definition and Binding.

### Phase 2: UI Annotation Configuration
- **Goal**: Define the UI layout (List Report, Object Page) using CDS annotations or Metadata Extensions.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-fiori-apps
- **Tools**: write_to_file
- **Actions**:
    - Configure List Report and Object Page annotations.
    - Configure Value Helps and custom actions.

### Phase 3: Project Generation & Configuration
- **Goal**: Use Fiori Tools to generate the project and configure manifest/page map.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-fiori-apps
- **Tools**: fiori-tools-cli
- **Actions**:
    - Create Fiori Elements project.
    - Configure app manifest and page map.

### Phase 4: Testing & Deployment
- **Goal**: Register the app in Fiori Launchpad and deploy to the target system.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: committing-releases, verifying-artifact-structures
- **Tools**: safe_release.py
- **Actions**:
    - Perform local testing-agents.
    - Register app in Launchpad and transport/deploy.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
