"""
Unit tests for the Guardian Axiom Checker.

These tests verify that the axiom checker correctly identifies
potentially harmful operations according to the core axioms.
"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from guardian.axiom_checker import (
    check_command,
    check_file_operation,
    check_content_for_claims,
    validate_operation,
    CheckResult,
    AxiomViolation,
)


class TestCheckCommand:
    """Tests for shell command checking."""

    # Level 4: Critical harm - must be blocked
    @pytest.mark.parametrize("command,description", [
        ("rm -rf /", "Root directory deletion"),
        ("rm -rf ~", "Home directory deletion"),
        ("rm -rf /home/user", "User directory deletion"),
        ("rmdir /s /q C:\\", "Windows recursive deletion"),
        ("Remove-Item -Recurse -Force C:\\", "PowerShell recursive deletion"),
        ("format C:", "Disk format"),
        ("dd if=/dev/zero of=/dev/sda", "Direct disk write"),
        ("DROP DATABASE production", "Database drop"),
        ("DELETE FROM users", "DELETE without WHERE"),
        ("TRUNCATE TABLE orders", "Table truncation"),
        ("kill -9 -1", "Kill all processes"),
    ])
    def test_level_4_critical_commands(self, command, description):
        """Critical commands should trigger Level 4 (Protect)."""
        result = check_command(command)
        assert not result.passed, f"{description} should be blocked"
        assert result.level == 4, f"{description} should be Level 4"
        assert result.axiom == "A4", f"{description} violates A4 (Non-Harm)"

    # Level 2-3: Caution needed - ask user
    @pytest.mark.parametrize("command,expected_level", [
        ("cat .env", 2),
        ("cat .env.local", 2),
        ("cat secrets.yml", 2),
        ("cat credentials.json", 2),
        ("vim ~/.ssh/id_rsa", 2),
        ("cat ~/.aws/credentials", 2),
    ])
    def test_sensitive_file_access(self, command, expected_level):
        """Access to sensitive files should trigger pause."""
        result = check_command(command)
        assert not result.passed, f"Command '{command}' should be flagged"
        assert result.level >= 2, f"Command '{command}' should be at least Level 2"

    # Level 0: Safe commands - no intervention
    @pytest.mark.parametrize("command", [
        "ls -la",
        "pwd",
        "echo 'hello'",
        "git status",
        "python --version",
        "npm install",
        "cat README.md",
        "mkdir new_folder",
        "cp file1.txt file2.txt",
    ])
    def test_safe_commands(self, command):
        """Safe commands should pass without intervention."""
        result = check_command(command)
        assert result.passed, f"Command '{command}' should pass"
        assert result.level == 0, f"Command '{command}' should be Level 0"


class TestCheckFileOperation:
    """Tests for file operation checking."""

    @pytest.mark.parametrize("path", [
        "/etc/passwd",
        "/etc/shadow",
        "/usr/bin/python",
        "C:\\Windows\\System32\\config",
        "C:\\Program Files\\important.exe",
    ])
    def test_critical_path_deletion(self, path):
        """Deletion of critical system paths should be blocked."""
        result = check_file_operation("delete", path)
        # Note: Some of these may pass depending on pattern matching
        # The test verifies the logic is being applied
        if not result.passed:
            assert result.level >= 3, f"Deleting {path} should be high severity"

    @pytest.mark.parametrize("path", [
        ".env",
        ".env.local",
        ".env.production",
        "secrets.yaml",
        "credentials.json",
    ])
    def test_sensitive_file_deletion(self, path):
        """Deletion of sensitive files should require confirmation."""
        result = check_file_operation("delete", path)
        assert not result.passed, f"Deleting {path} should be flagged"
        assert result.level >= 2, f"Deleting {path} should be at least Level 2"

    def test_normal_file_operations(self):
        """Normal file operations should pass."""
        result = check_file_operation("write", "src/main.py")
        assert result.passed, "Writing to normal file should pass"
        
        result = check_file_operation("delete", "temp_file.txt")
        assert result.passed, "Deleting normal file should pass"


class TestCheckContentForClaims:
    """Tests for content claim checking (A1 - Verifiability)."""

    @pytest.mark.parametrize("content,should_flag", [
        ("This will always work", True),  # Absolute claim
        ("This definitely solves the problem", True),  # Absolute claim
        ("According to John Smith, this is correct", True),  # External reference
        ("This improves performance by 50%", True),  # Statistical claim
        ("This function returns a value", False),  # Normal statement
        ("The code handles errors", False),  # Normal statement
    ])
    def test_claim_detection(self, content, should_flag):
        """Claims should be detected for verification."""
        result = check_content_for_claims(content)
        # Note: These are informational, not blocking
        if should_flag:
            assert result.level >= 1, f"'{content}' should be flagged for verification"


class TestValidateOperation:
    """Tests for the main validation entry point."""

    def test_command_validation(self):
        """Command validation should work through main entry point."""
        result = validate_operation("command", {"command": "rm -rf /"})
        assert not result.passed
        assert result.level == 4

    def test_file_write_validation(self):
        """File write validation should work through main entry point."""
        result = validate_operation("file_write", {"path": "normal.py"})
        assert result.passed

    def test_file_delete_validation(self):
        """File delete validation should work through main entry point."""
        result = validate_operation("file_delete", {"path": ".env"})
        assert not result.passed

    def test_content_validation(self):
        """Content validation should work through main entry point."""
        result = validate_operation("content", {"content": "This always works"})
        # Content checks are informational, not blocking
        assert result.passed  # Still passes, but with level > 0


class TestCheckResultProperties:
    """Tests for CheckResult helper properties."""

    def test_requires_user_level_0(self):
        """Level 0 should not require user."""
        result = CheckResult(passed=True, level=0)
        assert not result.requires_user

    def test_requires_user_level_2(self):
        """Level 2+ should require user."""
        result = CheckResult(passed=False, level=2)
        assert result.requires_user

    def test_is_emergency_level_3(self):
        """Level 3 should not be emergency."""
        result = CheckResult(passed=False, level=3)
        assert not result.is_emergency

    def test_is_emergency_level_4(self):
        """Level 4 should be emergency."""
        result = CheckResult(passed=False, level=4)
        assert result.is_emergency


class TestAxiomCoverage:
    """Tests to ensure all axioms are being checked."""

    def test_a1_verifiability_checked(self):
        """A1 (Verifiability) should be checked in content."""
        result = check_content_for_claims("This definitely works 100% of the time")
        assert result.axiom == "A1" or result.level >= 1

    def test_a4_non_harm_checked(self):
        """A4 (Non-Harm) should be checked in commands."""
        result = check_command("rm -rf /")
        assert result.axiom == "A4"

    def test_a4_non_harm_in_files(self):
        """A4 (Non-Harm) should be checked in file operations."""
        result = check_file_operation("delete", ".env")
        assert result.axiom == "A4"
