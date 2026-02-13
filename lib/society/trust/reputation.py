"""
Reputation System

Scoring and tracking agent reputation based on axiom compliance.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import logging
import math

logger = logging.getLogger(__name__)


class ReputationType(Enum):
    """Types of reputation contributions."""
    AXIOM_COMPLIANCE = "axiom_compliance"
    CONTRACT_FULFILLMENT = "contract_fulfillment"
    PEER_ENDORSEMENT = "peer_endorsement"
    HISTORICAL = "historical"


@dataclass
class ReputationEvent:
    """
    Record of a reputation-affecting event.
    
    Attributes:
        timestamp: When the event occurred.
        type: Type of reputation contribution.
        delta: Change in reputation (+/-).
        reason: Explanation of the change.
        source: Agent or system that reported the event.
    """
    timestamp: datetime
    type: ReputationType
    delta: float
    reason: str = ""
    source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "type": self.type.value,
            "delta": self.delta,
            "reason": self.reason,
            "source": self.source,
        }


@dataclass
class ReputationScore:
    """
    Agent reputation score with history.
    
    Attributes:
        agent_id: The agent this score belongs to.
        current_score: Current reputation score.
        history: Recent reputation events.
        first_seen: When agent was first observed.
        last_updated: When score was last updated.
    """
    agent_id: str
    current_score: float = 50.0  # Start at neutral
    history: List[ReputationEvent] = field(default_factory=list)
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Score bounds
    MIN_SCORE = 0.0
    MAX_SCORE = 100.0
    DEFAULT_SCORE = 50.0
    
    @property
    def trust_level(self) -> str:
        """Get human-readable trust level."""
        if self.current_score >= 80:
            return "high"
        elif self.current_score >= 50:
            return "medium"
        elif self.current_score >= 20:
            return "low"
        else:
            return "untrusted"
    
    @property
    def is_trusted(self) -> bool:
        """Check if agent is considered trusted."""
        return self.current_score >= 50.0
    
    def add_event(self, event: ReputationEvent) -> None:
        """Add a reputation event and update score."""
        self.history.append(event)
        self.current_score = max(
            self.MIN_SCORE,
            min(self.MAX_SCORE, self.current_score + event.delta)
        )
        self.last_updated = datetime.now(timezone.utc)
    
    def get_recent_history(
        self,
        limit: int = 10,
        window: Optional[timedelta] = None
    ) -> List[ReputationEvent]:
        """Get recent reputation events."""
        events = self.history
        
        if window:
            cutoff = datetime.now(timezone.utc) - window
            events = [e for e in events if e.timestamp > cutoff]
        
        return events[-limit:]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "current_score": self.current_score,
            "trust_level": self.trust_level,
            "history": [e.to_dict() for e in self.history[-10:]],
            "first_seen": self.first_seen.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }


class ReputationSystem:
    """
    Manages agent reputation across the society.
    
    Features:
    - Axiom compliance tracking
    - Contract fulfillment scoring
    - Peer endorsements
    - Time-decay for old events
    
    Usage:
        reputation = ReputationSystem()
        reputation.record_compliance(agent_id, True, "Followed A1 axiom")
        score = reputation.get_score(agent_id)
        
        if score.is_trusted:
            # Allow privileged operations
    """
    
    # Reputation change amounts
    COMPLIANCE_BONUS = 2.0
    VIOLATION_PENALTY = -5.0
    CONTRACT_FULFILLED_BONUS = 3.0
    CONTRACT_VIOLATED_PENALTY = -10.0
    ENDORSEMENT_BONUS = 1.0
    
    # Decay settings
    DECAY_HALF_LIFE_DAYS = 30
    
    def __init__(self, decay_enabled: bool = True):
        """
        Initialize reputation system.
        
        Args:
            decay_enabled: Whether to apply time decay to scores.
        """
        self._scores: Dict[str, ReputationScore] = {}
        self.decay_enabled = decay_enabled
    
    def get_score(self, agent_id: str) -> ReputationScore:
        """
        Get reputation score for an agent.
        
        Creates default score if agent is new.
        
        Args:
            agent_id: The agent ID.
            
        Returns:
            ReputationScore for the agent.
        """
        if agent_id not in self._scores:
            self._scores[agent_id] = ReputationScore(agent_id=agent_id)
        
        score = self._scores[agent_id]
        
        # Apply decay if enabled
        if self.decay_enabled:
            self._apply_decay(score)
        
        return score
    
    def record_compliance(
        self,
        agent_id: str,
        compliant: bool,
        reason: str = "",
        axiom: Optional[str] = None
    ) -> None:
        """
        Record axiom compliance or violation.
        
        Args:
            agent_id: The agent ID.
            compliant: Whether agent was compliant.
            reason: Explanation.
            axiom: Optional axiom identifier.
        """
        score = self.get_score(agent_id)
        
        delta = self.COMPLIANCE_BONUS if compliant else self.VIOLATION_PENALTY
        
        event = ReputationEvent(
            timestamp=datetime.now(timezone.utc),
            type=ReputationType.AXIOM_COMPLIANCE,
            delta=delta,
            reason=reason or f"Axiom {'compliance' if compliant else 'violation'}{': ' + axiom if axiom else ''}",
        )
        
        score.add_event(event)
        
        if not compliant:
            logger.warning(f"Reputation penalty for {agent_id}: {reason}")
    
    def record_contract_event(
        self,
        agent_id: str,
        fulfilled: bool,
        contract_id: str,
        reason: str = ""
    ) -> None:
        """
        Record contract fulfillment or violation.
        
        Args:
            agent_id: The agent ID.
            fulfilled: Whether contract was fulfilled.
            contract_id: The contract ID.
            reason: Explanation.
        """
        score = self.get_score(agent_id)
        
        delta = self.CONTRACT_FULFILLED_BONUS if fulfilled else self.CONTRACT_VIOLATED_PENALTY
        
        event = ReputationEvent(
            timestamp=datetime.now(timezone.utc),
            type=ReputationType.CONTRACT_FULFILLMENT,
            delta=delta,
            reason=reason or f"Contract {contract_id} {'fulfilled' if fulfilled else 'violated'}",
            source=contract_id,
        )
        
        score.add_event(event)
    
    def record_endorsement(
        self,
        agent_id: str,
        endorser_id: str,
        positive: bool = True,
        reason: str = ""
    ) -> None:
        """
        Record a peer endorsement.
        
        Args:
            agent_id: The agent receiving endorsement.
            endorser_id: The endorsing agent.
            positive: Whether endorsement is positive.
            reason: Explanation.
        """
        # Get endorser's reputation to weight the endorsement
        endorser_score = self.get_score(endorser_id)
        
        # Weight by endorser's trust level
        weight = endorser_score.current_score / 100.0
        delta = self.ENDORSEMENT_BONUS * weight * (1 if positive else -1)
        
        target_score = self.get_score(agent_id)
        
        event = ReputationEvent(
            timestamp=datetime.now(timezone.utc),
            type=ReputationType.PEER_ENDORSEMENT,
            delta=delta,
            reason=reason or f"{'Positive' if positive else 'Negative'} endorsement from {endorser_id}",
            source=endorser_id,
        )
        
        target_score.add_event(event)
    
    def _apply_decay(self, score: ReputationScore) -> None:
        """Apply time decay to move score toward neutral."""
        if not score.history:
            return
        
        last_update = score.last_updated
        now = datetime.now(timezone.utc)
        days_elapsed = (now - last_update).total_seconds() / 86400
        
        if days_elapsed < 1:
            return
        
        # Decay factor: half-life decay toward neutral
        decay_factor = math.pow(0.5, days_elapsed / self.DECAY_HALF_LIFE_DAYS)
        
        # Move toward neutral (50)
        deviation = score.current_score - ReputationScore.DEFAULT_SCORE
        decayed_deviation = deviation * decay_factor
        score.current_score = ReputationScore.DEFAULT_SCORE + decayed_deviation
        score.last_updated = now
    
    def get_trusted_agents(
        self,
        min_score: float = 50.0
    ) -> List[str]:
        """Get list of trusted agents."""
        return [
            agent_id
            for agent_id, score in self._scores.items()
            if score.current_score >= min_score
        ]
    
    def get_rankings(self, limit: int = 10) -> List[tuple]:
        """
        Get top agents by reputation.
        
        Returns:
            List of (agent_id, score) tuples.
        """
        rankings = [
            (agent_id, score.current_score)
            for agent_id, score in self._scores.items()
        ]
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings[:limit]
    
    def export(self) -> Dict[str, Any]:
        """Export reputation data."""
        return {
            agent_id: score.to_dict()
            for agent_id, score in self._scores.items()
        }
