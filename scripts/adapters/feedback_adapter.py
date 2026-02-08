"""
User Feedback Adapter for Knowledge Evolution

This adapter collects and processes feedback from generated projects,
learning from what works and what doesn't to improve knowledge files.

Features:
    - Feedback collection from generated projects
    - Success/failure pattern analysis
    - Common issue detection
    - Knowledge improvement suggestions

Note: This adapter works with local feedback data. Production use would
integrate with analytics or feedback collection systems.

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezonefrom pathlib import Path
from typing import Any, Dict, List, Optional
import json


from .base_adapter import (
    BaseAdapter,
    AdapterConfig,
    KnowledgeUpdate,
    KnowledgeChange,
    UpdatePriority,
    TrustLevel,
    ChangeType,
)


@dataclass
class ProjectFeedback:
    """Feedback from a generated project.
    
    Attributes:
        project_id: Unique project identifier
        blueprint_used: Blueprint that was used
        timestamp: When feedback was recorded
        success_metrics: Metrics indicating success
        issues: Issues encountered
        suggestions: Improvement suggestions
        knowledge_files_used: Which knowledge files were referenced
    """
    project_id: str
    blueprint_used: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))    success_metrics: Dict[str, Any] = field(default_factory=dict)
    issues: List[Dict[str, str]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    knowledge_files_used: List[str] = field(default_factory=list)


class FeedbackAdapter(BaseAdapter):
    """Adapter for learning from project feedback.
    
    This adapter analyzes feedback from generated projects to identify
    patterns that could improve knowledge files.
    
    Example:
        config = AdapterConfig()
        adapter = FeedbackAdapter(config, feedback_dir=Path("feedback/"))
        updates = await adapter.fetch_updates()
    """
    
    def __init__(
        self,
        config: AdapterConfig,
        feedback_dir: Optional[Path] = None,
        factory_root: Optional[Path] = None
    ):
        """Initialize the feedback adapter.
        
        Args:
            config: Adapter configuration
            feedback_dir: Directory containing feedback files
            factory_root: Factory root directory
        """
        super().__init__(config)
        config.trust_level = TrustLevel.COMMUNITY  # Feedback is community level
        
        if factory_root:
            self._factory_root = Path(factory_root)
        else:
            self._factory_root = Path(__file__).parent.parent.parent
        
        self._feedback_dir = feedback_dir or self._factory_root / "feedback"
        self._feedback_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def name(self) -> str:
        """Adapter identifier."""
        return "user_feedback"
    
    @property
    def description(self) -> str:
        """Human-readable description."""
        return "Learns from user feedback on generated projects"
    
    async def validate_connection(self) -> bool:
        """Validate feedback directory exists."""
        return self._feedback_dir.exists()
    
    async def fetch_updates(
        self,
        target_files: Optional[List[str]] = None,
        since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch updates based on collected feedback.
        
        Args:
            target_files: Optional filter by knowledge files
            since: Optional date filter
            
        Returns:
            List of proposed updates
        """
        updates: List[KnowledgeUpdate] = []
        
        # Load feedback data
        feedback_items = self._load_feedback(since)
        
        if not feedback_items:
            return updates
        
        # Analyze feedback for patterns
        analysis = self._analyze_feedback(feedback_items)
        
        # Generate updates based on analysis
        for knowledge_file, patterns in analysis.items():
            if target_files and knowledge_file not in target_files:
                continue
            
            changes = self._patterns_to_changes(patterns)
            
            if changes:
                update = KnowledgeUpdate(
                    target_file=knowledge_file,
                    priority=UpdatePriority.LOW,
                    source=self.create_source(
                        identifier="user_feedback",
                        version=datetime.now(timezone.utc).strftime("%Y%m%d"),                    ),
                    changes=changes,
                    new_version="1.0.0",  # Version determined by update engine
                    breaking=False,
                    rationale="Improvements based on user feedback",
                    axiom_alignment={
                        "A10": "Learning from actual usage",
                        "A2": "User primacy - improving based on user experience",
                    }
                )
                updates.append(update)
        
        return updates
    
    def _load_feedback(self, since: Optional[datetime] = None) -> List[ProjectFeedback]:
        """Load feedback files from the feedback directory.
        
        Args:
            since: Only load feedback after this date
            
        Returns:
            List of feedback items
        """
        feedback_items: List[ProjectFeedback] = []
        
        for feedback_file in self._feedback_dir.glob("*.json"):
            try:
                with open(feedback_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                timestamp_str = data.get("timestamp", datetime.now(timezone.utc).isoformat())
                timestamp = datetime.fromisoformat(timestamp_str)
                # Ensure timezone-aware
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=timezone.utc)                
                if since and timestamp < since:
                    continue
                
                feedback = ProjectFeedback(
                    project_id=data.get("project_id", feedback_file.stem),
                    blueprint_used=data.get("blueprint_used", "unknown"),
                    timestamp=timestamp,
                    success_metrics=data.get("success_metrics", {}),
                    issues=data.get("issues", []),
                    suggestions=data.get("suggestions", []),
                    knowledge_files_used=data.get("knowledge_files_used", []),
                )
                feedback_items.append(feedback)
            except Exception:
                continue
        
        return feedback_items
    
    def _analyze_feedback(
        self,
        feedback_items: List[ProjectFeedback]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze feedback to find patterns.
        
        Args:
            feedback_items: List of feedback to analyze
            
        Returns:
            Dictionary mapping knowledge files to detected patterns
        """
        # Group by knowledge file
        by_file: Dict[str, List[ProjectFeedback]] = {}
        for fb in feedback_items:
            for kf in fb.knowledge_files_used:
                if kf not in by_file:
                    by_file[kf] = []
                by_file[kf].append(fb)
        
        # Analyze patterns for each file
        analysis: Dict[str, List[Dict[str, Any]]] = {}
        
        for knowledge_file, items in by_file.items():
            patterns = []
            
            # Count issue frequencies
            issue_counts: Dict[str, int] = {}
            for fb in items:
                for issue in fb.issues:
                    issue_type = issue.get("type", "unknown")
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
            
            # Identify common issues (occurring in >30% of projects)
            threshold = len(items) * 0.3
            for issue_type, count in issue_counts.items():
                if count >= max(threshold, 2):
                    patterns.append({
                        "type": "common_issue",
                        "issue": issue_type,
                        "frequency": count,
                        "total_projects": len(items),
                    })
            
            # Collect suggestions
            suggestion_counts: Dict[str, int] = {}
            for fb in items:
                for suggestion in fb.suggestions:
                    suggestion_counts[suggestion] = suggestion_counts.get(suggestion, 0) + 1
            
            for suggestion, count in suggestion_counts.items():
                if count >= 2:
                    patterns.append({
                        "type": "suggestion",
                        "content": suggestion,
                        "frequency": count,
                    })
            
            if patterns:
                analysis[knowledge_file] = patterns
        
        return analysis
    
    def _patterns_to_changes(
        self,
        patterns: List[Dict[str, Any]]
    ) -> List[KnowledgeChange]:
        """Convert detected patterns to knowledge changes.
        
        Args:
            patterns: List of detected patterns
            
        Returns:
            List of knowledge changes
        """
        changes: List[KnowledgeChange] = []
        
        for pattern in patterns:
            if pattern["type"] == "common_issue":
                changes.append(KnowledgeChange(
                    change_type=ChangeType.ADDED,
                    path="feedback.common_issues",
                    description=f"Common issue detected: {pattern['issue']} ({pattern['frequency']} occurrences)",
                    impact="medium",
                ))
            elif pattern["type"] == "suggestion":
                changes.append(KnowledgeChange(
                    change_type=ChangeType.ADDED,
                    path="feedback.suggestions",
                    description=f"User suggestion: {pattern['content']}",
                    impact="low",
                ))
        
        return changes
    
    def record_feedback(self, feedback: ProjectFeedback) -> None:
        """Record new feedback to the feedback directory.
        
        Args:
            feedback: Feedback to record
        """
        feedback_file = self._feedback_dir / f"{feedback.project_id}.json"
        
        data = {
            "project_id": feedback.project_id,
            "blueprint_used": feedback.blueprint_used,
            "timestamp": feedback.timestamp.isoformat(),
            "success_metrics": feedback.success_metrics,
            "issues": feedback.issues,
            "suggestions": feedback.suggestions,
            "knowledge_files_used": feedback.knowledge_files_used,
        }
        
        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
