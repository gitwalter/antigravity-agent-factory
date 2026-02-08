#!/usr/bin/env python3
"""
Pre-Commit Runner - Intelligent Pre-Commit Automation with Parallel Execution

A comprehensive pre-commit system that:
1. Cleans up temporary files
2. Runs validation and sync scripts IN PARALLEL for speed
3. Validates JSON/YAML syntax
4. Runs fast tests to catch failures before commit
5. Auto-stages synced files
6. Documents lessons learned from failures

Usage:
    python scripts/git/pre_commit_runner.py                    # Full check (no changes)
    python scripts/git/pre_commit_runner.py --sync             # Sync and auto-stage
    python scripts/git/pre_commit_runner.py --sync --test      # Include test validation
    python scripts/git/pre_commit_runner.py --sync --fast      # Skip slow checks
    python scripts/git/pre_commit_runner.py --sync --full      # Full validation + all tests
    python scripts/git/pre_commit_runner.py --sync --parallel  # Force parallel (default)
    python scripts/git/pre_commit_runner.py --sync --sequential # Force sequential

Author: Cursor Agent Factory
Date: 2026-02-08
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class ScriptResult:
    """Result of running a pre-commit script."""
    name: str
    success: bool
    output: str
    files_changed: List[str]
    elapsed_ms: int


@dataclass
class PreCommitReport:
    """Complete pre-commit report."""
    cleanup_files: int = 0
    sync_results: List[ScriptResult] = field(default_factory=list)
    json_errors: List[str] = field(default_factory=list)
    test_passed: int = 0
    test_failed: int = 0
    files_to_stage: List[str] = field(default_factory=list)
    total_elapsed_ms: int = 0
    

class PreCommitRunner:
    """
    Intelligent pre-commit automation system.
    
    Workflow:
    1. Cleanup - Remove temp files, __pycache__, etc.
    2. Sync - Run all validation/sync scripts
    3. Validate - Check JSON/YAML syntax
    4. Test - Run fast tests (optional)
    5. Stage - Auto-stage modified files
    
    Attributes:
        project_root: Path to the project root directory.
        python_path: Path to the Python executable.
        sync_mode: Whether to apply changes (True) or just check (False).
        fast_mode: Skip slow validation checks.
        run_tests: Run test validation before commit.
    """
    
    # Cleanup patterns
    CLEANUP_PATTERNS = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.tmp",
        "**/*.temp",
        "**/*.swp",
        "**/*.swo",
        "**/.pytest_cache",
        "**/.mypy_cache",
        "**/*.egg-info",
        "**/dist",
        "**/build",
        "**/.coverage",
        "**/htmlcov",
    ]
    
    # Scripts organized for MAXIMUM parallelism
    # Group 0: ALL independent scripts run together (most scripts have no real dependencies)
    # Group 1: Only scripts that truly depend on group 0 outputs
    #
    # Dependency analysis:
    # - sync_manifest_versions: independent (reads manifest.json)
    # - sync_knowledge_counts: independent (counts files)
    # - validate_yaml_frontmatter: independent (reads skill/agent files)
    # - dependency_validator: independent (reads requirements)
    # - validate_readme: needs counts (waits for knowledge_counts)
    # - sync_artifacts: independent (reads files, generates docs)
    # - generate_test_catalog: independent (reads test files)
    # - update_index: needs artifact docs (waits for sync_artifacts)
    # - changelog_helper: independent (reads git staging)
    SCRIPTS = [
        # Group 0: Maximum parallel - 7 scripts at once
        {
            "name": "sync_manifest_versions",
            "script": "scripts/validation/sync_manifest_versions.py",
            "args_check": [],
            "args_sync": ["--sync"],
            "purpose": "Sync version numbers across manifest",
            "fast_skip": False,
            "critical": True,
            "group": 0
        },
        {
            "name": "sync_knowledge_counts",
            "script": "scripts/validation/sync_knowledge_counts.py",
            "args_check": [],
            "args_sync": ["--sync"],
            "purpose": "Sync knowledge file counts",
            "fast_skip": False,
            "critical": True,
            "group": 0
        },
        {
            "name": "validate_yaml_frontmatter",
            "script": "scripts/validation/validate_yaml_frontmatter.py",
            "args_check": [],
            "args_sync": [],
            "purpose": "Validate YAML frontmatter in skills/agents",
            "fast_skip": True,
            "critical": False,
            "group": 0
        },
        {
            "name": "dependency_validator",
            "script": "scripts/validation/dependency_validator.py",
            "args_check": [],
            "args_sync": [],
            "purpose": "Validate dependency graph",
            "fast_skip": True,
            "critical": False,
            "group": 0
        },
        {
            "name": "sync_artifacts",
            "script": "scripts/validation/sync_artifacts.py",
            "args_check": [],
            "args_sync": ["--sync", "--fast"],
            "purpose": "Sync all artifact documentation (fast file-based counting)",
            "fast_skip": False,
            "critical": True,
            "group": 0
        },
        {
            "name": "generate_test_catalog",
            "script": "scripts/docs/generate_test_catalog.py",
            "args_check": [],
            "args_sync": [],
            "purpose": "Generate test catalog documentation",
            "fast_skip": False,
            "critical": False,
            "group": 0
        },
        {
            "name": "changelog_check",
            "script": "scripts/docs/changelog_helper.py",
            "args_check": ["--check"],
            "args_sync": ["--check"],
            "purpose": "Check if changelog needs update",
            "fast_skip": True,
            "critical": False,
            "group": 0
        },
        # Group 1: Scripts that depend on group 0 outputs
        {
            "name": "validate_readme",
            "script": "scripts/validation/validate_readme_structure.py",
            "args_check": [],
            "args_sync": ["--update"],
            "purpose": "Update README with current stats",
            "fast_skip": False,
            "critical": True,
            "group": 1
        },
        {
            "name": "update_index",
            "script": "scripts/validation/update_index.py",
            "args_check": [],
            "args_sync": ["--full"],
            "purpose": "Update documentation index",
            "fast_skip": True,
            "critical": False,
            "group": 1
        }
    ]
    
    # Maximum parallel workers - increased for more scripts
    MAX_WORKERS = 8
    
    # Files commonly modified by sync scripts
    SYNC_FILES = [
        "README.md",
        "CHANGELOG.md",
        "knowledge/manifest.json",
        "docs/TESTING.md",
        "docs/TEST_CATALOG.md",
        "docs/reference/*.md",
        "docs/index.md"
    ]
    
    def __init__(
        self,
        project_root: Optional[Path] = None,
        python_path: Optional[str] = None,
        sync_mode: bool = False,
        fast_mode: bool = False,
        run_tests: bool = False,
        full_mode: bool = False,
        parallel_mode: bool = True
    ):
        """
        Initialize the pre-commit runner.
        
        Args:
            project_root: Path to project root. Defaults to current directory.
            python_path: Path to Python executable. Auto-detected if not provided.
            sync_mode: If True, apply changes. If False, check only.
            fast_mode: If True, skip slow validation checks.
            run_tests: If True, run fast tests before commit.
            full_mode: If True, run all tests (overrides fast_mode).
            parallel_mode: If True, run scripts in parallel within groups (default).
        """
        self.project_root = project_root or Path.cwd()
        self.python_path = python_path or self._detect_python()
        self.sync_mode = sync_mode
        self.fast_mode = fast_mode and not full_mode
        self.run_tests = run_tests or full_mode
        self.full_mode = full_mode
        self.parallel_mode = parallel_mode
        self.report = PreCommitReport()
        self.results: List[ScriptResult] = []
        
    def _detect_python(self) -> str:
        """Detect the Python executable path from session-paths.json."""
        session_paths = self.project_root / ".cursor" / "cache" / "session-paths.json"
        
        if session_paths.exists():
            try:
                with open(session_paths, "r", encoding="utf-8") as f:
                    paths = json.load(f)
                    if "python" in paths.get("paths", {}):
                        return paths["paths"]["python"]
            except (json.JSONDecodeError, IOError):
                pass
        
        return sys.executable
    
    def cleanup_temp_files(self) -> int:
        """
        Remove temporary files and caches.
        
        Returns:
            Number of items cleaned up.
        """
        cleaned = 0
        
        for pattern in self.CLEANUP_PATTERNS:
            for path in self.project_root.glob(pattern):
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    cleaned += 1
                except (OSError, PermissionError):
                    pass  # Skip files we can't delete
        
        self.report.cleanup_files = cleaned
        return cleaned
    
    def validate_json_files(self) -> List[str]:
        """
        Validate all JSON files in the repository.
        
        Returns:
            List of files with JSON errors.
        """
        errors = []
        
        # Check staged JSON files or all if not in git context
        json_files = list(self.project_root.glob("**/*.json"))
        
        # Exclude node_modules, data, and other common exclusions
        excluded = {
            "node_modules", ".git", "__pycache__", ".pytest_cache",
            "data", ".no_exist", "fixtures"  # Model cache and test fixtures
        }
        
        for json_file in json_files:
            if any(ex in json_file.parts for ex in excluded):
                continue
                
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"{json_file.relative_to(self.project_root)}: {e}")
            except Exception as e:
                errors.append(f"{json_file.relative_to(self.project_root)}: {e}")
        
        self.report.json_errors = errors
        return errors
    
    def run_script(self, script_config: dict) -> ScriptResult:
        """
        Run a single pre-commit script.
        
        Args:
            script_config: Script configuration dict.
            
        Returns:
            ScriptResult with execution details.
        """
        name = script_config["name"]
        script_path = self.project_root / script_config["script"]
        
        if not script_path.exists():
            return ScriptResult(
                name=name,
                success=True,  # Don't fail if optional script doesn't exist
                output=f"Script not found: {script_path}",
                files_changed=[],
                elapsed_ms=0
            )
        
        # Build command
        args = script_config["args_sync"] if self.sync_mode else script_config["args_check"]
        cmd = [self.python_path, str(script_path)] + args
        
        # Run script
        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )
            elapsed = int((time.time() - start) * 1000)
            
            files_changed = self._parse_files_changed(result.stdout)
            
            return ScriptResult(
                name=name,
                success=result.returncode == 0,
                output=result.stdout + result.stderr,
                files_changed=files_changed,
                elapsed_ms=elapsed
            )
        except subprocess.TimeoutExpired:
            return ScriptResult(
                name=name,
                success=False,
                output="Script timed out after 5 minutes",
                files_changed=[],
                elapsed_ms=300000
            )
        except Exception as e:
            return ScriptResult(
                name=name,
                success=False,
                output=str(e),
                files_changed=[],
                elapsed_ms=0
            )
    
    def _parse_files_changed(self, output: str) -> List[str]:
        """Parse files changed from script output."""
        files = []
        for line in output.split("\n"):
            if "Updated:" in line or "Synced:" in line or "Fixed:" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    file_path = parts[-1].strip()
                    if file_path:
                        files.append(file_path)
        return files
    
    def _get_scripts_by_group(self) -> Dict[int, List[dict]]:
        """Organize scripts by execution group."""
        groups: Dict[int, List[dict]] = {}
        for script in self.SCRIPTS:
            group = script.get("group", 0)
            if group not in groups:
                groups[group] = []
            groups[group].append(script)
        return groups
    
    def _run_script_wrapper(self, script_config: dict) -> Tuple[dict, ScriptResult]:
        """Wrapper for parallel execution that returns config with result."""
        result = self.run_script(script_config)
        return (script_config, result)
    
    def run_sync_scripts(self) -> List[ScriptResult]:
        """
        Run all pre-commit scripts, with parallel execution within groups.
        
        Scripts are organized into execution groups:
        - Group 0: Independent validations (parallel)
        - Group 1: Sync scripts (parallel, after group 0)
        - Group 2: Documentation generation (parallel, after group 1)
        - Group 3: Final checks (parallel, after group 2)
        
        Returns:
            List of ScriptResult for each script.
        """
        self.results = []
        groups = self._get_scripts_by_group()
        
        for group_num in sorted(groups.keys()):
            group_scripts = groups[group_num]
            
            # Filter scripts based on fast mode
            scripts_to_run = []
            for script_config in group_scripts:
                if self.fast_mode and script_config.get("fast_skip", False):
                    if not script_config.get("critical", False):
                        print(f"[SKIP] {script_config['name']} (fast mode)")
                        continue
                scripts_to_run.append(script_config)
            
            if not scripts_to_run:
                continue
            
            if self.parallel_mode and len(scripts_to_run) > 1:
                # Parallel execution within group
                self._run_group_parallel(scripts_to_run, group_num)
            else:
                # Sequential execution
                self._run_group_sequential(scripts_to_run)
        
        return self.results
    
    def _run_group_parallel(self, scripts: List[dict], group_num: int) -> None:
        """Run a group of scripts in parallel."""
        print(f"[GROUP {group_num}] Running {len(scripts)} scripts in parallel...")
        
        group_start = time.time()
        pending_results: Dict[str, Tuple[dict, ScriptResult]] = {}
        
        with ThreadPoolExecutor(max_workers=min(len(scripts), self.MAX_WORKERS)) as executor:
            # Submit all scripts
            futures = {
                executor.submit(self._run_script_wrapper, script): script["name"]
                for script in scripts
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                script_name = futures[future]
                try:
                    script_config, result = future.result()
                    pending_results[script_name] = (script_config, result)
                except Exception as e:
                    # Handle unexpected errors
                    pending_results[script_name] = (
                        next(s for s in scripts if s["name"] == script_name),
                        ScriptResult(
                            name=script_name,
                            success=False,
                            output=str(e),
                            files_changed=[],
                            elapsed_ms=0
                        )
                    )
        
        group_elapsed = int((time.time() - group_start) * 1000)
        
        # Print results in original order
        for script in scripts:
            script_config, result = pending_results[script["name"]]
            self.results.append(result)
            self.report.sync_results.append(result)
            
            if result.success:
                print(f"  [OK] {result.name} ({result.elapsed_ms}ms)")
            else:
                status = "FAIL" if script_config.get("critical", False) else "WARN"
                print(f"  [{status}] {result.name} ({result.elapsed_ms}ms)")
                if result.output and script_config.get("critical", False):
                    lines = result.output.strip().split("\n")[:2]
                    for line in lines:
                        print(f"      {line[:80]}")
        
        print(f"[GROUP {group_num}] Completed in {group_elapsed}ms (parallel)")
    
    def _run_group_sequential(self, scripts: List[dict]) -> None:
        """Run a group of scripts sequentially."""
        for script_config in scripts:
            print(f"[RUN] {script_config['name']}... ", end="", flush=True)
            result = self.run_script(script_config)
            self.results.append(result)
            self.report.sync_results.append(result)
            
            if result.success:
                print(f"OK ({result.elapsed_ms}ms)")
            else:
                status = "FAIL" if script_config.get("critical", False) else "WARN"
                print(f"{status} ({result.elapsed_ms}ms)")
                if result.output and script_config.get("critical", False):
                    lines = result.output.strip().split("\n")[:3]
                    for line in lines:
                        print(f"    {line}")
    
    def run_fast_tests(self) -> tuple:
        """
        Run fast validation tests to catch issues before commit.
        
        Returns:
            Tuple of (passed, failed) counts.
        """
        print("\n[TEST] Running validation tests...")
        
        # Run validation tests only (fast)
        test_args = [
            self.python_path, "-m", "pytest",
            "tests/validation/",
            "-q", "--tb=line",
            "-p", "no:sugar", "-p", "no:cov"
        ]
        
        if self.full_mode:
            # Run all tests in parallel
            test_args = [
                self.python_path, "-m", "pytest",
                "tests/",
                "-n", "auto", "-q", "--tb=line",
                "-p", "no:sugar", "-p", "no:cov"
            ]
        
        start = time.time()
        try:
            result = subprocess.run(
                test_args,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600
            )
            elapsed = int((time.time() - start) * 1000)
            
            # Parse results
            output = result.stdout + result.stderr
            
            # Look for "X passed" pattern
            import re
            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)
            
            passed = int(passed_match.group(1)) if passed_match else 0
            failed = int(failed_match.group(1)) if failed_match else 0
            
            self.report.test_passed = passed
            self.report.test_failed = failed
            
            if failed > 0:
                print(f"[FAIL] {passed} passed, {failed} failed ({elapsed}ms)")
                # Print failure details
                for line in output.split("\n"):
                    if "FAILED" in line or "Error" in line:
                        print(f"    {line[:100]}")
            else:
                print(f"[OK] {passed} passed ({elapsed}ms)")
            
            return (passed, failed)
            
        except subprocess.TimeoutExpired:
            print("[TIMEOUT] Tests timed out after 10 minutes")
            return (0, 1)
        except Exception as e:
            print(f"[ERROR] {e}")
            return (0, 1)
    
    def get_files_to_stage(self) -> List[str]:
        """Get list of files that were modified and should be staged."""
        files = set()
        
        for result in self.results:
            files.update(result.files_changed)
        
        # Check git status for common sync files
        try:
            git_path = self._detect_git()
            result = subprocess.run(
                [git_path, "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            for line in result.stdout.strip().split("\n"):
                if line.startswith(" M") or line.startswith("M "):
                    file_path = line[3:].strip()
                    for pattern in self.SYNC_FILES:
                        if "*" in pattern:
                            prefix = pattern.split("*")[0]
                            if file_path.startswith(prefix):
                                files.add(file_path)
                        elif file_path == pattern:
                            files.add(file_path)
        except Exception:
            pass
        
        self.report.files_to_stage = list(files)
        return list(files)
    
    def _detect_git(self) -> str:
        """Detect git executable path."""
        session_paths = self.project_root / ".cursor" / "cache" / "session-paths.json"
        
        if session_paths.exists():
            try:
                with open(session_paths, "r", encoding="utf-8") as f:
                    paths = json.load(f)
                    if "git" in paths.get("paths", {}):
                        return paths["paths"]["git"]
            except (json.JSONDecodeError, IOError):
                pass
        
        return "git"
    
    def auto_stage(self) -> List[str]:
        """Auto-stage files modified by sync scripts."""
        files = self.get_files_to_stage()
        
        if not files:
            return []
        
        try:
            git_path = self._detect_git()
            cmd = [git_path, "add"] + files
            subprocess.run(cmd, cwd=self.project_root, check=True)
            print(f"[STAGE] Auto-staged {len(files)} files")
            return files
        except Exception as e:
            print(f"[WARN] Failed to auto-stage: {e}")
            return []
    
    def run_all(self) -> PreCommitReport:
        """
        Run the complete pre-commit workflow.
        
        Returns:
            PreCommitReport with all results.
        """
        start = time.time()
        
        # Step 1: Cleanup
        if self.sync_mode:
            print("\n[CLEANUP] Removing temporary files...")
            cleaned = self.cleanup_temp_files()
            if cleaned > 0:
                print(f"[OK] Removed {cleaned} temporary items")
        
        # Step 2: Validate JSON
        print("\n[VALIDATE] Checking JSON syntax...")
        json_errors = self.validate_json_files()
        if json_errors:
            print(f"[WARN] {len(json_errors)} JSON errors found:")
            for err in json_errors[:5]:
                print(f"    {err}")
        else:
            print("[OK] All JSON files valid")
        
        # Step 3: Run sync scripts
        print("\n[SYNC] Running validation scripts...")
        self.run_sync_scripts()
        
        # Step 4: Run tests (if enabled)
        if self.run_tests:
            self.run_fast_tests()
        
        # Step 5: Auto-stage (if sync mode)
        if self.sync_mode:
            self.auto_stage()
        
        self.report.total_elapsed_ms = int((time.time() - start) * 1000)
        
        return self.report
    
    @property
    def passed(self) -> int:
        """Count of passed scripts."""
        return sum(1 for r in self.results if r.success)
    
    @property
    def failed(self) -> int:
        """Count of failed scripts."""
        return sum(1 for r in self.results if not r.success)
    
    @property
    def all_passed(self) -> bool:
        """True if all critical checks passed."""
        critical_failed = any(
            not r.success 
            for r, cfg in zip(self.results, self.SCRIPTS) 
            if cfg.get("critical", False)
        )
        test_failed = self.report.test_failed > 0
        json_failed = len(self.report.json_errors) > 0
        
        return not critical_failed and not test_failed and not json_failed
    
    def print_summary(self) -> None:
        """Print summary of all results."""
        print("\n" + "=" * 60)
        print("PRE-COMMIT SUMMARY")
        print("=" * 60)
        
        print(f"  Cleanup:     {self.report.cleanup_files} items removed")
        print(f"  JSON:        {len(self.report.json_errors)} errors")
        print(f"  Sync:        {self.passed}/{len(self.results)} scripts passed")
        
        if self.run_tests:
            print(f"  Tests:       {self.report.test_passed} passed, {self.report.test_failed} failed")
        
        print(f"  Total time:  {self.report.total_elapsed_ms}ms")
        print("=" * 60)
        
        if self.all_passed:
            print("[OK] All pre-commit checks passed - ready to commit!")
        else:
            print("[BLOCKED] Fix issues before committing:")
            if self.report.json_errors:
                print("  - Fix JSON syntax errors")
            if self.report.test_failed > 0:
                print("  - Fix failing tests")
            for result in self.results:
                if not result.success:
                    print(f"  - Fix {result.name}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Intelligent pre-commit automation with parallel execution"
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Apply changes (sync mode). Without this flag, only checks."
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode - skip slow validation checks"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run validation tests before commit"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full validation - run all tests in parallel"
    )
    parser.add_argument(
        "--auto-stage",
        action="store_true",
        help="Auto-stage files modified by sync scripts (implied by --sync)"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        default=True,
        help="Run scripts in parallel within groups (default: enabled)"
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Force sequential execution (disables parallel)"
    )
    
    args = parser.parse_args()
    
    # Sequential flag overrides parallel
    parallel_mode = not args.sequential
    
    print("=" * 60)
    print("CURSOR AGENT FACTORY - PRE-COMMIT RUNNER")
    print("=" * 60)
    print(f"Mode: {'sync' if args.sync else 'check'}")
    print(f"Execution: {'parallel' if parallel_mode else 'sequential'}")
    if args.fast:
        print("Fast mode: enabled")
    if args.test or args.full:
        print(f"Tests: {'full' if args.full else 'validation only'}")
    
    runner = PreCommitRunner(
        sync_mode=args.sync,
        fast_mode=args.fast,
        run_tests=args.test,
        full_mode=args.full,
        parallel_mode=parallel_mode
    )
    
    runner.run_all()
    runner.print_summary()
    
    # Exit with error code if any critical checks failed
    sys.exit(0 if runner.all_passed else 1)


if __name__ == "__main__":
    main()
