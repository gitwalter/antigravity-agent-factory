# Claude Skill Building Guide: Best Practices & Patterns

This guide summarizes the core patterns for building high-performance skills for Claude, optimized for the Antigravity Agent Factory.

## 1. The 3-Level Loading Paradigm
Skills use a tiered loading approach to maximize specialized expertise while minimizing token usage:
- **Level 1 (Metadata)**: YAML frontmatter. Decides *if* a skill is relevant.
- **Level 2 (Instructions)**: `SKILL.md`. Provides the expert "Recipe" or process.
- **Level 3 (Resources)**: `scripts/` and `references/`. Handles deterministic execution and external data.

## 2. Winning Path Extraction
The most effective way to build a skill is to:
1.  **Solve manually**: First, work through a complex task in-context until Claude succeeds.
2.  **Extract logic**: Identify the specific prompts, decision points, and code that led to the success.
3.  **Formalize**: Turn that "winning approach" into a reusable `SKILL.md` (Level 2) and deterministic scripts (Level 3).

## 3. The Kitchen vs. Recipe Analogy
- **MCP Servers** are the **Professional Kitchen**: They provide the tools (functions), equipment (environment), and raw ingredients (data access).
- **Skills** are the **Recipes**: They provide the expert instructions on *how* to combine those tools and ingredients to create something valuable.

## 4. Trigger-First Design
Design the Level 1 metadata (name/description) to be high-signal:
- **Gerund Naming**: Use active verbs (e.g., `optimizing-performance`, NOT `optimizer`).
- **Clear Bounds**: State exactly when the skill should activate (and when it shouldn't).

## 5. Testing Strategy
- **Trigger Tests**: Ensure the skill loads for relevant paraphrased requests and ignores unrelated ones.
- **Adherence Tests**: Verify Claude follows constraints defined in the `SKILL.md`.
