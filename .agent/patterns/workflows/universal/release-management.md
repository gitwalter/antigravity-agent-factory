# Release Management Workflow

## Overview

Systematic workflow for managing software releases including version bumping, changelog generation, tagging, and deployment coordination.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** All stacks

## Trigger Conditions

This workflow is activated when:

- Release preparation requested
- Version bump needed
- Changelog generation required
- Release deployment initiated

**Trigger Examples:**
- "Prepare release v2.0.0"
- "Create a new release"
- "Bump version to 1.2.0"
- "Generate release notes"

## Phases

### Phase 1: Pre-Release Checks

**Description:** Verify readiness for release.

**Entry Criteria:** Release decision made
**Exit Criteria:** Ready for release

#### Step 1.1: Verify Branch Status

**Actions:**
- Check main branch is clean
- Verify all PRs merged
- Check CI passing
- Review open issues

#### Step 1.2: Run Quality Checks

**Actions:**
- Execute full test suite
- Run security scans
- Check code coverage
- Verify documentation

**Outputs:**
- Quality report
- Release readiness

**Is Mandatory:** Yes

---

### Phase 2: Version Management

**Description:** Determine and apply version.

**Entry Criteria:** Quality checks passed
**Exit Criteria:** Version updated

#### Step 2.1: Determine Version

**Actions:**
- Analyze commits since last release
- Determine version bump type
- Apply semantic versioning

**Semantic Versioning:**

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking change | MAJOR | 1.0.0 → 2.0.0 |
| New feature | MINOR | 1.0.0 → 1.1.0 |
| Bug fix | PATCH | 1.0.0 → 1.0.1 |

#### Step 2.2: Update Version Files

**Actions:**
- Update package.json/pyproject.toml
- Update version constants
- Update documentation version

**Outputs:**
- Updated version files

**Is Mandatory:** Yes

---

### Phase 3: Changelog Generation

**Description:** Generate release notes.

**Entry Criteria:** Version determined
**Exit Criteria:** Changelog updated

#### Step 3.1: Collect Changes

**Actions:**
- Parse commits since last tag
- Categorize by type
- Extract PR descriptions
- Identify contributors

**Commit Categories:**
- feat: New features
- fix: Bug fixes
- docs: Documentation
- perf: Performance
- refactor: Refactoring
- test: Tests
- chore: Maintenance

#### Step 3.2: Generate Changelog Entry

**Actions:**
- Format changelog entry
- Add to CHANGELOG.md
- Include breaking changes
- Credit contributors

**Changelog Format:**
```markdown
## [2.0.0] - 2026-02-02

### Breaking Changes
- Removed deprecated API endpoint (#123)

### Features
- Added user profile management (#456)
- Implemented dashboard widgets (#789)

### Bug Fixes
- Fixed login redirect issue (#234)

### Contributors
- @developer1
- @developer2
```

**Outputs:**
- Updated CHANGELOG.md

**Is Mandatory:** Yes

---

### Phase 4: Release Creation

**Description:** Create the release artifacts.

**Entry Criteria:** Changelog generated
**Exit Criteria:** Release created

#### Step 4.1: Create Git Tag

**Actions:**
- Create annotated tag
- Push tag to remote
- Verify tag creation

#### Step 4.2: Create GitHub Release

**Actions:**
- Create release from tag
- Attach changelog
- Upload artifacts
- Mark as pre-release if needed

**MCP Tools:**
- `github-createRelease`: Create release

**Outputs:**
- Git tag
- GitHub release

**Is Mandatory:** Yes

---

### Phase 5: Deployment

**Description:** Deploy the release.

**Entry Criteria:** Release created
**Exit Criteria:** Deployed to production

#### Step 5.1: Deploy to Staging

**Actions:**
- Deploy release to staging
- Run smoke tests
- Verify functionality

#### Step 5.2: Deploy to Production

**Actions:**
- Obtain approval
- Deploy to production
- Verify deployment
- Monitor metrics

**Outputs:**
- Deployment confirmation

**Is Mandatory:** Yes

---

### Phase 6: Communication

**Description:** Announce the release.

**Entry Criteria:** Deployment complete
**Exit Criteria:** Stakeholders notified

#### Step 6.1: Notify Stakeholders

**Actions:**
- Send release announcement
- Update documentation
- Notify support team
- Update status page

**Outputs:**
- Release announcement

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Version Bump Type

| Changes | Bump |
|---------|------|
| Breaking changes | MAJOR |
| New features | MINOR |
| Bug fixes only | PATCH |

### Decision: Release Timing

| Condition | Action |
|-----------|--------|
| All checks pass | Proceed |
| Minor issues | Fix then release |
| Critical issues | Delay release |

### Decision: Hotfix vs Release

| Severity | Approach |
|----------|----------|
| Critical production issue | Hotfix branch |
| Normal changes | Standard release |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Version conflict | Resolve and retry |
| Changelog generation fails | Manual changelog |
| Tag creation fails | Check permissions |
| Deploy failure | Rollback tag and retry |

---

## Example Session

```
User: Prepare release for version 2.0.0

Agent:
━━━ PHASE 1: Pre-Release Checks ━━━
Verifying branch status...
✓ main branch clean
✓ 5 PRs merged since last release
✓ CI passing

Running quality checks...
✓ Tests: 456/456 passing
✓ Coverage: 84%
✓ Security: No issues

━━━ PHASE 2: Version Management ━━━
Determining version...
- Breaking changes detected
- Semantic version: 2.0.0

Updating version files...
✓ package.json: 1.5.0 → 2.0.0
✓ VERSION file updated

━━━ PHASE 3: Changelog Generation ━━━
Collecting changes...
- 15 features
- 8 bug fixes
- 3 breaking changes

Generating changelog...

## [2.0.0] - 2026-02-02

### Breaking Changes
- Removed v1 API endpoints
- Changed auth token format
- Updated minimum Node version to 20

### Features
- User profile management
- Dashboard customization
- Export functionality
[...12 more features]

### Bug Fixes
- Fixed session timeout
- Corrected date formatting
[...6 more fixes]

✓ CHANGELOG.md updated

━━━ PHASE 4: Release Creation ━━━
Creating git tag...
✓ Tag v2.0.0 created

Creating GitHub release...
✓ Release v2.0.0 published

━━━ PHASE 5: Deployment ━━━
Deploying to staging...
✓ Staging deployment complete

Requesting production approval...
✓ Approved by @release-manager

Deploying to production...
✓ Production deployment complete

━━━ PHASE 6: Communication ━━━
Sending announcements...
✓ Email sent to stakeholders
✓ Slack notification posted
✓ Documentation updated

✨ Release v2.0.0 complete!

Release URL: https://github.com/org/repo/releases/v2.0.0
```

---

## Related Artifacts

- **Workflows**: `workflows/operations/cicd-pipeline.md`
- **Knowledge**: `knowledge/cicd-patterns.json`
