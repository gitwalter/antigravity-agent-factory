#!/usr/bin/env python3
"""
Tests for the Research-First Development Pattern.

These tests verify that the research-first development pattern is properly
defined, documented, and available for use in generated projects.

Test Categories:
1. Knowledge file structure and schema
2. Required workflow steps
3. Trigger definitions
4. Integration with agents and skills
5. Availability in generated projects
"""

import json
from pathlib import Path

import pytest


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def knowledge_dir(project_root: Path) -> Path:
    """Get the knowledge directory."""
    return project_root / "knowledge"


@pytest.fixture
def research_first_pattern(knowledge_dir: Path) -> dict:
    """Load the research-first development pattern."""
    pattern_path = knowledge_dir / "research-first-development.json"
    if not pattern_path.exists():
        pytest.skip("research-first-development.json not yet created")
    return json.loads(pattern_path.read_text(encoding='utf-8'))


# =============================================================================
# TEST: Knowledge File Structure
# =============================================================================

class TestKnowledgeFileStructure:
    """Tests for knowledge file schema compliance."""
    
    def test_knowledge_file_exists(self, knowledge_dir: Path):
        """Research-first pattern knowledge file should exist."""
        pattern_path = knowledge_dir / "research-first-development.json"
        assert pattern_path.exists(), "research-first-development.json not found"
    
    def test_has_required_top_level_fields(self, research_first_pattern: dict):
        """Knowledge file should have required top-level fields."""
        required_fields = [
            "title",
            "description",
            "version",
        ]
        for field in required_fields:
            assert field in research_first_pattern, f"Missing required field: {field}"
    
    def test_has_axiom_alignment(self, research_first_pattern: dict):
        """Knowledge file should document axiom alignment."""
        assert "axiomAlignment" in research_first_pattern
        alignment = research_first_pattern["axiomAlignment"]
        
        # Should reference at least humility (A2) and transparency (A3)
        assert any("humility" in key.lower() or "A2" in key for key in alignment.keys()), \
            "Should align with humility axiom"
        assert any("transparency" in key.lower() or "A3" in key for key in alignment.keys()), \
            "Should align with transparency axiom"
    
    def test_valid_json_schema(self, research_first_pattern: dict):
        """Knowledge file should have valid JSON schema reference."""
        assert "$schema" in research_first_pattern
        assert "json-schema.org" in research_first_pattern["$schema"]


# =============================================================================
# TEST: Workflow Steps
# =============================================================================

class TestWorkflowSteps:
    """Tests for required workflow steps."""
    
    def test_has_workflow_definition(self, research_first_pattern: dict):
        """Pattern should define a workflow."""
        assert "workflow" in research_first_pattern
        assert isinstance(research_first_pattern["workflow"], dict)
    
    def test_workflow_includes_research_step(self, research_first_pattern: dict):
        """Workflow should include a research step."""
        workflow = research_first_pattern["workflow"]
        research_steps = [k for k in workflow.keys() if "research" in k.lower()]
        assert len(research_steps) > 0, "Workflow should include research step"
    
    def test_workflow_includes_document_step(self, research_first_pattern: dict):
        """Workflow should include a documentation step."""
        workflow = research_first_pattern["workflow"]
        doc_steps = [k for k in workflow.keys() if "document" in k.lower()]
        assert len(doc_steps) > 0, "Workflow should include documentation step"
    
    def test_workflow_includes_test_step(self, research_first_pattern: dict):
        """Workflow should include a test step."""
        workflow = research_first_pattern["workflow"]
        test_steps = [k for k in workflow.keys() if "test" in k.lower()]
        assert len(test_steps) > 0, "Workflow should include test step"
    
    def test_workflow_includes_build_step(self, research_first_pattern: dict):
        """Workflow should include a build/implementation step."""
        workflow = research_first_pattern["workflow"]
        build_steps = [k for k in workflow.keys() if "build" in k.lower() or "implement" in k.lower()]
        assert len(build_steps) > 0, "Workflow should include build step"
    
    def test_workflow_order_is_research_before_build(self, research_first_pattern: dict):
        """Research should come before build in workflow order."""
        workflow = research_first_pattern["workflow"]
        keys = list(workflow.keys())
        
        # Find positions of research and build steps
        research_pos = next((i for i, k in enumerate(keys) if "research" in k.lower()), -1)
        build_pos = next((i for i, k in enumerate(keys) if "build" in k.lower()), -1)
        
        assert research_pos != -1, "Research step not found"
        assert build_pos != -1, "Build step not found"
        assert research_pos < build_pos, "Research should come before build"


# =============================================================================
# TEST: Trigger Definitions
# =============================================================================

class TestTriggerDefinitions:
    """Tests for when the pattern should be applied."""
    
    def test_has_trigger_definitions(self, research_first_pattern: dict):
        """Pattern should define when to apply research-first approach."""
        assert "triggers" in research_first_pattern or \
               any("trigger" in str(v).lower() for v in research_first_pattern.values())
    
    def test_triggers_include_performance_optimization(self, research_first_pattern: dict):
        """Performance optimization should trigger research-first."""
        triggers = research_first_pattern.get("triggers", {})
        always_research = triggers.get("always_research", [])
        
        perf_triggers = [t for t in always_research if "performance" in t.lower()]
        assert len(perf_triggers) > 0, "Performance optimization should be a trigger"
    
    def test_triggers_include_security(self, research_first_pattern: dict):
        """Security implementations should trigger research-first."""
        triggers = research_first_pattern.get("triggers", {})
        always_research = triggers.get("always_research", [])
        
        security_triggers = [t for t in always_research if "security" in t.lower()]
        assert len(security_triggers) > 0, "Security should be a trigger"
    
    def test_has_counter_indicators(self, research_first_pattern: dict):
        """Pattern should define when NOT to apply research-first."""
        triggers = research_first_pattern.get("triggers", {})
        
        # Should have either skip_research or counter_indicators
        has_skip = "skip_research" in triggers
        has_counter = "counter_indicators" in triggers
        
        # Or check in workflow step
        workflow = research_first_pattern.get("workflow", {})
        has_counter_in_workflow = any(
            "counter_indicator" in str(v).lower() 
            for v in workflow.values() if isinstance(v, dict)
        )
        
        assert has_skip or has_counter or has_counter_in_workflow, \
            "Pattern should define when NOT to use research-first"


# =============================================================================
# TEST: Benefits Documentation
# =============================================================================

class TestBenefitsDocumentation:
    """Tests for benefit documentation."""
    
    def test_has_benefits_section(self, research_first_pattern: dict):
        """Pattern should document its benefits."""
        assert "benefits" in research_first_pattern
    
    def test_documents_multiplied_value(self, research_first_pattern: dict):
        """Pattern should explain multiplied value concept."""
        benefits = research_first_pattern.get("benefits", {})
        pattern_str = json.dumps(research_first_pattern).lower()
        
        assert "multiplied" in pattern_str or "reusable" in pattern_str, \
            "Pattern should explain multiplied/reusable value"


# =============================================================================
# TEST: Anti-Patterns
# =============================================================================

class TestAntiPatterns:
    """Tests for anti-pattern documentation."""
    
    def test_has_anti_patterns(self, research_first_pattern: dict):
        """Pattern should document anti-patterns to avoid."""
        assert "anti_patterns" in research_first_pattern
        assert len(research_first_pattern["anti_patterns"]) > 0
    
    def test_warns_against_not_invented_here(self, research_first_pattern: dict):
        """Should warn against 'not invented here' syndrome."""
        anti_patterns = research_first_pattern.get("anti_patterns", {})
        anti_pattern_text = json.dumps(anti_patterns).lower()
        
        assert "invented" in anti_pattern_text or "dismiss" in anti_pattern_text, \
            "Should warn against dismissing external solutions"
    
    def test_warns_against_analysis_paralysis(self, research_first_pattern: dict):
        """Should warn against analysis paralysis."""
        anti_patterns = research_first_pattern.get("anti_patterns", {})
        anti_pattern_text = json.dumps(anti_patterns).lower()
        
        assert "paralysis" in anti_pattern_text or "over-research" in anti_pattern_text, \
            "Should warn against analysis paralysis"


# =============================================================================
# TEST: Integration Points
# =============================================================================

class TestIntegrationPoints:
    """Tests for integration with agents and skills."""
    
    def test_references_related_patterns(self, research_first_pattern: dict):
        """Pattern should reference related patterns."""
        assert "related_patterns" in research_first_pattern
        assert len(research_first_pattern["related_patterns"]) > 0
    
    def test_defines_agent_integration(self, research_first_pattern: dict):
        """Pattern should define how agents should use it."""
        pattern_str = json.dumps(research_first_pattern).lower()
        
        # Should mention agents somewhere
        assert "agent" in pattern_str, "Pattern should define agent integration"
    
    def test_knowledge_file_is_listed_in_manifest(self, project_root: Path):
        """Knowledge file should be discoverable via manifest or directory."""
        knowledge_dir = project_root / "knowledge"
        pattern_path = knowledge_dir / "research-first-development.json"
        
        # Either file exists in knowledge dir, or is listed in manifest
        manifest_path = knowledge_dir / "manifest.json"
        
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            files = manifest.get("files", [])
            assert "research-first-development.json" in str(files) or pattern_path.exists()
        else:
            assert pattern_path.exists()


# =============================================================================
# TEST: Examples
# =============================================================================

class TestExamples:
    """Tests for example usage."""
    
    def test_has_examples(self, research_first_pattern: dict):
        """Pattern should include examples of application."""
        assert "examples" in research_first_pattern
        assert len(research_first_pattern["examples"]) > 0
    
    def test_reactive_indexing_example(self, research_first_pattern: dict):
        """Should include reactive indexing as an example."""
        examples = research_first_pattern.get("examples", {})
        example_str = json.dumps(examples).lower()
        
        assert "reactive" in example_str or "indexing" in example_str, \
            "Should include reactive indexing as an example"


# =============================================================================
# TEST: Availability in Generated Projects
# =============================================================================

class TestGeneratedProjectAvailability:
    """Tests for availability in generated projects."""
    
    def test_pattern_can_be_serialized(self, research_first_pattern: dict):
        """Pattern should be serializable for inclusion in generated projects."""
        # Should be able to serialize and deserialize without data loss
        serialized = json.dumps(research_first_pattern, indent=2)
        deserialized = json.loads(serialized)
        assert deserialized == research_first_pattern
    
    def test_no_absolute_paths(self, research_first_pattern: dict):
        """Pattern should not contain absolute paths."""
        pattern_str = json.dumps(research_first_pattern)
        
        # Check for common absolute path patterns
        assert "C:\\" not in pattern_str, "Should not contain Windows absolute paths"
        assert "/home/" not in pattern_str, "Should not contain Unix home paths"
        assert "/Users/" not in pattern_str, "Should not contain macOS user paths"
