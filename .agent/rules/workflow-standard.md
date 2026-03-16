# Rule: Workflow Standardization

## Context
Governs the structure, syntax, and quality of workflows in the Antigravity Agent Factory.

## Unified Syntax Requirement
All workflows MUST be defined as Markdown files with YAML frontmatter.

### 1. Frontmatter
Required fields:
- `description`: A clear, concise summary of the workflow.
- `tags`: Array of keywords for categorization.
- `version`: Semantic version (e.g., `2.0.0`).
- `author`: (Optional) The creator or specialist persona.

### 2. Structure
- `# [Title]`: H1 header matching the filename.
- `## Trigger Conditions`: Bullet points of when to use this workflow.
- `## Phases`: numbered sections (`### Phase N: Name`).
  - **Goal**: One sentence describing the outcome.
  - **Action(s)**: Specific tool calls or agent instructions.
- `## Best Practices`: Guidelines for successful execution.
- `## Related`: Links to other workflows or knowledge.

## Quality Standards ("Excellent Quality")
- **Axiomatic Alignment**: Every workflow must support Layer 0-4 (Truth, Beauty, Love).
- **Verifiability**: Steps must be concrete and testable.
- **Visualizable**: Must translate cleanly to the UI graph (React Flow).
- **No Hallucinations**: Paths and tool names must be 100% accurate.

## Synchronization Protocol
- Local workflows (`.agent/workflows/`) are the source of truth for execution.
- Global workflows (`~/.gemini/antigravity/global_workflows/`) are synced to maintain cross-project consistency.
