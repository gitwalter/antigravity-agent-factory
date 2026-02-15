---
description: Onboard existing repositories into the Cursor Agent Factory ecosystem
name: onboarding-flow
type: skill
---
# Onboarding Flow

Onboard existing repositories into the Cursor Agent Factory ecosystem

Integrate Cursor Agent Factory into existing repositories non-destructively, preserving existing artifacts while adding missing components.

## Philosophy

> Existing repositories have value. Our job is to enhance, not replace.

This skill enables seamless integration of the factory's agent system into repositories that already have code, configurations, and potentially some Cursor artifacts.

## Value Propagation Features

Every onboarded project receives layered capabilities that enable progressive autonomy:

**Layer 0: Foundation**
- `grounding-verification` skill: Two-pass verification for AI outputs
- Commands: "Verify this claim"

**Layer 1: Development Autonomy**
- `ci-monitor` skill: Continuous CI/CD monitoring
- `pipeline-error-fix` skill: Automatic error detection and fixing
- `debug-conductor` agent: Orchestrates debugging workflows
- Commands: "Monitor CI pipeline", "Fix pipeline errors", "Debug [issue]"

**Layer 2: Knowledge Independence**
- `knowledge-extender` agent: Add new knowledge independently
- `knowledge-evolution` agent: Track and manage knowledge
- Commands: "Extend knowledge for [topic]", "Check knowledge status"
- No Factory dependency - projects evolve independently

**Layer 3: PM Integration (Opt-In)**
- See Step 3.5 for PM setup options

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Gather Repository Information

Ask user for the repository path:

```
"Please provide the path to the repository you want to onboard.
For example: C:\Projects\my-existing-app"
```

Validate the path exists and is a directory.

### Step 2: Analyze Repository

Run the repository analyzer to detect existing artifacts:

```bash
python cli/factory_cli.py --analyze <repo_path>
```

**MCP Tools:** 
- **github**: Use `search_repositories` to verify remote existence.


Present the analysis results to user:
- Detected scenario (FRESH, MINIMAL, PARTIAL, UPGRADE, COMPLETE)
- Existing Cursor artifacts
- Detected technology stack
- Suggested blueprint

### Step 3: Confirm Blueprint Selection

Based on tech stack detection, suggest a blueprint:

```
"I detected the following:
- Languages: C#, TypeScript
- Frameworks: ASP.NET Core, React
- Suggested Blueprint: csharp-dotnet

Would you like to use this blueprint, or choose a different one?"
```

Available blueprints:
- `python-fastapi` - Python REST API development
- `typescript-react` - TypeScript web applications
- `java-spring` - Java enterprise applications
- `kotlin-spring` - Kotlin Spring applications
- `csharp-dotnet` - C#/.NET applications
- `sap-abap` - SAP ABAP development
- `sap-cpi-pi` - SAP CPI/PI integration

### Step 3.5: Project Management Setup (Optional)

After confirming the blueprint, offer PM system configuration:

```
"Would you like to set up project management for this repository?

This will add:
- PM agents (Product Owner, Sprint Master, Task Manager, Reporting)
- Integration with your issue tracker (GitHub, Jira, Azure DevOps, Linear)
- Sprint/Kanban workflow automation
- Metrics and reporting capabilities

Options:
1. [Yes] - Configure full project management
2. [Minimal] - Just issue tracking, no ceremonies
3. [No] - Skip for now (can add later with pm-configuration skill)"
```

If user selects "Yes" or "Minimal":
- Invoke the `pm-configuration` skill
- Merge PM artifacts into the generation preview
- Update the dry-run output to include PM files

If user selects "No":
- Acknowledge and continue to Step 4
- Note that PM can be added later using the `pm-configuration` skill

### Step 3.6: Tooling Setup (Optional)

After confirming the blueprint (and optionally PM), offer automation tooling:

```
"Would you like to set up automation tooling for this repository?

This can include:
- CI/CD pipelines (GitHub Actions)
- README structure validation and test catalog generation
- Pre-commit hooks with auto-sync
- Safe commit wrapper
- Secret scanning

Options:
1. [Essential] - CI pipeline, doc sync, .gitignore (recommended)
2. [Standard]  - Essential + git hooks, safe commit, CD pipeline
3. [Full]      - Standard + secret scanner, changelog generator
4. [Custom]    - Pick individual tools
5. [None]      - Skip for now (can add later via Factory updates)"
```

If user selects 1-3:
- Set `tooling_tier` accordingly in the generation config
- Continue to Step 4

If user selects 4 (Custom):
- Show the list of individual tools:
  - README validation, test catalog, CI workflow, PR checks, .gitignore
  - Pre-commit runner, install hooks, safe commit, CD workflow
  - Secret scanner, changelog generator
- Let user select by number
- Set `tooling_tier` to `custom` with selections

If user selects 5:
- Set `tooling_tier` to `none`
- Note that tooling can be added later using Factory updates
- Continue to Step 4

### Step 4: Preview Changes (Dry Run)

Before making any changes, show what will be modified:

```bash
python cli/factory_cli.py --onboard <repo_path> --blueprint <blueprint_id> --dry-run
```

Present the preview:
- Files that will be created
- Files that will be modified
- Conflicts that need resolution
- PM artifacts (if PM configuration was selected in Step 3.5)

### Step 5: Resolve Conflicts

For each conflict, ask user for resolution:

| Conflict Type | Options |
|---------------|---------|
| Existing agent with same name | Keep existing / Replace / Rename new |
| Existing .cursorrules | Merge / Replace / Keep existing |
| Existing knowledge file | Merge / Replace / Keep existing |
| Existing MCP config | Merge servers / Replace / Keep existing |

Default behavior: **Preserve existing** (ask for each conflict)

### Step 6: Execute Onboarding

With user confirmation, execute the onboarding:

```bash
python cli/factory_cli.py --onboard <repo_path> --blueprint <blueprint_id>
```

The process will:
1. Create backup of existing files
2. Generate missing directories
3. Add missing agents
4. Add missing skills
5. Merge or add .cursorrules sections
6. Add missing knowledge files
7. Generate workflow documentation and templates
8. Generate automation tooling scripts (based on tooling selection)
9. Generate CI/CD workflow configurations
10. Generate .gitignore
11. Generate PM configuration and agents (if PM was selected in Step 3.5)
12. Report results

### Step 7: Provide Summary and Next Steps

After completion, provide:

```
"Onboarding complete!

Summary:
- Scenario: PARTIAL
- Files created: 8
- Files merged: 2
- Skipped (preserved): 3
- Tooling tier: {TOOLING_TIER}
- PM configuration: Enabled (if PM was selected in Step 3.5)

A backup was created: .cursor-factory-backup/20260129_143022/

Next steps:
1. Review the merged .cursorrules file
2. Test the new agents by mentioning them
3. Check the {directories.knowledge}/ folder for new reference files
4. Review {directories.workflows}/ for available workflow templates
5. Run `python {directories.scripts}/git/install_hooks.py` to activate pre-commit hooks
6. Run `python {directories.scripts}/validation/validate_readme_structure.py --check` to verify README
7. Configure PM backend credentials (if PM was enabled)

If anything looks wrong, you can rollback:
python cli/factory_cli.py --rollback <repo_path>
"
```

## Scenario Handling

### FRESH Scenario (No Cursor artifacts)
- Full generation with all factory components
- Detect tech stack and suggest blueprint
- Create complete .cursor/ structure

### MINIMAL Scenario (Only .cursorrules)
- Augment with agents, skills, knowledge
- Merge new sections into existing .cursorrules
- Preserve user's custom rules

### PARTIAL Scenario (Some artifacts missing)
- Add only missing components
- Never overwrite existing agents/skills
- Offer to merge knowledge files

### UPGRADE Scenario (Old factory version)
- Show diff between old and new format
- Offer section-by-section upgrade
- Preserve user customizations

### COMPLETE Scenario (Fully configured)
- Report status
- Offer enhancements or updates
- No changes unless explicitly requested

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Path not found | Ask user to verify path |
| No write permission | Suggest running with admin rights |
| Unknown tech stack | Ask user to specify blueprint |
| Backup fails | Abort and report error |
| Conflict with no resolution | Skip artifact, report to user |

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `requirements-gathering` | Use if user wants to customize before onboarding |
| `stack-configuration` | Use if detected stack needs adjustment |
| `agent-generation` | Used for generating missing agents |
| `skill-generation` | Used for generating missing skills |
| `pm-configuration` | Invoked in Step 3.5 if user wants PM system setup |
| `team-workshop-onboarding` | Alternative for team onboarding with collaborative workshops |

## Team Onboarding Alternative

If a team (2+ people) is onboarding together, suggest the Team Workshop Onboarding:

```
"I notice you mentioned a team. Would you like to:

A) Individual Onboarding - I'll analyze and enhance your repo now
B) Team Workshop Series - Collaborative 5-workshop journey with games 
   and discussions that builds shared vision, ethics, and custom agents

The workshop series takes more time but creates deeper team alignment
and more customized results. It's grounded in Axiom 0: Love, Truth, and Beauty."
```

If they choose team workshops, hand off to `team-workshop-onboarding` skill.

## Important Rules

1. **Never overwrite without backup** - Always create backup before any modification
2. **Preserve user customizations** - Default to keeping existing content
3. **Ask for conflicts** - Don't make assumptions, ask user for each conflict
4. **Provide rollback path** - Always inform user how to undo changes
5. **Validate before acting** - Run dry-run first to preview changes
6. **Report completely** - Show summary of all actions taken
7. **Update CHANGELOG** - After any feature addition or modification, update CHANGELOG.md before committing

## CLI Quick Reference

```bash
# Analyze repository (no changes)
python cli/factory_cli.py --analyze C:\Projects\my-repo

# Preview onboarding (dry run)
python cli/factory_cli.py --onboard C:\Projects\my-repo --dry-run

# Onboard with auto-detected blueprint
python cli/factory_cli.py --onboard C:\Projects\my-repo

# Onboard with specific blueprint
python cli/factory_cli.py --onboard C:\Projects\my-repo --blueprint csharp-dotnet

# Rollback last onboarding
python cli/factory_cli.py --rollback C:\Projects\my-repo
```

## Example Conversation

**User:** "I have an existing C# project at C:\Projects\PaymentService that I want to enhance with Cursor agents"

**Agent:** "I'll analyze your repository to understand what's already configured.

*Running analysis...*

**Analysis Results:**
- Scenario: PARTIAL
- Existing: .cursorrules, 2 agents (code-reviewer, explorer)
- Missing: skills, knowledge files, templates
- Tech Stack: C# (.NET 8), ASP.NET Core
- Suggested Blueprint: csharp-dotnet

Would you like me to:
1. Show a preview of what will be added (dry run)
2. Proceed with onboarding using the csharp-dotnet blueprint
3. Choose a different blueprint

What would you prefer?"

**User:** "Proceed with onboarding"

**Agent:** "Great! Before I proceed, would you like to set up project management for this repository?

This will add:
- PM agents (Product Owner, Sprint Master, Task Manager, Reporting)
- Integration with your issue tracker (GitHub, Jira, Azure DevOps, Linear)
- Sprint/Kanban workflow automation
- Metrics and reporting capabilities

Options:
1. [Yes] - Configure full project management
2. [Minimal] - Just issue tracking, no ceremonies
3. [No] - Skip for now (can add later with pm-configuration skill)"

**User:** "Yes, let's set it up"

**Agent:** *Invokes pm-configuration skill, then proceeds with onboarding...*

**Agent:** "Onboarding complete!

Summary:
- Scenario: PARTIAL
- Files created: 12 (including PM agents and configuration)
- Files merged: 2
- Skipped (preserved): 3
- PM configuration: Enabled (Jira backend, Agile Scrum methodology)

Next steps:
1. Review the merged .cursorrules file
2. Test the new agents by mentioning them
3. Check the {directories.knowledge}/ folder for new reference files
4. Configure Jira credentials in .env.pm"

---

*Generated by Cursor Agent Factory*
*Skill: onboarding-flow v1.0.0*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.
