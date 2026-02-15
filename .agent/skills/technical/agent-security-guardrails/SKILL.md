---
description: Tactical Blueprint for AI Security and Guardrails. Focuses on prompt
  injection defense, PII detection, and content safety for agentic systems.
name: agent-security-guardrails
type: skill
---
# Capability Manifest: Agent Security Guardrails

This blueprint provides the **procedural truth** for securing AI agents against adversarial threats and ensuring output alignment.

## When to Use

This skill should be used when completing tasks related to agent security guardrails.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Prompt Injection Defense (Input Gating)
1.  **Pattern Audit**: Use regex and string matching (see `llm-guardrails` skill) to detect common jailbreak patterns (e.g., "ignore previous instructions").
2.  **LLM Classifier (The Guard Node)**: Before processing a user query in a complex system, route it through a low-temperature classifier node dedicated solely to identifying malicious intent.
3.  **Instruction Wrapping**: Use clear delimiters (e.g., `### USER INPUT ###`) and system-level instructions to explicitly isolate user data from system commands.

### Procedure 2: PII Redaction & Content Safety
1.  **Presidio Integration**: Automatically scan all user inputs for PII (Names, Emails, Keys) before they reach the model. Redact by default in logs and non-essential processing steps.
2.  **Self-Correction Loop**: If a model generates sensitive information or violates safety policies, the `reflexion` node must detect this in the output audit phase and trigger a "safe-fail" response.

### Procedure 3: Topic & Scope Control
1.  **Semantic Boundary Testing**: Use embedding distances to verify if a user's request falls within the agent's defined domain (e.g., SAP Configuration vs. General Chat).
2.  **Explicit Refusal**: Prepare specific, axiom-aligned refusal templates for off-topic or high-risk requests. Never "apologize" excessively; state the boundary clearly.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Injection Detected** | Adversarial user input. | Terminate the current cognitive cycle immediately; log the attempt; respond with a "Security Boundary Enforcement" message. |
| **PII Leakage** | Model hallucinated or retrieved sensitive data. | Truncate the response; scrub the conversation memory; notify the system orchestrator for audit. |
| **Alignment Drift** | Model is responding outside of its axioms. | Trigger the "Axiom Reset": Re-inject the specialist's core missions and axioms into the immediate context. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Scan for PII | `presidio-analyzer` / Custom Pydantic validator |
| Detect Injection | `NeMo-Guardrails` / Safety Classifier Node |
| Content Moderation | `LlamaGuard` / Gemini Safety Settings |
| Trace Audit | `LangSmith` Safety Evaluation |

## Best Practices
Before finalizing any agentic loop, verify:
- [ ] Every user input node is preceded by a safety check.
- [ ] No plaintext PII is stored in the `State` persistence.
- [ ] Explicit "Refusal Logic" exists for off-topic requests.
- [ ] Output nodes include a "Final Alignment" check.
