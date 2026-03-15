---
name: briefing-prototypes
type: skill
description: 'Converts the top-ranked opportunity cluster into a concrete, buildable
  prototype brief ready to hand off to the architecture phase. Defines the smallest
  testable slice, the riskiest assumption to validate, the AI components involved,
  and the success signal. Use this skill when the user is ready to move from ideas
  to building, asks "what should we prototype", "what do we build first", or "let''s
  make this concrete". Requires knowledge/opportunities.md. Writes to knowledge/prototype-brief.md
  and requires human approval before the phase gate.

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

# Briefing Prototypes

Produces a prototype brief that is concrete enough to start building but narrow enough
to test exactly one core hypothesis. This is the phase gate artifact — human must approve.

## Input

Load:
- `knowledge/opportunities.md` — use the top-scored cluster as the primary input
- `knowledge/problem-frame.md` — anchor all scoping decisions here
- `knowledge/competitive.md` — if present, use gaps to sharpen differentiation

If `opportunities.md` is missing, invoke `clustering-opportunities` first.

## The Prototype Philosophy

A prototype for the ideation phase is not a feature. It is an **experiment**.
The goal is to invalidate the biggest assumption as cheaply as possible.
Scope to the minimum that produces a real signal. Not a demo. A test.

## Output Format

Write to `knowledge/prototype-brief.md`. Mark as DRAFT until human approves.

```markdown
# Prototype Brief — [opportunity cluster name]
_Status: DRAFT — awaiting human approval_
_Date: [date]_

## One-Line Description
[What we are building in one sentence, verb-first]

## Hypothesis Being Tested
We believe [mechanism] will [outcome] for [persona].
We will know this is true when [measurable signal].
We will know this is false when [falsification condition].

## The Riskiest Assumption
[Single assumption — if wrong, this prototype teaches us nothing useful]
Method to test it: [how the prototype surface this assumption]

## Prototype Scope (what's IN)
- [Feature / capability 1 — why it's the minimum needed to test the hypothesis]
- [Feature / capability 2]

## Explicitly OUT of Scope
- [Thing that seems related but would delay the test — and why]

## AI Components
| Component | Role | Technology Options | Key Risk |
|--||--|-|
| [e.g. LLM call] | [what it does] | [Claude / Gemini / local] | [latency / cost / quality] |
| [e.g. RAG pipeline] | [retrieval use] | [pgvector / Pinecone] | [chunking quality] |

## Stack Recommendation (lightweight)
- Frontend: [e.g. Next.js / plain HTML — justify the choice]
- Backend: [e.g. FastAPI / Vercel Functions]
- AI runtime: [e.g. Claude API via Anthropic SDK]
- Data: [e.g. SQLite for prototype — migrate later]

## Success Signal
- Qualitative: [What does a user say or do that confirms the hypothesis?]
- Quantitative: [One metric, threshold, and measurement method]

## Time Box
Target: [X days / weeks] to a testable artifact.
If not testable in this window, the scope is too large — cut further.

## What We Learn Either Way
If it works: [what this unlocks — next steps]
If it fails: [what this rules out — pivot options]


_Human approval required before handoff to Architecture Phase._
```

## Guidelines

- The hypothesis must be falsifiable. "Users will like it" is not a hypothesis.
- One AI component at a time in the prototype. Stacking LLM + RAG + agents adds confounds.
- The time box is a forcing function. If the team says "we need 3 months", the scope is wrong.
- Do not include nice-to-haves in scope. Every addition increases prototype noise.
- The "What We Learn Either Way" section is mandatory — it prevents sunk-cost thinking.

## Phase Gate

After writing the brief, remind the user:
> "This brief needs your approval before moving to the Architecture Phase.
> Please review the hypothesis, scope, and AI components. Edit directly in `knowledge/prototype-brief.md`,
> then remove the DRAFT status marker when you are satisfied."


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
