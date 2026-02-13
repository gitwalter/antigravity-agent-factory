---
name: create-task
description: Create implementation task from story or description
type: skill
knowledge: [pm-metrics.json, workflow-patterns.json]
---

# Create Task Skill

Create implementation tasks that represent specific work items for development.

## Philosophy

> "Tasks are the actionable units of work. Each task should be completable by one person in one day or less."

Tasks bridge the gap between user stories and actual code changes.

## When to Use

- When breaking down stories into implementation tasks
- When creating standalone development tasks
- When user says "create task", "add task", "break down story"
- During sprint planning or implementation

## Prerequisites

- PM system configured with backend
- Story context (optional but recommended)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Gather Task Information

Prompt for task details:

```
"Let's create a task.

1. What needs to be done? (brief title)
2. What's the context? (related story or feature)
3. Any specific requirements or constraints?

Or describe the work and I'll help structure it."
```

### Step 2: Define the Task

Structure the task:

```
Title: [Verb] [object] [context]
Example: "Add category filter dropdown to products page"

Description:
- What: Specific implementation details
- Why: Link to parent story/epic
- How: Technical approach (optional)
- Done when: Completion criteria
```

### Step 3: Add Technical Details

Include implementation guidance:

```
Technical Notes:
- Files to modify: [list of files]
- Dependencies: [any blockers or prerequisites]
- Testing: [how to verify completion]
```

### Step 4: Estimate Effort

Suggest task size:

```
Estimated effort:
- Hours: 2-4 hours
- Complexity: Low/Medium/High
- Risk: None/Low/Medium
```

### Step 5: Create in Backend

Use backend adapter to create:

```
Operation: createTask
Parameters:
  title: Task title
  description: Full task description
  storyId: Parent story ID (if applicable)
  assignee: Suggested assignee (optional)
  estimation: Hours or points
  labels: Technical labels
```

### Step 6: Confirm Creation

Report created task:

```
"Created task: {TASK_ID}

Title: {TITLE}
Parent: {STORY_ID} (if linked)
Status: To Do
Link: {BACKEND_URL}

Would you like to:
1. Add more details
2. Assign to someone
3. Create related tasks
4. Start working on it"
```

## Backend Operations

| Operation | Parameters | Returns |
|-----------|------------|---------|
| `createTask` | title, description, storyId, estimation | Task ID, URL |
| `assignItem` | taskId, assignee | Updated task |
| `updateStatus` | taskId, status | Updated task |
| `linkItems` | taskId, relatedIds, type | Confirmation |

## Example Output

**Created Task:**

```json
{
  "id": "TASK-456",
  "title": "Add category filter dropdown to products page",
  "description": "Implement a dropdown component that allows users to filter products by category.\n\nFiles to modify:\n- src/components/ProductFilter.tsx\n- src/hooks/useProductFilter.ts\n\nDone when:\n- Dropdown shows all available categories\n- Selecting a category filters the product list\n- Clear option resets the filter",
  "storyId": "STORY-123",
  "estimation": "3h",
  "status": "todo",
  "labels": ["frontend", "feature"]
}
```

## Task Templates

### Frontend Task
```
Title: [Component] - [Action]
Description:
- Component: [name]
- Changes: [list]
- Styling: [requirements]
- Testing: [approach]
```

### Backend Task
```
Title: [Endpoint/Service] - [Action]
Description:
- Endpoint: [path]
- Changes: [list]
- Database: [migrations needed]
- Testing: [approach]
```

### Bug Fix Task
```
Title: Fix - [issue description]
Description:
- Issue: [what's wrong]
- Root cause: [if known]
- Fix approach: [proposed solution]
- Testing: [how to verify]
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `create-story` | Tasks are children of stories |
| `estimate-task` | Get estimation for task |
| `run-standup` | Report task progress |
| `close-sprint` | Tasks contribute to velocity |

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Task too large | Suggest breaking into subtasks |
| Missing story | Offer to create standalone or link later |
| Backend error | Queue for retry, notify user |
| Duplicate detected | Show existing task, confirm creation |

## Important Rules

1. Tasks should be completable in < 1 day
2. Always include completion criteria
3. Link to parent story when possible
4. Use consistent naming conventions
5. Add technical labels for filtering


## Best Practices
Placeholder content for Best Practices.
