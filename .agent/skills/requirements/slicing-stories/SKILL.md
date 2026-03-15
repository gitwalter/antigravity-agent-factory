---
name: slicing-stories
type: skill
description: 'Decomposes epics from knowledge/prd.md into vertically sliced, independently
  shippable user stories with BDD acceptance criteria. Detects horizontal slices and
  technical tasks masquerading as stories, and proposes corrected splits. Use when
  the user wants to break down epics, create sprint-ready stories, check if stories
  are independently shippable, or says "let''s slice the stories", "break this down",
  or "is this story too big". Reads knowledge/prd.md. Updates story sections in-place.

  '
license: MIT
allowed-tools: Read, Write
metadata:
  version: 1.0.0
  phase: requirements
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

# Slicing Stories

Transforms epics into a story map of vertical slices — each independently deployable
and directly testable against user value.

## The Core Principle: Vertical vs. Horizontal

A vertical slice cuts through all layers of the system (UI → API → DB → AI component)
to deliver one unit of user value. It can be shipped and measured independently.

A horizontal slice (anti-pattern) implements one layer across many features
(e.g. "Build the database schema for everything"). It cannot be shipped to users.

The test: can this story be deployed to production and measured for user value WITHOUT
any other story being complete first? If no — it is horizontal. Slice it.

## Input

Load `knowledge/prd.md`. Focus on Section 3 (Functional Requirements).

## Step 1 — Slice Detection Pass

For each story in the PRD, check against these anti-patterns:

| Anti-pattern | Signal | Fix |
|--|--|--|
| **Layer slice** | "Build the X layer for..." | Split by user journey, not layer |
| **Compound story** | Contains AND in the user value | Split at the AND |
| **Infrastructure story** | No direct user value | Convert to a tech task with a story dependency |
| **AI-only story** | "Integrate the LLM" | Must be attached to a user-visible outcome |
| **Spec story** | "Design the API" | This is a task — extract to pre-work list |

For each anti-pattern found, produce:
```
⚠️ Story [ID] — Anti-pattern detected: [type]
   Current: [current story statement]
   Problem: [why this is not a vertical slice]
   Proposed split:
     Story A: [new story — user value]
     Story B: [new story — user value]
```



## Step 2 — BDD Acceptance Criteria

For each story (new or validated), produce the full BDD specification:

```gherkin
Feature: [feature name — from Epic]
  Background:
    Given [precondition that applies to all scenarios in this feature]

  Scenario: [happy path name]
    Given [specific initial context]
    When [user or system action]
    Then [observable, testable outcome]
    And [secondary outcome if needed]

  Scenario: [alternative flow]
    Given [different context]
    When [same or different action]
    Then [different outcome]

  Scenario: [failure / edge case]
    Given [context that causes failure]
    When [action]
    Then [graceful failure behaviour — never "then an error occurs"]
```

### AI Component Scenarios (required for any story with an LLM)

Add these mandatory scenarios to every story that involves an AI component:

```gherkin
  Scenario: AI component latency SLO exceeded
    Given the AI component is responding slowly
    When the operation exceeds [p99 threshold from nfr.md]
    Then the user sees [specific fallback UI/message]
    And the timeout is logged with [required trace fields]

  Scenario: AI component returns low-confidence output
    Given the AI component produces output below the quality threshold
    When the confidence score is below [threshold]
    Then [fallback behaviour — not just "show error"]

  Scenario: AI component unavailable
    Given the AI provider returns a 503 or timeout
    When the user triggers the primary action
    Then [degraded mode behaviour]
    And [alerting condition is triggered]
```



## Step 3 — Story Map

After slicing, produce a story map table written to `knowledge/story-map.md`:

```markdown
# Story Map

## [Epic E-01 name]

| Story ID | Name | Size | Shippable | AI component | Priority |
|-|||--|--|-|
| E-01-S-01 | [name] | S | YES | none | P1 |
| E-01-S-02 | [name] | M | YES | [component] | P1 |
| E-01-S-03 | [name] | L | YES | [component] | P2 |

## Suggested Delivery Order
[Ordered list — which story delivers the most learning per unit of effort]

## Pre-work (not stories — no direct user value)
- [ ] [Technical prerequisite 1] — blocks: [story ID]
- [ ] [Technical prerequisite 2]
```



## Sizing Guide

| Size | Definition | Typical AI-system effort |
||--|--|
| XS | Single endpoint, no AI | 0.5 day |
| S | Single user flow, simple AI call | 1–2 days |
| M | Multi-step flow or RAG component | 3–5 days |
| L | New agent integration or eval pipeline | 1–2 weeks |
| XL | Too large — must be split | — |

Never accept XL as a final size. If a story is XL, run Step 1 again.



## After Slicing

Offer to update `knowledge/prd.md` Section 3 with the refined story set.
Then suggest running `reviewing-requirements` as the next step.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
