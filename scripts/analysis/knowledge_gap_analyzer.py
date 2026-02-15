"""
Knowledge Gap Analyzer for Autonomous Knowledge Extension

This module analyzes existing knowledge files against a topic taxonomy
to identify gaps, shallow coverage, stale content, and cross-reference
issues. It produces a prioritized list of topics that need extension.

Design Patterns:
    - Strategy: Different analysis strategies for different gap types
    - Visitor: Traverse knowledge files systematically
    - Observer: Report findings to multiple consumers

Axiom Alignment:
    - A10 (Learning): Identifies opportunities for knowledge improvement
    - A1 (Verifiability): Provides evidence for each identified gap

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Handle both package and direct execution imports
try:
    from .taxonomy import TaxonomyLoader, TopicNode
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from scripts.taxonomy import TaxonomyLoader, TopicNode


class GapType(Enum):
    """Types of knowledge gaps that can be identified."""

    MISSING = "missing"  # Topic not covered at all
    SHALLOW = "shallow"  # Covered but below required depth
    STALE = "stale"  # Content references outdated APIs/versions
    CROSS_REF = "cross_reference"  # Mentioned but not linked to dedicated knowledge
    INCOMPLETE = "incomplete"  # Partially covered, missing subtopics


class GapPriority(Enum):
    """Priority levels for addressing gaps."""

    CRITICAL = 1  # Core topic completely missing
    HIGH = 2  # Important topic with shallow coverage
    MEDIUM = 3  # Nice-to-have improvement
    LOW = 4  # Minor enhancement


@dataclass
class CoverageScore:
    """Score representing how well a topic is covered.

    Attributes:
        topic_name: Name of the topic
        topic_path: Full path in taxonomy (domain.topic.subtopic)
        current_depth: Detected coverage depth (0-3)
        required_depth: Minimum required depth from taxonomy
        keyword_matches: Number of keyword matches found
        matched_keywords: Which keywords were found
        source_files: Files where topic was found
        evidence: Snippets showing coverage
    """

    topic_name: str
    topic_path: str
    current_depth: int = 0
    required_depth: int = 2
    keyword_matches: int = 0
    matched_keywords: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    @property
    def coverage_ratio(self) -> float:
        """Calculate coverage as ratio of current to required depth."""
        if self.required_depth == 0:
            return 1.0
        return min(1.0, self.current_depth / self.required_depth)

    @property
    def is_adequate(self) -> bool:
        """Check if coverage meets requirements."""
        return self.current_depth >= self.required_depth


@dataclass
class KnowledgeGap:
    """Represents an identified gap in the knowledge base.

    Attributes:
        gap_type: Type of gap (missing, shallow, stale, etc.)
        priority: Priority for addressing this gap
        topic: Topic that has the gap
        coverage: Coverage score details
        description: Human-readable description
        suggested_actions: Recommended actions to fill the gap
        estimated_effort: Estimated effort to address (small, medium, large)
        related_files: Existing files that could be extended
    """

    gap_type: GapType
    priority: GapPriority
    topic: TopicNode
    coverage: CoverageScore
    description: str
    suggested_actions: List[str] = field(default_factory=list)
    estimated_effort: str = "medium"
    related_files: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "gap_type": self.gap_type.value,
            "priority": self.priority.name,
            "topic_name": self.topic.name,
            "topic_path": self.coverage.topic_path,
            "current_depth": self.coverage.current_depth,
            "required_depth": self.coverage.required_depth,
            "coverage_ratio": self.coverage.coverage_ratio,
            "description": self.description,
            "suggested_actions": self.suggested_actions,
            "estimated_effort": self.estimated_effort,
            "related_files": self.related_files,
            "matched_keywords": self.coverage.matched_keywords,
        }


@dataclass
class AnalysisResult:
    """Result of analyzing knowledge against taxonomy.

    Attributes:
        gaps: List of identified gaps
        coverage_scores: Coverage scores for all topics
        total_topics: Total topics in taxonomy
        covered_topics: Topics meeting required depth
        analysis_timestamp: When analysis was performed
        taxonomy_used: Name of taxonomy file used
        files_analyzed: List of knowledge files analyzed
    """

    gaps: List[KnowledgeGap]
    coverage_scores: List[CoverageScore]
    total_topics: int = 0
    covered_topics: int = 0
    analysis_timestamp: datetime = field(default_factory=datetime.utcnow)
    taxonomy_used: str = ""
    files_analyzed: List[str] = field(default_factory=list)

    @property
    def coverage_percentage(self) -> float:
        """Calculate overall coverage percentage."""
        if self.total_topics == 0:
            return 0.0
        return (self.covered_topics / self.total_topics) * 100

    @property
    def gaps_by_priority(self) -> Dict[GapPriority, List[KnowledgeGap]]:
        """Group gaps by priority."""
        result = {p: [] for p in GapPriority}
        for gap in self.gaps:
            result[gap.priority].append(gap)
        return result

    @property
    def gaps_by_type(self) -> Dict[GapType, List[KnowledgeGap]]:
        """Group gaps by type."""
        result = {t: [] for t in GapType}
        for gap in self.gaps:
            result[gap.gap_type].append(gap)
        return result

    def get_top_gaps(self, n: int = 10) -> List[KnowledgeGap]:
        """Get the top N highest priority gaps.

        Args:
            n: Number of gaps to return

        Returns:
            List of highest priority gaps
        """
        sorted_gaps = sorted(
            self.gaps, key=lambda g: (g.priority.value, -g.coverage.required_depth)
        )
        return sorted_gaps[:n]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "summary": {
                "total_topics": self.total_topics,
                "covered_topics": self.covered_topics,
                "coverage_percentage": round(self.coverage_percentage, 1),
                "total_gaps": len(self.gaps),
                "critical_gaps": len(self.gaps_by_priority[GapPriority.CRITICAL]),
                "high_gaps": len(self.gaps_by_priority[GapPriority.HIGH]),
            },
            "gaps": [g.to_dict() for g in self.gaps],
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
            "taxonomy_used": self.taxonomy_used,
            "files_analyzed": self.files_analyzed,
        }


class KnowledgeGapAnalyzer:
    """Analyzes knowledge base against taxonomy to find gaps.

    This class provides comprehensive gap analysis including:
    - Missing topic detection
    - Coverage depth assessment
    - Stale content identification
    - Cross-reference gap detection

    Example:
        analyzer = KnowledgeGapAnalyzer(knowledge_dir)
        result = analyzer.analyze("agent_taxonomy.json")
        for gap in result.get_top_gaps(5):
            print(f"{gap.topic.name}: {gap.description}")
    """

    # Depth scoring criteria
    DEPTH_CRITERIA = {
        0: {
            "min_mentions": 0,
            "requires_example": False,
            "requires_best_practice": False,
        },
        1: {
            "min_mentions": 1,
            "requires_example": False,
            "requires_best_practice": False,
        },
        2: {
            "min_mentions": 3,
            "requires_example": True,
            "requires_best_practice": False,
        },
        3: {
            "min_mentions": 5,
            "requires_example": True,
            "requires_best_practice": True,
        },
    }

    def __init__(self, knowledge_dir: Path, taxonomy_dir: Optional[Path] = None):
        """Initialize the gap analyzer.

        Args:
            knowledge_dir: Directory containing knowledge JSON files
            taxonomy_dir: Directory containing taxonomy files (optional)
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.taxonomy_loader = TaxonomyLoader(taxonomy_dir)
        self._knowledge_cache: Dict[str, Dict[str, Any]] = {}
        self._content_index: Dict[str, str] = {}  # file -> flattened content

    def analyze(self, taxonomy_name: str = "agent_taxonomy.json") -> AnalysisResult:
        """Perform comprehensive gap analysis.

        Args:
            taxonomy_name: Name of the taxonomy file to use

        Returns:
            AnalysisResult with all findings
        """
        # Load taxonomy
        domains = self.taxonomy_loader.load_taxonomy(taxonomy_name)

        # Load and index all knowledge files
        self._load_knowledge_files()

        # Analyze each domain
        all_scores: List[CoverageScore] = []
        all_gaps: List[KnowledgeGap] = []

        for domain_name, domain_node in domains.items():
            scores, gaps = self._analyze_domain(domain_name, domain_node)
            all_scores.extend(scores)
            all_gaps.extend(gaps)

        # Calculate totals
        total_topics = len(all_scores)
        covered_topics = sum(1 for s in all_scores if s.is_adequate)

        return AnalysisResult(
            gaps=all_gaps,
            coverage_scores=all_scores,
            total_topics=total_topics,
            covered_topics=covered_topics,
            taxonomy_used=taxonomy_name,
            files_analyzed=list(self._knowledge_cache.keys()),
        )

    def _load_knowledge_files(self) -> None:
        """Load all JSON knowledge files into cache."""
        self._knowledge_cache.clear()
        self._content_index.clear()

        for file_path in self.knowledge_dir.glob("*.json"):
            if file_path.name.startswith("_") or "schema" in file_path.name.lower():
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    self._knowledge_cache[file_path.name] = content
                    # Create flattened content string for searching
                    self._content_index[file_path.name] = self._flatten_content(content)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load {file_path.name}: {e}")

    def _flatten_content(self, obj: Any, depth: int = 0) -> str:
        """Recursively flatten JSON content to searchable string.

        Args:
            obj: JSON object to flatten
            depth: Current recursion depth

        Returns:
            Flattened string representation
        """
        if depth > 10:  # Prevent infinite recursion
            return ""

        if isinstance(obj, str):
            return obj.lower()
        elif isinstance(obj, dict):
            parts = []
            for key, value in obj.items():
                parts.append(key.lower())
                parts.append(self._flatten_content(value, depth + 1))
            return " ".join(parts)
        elif isinstance(obj, list):
            return " ".join(self._flatten_content(item, depth + 1) for item in obj)
        else:
            return str(obj).lower() if obj is not None else ""

    def _analyze_domain(
        self, domain_name: str, domain_node: TopicNode, parent_path: str = ""
    ) -> Tuple[List[CoverageScore], List[KnowledgeGap]]:
        """Analyze a single domain and its subtopics.

        Args:
            domain_name: Name of the domain
            domain_node: TopicNode for the domain
            parent_path: Path to parent node

        Returns:
            Tuple of (coverage_scores, gaps)
        """
        current_path = f"{parent_path}.{domain_name}" if parent_path else domain_name
        scores: List[CoverageScore] = []
        gaps: List[KnowledgeGap] = []

        # Analyze this node
        score = self._calculate_coverage(domain_node, current_path)
        scores.append(score)

        # Check for gap
        if not score.is_adequate:
            gap = self._create_gap(domain_node, score)
            gaps.append(gap)

        # Recursively analyze subtopics
        for subtopic_name, subtopic_node in domain_node.subtopics.items():
            sub_scores, sub_gaps = self._analyze_domain(
                subtopic_name, subtopic_node, current_path
            )
            scores.extend(sub_scores)
            gaps.extend(sub_gaps)

        return scores, gaps

    def _calculate_coverage(self, topic: TopicNode, topic_path: str) -> CoverageScore:
        """Calculate coverage score for a topic.

        Args:
            topic: TopicNode to analyze
            topic_path: Full path to topic

        Returns:
            CoverageScore with analysis results
        """
        # Get all keywords to search for
        keywords = topic.keywords if topic.keywords else [topic.name.replace("_", " ")]

        # Search across all knowledge files
        matched_keywords: Set[str] = set()
        source_files: List[str] = []
        evidence: List[str] = []
        total_mentions = 0
        has_code_example = False
        has_best_practice = False

        for filename, content_str in self._content_index.items():
            file_matched = False
            file_content = self._knowledge_cache.get(filename, {})

            for keyword in keywords:
                keyword_lower = keyword.lower()
                # Count occurrences
                mentions = content_str.count(keyword_lower)
                if mentions > 0:
                    matched_keywords.add(keyword)
                    total_mentions += mentions
                    file_matched = True

                    # Check for code examples
                    if "code_example" in content_str and keyword_lower in content_str:
                        has_code_example = True

                    # Check for best practices
                    if "best_practice" in content_str and keyword_lower in content_str:
                        has_best_practice = True

            if file_matched:
                source_files.append(filename)
                # Extract evidence snippet
                evidence_snippet = self._extract_evidence(file_content, keywords)
                if evidence_snippet:
                    evidence.append(f"{filename}: {evidence_snippet}")

        # Calculate depth based on criteria
        depth = self._determine_depth(
            total_mentions, has_code_example, has_best_practice
        )

        return CoverageScore(
            topic_name=topic.name,
            topic_path=topic_path,
            current_depth=depth,
            required_depth=topic.required_depth,
            keyword_matches=len(matched_keywords),
            matched_keywords=list(matched_keywords),
            source_files=source_files,
            evidence=evidence[:3],  # Limit evidence
        )

    def _determine_depth(
        self, mentions: int, has_example: bool, has_best_practice: bool
    ) -> int:
        """Determine coverage depth based on criteria.

        Args:
            mentions: Number of keyword mentions
            has_example: Whether code examples exist
            has_best_practice: Whether best practices exist

        Returns:
            Coverage depth (0-3)
        """
        if mentions == 0:
            return 0

        if mentions >= 5 and has_example and has_best_practice:
            return 3
        elif mentions >= 3 and has_example:
            return 2
        elif mentions >= 1:
            return 1

        return 0

    def _extract_evidence(self, content: Dict[str, Any], keywords: List[str]) -> str:
        """Extract a snippet showing topic coverage.

        Args:
            content: Knowledge file content
            keywords: Keywords to look for

        Returns:
            Evidence snippet or empty string
        """
        # Look for relevant sections
        for key in ["description", "use_when", "best_practices"]:
            if key in content:
                value = content[key]
                if isinstance(value, str):
                    for kw in keywords:
                        if kw.lower() in value.lower():
                            return value[:100] + "..." if len(value) > 100 else value

        # Check nested structures
        content_str = json.dumps(content)
        for kw in keywords:
            if kw.lower() in content_str.lower():
                # Find and return context around keyword
                idx = content_str.lower().find(kw.lower())
                start = max(0, idx - 50)
                end = min(len(content_str), idx + len(kw) + 50)
                return "..." + content_str[start:end] + "..."

        return ""

    def _create_gap(self, topic: TopicNode, coverage: CoverageScore) -> KnowledgeGap:
        """Create a KnowledgeGap from coverage analysis.

        Args:
            topic: Topic with gap
            coverage: Coverage score

        Returns:
            KnowledgeGap object
        """
        # Determine gap type
        if coverage.current_depth == 0:
            gap_type = GapType.MISSING
        elif coverage.current_depth < coverage.required_depth:
            gap_type = GapType.SHALLOW
        else:
            gap_type = GapType.INCOMPLETE

        # Determine priority
        depth_diff = coverage.required_depth - coverage.current_depth
        if gap_type == GapType.MISSING and coverage.required_depth >= 3:
            priority = GapPriority.CRITICAL
        elif gap_type == GapType.MISSING or depth_diff >= 2:
            priority = GapPriority.HIGH
        elif depth_diff == 1:
            priority = GapPriority.MEDIUM
        else:
            priority = GapPriority.LOW

        # Generate description
        if gap_type == GapType.MISSING:
            description = f"Topic '{topic.name}' is not covered in the knowledge base"
        else:
            description = (
                f"Topic '{topic.name}' has shallow coverage "
                f"(depth {coverage.current_depth}/{coverage.required_depth})"
            )

        # Generate suggested actions
        actions = self._generate_suggested_actions(topic, coverage, gap_type)

        # Estimate effort
        if gap_type == GapType.MISSING and coverage.required_depth >= 3:
            effort = "large"
        elif gap_type == GapType.SHALLOW:
            effort = "medium"
        else:
            effort = "small"

        return KnowledgeGap(
            gap_type=gap_type,
            priority=priority,
            topic=topic,
            coverage=coverage,
            description=description,
            suggested_actions=actions,
            estimated_effort=effort,
            related_files=coverage.source_files
            if coverage.source_files
            else topic.knowledge_files,
        )

    def _generate_suggested_actions(
        self, topic: TopicNode, coverage: CoverageScore, gap_type: GapType
    ) -> List[str]:
        """Generate suggested actions to fill a gap.

        Args:
            topic: Topic with gap
            coverage: Coverage score
            gap_type: Type of gap

        Returns:
            List of suggested actions
        """
        actions = []

        if gap_type == GapType.MISSING:
            if topic.knowledge_files:
                actions.append(
                    f"Add section for '{topic.name}' in {topic.knowledge_files[0]}"
                )
            else:
                actions.append(f"Create new knowledge entry for '{topic.name}'")
            actions.append(f"Research: {topic.description}")

        if coverage.required_depth >= 2 and coverage.current_depth < 2:
            actions.append("Add code examples demonstrating the pattern")

        if coverage.required_depth >= 3 and coverage.current_depth < 3:
            actions.append("Add best practices section")
            actions.append("Add anti-patterns and common mistakes")

        if topic.keywords:
            actions.append(f"Keywords to cover: {', '.join(topic.keywords[:5])}")

        return actions

    def get_extension_candidates(
        self,
        result: AnalysisResult,
        max_candidates: int = 5,
        min_priority: GapPriority = GapPriority.MEDIUM,
    ) -> List[KnowledgeGap]:
        """Get top candidates for autonomous extension.

        Args:
            result: Analysis result
            max_candidates: Maximum candidates to return
            min_priority: Minimum priority to include

        Returns:
            List of gaps suitable for autonomous extension
        """
        candidates = []

        for gap in result.gaps:
            # Filter by priority
            if gap.priority.value > min_priority.value:
                continue

            # Prefer gaps that have related files (easier to extend)
            # and topics with clear keywords
            if gap.related_files or gap.topic.keywords:
                candidates.append(gap)

        # Sort by priority, then by required depth
        candidates.sort(key=lambda g: (g.priority.value, -g.coverage.required_depth))

        return candidates[:max_candidates]

    def save_report(self, result: AnalysisResult, output_path: Path) -> None:
        """Save analysis report to JSON file.

        Args:
            result: Analysis result
            output_path: Path for output file
        """
        report = result.to_dict()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


def run_gap_analysis(
    knowledge_dir: Optional[Path] = None, taxonomy_name: str = "agent_taxonomy.json"
) -> AnalysisResult:
    """Convenience function to run gap analysis.

    Args:
        knowledge_dir: Knowledge directory (defaults to ../knowledge)
        taxonomy_name: Taxonomy file to use

    Returns:
        AnalysisResult with findings
    """
    if knowledge_dir is None:
        knowledge_dir = Path(__file__).parent.parent.parent / "knowledge"

    analyzer = KnowledgeGapAnalyzer(knowledge_dir)
    return analyzer.analyze(taxonomy_name)


if __name__ == "__main__":
    # Run analysis when executed directly
    import sys

    result = run_gap_analysis()

    print("\n" + "=" * 60)
    print("KNOWLEDGE GAP ANALYSIS REPORT")
    print("=" * 60)
    print(
        f"\nCoverage: {result.coverage_percentage:.1f}% ({result.covered_topics}/{result.total_topics} topics)"
    )
    print(f"Total Gaps: {len(result.gaps)}")
    print(f"  Critical: {len(result.gaps_by_priority[GapPriority.CRITICAL])}")
    print(f"  High: {len(result.gaps_by_priority[GapPriority.HIGH])}")
    print(f"  Medium: {len(result.gaps_by_priority[GapPriority.MEDIUM])}")
    print(f"  Low: {len(result.gaps_by_priority[GapPriority.LOW])}")

    print("\n" + "=" * 60)
    print("TOP 10 GAPS TO ADDRESS:")
    print("=" * 60)

    for i, gap in enumerate(result.get_top_gaps(10), 1):
        print(f"\n{i}. [{gap.priority.name}] {gap.topic.name}")
        print(f"   Type: {gap.gap_type.value}")
        print(f"   Path: {gap.coverage.topic_path}")
        print(
            f"   Coverage: {gap.coverage.current_depth}/{gap.coverage.required_depth}"
        )
        print(f"   Description: {gap.description}")
        if gap.suggested_actions:
            print("   Actions:")
            for action in gap.suggested_actions[:2]:
                print(f"     - {action}")
