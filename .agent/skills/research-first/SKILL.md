---
name: research-first
description: Research existing solutions before building to create multiplied value
type: skill
pattern: patterns/skills/reactive-index.json
knowledge: [research-first-development.json, best-practices.json, design-patterns.json]
triggers:
  - performance optimization
  - new architectural pattern
  - security implementation
  - caching strategy
  - integration with external systems
axioms: [A0_love_and_trust, A2_humility, A3_transparency]
---

# Research-First Development Skill

Research existing solutions before building significant features. This skill embodies **A2 (Humility)** - acknowledging that others may have solved the problem better - while creating **multiplied value** through reusable patterns.

## Core Principle

> **Option B: Research → Document → Test → Build**
>
> Each researched pattern benefits all future projects.

## When to Invoke

### Always Research

- Performance optimization
- Security implementation
- Authentication/authorization patterns
- Caching strategies
- Database design patterns
- API design decisions
- Build/deployment pipelines
- Testing strategies

### Consider Research

- Error handling patterns
- Logging and monitoring
- Configuration management
- State management
- Concurrency patterns

### Skip Research

- Bug fixes with known cause
- Minor UI adjustments
- Documentation updates
- Dependency version bumps

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 1. TRIGGER  │────▶│ 2. RESEARCH │────▶│ 3. DOCUMENT │
│ Recognize   │     │ Search      │     │ Knowledge   │
│ the need    │     │ sources     │     │ file        │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
┌─────────────┐     ┌─────────────┐     ┌──────▼──────┐
│ 6. INTEGRATE│◀────│ 5. BUILD    │◀────│ 4. TEST     │
│ Reuse in    │     │ Implement   │     │ TDD first   │
│ projects    │     │ solution    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Step 1: Recognize Trigger

Ask: "Does this feel like something someone else has solved well?"

**Indicators:**
- Problem is not domain-specific
- Performance or security implications
- Cross-cutting concern
- Will be used in multiple places

### Step 2: Research Sources

**Academic:**
- ACM Digital Library
- Google Scholar
- arXiv (cs.SE, cs.PL)

**Industry:**
- GitHub repositories and discussions
- Dev.to, Medium technical articles
- Stack Overflow patterns
- Official documentation

**Community:**
- Reddit (r/programming, language-specific)
- Discord/Slack communities

### Step 3: Document Findings

Create `knowledge/<pattern-name>.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Pattern Name",
  "description": "What this pattern solves",
  "version": "1.0.0",
  "axiomAlignment": {
    "A2_humility": "How this serves humility"
  },
  "research_sources": {
    "academic": { ... },
    "industry": { ... }
  },
  "patterns": { ... },
  "anti_patterns": { ... }
}
```

### Step 4: Write Tests First (TDD)

Create `tests/unit/test_<pattern>.py`:

- Test that knowledge file exists and is valid
- Test that required fields are present
- Test edge cases and integration points

### Step 5: Build Implementation

Follow the researched pattern, referencing the knowledge file.

### Step 6: Integrate for Reuse

- Add to relevant blueprints
- Create skill pattern if applicable
- Update templates

## Example Usage

### Scenario: Pre-commit hooks too slow

**1. Trigger recognized:**
"This is a performance optimization that will benefit all projects."

**2. Research:**
- pre-commit framework caching
- Nx/Turborepo affected pattern
- Salsa incremental computation
- Python watchdog file watching

**3. Document:**
`knowledge/reactive-indexing-patterns.json`

**4. Test:**
`tests/unit/test_reactive_index.py` (44 tests)

**5. Build:**
`scripts/validation/update_index.py`

**6. Integrate:**
`patterns/skills/reactive-index.json` for generated projects

## Anti-Patterns to Avoid

### Not Invented Here

**Symptom:** Dismissing external solutions without evaluation
**Remedy:** Always check if mature solutions exist first

### Analysis Paralysis

**Symptom:** Weeks of research with no implementation
**Remedy:** Time-box research (hours, not weeks)

### Copy-Paste Without Understanding

**Symptom:** Cannot explain why the approach was chosen
**Remedy:** Document rationale in knowledge file

### Research Once, Forget

**Symptom:** Repeating research for similar problems
**Remedy:** Always create knowledge file, even for rejected approaches

## Invocation

Agents can invoke this skill explicitly:

```
I need to implement [X]. Let me invoke research-first:
1. Is this a research trigger? [Check list above]
2. If yes: Research → Document → Test → Build
3. If no: Proceed directly
```

## Benefits

**Immediate:**
- Better solution quality
- Avoid common pitfalls
- Learn from others' experience

**Long-term:**
- Reusable patterns for all generated projects
- Knowledge base grows with each decision
- Reduced technical debt

**Multiplied Value:**
Each researched pattern benefits every future project generated by the Factory.

## Related

- **Knowledge:** `research-first-development.json`
- **Pattern:** `patterns/skills/reactive-index.json`
- **Skill:** `grounding-verification` (for claim verification)
