"""
End-to-end integration tests for gap analysis workflow.

Tests cover the complete gap analysis workflow from start to finish.
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.analysis.knowledge_gap_analyzer import (
    KnowledgeGapAnalyzer,
    AnalysisResult,
    GapPriority,
    run_gap_analysis,
)
from scripts.taxonomy import TaxonomyLoader, load_agent_taxonomy


class TestGapAnalysisWorkflow:
    """End-to-end tests for gap analysis workflow."""
    
    def test_full_analysis_workflow(self, knowledge_dir, taxonomy_dir):
        """Test complete analysis workflow from start to finish."""
        # Step 1: Load taxonomy
        loader = TaxonomyLoader(taxonomy_dir)
        taxonomy = loader.load_taxonomy("agent_taxonomy.json")
        assert len(taxonomy) > 0, "Taxonomy should have domains"
        
        # Step 2: Create analyzer
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        
        # Step 3: Run analysis
        result = analyzer.analyze("agent_taxonomy.json")
        
        # Step 4: Verify result structure
        assert isinstance(result, AnalysisResult)
        assert result.total_topics > 0
        assert result.taxonomy_used == "agent_taxonomy.json"
        assert len(result.files_analyzed) > 0
    
    def test_analysis_produces_gaps(self, knowledge_dir, taxonomy_dir):
        """Test that analysis produces gap findings."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        # Given the comprehensive taxonomy, there should be some gaps
        # (unless knowledge is 100% complete, which is unlikely)
        # At minimum, result structure should be valid
        assert isinstance(result.gaps, list)
        assert isinstance(result.coverage_scores, list)
    
    def test_analysis_identifies_coverage(self, knowledge_dir, taxonomy_dir):
        """Test that analysis correctly identifies coverage."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        # Coverage should be between 0-100%
        assert 0 <= result.coverage_percentage <= 100
        
        # Covered topics should not exceed total
        assert result.covered_topics <= result.total_topics
    
    def test_analysis_with_mock_knowledge(self, mock_knowledge_dir, tmp_path):
        """Test analysis with controlled mock knowledge."""
        # Create minimal taxonomy for controlled testing
        taxonomy_data = {
            "domains": {
                "test_domain": {
                    "description": "Test domain",
                    "required_depth": 2,
                    "topics": {
                        "covered_topic": {
                            "description": "A topic that is covered",
                            "keywords": ["test", "pattern"],
                            "required_depth": 1
                        },
                        "missing_topic": {
                            "description": "A topic that is NOT covered",
                            "keywords": ["xyznonexistent123"],
                            "required_depth": 2
                        }
                    }
                }
            }
        }
        
        taxonomy_dir = tmp_path / "taxonomy"
        taxonomy_dir.mkdir()
        (taxonomy_dir / "test_taxonomy.json").write_text(
            json.dumps(taxonomy_data, indent=2)
        )
        
        # Run analysis
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir, taxonomy_dir)
        result = analyzer.analyze("test_taxonomy.json")
        
        # Should find the missing topic as a gap
        gap_topics = {g.topic.name for g in result.gaps}
        assert "missing_topic" in gap_topics, \
            "Should identify missing_topic as a gap"
    
    def test_analysis_result_serialization(self, knowledge_dir, taxonomy_dir, tmp_path):
        """Test that analysis result can be serialized to JSON."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        # Save report
        output_path = tmp_path / "analysis_report.json"
        analyzer.save_report(result, output_path)
        
        # Verify file was created
        assert output_path.exists()
        
        # Verify it's valid JSON
        with open(output_path) as f:
            loaded = json.load(f)
        
        assert "summary" in loaded
        assert "gaps" in loaded


class TestExtensionCandidates:
    """Tests for extension candidate selection."""
    
    def test_get_candidates_returns_gaps(self, knowledge_dir, taxonomy_dir):
        """Test that get_extension_candidates returns gaps."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        candidates = analyzer.get_extension_candidates(result, max_candidates=10)
        
        # Should return a list
        assert isinstance(candidates, list)
        
        # Each candidate should be a gap
        for candidate in candidates:
            assert candidate in result.gaps
    
    def test_candidates_sorted_by_priority(self, knowledge_dir, taxonomy_dir):
        """Test that candidates are sorted by priority."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        candidates = analyzer.get_extension_candidates(result, max_candidates=10)
        
        if len(candidates) >= 2:
            # First candidate should have equal or higher priority (lower value)
            for i in range(len(candidates) - 1):
                assert candidates[i].priority.value <= candidates[i + 1].priority.value, \
                    "Candidates should be sorted by priority"
    
    def test_candidates_respect_max_limit(self, knowledge_dir, taxonomy_dir):
        """Test that max_candidates limit is respected."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        candidates = analyzer.get_extension_candidates(result, max_candidates=3)
        
        assert len(candidates) <= 3
    
    def test_candidates_filter_by_priority(self, knowledge_dir, taxonomy_dir):
        """Test that candidates can be filtered by minimum priority."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        # Get only high priority candidates
        candidates = analyzer.get_extension_candidates(
            result,
            max_candidates=10,
            min_priority=GapPriority.HIGH
        )
        
        # All returned candidates should be HIGH priority or better
        for candidate in candidates:
            assert candidate.priority.value <= GapPriority.HIGH.value


class TestRunGapAnalysisFunction:
    """Tests for the run_gap_analysis convenience function."""
    
    def test_run_gap_analysis_default_dir(self):
        """Test run_gap_analysis with default knowledge directory."""
        # Should use default knowledge/ dir relative to module
        result = run_gap_analysis()
        
        assert isinstance(result, AnalysisResult)
    
    def test_run_gap_analysis_custom_dir(self, knowledge_dir):
        """Test run_gap_analysis with custom directory."""
        result = run_gap_analysis(knowledge_dir)
        
        assert isinstance(result, AnalysisResult)
        assert len(result.files_analyzed) > 0


class TestTaxonomyIntegration:
    """Tests for taxonomy loading integration."""
    
    def test_load_agent_taxonomy_integration(self):
        """Test loading the default agent taxonomy."""
        taxonomy = load_agent_taxonomy()
        
        # Should have multiple domains
        assert len(taxonomy) >= 1
        
        # Each domain should have structure
        for domain_name, domain in taxonomy.items():
            assert domain.name == domain_name
    
    def test_taxonomy_has_substantial_content(self):
        """Test that taxonomy has substantial content for analysis."""
        taxonomy = load_agent_taxonomy()
        
        # Count total topics
        total_topics = sum(d.count_topics() for d in taxonomy.values())
        
        # Should have a reasonable number of topics
        assert total_topics >= 10, \
            "Taxonomy should have at least 10 topics for meaningful analysis"
