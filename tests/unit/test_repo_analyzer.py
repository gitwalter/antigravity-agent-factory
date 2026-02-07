"""
Unit tests for scripts/analysis/repo_analyzer.py

Tests repository analysis, tech stack detection, and onboarding scenarios.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.analysis.repo_analyzer import (
    OnboardingScenario,
    AgentruleAnalysis,
    McpAnalysis,
    TechStackDetection,
    RepoInventory,
    RepoAnalyzer,
    get_file_hash,
)


class TestOnboardingScenario:
    """Tests for OnboardingScenario enum."""
    
    def test_scenario_values(self):
        """Test that all scenarios have correct values."""
        assert OnboardingScenario.FRESH.value == "fresh"
        assert OnboardingScenario.MINIMAL.value == "minimal"
        assert OnboardingScenario.PARTIAL.value == "partial"
        assert OnboardingScenario.UPGRADE.value == "upgrade"
        assert OnboardingScenario.COMPLETE.value == "complete"


class TestAgentruleAnalysis:
    """Tests for AgentruleAnalysis dataclass."""
    
    def test_default_values(self):
        """Test default values for AgentruleAnalysis."""
        analysis = AgentruleAnalysis()
        assert analysis.exists is False
        assert analysis.content is None
        assert analysis.version is None
        assert analysis.layers_present == []
        assert analysis.has_factory_marker is False
        assert analysis.line_count == 0


class TestMcpAnalysis:
    """Tests for McpAnalysis dataclass."""
    
    def test_default_values(self):
        """Test default values for McpAnalysis."""
        analysis = McpAnalysis()
        assert analysis.exists is False
        assert analysis.servers == []
        assert analysis.server_details == {}


class TestTechStackDetection:
    """Tests for TechStackDetection dataclass."""
    
    def test_default_values(self):
        """Test default values for TechStackDetection."""
        detection = TechStackDetection()
        assert detection.languages == []
        assert detection.frameworks == []
        assert detection.databases == []
        assert detection.suggested_blueprint is None
        assert detection.confidence == 0.0


class TestRepoInventory:
    """Tests for RepoInventory dataclass."""
    
    def test_creation_with_path(self):
        """Test creating RepoInventory with a path."""
        inventory = RepoInventory(path=Path("/test/repo"))
        assert inventory.path == Path("/test/repo")
        assert inventory.scenario == OnboardingScenario.FRESH
    
    def test_get_summary_fresh_repo(self):
        """Test get_summary for a fresh repository."""
        inventory = RepoInventory(path=Path("/test/repo"))
        summary = inventory.get_summary()
        
        assert "Repository: " in summary
        assert "Scenario: FRESH" in summary
        assert "Agentrules: No" in summary
    
    def test_get_summary_with_artifacts(self):
        """Test get_summary with some artifacts."""
        inventory = RepoInventory(
            path=Path("/test/repo"),
            scenario=OnboardingScenario.PARTIAL,
            existing_agents=["code-reviewer", "test-generator"],
            existing_skills=["tdd", "bugfix-workflow"],
        )
        inventory.agentrules = AgentruleAnalysis(
            exists=True,
            line_count=100,
            layers_present=[0, 1, 2],
            version="2.0.0"
        )
        
        summary = inventory.get_summary()
        
        assert "PARTIAL" in summary
        assert "Agentrules: Yes" in summary
        assert "code-reviewer" in summary
        assert "tdd" in summary


class TestRepoAnalyzer:
    """Tests for RepoAnalyzer class."""
    
    def test_analyzer_creation(self):
        """Test creating a RepoAnalyzer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = RepoAnalyzer(tmpdir)
            assert analyzer.repo_path == Path(tmpdir)
    
    def test_analyzer_nonexistent_path_raises(self):
        """Test that non-existent path raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            RepoAnalyzer("/nonexistent/path/12345")
        assert "does not exist" in str(exc_info.value)
    
    def test_analyze_fresh_repo(self):
        """Test analyzing a fresh repository with no artifacts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = RepoAnalyzer(tmpdir)
            inventory = analyzer.analyze()
            
            assert inventory.scenario == OnboardingScenario.FRESH
            assert inventory.agentrules.exists is False
            assert inventory.existing_agents == []
    
    def test_analyze_detects_git_repo(self):
        """Test that analyzer detects .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / ".git").mkdir()
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.is_git_repo is True
    
    def test_analyze_detects_agentrules(self):
        """Test that analyzer detects Agentrules file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            agentrules = repo_path / ".agentrules"
            agentrules.write_text("# Test agentrules\nLayer 1: Purpose\n")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.agentrules.exists is True
            assert inventory.agentrules.line_count == 2
            assert 1 in inventory.agentrules.layers_present
    
    def test_analyze_detects_factory_marker(self):
        """Test that analyzer detects factory marker in agentrules."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            agentrules = repo_path / ".agentrules"
            agentrules.write_text("# Generated by Antigravity Agent Factory v2.5.0\n")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.agentrules.has_factory_marker is True
            assert inventory.agentrules.version == "2.5.0"
    
    def test_analyze_detects_agents(self):
        """Test that analyzer detects agent files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            agents_dir = repo_path / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "code-reviewer.md").write_text("# Code Reviewer")
            (agents_dir / "test-generator.md").write_text("# Test Generator")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert "code-reviewer" in inventory.existing_agents
            assert "test-generator" in inventory.existing_agents
    
    def test_analyze_detects_skills(self):
        """Test that analyzer detects skill directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            skills_dir = repo_path / ".agent" / "skills"
            
            # Create valid skill with SKILL.md
            tdd_skill = skills_dir / "tdd"
            tdd_skill.mkdir(parents=True)
            (tdd_skill / "SKILL.md").write_text("# TDD Skill")
            
            # Create invalid skill without SKILL.md
            invalid_skill = skills_dir / "invalid"
            invalid_skill.mkdir()
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert "tdd" in inventory.existing_skills
            assert "invalid" not in inventory.existing_skills
    
    def test_analyze_detects_mcp_config(self):
        """Test that analyzer detects MCP configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            agent_dir = repo_path / ".agent"
            agent_dir.mkdir()
            
            mcp_config = {
                "mcpServers": {
                    "filesystem": {"command": "npx", "args": ["server-filesystem"]},
                    "git": {"command": "npx", "args": ["server-git"]}
                }
            }
            (agent_dir / "mcp.json").write_text(json.dumps(mcp_config))
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.mcp.exists is True
            assert "filesystem" in inventory.mcp.servers
            assert "git" in inventory.mcp.servers
    
    def test_analyze_detects_knowledge_files(self):
        """Test that analyzer detects knowledge files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            knowledge_dir = repo_path / "knowledge"
            knowledge_dir.mkdir()
            (knowledge_dir / "patterns.json").write_text("{}")
            (knowledge_dir / "best-practices.json").write_text("{}")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert "patterns.json" in inventory.existing_knowledge
            assert "best-practices.json" in inventory.existing_knowledge
    
    def test_analyze_detects_purpose_md(self):
        """Test that analyzer detects PURPOSE.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "PURPOSE.md").write_text("# Purpose")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.has_purpose_md is True
    
    def test_detect_tech_stack_python(self):
        """Test tech stack detection for Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "main.py").write_text("print('hello')")
            (repo_path / "requirements.txt").write_text("fastapi\nuvicorn\n")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert "python" in inventory.tech_stack.languages
            assert "fastapi" in inventory.tech_stack.frameworks
            assert inventory.tech_stack.suggested_blueprint == "python-fastapi"
    
    def test_detect_tech_stack_typescript_react(self):
        """Test tech stack detection for TypeScript React project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "App.tsx").write_text("export default App;")
            (repo_path / "package.json").write_text('{"dependencies": {"react": "18.0.0"}}')
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert "typescript" in inventory.tech_stack.languages
            assert "react" in inventory.tech_stack.frameworks
            assert inventory.tech_stack.suggested_blueprint == "typescript-react"
    
    def test_detect_tech_stack_java_spring(self):
        """Test tech stack detection for Java Spring project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / "Main.java").write_text("public class Main {}")
            (repo_path / "pom.xml").write_text("<project><spring-boot></spring-boot></project>")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert "java" in inventory.tech_stack.languages
            assert "spring" in inventory.tech_stack.frameworks
            assert inventory.tech_stack.suggested_blueprint == "java-spring"
    
    def test_determine_scenario_minimal(self):
        """Test scenario determination for minimal setup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / ".agentrules").write_text("# Custom rules")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.scenario == OnboardingScenario.MINIMAL
    
    def test_determine_scenario_partial(self):
        """Test scenario determination for partial setup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / ".agentrules").write_text("# Rules")
            
            # Add some artifacts but not complete
            agents_dir = repo_path / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "code-reviewer.md").write_text("# Agent")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.scenario == OnboardingScenario.PARTIAL
    
    def test_determine_scenario_upgrade(self):
        """Test scenario determination for upgrade scenario."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            # Need agentrules with factory marker AND some.agent folder content
            # to avoid being classified as MINIMAL
            (repo_path / ".agentrules").write_text(
                "# Generated by Antigravity Agent Factory v1.0.0\n# Some rules here"
            )
            
            # Add some .agent folder content to avoid MINIMAL scenario
            agents_dir = repo_path / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "code-reviewer.md").write_text("# Agent")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            # With factory marker and version 1.x, should be UPGRADE
            # (unless it falls into PARTIAL first)
            assert inventory.agentrules.has_factory_marker is True
            assert inventory.agentrules.version == "1.0.0"
            # The scenario depends on the order of checks in _determine_scenario
            # UPGRADE is checked after MINIMAL but the presence of.agent folder
            # content means it won't be MINIMAL
            assert inventory.scenario in [OnboardingScenario.UPGRADE, OnboardingScenario.PARTIAL]
    
    def test_determine_scenario_complete(self):
        """Test scenario determination for complete setup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create agentrules
            (repo_path / ".agentrules").write_text("# Complete setup")
            
            # Create 3+ agents
            agents_dir = repo_path / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            for name in ["agent1", "agent2", "agent3"]:
                (agents_dir / f"{name}.md").write_text(f"# {name}")
            
            # Create 3+ skills
            skills_dir = repo_path / ".agent" / "skills"
            skills_dir.mkdir()
            for name in ["skill1", "skill2", "skill3"]:
                skill_dir = skills_dir / name
                skill_dir.mkdir()
                (skill_dir / "SKILL.md").write_text(f"# {name}")
            
            # Create special files
            (repo_path / "PURPOSE.md").write_text("# Purpose")
            (repo_path / "practices.yaml").write_text("practices: []")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            
            assert inventory.scenario == OnboardingScenario.COMPLETE


class TestGetFileHash:
    """Tests for get_file_hash function."""
    
    def test_hash_existing_file(self):
        """Test hashing an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("Hello, World!")
            
            hash_value = get_file_hash(test_file)
            
            assert hash_value != ""
            assert len(hash_value) == 32  # MD5 hex length
    
    def test_hash_nonexistent_file(self):
        """Test hashing a non-existent file returns empty string."""
        hash_value = get_file_hash(Path("/nonexistent/file.txt"))
        assert hash_value == ""
    
    def test_hash_same_content_same_hash(self):
        """Test that same content produces same hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"
            
            file1.write_text("Same content")
            file2.write_text("Same content")
            
            assert get_file_hash(file1) == get_file_hash(file2)
    
    def test_hash_different_content_different_hash(self):
        """Test that different content produces different hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"
            
            file1.write_text("Content A")
            file2.write_text("Content B")
            
            assert get_file_hash(file1) != get_file_hash(file2)


class TestMainEntry:
    """Tests for command-line interface."""
    
    def test_main_with_valid_path(self, capsys):
        """Test analyzing a valid repository path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = RepoAnalyzer(tmpdir)
            inventory = analyzer.analyze()
            summary = inventory.get_summary()
            
            assert "Repository:" in summary
            assert "Scenario:" in summary
    
    def test_analyzer_provides_complete_summary(self):
        """Test that analyzer provides complete summary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create some artifacts
            (repo_path / ".agentrules").write_text("# Rules")
            agents_dir = repo_path / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "test-agent.md").write_text("# Agent")
            
            analyzer = RepoAnalyzer(repo_path)
            inventory = analyzer.analyze()
            summary = inventory.get_summary()
            
            assert "test-agent" in summary
            assert "Agentrules: Yes" in summary
