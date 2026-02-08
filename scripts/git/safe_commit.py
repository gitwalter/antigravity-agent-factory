#!/usr/bin/env python3
"""
Safe Commit - Enforced Pre-Commit Validation Wrapper

This script ALWAYS runs pre-commit validation before committing.
It cannot be bypassed - ensuring consistent, validated commits.

Usage:
    python scripts/git/safe_commit.py "feat(scope): message"
    python scripts/git/safe_commit.py "feat(scope): message" --push
    python scripts/git/safe_commit.py "feat(scope): message" --body "Detailed description"
    python scripts/git/safe_commit.py --dry-run "feat(scope): message"

Why This Exists:
    Shell agents can accidentally use 'git commit --no-verify' without
    running pre-commit validation first. This wrapper makes it impossible
    to skip validation - one command does everything correctly.

Author: Cursor Agent Factory
Date: 2026-02-08
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def find_project_root() -> Path:
    """Find the project root by looking for .git directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find project root (.git directory)")


def find_python() -> str:
    """Find Python from tools.json config, with fallbacks."""
    try:
        project_root = find_project_root()
        tools_config = project_root / ".cursor" / "config" / "tools.json"
        
        if tools_config.exists():
            import json
            with open(tools_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            python_config = config.get("tools", {}).get("python", {})
            
            # Try fallbacks from config in order
            for path in python_config.get("fallbacks", []):
                if os.path.isfile(path):
                    return path
    except Exception:
        pass  # Fall through to sys.executable
    
    # Final fallback to sys.executable
    return sys.executable


def find_git() -> str:
    """Find Git from tools.json config, with fallbacks."""
    try:
        project_root = find_project_root()
        tools_config = project_root / ".cursor" / "config" / "tools.json"
        
        if tools_config.exists():
            import json
            with open(tools_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            git_config = config.get("tools", {}).get("git", {})
            
            # Try fallbacks from config in order
            for path in git_config.get("fallbacks", []):
                if os.path.isfile(path):
                    return path
    except Exception:
        pass  # Fall through to default
    
    # Final fallback
    return "git"


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    capture: bool = True
) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 5 minutes"
    except Exception as e:
        return 1, "", str(e)


def check_staged_files(git: str, cwd: Path) -> List[str]:
    """Get list of staged files."""
    code, stdout, _ = run_command(
        [git, "diff", "--cached", "--name-only"],
        cwd=cwd
    )
    if code != 0:
        return []
    return [f.strip() for f in stdout.strip().split("\n") if f.strip()]


def run_pre_commit(python: str, cwd: Path, fast: bool = False) -> Tuple[bool, str]:
    """
    Run pre-commit validation.
    
    Returns:
        Tuple of (success, output message)
    """
    script = cwd / "scripts" / "git" / "pre_commit_runner.py"
    if not script.exists():
        return False, f"Pre-commit runner not found: {script}"
    
    args = [python, str(script), "--sync"]
    if fast:
        args.append("--fast")
    
    print("=" * 60)
    print("RUNNING PRE-COMMIT VALIDATION")
    print("=" * 60)
    print(f"Command: {' '.join(args)}")
    print()
    
    # Run with live output
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            timeout=300,
        )
        if result.returncode == 0:
            return True, "Pre-commit validation passed"
        else:
            return False, f"Pre-commit validation failed (exit code {result.returncode})"
    except subprocess.TimeoutExpired:
        return False, "Pre-commit validation timed out"
    except Exception as e:
        return False, f"Pre-commit error: {e}"


def git_add_all(git: str, cwd: Path) -> Tuple[bool, str]:
    """Stage all changes."""
    code, stdout, stderr = run_command([git, "add", "-A"], cwd=cwd)
    if code != 0:
        return False, f"git add failed: {stderr}"
    return True, "Staged all changes"


def git_commit(
    git: str,
    cwd: Path,
    message: str,
    body: Optional[str] = None
) -> Tuple[bool, str, str]:
    """
    Create a commit with --no-verify (since we already ran pre-commit).
    
    Returns:
        Tuple of (success, output, commit_hash)
    """
    cmd = [git, "commit", "--no-verify", "-m", message]
    if body:
        cmd.extend(["-m", body])
    
    code, stdout, stderr = run_command(cmd, cwd=cwd)
    
    if code != 0:
        if "nothing to commit" in stderr or "nothing to commit" in stdout:
            return False, "Nothing to commit (working tree clean)", ""
        return False, f"Commit failed: {stderr or stdout}", ""
    
    # Extract commit hash
    commit_hash = ""
    for line in (stdout + stderr).split("\n"):
        if line.startswith("["):
            # Format: [branch hash] message
            parts = line.split()
            if len(parts) >= 2:
                commit_hash = parts[1].rstrip("]")
                break
    
    return True, stdout or stderr, commit_hash


def git_push(git: str, cwd: Path) -> Tuple[bool, str]:
    """Push to remote."""
    print()
    print("Pushing to remote...")
    code, stdout, stderr = run_command([git, "push"], cwd=cwd)
    if code != 0:
        return False, f"Push failed: {stderr or stdout}"
    return True, stderr or stdout or "Pushed successfully"


def main():
    parser = argparse.ArgumentParser(
        description="Safe commit with enforced pre-commit validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/git/safe_commit.py "feat(api): add new endpoint"
    python scripts/git/safe_commit.py "fix(auth): resolve token issue" --push
    python scripts/git/safe_commit.py "docs: update README" --body "Added examples"
    python scripts/git/safe_commit.py --dry-run "chore: test commit"
    python scripts/git/safe_commit.py --fast "fix: quick patch"
        """
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="Commit message (required unless --dry-run)"
    )
    parser.add_argument(
        "--body", "-b",
        help="Extended commit message body"
    )
    parser.add_argument(
        "--push", "-p",
        action="store_true",
        help="Push to remote after commit"
    )
    parser.add_argument(
        "--fast", "-f",
        action="store_true",
        help="Use fast mode for pre-commit (skip slow checks)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Run pre-commit but don't actually commit"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.message and not args.dry_run:
        parser.error("Commit message is required (or use --dry-run)")
    
    # Setup
    try:
        project_root = find_project_root()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return 1
    
    python = find_python()
    git = find_git()
    
    if args.verbose:
        print(f"Project root: {project_root}")
        print(f"Python: {python}")
        print(f"Git: {git}")
        print()
    
    # Step 1: Stage all changes
    print("Staging all changes...")
    success, msg = git_add_all(git, project_root)
    if not success:
        print(f"ERROR: {msg}")
        return 1
    
    # Check if there are staged files
    staged = check_staged_files(git, project_root)
    if not staged:
        print("Nothing to commit (no staged files)")
        return 0
    
    print(f"Staged {len(staged)} file(s)")
    if args.verbose:
        for f in staged[:10]:
            print(f"  - {f}")
        if len(staged) > 10:
            print(f"  ... and {len(staged) - 10} more")
    print()
    
    # Step 2: Run pre-commit validation (MANDATORY)
    success, msg = run_pre_commit(python, project_root, fast=args.fast)
    print()
    
    if not success:
        print("=" * 60)
        print("PRE-COMMIT VALIDATION FAILED")
        print("=" * 60)
        print(msg)
        print()
        print("Fix the issues above and try again.")
        return 1
    
    print("=" * 60)
    print("PRE-COMMIT VALIDATION PASSED")
    print("=" * 60)
    print()
    
    # Step 3: Dry run check
    if args.dry_run:
        print("DRY RUN: Would commit with message:")
        print(f"  {args.message}")
        if args.body:
            print(f"  Body: {args.body}")
        if args.push:
            print("  Would push to remote")
        return 0
    
    # Step 4: Commit
    print(f"Committing: {args.message}")
    success, output, commit_hash = git_commit(
        git, project_root, args.message, args.body
    )
    
    if not success:
        print(f"ERROR: {output}")
        return 1
    
    print(output)
    
    # Step 5: Push (if requested)
    if args.push:
        success, msg = git_push(git, project_root)
        if not success:
            print(f"ERROR: {msg}")
            return 1
        print(msg)
    
    # Success summary
    print()
    print("=" * 60)
    print("SUCCESS")
    print("=" * 60)
    if commit_hash:
        print(f"Commit: {commit_hash}")
    if args.push:
        print("Pushed to remote")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
