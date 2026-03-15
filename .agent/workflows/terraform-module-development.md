---
name: terraform-module-development
description: Workflow for developing and managing Cloud-Native infrastructure using Terraform modules.
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

### 1. Design & Structure
Define architecture and setup module boilerplate.
- **Agent**: `dotnet-cloud-specialist`
- **Action**: Create `main.tf`, `variables.tf`, and `outputs.tf`.

### 2. Initialization & Validation
Verify basic correctness and project setup.
- **Action**: Run `terraform init` and `terraform validate`.

### 3. Security & Compliance
Ensure infrastructure adheres to security standards.
- **Action**: Execute `tfsec` or `checkov` scans.

### 4. Implementation & Promotion
Apply changes through a staged pipeline.
- **Action**: Run `terraform plan` and apply to staging before production.

## Best Practices
- **Modularity**: Design modules to be small, focused, and reusable.
- **State Management**: Use remote backends with locking for all production state.
- **Pinning**: Always pin provider and module versions to ensure reproducibility.

## Related Workflows
- `cicd-pipeline.md` - Automates the Terraform execution.
- `security-audit.md` - Periodic review of infrastructure security.
