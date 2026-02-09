---
description: Create and extend workflow definitions using the workflow system architecture
---

# Extend Workflow

Create and extend workflow definitions using the workflow system architecture

## 
# Extend Workflow Skill

Create, extend, and manage workflow definitions using the Factory's workflow system architecture:
- **Workflow Creation**: Build new workflows from patterns
- **Workflow Extension**: Enhance existing workflows with new phases
- **Integration Design**: Configure MCP servers and skills for workflows
- **Schema Validation**: Ensure workflows conform to the schema

## 
# Extend Workflow Skill

Create, extend, and manage workflow definitions using the Factory's workflow system architecture:
- **Workflow Creation**: Build new workflows from patterns
- **Workflow Extension**: Enhance existing workflows with new phases
- **Integration Design**: Configure MCP servers and skills for workflows
- **Schema Validation**: Ensure workflows conform to the schema

## Artifacts Used
| Artifact | Path | Purpose |
|----------|------|---------|
| Workflow Template | `templates/workflows/workflow.md.tmpl` | Markdown structure for workflows |
| Workflow Schema | `knowledge/schemas/workflow-schema.json` | Validation rules |
| Workflow Entities | `knowledge/workflow-entities.json` | Entity definitions |
| Workflow Patterns | `knowledge/workflow-patterns.json` | Common patterns |
| MCP Catalog | `knowledge/mcp-servers-catalog.json` | Available tools |
| Skill Catalog | `knowledge/skill-catalog.json` | Available skills |

## Core Concepts
### Workflow System Architecture

Workflows follow the entity model defined in `knowledge/workflow-entities.json`:

```
Workflow
├── Phases (ordered groups of steps)
│   ├── Steps (atomic operations)
│   │   ├── Skills (reusable capabilities)
│   │   ├── MCP Servers (external tools)
│   │   └── Knowledge (reference data)
│   └── Decision Points (branching logic)
├── State Machine (lifecycle management)
├── Learning Hooks (continuous improvement)
└── Outputs (artifacts produced)
```

### Workflow Lifecycle States

| State | Description |
|-------|-------------|
| `draft` | Being designed, not executable |
| `active` | Ready for execution |
| `executing` | Currently running |
| `paused` | Awaiting input or resources |
| `completed` | Successfully finished |
| `failed` | Terminated with errors |
| `learning` | Post-execution analysis |

```
Workflow
├── Phases (ordered groups of steps)
│   ├── Steps (atomic operations)
│   │   ├── Skills (reusable capabilities)
│   │   ├── MCP Servers (external tools)
│   │   └── Knowledge (reference data)
│   └── Decision Points (branching logic)
├── State Machine (lifecycle management)
├── Learning Hooks (continuous improvement)
└── Outputs (artifacts produced)
```

## Research Methods
### Method 1: Pattern-Based Creation

Use when: Creating workflow from known patterns

**Steps**:
1. Read existing patterns: `knowledge/workflow-patterns.json`
2. Select applicable pattern (bugfix, feature, code-review, etc.)
3. Customize for specific use case
4. Add project-specific skills and tools

### Method 2: Research-Driven Creation

Use when: Creating workflow for new domain

**Tools**: `web_search`, `read_file`

```
Step 1: web_search("{{domain}} workflow best practices 2026")
Step 2: web_search("{{domain}} automation patterns")
Step 3: Synthesize into workflow structure
```

### Method 3: Existing Workflow Extension

Use when: Enhancing an existing workflow

**Tools**: `read_file`, `search_replace`

```
Step 1: read_file("workflows/{{existing-workflow}}.md")
Step 2: Identify extension points
Step 3: Add new phases/steps
Step 4: Update MCP tools and skills
```

```
Step 1: web_search("{{domain}} workflow best practices 2026")
Step 2: web_search("{{domain}} automation patterns")
Step 3: Synthesize into workflow structure
```

```
Step 1: read_file("workflows/{{existing-workflow}}.md")
Step 2: Identify extension points
Step 3: Add new phases/steps
Step 4: Update MCP tools and skills
```

## Creation Procedures
### Procedure A: Create New Workflow

**Trigger**: "Create workflow for {{purpose}}", "Add workflow that {{does_what}}"

**Steps**:

1. **Understand Requirements**
   ```
   → What problem does the workflow solve?
   → What are the inputs and outputs?
   → What tools and skills are needed?
   → What are the success criteria?
   ```

2. **Check Existing Patterns**
   ```
   read_file("knowledge/workflow-patterns.json")
   → Find similar patterns to use as base
   ```

3. **Read Workflow Schema**
   ```
   read_file("knowledge/schemas/workflow-schema.json")
   → Understand required structure
   ```

4. **Read Entity Definitions**
   ```
   read_file("knowledge/workflow-entities.json")
   → Understand entity relationships
   ```

5. **Identify Required MCP Servers**
   ```
   read_file("knowledge/mcp-servers-catalog.json")
   → Select tools needed for workflow steps
   ```

6. **Identify Required Skills**
   ```
   read_file("knowledge/skill-catalog.json")
   → Select skills for each step
   ```

7. **Design Workflow Structure**
   - Define phases (ordered groups)
   - Define steps within phases
   - Add decision points for branching
   - Configure escalation paths
   - Define learning hooks

8. **Read Template**
   ```
   read_file("templates/workflows/workflow.md.tmpl")
   → Get markdown structure
   ```

9. **Generate Workflow**
   ```
   write("workflows/{{workflow-name}}.md", content)
   ```

10. **Validate Structure**
    - Check all required sections present
    - Verify MCP tools exist in catalog
    - Verify skills exist in catalog
    - Ensure phases have clear outputs

**Output**: `workflows/{workflow-name}.md`

---

### Procedure B: Create Workflow from Pattern

**Trigger**: "Create {{pattern_type}} workflow for my project"

**Steps**:

1. **Load Pattern**
   ```
   read_file("knowledge/workflow-patterns.json")
   → Extract pattern: bugfix, feature, code-review, etc.
   ```

2. **Customize for Project**
   - Replace placeholders with project values
   - Add project-specific tools
   - Configure project-specific skills
   - Set project-specific outputs

3. **Generate Workflow**
   ```
   write("workflows/{{workflow-name}}.md", content)
   ```

**Output**: `workflows/{workflow-name}.md` (customized from pattern)

---

### Procedure C: Extend Existing Workflow

**Trigger**: "Add {{capability}} to {{workflow_name}}", "Extend workflow with {{feature}}"

**Steps**:

1. **Read Existing Workflow**
   ```
   read_file("workflows/{{workflow-name}}.md")
   → Understand current structure
   ```

2. **Identify Extension Points**
   - Which phase to add steps to?
   - Need new phase?
   - Need new decision points?

3. **Design Extension**
   - New steps with tools and skills
   - New decision logic
   - Updated outputs

4. **Apply Extension**
   ```
   search_replace("workflows/{{workflow-name}}.md", ...)
   ```

5. **Validate Extended Workflow**
   - Ensure flow is coherent
   - Verify all tools exist
   - Check for circular dependencies

**Output**: Updated `workflows/{workflow-name}.md`

---

### Procedure D: Create Agent-Specific Workflow

**Trigger**: "Create workflow for {{agent_name}} agent"

**Steps**:

1. **Understand Agent Purpose**
   ```
   read_file(".cursor/agents/{{agent-name}}.md")
   → Extract responsibilities and skills
   ```

2. **Map Agent Skills to Workflow Steps**
   - Each skill becomes potential workflow step
   - Identify orchestration needs
   - Define phase boundaries

3. **Design Workflow**
   - Structure around agent's decision process
   - Include escalation to human/other agents
   - Add learning hooks for improvement

4. **Generate Workflow**
   ```
   write("workflows/{{agent-name}}-workflow.md", content)
   ```

**Output**: `workflows/{agent-name}-workflow.md`

---

```
→ What problem does the workflow solve?
   → What are the inputs and outputs?
   → What tools and skills are needed?
   → What are the success criteria?
```

```
read_file("knowledge/workflow-patterns.json")
   → Find similar patterns to use as base
```

```
read_file("knowledge/schemas/workflow-schema.json")
   → Understand required structure
```

```
read_file("knowledge/workflow-entities.json")
   → Understand entity relationships
```

```
read_file("knowledge/mcp-servers-catalog.json")
   → Select tools needed for workflow steps
```

```
read_file("knowledge/skill-catalog.json")
   → Select skills for each step
```

```
read_file("templates/workflows/workflow.md.tmpl")
   → Get markdown structure
```

```
write("workflows/{{workflow-name}}.md", content)
```

```
read_file("knowledge/workflow-patterns.json")
   → Extract pattern: bugfix, feature, code-review, etc.
```

```
write("workflows/{{workflow-name}}.md", content)
```

```
read_file("workflows/{{workflow-name}}.md")
   → Understand current structure
```

```
search_replace("workflows/{{workflow-name}}.md", ...)
```

```
read_file(".cursor/agents/{{agent-name}}.md")
   → Extract responsibilities and skills
```

```
write("workflows/{{agent-name}}-workflow.md", content)
```

## Workflow Template Structure
```markdown
# {{Workflow Name}}

## Overview
{{Brief description of what this workflow accomplishes}}

**Project:** {{PROJECT_NAME}}
**Version:** {{VERSION}}
**Created:** {{DATE}}

## Trigger Conditions
{{When this workflow is activated}}

## Phases
### Phase 1: {{Phase Name}}
**Description:** {{What this phase accomplishes}}
**Entry Criteria:** {{When to enter this phase}}
**Exit Criteria:** {{When phase is complete}}

#### Step 1.1: {{Step Name}}
**Description:** {{What this step does}}
**Actions:**
- {{action 1}}
- {{action 2}}

**MCP Tools:**
- `{{server}}-{{tool}}`: {{purpose}}

**Skills:**
- `{{skill-name}}`: {{purpose}}

**Knowledge:**
- `{{knowledge-file}}`: {{purpose}}

**Outputs:**
- {{output 1}}
- {{output 2}}

**Is Mandatory:** Yes/No

---

## Decision Points
### Decision: {{Decision Name}}
**Condition:** {{What triggers this decision}}
**Options:**
| Condition | Next Phase | Rationale |
|-----------|------------|-----------|
| {{condition}} | {{phase}} | {{why}} |

---

## Escalation Paths
| Trigger | Action | Escalate To |
|---------|--------|-------------|
| {{trigger}} | {{action}} | {{target}} |

---

## Learning Hooks
| Hook Point | Capture | Use For |
|------------|---------|---------|
| {{when}} | {{what data}} | {{improvement}} |

---

## Output Artifacts
| Artifact | Location | Purpose |
|----------|----------|---------|
| {{name}} | {{path}} | {{purpose}} |

---

## Fallback Procedures
| Condition | Action |
|-----------|--------|
| {{issue}} | {{resolution}} |

---

## Related Artifacts
- **Agent**: {{agent if any}}
- **Skills**: {{list of skills}}
- **Knowledge**: {{list of knowledge files}}
```

## Chat Examples
### Example 1: Create Debugging Workflow
```
User: Create a workflow for debugging pipeline failures

Agent: I'll create a comprehensive debugging workflow.

[read_file("knowledge/workflow-patterns.json")] → Check existing patterns
[read_file("knowledge/mcp-servers-catalog.json")] → Available tools
[read_file("knowledge/skill-catalog.json")] → Available skills
[Designs workflow structure]
[write("workflows/operations/debug-pipeline.md", ...)]

Created: workflows/operations/debug-pipeline.md

Phases:
1. Error Detection - Parse logs, identify failure
2. Root Cause Analysis - Trace error origins
3. Resolution Strategy - Plan fix approach
4. Implementation - Apply fixes
5. Verification - Confirm resolution
6. Learning - Capture lessons learned

MCP Tools: github, sentry (if available)
Skills: pipeline-error-fix, tdd

Would you like me to create an agent to execute this workflow?
```

### Example 2: Extend Workflow with Learning
```
User: Add learning hooks to the TDD workflow

Agent: I'll extend the TDD workflow with learning capabilities.

[read_file("workflows/tdd-workflow.md")]
[read_file("knowledge/workflow-entities.json")] → Learning hook structure
[Designs learning extensions]
[search_replace("workflows/tdd-workflow.md", ...)]

Updated: workflows/tdd-workflow.md

Added Learning Hooks:
- After Phase 5 (Refactor): Capture refactoring patterns
- After Phase 7 (Integration): Capture test effectiveness metrics
- On failure: Capture failure patterns for future prevention

Would you like me to create a knowledge file to store learned patterns?
```

### Example 3: Create from Pattern
```
User: Create a bugfix workflow for my SAP project

Agent: I'll create a bugfix workflow customized for SAP.

[read_file("knowledge/workflow-patterns.json")] → bugfix pattern
[read_file("knowledge/sap-grounding-patterns.json")] → SAP-specific
[Customizes pattern for SAP]
[write("workflows/sap-bugfix-workflow.md", ...)]

Created: workflows/sap-bugfix-workflow.md

Customizations for SAP:
- Phase 1 uses SAP documentation MCP
- Grounding phase checks SAP data models
- Implementation follows RAP/ABAP patterns
- Testing uses SAP Unit framework

Tools: atlassian, SAP-documentation
Skills: grounding, bugfix-workflow, sap-development
```

```
User: Create a workflow for debugging pipeline failures

Agent: I'll create a comprehensive debugging workflow.

[read_file("knowledge/workflow-patterns.json")] → Check existing patterns
[read_file("knowledge/mcp-servers-catalog.json")] → Available tools
[read_file("knowledge/skill-catalog.json")] → Available skills
[Designs workflow structure]
[write("workflows/operations/debug-pipeline.md", ...)]

Created: workflows/operations/debug-pipeline.md

Phases:
1. Error Detection - Parse logs, identify failure
2. Root Cause Analysis - Trace error origins
3. Resolution Strategy - Plan fix approach
4. Implementation - Apply fixes
5. Verification - Confirm resolution
6. Learning - Capture lessons learned

MCP Tools: github, sentry (if available)
Skills: pipeline-error-fix, tdd

Would you like me to create an agent to execute this workflow?
```

```
User: Add learning hooks to the TDD workflow

Agent: I'll extend the TDD workflow with learning capabilities.

[read_file("workflows/tdd-workflow.md")]
[read_file("knowledge/workflow-entities.json")] → Learning hook structure
[Designs learning extensions]
[search_replace("workflows/tdd-workflow.md", ...)]

Updated: workflows/tdd-workflow.md

Added Learning Hooks:
- After Phase 5 (Refactor): Capture refactoring patterns
- After Phase 7 (Integration): Capture test effectiveness metrics
- On failure: Capture failure patterns for future prevention

Would you like me to create a knowledge file to store learned patterns?
```

```
User: Create a bugfix workflow for my SAP project

Agent: I'll create a bugfix workflow customized for SAP.

[read_file("knowledge/workflow-patterns.json")] → bugfix pattern
[read_file("knowledge/sap-grounding-patterns.json")] → SAP-specific
[Customizes pattern for SAP]
[write("workflows/sap-bugfix-workflow.md", ...)]

Created: workflows/sap-bugfix-workflow.md

Customizations for SAP:
- Phase 1 uses SAP documentation MCP
- Grounding phase checks SAP data models
- Implementation follows RAP/ABAP patterns
- Testing uses SAP Unit framework

Tools: atlassian, SAP-documentation
Skills: grounding, bugfix-workflow, sap-development
```

## Summary: What Gets Created
| Extension Type | Output Location | Format |
|----------------|-----------------|--------|
| Workflow | `workflows/{name}.md` | Markdown |
| Agent Workflow | `workflows/{agent}-workflow.md` | Markdown |
| Pattern-Based | `workflows/{pattern}-{project}.md` | Markdown |

## Post-Extension Automation (MANDATORY)
After creating or extending ANY workflow:

### Step 1: Update Manifest (if applicable)

If workflow adds new knowledge:
```
read_file("knowledge/manifest.json")
→ Update if new knowledge file created
```

### Step 2: Update Documentation

```
read_file("docs/reference/WORKFLOW_PATTERNS.md")
→ Add new workflow to catalog if reusable pattern
```

### Step 3: Update Changelog

```
read_file("CHANGELOG.md")
→ Add entry for new/extended workflow
```

### Step 4: Validate Workflow

- Check all referenced MCP tools exist
- Check all referenced skills exist
- Check all referenced knowledge files exist
- Validate phase/step structure

### Step 5: Git Operations (Ask User First)

**ALWAYS ask before git operations**:
```
⚠️ Ready to commit workflow changes:

Created/Modified: [list files]

Proposed commit: feat(workflow): {{description}}

Proceed? (yes/no/commit only)
```

```
read_file("knowledge/manifest.json")
→ Update if new knowledge file created
```

```
read_file("docs/reference/WORKFLOW_PATTERNS.md")
→ Add new workflow to catalog if reusable pattern
```

```
read_file("CHANGELOG.md")
→ Add entry for new/extended workflow
```

```
⚠️ Ready to commit workflow changes:

Created/Modified: [list files]

Proposed commit: feat(workflow): {{description}}

Proceed? (yes/no/commit only)
```

## Best Practices
- **Design workflows with clear entry and exit conditions**: Each phase should have explicit criteria for when it starts and when it's considered complete
- **Include error handling and rollback procedures**: Every workflow should define what happens when steps fail, including how to undo partial changes
- **Document workflow dependencies and requirements**: Clearly list all MCP servers, skills, and knowledge files needed before execution begins
- **Test workflows with representative data before deployment**: Validate workflows with sample inputs that match real-world scenarios to catch issues early
- **Design for observability**: Include learning hooks and decision points that capture metrics and outcomes for continuous improvement
- **Keep workflows focused and composable**: Each workflow should solve one specific problem; combine multiple workflows for complex processes rather than creating monolithic workflows

## Validation Checklist
### Workflows
- [ ] Has Overview section
- [ ] Has Trigger Conditions
- [ ] Has at least one Phase
- [ ] Each Phase has Steps
- [ ] Steps reference valid MCP tools
- [ ] Steps reference valid Skills
- [ ] Has Fallback Procedures
- [ ] Has Output Artifacts
- [ ] **Changelog entry added**

## Error Handling
| Issue | Resolution |
|-------|------------|
| Unknown MCP tool | Check catalog, suggest alternatives |
| Unknown skill | Check catalog, offer to create skill |
| Circular phases | Restructure workflow |
| Missing outputs | Add output definitions |
| No trigger conditions | Add activation triggers |

## Integration with Onboarding
When onboarding a project:
1. Analyze project type and requirements
2. Select applicable workflow patterns
3. Generate customized workflows for project
4. Include in generated `.cursor/` structure

## Integration with Generation
When generating a project:
1. Blueprint specifies workflow patterns
2. Generator creates `workflows/` directory
3. Customized workflows from patterns
4. Workflows reference project-specific tools/skills

## Related Artifacts
- **Agent**: `.cursor/agents/workflow-architect.md`
- **Templates**: `templates/workflows/*.tmpl`
- **Schema**: `knowledge/schemas/workflow-schema.json`
- **Entities**: `knowledge/workflow-entities.json`
- **Patterns**: `knowledge/workflow-patterns.json`
- **Documentation**: `docs/WORKFLOW_AUTHORING.md`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: workflow-entities.json, workflow-patterns.json, mcp-servers-catalog.json
