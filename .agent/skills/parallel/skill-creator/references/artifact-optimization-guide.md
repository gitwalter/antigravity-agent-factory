# Artifact Optimization Guide

This guide details the technical mandates for scaling agent capabilities within the Antigravity Agent Factory.

## The 3-Level Loading Paradigm

### Level 1: Metadata (Always In Context)
- **Purpose**: Semantic routing and discovery.
- **Trigger-First Design**: The metadata is the "Trigger" that pulls the skill into context. It must be high-signal and precisely bound to the user's intent.
- **Constraints**:
    - **Name**: Must be a **hyphen-case gerund** (e.g., `fetching-github-issues`).
    - **Description**: Written in 3rd person. Clearly state the trigger context. Max 1024 characters.
- **Optimization**: Keeps the system prompt lean while supporting hundreds of skills.

## The Kitchen vs. Recipe Analogy

- **MCP Servers (The Kitchen)**: Tools, environment, and data access.
- **Skills (The Recipe)**: Expert instructions on how to use those tools to perform complex, repeatable tasks.

### Level 2: SKILL.md Body (Loaded on Trigger)
- **Purpose**: Procedural logic and expert guidance.
- **Constraints**:
    - **Length**: Strictly under **500 lines**.
    - **Abstraction**: Assume core model intelligence. Do not explain generic concepts.
    - **Structure**: Use XML tags for output specifications.

### Level 3: Bundled Resources (Loaded as Needed)
- **Scripts**: Store in `scripts/`. These define **deterministic execution paths**.
- **Isolation**: The source code of Level 3 scripts **never** enters the LLM context. Only the output is returned.
- **References**: Store in `references/`. Use for long documentation or datasets.
- **Master Library Pattern**: Never include general system catalogs (MCP catalogs, registry indexes) in a skill. Level 3 resources must be **exclusive** to the skill's specific domain. Centralize shared metadata in "Authority Skills" (e.g., `selecting-mcp`).

## Avoiding "Voodoo Constants"
- Never use undefined timeouts or retry counts in instructions.
- All external calls must have explicit, hard-coded thresholds in the Level 3 scripts.

## Token Economics Formula
`TotalContext = SystemPrompt + History + Σ(Metadata_i) + Σ(Triggered_SKILL_j) + ScriptOutput`

By maximizing the use of Level 3 scripts, we achieve near-infinite computational capacity with zero upfront token cost.
