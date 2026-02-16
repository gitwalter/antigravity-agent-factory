---
description: On-demand version audits using version-registry.json as source of truth
name: checking-versions
type: skill
---
# Version Check

On-demand version audits using version-registry.json as source of truth

Performs on-demand version audits for packages, blueprints, and projects using `{directories.knowledge}/version-registry.json` as the authoritative source of truth for recommended versions.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Load Version Registry

Load and parse the version registry:

```yaml
load_registry:
  file: {directories.knowledge}/version-registry.json
  structure:
    packages:
      python: {package: version}
      javascript: {package: version}
      java: {package: version}
      dotnet: {package: version}
      rust: {package: version}
    llm_models:
      openai: {model_type: model_name}
      anthropic: {model_type: model_name}
      google: {model_type: model_name}
```

### Step 2: Parse Version Specifications

Handle different version formats:

```yaml
version_parsing:
  exact: "1.2.3" → exact match required
  range: "1.2+" → >= 1.2.0
  major: "2.x" → >= 2.0.0, < 3.0.0
  latest: "+" → use latest from registry
  caret: "^1.2.3" → >= 1.2.3, < 2.0.0
  tilde: "~1.2.3" → >= 1.2.3, < 1.3.0
```

### Step 3: Check Single Package Version

Compare a single package against registry:

```yaml
check_package:
  input:
    package_name: "fastapi"
    current_version: "0.128.0"
    language: "python"

  process:
    1_lookup:
      action: Find package in registry.packages.{language}
      registry_version: "0.128.4"

    2_compare:
      action: Compare versions
      current: "0.128.0"
      registry: "0.128.4"
      status: "outdated"
      difference: "patch"

    3_report:
      format: |
        Package: fastapi
        Current: 0.128.0
        Recommended: 0.128.4
        Status: ⚠️ Outdated (patch update available)
        Update: pip install fastapi==0.128.4
```

### Step 4: Audit Blueprint Dependencies

Check all dependencies in a blueprint:

```yaml
audit_blueprint:
  input:
    blueprint_file: "{directories.blueprints}/python-fastapi/blueprint.json"

  process:
    1_extract_dependencies:
      sources:
        - stack.frameworks[].version
        - stack.tools[].version
        - Any other version fields

    2_map_to_registry:
      for each dependency:
        - Match package name to registry
        - Compare versions
        - Flag mismatches

    3_generate_report:
      format: |
        ## Blueprint Version Audit: python-fastapi

        ### Frameworks
        | Package | Blueprint | Registry | Status |
        |---------|-----------|----------|--------|
        | FastAPI | 0.128+ | 0.128.4 | ✅ Compatible |
        | Pydantic | 2.10+ | 2.10.0 | ✅ Compatible |
        | SQLAlchemy | 2.0+ | (not in registry) | ⚠️ Not tracked |

        ### Tools
        | Package | Blueprint | Registry | Status |
        |---------|-----------|----------|--------|
        | uvicorn | 0.34+ | (not in registry) | ⚠️ Not tracked |

        ### Summary
        - ✅ Up to date: 2
        - ⚠️ Not tracked: 2
        - ❌ Outdated: 0
```

### Step 5: Find Outdated Packages in Project

Scan project dependency files:

```yaml
scan_project:
  input:
    project_root: "{PROJECT_ROOT}"
    dependency_files:
      python: ["requirements.txt", "pyproject.toml", "setup.py"]
      javascript: ["package.json", "package-lock.json"]
      java: ["pom.xml", "build.gradle"]
      dotnet: ["*.csproj", "packages.config"]
      rust: ["Cargo.toml"]

  process:
    1_identify_language:
      action: Detect from dependency files present

    2_parse_dependencies:
      action: Extract package names and versions
      tools:
        python: pip list, pip freeze, poetry show
        javascript: npm list, yarn list
        java: mvn dependency:tree, gradle dependencies
        dotnet: dotnet list package
        rust: cargo tree

    3_check_against_registry:
      action: Compare each package to registry
      filter: Only check packages in registry

    4_categorize:
      outdated:
        - Major version behind
        - Minor version behind
        - Patch version behind
      current:
        - Matches registry
        - Compatible with registry range
      unknown:
        - Not in registry
        - Cannot determine version

    5_generate_report:
      format: |
        ## Project Version Audit

        **Language**: Python
        **Registry Date**: 2026-02-08

        ### Outdated Packages

        | Package | Current | Recommended | Update Type | Priority |
        |---------|---------|-------------|-------------|----------|
        | fastapi | 0.128.0 | 0.128.4 | Patch | Low |
        | langchain | 1.2.5 | 1.2.9 | Patch | Medium |
        | pydantic | 2.9.0 | 2.10.0 | Minor | High |

        ### Current Packages

        | Package | Version | Status |
        |---------|---------|--------|
        | crewai | 1.9.3 | ✅ Current |
        | langgraph | 1.0.8 | ✅ Current |

        ### Not Tracked

        | Package | Version | Note |
        |---------|---------|------|
        | local-package | 1.0.0 | Custom package |

        ### Update Recommendations

        **High Priority** (Minor/Major updates):
        - pydantic: 2.9.0 → 2.10.0
          - Review: https://docs.pydantic.dev/latest/migration/
          - Breaking: None expected for patch
          - Action: `pip install --upgrade pydantic==2.10.0`

        **Medium Priority** (Security patches):
        - langchain: 1.2.5 → 1.2.9
          - Review: Check changelog for security fixes
          - Action: `pip install --upgrade langchain==1.2.9`

        **Low Priority** (Patch updates):
        - fastapi: 0.128.0 → 0.128.4
          - Action: `pip install --upgrade fastapi==0.128.4`
```

### Step 6: Suggest Updates with Migration Notes

Provide actionable update guidance:

```yaml
suggest_updates:
  input:
    package: "pydantic"
    current: "2.9.0"
    target: "2.10.0"

  process:
    1_research_changes:
      sources:
        - Official changelog
        - Migration guides
        - Release notes
        - GitHub releases

    2_identify_breaking_changes:
      check:
        - API changes
        - Deprecated features
        - Configuration changes
        - Dependency updates

    3_generate_migration_plan:
      format: |
        ## Update Plan: pydantic 2.9.0 → 2.10.0

        ### Version Information
        - **Current**: 2.9.0
        - **Target**: 2.10.0
        - **Update Type**: Minor
        - **Release Date**: (from changelog)

        ### Changes Summary
        - New features: [list]
        - Bug fixes: [list]
        - Performance improvements: [list]

        ### Breaking Changes
        ⚠️ **None detected** (minor version update)

        ### Migration Steps

        1. **Backup current environment**
           ```bash
           pip freeze > requirements.backup.txt
           ```

        2. **Update package**
           ```bash
           pip install --upgrade pydantic==2.10.0
           ```

        3. **Run tests**
           ```bash
           pytest {directories.tests}/
           ```

        4. **Check for deprecation warnings**
           - Review test output
           - Update any deprecated usage

        5. **Verify functionality**
           - Run application
           - Check critical paths

        ### Rollback Plan
        If issues occur:
        ```bash
        pip install pydantic==2.9.0
        ```

        ### References
        - Changelog: https://docs.pydantic.dev/latest/changelog/
        - Migration Guide: https://docs.pydantic.dev/latest/migration/
```

## Output Formats

### Single Package Check

```markdown

## Version Check: {package_name}

**Language**: {language}
**Registry Date**: {registry.last_updated}

| Field | Value |
|-------|-------|
| Current Version | {current} |
| Registry Version | {registry} |
| Status | {current/outdated/unknown} |
| Update Type | {none/patch/minor/major} |
| Recommendation | {update command} |
```

### Blueprint Audit

```markdown

## Blueprint Version Audit: {blueprint_id}

**Blueprint**: {blueprint_name}
**Registry Date**: {registry.last_updated}

### Summary
- ✅ Current: {count}
- ⚠️ Outdated: {count}
- ❓ Not tracked: {count}

### Details
[Tables for frameworks, tools, dependencies]

### Recommendations
[List of suggested updates]
```

### Project Scan

```markdown

## Project Version Audit

**Project**: {project_name}
**Language**: {language}
**Scanned Files**: {files}
**Registry Date**: {registry.last_updated}

### Summary Statistics
- Total packages: {total}
- Current: {current_count}
- Outdated: {outdated_count}
- Not tracked: {unknown_count}

### Outdated Packages (Priority Order)
[Table with update recommendations]

### Update Commands
```bash
{generated update commands}
```

### Migration Notes
[Per-package migration guidance]
```

## Example Prompts

Users can trigger this skill with prompts like:

### Single Package Checks

- "Check if fastapi version 0.128.0 is current"
- "What's the recommended version for langchain?"
- "Is pydantic 2.9.0 up to date?"

### Blueprint Audits

- "Audit the python-fastapi blueprint dependencies"
- "Check all versions in the nextjs-fullstack blueprint"
- "Are blueprint dependencies current?"

### Project Scans

- "Find outdated packages in this project"
- "Check all Python dependencies against the registry"
- "What packages need updating?"
- "Audit project dependencies"

### Update Planning

- "Suggest updates for outdated packages"
- "Create migration plan for pydantic update"
- "What breaking changes in langchain 1.2.9?"
- "Generate update commands for all outdated packages"

## Commands

The skill supports these command patterns:

| Command | Action |
|---------|--------|
| `version-check package <name> [version]` | Check single package |
| `version-check blueprint <blueprint-id>` | Audit blueprint dependencies |
| `version-check project [path]` | Scan project dependencies |
| `version-check update-plan <package>` | Generate migration plan |
| `version-check outdated` | Find all outdated packages |

## Important Rules

1. **Registry is source of truth** - Always use `{directories.knowledge}/version-registry.json` as authoritative
2. **Handle version ranges** - Support `+`, `x`, `^`, `~` syntax
3. **Respect compatibility** - Mark compatible versions even if not exact match
4. **Prioritize updates** - Major > Minor > Patch for priority ordering
5. **Provide context** - Include registry date and update type in reports
6. **Migration guidance** - Always include migration steps and rollback plans
7. **Unknown packages** - Clearly mark packages not in registry
8. **Breaking changes** - Highlight breaking changes prominently

## Version Comparison Logic

```yaml
version_comparison:
  exact_match:
    current: "1.2.3"
    registry: "1.2.3"
    status: "current"

  compatible_range:
    current: "1.2.3"
    registry: "1.2+"
    status: "current"
    reason: "Meets minimum requirement"

  patch_behind:
    current: "1.2.3"
    registry: "1.2.5"
    status: "outdated"
    update_type: "patch"
    priority: "low"

  minor_behind:
    current: "1.2.3"
    registry: "1.3.0"
    status: "outdated"
    update_type: "minor"
    priority: "medium"

  major_behind:
    current: "1.2.3"
    registry: "2.0.0"
    status: "outdated"
    update_type: "major"
    priority: "high"
    warning: "May include breaking changes"
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Registry file not found | Report error, suggest checking {directories.knowledge}/ directory |
| Package not in registry | Mark as "not tracked", continue with others |
| Invalid version format | Attempt to parse, fallback to "unknown" status |
| Dependency file not found | Skip language, report missing files |
| Cannot parse dependency file | Report parsing error, suggest manual check |

## Success Criteria

Version check is successful when:
- [ ] Registry loaded and parsed correctly
- [ ] All requested packages checked
- [ ] Versions compared accurately
- [ ] Status correctly categorized (current/outdated/unknown)
- [ ] Update recommendations provided
- [ ] Migration notes included (when applicable)
- [ ] Clear, actionable report generated

## Related Skills

- `update-knowledge` - Updates the version registry itself
- `stack-configuration` - Uses version info for stack setup
- `blueprint-generation` - Validates blueprint versions

## References

- `{directories.knowledge}/version-registry.json` - Source of truth for package versions
- `{directories.blueprints}/*/blueprint.json` - Blueprint dependency definitions
- Project dependency files (`requirements.txt`, `package.json`, etc.)

---

*This skill ensures projects stay current with Factory-recommended package versions while providing safe migration paths.*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.
