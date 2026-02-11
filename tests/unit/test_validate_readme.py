"""
Unit tests for scripts/validation/validate_readme_structure.py

Tests README structure validation and update functionality.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.validation.validate_readme_structure import StructureValidator, main


class TestStructureValidatorInit:
    """Tests for StructureValidator initialization."""
    
    def test_init_with_default_path(self):
        """Test initialization with default path."""
        validator = StructureValidator()
        assert validator.root_path.exists()
        assert validator.readme_path.name == "README.md"
    
    def test_init_with_custom_path(self):
        """Test initialization with custom path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            assert validator.root_path == Path(tmpdir)


class TestShouldIgnore:
    """Tests for _should_ignore method."""
    
    def test_ignores_pycache(self):
        """Test that __pycache__ is ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            pycache = Path(tmpdir) / "__pycache__"
            pycache.mkdir()
            
            assert validator._should_ignore(pycache) is True
    
    def test_ignores_git(self):
        """Test that .git is ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            git = Path(tmpdir) / ".git"
            git.mkdir()
            
            assert validator._should_ignore(git) is True
    
    def test_ignores_dotfiles(self):
        """Test that dotfiles are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            dotdir = Path(tmpdir) / ".hidden"
            dotdir.mkdir()
            
            assert validator._should_ignore(dotdir) is True
    
    def test_ignores_pyc_files(self):
        """Test that .pyc files are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            pyc = Path(tmpdir) / "module.pyc"
            pyc.touch()
            
            assert validator._should_ignore(pyc) is True
    
    def test_does_not_ignore_valid_dir(self):
        """Test that valid directories are not ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            valid_dir = Path(tmpdir) / "valid_directory"
            valid_dir.mkdir()
            
            assert validator._should_ignore(valid_dir) is False


class TestCountFilesByExtension:
    """Tests for _count_files_by_extension method."""
    
    def test_counts_json_files(self):
        """Test counting JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "file1.json").touch()
            (root / "file2.json").touch()
            (root / "file.txt").touch()
            
            validator = StructureValidator(root)
            count = validator._count_files_by_extension(root, ".json")
            
            assert count == 2
    
    def test_counts_in_subdirectories(self):
        """Test counting files in subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subdir = root / "subdir"
            subdir.mkdir()
            (root / "file1.json").touch()
            (subdir / "file2.json").touch()
            
            validator = StructureValidator(root)
            count = validator._count_files_by_extension(root, ".json")
            
            assert count == 2
    
    def test_excludes_pycache(self):
        """Test that __pycache__ files are excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pycache = root / "__pycache__"
            pycache.mkdir()
            (root / "file1.json").touch()
            (pycache / "cache.json").touch()
            
            validator = StructureValidator(root)
            count = validator._count_files_by_extension(root, ".json")
            
            assert count == 1


class TestScanAgents:
    """Tests for scan_agents method."""
    
    def test_scan_no_agents_dir(self):
        """Test scanning when agents directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_agents()
            
            assert result["count"] == 0
            assert result["agents"] == []
    
    def test_scan_with_agents(self):
        """Test scanning with agents present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            agents_dir = root / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "code-reviewer.md").touch()
            (agents_dir / "test-generator.md").touch()
            
            validator = StructureValidator(root)
            result = validator.scan_agents()
            
            assert result["count"] == 2
            assert "code-reviewer" in result["agents"]
            assert "test-generator" in result["agents"]


class TestScanSkills:
    """Tests for scan_skills method."""
    
    def test_scan_no_skills_dir(self):
        """Test scanning when skills directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_skills()
            
            assert result["count"] == 0
            assert result["skills"] == []
    
    def test_scan_with_skills(self):
        """Test scanning with skills present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skills_dir = root / ".agent" / "skills"            
            # Create valid skill (has SKILL.md)
            tdd = skills_dir / "tdd"
            tdd.mkdir(parents=True)
            (tdd / "SKILL.md").touch()
            
            # Create invalid skill (no SKILL.md)
            invalid = skills_dir / "invalid"
            invalid.mkdir()
            
            validator = StructureValidator(root)
            result = validator.scan_skills()
            
            assert result["count"] == 1
            assert "tdd" in result["skills"]
            assert "invalid" not in result["skills"]


class TestScanBlueprints:
    """Tests for scan_blueprints method."""
    
    def test_scan_no_blueprints_dir(self):
        """Test scanning when blueprints directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_blueprints()
            
            assert result["count"] == 0
            assert result["blueprints"] == []
    
    def test_scan_with_blueprints(self):
        """Test scanning with blueprints present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            blueprints_dir = root / ".agent" / "blueprints"
            
            # Create valid blueprint
            bp = blueprints_dir / "python-fastapi"
            bp.mkdir(parents=True)
            (bp / "blueprint.json").touch()
            
            # Create invalid blueprint (no blueprint.json)
            invalid = blueprints_dir / "invalid"
            invalid.mkdir()
            
            validator = StructureValidator(root)
            result = validator.scan_blueprints()
            
            assert result["count"] == 1
            assert "python-fastapi" in result["blueprints"]


class TestScanPatterns:
    """Tests for scan_patterns method."""
    
    def test_scan_no_patterns_dir(self):
        """Test scanning when patterns directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_patterns()
            
            assert result["categories"] == []
            assert result["total_files"] == 0
    
    def test_scan_with_patterns(self):
        """Test scanning with patterns present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            patterns_dir = root / "patterns"
            
            agents = patterns_dir / "agents"
            agents.mkdir(parents=True)
            (agents / "code-reviewer.json").touch()
            (agents / "test-generator.json").touch()
            
            skills = patterns_dir / "skills"
            skills.mkdir()
            (skills / "tdd.json").touch()
            
            validator = StructureValidator(root)
            result = validator.scan_patterns()
            
            assert result["total_files"] == 3
            assert "agents" in result["categories"]
            assert len(result["categories"]["agents"]) == 2


class TestScanKnowledge:
    """Tests for scan_knowledge method."""
    
    def test_scan_no_knowledge_dir(self):
        """Test scanning when knowledge directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_knowledge()
            
            assert result["count"] == 0
            assert result["files"] == []
    
    def test_scan_with_knowledge(self):
        """Test scanning with knowledge files present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            knowledge_dir = root / "knowledge"
            knowledge_dir.mkdir()
            (knowledge_dir / "patterns.json").touch()
            (knowledge_dir / "best-practices.json").touch()
            (knowledge_dir / "not-json.txt").touch()
            
            validator = StructureValidator(root)
            result = validator.scan_knowledge()
            
            assert result["count"] == 2
            assert "patterns.json" in result["files"]


class TestScanTemplates:
    """Tests for scan_templates method."""
    
    def test_scan_no_templates_dir(self):
        """Test scanning when templates directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_templates()
            
            assert result["categories"] == []
            assert result["total_files"] == 0
    
    def test_scan_with_templates(self):
        """Test scanning with templates present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            templates_dir = root / "templates"
            
            python_dir = templates_dir / "python"
            python_dir.mkdir(parents=True)
            (python_dir / "main.tmpl").touch()
            (python_dir / "readme.md").touch()
            
            validator = StructureValidator(root)
            result = validator.scan_templates()
            
            assert result["total_files"] == 2
            assert "python" in result["categories"]


class TestScanAll:
    """Tests for scan_all method."""
    
    def test_scan_all_returns_all_sections(self):
        """Test that scan_all returns all sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.scan_all()
            
            assert "agents" in result
            assert "skills" in result
            assert "blueprints" in result
            assert "patterns" in result
            assert "knowledge" in result
            assert "templates" in result


class TestRoundToThreshold:
    """Tests for _round_to_threshold method."""
    
    def test_round_small_numbers(self):
        """Test rounding small numbers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            
            assert validator._round_to_threshold(3) == 0
            assert validator._round_to_threshold(5) == 5
            assert validator._round_to_threshold(7) == 5
    
    def test_round_medium_numbers(self):
        """Test rounding medium numbers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            
            assert validator._round_to_threshold(12) == 10
            assert validator._round_to_threshold(27) == 25
            assert validator._round_to_threshold(45) == 40
    
    def test_round_large_numbers(self):
        """Test rounding large numbers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            
            assert validator._round_to_threshold(80) == 75
            assert validator._round_to_threshold(120) == 100
            assert validator._round_to_threshold(600) == 500


class TestGenerateCountsSummary:
    """Tests for generate_counts_summary method."""
    
    def test_returns_all_counts(self):
        """Test that all counts are returned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            # Use mock_counts to be machine independent
            mock_counts = {
                "agents": 5, "skills": 10, "blueprints": 2, 
                "patterns": 3, "knowledge": 4, "templates": 1, "tests": 0
            }
            with patch.object(StructureValidator, 'scan_all', return_value=mock_counts):
                result = validator.generate_counts_summary()
                
                assert result["agents"] == 5
                assert result["skills"] == 10
                assert "blueprints" in result
                assert "knowledge" in result


class TestExtractReadmeCounts:
    """Tests for extract_readme_counts method."""
    
    def test_no_readme(self):
        """Test when README doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.extract_readme_counts()
            
            assert result == {}
    
    def test_extract_exact_counts(self):
        """Test extracting exact counts from README."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("""
# Project

## Project Structure

```
+-- .agent/|   +-- agents/                  # Factory's own agents (5 agents)
|   +-- skills/                  # Factory's own skills (10 skills)
+-- blueprints/                  # Technology stack blueprints (28 blueprints)
```
""", encoding="utf-8")
            
            validator = StructureValidator(root)
            result = validator.extract_readme_counts()
            
            assert result["agents"]["count"] == 5
            assert result["agents"]["is_threshold"] is False
            assert result["skills"]["count"] == 10
            assert result["blueprints"]["count"] == 28
    
    def test_extract_threshold_counts(self):
        """Test extracting threshold counts (50+ files)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("""
# Project

## Project Structure

```
+-- knowledge/                   # Reference data (50+ files)
+-- patterns/                    # Reusable patterns (75+ files)
+-- templates/                   # Code templates (100+ files)
```
""", encoding="utf-8")
            
            validator = StructureValidator(root)
            result = validator.extract_readme_counts()
            
            assert result["knowledge"]["count"] == 50
            assert result["knowledge"]["is_threshold"] is True
            assert result["patterns"]["count"] == 75
            assert result["patterns"]["is_threshold"] is True
            
    def test_extract_unconfigured_section(self):
        """Test extracting section not in config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("## Structure\n(5 unknown)", encoding="utf-8")
            
            validator = StructureValidator(root)
            result = validator.extract_readme_counts()
            assert "unknown" not in result


class TestValidate:
    """Tests for validate method."""
    
    def test_validate_matching_counts(self):
        """Test validation with matching counts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Create actual structure
            agents_dir = root / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "agent1.md").touch()
            (agents_dir / "agent2.md").touch()
            
            # Create README with matching counts
            readme = root / "README.md"
            readme.write_text("""
## Project Structure

```
+-- .agent/|   +-- agents/                  # Factory's own agents (2 agents)
```
""", encoding="utf-8")
            
            validator = StructureValidator(root)
            is_valid, messages = validator.validate()
            
            # Agents should match correctly (actual 2 vs README 2)
            assert any("✅ 'agents': 2 (matches README.md)" in m for m in messages)
    
    def test_validate_threshold_passing(self):
        """Test validation with threshold counts that pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Create 55 knowledge files
            knowledge_dir = root / ".agent" / "knowledge"
            knowledge_dir.mkdir()
            for i in range(55):
                (knowledge_dir / f"file{i}.json").touch()
            
            # README says 50+
            readme = root / "README.md"
            readme.write_text("""
## Project Structure

```
+-- knowledge/                   # Reference data (50+ files)
```
""", encoding="utf-8")
            
            validator = StructureValidator(root)
            is_valid, messages = validator.validate()
            
            # Knowledge should not be in discrepancies (55 >= 50)
            assert any("✅ 'knowledge': 55 (matches README.md threshold 50+)" in m for m in messages)


class TestUpdateReadme:
    """Tests for update_readme method."""
    
    def test_update_no_readme(self):
        """Test update when README doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = StructureValidator(Path(tmpdir))
            result = validator.update_readme()
            
            assert result is False
    
    def test_update_with_structure_section(self):
        """Test updating README with existing structure section."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("""## Project Structure\n\n- (5 agents)""", encoding="utf-8")
            
            validator = StructureValidator(root)
            with patch.object(StructureValidator, 'scan_all', return_value={"agents": 8}):
                result = validator.update_readme()
                
                assert result is True
                content = readme.read_text(encoding="utf-8")
                assert "(8 agents)" in content
    def test_update_no_structure_section(self):
        """Test updating README without structure section."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Create minimal patterns for generate_structure_markdown to work
            patterns_dir = root / "patterns" / "agents"
            patterns_dir.mkdir(parents=True)
            (patterns_dir / "test.json").touch()
            
            readme = root / "README.md"
            readme.write_text("""# Project

## Some Other Section

Content here.
""", encoding="utf-8")
            
            validator = StructureValidator(root)
            result = validator.update_readme()
            
            assert result is False


class TestGenerateStructureMarkdown:
    """Tests for generate_structure_markdown method."""
    
    def test_generates_markdown(self):
        """Test that markdown is generated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            validator = StructureValidator(root)
            mock_counts = {"agents": 5, "skills": 10}
            with patch.object(StructureValidator, 'scan_all', return_value=mock_counts):
                markdown = validator.generate_structure_markdown()
                
                assert "# Project Structure" in markdown
                assert "agents" in markdown.lower()
                assert "5" in markdown
                assert "skills" in markdown.lower()
                assert "10" in markdown
    
    def test_includes_counts(self):
        """Test that counts are included in markdown."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            validator = StructureValidator(root)
            mock_counts = {"agents": 28, "skills": 116, "blueprints": 34}
            with patch.object(StructureValidator, 'scan_all', return_value=mock_counts):
                markdown = validator.generate_structure_markdown()
                
                assert "28" in markdown
                assert "116" in markdown
                assert "34" in markdown


class TestMain:
    """Tests for main function."""
    
    def test_main_check_mode(self, capsys):
        """Test main with --check."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("# Test\n## Project Structure\n(0 agents)", encoding="utf-8")
            with patch('sys.argv', ['validate_readme_structure.py', '--check', '--root', str(root)]):
                result = main()
                
                captured = capsys.readouterr()
                assert "[OK]" in captured.out or "[FAIL]" in captured.out
    
    def test_main_generate_mode(self, capsys):
        """Test main with --generate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("# Test\n## Project Structure\n(0 agents)", encoding="utf-8")
            with patch('sys.argv', ['validate_readme_structure.py', '--generate', '--root', str(root)]):
                result = main()
                
                assert result == 0
                captured = capsys.readouterr()
                assert "agents" in captured.out    
    def test_main_json_mode(self, capsys):
        """Test main with --json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("# Test\n## Project Structure\n(0 agents)", encoding="utf-8")
            with patch('sys.argv', ['validate_readme_structure.py', '--json', '--root', str(root)]):
                result = main()
                
                assert result == 0
                captured = capsys.readouterr()
                # Should be valid JSON
                data = json.loads(captured.out)
                assert "agents" in data
    
    def test_main_update_mode(self, capsys):
        """Test main with --update."""
        with patch('sys.argv', ['validate_readme_structure.py', '--update']):
            result = main()
            
            captured = capsys.readouterr()
            assert "README.md" in captured.out
    
    def test_main_with_custom_root(self, capsys):
        """Test main with --root argument."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("# Test")
            
            with patch('sys.argv', ['validate_readme_structure.py', '--check', '--root', str(root)]):
                result = main()
    
    def test_main_default_is_check(self, capsys):
        """Test that default mode is --check."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("# Test\n## Project Structure\n(0 agents)", encoding="utf-8")
            with patch('sys.argv', ['validate_readme_structure.py', '--root', str(root)]):
                result = main()
                
                captured = capsys.readouterr()
                assert "[OK]" in captured.out or "[FAIL]" in captured.out
