#!/usr/bin/env python3
"""
Install Git hooks for the Antigravity Agent Factory project.
This script sets up pre-commit hooks that automatically maintain
README structure counts, ensuring documentation stays synchronized.

Usage:
    python scripts/git/install_hooks.py
"""

import os
import stat
import sys
from pathlib import Path


# Fast, simple pre-commit hook (A10 Learning: failures teach us)
# Design: Only block for unfixable issues. Auto-fix everything else.
PRE_COMMIT_HOOK = '''#!/bin/sh
#
# Pre-commit hook for Antigravity Agent Factory# 
# Philosophy (A10 Learning): Fast, non-blocking, auto-fixing.
# Only blocks for: secrets, JSON syntax errors.
# Everything else: auto-fix and stage silently.
#

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Find Python (prefer cursor-factory conda env)
PYTHON=""
for p in "/d/Anaconda/envs/cursor-factory/python.exe" "/c/App/Anaconda/envs/cursor-factory/python.exe" "/d/Anaconda/python.exe" "/c/App/Anaconda/python.exe" "python3" "python"; do    if command -v "$p" >/dev/null 2>&1; then
        PYTHON="$p"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    exit 0  # No Python, skip checks
fi

# Get staged files once
STAGED=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)
[ -z "$STAGED" ] && exit 0

echo "Pre-commit: checking..."

# 1. SECRET SCAN (blocks) - skip files that contain secret patterns as code
for file in $STAGED; do
    [ -f "$file" ] || continue
    # Skip hook installer (contains patterns as code, not secrets)
    case "$file" in scripts/git/install_hooks.py) continue;; esac
    if grep -qE 'sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|-----BEGIN.*PRIVATE KEY' "$file" 2>/dev/null; then
        echo "BLOCKED: Possible secret in $file"
        echo "Use --no-verify to bypass"
        exit 1
    fi
done

# 2. JSON SYNTAX (blocks) - utf-8-sig handles BOM from Windows tools
for file in $STAGED; do
    case "$file" in *.json)
        [ -f "$file" ] || continue
        if ! $PYTHON -c "import json; json.load(open('$file', encoding='utf-8-sig'))" 2>/dev/null; then
            echo "BLOCKED: Invalid JSON in $file"
            exit 1
        fi
    esac
done

# 3. VERSION SYNC (auto-fix, silent)
SYNC_VERSIONS="$REPO_ROOT/scripts/validation/sync_manifest_versions.py"
if [ -f "$SYNC_VERSIONS" ]; then
    $PYTHON "$SYNC_VERSIONS" --sync >/dev/null 2>&1 || true
    git add README.md .agentrules knowledge/manifest.json 2>/dev/null || true
    git add docs/GETTING_STARTED.md docs/ONBOARDING_GUIDE.md 2>/dev/null || true
fi

# 4. ARTIFACT SYNC (auto-fix, fast mode for wu-wei flow)
SYNC_ARTIFACTS="$REPO_ROOT/scripts/validation/sync_artifacts.py"
if [ -f "$SYNC_ARTIFACTS" ]; then
    $PYTHON "$SYNC_ARTIFACTS" --sync --fast >/dev/null 2>&1 || true
    git add README.md docs/reference/KNOWLEDGE_FILES.md 2>/dev/null || true
    git add docs/TESTING.md knowledge/manifest.json 2>/dev/null || true
fi

# 5. TEST CATALOG (always sync to avoid CI failures)
TEST_CATALOG="$REPO_ROOT/scripts/docs/generate_test_catalog.py"
if [ -f "$TEST_CATALOG" ]; then
    $PYTHON "$TEST_CATALOG" >/dev/null 2>&1 || true
    git add docs/TEST_CATALOG.md 2>/dev/null || true
fi

# 6. KNOWLEDGE COUNTS (auto-fix)
SYNC_KNOWLEDGE="$REPO_ROOT/scripts/validation/sync_knowledge_counts.py"
if [ -f "$SYNC_KNOWLEDGE" ]; then
    $PYTHON "$SYNC_KNOWLEDGE" --sync >/dev/null 2>&1 || true
    git add docs/reference/KNOWLEDGE_FILES.md 2>/dev/null || true
fi

# 7. UPDATE INDEX (auto-fix)
UPDATE_INDEX="$REPO_ROOT/scripts/validation/update_index.py"
if [ -f "$UPDATE_INDEX" ]; then
    $PYTHON "$UPDATE_INDEX" --full >/dev/null 2>&1 || true
    git add docs/index.md 2>/dev/null || true
fi

# 8. CHANGELOG CHECK (warn only - manual update required)
CHANGELOG_HELPER="$REPO_ROOT/scripts/docs/changelog_helper.py"
if [ -f "$CHANGELOG_HELPER" ]; then
    if ! $PYTHON "$CHANGELOG_HELPER" --check >/dev/null 2>&1; then
        echo "[INFO] Significant changes detected - consider updating CHANGELOG.md"
        echo "       Run: python scripts/docs/changelog_helper.py --suggest"
    fifi

echo "[OK] Pre-commit passed"
exit 0
'''

# Keep backward compatibility aliases
PRE_COMMIT_HOOK_UNIX = PRE_COMMIT_HOOK
PRE_COMMIT_HOOK_WINDOWS = PRE_COMMIT_HOOK


def install_hooks():
    """Install Git hooks for the project."""
    # Find .git directory (scripts/git/ -> scripts/ -> repo_root)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    git_dir = repo_root / ".git"
    
    if not git_dir.exists():
        print("Error: .git directory not found. Are you in a git repository?")
        return 1
    
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    
    # Install pre-commit hook
    pre_commit_path = hooks_dir / "pre-commit"
    
    # Check if hook already exists
    if pre_commit_path.exists():
        print(f"Pre-commit hook already exists at {pre_commit_path}")
        response = input("Overwrite? [y/N]: ").strip().lower()
        if response != 'y':
            print("Skipping pre-commit hook installation")
            return 0
    
    # Write the hook (use Windows version on Windows for Anaconda path)
    hook_content = PRE_COMMIT_HOOK_WINDOWS if os.name == 'nt' else PRE_COMMIT_HOOK_UNIX
    # Write with Unix line endings for Git (works on all platforms)
    with open(pre_commit_path, 'w', newline='\n') as f:
        f.write(hook_content)
    
    # Make it executable (Unix)
    if os.name != 'nt':
        pre_commit_path.chmod(pre_commit_path.stat().st_mode | stat.S_IEXEC)
    
    print(f"Installed pre-commit hook at {pre_commit_path}")
    print("\nThe hook will automatically:")
    print("  1. Block commits with secrets (API keys, tokens, private keys)")
    print("  2. Block commits with invalid JSON syntax")
    print("  3. Auto-sync version numbers (silent, auto-staged)")
    print("  4. Auto-sync artifacts (fast mode, auto-staged)")
    print("  5. Regenerate test catalog when test files change")
    print("\nDesign: Fast (~5-10s), wu-wei sync on every commit.")
    print("Prevents CI failures from out-of-sync artifacts.")    
    return 0


if __name__ == "__main__":
    sys.exit(install_hooks())
