---
name: writing-prd
type: skill
description: 'Produces a complete Agentic PRD from the approved prototype brief. Combines
  human-readable product context with machine-executable acceptance criteria, structured
  story format, and explicit AI-component requirements. Use when the user wants to
  write requirements, create a PRD, document what to build, or says "let''s write
  the spec", "document the requirements", or "what are we building". Requires knowledge/prototype-brief.md
  to be present and approved. Writes to knowledge/prd.md.

  '
license: MIT
allowed-tools: Read, Write
metadata:
  version: 1.0.0
  phase: requirements
  llm-preference: claude
  standard: agentic-prd
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

# Writing PRD

Produces a single authoritative document that serves two audiences simultaneously:
human product/engineering stakeholders AND downstream AI coding agents.
The spec must be parseable by both. Every section has a purpose.

## Philosophy: The Agentic PRD

A traditional PRD is prose designed for humans to interpret. An Agentic PRD adds a
machine-executable layer: structured acceptance criteria with predicates and examples
that agents can consume without interpretation drift.

Structure: **human context → machine spec → AI-specific requirements**.

## Input

Load and read:
- `knowledge/prototype-brief.md` (primary input — must be approved, DRAFT marker removed)
- `../ideation-phase/knowledge/vision.md` (north star context — if accessible)
- `knowledge/nfr.md` (if already exists from eliciting-nfr)

If prototype-brief.md is missing or still marked DRAFT, stop and tell the user.

## Output

Write to `knowledge/prd.md`. Mark as DRAFT until human approves.



## PRD Template

```markdown
# PRD — [feature/product name]
_Status: DRAFT — awaiting human approval_
_Phase: Requirements_
_Date: [date]_
_Version: 1.0.0_



## 1. Executive Summary
One paragraph. For humans who won't read further.
What is being built, for whom, and what outcome it produces.
Success criterion in one sentence.



## 2. Product Context

### Problem Statement
[Single sentence from problem-frame.md]

### Target Persona
- **Primary**: [name, role, key frustration, technical literacy]
- **Scenario**: [the specific moment when this product is used]

### Success Metrics
| Metric | Baseline | Target | Measurement method |
|--|-|--|-|
| [HEART/AARRR metric] | [now] | [goal] | [how measured] |

### Explicitly Out of Scope
- [Item] — reason: [why excluded, not just what]



## 3. Functional Requirements

### Epics

#### Epic [E-01]: [verb-noun name]
_Hypothesis: [from prototype-brief.md — copied verbatim]_

##### Story [E-01-S-01]: [verb-noun name]

**Human-readable**:
As a [persona], I want [capability] so that [value delivered].

**Machine-executable acceptance criteria**:
```json
{
  "story_id": "E-01-S-01",
  "acceptance": [
    {
      "type": "predicate",
      "id": "AC-01",
      "expr": "[logical condition in plain English — one truth condition per entry]",
      "given": "[precondition]",
      "when": "[action]",
      "then": "[outcome]"
    }
  ],
  "invariants": [
    {
      "type": "invariant",
      "id": "INV-01",
      "expr": "[condition that must always hold — e.g. response_time < 2000ms]"
    }
  ],
  "examples": [
    { "input": "[example input]", "expected": "[expected output or behaviour]" },
    { "input": "[edge case]", "expected": "[expected output or behaviour]" },
    { "input": "[failure case]", "expected": "[graceful failure behaviour]" }
  ]
}
```

**Dependencies**: [story IDs this story depends on, or NONE]
**Estimated size**: XS / S / M / L / XL
**Shippable independently**: YES / NO — if NO, explain why and propose a split



## 4. Non-Functional Requirements

_See knowledge/nfr.md for full detail. Summary below._

### Performance
| Requirement | Threshold | Measurement |
|-|--|-|
| [e.g. API response time p95] | [< 500ms] | [load test] |

### AI-Specific NFRs
| Requirement | Threshold | Fallback |
|-|--|-|
| LLM response latency p95 | [value] | [behaviour if exceeded] |
| Token budget per operation | [value] | [model downgrade or truncation strategy] |
| Hallucination tolerance | [none/low/medium] | [grounding strategy] |
| LLM availability SLO | [99.x%] | [cached response / rule-based fallback] |
| Output safety | [content policy level] | [filter + human review gate] |

### Security
- [Auth requirement]
- [Data sensitivity classification and handling rule]

### Compliance
- [Any regulatory constraints — GDPR, HIPAA, etc.]



## 5. AI Component Specifications

_For each AI component identified in prototype-brief.md_

#### Component: [name]

| Attribute | Value |
|--|-|
| Role | [what it does in one sentence] |
| Input | [format, max size, source] |
| Output | [format, structure, max length] |
| Model options | [Claude / Gemini / local — with rationale] |
| Prompt strategy | [zero-shot / few-shot / CoT / structured output] |
| Grounding | [RAG / tool-use / none] |
| Evaluation method | [how quality is measured] |
| Failure mode | [what happens when it produces bad output] |



## 6. Three-Tier Boundaries

_Explicit constraints for AI agents implementing this spec._

**Always do**:
- [Non-negotiable behaviour — e.g. "Always validate user input before LLM submission"]

**Ask first** (do not proceed autonomously):
- [Decision requiring human confirmation — e.g. "Before deleting any user data"]

**Never do**:
- [Hard prohibition — e.g. "Never expose raw LLM outputs without filtering"]



## 7. Open Questions

| ID | Question | Owner | Due |
|-|-|-|--|
| Q-01 | [unresolved decision] | [name] | [date] |



## 8. Glossary

_Define domain terms used in acceptance criteria. Agents need unambiguous vocabulary._

- **[term]**: [precise definition]


_Human approval required. Remove DRAFT and change status to READY before Architecture Phase._
```



## Writing Guidelines

- Each acceptance criterion must be **singular** — one truth condition per entry.
  Bad: "The system saves the record AND sends a confirmation email."
  Good: Two separate criteria.

- Examples must include at least one **failure/edge case** per story.
  Agents use examples as few-shot context. Missing edge cases cause silent failures.

- The Three-Tier Boundaries section is **mandatory for any story involving an AI component**.
  Agents implementing the spec use it as a behavioural contract.

- Do not pad the PRD. Every section that has no content should be omitted, not filled with
  placeholder text. Downstream agents treat all content as signal.

## References

See `references/prd-examples.md` for worked examples including AI-native feature specs.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
