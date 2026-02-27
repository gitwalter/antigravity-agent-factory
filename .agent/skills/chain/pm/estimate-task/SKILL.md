---
agents:
- none
category: general
description: Suggest story point estimation
knowledge:
- workflow-patterns.json
- best-practices.json
name: estimate-task
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Estimate Task Skill

Suggests story point estimates by analyzing task complexity, dependencies, and risk. Applies estimates to work items (stories or tasks) in the PM backend to help teams plan and track velocity.

## Philosophy

> Estimation helps teams plan, not predict.

Story points estimate relative complexity, not absolute time. They help teams understand work size, plan capacity, and track velocity over time. This skill provides thoughtful estimation guidance grounded in love for team planning, truth in assessment, and beauty in collaboration.

## When to Use

- When estimating user stories or tasks
- During sprint planning when sizing work
- When user mentions "estimate", "story points", "sizing", "points"
- During backlog refinement sessions
- When reviewing work before sprint commitment
- When tracking team velocity

## Prerequisites

Before estimating, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Work item (story or task) exists
3. Item details are available for analysis

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Identify Item to Estimate

Determine what needs estimation:

```
"I'll help you estimate a work item. What would you like to estimate?

A) Specific item: {ITEM_ID or ITEM_TITLE}
B) Multiple items from backlog
C) Items in current sprint
D) All unestimated items in project

[If user selects A, fetch item details. Otherwise, list items for selection]"
```

### Step 2: Analyze Item Complexity

Gather information about the item:

**For Stories:**
```
"Let me analyze this story for estimation:

**Story:** {STORY_TITLE}
**Description:** {STORY_DESCRIPTION}

**Questions to consider:**
1. **Scope:** How much work is involved?
   - Small feature (1-2 endpoints/components)
   - Medium feature (3-5 endpoints/components)
   - Large feature (6+ endpoints/components)

2. **Complexity:** How complex is the implementation?
   - Straightforward (similar to existing code)
   - Moderate (some new patterns/concepts)
   - Complex (new architecture, significant research)

3. **Dependencies:** What dependencies exist?
   - None (can start immediately)
   - Some (waiting on 1-2 items)
   - Many (waiting on multiple items)

4. **Risk:** What's the risk level?
   - Low (well-understood, low uncertainty)
   - Medium (some unknowns, manageable)
   - High (significant unknowns, high uncertainty)

5. **Testing:** How much testing is needed?
   - Unit tests only
   - Unit + integration tests
   - Unit + integration + E2E tests

Based on these factors, I'll suggest a story point estimate."
```

**For Tasks:**
```
"Let me analyze this task for estimation:

**Task:** {TASK_TITLE}
**Description:** {TASK_DESCRIPTION}
**Type:** {TASK_TYPE}

**Estimation factors:**
- Scope and complexity
- Technical difficulty
- Dependencies and blockers
- Testing requirements
- Documentation needs

I'll suggest an estimate based on these factors."
```

### Step 3: Suggest Estimate

Provide estimation guidance:

**Estimation Framework:**

| Points | Complexity | Examples |
|--------|------------|----------|
| 1 | Trivial | Simple bug fix, minor text change |
| 2 | Simple | Small feature, straightforward implementation |
| 3 | Small | Standard feature, some complexity |
| 5 | Medium | Moderate feature, some unknowns |
| 8 | Large | Complex feature, multiple components |
| 13 | Very Large | Major feature, significant complexity |
| 21+ | Epic | Should be broken down |

**Estimation Logic:**

```python
def estimate_item(scope, complexity, dependencies, risk, testing):
    base_points = {
        "small": 2,
        "medium": 5,
        "large": 8
    }

    points = base_points[scope]

    # Adjust for complexity
    if complexity == "complex":
        points += 3
    elif complexity == "moderate":
        points += 1

    # Adjust for risk
    if risk == "high":
        points += 2
    elif risk == "medium":
        points += 1

    # Adjust for dependencies
    if dependencies == "many":
        points += 1

    # Adjust for testing
    if testing == "comprehensive":
        points += 1

    # Round to Fibonacci sequence
    return round_to_fibonacci(points)
```

**Present Estimate:**

```
"Based on my analysis, I suggest:

**Suggested Estimate:** {POINTS} story points

**Reasoning:**
- Scope: {SCOPE_ASSESSMENT} ({SCOPE_POINTS} points)
- Complexity: {COMPLEXITY_ASSESSMENT} ({COMPLEXITY_ADJUSTMENT})
- Risk: {RISK_ASSESSMENT} ({RISK_ADJUSTMENT})
- Dependencies: {DEPENDENCY_ASSESSMENT} ({DEPENDENCY_ADJUSTMENT})
- Testing: {TESTING_ASSESSMENT} ({TESTING_ADJUSTMENT})

**Estimation Range:** {MIN_POINTS} - {MAX_POINTS} points
(If team velocity suggests different, adjust accordingly)

Would you like to:
A) Apply this estimate ({POINTS} points)
B) Adjust estimate ({NEW_POINTS} points)
C) Skip estimation for now
D) Compare with similar items"
```

### Step 4: Compare with Similar Items (Optional)

If user wants comparison:

```
"Let me find similar items for comparison:

**Similar Items:**
- {ITEM_1}: {ESTIMATE} points (completed)
- {ITEM_2}: {ESTIMATE} points (completed)
- {ITEM_3}: {ESTIMATE} points (in progress)

**Average for similar items:** {AVG_POINTS} points

**Your item complexity vs. similar:**
- {COMPARISON_ASSESSMENT}

**Adjusted suggestion:** {ADJUSTED_POINTS} points
```

### Step 5: Apply Estimate

If user confirms, apply estimate to item:

**Backend Operation:** `updateStatus`

**Note:** Some backends use a dedicated `updateEstimate` operation. Check adapter interface.

**Parameters:**
```json
{
  "itemId": "{ITEM_ID}",
  "status": "{CURRENT_STATUS}", // preserve status
  "estimate": "{POINTS}" // add estimate field
}
```

**Alternative:** If backend supports direct estimate update:
```json
{
  "itemId": "{ITEM_ID}",
  "estimate": "{POINTS}"
}
```

### Step 6: Confirm and Summarize

Present the applied estimate:

```
"✅ Estimate applied successfully!

**Item:** {ITEM_TITLE}
**Estimate:** {POINTS} story points
**Previous Estimate:** {PREVIOUS_ESTIMATE or "None"}

**Estimation Notes:**
{REASONING_SUMMARY}

**Next Steps:**
1. Review estimate: {BACKEND_URL}
2. Use in sprint planning (team velocity: {VELOCITY} points/sprint)
3. Track actual vs. estimated after completion
4. Adjust future estimates based on learnings

Estimate is ready for planning!"
```

## Example Outputs

### Example 1: Story Estimation

**User:** "Estimate STORY-101"

**Agent:** "Let me analyze STORY-101 for estimation.

**Story:** User Authentication
**Description:** As a user, I want to log in with email and password, so that I can access my account.

**Analysis:**
- **Scope:** Medium (login endpoint, password validation, session management)
- **Complexity:** Moderate (standard auth patterns, some security considerations)
- **Dependencies:** None (can start immediately)
- **Risk:** Low (well-understood patterns)
- **Testing:** Comprehensive (unit + integration + security tests)

**Suggested Estimate:** 5 story points

**Reasoning:**
- Base scope: 5 points (medium feature)
- Complexity: +1 (moderate complexity)
- Risk: 0 (low risk)
- Dependencies: 0 (no dependencies)
- Testing: +1 (comprehensive testing)
- **Total:** 5 points

Would you like to apply this estimate?"

**Output:**
```
✅ Estimate applied successfully!

**Item:** User Authentication (STORY-101)
**Estimate:** 5 story points
**Previous Estimate:** None

**Estimation Notes:**
Medium scope feature with moderate complexity and comprehensive testing requirements.

**Next Steps:**
1. Review estimate: https://company.atlassian.net/browse/STORY-101
2. Use in sprint planning (team velocity: 20 points/sprint)
3. Track actual vs. estimated after completion
```

### Example 2: Task Estimation

**User:** "Estimate TASK-201: Implement payment gateway integration"

**Agent:** [Analyzes task, suggests estimate]

**Output:**
```
✅ Estimate applied successfully!

**Item:** Implement Payment Gateway Integration (TASK-201)
**Estimate:** 8 story points
**Previous Estimate:** None

**Estimation Notes:**
Large scope task with high complexity (external API integration), some risk (payment handling), and comprehensive testing needs.

**Next Steps:**
1. Review estimate: https://linear.app/team/task/201
2. Consider breaking into smaller tasks if too large
3. Track actual time vs. estimate
```

### Example 3: Estimation with Comparison

**User:** "Estimate STORY-102 and compare with similar stories"

**Agent:** [Analyzes story, finds similar items, compares]

**Output:**
```
**Similar Items Found:**
- STORY-045: User Profile View (3 points, completed)
- STORY-067: User Settings Update (5 points, completed)
- STORY-089: User Preferences (3 points, in progress)

**Average for similar items:** 3.7 points

**Your Story:** User Profile Edit
**Complexity vs. similar:** More complex (includes validation, image upload)

**Suggested Estimate:** 5 story points

✅ Estimate applied successfully!

**Item:** User Profile Edit (STORY-102)
**Estimate:** 5 story points
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `updateStatus` | `workItems.updateStatus` | Apply estimate (may include estimate field) |
| `getItem` | `workItems.getItem` | Fetch item details for analysis |
| `listItems` | `workItems.listItems` | Find similar items for comparison |

### Operation Details

**updateStatus (with estimate):**
- **Parameters:** `itemId` (required), `status` (preserve current), `estimate` (new field)
- **Returns:** Updated item with estimate
- **Error Handling:** Validate itemId exists, estimate is valid number

**getItem:**
- **Parameters:** `itemId` (required)
- **Returns:** Item details including current estimate
- **Error Handling:** Validate itemId exists

**listItems:**
- **Parameters:** `projectId`, `type`, `status` (for finding similar items)
- **Returns:** List of items with estimates
- **Error Handling:** Handle empty results gracefully

## Estimation Best Practices

### Fibonacci Sequence

Use Fibonacci sequence for story points:
1, 2, 3, 5, 8, 13, 21, 34, ...

**Why Fibonacci:**
- Reflects uncertainty (larger numbers have wider ranges)
- Prevents false precision
- Encourages breaking down large items

### Relative Sizing

Estimate relative to a baseline:
- **Baseline:** Pick a medium-complexity story as "5 points"
- **Compare:** Estimate other items relative to baseline
- **Calibrate:** Adjust baseline based on actuals

### Team Velocity

Track velocity to inform planning:
- **Velocity:** Average points completed per sprint
- **Use:** Plan sprint capacity based on velocity
- **Adjust:** Re-estimate if velocity changes significantly

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Item not found | List available items, ask user to select |
| Item details insufficient | Ask user for more context about scope/complexity |
| Estimate seems off | Ask user to reconsider, provide more context |
| Backend doesn't support estimates | Warn user, suggest using custom fields or comments |
| Similar items not found | Provide estimate without comparison |
| Team velocity unknown | Estimate without velocity context, suggest tracking velocity |

## Integration with Other Skills

### Integration with create-story Skill

After story creation:
```
"Would you like to estimate this story now?
I can help you assign story points using the estimate-task skill."
```

### Integration with plan-sprint Skill

Estimates inform sprint planning:
```
"When planning sprints, I can:
1. Show total estimated points for selected stories
2. Compare against team velocity
3. Warn if sprint is over/under capacity"
```

### Integration with close-sprint Skill

Estimates inform velocity calculation:
```
"When closing sprints, I can:
1. Compare estimated vs. actual points
2. Calculate team velocity
3. Identify estimation patterns for improvement"
```

## Important Rules

1. **Use Fibonacci sequence** - 1, 2, 3, 5, 8, 13, 21...
2. **Estimate relative complexity** - Not absolute time
3. **Consider all factors** - Scope, complexity, risk, dependencies, testing
4. **Provide reasoning** - Explain why estimate was chosen
5. **Support comparison** - Compare with similar completed items
6. **Respect team judgment** - Suggest, don't dictate
7. **Track and learn** - Use actuals to improve future estimates
8. **Ground in team velocity** - Consider team's historical performance

## CLI Quick Reference

```bash
# Estimate item via CLI (if implemented)
python cli/factory_cli.py --estimate-item \
  --item-id "STORY-101" \
  --points "5"

# List unestimated items
python cli/factory_cli.py --list-items --project-id "PROJ-123" --unestimated

# Compare estimates
python cli/factory_cli.py --compare-estimates --item-id "STORY-101"
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for estimation
- `knowledge/best-practices.json` - Best practices for story point estimation
- `.agent/skills/pm/create-story/SKILL.md` - Story creation skill
- `.agent/skills/pm/plan-sprint/SKILL.md` - Sprint planning skill
- `.agent/skills/pm/close-sprint/SKILL.md` - Sprint closure skill

---

*Generated by Antigravity Agent Factory*
*Skill: estimate-task v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.
