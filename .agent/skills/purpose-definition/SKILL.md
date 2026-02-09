---
description: Guide users through articulating why their agent system should exist, who it serves, and how success will be measured
---

# Purpose Definition

Guide users through articulating why their agent system should exist, who it serves, and how success will be measured

## 
# Purpose Definition Skill

## 
# Purpose Definition Skill

## Overview
This skill handles **Phase 0 (Layer 1)** of the onboarding process, where users define the purpose, stakeholders, and success criteria for their agent system.

## Purpose
Guide users through articulating why their agent system should exist, who it serves, and how success will be measured. The purpose must align with the selected axioms from Layer 0.

## Trigger
- After axiom selection is complete
- User mentions "purpose", "mission", or "why"
- Explicit request to define project goals

## Process
### Step 1: Mission Statement

Ask for a one-sentence mission:

```
Based on your foundational axioms, let's define your agent system's purpose.

Q1: In ONE sentence, why should this agent system exist?

Good examples:
- "To accelerate API development by automating boilerplate and enforcing best practices"
- "To ensure code quality by catching bugs before they reach production"
- "To reduce research iteration time by automating experiment tracking"

Note: Your mission must be verifiable (A1) and serve users (A2).
```

Validate against axioms:
- A1: Is the outcome measurable/verifiable?
- A2: Does it clearly serve human users?

### Step 2: Stakeholder Identification

Ask who benefits:

```
Q2: Who are the PRIMARY users or beneficiaries of this system?

Be specific. Examples:
- "Backend developers on the payments team"
- "Data scientists in the ML platform group"
- "QA engineers responsible for integration testing"

Note: This ensures your agents prioritize these users (A2).
```

Validate:
- Are these human stakeholders?
- Are they specific enough to guide decisions?

### Step 3: Success Criteria

Ask for measurable outcome:

```
Q3: What is the SINGLE most important outcome that defines success?

This must be measurable (A1). Examples:
- "Reduce time from API design to working implementation by 50%"
- "Achieve 90%+ test coverage on all new code"
- "Cut bug escape rate to production by 80%"

How will you measure this?
```

Validate:
- Is it quantifiable?
- Is there a clear measurement approach?

### Step 4: Value Derivation

Based on selected axioms, derive guiding values:

```
Based on your axioms and purpose, here are your system's guiding values:

From A1 (Verifiability): Evidence-Based Decisions
From A2 (User Primacy): User-Focus
From A3 (Transparency): Open Communication
{If A6 selected}: Simplicity-First
{If A10 selected}: Continuous Learning

These values will guide your agents' behavior.
```

### Step 5: Generate PURPOSE.md

Create the purpose document:

```markdown
# {PROJECT_NAME} - Purpose & Mission

```
Based on your foundational axioms, let's define your agent system's purpose.

Q1: In ONE sentence, why should this agent system exist?

Good examples:
- "To accelerate API development by automating boilerplate and enforcing best practices"
- "To ensure code quality by catching bugs before they reach production"
- "To reduce research iteration time by automating experiment tracking"

Note: Your mission must be verifiable (A1) and serve users (A2).
```

```
Q2: Who are the PRIMARY users or beneficiaries of this system?

Be specific. Examples:
- "Backend developers on the payments team"
- "Data scientists in the ML platform group"
- "QA engineers responsible for integration testing"

Note: This ensures your agents prioritize these users (A2).
```

```
Q3: What is the SINGLE most important outcome that defines success?

This must be measurable (A1). Examples:
- "Reduce time from API design to working implementation by 50%"
- "Achieve 90%+ test coverage on all new code"
- "Cut bug escape rate to production by 80%"

How will you measure this?
```

```
Based on your axioms and purpose, here are your system's guiding values:

From A1 (Verifiability): Evidence-Based Decisions
From A2 (User Primacy): User-Focus
From A3 (Transparency): Open Communication
{If A6 selected}: Simplicity-First
{If A10 selected}: Continuous Learning

These values will guide your agents' behavior.
```

## Mission Statement
{one_sentence_purpose}

## Who We Serve
**Primary Stakeholders**: {primary_stakeholders}

**How They Benefit**: {derived_from_mission}

## Success Definition
**Primary Outcome**: {success_criteria}

**How We Measure**: {measurement_approach}

## Guiding Values
These values derive from our foundational axioms:

1. **Evidence-Based** (from A1): All decisions backed by verifiable data
2. **User-Focused** (from A2): Stakeholder needs drive every action
3. **Transparent** (from A3): Reasoning is always explainable
{additional values from optional axioms}

## Alignment with Axioms
| Axiom | How This Purpose Aligns |
|-------|------------------------|
| A1 - Verifiability | {mission is measurable via success criteria} |
| A2 - User Primacy | {serves identified stakeholders} |
| A4 - Non-Harm | {does not harm users or systems} |

---

*This purpose document guides all agent behavior in this system.*
*Last updated: {date}*
```

## Outputs
1. **PURPOSE.md** - Purpose document for generated project
2. **Purpose Configuration** - Stored in project requirements
3. **Value Derivations** - For `.cursorrules` Layer 1 section

## Integration Points
- **Input from**: Axiom selection (Layer 0 configuration)
- **Outputs to**: `PURPOSE.md`, project configuration
- **Next skill**: Depth selection, then `principle-generation` or `methodology-selection`

## Validation Rules
1. **Mission Validation**:
   - Must be single sentence
   - Must describe a verifiable outcome
   - Must imply user benefit

2. **Stakeholder Validation**:
   - Must be human users/beneficiaries
   - Must be specific enough for prioritization
   - Cannot be abstract (e.g., not "everyone")

3. **Success Criteria Validation**:
   - Must be quantifiable
   - Must have measurement approach
   - Must align with mission

## Best Practices
1. Keep mission to ONE sentence
2. Push for specific, named stakeholders
3. Require quantifiable success criteria
4. Derive values directly from axioms
5. Show axiom alignment explicitly

## Prerequisites
> [!IMPORTANT]
> Requirements:
