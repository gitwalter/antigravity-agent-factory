---
description: Guide users through selecting practices that maintain excellence, alignment,
  and continuous improvement
name: selecting-practices
type: skill
---
# Practice Selection

Guide users through selecting practices that maintain excellence, alignment, and continuous improvement

# Practice Selection Skill

## Overview

This skill guides users through selecting practices (regular disciplines) that will maintain excellence, alignment, and continuous improvement.

## Philosophy

> Excellence emerges from consistent, intentional practice.
> "Soli Deo Gloria" - J.S. Bach (inscribed on his works)

Like Bach who praised through the excellence of his craft, we express our values through the quality and intentionality of our daily work. Practices are the rhythms that keep us aligned with our purpose.

## Purpose

Help users select practices that fit their team culture and methodology, ensuring regular moments of reflection, learning, and alignment.

## Trigger

- During onboarding after methodology is selected
- User mentions "practices", "rituals", "habits", "ceremonies"
- Request to configure team routines

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Explain Practice Philosophy

```
Practices are the regular disciplines that maintain excellence.

They are not bureaucracy - they are:
- Moments of intentional reflection
- Opportunities for continuous improvement
- Rhythms that keep us aligned with purpose

"Each day is an opportunity to serve well and grow in craft."

The best teams have practices so natural they feel like breathing.
```

### Step 2: Present Practice Categories

```
Select practices that fit your team:

DAILY PRACTICES (Personal & Team Rhythm)
[ ] P1: Morning Intention Setting - Start with clarity
[ ] P2: Evening Reflection - End with learning
[x] P3: Focused Stand-up - Align and unblock

CRAFT PRACTICES (Quality of Work)
[x] P4: Code as Craft Review - Excellence per commit
[x] P5: Thoughtful Code Review - Collaborative refinement
[ ] P6: Continuous Refactoring - Leave things better

ALIGNMENT PRACTICES (Purpose & Growth)
[ ] P7: Weekly Learning Session - Grow together
[x] P8: Sprint Retrospective - Improve continuously
[ ] P9: Release Blessing - Mark completion with intention
[ ] P10: Quarterly Purpose Alignment - Stay true to mission

Recommended minimum: P3, P4, P5, P8
Full excellence: All practices
```

### Step 3: Customize Practices

For each selected practice, customize to team needs:

```
P3 - Focused Stand-up:
  Time: [9:00 AM]
  Duration: [15 minutes]
  Format: [Progress, Focus, Blockers, Offers]

P4 - Code as Craft Review:
  Checklist enabled: [yes]
  Commit message format: [Conventional Commits]

P8 - Sprint Retrospective:
  Duration: [1 hour]
  Format: [Start/Stop/Continue]
  Include purpose check: [yes]
```

### Step 4: Map Practices to Methodology

Align practices with selected methodology:

```
Your methodology: Agile Scrum

Methodology ceremonies already include:
✓ Daily Stand-up (similar to P3)
✓ Sprint Retrospective (P8)

Additional practices to enhance:
+ P4: Code as Craft Review - Per commit quality
+ P5: Thoughtful Code Review - Collaborative refinement
+ P9: Release Blessing - Mark sprint completion

Consider adding:
~ P7: Weekly Learning Session - Continuous growth
~ P10: Quarterly Alignment - Purpose check
```

### Step 5: Generate Practice Configuration

```yaml
# practices.yaml - Team practices configuration

practices:
  daily:
    P3_focused_standup:
      enabled: true
      time: "09:00"
      duration: "15 minutes"
      format:
        - "Progress since yesterday"
        - "Focus for today"
        - "Blockers"
        - "Offers of help"
      reflection_prompt: "Is the team moving toward our success criteria?"

  per_commit:
    P4_code_as_craft:
      enabled: true
      checklist:
        - "Code is self-documenting"
        - "Tests cover new functionality"
        - "No unnecessary complexity"
        - "Commit message explains intent"

  per_task:
    P5_thoughtful_review:
      enabled: true
      dimensions:
        - "Correctness"
        - "Clarity"
        - "Completeness"
        - "Consistency"
        - "Craft"

  per_sprint:
    P8_retrospective:
      enabled: true
      duration: "1 hour"
      format: "start_stop_continue"
      include_purpose_check: true
      reflection_prompts:
        - "Did we serve our stakeholders well?"
        - "Did we maintain our quality standards?"
        - "Are we proud of what we delivered?"

  per_release:
    P9_release_blessing:
      enabled: true
      checklist:
        - "All tests passing"
        - "Security scan clean"
        - "Documentation updated"
        - "Stakeholders informed"
      acknowledgment: true
      lessons_capture: true
```

## Outputs

1. **Practice Configuration** - `practices.yaml` for generated project
2. **Practice Guide** - Documentation for team reference
3. **Calendar Integration** - Suggested recurring events

## Sample Practice Guide Output

```markdown
# Team Practices Guide

## Our Philosophy

We express our values through the quality and intentionality of our work.
These practices are rhythms that keep us aligned with our purpose.

## Daily Rhythm

### 9:00 AM - Focused Stand-up (15 min)
Share: Progress, Focus, Blockers, Offers
Ask yourself: "Is the team moving toward our success criteria?"

## Per Commit

### Code as Craft Review
Before each commit:
- [ ] Code is self-documenting
- [ ] Tests cover new functionality
- [ ] No unnecessary complexity
- [ ] Commit message explains intent

Ask yourself: "Would I be proud to show this to a mentor?"

## Per Sprint

### Retrospective (1 hour)
Format: Start / Stop / Continue
Always include: Purpose alignment check

Ask: "Did we serve our stakeholders well this sprint?"
```

## Integration Points

- **Input from**: Methodology selection, team size
- **Reads**: `{directories.patterns}/practices/*.json`
- **Outputs to**: `practices.yaml`, practice guide, calendar suggestions
- **Related**: `enforcement-selection` skill

## Best Practices

1. Start with core practices (P3, P4, P5, P8)
2. Add practices gradually as team matures
3. Keep practices lightweight - they should energize, not burden
4. Include reflection prompts to maintain intentionality
5. Review practice effectiveness in retrospectives
6. Adapt practices to team culture, not the other way around

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
