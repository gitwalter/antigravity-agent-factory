---
name: committing-releases
description: 'Automated release management using semantic versioning and automated changelog maintenance.
  '
type: skill
version: 1.0.0
category: management
agents:
- master-system-orchestrator
- registry-clerk
knowledge:
- plane-integration.json
tools:
- run_command
related_skills:
- managing-plane-tasks
- orchestrating-mcp
references:
- CHANGELOG.md
templates:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

This skill formalizes the release process for the Antigravity Agent Factory. It extends the Robust Commit Workflow (RCW) by adding automated semantic versioning.

## When to Use
- When completing a major feature phase (e.g., transition from Phase 5 to Phase 6).
- When a set of verified bugs or features needs to be bundled into a stable release.
- For managing production-ready snapshots of the factory.

## Prerequisites
- **High-Fidelity State**: All local changes must be ready for commitment.
- **Git Config**: User must have `git` configured with push access to remote.
- **Environment**: Must be running in the `cursor-factory` conda environment.

## Process

The release process is fully automated via the `safe_release.py` script.

### 1. Version Selection
Determine the bump type based on [Semantic Versioning](https://semver.org/):
- `patch`: Bug fixes and minor maintenance.
- `minor`: New features, no breaking changes.
- `major`: Breaking changes or fundamental architectural shifts.

### 2. Automated Execution
Run the release script. This will automatically:
1. **Analyze Plane Issues**: Perform a federated search for all implemented Plane issues since the last release to ensure the changelog is exhaustive.
2. Extract the current version from `CHANGELOG.md`.
3. Update `CHANGELOG.md` with the new version and date.
4. Run `safe_commit.py` (which runs full verification/smoke tests).
5. Push commit to the remote repository.

```bash
# Example: Minor release (e.g., 1.6.0 -> 1.7.0)
conda run -p D:\Anaconda\envs\cursor-factory python scripts/git/safe_release.py --bump minor --no-tag
```

### 3. Verification
After execution, verify:
- `CHANGELOG.md` contains the new version header.
- Remote repository reflects the new version commit.

## Best Practices
- **Never manual bump**: Always use `safe_release.py` to ensure the `CHANGELOG.md` and `git tag` are perfectly synchronized.
- **Verification First**: The script depends on `safe_commit.py`. If tests fail, the release will be aborted. Fix all failures before releasing.
- **Informative Changelogs**: Ensure that recent changes are properly documented in the draft section of `CHANGELOG.md` before running the release.
- **Tag Signing**: (Future) Enable GPG signing for release tags for non-repudiation.


*Immutable releases are the anchor of engineering reliability.*
