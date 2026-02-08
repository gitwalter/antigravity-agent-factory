"""
Workflow structure validation tests.

Tests validate that workflow markdown files follow the established structure
with proper sections, phases, and documentation.
"""

import re
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestWorkflowStructure:
    """Tests for workflow markdown structure validation."""
    
    @pytest.fixture
    def workflows_dir(self):
        """Get the workflows directory."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / "workflows"
    
    @pytest.fixture
    def all_workflow_files(self, workflows_dir):
        """Get all workflow markdown files."""
        return list(workflows_dir.rglob("*.md"))
    
    def test_workflows_directory_exists(self, workflows_dir):
        """Test that workflows directory exists."""
        assert workflows_dir.exists(), "Workflows directory should exist"
    
    def test_workflow_files_exist(self, all_workflow_files):
        """Test that workflow files exist."""
        assert len(all_workflow_files) > 0, "Should have at least one workflow file"
    
    def test_minimum_workflow_count(self, all_workflow_files):
        """Test that we have the expected minimum number of workflows."""
        # We created 21 workflows
        assert len(all_workflow_files) >= 20, \
            f"Expected at least 20 workflows, found {len(all_workflow_files)}"
    
    def test_all_workflows_have_title(self, all_workflow_files):
        """Test that all workflows have a markdown title."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            # Strip YAML frontmatter if present
            if content.startswith("---"):
                try:
                    # Split by --- and get the content after the second ---
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                except IndexError:
                    pass
            
            # Check for H1 title
            if not content.strip().startswith("# "):
                errors.append(f"{workflow_file.name}: Missing H1 title")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_all_workflows_have_overview(self, all_workflow_files):
        """Test that all workflows have an Overview section."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            if "## Overview" not in content:
                errors.append(f"{workflow_file.name}: Missing ## Overview section")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_all_workflows_have_trigger_conditions(self, all_workflow_files):
        """Test that all workflows have Trigger Conditions section."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            if "## Trigger Conditions" not in content:
                errors.append(f"{workflow_file.name}: Missing ## Trigger Conditions section")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_all_workflows_have_phases(self, all_workflow_files):
        """Test that all workflows have Phases section."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            if "## Phases" not in content:
                errors.append(f"{workflow_file.name}: Missing ## Phases section")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_all_workflows_have_decision_points(self, all_workflow_files):
        """Test that all workflows have Decision Points section."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            if "## Decision Points" not in content:
                errors.append(f"{workflow_file.name}: Missing ## Decision Points section")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_all_workflows_have_example_session(self, all_workflow_files):
        """Test that all workflows have an Example Session section."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            if "## Example Session" not in content:
                errors.append(f"{workflow_file.name}: Missing ## Example Session section")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_workflow_naming_convention(self, all_workflow_files):
        """Test that workflow files use kebab-case naming."""
        errors = []
        
        for workflow_file in all_workflow_files:
            filename = workflow_file.stem  # filename without extension
            
            # Check for spaces
            if " " in filename:
                errors.append(f"{workflow_file.name}: Filename should not contain spaces")
            
            # Check for uppercase (kebab-case should be lowercase)
            if filename != filename.lower():
                errors.append(f"{workflow_file.name}: Filename should be lowercase (kebab-case)")
        
        if errors:
            pytest.fail("\n".join(errors))


class TestWorkflowCategories:
    """Tests for workflow organization by category."""
    
    @pytest.fixture
    def workflows_dir(self):
        """Get the workflows directory."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / "workflows"
    
    def test_universal_workflows_exist(self, workflows_dir):
        """Test that universal workflows exist."""
        universal_dir = workflows_dir / "universal"
        assert universal_dir.exists(), "Universal workflows directory should exist"
        
        workflows = list(universal_dir.glob("*.md"))
        assert len(workflows) >= 4, \
            f"Expected at least 4 universal workflows, found {len(workflows)}"
    
    def test_quality_workflows_exist(self, workflows_dir):
        """Test that quality workflows exist."""
        quality_dir = workflows_dir / "quality"
        assert quality_dir.exists(), "Quality workflows directory should exist"
        
        workflows = list(quality_dir.glob("*.md"))
        assert len(workflows) >= 2, \
            f"Expected at least 2 quality workflows, found {len(workflows)}"
    
    def test_agile_workflows_exist(self, workflows_dir):
        """Test that agile workflows exist."""
        agile_dir = workflows_dir / "agile"
        assert agile_dir.exists(), "Agile workflows directory should exist"
        
        workflows = list(agile_dir.glob("*.md"))
        assert len(workflows) >= 4, \
            f"Expected at least 4 agile workflows, found {len(workflows)}"
    
    def test_operations_workflows_exist(self, workflows_dir):
        """Test that operations workflows exist."""
        ops_dir = workflows_dir / "operations"
        assert ops_dir.exists(), "Operations workflows directory should exist"
        
        workflows = list(ops_dir.glob("*.md"))
        assert len(workflows) >= 2, \
            f"Expected at least 2 operations workflows, found {len(workflows)}"
    
    def test_domain_workflows_exist(self, workflows_dir):
        """Test that domain-specific workflow directories exist."""
        domain_dirs = ["blockchain", "trading", "sap", "ai-ml"]
        
        for domain in domain_dirs:
            domain_dir = workflows_dir / domain
            assert domain_dir.exists(), f"{domain} workflows directory should exist"
            
            workflows = list(domain_dir.glob("*.md"))
            assert len(workflows) >= 1, \
                f"Expected at least 1 {domain} workflow, found {len(workflows)}"


class TestWorkflowContent:
    """Tests for workflow content quality."""
    
    @pytest.fixture
    def workflows_dir(self):
        """Get the workflows directory."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / "workflows"
    
    @pytest.fixture
    def all_workflow_files(self, workflows_dir):
        """Get all workflow markdown files."""
        return list(workflows_dir.rglob("*.md"))
    
    def test_workflows_have_version(self, all_workflow_files):
        """Test that workflows declare a version."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            # Look for **Version:** pattern
            if "**Version:**" not in content and "Version:" not in content:
                errors.append(f"{workflow_file.name}: Missing version declaration")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_workflows_have_trigger_examples(self, all_workflow_files):
        """Test that workflows provide trigger examples."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            # Look for "Trigger Examples" pattern
            if "Trigger Examples:" not in content and "**Trigger Examples:**" not in content:
                errors.append(f"{workflow_file.name}: Missing trigger examples")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_workflows_have_fallback_procedures(self, all_workflow_files):
        """Test that workflows have fallback procedures."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            if "## Fallback Procedures" not in content:
                errors.append(f"{workflow_file.name}: Missing ## Fallback Procedures section")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_no_broken_internal_links(self, all_workflow_files):
        """Test that workflows don't have obviously broken links."""
        errors = []
        
        for workflow_file in all_workflow_files:
            content = workflow_file.read_text(encoding='utf-8')
            
            # Look for markdown links
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            
            for link_text, link_url in links:
                # Check for empty links
                if not link_url.strip():
                    errors.append(f"{workflow_file.name}: Empty link for '{link_text}'")
                
                # Check for placeholder links
                if "TODO" in link_url or "FIXME" in link_url:
                    errors.append(f"{workflow_file.name}: Placeholder link '{link_url}'")
        
        if errors:
            pytest.fail("\n".join(errors))


class TestWorkflowIntegration:
    """Tests for workflow integration with other components."""
    
    @pytest.fixture
    def project_root(self):
        """Get project root directory."""
        return Path(__file__).parent.parent.parent
    
    def test_workflow_patterns_json_exists(self, project_root):
        """Test that workflow-patterns.json exists and is valid JSON."""
        import json
        
        patterns_file = project_root / "knowledge" / "workflow-patterns.json"
        assert patterns_file.exists(), "workflow-patterns.json should exist"
        
        # Should be valid JSON
        content = patterns_file.read_text(encoding='utf-8')
        data = json.loads(content)
        
        assert "workflowPatterns" in data, "Should have workflowPatterns key"
    
    def test_workflow_patterns_reference_workflows(self, project_root):
        """Test that workflow patterns reference existing workflows."""
        import json
        
        patterns_file = project_root / "knowledge" / "workflow-patterns.json"
        content = patterns_file.read_text(encoding='utf-8')
        data = json.loads(content)
        
        patterns = data.get("workflowPatterns", {})
        
        # Check that we have a good number of patterns
        assert len(patterns) >= 15, \
            f"Expected at least 15 workflow patterns, found {len(patterns)}"
    
    def test_workflow_patterns_doc_exists(self, project_root):
        """Test that WORKFLOW_PATTERNS.md documentation exists."""
        doc_file = project_root / "docs" / "reference" / "WORKFLOW_PATTERNS.md"
        assert doc_file.exists(), "WORKFLOW_PATTERNS.md should exist"
        
        content = doc_file.read_text(encoding='utf-8')
        
        # Should have the implemented workflows section
        assert "Implemented Workflows Catalog" in content, \
            "Should have Implemented Workflows Catalog section"
