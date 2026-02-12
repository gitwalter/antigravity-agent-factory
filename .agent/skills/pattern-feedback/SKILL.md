---
description: Implement inductive learning by observing patterns and proposing improvements
  to axioms, principles, and methodologies
name: pattern-feedback
type: skill
---

# Pattern Feedback

Implement inductive learning by observing patterns and proposing improvements to axioms, principles, and methodologies

## 
# Pattern Feedback Skill

## 
# Pattern Feedback Skill

## Overview
This skill implements the **Inductive Learning** component of the 5-layer architecture. It observes patterns from development experience, generalizes them, and proposes improvements to the axioms, principles, and methodologies.

## Purpose
Enable continuous improvement by learning from actual development outcomes. When patterns emerge that could improve the system, this skill captures, validates, and integrates them - embodying Axiom A10 (Learning).

## Philosophical Foundation
> "Every failure is an opportunity to improve" - A10 (Learning)

This skill closes the loop between experience and knowledge, ensuring that:
- Successful patterns are captured and shared
- Failures become lessons rather than repeated mistakes
- The system evolves toward greater effectiveness

## Trigger
- End of sprint/iteration (automatic review)
- User mentions "what did we learn", "patterns", "retrospective"
- Multiple similar issues encountered
- Explicit request to analyze patterns

## Process
### Step 1: Observation Collection

Gather data from development activities:

```yaml
observation_sources:
  code_reviews:
    - common_issues_found
    - frequently_applied_fixes
    - quality_improvements
  
  test_results:
    - recurring_failure_patterns
    - coverage_gaps
    - performance_regressions
  
  user_interactions:
    - clarification_requests
    - repeated_questions
    - confusion_points
  
  workflow_execution:
    - bottlenecks_identified
    - skipped_steps
    - time_spent_per_phase
```

### Step 2: Pattern Recognition

Analyze observations to identify patterns:

```python
def identify_patterns(observations: List[Observation]) -> List[Pattern]:
    """
    Identify recurring patterns from observations.
    
    Pattern criteria:
    - Occurs 3+ times
    - Has consistent characteristics
    - Suggests actionable improvement
    """
    patterns = []
    
    # Group by similarity
    grouped = cluster_by_similarity(observations)
    
    for group in grouped:
        if len(group) >= 3:
            pattern = Pattern(
                observations=group,
                frequency=len(group),
                category=categorize(group),
                suggested_action=derive_action(group)
            )
            patterns.append(pattern)
    
    return patterns
```

### Step 3: Generalization

Propose general rules from specific patterns:

```yaml
generalization_process:
  1_identify_commonality:
    question: "What do all instances share?"
    output: "Common characteristics"
  
  2_abstract_to_rule:
    question: "What general rule would prevent/encourage this?"
    output: "Proposed rule statement"
  
  3_trace_to_axiom:
    question: "Which axiom does this support?"
    output: "Axiom alignment justification"
  
  4_validate_consistency:
    question: "Does this contradict any existing rule?"
    output: "Consistency check result"
```

### Step 4: Proposal Generation

Create improvement proposals:

```markdown

```yaml
observation_sources:
  code_reviews:
    - common_issues_found
    - frequently_applied_fixes
    - quality_improvements
  
  test_results:
    - recurring_failure_patterns
    - coverage_gaps
    - performance_regressions
  
  user_interactions:
    - clarification_requests
    - repeated_questions
    - confusion_points
  
  workflow_execution:
    - bottlenecks_identified
    - skipped_steps
    - time_spent_per_phase
```

```python
def identify_patterns(observations: List[Observation]) -> List[Pattern]:
    """
    Identify recurring patterns from observations.
    
    Pattern criteria:
    - Occurs 3+ times
    - Has consistent characteristics
    - Suggests actionable improvement
    """
    patterns = []
    
    # Group by similarity
    grouped = cluster_by_similarity(observations)
    
    for group in grouped:
        if len(group) >= 3:
            pattern = Pattern(
                observations=group,
                frequency=len(group),
                category=categorize(group),
                suggested_action=derive_action(group)
            )
            patterns.append(pattern)
    
    return patterns
```

```yaml
generalization_process:
  1_identify_commonality:
    question: "What do all instances share?"
    output: "Common characteristics"
  
  2_abstract_to_rule:
    question: "What general rule would prevent/encourage this?"
    output: "Proposed rule statement"
  
  3_trace_to_axiom:
    question: "Which axiom does this support?"
    output: "Axiom alignment justification"
  
  4_validate_consistency:
    question: "Does this contradict any existing rule?"
    output: "Consistency check result"
```

## Pattern Feedback Report
### Observed Pattern

**Category**: {category}
**Frequency**: {count} occurrences over {time_period}
**Impact**: {impact_assessment}

### Specific Observations

1. {observation_1}
2. {observation_2}
3. {observation_3}

### Proposed Improvement

**Type**: {New Rule | Rule Modification | Process Change}

**Proposed Rule**:
> {rule_statement}

**Axiom Alignment**:
- Supports: {axiom_id} - {axiom_name}
- Rationale: {why_this_supports_axiom}

**Consistency Check**:
- Conflicts with: {none | list_of_conflicts}
- Resolution: {how_to_resolve if conflicts exist}

### Recommended Action

{action_to_take}

### Validation Criteria

How to know if this improvement works:
- {measurable_criterion_1}
- {measurable_criterion_2}
```

### Step 5: Integration

When proposal is approved, integrate into the system:

```yaml
integration_targets:
  layer0_axiom:
    when: "Pattern reveals need for new foundational principle"
    how: "Add to optional-axioms.json, document rationale"
    validation: "Peer review, conflict check"
  
  layer2_principle:
    when: "Pattern suggests new quality standard or boundary"
    how: "Add to .cursorrules principles section"
    validation: "Trace to axiom, consistency check"
  
  layer3_methodology:
    when: "Pattern suggests process improvement"
    how: "Update methodology.yaml or ceremony definitions"
    validation: "Trial period, metric tracking"
  
  layer4_technical:
    when: "Pattern suggests code/tool improvement"
    how: "Update templates, knowledge files, or skills"
    validation: "Testing, code review"
```

```
### Step 5: Integration

When proposal is approved, integrate into the system:
```

## Example Patterns
### Example 1: Repeated Clarification Requests

```yaml
pattern:
  observation: "Users frequently ask for clarification on API error codes"
  frequency: 8 times in 2 weeks
  category: "transparency"

generalization:
  rule: "All API endpoints must return standardized error codes with descriptions"
  axiom: "A3 (Transparency) - reasoning must be explainable"

proposal:
  type: "New Quality Standard"
  statement: "QS_API_ERRORS: All API error responses must include error_code, message, and suggested_action"
  target: "Layer 2 - Principles"
```

### Example 2: Destructive Action Recovery

```yaml
pattern:
  observation: "Three incidents of accidental data deletion required recovery"
  frequency: 3 times in 1 month
  category: "safety"

generalization:
  rule: "Destructive operations must have automatic backup"
  axiom: "A4 (Non-Harm), A7 (Reversibility)"

proposal:
  type: "Principle Enhancement"
  statement: "EB_DESTRUCTIVE: All delete operations must create automatic backup with 30-day retention"
  target: "Layer 2 - Principles"
```

### Example 3: Sprint Velocity Pattern

```yaml
pattern:
  observation: "Velocity drops 40% in sprints with 3+ new features"
  frequency: 4 sprints observed
  category: "methodology"

generalization:
  rule: "Limit new features per sprint based on team capacity"
  axiom: "A2 (User Primacy) - sustainable pace serves users better"

proposal:
  type: "Methodology Adjustment"
  statement: "Limit new features to 2 per sprint; additional features require capacity review"
  target: "Layer 3 - Methodology (agile-scrum)"
```

```yaml
pattern:
  observation: "Users frequently ask for clarification on API error codes"
  frequency: 8 times in 2 weeks
  category: "transparency"

generalization:
  rule: "All API endpoints must return standardized error codes with descriptions"
  axiom: "A3 (Transparency) - reasoning must be explainable"

proposal:
  type: "New Quality Standard"
  statement: "QS_API_ERRORS: All API error responses must include error_code, message, and suggested_action"
  target: "Layer 2 - Principles"
```

```yaml
pattern:
  observation: "Three incidents of accidental data deletion required recovery"
  frequency: 3 times in 1 month
  category: "safety"

generalization:
  rule: "Destructive operations must have automatic backup"
  axiom: "A4 (Non-Harm), A7 (Reversibility)"

proposal:
  type: "Principle Enhancement"
  statement: "EB_DESTRUCTIVE: All delete operations must create automatic backup with 30-day retention"
  target: "Layer 2 - Principles"
```

```yaml
pattern:
  observation: "Velocity drops 40% in sprints with 3+ new features"
  frequency: 4 sprints observed
  category: "methodology"

generalization:
  rule: "Limit new features per sprint based on team capacity"
  axiom: "A2 (User Primacy) - sustainable pace serves users better"

proposal:
  type: "Methodology Adjustment"
  statement: "Limit new features to 2 per sprint; additional features require capacity review"
  target: "Layer 3 - Methodology (agile-scrum)"
```

## Outputs
1. **Pattern Feedback Report** - Documented analysis
2. **Improvement Proposal** - Actionable recommendation
3. **Integration PR** - Changes to appropriate layer
4. **Validation Plan** - How to measure success

## Integration Points
- **Input from**: All development activities, retrospectives, metrics
- **Reads**: All layer configurations, historical patterns
- **Outputs to**: Proposals for any layer (L0-L4)
- **Validation**: Human review required before integration

## Best Practices
1. **Require Evidence**: Minimum 3 observations before proposing pattern
2. **Trace to Axioms**: Every proposal must align with at least one axiom
3. **Check Consistency**: Validate no conflicts with existing rules
4. **Propose Incrementally**: Small changes, measure, iterate
5. **Document Rationale**: Explain why this improvement helps
6. **Include Rollback**: Define how to undo if improvement fails

## Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Patterns identified per month | 5+ | Count of validated patterns |
| Proposals accepted | 60%+ | Accepted / Proposed |
| Improvement impact | Positive | Before/after metrics |
| Time to integration | < 1 sprint | From proposal to implementation |

---

*This skill embodies our commitment to continuous improvement (A10) while maintaining the integrity of our foundational principles.*

## Prerequisites
> [!IMPORTANT]
> Requirements:
