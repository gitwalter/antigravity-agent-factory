---
name: brainstorming-ideas
type: skill
description: 'Runs a high-volume divergent ideation session anchored to a problem
  frame. Generates a minimum of 20 raw feature or solution ideas without filtering,
  evaluation, or judgment. Use this skill whenever the user wants to generate ideas,
  explore possibilities, think broadly, or says "what could we build", "give me ideas",
  or "let''s brainstorm". Must be run after framing-problems. Appends raw output to
  knowledge/ideas/raw/.

  '
license: MIT
metadata:
  version: 1.0.0
  phase: ideation
  llm-preference: claude
agents:
- python-ai-specialist
knowledge:
- none
templates:
- none
related_skills:
- managing-plane-tasks
- orchestrating-mcp
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Brainstorming Ideas

Generates a high-volume, unfiltered idea dump. Volume and diversity beat quality at this stage.
Do not evaluate, filter, rank, or discard any idea during this skill. That is a later step.

## Input

Requires `knowledge/problem-frame.md` to be present. Load it before starting.
If it is missing, invoke `framing-problems` first and tell the user.

## Divergence Modes

Apply all four lenses to maximise variety. Do not skip a lens to save time.

### Lens 1 — Conventional
Ideas that follow existing patterns in the domain. What would a typical product team build?
Generate 5 ideas minimum.

### Lens 2 — Analogical
Borrow solutions from adjacent domains. How does aviation solve this? Healthcare? Gaming? Finance?
Generate 5 ideas minimum. Label each with its source domain.

### Lens 3 — Extreme / Wild
Remove all constraints. Ignore feasibility, cost, technical limits. What if compute were free?
What if the user had infinite patience? What if an AI handled every step autonomously?
Generate 5 ideas minimum. Mark each with 🌀.

### Lens 4 — AI-Native
Ideas that are only possible with modern LLMs, agents, RAG, or multimodal AI.
What could not have existed before 2023? What breaks if you remove the AI component?
Generate 5 ideas minimum. Mark each with 🤖.

## Output Format

Append to `knowledge/ideas/raw/YYYY-MM-DD-session.md`:

```markdown
# Idea Dump — [date] — [session title]

## Source: problem-frame.md snapshot
[paste the one-sentence problem statement]

## Conventional Ideas
1. [idea]
2. [idea]
...

## Analogical Ideas
6. [idea] _(from: [source domain])_
...

## Wild Ideas 🌀
11. [idea]
...

## AI-Native Ideas 🤖
16. [idea]
...

## Sparks (things that came up that don't fit above)
- [anything worth capturing even if half-formed]
```

## Critical Rules

- **Minimum 20 ideas** before stopping. More is better.
- **No filtering** during this step. Terrible ideas stay in. They often spark good ones.
- **No elaboration** per idea — one sentence maximum. Depth comes in the clustering step.
- **Never say "this isn't feasible"** during this skill. Feasibility is evaluated later.
- If the user starts evaluating ideas mid-session, acknowledge and redirect: "Let's capture that judgment for the clustering step — for now, can we keep generating?"

## After the Session

Offer to immediately run `clustering-opportunities` on the output.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
