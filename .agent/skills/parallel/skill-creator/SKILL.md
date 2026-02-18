---
name: skill-creator
type: skill
description: Orchestrates the creation and optimization of Anthropic-aligned skills
  within the Antigravity Agent Factory. It enforces Level 1-3 progressive disclosure,
  gerund naming conventions, and 500-line body limits.
---

# Skill Creator

## The Kitchen vs. Recipe Analogy
Understanding the division of labor between tools and instructions:
- **MCP Servers (The Kitchen)**: Access to tools, equipment, and raw data.
- **Skills (The Recipe)**: Expert instructions and standardized workflows for combining those tools to achieve complex goals.

## When to Use
Use this skill when you need to formalize a manual workflow into a reusable agent capability. It is specifically designed for:
- Creating new specialized skills from scratch.
- Optimizing existing skills for context-window efficiency.
- Converting complex research findings into deterministic agentic scripts.

## Level 1-3 Structure
Every skill must adhere to the **Progressive Disclosure** system to optimize context economics:

1.  **Level 1 (Metadata)**:
    *   **Name**: Hyphen-case gerund (e.g., `writing-clean-code`). Max 64 chars.
    *   **Description**: **Trigger-First Design**. Must clearly state the specific intent that activates this skill.
2.  **Level 2 (SKILL.md Body)**:
    *   **Length**: Max 500 lines.
    *   **Content**: Focus on procedural logic. Use the **Winning Path Extraction** method (formalizing successful manual workflows).
    *   **Output**: Mandates strict XML tags for artifact outputs.
3.  **Level 3 (Bundled Resources)**:
    *   **scripts/**: Deterministic Python/Bash/Node scripts. No "voodoo constants".
    *   **references/**: High-value context (e.g., `claude-skill-building-guide.md`).
    *   **Master Library Pattern**: **Strict prohibition** on general system metadata (catalogs, selection guides) that are not domain-specific. Dedicate an "Authority Skill" for shared data and link to it instead of copying files.

## Prerequisites
- A validated manual "Winning Path" for the task.
- Access to the `antigravity-agent-factory` repository structure.
- Familiarity with the Gerund naming convention and Level 1-3 hierarchy.

## Process
1.  **Winning Path Extraction**: Solve a complex task manually in-context first. Once successful, extract that winning approach as the template for the skill.
2.  **Analyze**: Use `deepwiki` or RAG to understand the domain.
3.  **Decompose**: Identify the core pattern (Chain, Parallel, Routing, etc.).
4.  **Initialize**: Create the 3-level structure.
5.  **Draft**: Write `SKILL.md` (Level 2) and extract deterministic logic into `scripts/` (Level 3).
6.  **Validate**: Run `scripts/quick_validate.py` to ensure naming and length compliance.

## Best Practices
- **Gerund Naming**: Always use active verbs ending in -ing.
- **Deterministic Scripts**: Move heavy logic that can be written in code into `scripts/`.
- **Progressive Disclosure**: Keep Level 1 and 2 lean; use Level 3 for depth.

## Resources
- `scripts/init_skill.py`: Initializes the 3-level folder structure.
- `scripts/quick_validate.py`: Enforces naming, line limits, and gerund conventions.
- `references/artifact-optimization-guide.md`: Detailed optimization mandates.
- `references/claude-skill-building-guide.md`: Official Claude Skill Building patterns.
