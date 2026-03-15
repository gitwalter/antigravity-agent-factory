---
name: eliciting-nfr
type: skill
description: 'Conducts a structured Socratic elicitation session to surface all non-functional
  requirements, with deep focus on AI-specific NFRs that standard templates miss.
  Use when the user wants to define performance requirements, talk through constraints,
  discuss what the system must not do, or says "what are the NFRs", "let''s think
  about performance", "how fast does it need to be", or "what are the constraints".
  Reads knowledge/prototype-brief.md. Writes to knowledge/nfr.md.

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

# Eliciting NFR

Non-Functional Requirements are the leading cause of production AI failures.
Most are never written down. This skill surfaces them through structured dialogue.

## Philosophy

NFRs are not a checklist to fill in. They are discovered through probing questions
that force concrete answers. A vague NFR ("the system should be responsive") is
worthless to an agent building the system. Every NFR must have a threshold and a
measurement method.

AI systems require a second NFR layer that traditional templates never include.
This skill treats AI NFRs as a first-class category, not an afterthought.

## Input

Load `knowledge/prototype-brief.md`.
If `knowledge/prd.md` exists (partial draft), load it for context.

## Session Protocol

Work through each domain in order. For each, ask the probing question, wait for the
answer, then press for a specific number. Do not accept qualitative answers.

If the user says "it depends" — ask "on what?" and get at least two concrete scenarios.
If the user says "as fast as possible" — ask "what is the slowest acceptable?" and
convert to a numeric threshold.



### Domain 1 — Latency

**Probe**: "When a user takes the primary action, how long can they wait before they
lose confidence in the system?"

Press for:
- p50 (median acceptable wait)
- p95 (worst-case acceptable wait)
- p99 (absolute maximum before showing an error)
- Distinguish: first byte / streaming start vs. complete response

**AI-specific probe**: "When the AI component is involved in this action, does the
user see a loading state? Can the response be streamed, or must it be atomic?"



### Domain 2 — Token Budget and Cost

**Probe**: "What is your monthly cost ceiling for AI inference on this feature?"

Press for:
- Max tokens per single operation (input + output)
- Max cost per operation (in USD or equivalent)
- Daily/monthly budget ceiling
- Cost per user at target DAU — is this sustainable?

**AI-specific probe**: "If the LLM call for this operation costs $0.05, and you have
10,000 daily active users each triggering it once — that's $500/day. Is that acceptable?
If not, what is the ceiling, and what model or strategy would you use when it's exceeded?"



### Domain 3 — Reliability and Fallback

**Probe**: "If the AI component becomes unavailable or returns a bad response, what
should the user experience?"

Elicit for each:
- LLM provider outage (hard fail) — expected frequency, max acceptable downtime
- LLM latency spike (soft fail) — timeout threshold, retry strategy
- LLM bad output / hallucination detected — filter and retry? Show raw? Block?
- Degraded mode: is a rule-based fallback acceptable?

**AI-specific probe**: "What is the minimum acceptable quality of a fallback response?
For example, if the AI can't summarise a document, is it acceptable to return the first
paragraph? Or must the feature be completely unavailable?"



### Domain 4 — Output Quality and Safety

**Probe**: "What level of factual error in AI outputs is acceptable to your users?"

Elicit:
- Hallucination tolerance: none (must be grounded) / low / medium / not safety-critical
- Grounding requirement: must cite sources? must be retrievable from known corpus?
- Toxicity / safety filtering level: public-facing vs. internal tool
- PII handling: does any user data pass through the LLM? Classification required?

**AI-specific probe**: "Is there a scenario where the AI output could cause direct harm
— financial, reputational, legal, or physical? If yes, what is the human-in-the-loop gate?"



### Domain 5 — Scale

**Probe**: "How many users will use this feature simultaneously at peak?"

Press for:
- Current baseline users
- Target at 6 months / 1 year
- Peak concurrency (e.g. Monday morning spike)
- Growth rate assumption

**AI-specific probe**: "LLM inference does not scale horizontally the same way as
stateless compute. If you have 1,000 concurrent users hitting the AI component,
each waiting up to 3 seconds — does your provider support that concurrency? Have
you checked your rate limits?"



### Domain 6 — Observability (mandatory for AI systems)

**Probe**: "When the AI component produces a bad result in production, how will you
know?"

Elicit:
- Minimum traces required per LLM call (prompt version, model, latency, token count)
- User feedback signal (thumbs up/down, explicit rating, implicit engagement)
- Eval cadence: how often are outputs evaluated against a quality benchmark?
- Alert threshold: at what error rate or quality degradation is an alert fired?

**AI-specific probe**: "What is your eval strategy? Do you have a golden dataset?
Who reviews model outputs in production, and how often?"



### Domain 7 — Security and Compliance

**Probe**: "Who can access the data that flows through this feature?"

Elicit:
- Data classification of inputs to the LLM (public / internal / confidential / regulated)
- Whether third-party LLM providers are permitted to receive this data
- Prompt injection risk: does user-provided text enter the prompt directly?
- Compliance scope: GDPR / HIPAA / SOC2 / none



## Output Format

Write to `knowledge/nfr.md`:

```markdown
# Non-Functional Requirements
_Date: [date] | Version: 1.0.0_

## Latency
| Operation | p50 | p95 | p99 | Notes |
|--|--|--|--|-|
| [action]  | [ms]| [ms]| [ms]| [streaming / atomic] |

## AI Inference Budget
| Operation | Max input tokens | Max output tokens | Max cost/call | Monthly ceiling |
|--|--|||-|
| [component] | [n] | [n] | [$] | [$] |

## Reliability and Fallback
| Failure mode | Threshold | Fallback behaviour | Acceptable degradation |
|--|--|-|-|
| LLM outage | [timeout] | [behaviour] | [yes/no] |
| Bad output detected | [condition] | [behaviour] | [yes/no] |

## Output Quality
- Hallucination tolerance: [none / low / medium]
- Grounding required: [yes — specify corpus / no]
- Safety filtering: [level — specify policy]
- PII in prompt: [yes — classification / no]
- Human-in-the-loop gate: [condition that triggers it]

## Scale Targets
- Current baseline: [DAU / RPS]
- 6-month target: [DAU / RPS]
- Peak concurrency: [simultaneous users]
- LLM concurrency limit checked: [yes / no — provider + limit]

## Observability Requirements
- Required trace fields per LLM call: [list]
- User feedback signal: [mechanism]
- Eval cadence: [frequency + method]
- Alert threshold: [condition]

## Security and Compliance
- Data classification: [level]
- Third-party LLM permitted: [yes / no / restricted to these data types]
- Prompt injection mitigation: [strategy]
- Compliance scope: [list]

## Open NFR Questions
- [ ] [Question with owner and due date]
```

## After the Session

Offer to immediately feed this output into `writing-prd` to populate Section 4.


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
