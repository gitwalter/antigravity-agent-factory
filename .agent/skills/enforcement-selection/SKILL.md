# Enforcement Selection Skill

## Overview

This skill guides users through selecting enforcement patterns that will ensure their agent system lives its values, not just states them.

## Philosophy

> Values without enforcement are just aspirations.

Enforcement patterns translate our aspirations into operational reality. They are the mechanisms that ensure our values are practiced, not just professed.

## Purpose

Help users select and configure enforcement patterns that match their project's needs and risk profile, ensuring the agent system maintains integrity through measurable, enforceable standards.

## Trigger

- During onboarding after principles are defined
- User mentions "enforcement", "quality gates", "standards"
- Request to configure automated checks

## Process

### Step 1: Explain Enforcement Philosophy

```
Your axioms and principles define what you value.
Enforcement patterns ensure those values are lived.

Think of enforcement as:
- Quality: Craftsmanship standards that code must meet
- Safety: Guardrails that protect users and systems
- Integrity: Checks that keep you true to your purpose

Excellence emerges from consistent discipline.
```

### Step 2: Present Enforcement Categories

```
Select enforcement patterns by category:

QUALITY ENFORCEMENT (Craftsmanship)
[x] E1: Test Coverage Gate - Verify code is tested
[x] E2: Peer Review Gate - Ensure collaborative refinement
[ ] E3: Documentation Completeness - Share knowledge clearly
[x] E4: Style Consistency - Harmony in the details

SAFETY ENFORCEMENT (Protection)
[x] E5: Destructive Action Confirmation - Prevent accidental harm
[ ] E6: Backup Before Modification - Enable recovery
[ ] E7: Security Vulnerability Check - Protect against threats
[ ] E8: Production Safeguard - Extra care for live systems

INTEGRITY ENFORCEMENT (Alignment)
[x] E9: Axiom Compliance Check - Rules trace to axioms
[ ] E10: Purpose Alignment Check - Work serves mission
[ ] E11: Transparency Log - Decisions are documented

Recommended minimum: E1, E2, E4, E5, E9
```

### Step 3: Configure Thresholds

For each selected enforcement, configure thresholds:

```
E1 - Test Coverage Gate:
  Minimum coverage: [80]%
  New code coverage: [90]%
  Severity: [blocking]

E2 - Peer Review Gate:
  Minimum reviewers: [1]
  Approval required: [yes]
  Comments must be resolved: [yes]

(continue for each selected enforcement...)
```

### Step 4: Configure Override Policies

```
Override policies define when rules can be bypassed:

E1 (Test Coverage): 
  [ ] Never - Must always pass
  [x] With justification - Document why
  [ ] With approval - Requires senior sign-off

E5 (Destructive Confirmation):
  [x] Never - Always require confirmation
  [ ] With justification
  [ ] With approval

For safety-critical projects, recommend "Never" or "With approval" for most enforcements.
```

### Step 5: Generate Enforcement Configuration

```yaml
# enforcement.yaml - Generated enforcement configuration

enforcements:
  quality:
    E1_test_coverage:
      enabled: true
      threshold: 80
      severity: blocking
      override: with_justification
    
    E2_code_review:
      enabled: true
      min_reviewers: 1
      require_approval: true
      override: with_approval
    
    E4_style_consistency:
      enabled: true
      severity: blocking
      override: never
  
  safety:
    E5_destructive_confirmation:
      enabled: true
      severity: blocking
      override: never
    
    E8_production_safeguard:
      enabled: true
      require_staging_test: true
      override: with_approval
  
  integrity:
    E9_axiom_compliance:
      enabled: true
      severity: blocking
      override: never
```

## Outputs

1. **Enforcement Configuration** - `enforcement.yaml` for generated project
2. **Integration with CI/CD** - Hooks for automated enforcement
3. **Override Log Template** - For documenting exceptions

## Integration Points

- **Input from**: Axiom selection, principle definition
- **Reads**: `patterns/enforcement/*.json`
- **Outputs to**: `enforcement.yaml`, CI/CD configuration
- **Related**: `practice-selection` skill

## Best Practices

1. Start with essential enforcements (E1, E2, E5, E9)
2. Match enforcement strictness to project risk level
3. "Never" override for safety-critical enforcements
4. Document rationale for all override policies
5. Review enforcement effectiveness quarterly
