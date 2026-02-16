---
description: Universal two-pass verification for LLM grounding using confidence delta
  comparison
name: verifying-grounding
type: skill
---
# Grounding Verification

Universal two-pass verification for LLM grounding using confidence delta comparison

Universal two-pass verification for any LLM grounding scenario. Detects when the LLM may be confabulating by comparing confidence between scrubbed and full evidence passes.

## Core Principle

> **If removing specific identifiers from evidence doesn't significantly change LLM confidence, the evidence may not have been used - indicating potential confabulation.**

## How It Works

```
┌─────────────────┐     ┌─────────────────┐
│ Scrubbed Pass   │     │ Full Pass       │
│ (anonymized)    │     │ (complete)      │
│                 │     │                 │
│ [TABLE_1] has   │     │ users table has │
│ [FIELD_1] of    │     │ email field of  │
│ type [TYPE_1]   │     │ type VARCHAR    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
   confidence: 0.3         confidence: 0.95
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
              delta = 0.65
              (>= 0.3 threshold)
                     │
                     ▼
              ✓ VERIFIED
        (evidence is essential)
```

## Best Practices

- **Select appropriate profile**: Choose the verification profile (strawberry, code, documentation, data, security) that matches your domain for optimal thresholds
- **Use triggers wisely**: Configure triggers (always, on_medium_confidence, on_critical_claim, on_conflict) based on cost/latency trade-offs
- **Scrub consistently**: Replace all domain-specific identifiers (table names, classes, functions) with typed placeholders to test evidence dependency
- **Handle UNSURE gracefully**: UNSURE responses don't always indicate failure - consider context and gather more evidence when needed
- **Monitor verification costs**: Balance verification frequency with API costs - use selective triggers for non-critical claims
- **Document violations**: When violations occur, log them for pattern analysis and system improvement

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Collect Evidence
Gather evidence spans from grounding skills or other sources that support the claim to be verified.

### Step 2: Create Scrubbed Version
Replace specific identifiers (table names, field names, classes, functions, etc.) with typed placeholders like `[TABLE_1]`, `[FIELD_1]`, `[CLASS_1]`.

### Step 3: Run Scrubbed Pass
Query the LLM with scrubbed evidence and measure confidence in the claim. This tests whether the evidence structure alone supports the claim.

### Step 4: Run Full Pass
Query the LLM with complete evidence containing all identifiers. Measure confidence again.

### Step 5: Calculate Delta
Compute the difference: `delta = full_confidence - scrubbed_confidence`. A high delta indicates the specific identifiers are essential.

### Step 6: Determine Status
Compare delta against profile thresholds to determine verification status (VERIFIED, PLAUSIBLE, SUSPICIOUS, or UNSUPPORTED).

### Step 7: Take Action
Proceed with confidence, add warnings, or stop based on the verification status.

## Available Profiles

Skills opt-in to verification by selecting a profile that matches their domain:

| Profile | Domain | Thresholds | Default Trigger |
|---------|--------|------------|-----------------|
| `strawberry` | General factual claims | Standard (delta >= 0.3) | on_medium_confidence |
| `code` | Code structure, APIs, functions | Standard | on_medium_confidence |
| `documentation` | External docs, API refs | Relaxed (delta >= 0.25) | on_conflict |
| `data` | Database schemas, data models | Strict (delta >= 0.35) | on_medium_confidence |
| `security` | Security-critical claims | Very strict (delta >= 0.4) | always |

## Opting In

Skills add verification to their frontmatter:

```json
{
  "frontmatter": {
    "name": "your-skill",
    "verification": {
      "enabled": true,
      "profile": "data",
      "trigger": "on_medium_confidence"
    }
  }
}
```

## Trigger Options

| Trigger | When | Use Case |
|---------|------|----------|
| `always` | Every grounding result | Critical systems, security |
| `on_medium_confidence` | Initial confidence is MEDIUM | Default for most skills |
| `on_critical_claim` | Claims marked critical | Selective verification |
| `on_conflict` | Sources conflict | Documentation lookups |
| `manual` | Explicitly called | Exploratory queries |

## Verification Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| **VERIFIED** | Evidence essential (high delta) | Proceed with confidence |
| **PLAUSIBLE** | Evidence helpful (medium delta) | Proceed with caution |
| **SUSPICIOUS** | Evidence may not be used (low delta) | Add warning, investigate |
| **UNSUPPORTED** | Insufficient evidence | STOP - gather more or ask user |

## Profile Details

### Strawberry (General/Factual)

The canonical profile, inspired by Pythea/Strawberry.

**Scrubbing:** Tables, fields, classes, functions, numbers, strings, paths, URLs

**Thresholds:**
- VERIFIED: confidence >= 0.8, delta >= 0.3
- PLAUSIBLE: confidence >= 0.6, delta >= 0.15
- SUSPICIOUS: confidence >= 0.6, delta < 0.15
- UNSUPPORTED: confidence < 0.6

### Code (Structure/APIs)

For verifying claims about code structure, APIs, and function behavior.

**Scrubbing:** Classes, functions, methods, variables, types, paths, line numbers, modules, packages

**Thresholds:** Same as strawberry

### Documentation (External Docs)

For verifying claims from external documentation, API docs, configuration references.

**Scrubbing:** Versions, endpoints, config keys, parameters, values, URLs, commands

**Thresholds (relaxed):**
- VERIFIED: confidence >= 0.75, delta >= 0.25
- PLAUSIBLE: confidence >= 0.55, delta >= 0.1
- Note: Documentation is often partial or version-specific

### Data (Schemas/Models)

For verifying database schemas, data models, entity relationships.

**Scrubbing:** Tables, columns, data types, constraints, indexes, schemas, databases

**Thresholds (strict):**
- VERIFIED: confidence >= 0.85, delta >= 0.35
- Note: Data errors are costly and hard to detect

### Security (Critical Claims)

For verifying security-critical claims, vulnerabilities, auth/authz.

**Scrubbing:** CVEs, vulnerabilities, attack vectors, algorithms, keys, secrets, permissions, roles

**Thresholds (very strict):**
- VERIFIED: confidence >= 0.9, delta >= 0.4
- PLAUSIBLE: confidence >= 0.75, delta >= 0.25
- Note: Security errors can be catastrophic

## Algorithm

### Two-Pass Comparison

1. **Scrubbed Pass**: Replace identifiers with typed placeholders
2. **Full Pass**: Use complete evidence
3. **Calculate Delta**: `delta = full_confidence - scrubbed_confidence`
4. **Determine Status**: Compare delta against profile thresholds

### Response Schema

```json
{
  "verdict": "ENTAILED | CONTRADICTED | UNSURE",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation"
}
```

### Verdict Rules

- **ENTAILED**: Claim explicitly supported by context
- **CONTRADICTED**: Context explicitly contradicts claim
- **UNSURE**: Context neither confirms nor denies

## Error Handling

### Parse Failure
- Retry with simplified prompt (max 2 retries)
- Fallback: extract verdict via regex

### Conflicting Verdicts
- Mark as SUSPICIOUS
- Require user confirmation

### UNSURE Response
- UNSURE on scrubbed + ENTAILED on full → VERIFIED
- UNSURE on both → PLAUSIBLE (gather more evidence)

## When NOT to Verify

To save cost/latency, skip verification when:

- HIGH confidence from cached/pre-verified sources
- Exploratory queries where precision isn't critical
- Time-sensitive operations where latency matters

## Integration with Existing Skills

| Skill | Profile | Trigger |
|-------|---------|---------|
| `grounding` | data | on_medium_confidence |
| `security-audit` | security | always |
| `code-review` | code | on_medium_confidence |
| `mcp-results` | documentation | on_conflict |

## Output Format

```markdown
### Grounding Verification Report

**Profile:** {PROFILE}
**Trigger:** {TRIGGER}
**Claims Analyzed:** {COUNT}

---

#### Claim Verification

| Claim | Scrubbed Conf | Full Conf | Delta | Status |
|-------|---------------|-----------|-------|--------|
| {CLAIM} | {0.XX} | {0.XX} | {0.XX} | {STATUS} |

---

### RECOMMENDATION: {PROCEED|PROCEED_WITH_WARNINGS|STOP|GATHER_MORE_EVIDENCE}

**Rationale:** {RATIONALE}
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `strawberry-verification` | Profile implementation (extends this base) |
| `grounding` | Consumer (opts in with data profile) |
| `security-audit` | Consumer (opts in with security profile) |

## Axiom Alignment

| Axiom | How This Skill Applies |
|-------|------------------------|
| A1 (Verifiability) | Mathematically verify claims against evidence |
| A3 (Transparency) | Make verification reasoning visible |
| A4 (Non-Harm) | Prevent acting on hallucinated claims |
| A5 (Consistency) | Apply uniform verification across all grounding |

## References

- [Pythea/Strawberry](https://github.com/leochlon/pythea) - Original implementation by Leon Chlon
- `{directories.patterns}/skills/grounding-verification.json` - Full pattern specification
- `{directories.patterns}/skills/strawberry-verification.json` - Strawberry profile
- `diagrams/verification-flow.md` - Flow diagrams

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
