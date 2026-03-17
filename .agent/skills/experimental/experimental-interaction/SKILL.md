---
name: experimental-interaction
description: Skill for coordinating experimental interactions including agent-to-agent handoffs and voice-to-PRD workflows.
type: skill
category: experimental
axiomAlignment:
  A1_verifiability: Patterns are documented for verifiable execution.
  A3_transparency: Handoff protocols use explicit metadata.
---

# Experimental Interaction Skill

## Overview
This skill provides the logic for specialized interaction patterns within the Antigravity Agent Factory. It handles high-fidelity context exchange between agents and experimental input modalities (e.g., voice).

## When to Use
Use this skill when exploring new interaction modalities or when coordinating complex multi-agent handoffs that require the Universal Context Protocol (UCO).

## Prerequisites
- Conda environment `cursor-factory` active.
- Access to `.agent/knowledge/agent-handoff-protocol.json`.

## Process
1. Initialize the experimental context.
2. Formulate the UCO handoff object.
3. Execute the transition logic.

## Tools
- `scripts/experimental/voice_to_prd.py`: Process simulated voice transcripts into PRDs.
- `.agent/knowledge/agent-handoff-protocol.json`: Schema for UCO exchange.

## Best Practices
- Always validate the UCO schema before handoff.
- Use explicit metadata for all experimental transitions.

## Related Knowledge
- `agent-handoff-protocol.json`
- `zero-knowledge-patterns.json`
- `agent-handoff-patterns.json`
