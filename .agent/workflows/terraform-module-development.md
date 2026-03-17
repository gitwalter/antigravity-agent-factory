---
agents:
- workflow-quality-specialist
- dotnet-cloud-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for terraform-module-development. Standardized for
  IDX Visual Editor.
domain: universal
name: terraform-module-development
steps:
- actions:
  - '**Agents**: `dotnet-cloud-specialist`'
  - '**Actions**:'
  - Create `main.tf`, `variables.tf`, and `outputs.tf`.
  agents:
  - dotnet-cloud-specialist
  goal: Define infrastructure architecture and set up module boilerplate.
  name: Design & Structure
  skills:
  - terraform-module-development
  tools:
  - write_to_file
- actions:
  - '**Agents**: `dotnet-cloud-specialist`'
  - '**Actions**:'
  - Run `terraform init` and `terraform validate`.
  agents:
  - dotnet-cloud-specialist
  goal: Verify project setup and syntactic correctness.
  name: Initialization & Validation
  skills:
  - terraform-module-development
  tools:
  - terraform-cli
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Execute security scanning and compliance checks.
  agents:
  - workflow-quality-specialist
  goal: Ensure infrastructure adheres to security standards.
  name: Security & Compliance
  skills:
  - securing-ai-systems
  tools:
  - tfsec
  - checkov
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Run `terraform plan` and apply to staging.
  - Promote to production after verification.
  - '**Modularity**: Design modules to be small, focused, and reusable.'
  - '**State Management**: Use remote backends with locking for all production state.'
  - '**Pinning**: Always pin provider and module versions to ensure reproducibility.'
  - '`cicd-pipeline.md` - Automates the Terraform execution.'
  - '`securing-ai-systems.md` - Periodic review of infrastructure security.'
  - '"Execute terraform-module-development.md"'
  agents:
  - project-operations-specialist
  goal: Generate execution plan and promote changes through environments.
  name: Implementation & Promotion
  skills:
  - committing-releases
  - terraform-module-development
  tools:
  - terraform-cli
tags: []
type: sequential
version: 2.0.0
---
# Terraform Module Development

**Version:** 1.0.0

## Overview
Antigravity workflow for designing, building, and deploying reusable Terraform modules for infrastructure-as-code. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for new cloud infrastructure or cloud resource management.
- Need to create or update reusable infrastructure components (modules).
- User request: `/terraform-module-development`.

**Trigger Examples:**
- "Develop a Terraform module for a 'High-Availability PostgreSQL Cluster' on Azure."
- "Update the existing 'VPC Peering' module with new security compliance checks."

## Phases

### 1. Design & Structure
- **Goal**: Define infrastructure architecture and set up module boilerplate.
- **Agents**: `dotnet-cloud-specialist`
- **Skills**: terraform-module-development
- **Tools**: write_to_file
- **Agents**: `dotnet-cloud-specialist`
- **Actions**:
- Create `main.tf`, `variables.tf`, and `outputs.tf`.

### 2. Initialization & Validation
- **Goal**: Verify project setup and syntactic correctness.
- **Agents**: `dotnet-cloud-specialist`
- **Skills**: terraform-module-development
- **Tools**: terraform-cli
- **Agents**: `dotnet-cloud-specialist`
- **Actions**:
- Run `terraform init` and `terraform validate`.

### 3. Security & Compliance
- **Goal**: Ensure infrastructure adheres to security standards.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: tfsec, checkov
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Execute security scanning and compliance checks.

### 4. Implementation & Promotion
- **Goal**: Generate execution plan and promote changes through environments.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, terraform-module-development
- **Tools**: terraform-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Run `terraform plan` and apply to staging.
- Promote to production after verification.
- **Modularity**: Design modules to be small, focused, and reusable.
- **State Management**: Use remote backends with locking for all production state.
- **Pinning**: Always pin provider and module versions to ensure reproducibility.
- `cicd-pipeline.md` - Automates the Terraform execution.
- `securing-ai-systems.md` - Periodic review of infrastructure security.
- "Execute terraform-module-development.md"
