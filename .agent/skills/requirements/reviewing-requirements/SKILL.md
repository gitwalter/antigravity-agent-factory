---
name: reviewing-requirements
type: skill
description: 'Conducts a multi-perspective adversarial review of knowledge/prd.md
  using a structured debate pattern. Activates three reviewer personas — Product Critic,
  AI Systems Engineer, and Security Auditor — to surface gaps, contradictions, missing
  edge cases, and AI-specific failure modes. Use when the user wants to validate requirements,
  check the PRD, find gaps, stress-test the spec, or says "review the requirements",
  "what are we missing", "is this complete", or "let''s pressure-test this". Requires
  knowledge/prd.md. Writes findings to knowledge/review-findings.md.

  '
license: MIT
allowed-tools: Read, Write
metadata:
  version: 1.0.0
  phase: requirements
  llm-preference: claude
  pattern: multi-agent-debate
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

# Reviewing Requirements

Applies a structured Multi-Agent Debate (MAD) pattern to the PRD.
Research shows MAD improves requirements quality F1-scores from 0.726 to 0.841 versus
single-pass review by surfacing contradictions that a single perspective misses.

Three reviewer personas each read the full PRD independently, produce findings, then
their findings are synthesised by a Judge into a prioritised issue list.

## Input

Load `knowledge/prd.md` (required).
Load `knowledge/nfr.md` if present.
Load `knowledge/dependencies.md` if present.

## The Three Reviewer Personas

Activate each persona in sequence. Think from their perspective completely before
moving to the next. Do not blend perspectives.



### Persona 1 — Product Critic

**Role**: Senior PM who has shipped three AI features to production and seen all the ways
requirements drift, features get misunderstood, and success metrics go unmeasured.

**Review focus**:
- Is every requirement traceable to a user need? Flag any requirement that exists for
  technical reasons but has no user value statement.
- Are success metrics measurable with existing instrumentation, or do they require
  new tracking to be built?
- Is there anything in scope that a competitor already does better with less effort?
  (flag as "reconsider" not "cut")
- Are there missing user scenarios — edge users, failure states, first-time users?
- Does the PRD tell an agent what NOT to do as clearly as what TO do?

**Output format**:
```
## Product Critic Findings

### Missing User Scenarios
- [ID] [description] — risk: [consequence if missed]

### Untraceable Requirements
- [requirement ref] — no user need found — suggest: [remove / reframe]

### Metric Gaps
- [metric] — cannot be measured because: [reason] — suggest: [instrument X or change metric]

### Scope Questions
- [question about whether something is truly necessary]
```



### Persona 2 — AI Systems Engineer

**Role**: Senior engineer who has built four production LLM systems, all of which had
prompt failures, hallucination incidents, and token-budget surprises in production.

**Review focus**:
- Are all AI component failure modes specified with concrete fallback behaviours?
  "Return an error" is not a fallback behaviour.
- Are prompt injection risks identified for any story where user input reaches the LLM?
- Is the token budget feasible? Calculate: max input context × expected calls per day ×
  token cost. Flag if this exceeds the budget ceiling in nfr.md.
- Are streaming vs. blocking requirements specified for every LLM call?
- Is there an eval strategy? No eval strategy = no way to detect degradation in production.
- Are there any stories where the AI component is a single point of failure with no
  fallback, AND the operation is user-visible and blocking?
- Are output schemas specified for structured output calls, or is the agent expected
  to parse free text?

**Output format**:
```
## AI Systems Engineer Findings

### Underspecified Failure Modes
- Story [ID] — [component] — current spec says: "[what it says]" — missing: [fallback]

### Prompt Injection Risks
- Story [ID] — user input "[field]" enters prompt at [injection point] — mitigation: [strategy]

### Token Budget Analysis
| Component | Estimated tokens/call | Calls/day (at target DAU) | Daily cost | Within budget? |
|--|-|--||-|
| [name] | [n] | [n] | [$] | YES/NO |

### Missing Eval Strategy
- [component or flow] — no eval defined — suggest: [RAGAS metric / golden dataset / human review]

### Output Schema Gaps
- Story [ID] — [component] returns free text but [downstream consumer] needs structure — add: [schema]
```



### Persona 3 — Security Auditor

**Role**: Security engineer who has found data leaks in LLM systems and understands
that AI surfaces new attack vectors traditional security reviews miss.

**Review focus**:
- Does any PII flow through the LLM? Is this disclosed in the PRD and compliant with
  the stated compliance scope?
- Are there prompt injection vectors? (User-controlled text entering a prompt)
- Are there insecure output handling risks? (LLM output rendered directly as HTML/SQL/code)
- Are API keys and model credentials handled securely in the spec?
- Is there a data retention policy for prompt logs and LLM traces?
- Does the Three-Tier Boundaries section (PRD Section 6) exist and cover AI components?
- Are there any "Never do" items that are currently implied but not explicitly stated?

**Output format**:
```
## Security Auditor Findings

### PII / Data Classification Issues
- Story [ID] — [data type] flows to [destination] — classification: [level] — compliant: YES/NO

### Prompt Injection Vectors
- Story [ID] — attack vector: [description] — severity: H/M/L — mitigation: [strategy]

### Insecure Output Handling
- Story [ID] — output goes to: [renderer/consumer] — risk: [injection/execution] — fix: [sanitization]

### Missing Boundaries
- [boundary that should be in Section 6 but isn't]

### Retention Policy Gap
- Prompt logs retained for: [duration / not specified] — required by compliance: [yes/no]
```



## Judge Synthesis

After all three personas have produced their findings, synthesise into a prioritised
master issue list:

```markdown
# Requirements Review — Findings
_Date: [date]_
_PRD version reviewed: [version]_

## 🔴 Critical — Must resolve before Architecture Phase

| ID | Finding | Source | Action required |
|-||--|-|
| R-01 | [issue] | [persona] | [specific fix] |

## 🟡 Important — Should resolve before Build Phase

| ID | Finding | Source | Action required |
|-||--|-|
| R-02 | [issue] | [persona] | [specific fix] |

## 🔵 Minor — Address in iteration

| ID | Finding | Source | Action required |
|-||--|-|
| R-03 | [issue] | [persona] | [specific fix] |

## ✅ Strengths (what the PRD does well)
- [strength 1]
- [strength 2]

## Phase Gate Recommendation
[ ] READY — no critical issues found
[ ] BLOCKED — [N] critical issues must be resolved first
```

## After Review

Present the summary to the user.
For any BLOCKED finding, offer to open `knowledge/prd.md` and fix the issue directly.
Do not mark the PRD as READY — this requires explicit human confirmation.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
