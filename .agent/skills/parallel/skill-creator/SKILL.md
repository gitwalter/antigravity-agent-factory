---
name: skill-creator
type: skill
description: Orchestrates the creation and optimization of Anthropic-aligned skills
  within the Antigravity Agent Factory. It enforces Level 1-3 progressive disclosure,
  gerund naming conventions, and 500-line body limits.
---

# Skill Creator

## Overview
This skill provides a standardized framework for developing, validating, and packaging skills for the Antigravity Agent Factory. It ensures that every skill is optimized for context economics and deterministic execution.

## When to Use
- When creating a new AI agent skill from scratch.
- When refactoring existing scripts into a specialized agentic bundle.
- When enriching a structural shell with Level 3 resources (References, Scripts).

## Prerequisites
- Access to the Antigravity Agent Factory ecosystem.
- `conda` environment `cursor-factory` active.
- Fundamental understanding of the 3-tier knowledge architecture.

## Level 1-3 Structure
Every skill must adhere to the 3-level hierarchical loading system:

1.  **Level 1 (Metadata)**:
    *   **Name**: Hyphen-case gerund (e.g., `writing-clean-code`). Max 64 chars.
    *   **Description**: 3rd person objective. Must clearly state the trigger context.
2.  **Level 2 (SKILL.md Body)**:
    *   **Length**: Max 500 lines.
    *   **Content**: Focus on procedural logic and decision trees. Strip generic definitions.
    *   **Output**: Mandates strict XML tags for artifact outputs.
3.  **Level 3 (Bundled Resources)**:
    *   **scripts/**: Deterministic Python/Bash/Node scripts. No "voodoo constants".
    *   **references/**: Contextual docs (TOC required if >100 lines).

## Process
1.  **Analyze**: Use `deepwiki` to understand the domain or repository.
2.  **Decompose**: Identify the core agentic pattern (Chain, Parallel, Routing, Evaluator-Optimizer, Orchestrator-Workers).
3.  **Initialize**: Run `scripts/init_skill.py` to create the bundle structure.
4.  **Draft**: Write `SKILL.md` body (Level 2) and extract logic into `scripts/` (Level 3).
5.  **Validate**: Run `scripts/quick_validate.py` to ensure compliance with length and naming rules.
6.  **Package**: Run `scripts/package_skill.py` to finalize the bundle.

## Best Practices
- **Gerund Naming**: Always use active verbs ending in -ing for skill names.
- **Deterministic Scripts**: Move all logic that can be written in Python into the `scripts/` directory.
- **Axiom Alignment**: Ensure all processes align with the core Factory axioms.

## Resources
- `scripts/init_skill.py`: Initializes the 3-level folder structure.
- `scripts/quick_validate.py`: Enforces naming, line limits, and gerund conventions.
- `references/artifact-optimization-guide.md`: Detailed optimization mandates.
