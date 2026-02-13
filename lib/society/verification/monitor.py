"""
Axiom Compliance Monitor

Central monitor for verifying agent events against all axioms.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging

from lib.society.events.schema import AgentEvent
from lib.society.verification.verifiers.base import AxiomVerifier, AxiomResult

logger = logging.getLogger(__name__)


class VerificationStatus(Enum):
    """Status of event verification."""
    PENDING = "pending"
    VERIFIED = "verified"
    VIOLATION = "violation"
    ESCALATED = "escalated"


@dataclass
class VerificationResult:
    """
    Complete verification result for an event.
    
    Attributes:
        event_id: ID of the verified event.
        status: Overall verification status.
        axiom_results: Results from each axiom verifier.
        verified_at: Timestamp of verification.
        escalated: Whether violation was escalated.
    """
    event_id: str
    status: VerificationStatus
    axiom_results: List[AxiomResult]
    verified_at: datetime = field(default_factory=datetime.utcnow)
    escalated: bool = False
    
    def has_violations(self) -> bool:
        """Check if any axiom was violated."""
        return any(not r.passed for r in self.axiom_results)
    
    def get_violations(self) -> List[AxiomResult]:
        """Get list of violated axioms."""
        return [r for r in self.axiom_results if not r.passed]
    
    def get_passing(self) -> List[AxiomResult]:
        """Get list of passing axioms."""
        return [r for r in self.axiom_results if r.passed]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "status": self.status.value,
            "axiom_results": [r.to_dict() for r in self.axiom_results],
            "verified_at": self.verified_at.isoformat(),
            "escalated": self.escalated,
        }


# Type alias for violation handlers
ViolationHandler = Callable[[AgentEvent, VerificationResult], None]


class AxiomComplianceMonitor:
    """
    Monitors agent events for axiom compliance.
    
    Implements real-time verification against foundational axioms
    with configurable escalation thresholds.
    
    Usage:
        monitor = AxiomComplianceMonitor()
        monitor.register_default_verifiers()
        result = monitor.verify(event)
        
        if result.has_violations():
            for violation in result.get_violations():
                print(f"Violated {violation.axiom.name}: {violation.reason}")
    """
    
    def __init__(
        self,
        escalation_threshold: int = 3,
        escalation_window: timedelta = timedelta(hours=24),
    ):
        """
        Initialize monitor.
        
        Args:
            escalation_threshold: Number of violations before escalation.
            escalation_window: Time window for counting violations.
        """
        self.escalation_threshold = escalation_threshold
        self.escalation_window = escalation_window
        
        self._verifiers: List[AxiomVerifier] = []
        self._violation_handlers: List[ViolationHandler] = []
        self._violation_history: Dict[str, List[datetime]] = {}  # agent_id -> times
    
    @property
    def verifiers(self) -> List[AxiomVerifier]:
        """Get registered verifiers."""
        return list(self._verifiers)
    
    def register_verifier(self, verifier: AxiomVerifier) -> None:
        """
        Register an axiom verifier.
        
        Args:
            verifier: The verifier to register.
        """
        self._verifiers.append(verifier)
        logger.info(f"Registered verifier: {verifier.name}")
    
    def register_default_verifiers(self) -> None:
        """Register all default axiom verifiers (A0-A5)."""
        from lib.society.verification.verifiers import (
            A0SDGVerifier,
            A1LoveVerifier,
            A2TruthVerifier,
            A3BeautyVerifier,
            A4GuardianVerifier,
            A5MemoryVerifier,
        )
        
        self.register_verifier(A0SDGVerifier())
        self.register_verifier(A1LoveVerifier())
        self.register_verifier(A2TruthVerifier())
        self.register_verifier(A3BeautyVerifier())
        self.register_verifier(A4GuardianVerifier())
        self.register_verifier(A5MemoryVerifier())
    
    def register_violation_handler(self, handler: ViolationHandler) -> None:
        """
        Register a handler for violations.
        
        Args:
            handler: Callback receiving (event, result) on violation.
        """
        self._violation_handlers.append(handler)
    
    def unregister_violation_handler(self, handler: ViolationHandler) -> None:
        """
        Unregister a violation handler.
        
        Args:
            handler: The handler to remove.
        """
        if handler in self._violation_handlers:
            self._violation_handlers.remove(handler)
    
    def verify(self, event: AgentEvent) -> VerificationResult:
        """
        Verify event against all registered axiom verifiers.
        
        Args:
            event: The agent event to verify.
            
        Returns:
            VerificationResult with status and axiom results.
        """
        axiom_results = []
        
        for verifier in self._verifiers:
            if verifier.applies_to(event):
                try:
                    result = verifier.verify(event)
                    axiom_results.append(result)
                    
                    if not result.passed:
                        logger.warning(
                            f"Axiom {result.axiom.value} violation: {result.reason} "
                            f"(event: {event.event_id}, agent: {event.agent.id})"
                        )
                except Exception as e:
                    logger.error(f"Verifier {verifier.name} error: {e}")
                    # Create error result
                    axiom_results.append(AxiomResult(
                        axiom=verifier.axiom,
                        passed=False,
                        reason=f"Verification error: {str(e)}",
                        confidence=0.0,
                    ))
        
        # Determine overall status
        has_violations = any(not r.passed for r in axiom_results)
        escalated = False
        
        if has_violations:
            # Track violation
            self._record_violation(event.agent.id)
            
            # Check escalation threshold
            if self._should_escalate(event.agent.id):
                escalated = True
                logger.error(
                    f"Escalation threshold reached for agent {event.agent.id}"
                )
        
        status = VerificationStatus.ESCALATED if escalated else (
            VerificationStatus.VIOLATION if has_violations 
            else VerificationStatus.VERIFIED
        )
        
        result = VerificationResult(
            event_id=event.event_id,
            status=status,
            axiom_results=axiom_results,
            escalated=escalated,
        )
        
        # Call violation handlers
        if has_violations:
            for handler in self._violation_handlers:
                try:
                    handler(event, result)
                except Exception as e:
                    logger.error(f"Violation handler error: {e}")
        
        return result
    
    def verify_batch(self, events: List[AgentEvent]) -> List[VerificationResult]:
        """
        Verify multiple events.
        
        Args:
            events: List of events to verify.
            
        Returns:
            List of verification results.
        """
        return [self.verify(event) for event in events]
    
    def _record_violation(self, agent_id: str) -> None:
        """Record a violation for tracking."""
        if agent_id not in self._violation_history:
            self._violation_history[agent_id] = []
        self._violation_history[agent_id].append(datetime.now(timezone.utc))
    
    def _should_escalate(self, agent_id: str) -> bool:
        """Check if agent has exceeded escalation threshold."""
        if agent_id not in self._violation_history:
            return False
        
        now = datetime.now(timezone.utc)
        cutoff = now - self.escalation_window
        recent_violations = [
            v for v in self._violation_history[agent_id]
            if v > cutoff
        ]
        
        return len(recent_violations) >= self.escalation_threshold
    
    def get_violation_count(
        self,
        agent_id: str,
        window: Optional[timedelta] = None
    ) -> int:
        """
        Get violation count for an agent.
        
        Args:
            agent_id: The agent ID.
            window: Optional time window (defaults to escalation_window).
            
        Returns:
            Number of violations in the window.
        """
        if agent_id not in self._violation_history:
            return 0
        
        window = window or self.escalation_window
        now = datetime.now(timezone.utc)
        cutoff = now - window
        
        return len([
            v for v in self._violation_history[agent_id]
            if v > cutoff
        ])
    
    def clear_violation_history(self, agent_id: Optional[str] = None) -> None:
        """
        Clear violation history.
        
        Args:
            agent_id: Optional agent ID. If None, clears all.
        """
        if agent_id:
            self._violation_history.pop(agent_id, None)
        else:
            self._violation_history.clear()
    
    def get_reputation_impact(self, agent_id: str) -> float:
        """
        Calculate reputation impact from violations.
        
        Returns negative value representing reputation penalty.
        
        Args:
            agent_id: The agent ID.
            
        Returns:
            Reputation adjustment (negative for violations).
        """
        violation_count = self.get_violation_count(agent_id)
        # -5 points per violation
        return -5.0 * violation_count


def create_default_monitor(
    escalation_threshold: int = 3,
    escalation_window: timedelta = timedelta(hours=24),
) -> AxiomComplianceMonitor:
    """
    Create monitor with default verifiers.
    
    Args:
        escalation_threshold: Violations before escalation.
        escalation_window: Time window for counting.
        
    Returns:
        Configured AxiomComplianceMonitor.
    """
    monitor = AxiomComplianceMonitor(
        escalation_threshold=escalation_threshold,
        escalation_window=escalation_window,
    )
    monitor.register_default_verifiers()
    
    # Add default logging handler
    def log_violation(event: AgentEvent, result: VerificationResult) -> None:
        violations = result.get_violations()
        logger.warning(
            f"[VIOLATION] Agent {event.agent.id} violated axioms: "
            f"{[v.axiom.value for v in violations]} - {event.action.description}"
        )
    
    monitor.register_violation_handler(log_violation)
    
    return monitor
