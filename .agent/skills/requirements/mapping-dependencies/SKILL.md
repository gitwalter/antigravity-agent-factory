---
name: mapping-dependencies
type: skill
description: 'Maps all upstream, downstream, data, and AI dependencies needed to implement
  the requirements. Produces a dependency graph with integration contracts and a risk
  register. Use when the user wants to understand what systems need to be connected,
  asks "what do we depend on", "what integrations are needed", "what could block us",
  or is preparing for architecture. Requires knowledge/prd.md or knowledge/prototype-brief.md.
  Writes to knowledge/dependencies.md.

  '
license: MIT
allowed-tools: Read, Write
metadata:
  version: 1.0.0
  phase: requirements
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

# Mapping Dependencies

Produces a complete dependency map before architecture begins.
Unknown dependencies discovered during implementation are the primary cause of
scope creep and schedule risk. Surface them now, not during a sprint.

## Input

Load (in order of preference):
1. `knowledge/prd.md` — if written
2. `knowledge/prototype-brief.md` — if PRD not yet written
3. `../ideation-phase/knowledge/competitive.md` — for third-party service context

## Dependency Taxonomy

Classify every dependency into exactly one of these types.
Do not invent new types — lack of precision defeats the purpose.

| Type | Definition | Example |
||--||
| **upstream-system** | A system that must exist and be callable before this feature works | Auth service, user profile API |
| **downstream-system** | A system this feature writes to or triggers | Analytics pipeline, email service |
| **data-dependency** | A dataset, schema, or corpus that must exist at runtime | User embeddings table, product catalogue |
| **ai-model** | An LLM, embedding model, or classifier called at runtime | Claude API, text-embedding-3-small |
| **mcp-server** | An MCP server providing tools or resources to an agent | filesystem, web-search, database |
| **external-api** | A third-party API not under team control | Stripe, SendGrid, Mapbox |
| **infrastructure** | Cloud services, queues, caches, storage | S3, Redis, SQS |
| **team-dependency** | Another team whose work must ship before this can | Platform team's auth redesign |



## Step 1 — Discovery

For each functional requirement in the PRD (or each AI component in the prototype brief):

Ask: "For this to work, what must already exist?"
Ask: "What does this write to or trigger downstream?"
Ask: "What data must be present at runtime for the AI component?"

Use web-search to verify:
- Third-party API rate limits and pricing (search: `[service] API rate limits 2025`)
- LLM provider concurrency limits (search: `[provider] API rate limits tokens per minute`)
- Known outage history for critical external dependencies (search: `[service] status incidents`)



## Step 2 — Integration Contracts

For each dependency, define the integration contract:

```markdown
### [dependency name] ([type])

| Attribute | Value |
|--|-|
| Owner | [team / vendor] |
| Interface | [REST / GraphQL / gRPC / MCP / SDK / async event] |
| Auth method | [API key / OAuth2 / mTLS / IAM role] |
| SLA | [uptime % / latency p99] |
| Rate limit | [requests/min or tokens/min] |
| Data sent | [what we send — include data classification] |
| Data received | [what we receive] |
| Version pinned | [yes — version / no] |
| Fallback | [behaviour if unavailable] |
| Cost | [per-call or monthly estimate] |
```

For AI model dependencies, additionally capture:
```markdown
| Max context window | [tokens] |
| Streaming supported | [yes / no] |
| Structured output | [yes / no — JSON mode / tool use] |
| Fine-tuning available | [yes / no] |
| Data residency | [region(s) — relevant for compliance] |
```



## Step 3 — Dependency Graph (text representation)

Produce a Mermaid diagram description saved as a reference:

```
flowchart LR
  feature["[Feature Name]"]
  feature --> upstream1["[upstream-system]"]
  feature --> ai1["[ai-model]"]
  feature --> mcp1["[mcp-server]"]
  downstream1["[downstream-system]"] <-- feature
```



## Step 4 — Risk Register

For each dependency, assess:

| Dependency | Type | Risk | Likelihood | Impact | Mitigation |
|||||--||
| [name] | [type] | [what could go wrong] | H/M/L | H/M/L | [strategy] |

Flag any dependency where:
- The owning team has not confirmed availability
- The external API has had > 1 major incident in the past 6 months
- The rate limit is within 2× of the projected load at target scale
- The data required does not yet exist and must be backfilled



## Output

Write to `knowledge/dependencies.md` with all four sections:
1. Dependency inventory (all dependencies, classified)
2. Integration contracts (one per dependency)
3. Mermaid graph (text)
4. Risk register

## After Mapping

Flag the top 3 risks to the user explicitly:
> "The three highest-risk dependencies in this map are: [list].
> Before architecture begins, these three need owner confirmation or a mitigation plan."


## When to Use
Follow standard when to use documentation.

## Prerequisites
Follow standard prerequisites documentation.

## Process
Follow standard process documentation.

## Best Practices
Follow standard best practices documentation.
