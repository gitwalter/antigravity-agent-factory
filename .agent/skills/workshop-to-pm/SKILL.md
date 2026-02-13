---
description: Convert team workshop outputs to project management artifacts
name: workshop-to-pm
type: skill
---
# Workshop To Pm

Convert team workshop outputs to project management artifacts

Converts team workshop outputs into structured project management artifacts, transforming collaborative insights into actionable work items that teams can track and execute.

## Philosophy

> Workshop insights become actionable work items.

Team workshops generate rich insights about vision, stakeholders, values, and workflows. These insights should flow seamlessly into project management systems where they become epics, stories, labels, and definitions of done. This skill bridges the gap between collaborative discovery and structured execution, ensuring that workshop outputs don't get lost but instead seed the PM system with meaningful, team-aligned work.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Collect Workshop Outputs

Read from workshop artifacts and identify extractable content:

**Artifacts to Read:**

1. **TEAM_CHARTER.md** → Project mission and success criteria
   - Mission statement → Epic descriptions
   - Future Headlines → Epic titles
   - Stakeholder list → Labels/tags
   - Success criteria → Acceptance criteria

2. **Future Headlines** → Epic descriptions
   - Each headline becomes a potential epic
   - Extract themes and group related headlines

3. **Stakeholder Safari** → User personas for story templates
   - Stakeholder names → Labels/tags
   - Stakeholder needs → User story templates
   - Priority order → Label hierarchy

4. **ETHICS_FRAMEWORK.md** → Definition of Done items
   - Core values → Quality gates
   - Ethical boundaries → Definition of Done checklist
   - Decision-making principles → Story acceptance criteria

5. **Agent Assembly workflows** → Task templates
   - Agent roles → Story types
   - Workflow sequences → Task templates
   - Skill assignments → Story tags

**Collection Script:**

```
"I'll help you convert your workshop outputs into PM artifacts.

Let me scan your workshop artifacts:

📄 Reading TEAM_CHARTER.md...
   ✓ Found {N} Future Headlines
   ✓ Found {N} Stakeholders
   ✓ Found mission statement

📄 Reading ETHICS_FRAMEWORK.md...
   ✓ Found {N} core values
   ✓ Found {N} ethical boundaries
   ✓ Found decision-making principles

📄 Reading agent-roster.json...
   ✓ Found {N} agents
   ✓ Found {N} workflows

Would you like me to:
A) Convert all identified items
B) Review and select specific items
C) Customize the transformation rules

Which option do you prefer?"
```

**Validation:**

- Verify artifacts exist and are readable
- Check for required fields (mission, stakeholders, values)
- Identify any missing context that might affect transformation

### Step 2: Transform to PM Artifacts

Transform workshop outputs into PM system structures:

#### Transformation Rules

**For each Future Headline:**

```yaml
Workshop Output:
  headline: "Local news platform connects neighbors during crisis"
  
PM Artifact:
  type: epic
  title: "Local News Platform - Crisis Connection"
  description: "Build platform that connects neighbors during crisis events"
  acceptance_criteria:
    - "Platform enables real-time neighbor communication"
    - "Crisis events trigger automatic connection flows"
    - "Users can find and help nearby neighbors"
  linked_stakeholders: ["local-residents", "crisis-responders"]
```

**For each Stakeholder:**

```yaml
Workshop Output:
  stakeholder:
    name: "Local Residents"
    priority: 1
    needs: ["real-time updates", "trusted information", "community connection"]
    
PM Artifact:
  type: label
  name: "stakeholder:local-residents"
  color: "#4A90E2"  # Primary stakeholder color
  description: "Primary stakeholder - local residents seeking community connection"
  
  user_story_template:
    as_a: "local resident"
    i_want: "{capability}"
    so_that: "I can {benefit}"
```

**For Ethics Framework:**

```yaml
Workshop Output:
  ethics_framework:
    core_values: ["Privacy", "Transparency", "Accessibility"]
    boundaries: ["Never sell user data", "Never hide data usage"]
    principles: ["User consent required", "Open source when possible"]
    
PM Artifact:
  type: definition_of_done
  checklist:
    - "Privacy: User data encrypted and consent obtained"
    - "Transparency: Data usage clearly documented"
    - "Accessibility: WCAG 2.1 AA compliance verified"
    - "Ethical boundary: No user data sold"
    - "Ethical boundary: No hidden data usage"
  applies_to: ["all_stories", "all_epics"]
```

**For Agent Workflows:**

```yaml
Workshop Output:
  workflow:
    name: "Code Review Flow"
    agents: ["code-reviewer", "security-auditor"]
    steps: ["analyze", "review", "approve"]
    
PM Artifact:
  type: task_template
  name: "Code Review Task Template"
  description: "Standard code review workflow"
  tasks:
    - "Code Reviewer analyzes changes"
    - "Security Auditor checks vulnerabilities"
    - "Team lead approves"
  tags: ["code-review", "security"]
```

**Transformation Script:**

```
"Transforming workshop outputs into PM artifacts:

📦 Creating Epics from Future Headlines...
   ✓ Epic 1: {EPIC_TITLE} (from headline: {HEADLINE})
   ✓ Epic 2: {EPIC_TITLE} (from headline: {HEADLINE})
   ...

🏷️ Creating Labels from Stakeholders...
   ✓ Label: stakeholder:{STAKEHOLDER_NAME}
   ✓ Label: stakeholder:{STAKEHOLDER_NAME}
   ...

✅ Creating Definition of Done from Ethics Framework...
   ✓ Added {N} quality gates
   ✓ Added {N} ethical boundaries
   ...

📋 Creating Task Templates from Workflows...
   ✓ Template: {TEMPLATE_NAME}
   ...

Transformation complete! Ready to create in backend."
```

### Step 3: Create in Backend

Use configured backend adapter to create artifacts:

**Epic Creation:**

For each transformed epic:

**Backend Operation:** `createEpic`

**Parameters:**
```json
{
  "title": "{EPIC_TITLE}",
  "description": "{EPIC_DESCRIPTION}",
  "projectId": "{PROJECT_ID}",
  "labels": ["{STAKEHOLDER_LABEL_1}", "{STAKEHOLDER_LABEL_2}"],
  "acceptanceCriteria": [
    "{CRITERION_1}",
    "{CRITERION_2}"
  ]
}
```

**Label Creation:**

For each stakeholder label:

**Backend Operation:** `createLabel`

**Parameters:**
```json
{
  "name": "stakeholder:{STAKEHOLDER_NAME}",
  "color": "{COLOR_CODE}",
  "description": "{STAKEHOLDER_DESCRIPTION}",
  "projectId": "{PROJECT_ID}"
}
```

**Definition of Done Creation:**

**Backend Operation:** `createDefinitionOfDone`

**Parameters:**
```json
{
  "name": "Workshop Ethics Framework - Definition of Done",
  "checklist": [
    "{CHECKLIST_ITEM_1}",
    "{CHECKLIST_ITEM_2}"
  ],
  "projectId": "{PROJECT_ID}",
  "appliesTo": ["all_stories", "all_epics"]
}
```

**Task Template Creation:**

For each workflow template:

**Backend Operation:** `createTaskTemplate`

**Parameters:**
```json
{
  "name": "{TEMPLATE_NAME}",
  "description": "{TEMPLATE_DESCRIPTION}",
  "tasks": [
    {
      "title": "{TASK_TITLE}",
      "description": "{TASK_DESCRIPTION}",
      "tags": ["{TAG_1}", "{TAG_2}"]
    }
  ],
  "projectId": "{PROJECT_ID}"
}
```

**Creation Script:**

```
"Creating artifacts in {BACKEND_NAME}...

📦 Creating epics...
   ✓ Created EPIC-{ID}: {TITLE}
   ✓ Created EPIC-{ID}: {TITLE}
   ...

🏷️ Creating labels...
   ✓ Created label: stakeholder:{NAME}
   ✓ Created label: stakeholder:{NAME}
   ...

✅ Creating Definition of Done...
   ✓ Created DoD checklist with {N} items

📋 Creating task templates...
   ✓ Created template: {TEMPLATE_NAME}
   ...

All artifacts created successfully!"
```

### Step 4: Generate Report

Output summary of created artifacts with links:

**Report Format:**

```
✅ Workshop outputs successfully converted to PM artifacts!

## Summary

**Epics Created:** {COUNT}
{EPIC_LIST_WITH_LINKS}

**Labels Created:** {COUNT}
{LABEL_LIST}

**Definition of Done:** {LINK}
- {CHECKLIST_ITEM_COUNT} items
- Applies to: All stories and epics

**Task Templates:** {COUNT}
{TEMPLATE_LIST}

## Links

**PM Backend:** {BACKEND_URL}
**Project:** {PROJECT_NAME} ({PROJECT_ID})

## Next Steps

1. **Review epics** - Verify epic titles and descriptions match your vision
2. **Add stories** - Break down epics into user stories
3. **Assign labels** - Use stakeholder labels when creating stories
4. **Plan sprint** - Use epics to organize sprint planning
5. **Apply DoD** - Ensure Definition of Done is used in all stories

## Mapping Reference

Workshop Output → PM Artifact:
- Future Headlines → Epics
- Stakeholders → Labels
- Ethics Framework → Definition of Done
- Agent Workflows → Task Templates

Your workshop insights are now actionable work items!
```

## Example Transformations

### Example 1: Vision Quest → Epics

**Workshop Output (TEAM_CHARTER.md):**

```markdown

## Vision Headlines

- "Local news platform connects neighbors during crisis"
- "Community garden app helps urban residents grow food"
- "Neighborhood safety network reduces crime by 40%"

## Stakeholders (Priority Order)

1. Local Residents
2. Community Organizers
3. City Officials
```

**Transformed PM Artifacts:**

```yaml
Epics:
  - id: EPIC-101
    title: "Local News Platform - Crisis Connection"
    description: "Build platform that connects neighbors during crisis events"
    labels: ["stakeholder:local-residents", "stakeholder:community-organizers"]
    acceptance_criteria:
      - "Platform enables real-time neighbor communication"
      - "Crisis events trigger automatic connection flows"
  
  - id: EPIC-102
    title: "Community Garden App"
    description: "Help urban residents grow food through community gardens"
    labels: ["stakeholder:local-residents"]
  
  - id: EPIC-103
    title: "Neighborhood Safety Network"
    description: "Reduce crime by 40% through neighborhood safety network"
    labels: ["stakeholder:local-residents", "stakeholder:city-officials"]

Labels:
  - name: "stakeholder:local-residents"
    color: "#4A90E2"
    priority: 1
  
  - name: "stakeholder:community-organizers"
    color: "#7B68EE"
    priority: 2
  
  - name: "stakeholder:city-officials"
    color: "#20B2AA"
    priority: 3
```

### Example 2: Ethics Arena → Definition of Done

**Workshop Output (ETHICS_FRAMEWORK.md):**

```markdown

## Core Values (Ranked by Priority)

1. Privacy - 95 points
2. Transparency - 88 points
3. Accessibility - 82 points

## Ethical Boundaries

- We will never: Sell user data
- We will never: Hide data usage from users
- We will never: Exclude users due to accessibility barriers

## Decision-Making Principles

- When facing dilemmas about data, we prioritize user privacy
- All features must be accessible to users with disabilities
```

**Transformed PM Artifact:**

```yaml
Definition of Done:
  name: "Workshop Ethics Framework - Definition of Done"
  checklist:
    - "Privacy: User data encrypted and explicit consent obtained"
    - "Privacy: No user data sold or shared without consent"
    - "Transparency: Data usage clearly documented and visible to users"
    - "Transparency: No hidden data collection or usage"
    - "Accessibility: WCAG 2.1 AA compliance verified"
    - "Accessibility: Feature tested with screen readers"
    - "Accessibility: Keyboard navigation fully functional"
    - "Ethical boundary: No user data sold (non-negotiable)"
    - "Ethical boundary: No hidden data usage (non-negotiable)"
    - "Ethical boundary: No accessibility exclusions (non-negotiable)"
  applies_to: ["all_stories", "all_epics"]
```

### Example 3: Agent Assembly → Task Templates

**Workshop Output (agent-roster.json):**

```json
{
  "workflows": [
    {
      "name": "Feature Development Flow",
      "agents": ["code-reviewer", "test-generator", "documentation"],
      "steps": [
        "Code Reviewer analyzes changes",
        "Test Generator creates test suite",
        "Documentation updates user guides"
      ]
    }
  ]
}
```

**Transformed PM Artifact:**

```yaml
Task Template:
  name: "Feature Development Task Template"
  description: "Standard workflow for feature development"
  tasks:
    - title: "Code Review"
      description: "Code Reviewer analyzes changes against best practices"
      tags: ["code-review", "quality"]
    
    - title: "Test Generation"
      description: "Test Generator creates comprehensive test suite"
      tags: ["testing", "quality"]
    
    - title: "Documentation Update"
      description: "Documentation agent updates user guides"
      tags: ["documentation", "user-experience"]
  tags: ["feature-development", "standard-workflow"]
```

## Backend Mapping Table

Different PM backends may have different structures. This table shows how workshop outputs map to each backend:

| Workshop Output | Jira | Linear | GitHub Projects | Azure DevOps |
|----------------|------|--------|----------------|--------------|
| Future Headline | Epic | Epic | Milestone | Epic |
| Stakeholder | Label | Label | Label | Tag |
| Ethics Framework | Custom Field (DoD) | Template | Project Note | Definition of Done |
| Agent Workflow | Issue Template | Template | Issue Template | Work Item Template |
| Success Criteria | Epic Acceptance Criteria | Epic Success Criteria | Milestone Description | Epic Acceptance Criteria |

### Backend-Specific Transformations

**Jira:**

```yaml
Epic:
  type: "Epic"
  fields:
    summary: "{EPIC_TITLE}"
    description: "{EPIC_DESCRIPTION}"
    customfield_10011: "{EPIC_LABEL}"  # Epic Label
    labels: ["{STAKEHOLDER_LABEL}"]
    acceptance_criteria: "{ACCEPTANCE_CRITERIA}"

Definition of Done:
  type: "Custom Field"
  name: "Definition of Done"
  field_type: "Checkboxes"
  options: ["{CHECKLIST_ITEM_1}", "{CHECKLIST_ITEM_2}"]
```

**Linear:**

```yaml
Epic:
  type: "Epic"
  title: "{EPIC_TITLE}"
  description: "{EPIC_DESCRIPTION}"
  labels: ["{STAKEHOLDER_LABEL}"]
  success_criteria: "{ACCEPTANCE_CRITERIA}"

Definition of Done:
  type: "Template"
  name: "Workshop DoD"
  checklist: ["{CHECKLIST_ITEM_1}", "{CHECKLIST_ITEM_2}"]
```

**GitHub Projects:**

```yaml
Milestone:
  title: "{EPIC_TITLE}"
  description: "{EPIC_DESCRIPTION}"
  labels: ["{STAKEHOLDER_LABEL}"]
  due_date: null

Definition of Done:
  type: "Project Note"
  title: "Definition of Done"
  body: "- [ ] {CHECKLIST_ITEM_1}\n- [ ] {CHECKLIST_ITEM_2}"
```

**Azure DevOps:**

```yaml
Epic:
  type: "Epic"
  title: "{EPIC_TITLE}"
  description: "{EPIC_DESCRIPTION}"
  tags: ["{STAKEHOLDER_LABEL}"]
  acceptance_criteria: "{ACCEPTANCE_CRITERIA}"

Definition of Done:
  type: "Definition of Done"
  name: "Workshop DoD"
  checklist: ["{CHECKLIST_ITEM_1}", "{CHECKLIST_ITEM_2}"]
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `createEpic` | `workItems.createEpic` | Create epic from Future Headline |
| `createLabel` | `labels.createLabel` | Create label from Stakeholder |
| `createDefinitionOfDone` | `project.createDefinitionOfDone` | Create DoD from Ethics Framework |
| `createTaskTemplate` | `templates.createTaskTemplate` | Create template from workflow |
| `linkItems` | `workItems.linkItems` | Link epics to labels |

### Operation Details

**createEpic:**
- **Parameters:** `title` (required), `description`, `projectId` (required), `labels` (array), `acceptanceCriteria` (array)
- **Returns:** Epic object with ID, title, status, projectId, labels
- **Error Handling:** Validate projectId exists, title is non-empty, labels exist

**createLabel:**
- **Parameters:** `name` (required), `color` (optional), `description`, `projectId` (required)
- **Returns:** Label object with ID, name, color
- **Error Handling:** Validate name is unique, projectId exists

**createDefinitionOfDone:**
- **Parameters:** `name` (required), `checklist` (required, array), `projectId` (required), `appliesTo` (array)
- **Returns:** DoD object with ID, name, checklist
- **Error Handling:** Validate checklist is non-empty, projectId exists

**createTaskTemplate:**
- **Parameters:** `name` (required), `description`, `tasks` (required, array), `projectId` (required), `tags` (array)
- **Returns:** Template object with ID, name, tasks
- **Error Handling:** Validate tasks is non-empty, projectId exists

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Workshop artifacts missing | Ask user to provide artifacts or run workshop first |
| Artifact parsing fails | Show parsing errors, offer manual entry option |
| Epic creation fails | Continue with other artifacts, note which epics failed |
| Label creation fails | Continue with other artifacts, note which labels failed |
| DoD creation fails | Continue with other artifacts, note DoD skipped |
| Backend connection timeout | Retry once, then suggest checking credentials |
| Partial transformation | Show what succeeded, offer to retry failed items |
| Backend doesn't support feature | Use alternative approach (e.g., custom fields instead of DoD) |

## Integration with Other Skills

### Integration with team-workshop-onboarding Skill

When used after workshops:

```
"After completing your team workshops, I can convert the outputs
into PM artifacts:

- Future Headlines → Epics
- Stakeholders → Labels
- Ethics Framework → Definition of Done
- Agent Workflows → Task Templates

This seeds your PM system with meaningful, team-aligned work."
```

**Integration Points:**
- Runs after Workshop 1: Vision Quest (for epics and stakeholders)
- Runs after Workshop 2: Ethics Arena (for Definition of Done)
- Runs after Workshop 4: Agent Assembly (for task templates)
- Uses PM configuration from Workshop 3: Stack Safari

### Integration with pm-configuration Skill

PM configuration must exist:

```
"Before converting workshop outputs, ensure PM backend is configured.
If not configured, I'll guide you through pm-configuration first."
```

**Integration Points:**
- Requires PM backend configuration
- Uses project ID from PM configuration
- Respects backend type for transformation rules

### Integration with create-epic Skill

Epic creation uses same backend operations:

```
"When creating epics from Future Headlines, I use the same
create-epic operations, ensuring consistency across your PM system."
```

**Integration Points:**
- Uses same `createEpic` backend operation
- Follows same epic structure and validation
- Links epics to stakeholders via labels

### Integration with plan-sprint Skill

Converted epics inform sprint planning:

```
"After converting workshop outputs, you can use plan-sprint to:
1. Pull epics into sprints
2. Break epics into stories
3. Track epic progress across sprints"
```

**Integration Points:**
- Epics created here appear in sprint planning
- Stakeholder labels help prioritize stories
- Definition of Done applies to all sprint work

## Important Rules

1. **Preserve workshop intent** - Transformations should maintain the spirit and meaning of workshop outputs
2. **Validate before creating** - Check that artifacts exist and are readable before transformation
3. **Handle missing data gracefully** - If required fields are missing, ask user or use defaults
4. **Respect backend differences** - Different backends have different structures; adapt accordingly
5. **Link related artifacts** - Always link epics to stakeholder labels, stories to epics
6. **Provide clear feedback** - Show what was created, with links and summaries
7. **Allow customization** - Let users review and modify transformations before creating
8. **Support partial success** - If some artifacts fail to create, continue with others
9. **Document transformations** - Keep mapping of workshop output → PM artifact for reference
10. **Ground in purpose** - Connect all artifacts to project mission and stakeholder needs

## CLI Quick Reference

```bash
# Convert workshop outputs to PM artifacts
python cli/factory_cli.py --workshop-to-pm \
  --charter TEAM_CHARTER.md \
  --ethics ETHICS_FRAMEWORK.md \
  --project-id "PROJ-123"

# Review transformation before creating
python cli/factory_cli.py --workshop-to-pm \
  --charter TEAM_CHARTER.md \
  --preview-only

# Convert specific artifacts only
python cli/factory_cli.py --workshop-to-pm \
  --epics-only \
  --charter TEAM_CHARTER.md
```

## References

- `{directories.knowledge}/pm-metrics.json` - PM metrics definitions and tracking
- `{directories.knowledge}/workflow-patterns.json` - Workflow patterns for PM integration
- `{directories.knowledge}/team-dynamics.json` - Team dynamics and stakeholder patterns
- `{directories.knowledge}/workshop-facilitation.json` - Workshop facilitation patterns
- `{directories.skills}/team-workshop-onboarding/SKILL.md` - Team workshop onboarding skill
- `{directories.skills}/pm-configuration/SKILL.md` - PM configuration skill
- `{directories.skills}/pm/create-epic/SKILL.md` - Epic creation skill
- `{directories.patterns}/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface

---

*Generated by Cursor Agent Factory*
*Skill: workshop-to-pm v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.
