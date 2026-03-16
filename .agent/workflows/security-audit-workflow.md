---
agents:
- blockchain-guru-specialist
- workflow-quality-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for security-audit-workflow. Standardized for IDX
  Visual Editor.
domain: universal
name: security-audit-workflow
steps:
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Define scope and discover environmental dependencies.
  agents:
  - workflow-quality-specialist
  goal: Define audit scope and prepare the detection environment.
  name: Scope & Discovery
  skills:
  - securing-ai-systems
  - securing-ai-systems
  tools:
  - mcp_memory_search_nodes
  - slither-cli
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run scanners and triage findings into high/medium/low severity.
  agents:
  - workflow-quality-specialist
  goal: Execute automated scanners and triage identified findings based on severity.
  name: Vulnerability Hunting & Triage
  skills:
  - securing-ai-systems
  tools:
  - slither-cli
  - mythril-cli
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Manually verify ACLs and logical flows for "rug-pull" or "re-entrancy" vectors.
  agents:
  - blockchain-guru-specialist
  - workflow-quality-specialist
  goal: Deep dive into manual review of access controls and business logic.
  name: Manual Logic & Access Control Review
  skills:
  - securing-ai-systems
  - securing-ai-systems
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Compile audit report and verify remediation findings before release.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - knowledge-operations-specialist
  goal: Generate high-fidelity audit reports and verify remediation.
  name: Reporting & Verification
  skills:
  - generating-documentation
  - committing-releases
  tools:
  - pdf-generator
  - safety-gate
tags: []
type: sequential
version: 1.0.0
---

# Security Audit Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for comprehensive security auditing of smart contracts and AI systems. Standardized for IDX Visual Editor.

## Trigger Conditions
- Pre-deployment security review requirement.
- Scheduled security audit for existing critical infrastructure.
- User request: `/security-audit`.

**Trigger Examples:**
- "Conduct a full security audit of the 'Token Vesting' smart contract."
- "Execute the security audit workflow for our new 'Context Engineering' RAG pipeline."

## Phases

### 1. Scope & Discovery
- **Goal**: Define audit scope and prepare the detection environment.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: mcp_memory_search_nodes, slither-cli
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Define scope and discover environmental dependencies.

### 2. Vulnerability Hunting & Triage
- **Goal**: Execute automated scanners and triage identified findings based on severity.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: slither-cli, mythril-cli
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run scanners and triage findings into high/medium/low severity.

### 3. Manual Logic & Access Control Review
- **Goal**: Deep dive into manual review of access controls and business logic.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Actions**:
- Manually verify ACLs and logical flows for "rug-pull" or "re-entrancy" vectors.

### 4. Reporting & Verification
- **Goal**: Generate high-fidelity audit reports and verify remediation.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, committing-releases
- **Tools**: pdf-generator, safety-gate
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Compile audit report and verify remediation findings before release.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
