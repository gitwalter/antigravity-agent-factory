---
name: terraform-module-development
description: Workflow for developing and managing Cloud-Native infrastructure using
  Terraform modules.
version: 1.0.0
type: sequential
domain: operations
agents:
- dotnet-cloud-specialist
blueprints:
- infrastructure-as-code
steps:
- name: Requirements
  description: Define infrastructure requirements and architecture.
- name: Structuring
  description: Structure the Terraform module with main.tf, variables.tf, and outputs.tf.
- name: Backend Config
  description: Configure remote state storage and backend locking.
- name: Provider Config
  description: Configure provider configurations for targeted cloud (Azure, AWS, GCP).
- name: Initialization
  description: Run terraform init to initialize the working directory.
- name: Validation
  description: Execute terraform validate to ensure syntactic correctness.
- name: Security Scan
  description: Perform security scanning using tfsec or checkov.
- name: Planning
  description: Generate an execution plan (terraform plan).
- name: Testing
  description: Apply changes to a staging environment and verify.
- name: Promotion
  description: Promote to production using automated CI/CD gating.
tags:
- terraform
- module
- development
- standardized
---


# Terraform Module Development Workflow

**Version:** 1.0.0

**Goal:** Ensure robust, secure, and reusable infrastructure as code through modular Terraform development.

## Trigger Conditions
- Infrastructure requirement defined for a new project.
- Updates needed for existing cloud resources.
- Security vulnerability identified in infrastructure configuration.

**Trigger Examples:**
- "Create a Terraform module for an Azure App Service."
- "Update the AWS VPC module to include new subnets."
- "Scan the infrastructure code for security misconfigurations."
- "Plan and apply the infrastructure changes to the staging environment."

## Phases

### Phase 1: Design & Structure
- **Goal**: Define infrastructure architecture and set up module boilerplate.
- **Agents**: `dotnet-cloud-specialist`
- **Skills**: terraform-module-development
- **Tools**: write_to_file
- **Actions**:
    - Create `main.tf`, `variables.tf`, and `outputs.tf`.

### Phase 2: Initialization & Validation
- **Goal**: Verify project setup and syntactic correctness.
- **Agents**: `dotnet-cloud-specialist`
- **Skills**: terraform-module-development
- **Tools**: terraform-cli
- **Actions**:
    - Run `terraform init` and `terraform validate`.

### Phase 3: Security & Compliance
- **Goal**: Ensure infrastructure adheres to security standards.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: tfsec, checkov
- **Actions**:
    - Execute security scanning and compliance checks.

### Phase 4: Implementation & Promotion
- **Goal**: Generate execution plan and promote changes through environments.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, terraform-module-development
- **Tools**: terraform-cli
- **Actions**:
    - Run `terraform plan` and apply to staging.
    - Promote to production after verification.

## Best Practices
- **Modularity**: Design modules to be small, focused, and reusable.
- **State Management**: Use remote backends with locking for all production state.
- **Pinning**: Always pin provider and module versions to ensure reproducibility.

## Related Workflows
- `cicd-pipeline.md` - Automates the Terraform execution.
- `securing-ai-systems.md` - Periodic review of infrastructure security.


## Trigger Examples
- "Execute terraform-module-development.md"
