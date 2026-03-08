# Trust Tier Selection Guide

The **Trust Tier Decision Matrix** is the core mechanism of the Antigravity Agent Society Protocol (ASP) for managing safety and autonomy. It defines the constraints and permissions for agent interactions based on risk and complexity.

## 1. Trust Tier Overview

| Tier | Name | Description | Verification Method |
| :--- | :--- | :--- | :--- |
| **Tier 0** | **Identity** | Basic identity verification. | JWT / Simple Auth |
| **Tier 1** | **Capability** | Verification of agent's defined skills and permissions. | Skill Manifest Check |
| **Tier 2** | **Contractual** | Multi-agent agreement with explicit obligations. | Contract Sourcing |
| **Tier 3** | **Behavioral** | Real-time monitoring of agent outputs against norms. | Guardian Interdiction |
| **Tier 4** | **Axiomatic** | Full formal proof of safety and alignment. | Lean 4 Prover |

## 2. Selection Criteria
When designing a multi-agent system, select tiers based on:
- **Risk Profile**: High-stakes operations (e.g., financial, medical) require Tier 3 or 4.
- **Autonomy Needs**: Agents with high autonomy need robust behavioral monitoring (Tier 3).
- **Context Depth**: Complex coordination requires Tier 2 contracts.

## 3. Implementation Flow
1.  **Analyze Request**: Determine the risk and complexity of the task.
2.  **Lookup Matrix**: Consult the `trust-tier-decision-matrix.json` knowledge file.
3.  **Configure Society**: Set the required tier in the society configuration or blueprint.

---
*Antigravity Agent Factory v1.6.0*
