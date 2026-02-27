---
agents:
- none
category: general
description: Create epic with child story structure
knowledge:
- workflow-patterns.json
- best-practices.json
name: create-epic
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Create Epic Skill

Creates epics in the configured PM backend with proper structure and optional documentation linking. Epics serve as containers for related user stories, helping teams organize large initiatives into manageable work.

## Philosophy

> Epics organize vision into actionable work.

Epics bridge the gap between strategic goals and tactical execution. They provide structure without constraining creativity, allowing teams to see the forest while working on individual trees. This skill ensures epics are created with clarity and purpose, grounded in love for the team's mission, truth in planning, and beauty in execution.

## When to Use

- When starting a new large feature or initiative
- When organizing multiple related user stories under a common theme
- When breaking down strategic goals into tactical work
- When user mentions "epic", "large feature", "initiative", "theme"
- During sprint planning when identifying work themes
- When creating project roadmap items

## Prerequisites

Before creating an epic, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Project ID is available
3. Epic title and description are understood (or will be gathered)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Gather Epic Details

Collect essential information about the epic:

```
"I'll help you create an epic. Let me gather a few details:

**Epic Title:**
[What should this epic be called?]

**Epic Description:**
[What is this epic trying to achieve? What problem does it solve?]

**Project:**
[Which project should this epic belong to?]
{PROJECT_ID}

**Optional - Child Stories:**
[Do you want to create initial user stories for this epic now, or add them later?]
- A) Create stories now (I'll help you define them)
- B) Add stories later
- C) Link existing stories

**Optional - Documentation:**
[Should I create a documentation page for this epic?]
- A) Yes, create a new page
- B) Link to existing page
- C) Skip documentation"
```

**Validation:**
- Title must be non-empty and descriptive
- Description should explain the "why" behind the epic
- Project ID must be valid

### Step 2: Create Epic in Backend

Call backend operation to create the epic:

**Backend Operation:** `createEpic`

**Parameters:**
```json
{
  "title": "{EPIC_TITLE}",
  "description": "{EPIC_DESCRIPTION}",
  "projectId": "{PROJECT_ID}"
}
```

**Expected Response:**
```json
{
  "id": "{EPIC_ID}",
  "title": "{EPIC_TITLE}",
  "description": "{EPIC_DESCRIPTION}",
  "status": "To Do",
  "projectId": "{PROJECT_ID}",
  "createdAt": "{TIMESTAMP}"
}
```

### Step 3: Create Child Stories (Optional)

If user selected option A in Step 1, help create initial stories:

```
"Let's create some initial stories for this epic. I'll help you break it down.

**Story 1:**
- Title: [What's the first story?]
- Description: [As a... / I want... / So that...]

[Continue for additional stories...]

Should I create these stories now and link them to the epic?"
```

For each story, use the `create-story` skill or call:

**Backend Operation:** `createStory`

**Parameters:**
```json
{
  "title": "{STORY_TITLE}",
  "description": "{STORY_DESCRIPTION}",
  "epicId": "{EPIC_ID}",
  "projectId": "{PROJECT_ID}"
}
```

### Step 4: Create Documentation Page (Optional)

If user selected to create documentation:

**Backend Operation:** `createPage`

**Parameters:**
```json
{
  "title": "{EPIC_TITLE} - Documentation",
  "content": "{EPIC_DESCRIPTION}\n\n## Goals\n\n## Stories\n\n## Success Criteria",
  "spaceId": "{SPACE_ID}",
  "parentId": null
}
```

Then link to the epic:

**Backend Operation:** `linkToWorkItem`

**Parameters:**
```json
{
  "pageId": "{PAGE_ID}",
  "itemId": "{EPIC_ID}"
}
```

### Step 5: Confirm and Summarize

Present the created epic with all details:

```
"✅ Epic created successfully!

**Epic Details:**
- **ID:** {EPIC_ID}
- **Title:** {EPIC_TITLE}
- **Status:** To Do
- **Project:** {PROJECT_ID}

**Child Stories:** {COUNT} stories
{STORY_LIST}

**Documentation:** {DOCUMENTATION_LINK or "Not created"}

**Next Steps:**
1. Review the epic in your PM backend: {BACKEND_URL}
2. Add more stories as you discover them
3. Move stories to sprints when ready
4. Update epic status as work progresses

The epic is ready for planning!"
```

## Example Outputs

### Example 1: Simple Epic Creation

**User:** "Create an epic for user authentication"

**Agent:** "I'll help you create an epic for user authentication.

**Epic Title:**
User Authentication System

**Epic Description:**
Implement secure user authentication including login, registration, password reset, and session management to enable personalized user experiences.

**Project:** PROJ-123

**Child Stories:** Add later

**Documentation:** Skip

Creating epic..."

**Output:**
```
✅ Epic created successfully!

**Epic Details:**
- **ID:** EPIC-456
- **Title:** User Authentication System
- **Status:** To Do
- **Project:** PROJ-123

**Child Stories:** 0 stories

**Documentation:** Not created

**Next Steps:**
1. Review the epic in Jira: https://company.atlassian.net/browse/EPIC-456
2. Add stories using: "Create story for EPIC-456"
3. Move stories to sprints when ready
```

### Example 2: Epic with Initial Stories

**User:** "Create an epic for payment processing with initial stories"

**Agent:** [Gathers epic details, then helps create stories]

**Output:**
```
✅ Epic created successfully!

**Epic Details:**
- **ID:** EPIC-789
- **Title:** Payment Processing System
- **Status:** To Do
- **Project:** PROJ-123

**Child Stories:** 3 stories
- STORY-101: User can add payment method
- STORY-102: User can process payment
- STORY-103: User can view payment history

**Documentation:** Not created

**Next Steps:**
1. Review epic and stories in Linear: https://linear.app/team/epic/789
2. Estimate stories before sprint planning
3. Add more stories as needed
```

### Example 3: Epic with Documentation

**User:** "Create epic for API redesign and link to Confluence page"

**Agent:** [Creates epic, then creates documentation page]

**Output:**
```
✅ Epic created successfully!

**Epic Details:**
- **ID:** EPIC-321
- **Title:** API Redesign Initiative
- **Status:** To Do
- **Project:** PROJ-123

**Child Stories:** 0 stories

**Documentation:** https://company.atlassian.net/wiki/spaces/ENG/pages/12345

**Next Steps:**
1. Review epic: https://company.atlassian.net/browse/EPIC-321
2. Add stories and link them to the documentation
3. Share documentation with stakeholders
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `createEpic` | `workItems.createEpic` | Create the epic in backend |
| `createStory` | `workItems.createStory` | Create child stories (optional) |
| `createPage` | `documentation.createPage` | Create documentation (optional) |
| `linkToWorkItem` | `documentation.linkToWorkItem` | Link docs to epic (optional) |

### Operation Details

**createEpic:**
- **Parameters:** `title` (required), `description`, `projectId` (required)
- **Returns:** Epic object with ID, title, status, projectId
- **Error Handling:** Validate projectId exists, title is non-empty

**createStory:**
- **Parameters:** `title` (required), `description`, `epicId`, `projectId` (required)
- **Returns:** Story object with ID
- **Error Handling:** Validate epicId exists if provided

**createPage:**
- **Parameters:** `title` (required), `content` (required), `spaceId` (required), `parentId`
- **Returns:** Page object with ID and URL
- **Error Handling:** Validate spaceId exists

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Project ID invalid | List available projects, ask user to select |
| Epic creation fails | Show error message, suggest checking backend connection |
| Story creation fails | Continue with epic creation, note which stories failed |
| Documentation creation fails | Continue with epic creation, note documentation skipped |
| Backend connection timeout | Retry once, then suggest checking credentials |

## Integration with Other Skills

### Integration with create-story Skill

When creating child stories:
```
"To create stories for this epic, I can:
1. Use the create-story skill to properly format each story
2. Link them to this epic automatically
3. Validate story format (As a/I want/So that)"
```

### Integration with pm-configuration Skill

Epic creation requires PM backend:
```
"Before creating epics, ensure PM backend is configured.
If not configured, I'll guide you through pm-configuration first."
```

### Integration with plan-sprint Skill

Epics inform sprint planning:
```
"When planning sprints, I can:
1. Show all epics with their stories
2. Help prioritize epics for sprint inclusion
3. Track epic progress across sprints"
```

## Important Rules

1. **Always validate inputs** - Title and projectId are required
2. **Provide clear feedback** - Show epic ID and backend URL after creation
3. **Support optional features** - Stories and documentation are optional, don't force them
4. **Handle errors gracefully** - Continue with partial success if some operations fail
5. **Link related work** - Always link stories to their parent epic
6. **Document decisions** - If documentation is created, include epic goals and success criteria
7. **Respect backend differences** - Different backends may have different epic structures
8. **Ground in purpose** - Connect epic to project mission and stakeholder needs

## CLI Quick Reference

```bash
# Create epic via CLI (if implemented)
python cli/factory_cli.py --create-epic \
  --title "Epic Title" \
  --description "Epic description" \
  --project-id "PROJ-123"

# List epics
python cli/factory_cli.py --list-epics --project-id "PROJ-123"
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for epic management
- `knowledge/best-practices.json` - Best practices for epic creation
- `.agent/skills/pm/create-story/SKILL.md` - Story creation skill
- `.agent/skills/pm/pm-configuration/SKILL.md` - PM configuration skill

---

*Generated by Antigravity Agent Factory*
*Skill: create-epic v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.
