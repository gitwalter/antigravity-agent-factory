---
agents:
- none
category: general
description: Create user story from description with acceptance criteria
knowledge:
- pm-metrics.json
- workflow-patterns.json
name: create-story
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Create Story Skill

Create user stories following the "As a / I want / So that" format with acceptance criteria.

## Philosophy

> "Good user stories capture user needs, not implementation details."

Every story should articulate user value, be small enough to complete in a sprint, and have clear acceptance criteria.

## When to Use

- When creating new user stories from requirements
- When breaking down epics into implementable stories
- When user says "create story", "add user story", "new story"
- During sprint planning or backlog grooming

## Prerequisites

- PM system configured with backend
- Epic or backlog context (optional)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Gather Story Information

Prompt for story details:

```
"Let's create a user story.

1. Who is this for? (the persona/role)
2. What do they want to do? (the action)
3. Why do they want it? (the value)

Or provide a description and I'll help structure it."
```

### Step 2: Structure the Story

Format as standard user story:

```
As a [persona],
I want to [action],
So that [benefit/value].
```

### Step 3: Define Acceptance Criteria

Generate acceptance criteria using Given/When/Then:

```
Acceptance Criteria:

1. Given [context]
   When [action]
   Then [expected result]

2. Given [another context]
   When [action]
   Then [expected result]
```

### Step 4: Add Metadata

Add standard fields:
- Priority (P0-P3 or High/Medium/Low)
- Estimation (story points or t-shirt size)
- Labels/Tags
- Epic link (if applicable)

### Step 5: Create in Backend

Use backend adapter to create:

```
Operation: createStory
Parameters:
  title: "{persona} can {action}"
  description: Full user story format
  acceptanceCriteria: List of criteria
  priority: Determined priority
  estimation: Suggested estimate
  epicId: Parent epic ID (if provided)
```

### Step 6: Confirm Creation

Report created story with link:

```
"Created story: {STORY_ID}

Title: {TITLE}
Status: Ready for refinement
Link: {BACKEND_URL}

Would you like to:
1. Add more acceptance criteria
2. Link to an epic
3. Estimate this story
4. Create another story"
```

## Backend Operations

| Operation | Parameters | Returns |
|-----------|------------|---------|
| `createStory` | title, description, acceptanceCriteria, priority, epicId | Story ID, URL |
| `updateStatus` | storyId, status | Updated story |
| `addToSprint` | storyId, sprintId | Confirmation |

## Example Output

**Created Story:**

```json
{
  "id": "STORY-123",
  "title": "Customer can filter products by category",
  "description": "As a customer,\nI want to filter products by category,\nSo that I can quickly find what I'm looking for.",
  "acceptanceCriteria": [
    "Given I am on the products page, When I select a category filter, Then only products in that category are shown",
    "Given I have a category filter active, When I clear the filter, Then all products are shown again"
  ],
  "priority": "P2",
  "estimation": "3",
  "status": "ready",
  "epicId": "EPIC-45"
}
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `create-epic` | Stories can be linked to epics |
| `create-task` | Stories can be broken into tasks |
| `estimate-task` | Invoke for estimation |
| `plan-sprint` | Add story to sprint |

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Missing persona | Suggest common personas from project |
| Vague action | Ask clarifying questions |
| Backend error | Queue for retry, notify user |
| Missing epic | Offer to create standalone or select epic |

## Important Rules

1. Always use standard user story format
2. Include at least 2 acceptance criteria
3. Never create stories without user value statement
4. Link to epic when context is available
5. Suggest estimation but don't block on it


## Best Practices
Placeholder content for Best Practices.
