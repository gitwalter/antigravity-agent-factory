"""
Unit tests for the Guardian Secret Scanner.

These tests verify that the secret scanner correctly identifies
credentials and secrets in content to prevent accidental exposure.
"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from guardian.secret_scanner import (
    scan_content,
    scan_file,
    scan_diff,
    get_severity_level,
    redact_secret,
    is_false_positive,
    SecretMatch,
)


class TestScanContent:
    """Tests for content scanning."""

    # High severity secrets - must be detected
    @pytest.mark.parametrize("content,secret_type", [
        ('api_key = "sk-1234567890abcdefghijklmnopqrstuv"', "OpenAI API Key"),
        ('key = "sk-proj-abcdefghijklmnopqrstuvwxyz"', "OpenAI Project API Key"),        ('AWS_KEY = "AKIAIOSFODNN7A1B2C3D"', "AWS Access Key ID"),  # Valid format, no "EXAMPLE"
        ('token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"', "GitHub Personal Access Token"),
        ('GITLAB_TOKEN = "glpat-Abc123Def456Ghi789Jkl"', "GitLab Personal Access Token"),  # Realistic
        ('SENDGRID_KEY = "SG.1234567890abcdefghijkl.12345678901234567890123456789012345678901234"', "SendGrid API Key"),
        ('GOOGLE_API = "AIzaSyC1234567890abcdefghijk"', "Google API Key"),  # 27 chars after AIza
    ])
    def test_high_severity_api_keys(self, content, secret_type):
        """High severity API keys should be detected."""
        matches = scan_content(content)
        assert len(matches) >= 1, f"{secret_type} should be detected"
        assert any(m.severity == "high" for m in matches), f"{secret_type} should be high severity"

    # Private keys - must be detected
    @pytest.mark.parametrize("content", [
        "-----BEGIN RSA PRIVATE KEY-----",        "-----BEGIN PRIVATE KEY-----",
        "-----BEGIN EC PRIVATE KEY-----",
        "-----BEGIN OPENSSH PRIVATE KEY-----",
        "-----BEGIN PGP PRIVATE KEY BLOCK-----",
    ])
    def test_private_keys(self, content):
        """Private keys should be detected as high severity."""
        matches = scan_content(content)
        assert len(matches) >= 1, "Private key should be detected"
        assert matches[0].severity == "high", "Private key should be high severity"

    # Database connection strings - must be detected
    @pytest.mark.parametrize("content,db_type", [
        ('DATABASE_URL = "postgres://user:password@localhost/db"', "PostgreSQL"),        ('MONGO_URI = "mongodb://admin:secret@localhost/mydb"', "MongoDB"),
        ('MYSQL_URL = "mysql://root:pass123@localhost/app"', "MySQL"),
        ('REDIS_URL = "redis://user:secret@localhost:6379"', "Redis"),
    ])
    def test_database_connection_strings(self, content, db_type):
        """Database connection strings should be detected."""
        matches = scan_content(content)
        assert len(matches) >= 1, f"{db_type} connection string should be detected"
        assert any(m.severity == "high" for m in matches), f"{db_type} should be high severity"

    # Medium severity - should be detected but may be intentional
    @pytest.mark.parametrize("content", [
        'password = "mysecretpassword123"',
        'api_key = "1234567890abcdefghij"',
        'secret = "this_is_my_secret_value"',
    ])
    def test_medium_severity_patterns(self, content):
        """Medium severity patterns should be detected."""
        matches = scan_content(content)
        assert len(matches) >= 1, "Pattern should be detected"
        # At least one should be medium or higher
        assert any(m.severity in ["medium", "high"] for m in matches)

    # False positives - should NOT be detected
    @pytest.mark.parametrize("content", [
        'api_key = "your-api-key-here"',
        'secret = "placeholder"',
        'token = "example-token"',
        'password = "xxxxxxxxxx"',
        'key = "${API_KEY}"',
        'secret = "<your-secret>"',
    ])
    def test_false_positives_filtered(self, content):
        """Placeholder values should not be detected as secrets."""
        matches = scan_content(content)
        # Should either be empty or filtered out
        assert len(matches) == 0 or all(
            is_false_positive(m.matched_text) for m in matches
        ), f"'{content}' should be filtered as false positive"

    def test_multiline_content(self):
        """Scanner should handle multiline content correctly."""
        content = """
        # Configuration
        DEBUG = True
        API_KEY = "sk-1234567890abcdefghijklmnopqrstuv"
        DATABASE_URL = "postgres://user:pass@localhost/db"        """
        matches = scan_content(content)
        assert len(matches) >= 2, "Should detect multiple secrets"
        
        # Check line numbers are correct
        line_numbers = {m.line_number for m in matches}
        assert len(line_numbers) >= 2, "Secrets should be on different lines"


class TestRedactSecret:
    """Tests for secret redaction."""

    def test_short_secret(self):
        """Short secrets should be fully redacted."""
        assert redact_secret("abc") == "***"
        assert redact_secret("12345678") == "********"

    def test_long_secret(self):
        """Long secrets should show first and last 4 chars."""
        result = redact_secret("sk-1234567890abcdefghijklmnopqrstuv")
        assert result.startswith("sk-1")
        assert result.endswith("stuv")
        assert "*" in result


class TestIsFalsePositive:
    """Tests for false positive detection."""

    @pytest.mark.parametrize("text,expected", [
        ("your-api-key-here", True),
        ("example-token", True),
        ("placeholder", True),
        ('"xxxxxxxxxx"', True),  # Needs quotes for the pattern to match
        ("${API_KEY}", True),
        ("<your-secret>", True),
        ("sk-1234567890abcdef", False),
        ("ghp_realtoken12345", False),
    ])
    def test_false_positive_patterns(self, text, expected):
        """False positive patterns should be correctly identified."""
        assert is_false_positive(text) == expected


class TestScanDiff:
    """Tests for git diff scanning."""

    def test_only_added_lines_checked(self):
        """Only added lines (starting with +) should be checked."""
        diff = """
diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,3 +1,4 @@
 DEBUG = True
-OLD_KEY = "sk-oldkey12345678901234567890123456"
+API_KEY = "sk-newkey12345678901234567890123456"
+PASSWORD = "secretpass123456"
"""
        matches = scan_diff(diff)
        # Should find secrets in added lines
        assert len(matches) >= 1, "Should detect secrets in added lines"

    def test_removed_lines_ignored(self):
        """Removed lines (starting with -) should not be checked."""
        diff = """
-SECRET_KEY = "sk-1234567890abcdefghijklmnopqrstuv"
"""
        matches = scan_diff(diff)
        assert len(matches) == 0, "Removed lines should not trigger detection"


class TestGetSeverityLevel:
    """Tests for severity to Guardian level mapping."""

    def test_no_matches(self):
        """No matches should return Level 0."""
        assert get_severity_level([]) == 0

    def test_high_severity(self):
        """High severity should return Level 4."""
        matches = [SecretMatch("test", "secret", 1, "high", "****")]
        assert get_severity_level(matches) == 4

    def test_medium_severity(self):
        """Medium severity should return Level 3."""
        matches = [SecretMatch("test", "secret", 1, "medium", "****")]
        assert get_severity_level(matches) == 3

    def test_low_severity(self):
        """Low severity should return Level 2."""
        matches = [SecretMatch("test", "secret", 1, "low", "****")]
        assert get_severity_level(matches) == 2

    def test_mixed_severity(self):
        """Mixed severity should return highest level."""
        matches = [
            SecretMatch("test", "secret1", 1, "low", "****"),
            SecretMatch("test", "secret2", 2, "high", "****"),
        ]
        assert get_severity_level(matches) == 4


class TestScanFile:
    """Tests for file scanning."""

    def test_scan_nonexistent_file(self):
        """Scanning nonexistent file should return empty list."""
        matches = scan_file("/nonexistent/path/file.txt")
        assert matches == []

    def test_skip_binary_files(self):
        """Binary files should be skipped."""
        for ext in [".exe", ".dll", ".png", ".jpg", ".zip"]:
            matches = scan_file(f"test{ext}")
            assert matches == [], f"Binary file {ext} should be skipped"
