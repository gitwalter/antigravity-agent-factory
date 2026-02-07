"""
Unit tests for scripts/analysis/knowledge_gap_analyzer.py

Tests for CoverageScore, KnowledgeGap, AnalysisResult, and KnowledgeGapAnalyzer.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.analysis.knowledge_gap_analyzer import (
    CoverageScore,
    KnowledgeGap,
    AnalysisResult,
    KnowledgeGapAnalyzer,
    GapType,
    GapPriority,
    run_gap_analysis,
)
from scripts.taxonomy import TopicNode


class TestCoverageScore:
    """Tests for CoverageScore dataclass."""
    
    def test_create_coverage_score(self):
        """Test creating a basic CoverageScore."""
        score = CoverageScore(
            topic_name="test_topic",
            topic_path="domain.test_topic",
            current_depth=2,
            required_depth=3
        )
        
        assert score.topic_name == "test_topic"
        assert score.topic_path == "domain.test_topic"
        assert score.current_depth == 2
        assert score.required_depth == 3
    
    def test_coverage_ratio_calculation(self):
        """Test coverage_ratio property calculation."""
        score = CoverageScore(
            topic_name="test",
            topic_path="test",
            current_depth=1,
            required_depth=2
        )
        
        assert score.coverage_ratio == 0.5
    
    def test_coverage_ratio_capped_at_one(self):
        """Test coverage_ratio doesn't exceed 1.0."""
        score = CoverageScore(
            topic_name="test",
            topic_path="test",
            current_depth=5,
            required_depth=2
        )
        
        assert score.coverage_ratio == 1.0
    
    def test_is_adequate_true(self):
        """Test is_adequate when coverage meets requirement."""
        score = CoverageScore(
            topic_name="test",
            topic_path="test",
            current_depth=3,
            required_depth=2
        )
        
        assert score.is_adequate is True
    
    def test_is_adequate_false(self):
        """Test is_adequate when coverage below requirement."""
        score = CoverageScore(
            topic_name="test",
            topic_path="test",
            current_depth=1,
            required_depth=3
        )
        
        assert score.is_adequate is False
    
    def test_is_adequate_exact_match(self):
        """Test is_adequate when coverage exactly meets requirement."""
        score = CoverageScore(
            topic_name="test",
            topic_path="test",
            current_depth=2,
            required_depth=2
        )
        
        assert score.is_adequate is True
    
    def test_zero_required_depth(self):
        """Test coverage_ratio with zero required depth."""
        score = CoverageScore(
            topic_name="test",
            topic_path="test",
            current_depth=0,
            required_depth=0
        )
        
        assert score.coverage_ratio == 1.0
        assert score.is_adequate is True


class TestKnowledgeGap:
    """Tests for KnowledgeGap dataclass."""
    
    @pytest.fixture
    def sample_topic(self):
        """Create a sample TopicNode for testing."""
        return TopicNode(
            name="test_topic",
            description="A test topic",
            required_depth=2,
            keywords=["test", "sample"]
        )
    
    @pytest.fixture
    def sample_coverage(self):
        """Create a sample CoverageScore for testing."""
        return CoverageScore(
            topic_name="test_topic",
            topic_path="domain.test_topic",
            current_depth=0,
            required_depth=2
        )
    
    def test_create_gap(self, sample_topic, sample_coverage):
        """Test creating a KnowledgeGap."""
        gap = KnowledgeGap(
            gap_type=GapType.MISSING,
            priority=GapPriority.CRITICAL,
            topic=sample_topic,
            coverage=sample_coverage,
            description="Topic is missing"
        )
        
        assert gap.gap_type == GapType.MISSING
        assert gap.priority == GapPriority.CRITICAL
        assert gap.topic.name == "test_topic"
        assert gap.description == "Topic is missing"
    
    def test_to_dict_serialization(self, sample_topic, sample_coverage):
        """Test to_dict produces serializable output."""
        gap = KnowledgeGap(
            gap_type=GapType.SHALLOW,
            priority=GapPriority.HIGH,
            topic=sample_topic,
            coverage=sample_coverage,
            description="Shallow coverage",
            suggested_actions=["Add more content"],
            estimated_effort="medium"
        )
        
        result = gap.to_dict()
        
        assert result["gap_type"] == "shallow"
        assert result["priority"] == "HIGH"
        assert result["topic_name"] == "test_topic"
        assert result["description"] == "Shallow coverage"
        assert "Add more content" in result["suggested_actions"]
        
        # Should be JSON serializable
        json.dumps(result)
    
    def test_gap_with_related_files(self, sample_topic, sample_coverage):
        """Test gap with related files."""
        gap = KnowledgeGap(
            gap_type=GapType.INCOMPLETE,
            priority=GapPriority.MEDIUM,
            topic=sample_topic,
            coverage=sample_coverage,
            description="Incomplete",
            related_files=["file1.json", "file2.json"]
        )
        
        assert len(gap.related_files) == 2
        assert "file1.json" in gap.related_files


class TestAnalysisResult:
    """Tests for AnalysisResult dataclass."""
    
    @pytest.fixture
    def sample_gaps(self):
        """Create sample gaps for testing."""
        topic = TopicNode(name="test", required_depth=2)
        coverage = CoverageScore(
            topic_name="test",
            topic_path="domain.test",
            current_depth=0,
            required_depth=2
        )
        
        return [
            KnowledgeGap(
                gap_type=GapType.MISSING,
                priority=GapPriority.CRITICAL,
                topic=topic,
                coverage=coverage,
                description="Critical gap"
            ),
            KnowledgeGap(
                gap_type=GapType.SHALLOW,
                priority=GapPriority.HIGH,
                topic=topic,
                coverage=coverage,
                description="High gap"
            ),
            KnowledgeGap(
                gap_type=GapType.MISSING,
                priority=GapPriority.MEDIUM,
                topic=topic,
                coverage=coverage,
                description="Medium gap"
            ),
        ]
    
    @pytest.fixture
    def sample_scores(self):
        """Create sample coverage scores for testing."""
        return [
            CoverageScore("topic1", "d.topic1", current_depth=2, required_depth=2),
            CoverageScore("topic2", "d.topic2", current_depth=1, required_depth=2),
            CoverageScore("topic3", "d.topic3", current_depth=0, required_depth=2),
        ]
    
    def test_coverage_percentage(self, sample_gaps, sample_scores):
        """Test coverage_percentage calculation."""
        result = AnalysisResult(
            gaps=sample_gaps,
            coverage_scores=sample_scores,
            total_topics=3,
            covered_topics=1
        )
        
        assert result.coverage_percentage == pytest.approx(33.33, rel=0.01)
    
    def test_coverage_percentage_zero_topics(self):
        """Test coverage_percentage with zero topics."""
        result = AnalysisResult(
            gaps=[],
            coverage_scores=[],
            total_topics=0,
            covered_topics=0
        )
        
        assert result.coverage_percentage == 0.0
    
    def test_gaps_by_priority(self, sample_gaps, sample_scores):
        """Test gaps_by_priority grouping."""
        result = AnalysisResult(
            gaps=sample_gaps,
            coverage_scores=sample_scores,
            total_topics=3,
            covered_topics=1
        )
        
        by_priority = result.gaps_by_priority
        
        assert len(by_priority[GapPriority.CRITICAL]) == 1
        assert len(by_priority[GapPriority.HIGH]) == 1
        assert len(by_priority[GapPriority.MEDIUM]) == 1
        assert len(by_priority[GapPriority.LOW]) == 0
    
    def test_gaps_by_type(self, sample_gaps, sample_scores):
        """Test gaps_by_type grouping."""
        result = AnalysisResult(
            gaps=sample_gaps,
            coverage_scores=sample_scores,
            total_topics=3,
            covered_topics=1
        )
        
        by_type = result.gaps_by_type
        
        assert len(by_type[GapType.MISSING]) == 2
        assert len(by_type[GapType.SHALLOW]) == 1
    
    def test_get_top_gaps(self, sample_gaps, sample_scores):
        """Test get_top_gaps returns highest priority first."""
        result = AnalysisResult(
            gaps=sample_gaps,
            coverage_scores=sample_scores,
            total_topics=3,
            covered_topics=1
        )
        
        top_2 = result.get_top_gaps(2)
        
        assert len(top_2) == 2
        assert top_2[0].priority == GapPriority.CRITICAL
        assert top_2[1].priority == GapPriority.HIGH
    
    def test_to_dict(self, sample_gaps, sample_scores):
        """Test to_dict produces complete serializable output."""
        result = AnalysisResult(
            gaps=sample_gaps,
            coverage_scores=sample_scores,
            total_topics=10,
            covered_topics=7,
            taxonomy_used="test.json",
            files_analyzed=["file1.json", "file2.json"]
        )
        
        output = result.to_dict()
        
        assert "summary" in output
        assert output["summary"]["total_topics"] == 10
        assert output["summary"]["coverage_percentage"] == 70.0
        assert len(output["gaps"]) == 3
        assert output["taxonomy_used"] == "test.json"
        
        # Should be JSON serializable
        json.dumps(output)


class TestKnowledgeGapAnalyzer:
    """Tests for KnowledgeGapAnalyzer class."""
    
    def test_init(self, mock_knowledge_dir, taxonomy_dir):
        """Test analyzer initialization."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir, taxonomy_dir)
        
        assert analyzer.knowledge_dir == mock_knowledge_dir
        assert analyzer._knowledge_cache == {}
    
    def test_analyze_returns_result(self, knowledge_dir, taxonomy_dir):
        """Test analyze returns AnalysisResult."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        assert isinstance(result, AnalysisResult)
        assert result.total_topics > 0
    
    def test_load_knowledge_files(self, mock_knowledge_dir):
        """Test loading knowledge files into cache."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        analyzer._load_knowledge_files()
        
        assert len(analyzer._knowledge_cache) >= 1
        assert "test-patterns.json" in analyzer._knowledge_cache
    
    def test_load_knowledge_files_skips_invalid(self, tmp_path):
        """Test that invalid JSON files are skipped."""
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "valid.json").write_text('{"valid": true}')
        (knowledge_dir / "invalid.json").write_text('{ invalid }')
        
        analyzer = KnowledgeGapAnalyzer(knowledge_dir)
        analyzer._load_knowledge_files()
        
        assert "valid.json" in analyzer._knowledge_cache
        assert "invalid.json" not in analyzer._knowledge_cache
    
    def test_flatten_content_string(self, mock_knowledge_dir):
        """Test flattening string content."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        result = analyzer._flatten_content("Hello World")
        
        assert result == "hello world"
    
    def test_flatten_content_dict(self, mock_knowledge_dir):
        """Test flattening dictionary content."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        result = analyzer._flatten_content({"key": "Value", "nested": {"inner": "Data"}})
        
        assert "key" in result
        assert "value" in result
        assert "nested" in result
        assert "data" in result
    
    def test_flatten_content_list(self, mock_knowledge_dir):
        """Test flattening list content."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        result = analyzer._flatten_content(["item1", "item2"])
        
        assert "item1" in result
        assert "item2" in result
    
    def test_determine_depth_no_mentions(self, mock_knowledge_dir):
        """Test depth determination with no mentions."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        depth = analyzer._determine_depth(0, False, False)
        
        assert depth == 0
    
    def test_determine_depth_basic_mention(self, mock_knowledge_dir):
        """Test depth determination with basic mentions."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        depth = analyzer._determine_depth(2, False, False)
        
        assert depth == 1
    
    def test_determine_depth_with_examples(self, mock_knowledge_dir):
        """Test depth determination with examples."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        depth = analyzer._determine_depth(4, True, False)
        
        assert depth == 2
    
    def test_determine_depth_comprehensive(self, mock_knowledge_dir):
        """Test depth determination with all criteria."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir)
        
        depth = analyzer._determine_depth(6, True, True)
        
        assert depth == 3
    
    def test_get_extension_candidates(self, knowledge_dir, taxonomy_dir):
        """Test getting extension candidates."""
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze()
        
        candidates = analyzer.get_extension_candidates(result, max_candidates=5)
        
        assert len(candidates) <= 5
        # Candidates should be sorted by priority
        if len(candidates) >= 2:
            assert candidates[0].priority.value <= candidates[1].priority.value
    
    def test_save_report(self, mock_knowledge_dir, taxonomy_dir, tmp_path):
        """Test saving analysis report."""
        analyzer = KnowledgeGapAnalyzer(mock_knowledge_dir, taxonomy_dir)
        result = AnalysisResult(
            gaps=[],
            coverage_scores=[],
            total_topics=5,
            covered_topics=3
        )
        
        output_path = tmp_path / "report.json"
        analyzer.save_report(result, output_path)
        
        assert output_path.exists()
        
        with open(output_path) as f:
            saved = json.load(f)
        
        assert saved["summary"]["total_topics"] == 5


class TestRunGapAnalysis:
    """Tests for run_gap_analysis convenience function."""
    
    def test_run_with_defaults(self, knowledge_dir):
        """Test running gap analysis with defaults."""
        result = run_gap_analysis(knowledge_dir)
        
        assert isinstance(result, AnalysisResult)
    
    def test_run_with_custom_taxonomy(self, knowledge_dir, taxonomy_dir):
        """Test running gap analysis with custom taxonomy."""
        result = run_gap_analysis(
            knowledge_dir,
            taxonomy_name="agent_taxonomy.json"
        )
        
        assert result.taxonomy_used == "agent_taxonomy.json"
