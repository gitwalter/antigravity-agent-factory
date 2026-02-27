---
agents:
- none
category: chain
description: Interactive skill for reviewing, applying, and managing knowledge updates
knowledge:
- none
name: updating-knowledge
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Update Knowledge

Interactive skill for reviewing, applying, and managing knowledge updates

# Update Knowledge Skill

## Overview

This skill provides an interactive interface for reviewing available knowledge updates, previewing changes, applying updates, and managing rollbacks. It respects the knowledge evolution configuration set in settings.json.

## Purpose

Enable controlled, transparent knowledge evolution that:
- Shows available updates with changelogs
- Allows preview before applying
- Supports partial updates (select which to apply)
- Provides rollback capability
- Tracks update history

## Axiom Alignment

- **A1 (Verifiability)**: All updates verified against checksums
- **A3 (Transparency)**: Full changelog and source attribution
- **A7 (Reversibility)**: All updates can be rolled back
- **A10 (Learning)**: System evolves from trusted sources

## Trigger

This skill is activated when:
- User says "update knowledge", "check for updates", "refresh patterns"
- Startup notification shows available updates
- User requests "rollback knowledge" or "undo update"
- Scheduled update check runs (if configured)

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Check Configuration

Load and validate knowledge evolution settings:

```yaml
configuration_check:
  load_settings:
    file: {directories.config}/settings.json
    section: knowledge_evolution

  validate:
    - mode is valid (stability_first, awareness_hybrid, freshness_first, subscription)
    - sources are configured
    - credentials are available (if needed)

  apply_mode:
    stability_first:
      action: Only check, never auto-apply
      confirmation: Always required
    awareness_hybrid:
      action: Check and notify
      confirmation: Required before apply
    freshness_first:
      action: Check and auto-apply with backup
      confirmation: Only for breaking changes
    subscription:
      action: Check subscribed files only
      confirmation: Required
```

### Step 2: Fetch Available Updates

Query all configured sources for updates:

```yaml
fetch_updates:
  parallel_sources:
    - adapter: github
      enabled: ${sources.github_trending}
      action: Check tracked repositories using `get_latest_release` and `search_repositories`

    - adapter: pypi
      enabled: ${sources.package_registries}
      action: Check Python packages for updates

    - adapter: npm
      enabled: ${sources.package_registries}
      action: Check NPM packages for updates

    - adapter: official_docs
      enabled: ${sources.official_docs}
      action: Check documentation sources

    - adapter: community
      enabled: ${sources.community_curated}
      action: Check community sources

  aggregate:
    action: Combine all updates
    deduplicate: By target_file + source
    sort_by: priority (CRITICAL first)
```

### Step 3: Present Update Summary

Show user what updates are available:

```markdown

## Knowledge Updates Available

**Mode**: {knowledge_evolution.mode}
**Last Check**: {last_check_time}

### Critical Updates (Apply Immediately)

| File | Version | Source | Change |
|------|---------|--------|--------|
| langchain-patterns.json | 1.0.0 → 1.1.0 | GitHub langchain-ai/langchain | Security fix |

### High Priority Updates

| File | Version | Source | Change |
|------|---------|--------|--------|
| fastapi-patterns.json | 1.0.0 → 2.0.0 | GitHub tiangolo/fastapi | Breaking changes |
| nextjs-patterns.json | 1.0.0 → 1.2.0 | NPM next@14.1.0 | New features |

### Medium Priority Updates

| File | Version | Source | Change |
|------|---------|--------|--------|
| {more updates...} |

### Summary

- **Critical**: {count} updates
- **High**: {count} updates
- **Medium**: {count} updates
- **Low**: {count} updates
- **Total**: {total} updates available
```

### Step 4: Preview Changes

Allow user to preview specific updates:

```yaml
preview_options:
  show_diff:
    action: Show JSON diff for selected file
    format: Side-by-side comparison
    highlight: Added, changed, removed sections

  show_changelog:
    action: Show changelog entries
    include:
      - Version history
      - Change descriptions
      - Source links
      - Breaking change warnings

  show_impact:
    action: Analyze impact on project
    check:
      - Affected blueprints
      - Affected skills
      - Affected templates
```

### Step 5: Apply Updates

Apply selected or all updates:

```yaml
apply_updates:
  pre_apply:
    - Create backup of current files
    - Validate update checksums
    - Check for conflicts

  apply_options:
    all:
      action: Apply all updates
      confirm: "Apply {count} updates?"

    selected:
      action: Apply user-selected updates
      prompt: "Select updates to apply"

    by_priority:
      action: Apply updates above threshold
      prompt: "Apply CRITICAL and HIGH priority? (y/n)"

    by_file:
      action: Apply updates to specific file
      prompt: "Which file to update?"

  apply_process:
    1_backup:
      action: Create timestamped backup
      path: {directories.knowledge}/backups/{filename}.{timestamp}.json

    2_merge:
      action: Apply changes using merge strategy
      strategies:
        conservative: Only add, never modify
        balanced: Add and update, preserve custom
        aggressive: Full replacement

    3_validate:
      action: Validate merged content against schema
      on_error: Rollback and report

    4_update_manifest:
      action: Update manifest.json with new versions
      record: timestamp, source, changes
```

### Step 6: Rollback (If Needed)

Support rolling back updates:

```yaml
rollback_options:
  list_backups:
    action: Show available backups
    display:
      - Filename
      - Backup timestamp
      - Version before backup
      - Changes that were applied

  rollback_file:
    action: Rollback specific file
    process:
      1: Select backup to restore
      2: Confirm rollback
      3: Restore file from backup
      4: Update manifest

  rollback_batch:
    action: Rollback entire update batch
    process:
      1: Select batch timestamp
      2: Confirm rollback
      3: Restore all files in batch
      4: Update manifest
```

## Update Report Format

After applying updates:

```markdown

## Knowledge Update Report

**Timestamp**: {datetime}
**Mode**: {mode}

### Applied Updates

| File | Previous | New | Status |
|------|----------|-----|--------|
| fastapi-patterns.json | 1.0.0 | 2.0.0 | ✅ Applied |
| langchain-patterns.json | 1.0.0 | 1.1.0 | ✅ Applied |
| nextjs-patterns.json | 1.0.0 | 1.2.0 | ⚠️ Conflicts (merged) |

### Backup Created

- Location: `{directories.knowledge}/backups/`
- Files backed up: {count}
- Retention: {max_backups} versions

### Next Steps

1. Review applied changes in knowledge files
2. Test affected blueprints and skills
3. Rollback if issues: `update-knowledge rollback`

### Skipped Updates

| File | Reason |
|------|--------|
| {file} | User declined |
| {file} | Locked in manifest |
```

## Commands

The skill supports these commands:

| Command | Action |
|---------|--------|
| `update-knowledge check` | Check for available updates |
| `update-knowledge apply` | Apply pending updates |
| `update-knowledge preview <file>` | Preview changes to file |
| `update-knowledge rollback` | Rollback recent updates |
| `update-knowledge history` | Show update history |
| `update-knowledge status` | Show current knowledge status |

## Important Rules

1. **Always backup first** - Never apply without backup
2. **Respect mode** - Honor configured update mode
3. **Verify checksums** - Validate update integrity
4. **Preserve custom** - Don't overwrite user customizations
5. **Document everything** - Full changelog and source tracking

## Error Handling

| Error | Resolution |
|-------|------------|
| Source unavailable | Skip source, continue with others |
| Checksum mismatch | Reject update, report error |
| Merge conflict | Use conservative merge, flag for review |
| Schema validation failed | Rollback, report specific errors |
| Backup failed | Abort update, preserve current state |

## Success Criteria

Update process is successful when:
- [ ] All selected updates applied without errors
- [ ] Backups created for all changed files
- [ ] Manifest updated with new versions
- [ ] No schema validation errors
- [ ] User receives clear summary

## Related Skills

- `system-configuration` - Configures update behavior
- `pattern-feedback` - Generates feedback for improvements
- `grounding-verification` - Verifies knowledge accuracy

---

*This skill ensures controlled, transparent, and reversible knowledge evolution.*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.
