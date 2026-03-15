---
name: scanning-competition
type: skill
description: 'Researches the competitive landscape for the problem space defined in
  knowledge/problem-frame.md. Maps existing solutions, extracts differentiators, and
  surfaces market gaps. Use this skill when the user asks about competitors, existing
  tools, market landscape, or says "what''s already out there" or "how is this solved
  today". Requires web-search MCP tool. Writes output to knowledge/competitive.md.

  '
license: MIT
metadata:
  version: 1.0.0
  phase: ideation
  llm-preference: gemini
compatibility:
  tools:
  - web-search
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

# Scanning Competition

Produces an evidence-based competitive map grounded in real products, not assumptions.
Route to Gemini when available — better web grounding for current market data.

## Input

Load `knowledge/problem-frame.md`.
Use the primary persona and problem statement to anchor all searches.

## Research Protocol

Execute searches in this order. Do not skip steps.

### Step 1 — Direct Competitors
Search for products that directly solve the stated problem for the same persona.
Query pattern: `[problem domain] tool for [persona] [year]`
Capture: product name, core mechanism, pricing tier (free/paid/enterprise), AI features.

### Step 2 — Adjacent Solutions
Search for tools the persona likely uses as a workaround today.
Query pattern: `how do [persona] solve [problem] without [direct tool]`
Capture: manual workarounds, spreadsheet hacks, glue scripts, incumbent tools.

### Step 3 — AI-Native Entrants
Search specifically for LLM-powered or agent-based tools in this space launched after 2023.
Query pattern: `AI agent [problem domain] 2024 2025`
Capture: LLM architecture if described, agent patterns used.

### Step 4 — Gap Signal
Search for complaints and unmet needs.
Query pattern: `[competitor name] limitations OR "wish it could" OR "doesn't support"`
Capture: recurring complaints, missing features, friction points.

## Output Format

Write to `knowledge/competitive.md`:

```markdown
# Competitive Landscape — [date]

## Problem Anchor
[paste one-sentence problem statement]

## Direct Competitors

| Product | Core Mechanism | AI Features | Pricing | Key Weakness |
|||-||--|
| [name]  | [how it works] | [LLM use]  | [tier]  | [gap]        |

## How Users Solve This Today (workarounds)
- [workaround 1 — source]
- [workaround 2]

## AI-Native Entrants (post-2023)
- **[product]**: [mechanism], [agent pattern if applicable]

## Market Gaps (evidence-based)
1. [Gap] — evidence: [source or complaint pattern]
2. [Gap]

## Our Potential Differentiator
Given the above, a new entrant wins if it: [1–2 sentence hypothesis]
```

## Guidelines

- Every claim must have a source. Label unsourced claims as [unverified].
- Do not pad the competitor table — 5 well-researched competitors beat 15 shallow ones.
- The "Market Gaps" section is the most valuable output. Invest research time here.
- If a gap is already addressed by a competitor on their roadmap, note it as "closing gap".
- After writing, offer to run `clustering-opportunities` with competitive gaps as an additional input lens.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
