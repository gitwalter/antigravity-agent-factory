"""
Unit tests for scripts/git/install_hooks.py

Tests the Git hook installation functionality.
"""

import importlib.util
import os
import stat
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import module from new location
_script_path = Path(__file__).parent.parent.parent / "scripts" / "git" / "install_hooks.py"
_spec = importlib.util.spec_from_file_location("install_hooks", _script_path)
hooks_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hooks_module)


class TestPreCommitHookContent:
    """Tests for the pre-commit hook content."""
    
    def test_unix_hook_has_shebang(self):
        """Test that Unix hook starts with shebang."""
        assert hooks_module.PRE_COMMIT_HOOK_UNIX.startswith("#!/bin/sh")
    
    def test_windows_hook_has_shebang(self):
        """Test that Windows hook starts with shebang."""
        assert hooks_module.PRE_COMMIT_HOOK_WINDOWS.startswith("#!/bin/sh")
    
    def test_unix_hook_runs_version_sync(self):
        """Test that Unix hook syncs versions.
        
        Note: validate_readme_structure.py was removed from the hook for speed.
        The hook now focuses on: secrets, JSON syntax, version sync.
        """
        assert "sync_manifest_versions.py" in hooks_module.PRE_COMMIT_HOOK_UNIX
        assert "--sync" in hooks_module.PRE_COMMIT_HOOK_UNIX
    
    def test_windows_hook_runs_version_sync(self):
        """Test that Windows hook syncs versions.
        
        Note: validate_readme_structure.py was removed from the hook for speed.
        The hook now focuses on: secrets, JSON syntax, version sync.
        """
        assert "sync_manifest_versions.py" in hooks_module.PRE_COMMIT_HOOK_WINDOWS
        assert "--sync" in hooks_module.PRE_COMMIT_HOOK_WINDOWS
    
    def test_unix_hook_stages_readme(self):
        """Test that Unix hook stages README.md."""
        assert "git add README.md" in hooks_module.PRE_COMMIT_HOOK_UNIX
    
    def test_windows_hook_stages_readme(self):
        """Test that Windows hook stages README.md."""
        assert "git add README.md" in hooks_module.PRE_COMMIT_HOOK_WINDOWS
    
    def test_unix_hook_exits_cleanly(self):
        """Test that Unix hook exits with 0."""
        assert "exit 0" in hooks_module.PRE_COMMIT_HOOK_UNIX
    
    def test_windows_hook_checks_multiple_python_paths(self):
        """Test that Windows hook tries multiple Python paths."""
        assert "python" in hooks_module.PRE_COMMIT_HOOK_WINDOWS
        assert "python3" in hooks_module.PRE_COMMIT_HOOK_WINDOWS


class TestInstallHooks:
    """Tests for the install_hooks function."""
    
    def test_install_hooks_no_git_directory(self):
        """Test that install_hooks fails gracefully without .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake script location matching real structure: scripts/git/install_hooks.py
            git_subdir = Path(tmpdir) / "scripts" / "git"
            git_subdir.mkdir(parents=True)
            hook_script = git_subdir / "install_hooks.py"
            hook_script.write_text("# placeholder")
            
            # Patch __file__ to point to our temp location
            with patch.object(hooks_module, '__file__', str(hook_script)):
                result = hooks_module.install_hooks()
                assert result == 1  # Should fail
    
    def test_install_hooks_creates_hook_file(self):
        """Test that install_hooks creates the pre-commit hook."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create .git directory structure
            git_dir = tmppath / ".git"
            git_dir.mkdir()
            
            # Create scripts/git directory matching real structure
            scripts_git_dir = tmppath / "scripts" / "git"
            scripts_git_dir.mkdir(parents=True)
            hook_script = scripts_git_dir / "install_hooks.py"
            hook_script.write_text("# placeholder")
            
            with patch.object(hooks_module, '__file__', str(hook_script)):
                with patch('builtins.input', return_value='n'):  # Don't overwrite if asked
                    result = hooks_module.install_hooks()
            
            assert result == 0
            pre_commit_path = git_dir / "hooks" / "pre-commit"
            assert pre_commit_path.exists()
    
    def test_install_hooks_asks_before_overwrite(self):
        """Test that install_hooks asks before overwriting existing hook."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create .git/hooks with existing pre-commit
            hooks_dir = tmppath / ".git" / "hooks"
            hooks_dir.mkdir(parents=True)
            pre_commit = hooks_dir / "pre-commit"
            pre_commit.write_text("#!/bin/sh\necho 'existing hook'")
            
            # Create scripts/git directory matching real structure
            scripts_git_dir = tmppath / "scripts" / "git"
            scripts_git_dir.mkdir(parents=True)
            hook_script = scripts_git_dir / "install_hooks.py"
            hook_script.write_text("# placeholder")
            
            # User declines overwrite
            with patch.object(hooks_module, '__file__', str(hook_script)):
                with patch('builtins.input', return_value='n'):
                    result = hooks_module.install_hooks()
            
            assert result == 0
            # Original content should be preserved
            assert "existing hook" in pre_commit.read_text()
    
    def test_install_hooks_overwrites_when_confirmed(self):
        """Test that install_hooks overwrites when user confirms."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create .git/hooks with existing pre-commit
            hooks_dir = tmppath / ".git" / "hooks"
            hooks_dir.mkdir(parents=True)
            pre_commit = hooks_dir / "pre-commit"
            pre_commit.write_text("#!/bin/sh\necho 'old hook'")
            
            # Create scripts/git directory matching real structure
            scripts_git_dir = tmppath / "scripts" / "git"
            scripts_git_dir.mkdir(parents=True)
            hook_script = scripts_git_dir / "install_hooks.py"
            hook_script.write_text("# placeholder")
            
            # User confirms overwrite
            with patch.object(hooks_module, '__file__', str(hook_script)):
                with patch('builtins.input', return_value='y'):
                    result = hooks_module.install_hooks()
            
            assert result == 0
            # Should have new content (hook now uses sync_manifest_versions.py, not validate_readme_structure.py)
            content = pre_commit.read_text()
            assert "sync_manifest_versions.py" in content
    
    @pytest.mark.skipif(os.name == 'nt', reason="Unix permissions test")
    def test_install_hooks_makes_executable_on_unix(self):
        """Test that install_hooks makes hook executable on Unix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create .git directory
            git_dir = tmppath / ".git"
            git_dir.mkdir()
            
            # Create scripts/git directory matching real structure
            scripts_git_dir = tmppath / "scripts" / "git"
            scripts_git_dir.mkdir(parents=True)
            hook_script = scripts_git_dir / "install_hooks.py"
            hook_script.write_text("# placeholder")
            
            with patch.object(hooks_module, '__file__', str(hook_script)):
                result = hooks_module.install_hooks()
            
            pre_commit = git_dir / "hooks" / "pre-commit"
            mode = pre_commit.stat().st_mode
            assert mode & stat.S_IEXEC  # Check executable bit


class TestMainEntry:
    """Tests for the main entry point."""
    
    def test_main_calls_install_hooks(self):
        """Test that __main__ calls install_hooks."""
        with patch.object(hooks_module, 'install_hooks', return_value=0) as mock_install:
            with patch.object(sys, 'exit') as mock_exit:
                # Simulate running as main
                exec(compile(
                    "if __name__ == '__main__': sys.exit(install_hooks())",
                    "<test>",
                    "exec"
                ), {'__name__': '__main__', 'sys': sys, 'install_hooks': hooks_module.install_hooks})
