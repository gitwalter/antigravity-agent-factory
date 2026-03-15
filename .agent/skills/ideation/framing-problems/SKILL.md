---
name: framing-problems
type: skill
description: 'Structures an ambiguous idea or pain point into a crisp, bounded problem
  statement with user context, assumptions, success criteria, and out-of-scope boundaries.
  Use this skill at the very start of any ideation session, when the user describes
  a vague goal, a frustration, an opportunity, or says something like "I want to build
  X" or "users are struggling with Y". Invoke before brainstorming — framing must
  precede divergence.

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

# Framing Problems

Produces a structured problem frame that gives all subsequent ideation a solid foundation.
Run this before any brainstorm. A well-framed problem prevents wasted divergence.

## Input

The user provides one of:
- A raw idea ("I want to build a tool for X")
- A pain point ("users keep struggling with Y")
- An opportunity signal ("nobody has solved Z well")

If the input is missing key context, ask **one** clarifying question before proceeding.

## Output Format

Produce a markdown document saved to `knowledge/problem-frame.md`:

```markdown
# Problem Frame

## Problem Statement (one sentence)
[Subject] struggle to [task] when [context], which results in [consequence].

## User Context
- **Primary persona**: [name, role, key trait]
- **Secondary personas**: [list if relevant]
- **Setting**: [when/where this problem occurs]

## Root Causes (5 Whys)
1. Why does this happen? →
2. Why? →
3. Why? →
4. Why? →
5. Root cause: →

## Assumptions (explicit)
- [ ] [Assumption 1 — mark confidence: high/medium/low]
- [ ] [Assumption 2]

## Success Criteria
- Qualitative: [What does "solved" look like for the user?]
- Quantitative: [One measurable signal we could track]

## Explicitly Out of Scope
- [Thing 1 — and why it's excluded]
- [Thing 2]

## Open Questions
- [Unresolved question that affects direction]
```

## Guidelines

- Keep the problem statement to one sentence. If you need two, split into two frames.
- The 5 Whys must reach a structural or systemic root cause — not just restate the symptom.
- Assumptions must be explicit and falsifiable. Vague beliefs are not assumptions.
- Do not propose solutions in this step. Frame only.
- Flag if the stated problem is actually a solution in disguise (e.g. "I need a chatbot" → reframe to the underlying need).

## References

See `references/problem-frame-examples.md` for worked examples across three domains.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
