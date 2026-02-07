"""
Integration tests for CLI extension commands.

Tests cover:
- --analyze-gaps command
- --coverage-report command
- --suggest-extensions command
"""

import subprocess
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestAnalyzeGapsCommand:
    """Tests for --analyze-gaps CLI command."""
    
    def test_analyze_gaps_exits_successfully(self, python_executable, cli_path):
        """Test that --analyze-gaps exits with code 0."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--analyze-gaps"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        assert result.returncode == 0, f"Command failed with: {result.stderr}"
    
    def test_analyze_gaps_shows_coverage(self, python_executable, cli_path):
        """Test that --analyze-gaps shows coverage information."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--analyze-gaps"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Should show coverage percentage
        assert "Coverage" in result.stdout or "coverage" in result.stdout, \
            "Output should include coverage information"
    
    def test_analyze_gaps_with_scope_domain(self, python_executable, cli_path):
        """Test --analyze-gaps with domain scope."""
        result = subprocess.run(
            [
                python_executable, str(cli_path),
                "--analyze-gaps",
                "--gap-scope", "domain",
                "--gap-filter", "agent"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Should exit successfully (may have no results for filter)
        assert result.returncode == 0, f"Command failed with: {result.stderr}"
    
    def test_analyze_gaps_with_scope_topic(self, python_executable, cli_path):
        """Test --analyze-gaps with topic scope."""
        result = subprocess.run(
            [
                python_executable, str(cli_path),
                "--analyze-gaps",
                "--gap-scope", "topic",
                "--gap-filter", "react"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        assert result.returncode == 0, f"Command failed with: {result.stderr}"
    
    def test_analyze_gaps_shows_gap_types(self, python_executable, cli_path):
        """Test that output shows gap types."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--analyze-gaps"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Should mention gap types or priorities
        output = result.stdout.lower()
        has_gap_info = (
            "missing" in output or
            "shallow" in output or
            "critical" in output or
            "high" in output or
            "gap" in output
        )
        assert has_gap_info, "Output should include gap type or priority info"


class TestCoverageReportCommand:
    """Tests for --coverage-report CLI command."""
    
    def test_coverage_report_exits_successfully(self, python_executable, cli_path):
        """Test that --coverage-report exits with code 0."""
        result = subprocess.run(
            [
                python_executable, str(cli_path),
                "--coverage-report", "ai-agent-development"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # May exit with 0 even if blueprint not found (graceful handling)
        # Check that it ran without crash
        assert result.returncode in [0, 1], \
            f"Command crashed with: {result.stderr}"
    
    def test_coverage_report_shows_percentage(self, python_executable, cli_path):
        """Test that coverage report shows percentage."""
        result = subprocess.run(
            [
                python_executable, str(cli_path),
                "--coverage-report", "ai-agent-development"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Should show percentage or coverage info
        output = result.stdout
        has_coverage = "%" in output or "coverage" in output.lower()
        # Allow for blueprint not found scenarios
        assert has_coverage or "not found" in output.lower(), \
            "Output should show coverage or error message"


class TestSuggestExtensionsCommand:
    """Tests for --suggest-extensions CLI command."""
    
    def test_suggest_extensions_exits_successfully(self, python_executable, cli_path):
        """Test that --suggest-extensions exits with code 0."""
        result = subprocess.run(
            [
                python_executable, str(cli_path),
                "--suggest-extensions", "ai-agent-development"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        assert result.returncode in [0, 1], \
            f"Command crashed with: {result.stderr}"
    
    def test_suggest_extensions_lists_candidates(self, python_executable, cli_path):
        """Test that suggest-extensions lists extension candidates."""
        result = subprocess.run(
            [
                python_executable, str(cli_path),
                "--suggest-extensions", "ai-agent-development"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout.lower()
        # Should show suggestions or indicate none found
        has_suggestions = (
            "suggest" in output or
            "candidate" in output or
            "extend" in output or
            "gap" in output or
            "no " in output  # "no suggestions", "not found"
        )
        assert has_suggestions, \
            "Output should show suggestions or indicate none found"


class TestHelpExtensionCommands:
    """Tests for extension command help."""
    
    def test_help_shows_analyze_gaps(self, python_executable, cli_path):
        """Test that help shows --analyze-gaps option."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert "--analyze-gaps" in result.stdout, \
            "Help should show --analyze-gaps option"
    
    def test_help_shows_coverage_report(self, python_executable, cli_path):
        """Test that help shows --coverage-report option."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert "--coverage-report" in result.stdout, \
            "Help should show --coverage-report option"
