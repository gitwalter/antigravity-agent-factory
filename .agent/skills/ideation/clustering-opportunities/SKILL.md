---
name: clustering-opportunities
type: skill
description: 'Synthesises all raw idea dumps in knowledge/ideas/raw/ into labelled
  opportunity clusters with themes, strength signals, and a prioritisation matrix.
  Use this skill after one or more brainstorming sessions, when the user wants to
  make sense of accumulated ideas, find patterns, or asks "what themes are emerging"
  or "which ideas are worth pursuing". Writes output to knowledge/opportunities.md.

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

# Clustering Opportunities

Transforms a messy idea dump into a structured opportunity map.
This is the first convergent step — evaluate and group, but do not yet discard.

## Input

Load all files matching `knowledge/ideas/raw/*.md`.
Load `knowledge/problem-frame.md` as the evaluation anchor.

## Step 1 — Affinity Grouping

Read all raw ideas. Group by underlying theme or mechanism — not by feature surface.
Aim for 3–7 clusters. Fewer means you are being too abstract; more means you haven't clustered.

Name each cluster with a verb phrase describing the core value it delivers to the user
(e.g. "Automating repetitive context switches" not "AI features").

## Step 2 — Cluster Profiles

For each cluster, produce:

```markdown
## Cluster: [verb-phrase name]

**Core hypothesis**: We believe [solution mechanism] will [user outcome] because [evidence or analogy].

**Ideas in this cluster**:
- [idea ref from raw dump]
- [idea ref]

**Why this clusters**: [1-2 sentences on the shared mechanism]

**Signal strength**:
- Recurrence: [how many independent ideas pointed here — high/med/low]
- Analogy depth: [does this solve well in other domains? — yes/partial/no]
- AI leverage: [is an AI component natural here? — strong/weak/none]

**Biggest unknown**: [the one assumption that, if wrong, kills this cluster]
```

## Step 3 — Prioritisation Matrix

Produce a markdown table:

| Cluster | User Impact | Confidence | AI Leverage | Effort Estimate | Score |
||||-|--|-|
| [name]  | H/M/L      | H/M/L      | H/M/L       | H/M/L (inv.)    | [sum] |

Score = Impact + Confidence + AI Leverage + (inverted Effort). Max 12.
Flag the top 1–2 clusters as **Recommended Bets**.

## Output

Write to `knowledge/opportunities.md`. Do not overwrite — append a dated section if the file exists.

## Guidelines

- Group by mechanism, not by feature name. Two ideas may look different but solve the same way.
- The "biggest unknown" per cluster is the most important output. It drives what to prototype.
- A cluster with one wild idea and four conventional ideas is still valid — the wild idea may be the insight.
- If only one cluster emerges with a strong score, say so clearly. Don't manufacture false balance.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
