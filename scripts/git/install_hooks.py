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
# Pre-commit hook for Antigravity Agent Factory
# 
# Philosophy (A10 Learning): Fast, non-blocking, auto-fixing.
# Only blocks for: secrets, JSON syntax errors.
# Everything else: auto-fix and stage silently.
#

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Find Python
PYTHON=""
for p in "/c/App/Anaconda/python.exe" "/d/Anaconda/python.exe" "python3" "python"; do
    if command -v "$p" >/dev/null 2>&1; then
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

# 4. ARTIFACT SYNC (auto-fix, silent) - wu wei: let counts flow from reality
SYNC_ARTIFACTS="$REPO_ROOT/scripts/validation/sync_artifacts.py"
if [ -f "$SYNC_ARTIFACTS" ]; then
    $PYTHON "$SYNC_ARTIFACTS" --sync --fast >/dev/null 2>&1 || true
    # Stage any auto-fixed files
    git add docs/reference/KNOWLEDGE_FILES.md 2>/dev/null || true
    git add knowledge/manifest.json 2>/dev/null || true
    git add README.md 2>/dev/null || true
fi

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
    print("\nDesign: Fast (~3s), only blocks for unfixable issues.")
    print("For artifact sync, run manually: python scripts/validation/sync_artifacts.py --sync --fast")
    
    return 0


if __name__ == "__main__":
    sys.exit(install_hooks())
