---
agents:
- none
category: chain
description: Guide users through selecting and configuring development methodology
  for agent system
knowledge:
- none
name: selecting-methodologies
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Methodology Selection

Guide users through selecting and configuring development methodology for agent system

# Methodology Selection Skill

## Overview

This skill handles **Phase 0.7 (Layer 3)** of the onboarding process, where users select and configure the development methodology for their agent system.

## Purpose

Guide users through selecting an appropriate development methodology that defines how work is organized, how agents coordinate, and what ceremonies/processes govern the project.

## Trigger

- After principles are defined (or skipped in Quick mode)
- User mentions "methodology", "agile", "scrum", "kanban", "process"
- Explicit request to configure development workflow

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Present Methodology Options

Based on project type and purpose, present options:

```
Let's define how your team works. Select a development methodology:

1. **Agile Scrum** [Recommended for: Product development, feature teams]
   - Sprint-based iterations
   - Defined roles (PO, Tech Lead, Developers, QA)
   - Ceremonies: Standups, Planning, Review, Retro

2. **Kanban** [Recommended for: Support, maintenance, ops]
   - Continuous flow with WIP limits
   - Pull-based work selection
   - Metrics: Lead time, cycle time, throughput

3. **Research & Development** [Recommended for: AI/ML, innovation, R&D]
   - Experiment-based approach
   - Knowledge mesh coordination
   - Focus on learning and discovery

4. **Enterprise Integration** [Recommended for: Large-scale, compliance-driven]
   - Formal architecture governance
   - Milestone-based delivery
   - Compliance and audit focus

Which methodology best fits your project?
```

### Step 2: Confirm Based on Purpose

Validate choice against purpose:

```
You selected: {methodology}
Your purpose: {mission_statement}
Your stakeholders: {stakeholders}

This methodology emphasizes:
- {key_characteristics}

Alignment check:
✓ Supports your mission by: {alignment_explanation}
✓ Serves your stakeholders through: {stakeholder_benefit}

Does this feel right for your project?
```

### Step 3: Customize Methodology

Based on team size and needs:

```
Let's customize {methodology} for your team.

Team size: [ ] 1-3  [ ] 4-6  [ ] 7-10  [ ] 10+

{If Agile Scrum}
Sprint length: [ ] 1 week  [ ] 2 weeks  [ ] 3 weeks
{End If}

{If Kanban}
WIP limits:
- In Progress: [3]
- Review: [2]
{End If}

{If R&D}
Exploration ratio: [70]% exploration, [30]% exploitation
{End If}
```

### Step 4: Agent Role Mapping

Map methodology roles to Cursor agents:

```
Based on {methodology}, here's how agents can support each role:

{If Agile Scrum}
| Role | Agent Support |
|------|--------------|
| Product Owner | Documentation agent for user stories |
| Tech Lead | Code reviewer agent for oversight |
| Developer | Test generator, code assistant |
| QA | Test generator, security audit |
{End If}

{If R&D}
| Role | Agent Support |
|------|--------------|
| Research Lead | Explorer agent for literature |
| Scientists | Documentation agent for findings |
| Engineers | Code reviewer, test generator |
| Data Scientists | Code templates for analysis |
{End If}
```

### Step 5: Generate Methodology Artifacts

Generate the methodology configuration:

```yaml
# {directories.workflows}/methodology.yaml
metadata:
  name: "{methodology_name}"
  pattern: "{coordination_pattern}"
  customized: true

configuration:
  team_size: {team_size}
  {methodology_specific_settings}

ceremonies:
  {adapted_ceremonies}

quality_gates:
  {quality_gates}

metrics:
  {metrics_to_track}
```

## Outputs

1. **Methodology Configuration** - `{directories.workflows}/methodology.yaml`
2. **Agent Role Mapping** - Recommendations for agent capabilities
3. **Ceremonies Schedule** - For project planning
4. **Metrics Dashboard Config** - What to track

## Methodology Templates

### Agile Scrum Defaults

```yaml
methodology: agile-scrum
ceremonies:
  daily_standup:
    enabled: true
    duration: 15_minutes
  sprint_planning:
    enabled: true
    sprint_length: 2_weeks
  sprint_review:
    enabled: true
  retrospective:
    enabled: true
quality_gates:
  peer_review: required
  test_coverage: 80%
```

### Kanban Defaults

```yaml
methodology: kanban
board:
  columns: [Backlog, Ready, In Progress, Review, Done]
  wip_limits:
    ready: 5
    in_progress: 3
    review: 2
metrics:
  lead_time: tracked
  cycle_time: tracked
  throughput: tracked
```

### R&D Defaults

```yaml
methodology: research-development
exploration_ratio: 70
ceremonies:
  research_seminars: weekly
  experiment_reviews: bi_weekly
  brainstorming: monthly
quality_gates:
  reproducibility: required
  peer_review: required
```

### Enterprise Defaults

```yaml
methodology: enterprise-integration
governance:
  architecture_review_board: weekly
  compliance_reviews: milestone_based
standards:
  architecture: TOGAF
  security: ISO_27001
```

## Integration Points

- **Input from**: Purpose definition, optional principles
- **Reads**: `{directories.patterns}/methodologies/*.json`
- **Outputs to**: `{directories.workflows}/methodology.yaml`, agent recommendations
- **Next phase**: Technical configuration (Phases 1-5)

## Recommendation Logic

```python
def recommend_methodology(project_type, team_size, purpose):
    if "AI" in project_type or "ML" in project_type or "research" in purpose.lower():
        return "research-development"
    elif team_size > 10 or "enterprise" in project_type.lower() or "compliance" in purpose.lower():
        return "enterprise-integration"
    elif "support" in purpose.lower() or "maintenance" in purpose.lower():
        return "kanban"
    else:
        return "agile-scrum"
```

## Best Practices

1. Recommend based on project type and purpose
2. Allow customization of team size and cadence
3. Map roles to agent capabilities
4. Show axiom alignment for chosen methodology
5. Generate complete, ready-to-use configuration

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
