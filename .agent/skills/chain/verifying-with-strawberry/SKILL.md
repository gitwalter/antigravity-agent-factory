---
agents:
- none
category: chain
description: Factual claim verification - the canonical profile of grounding-verification
knowledge:
- none
name: verifying-with-strawberry
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Strawberry Verification

Factual claim verification - the canonical profile of grounding-verification

The canonical profile of the grounding-verification pattern. Detects procedural hallucinations by comparing LLM confidence between scrubbed and full evidence passes.

## Relationship to Base Pattern

This skill **extends** `grounding-verification` with the `strawberry` profile:

```
grounding-verification.json (base)
    └── strawberry-verification.json (profile: strawberry)
```

For the full algorithm, response schema, and error handling, see the base skill: `{directories.skills}/grounding-verification/SKILL.md`

## Philosophy

> If removing specific identifiers from evidence doesn't change confidence, the evidence wasn't actually used - indicating confabulation.

This skill implements an adapted version of the Pythea/Strawberry verification method. Since Cursor's LLM doesn't expose logprobs (required for true bit-budget calculation), we use a **confidence delta method** as a pragmatic approximation.

## The Strawberry Problem

Ask an LLM: "How many r's are in 'strawberry'?"

The LLM might:
1. Write out "s-t-r-a-w-b-e-r-r-y"
2. Correctly identify each 'r' position
3. Count: 3 r's
4. Then output: "There are 2 r's"

This is a **procedural hallucination** - the AI generates correct intermediate steps but ignores them in the final output.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Prepare Scrubbed Evidence
Replace specific identifiers (tables, fields, classes, functions, numbers, paths) with typed placeholders like `[TABLE_1]`, `[FIELD_1]`, `[CLASS_1]`, `[NUM_1]`.

### Step 2: Run Scrubbed Pass
Query LLM with scrubbed evidence and request structured JSON response with verdict (ENTAILED/CONTRADICTED/UNSURE) and confidence score.

### Step 3: Run Full Pass
Query LLM with complete evidence containing all identifiers. Request same structured response format.

### Step 4: Calculate Delta
Compute `delta = full_confidence - scrubbed_confidence` to measure how essential the specific identifiers are.

### Step 5: Determine Status
Compare delta and confidence scores against strawberry profile thresholds:
- **VERIFIED**: full_confidence >= 0.8 AND delta >= 0.3
- **PLAUSIBLE**: full_confidence >= 0.6 AND delta >= 0.15
- **SUSPICIOUS**: full_confidence >= 0.6 AND delta < 0.15
- **UNSUPPORTED**: full_confidence < 0.6 OR verdict == CONTRADICTED

### Step 6: Take Action
- VERIFIED: Proceed with confidence
- PLAUSIBLE: Proceed with caution, note uncertainty
- SUSPICIOUS: Add warning, investigate if claim is from evidence or pattern guess
- UNSUPPORTED: STOP - gather more evidence or ask user

## Two-Pass Verification Process

### Pass 1: Scrubbed Evidence Test

Replace specific identifiers with placeholders:

**Original Evidence:**
```
Table users has field email of type VARCHAR(255)
```

**Scrubbed Evidence:**
```
Table [TABLE_1] has field [FIELD_1] of type VARCHAR([NUM_1])
```

**Question:** "Based on this scrubbed evidence, can the claim be verified?"

### Pass 2: Full Evidence Test

Use complete evidence with all identifiers intact.

**Question:** "Based on this complete evidence, is the claim verified?"

### Compare Results

Calculate the confidence delta:

```
delta = full_confidence - scrubbed_confidence
```

| Delta | Interpretation | Status |
|-------|---------------|--------|
| >= 0.3 | Evidence is essential | VERIFIED |
| 0.15 - 0.3 | Evidence is helpful | PLAUSIBLE |
| < 0.15 | Evidence may not be used | SUSPICIOUS |
| Both low | Insufficient evidence | UNSUPPORTED |

## Response Format

Request JSON responses from the LLM:

```json
{
  "verdict": "ENTAILED | CONTRADICTED | UNSURE",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation"
}
```

## Scrubbing Rules

Use typed placeholders for consistent mapping:

| Pattern | Placeholder | Example |
|---------|-------------|---------|
| Table/entity names | `[TABLE_{N}]` | users → [TABLE_1] |
| Field/column names | `[FIELD_{N}]` | email → [FIELD_1] |
| Class names | `[CLASS_{N}]` | UserService → [CLASS_1] |
| Function names | `[FUNC_{N}]` | getUserById → [FUNC_1] |
| Specific numbers | `[NUM_{N}]` | 255 → [NUM_1] |
| File paths | `[PATH_{N}]` | src/auth.ts → [PATH_1] |

## Verification Thresholds

```
VERIFIED:    full_confidence >= 0.8 AND delta >= 0.3
PLAUSIBLE:   full_confidence >= 0.6 AND delta >= 0.15
SUSPICIOUS:  full_confidence >= 0.6 AND delta < 0.15
UNSUPPORTED: full_confidence < 0.6 OR verdict == CONTRADICTED
```

## Decision Actions

| Status | Action |
|--------|--------|
| VERIFIED | Proceed with confidence |
| PLAUSIBLE | Proceed with caution, note uncertainty |
| SUSPICIOUS | Add warning, consider if claim is from evidence or pattern guess |
| UNSUPPORTED | STOP - gather more evidence or ask user |

## Error Handling

### Parse Failure
If LLM response isn't valid JSON:
1. Retry with simplified prompt (max 2 retries)
2. Fallback: extract verdict via regex

### Conflicting Verdicts
If passes give contradictory results:
- Mark as SUSPICIOUS
- Require user confirmation

### UNSURE Response
If LLM returns UNSURE:
- UNSURE on scrubbed + ENTAILED on full → VERIFIED
- UNSURE on both → PLAUSIBLE (gather more evidence)

## Example Verification

**Claim:** "Table users contains field email with data type VARCHAR and length 255"

**Evidence Spans:**
- S0: "From database docs: users.email stores user email addresses, VARCHAR(255)"
- S1: "From schema catalog: email column, type VARCHAR, max length 255"

**Scrubbed Evidence:**
- S0: "From documentation: [TABLE_1].[FIELD_1] stores [STR_1], VARCHAR([NUM_1])"
- S1: "From catalog: [FIELD_1] column, type VARCHAR, max length [NUM_1]"

**Scrubbed Test Result:**
```json
{
  "verdict": "UNSURE",
  "confidence": 0.3,
  "reasoning": "Cannot verify specific table/field without identifiers"
}
```

**Full Test Result:**
```json
{
  "verdict": "ENTAILED",
  "confidence": 0.95,
  "reasoning": "Both sources confirm users.email is VARCHAR(255)"
}
```

**Analysis:**
- Delta = 0.95 - 0.3 = 0.65 (well above 0.3 threshold)
- Evidence is essential - scrubbed pass cannot verify
- **Status: VERIFIED**

## Confabulation Indicators

Watch for these signs that the LLM may be confabulating:

- Claim seems obvious without needing specific evidence
- Scrubbed evidence supports claim just as well as full evidence
- Confidence doesn't increase when adding specific identifiers
- Claim uses generic patterns that would work for any similar object

## Best Practices

- **Scrub consistently across passes**: Use the same scrubbing rules and placeholder mapping for both scrubbed and full evidence passes to ensure fair comparison
- **Set appropriate confidence thresholds**: Adjust verification thresholds based on the criticality of the claim; use stricter thresholds for production-impacting decisions
- **Verify multiple independent claims separately**: Don't batch multiple claims into a single verification; verify each claim individually to identify which specific claims are unsupported
- **Document scrubbing transformations**: Keep a record of what identifiers were scrubbed and how they map to placeholders for transparency and debugging
- **Retry on UNSURE with clearer prompts**: If the LLM returns UNSURE, refine the question or provide more context rather than immediately marking as UNSUPPORTED
- **Use verification before major actions**: Always run strawberry verification before committing to implementation decisions, especially when grounding confidence is MEDIUM

## Integration with Other Skills

| Skill | How Strawberry Verification Helps |
|-------|-----------------------------------|
| `grounding` | Verify grounding results before use |
| `code-review` | Validate claims about code behavior |
| `security-audit` | Verify security vulnerability claims |
| `requirements-gathering` | Validate requirement interpretations |

## Axiom Alignment

| Axiom | How This Skill Applies |
|-------|------------------------|
| A1 (Verifiability) | Mathematically verify claims against evidence |
| A3 (Transparency) | Make verification reasoning visible |
| A4 (Non-Harm) | Prevent acting on hallucinated claims |
| A5 (Consistency) | Apply uniform verification method |

## Output Format

```markdown
### Strawberry Verification Report

**Verification Method:** Confidence Delta (Native)
**Claims Analyzed:** {COUNT}

---

#### Evidence Spans

| Span | Content Summary | Source |
|------|-----------------|--------|
| S0 | {SUMMARY} | {SOURCE} |

---

#### Claim Verification

| Claim | Scrubbed Conf | Full Conf | Delta | Status |
|-------|---------------|-----------|-------|--------|
| {CLAIM} | {0.XX} | {0.XX} | {0.XX} | {STATUS} |

---

### RECOMMENDATION: {PROCEED|PROCEED_WITH_WARNINGS|STOP|GATHER_MORE_EVIDENCE}

**Rationale:** {RATIONALE}
```

## References

- [Pythea/Strawberry](https://github.com/leochlon/pythea) - Original implementation by Leon Chlon
- `{directories.patterns}/skills/strawberry-verification.json` - Full pattern specification
- `diagrams/verification-flow.md` - Flow diagrams

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
