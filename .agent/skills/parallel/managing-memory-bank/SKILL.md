---
agents:
- python-ai-specialist
category: parallel
description: 'Foundational skill for navigating the Tier 0 Active Consciousness and
  proposing Tier 4 Memories.

  '
knowledge:
- agent-memory-patterns.json
name: managing-memory-bank
related_skills:
- managing-plane-tasks
templates:
- none
tools:
- none
type: skill
version: 2.0.0
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---
# Memory Bank (Active Consciousness Governance)

Govern the factory's "Tier 0 Active Consciousness" (FalkorDB via `memory` MCP) and manage the "Tier 4 Consent Queue".

## Architectural Role
This skill enforces the exact specifications of the **Memory System Integration Architecture (AGENT-50)** and the **Consent-Driven Learning System**:
1. **Tier 0 Navigation**: The memory graph is ephemeral but incredibly fast. It is used to build rapid situational awareness (topography) before any search or execution begins.
2. **Tier 4 Proposal**: The factory is mathematically forbidden from altering core system axioms without User Consent. You do not write directly to Tier 1 Permanent Memory; you generate a *Proposal* (Tier 4) for the user to review.

## When to Use
- When initially orienting yourself to a new codebase, epic, or problem space (Phase 0).
- When you reach the final phases of a task and need to propose architectural, methodological, or technical changes based on your learnings (Phase Final).
- Use this skill as the mandatory "bookends" (start and end) of any formal development task according to the AGENT-50 Factory rules.

## Prerequisites
- The `memory` MCP server must be active and configured via your tools.

## Process

The process of managing the memory bank requires careful mapping of the existing topography before extracting learning or creating proposals.

### Phase 0: Context Engineering & Active Memory Building (MANDATORY)
**Before** deep-diving into codebases or initiating web searches, you MUST establish structural topography.

### Step 1: Broad Mapping
Identify the overarching concept within the Active Consciousness.
```python
# Use MCP tool: search_nodes
search_nodes(query="<core task concept>")
```

### Step 2: Zero-Context Fallback (IMPORTANT)
If `search_nodes` returns NO relevant results for a core domain concept, or if the nodes look clearly outdated, you MUST NOT hallucinate context.
- **Action**: Pause your execution. Use `notify_user` to ask the human operator exactly how this concept should be structured according to current factory standards.
- **Action**: If you discover outdated nodes (e.g., legacy patterns the user tells you are no longer used), you must flag them for deletion (`mcp_memory_delete_entities`) and build the correct ones.
- **Goal**: *Always build the memory right now.* Never proceed into a task without establishing verified truth coordinates.

### Step 3: Relational Traversing
Follow the active verbs ("implements", "solves", "extends") to map the surrounding architecture.
```python
# Use MCP tool: open_nodes
open_nodes(names=["<discovered entity 1>", "<discovered entity 2>"])
```
*Goal: Understand the ecosystem you are entering so you do not duplicate work or violate existing Layer 3 (Methodology) / Layer 4 (Technical) standards.*



### Phase Final: Memory Induction & Consent Loop
At the end of a session, if you detect a "Significant Pattern" (a new architectural decision, a recurring bug fix, a new coding standard), you MUST propose it.

### Step 1: Rejection Similarity Check
Before proposing, verify the pattern was not previously rejected.
*Note: In the future, this will be an automated vector check. For now, rely on your Tier 3 Episodic session context to ensure you aren't repeating a declined idea.*

### Step 2: Layer Verification
Ensure the pattern only affects **Layer 3 (Methodology)** or **Layer 4 (Technical)**.
You may NOT propose modifications to:
- Layer 0: Axioms
- Layer 1: Purpose
- Layer 2: Principles

### Step 3: Propose via Tasks
The standard mechanism for submitting a Tier 4 Proposal is via task closure.
Use the `managing-plane-tasks` skill to draft a High-Fidelity solution. Enter your proposed rule or pattern into the `architectural_decisions` array.

```json
"architectural_decisions": [
  "New Pattern Proposed: Enforce Pydantic Output Parsers over raw dictionaries for all async endpoints to prevent silent type coercion failures (Confidence: 0.9, Explicit Rule)."
]
```

### Step 4: Hydration (Post-Approval)
If a proposal is Approved by the user, it becomes Tier 1 Permanent Memory (`.agent/knowledge/*.json`).
**CRITICAL**: You MUST run the mandatory filesystem synchronization suite (`sync_artifacts.py`, etc.) BEFORE hydrating the Active Consciousness to ensure the memory coordinates match the physical repository state.
```python
# Use MCP tools: create_entities, create_relations
create_entities(entities=[{"name": "AsyncPydanticRule", "entityType": "Layer4Pattern", "observations": ["Always use structured parsers for outputs"]}])
create_relations(relations=[{"from": "FastAPIDevelopment", "to": "AsyncPydanticRule", "relationType": "enforces"}])
```

## Best Practices
- Always query the Memory MCP first to build situational awareness (topography) before any search or execution begins.
- Never hallucinate context boundaries if an entity is missing in the memory bank.
- Prioritize Tier 3 Episodic Context to avoid repetitive patterns in your solutions.
