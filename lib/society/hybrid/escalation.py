"""
Escalation System

Handles violation escalation and resolution for agent societies.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class EscalationLevel(Enum):
    """Escalation severity levels."""

    INFO = 1
    WARNING = 2
    VIOLATION = 3
    CRITICAL = 4
    EMERGENCY = 5


class EscalationStatus(Enum):
    """Status of an escalation."""

    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    DISMISSED = "dismissed"


@dataclass
class Escalation:
    """
    Represents an escalation event.

    Attributes:
        id: Unique escalation identifier.
        level: Severity level.
        source: Source of the escalation (agent/system).
        subject: Subject of the escalation (agent/event/contract).
        reason: Description of the issue.
        evidence: Supporting evidence.
        created: When escalation was created.
        status: Current status.
        assignee: Handler assigned to resolve.
        resolution: Resolution notes if resolved.
    """

    id: str
    level: EscalationLevel
    source: str
    subject: str
    reason: str
    evidence: List[str] = field(default_factory=list)
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: EscalationStatus = EscalationStatus.OPEN
    assignee: Optional[str] = None
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None

    @property
    def is_open(self) -> bool:
        """Check if escalation is still open."""
        return self.status in [
            EscalationStatus.OPEN,
            EscalationStatus.ACKNOWLEDGED,
            EscalationStatus.INVESTIGATING,
        ]

    @property
    def age(self) -> timedelta:
        """Get age of escalation."""
        return datetime.now(timezone.utc) - self.created

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "id": self.id,
            "level": self.level.value,
            "level_name": self.level.name,
            "source": self.source,
            "subject": self.subject,
            "reason": self.reason,
            "evidence": self.evidence,
            "created": self.created.isoformat(),
            "status": self.status.value,
            "assignee": self.assignee,
            "resolution": self.resolution,
        }
        if self.resolved_at:
            result["resolved_at"] = self.resolved_at.isoformat()
        return result


EscalationHandler = Callable[[Escalation], None]


class EscalationPolicy(ABC):
    """
    Abstract base class for escalation policies.

    Defines how escalations are routed and handled.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Policy name."""
        pass

    @abstractmethod
    def should_escalate(self, escalation: Escalation) -> bool:
        """Determine if escalation should be auto-escalated."""
        pass

    @abstractmethod
    def get_handler(self, escalation: Escalation) -> Optional[str]:
        """Get the appropriate handler for an escalation."""
        pass

    @abstractmethod
    def get_timeout(self, escalation: Escalation) -> timedelta:
        """Get timeout before auto-escalation."""
        pass


class DefaultPolicy(EscalationPolicy):
    """
    Default escalation policy.

    - INFO/WARNING: 24h timeout, any handler
    - VIOLATION: 4h timeout, senior handler
    - CRITICAL: 1h timeout, admin handler
    - EMERGENCY: 15min timeout, all admins notified
    """

    def __init__(
        self, handlers: Optional[List[str]] = None, admins: Optional[List[str]] = None
    ):
        """
        Initialize policy.

        Args:
            handlers: List of regular handlers.
            admins: List of admin handlers.
        """
        self._handlers = handlers or []
        self._admins = admins or []

    @property
    def name(self) -> str:
        return "default"

    def add_handler(self, handler_id: str, is_admin: bool = False) -> None:
        """Add a handler."""
        if is_admin:
            self._admins.append(handler_id)
        else:
            self._handlers.append(handler_id)

    def should_escalate(self, escalation: Escalation) -> bool:
        """Check if escalation has timed out."""
        timeout = self.get_timeout(escalation)
        return escalation.age > timeout and escalation.is_open

    def get_handler(self, escalation: Escalation) -> Optional[str]:
        """Get appropriate handler based on level."""
        if escalation.level.value >= EscalationLevel.CRITICAL.value:
            # Admin required
            return self._admins[0] if self._admins else None
        elif escalation.level.value >= EscalationLevel.VIOLATION.value:
            # Prefer admin, fallback to handler
            return (
                self._admins[0]
                if self._admins
                else (self._handlers[0] if self._handlers else None)
            )
        else:
            # Any handler
            return self._handlers[0] if self._handlers else None

    def get_timeout(self, escalation: Escalation) -> timedelta:
        """Get timeout based on level."""
        timeouts = {
            EscalationLevel.INFO: timedelta(hours=24),
            EscalationLevel.WARNING: timedelta(hours=24),
            EscalationLevel.VIOLATION: timedelta(hours=4),
            EscalationLevel.CRITICAL: timedelta(hours=1),
            EscalationLevel.EMERGENCY: timedelta(minutes=15),
        }
        return timeouts.get(escalation.level, timedelta(hours=4))


class EscalationManager:
    """
    Manages escalations within an agent society.

    Features:
    - Create and track escalations
    - Route to appropriate handlers
    - Auto-escalate based on policy
    - Resolution tracking

    Usage:
        manager = EscalationManager()
        manager.set_policy(DefaultPolicy(handlers=["handler-1"]))

        # Create escalation
        escalation = manager.create_escalation(
            level=EscalationLevel.VIOLATION,
            source="axiom-monitor",
            subject="agent-123",
            reason="A1 axiom violation detected"
        )

        # Acknowledge
        manager.acknowledge(escalation.id, "handler-1")

        # Resolve
        manager.resolve(escalation.id, "Action was valid, false positive")

    Axiom alignment:
    - A4 Guardian: Systematic harm prevention
    - A2 Truth: Transparent issue tracking
    """

    def __init__(self, policy: Optional[EscalationPolicy] = None):
        """
        Initialize escalation manager.

        Args:
            policy: Escalation routing policy.
        """
        self.policy = policy or DefaultPolicy()
        self._escalations: Dict[str, Escalation] = {}
        self._handlers: Dict[EscalationLevel, List[EscalationHandler]] = {}
        self._notification_handlers: List[Callable[[Escalation], None]] = []

    def set_policy(self, policy: EscalationPolicy) -> None:
        """Set the escalation policy."""
        self.policy = policy

    def register_handler(
        self, level: EscalationLevel, handler: EscalationHandler
    ) -> None:
        """Register a handler for a level."""
        if level not in self._handlers:
            self._handlers[level] = []
        self._handlers[level].append(handler)

    def add_notification_handler(self, handler: Callable[[Escalation], None]) -> None:
        """Add a notification handler for new escalations."""
        self._notification_handlers.append(handler)

    def create_escalation(
        self,
        level: EscalationLevel,
        source: str,
        subject: str,
        reason: str,
        evidence: Optional[List[str]] = None,
    ) -> Escalation:
        """
        Create a new escalation.

        Args:
            level: Severity level.
            source: Source of the escalation.
            subject: Subject being escalated.
            reason: Description of the issue.
            evidence: Supporting evidence.

        Returns:
            Created Escalation.
        """
        escalation_id = f"esc-{len(self._escalations) + 1}"

        escalation = Escalation(
            id=escalation_id,
            level=level,
            source=source,
            subject=subject,
            reason=reason,
            evidence=evidence or [],
        )

        self._escalations[escalation_id] = escalation

        # Auto-assign handler
        handler = self.policy.get_handler(escalation)
        if handler:
            escalation.assignee = handler

        # Trigger notification handlers
        for handler in self._notification_handlers:
            try:
                handler(escalation)
            except Exception as e:
                logger.error(f"Notification handler error: {e}")

        # Trigger level handlers
        level_handlers = self._handlers.get(level, [])
        for h in level_handlers:
            try:
                h(escalation)
            except Exception as e:
                logger.error(f"Level handler error: {e}")

        logger.info(
            f"Escalation created: {escalation_id} [{level.name}] {subject}: {reason}"
        )

        return escalation

    def get(self, escalation_id: str) -> Optional[Escalation]:
        """Get an escalation by ID."""
        return self._escalations.get(escalation_id)

    def acknowledge(self, escalation_id: str, handler_id: str) -> bool:
        """
        Acknowledge an escalation.

        Args:
            escalation_id: The escalation to acknowledge.
            handler_id: The handler acknowledging.

        Returns:
            True if successful.
        """
        escalation = self.get(escalation_id)
        if not escalation or escalation.status != EscalationStatus.OPEN:
            return False

        escalation.status = EscalationStatus.ACKNOWLEDGED
        escalation.assignee = handler_id

        logger.info(f"Escalation {escalation_id} acknowledged by {handler_id}")
        return True

    def start_investigation(self, escalation_id: str) -> bool:
        """Mark escalation as under investigation."""
        escalation = self.get(escalation_id)
        if not escalation or not escalation.is_open:
            return False

        escalation.status = EscalationStatus.INVESTIGATING
        logger.info(f"Escalation {escalation_id} under investigation")
        return True

    def resolve(
        self, escalation_id: str, resolution: str, resolver_id: Optional[str] = None
    ) -> bool:
        """
        Resolve an escalation.

        Args:
            escalation_id: The escalation to resolve.
            resolution: Resolution description.
            resolver_id: Optional resolver ID.

        Returns:
            True if successful.
        """
        escalation = self.get(escalation_id)
        if not escalation or not escalation.is_open:
            return False

        escalation.status = EscalationStatus.RESOLVED
        escalation.resolution = resolution
        escalation.resolved_at = datetime.now(timezone.utc)

        if resolver_id:
            escalation.assignee = resolver_id

        logger.info(f"Escalation {escalation_id} resolved: {resolution}")
        return True

    def dismiss(self, escalation_id: str, reason: str) -> bool:
        """
        Dismiss an escalation as invalid.

        Args:
            escalation_id: The escalation to dismiss.
            reason: Reason for dismissal.

        Returns:
            True if successful.
        """
        escalation = self.get(escalation_id)
        if not escalation or not escalation.is_open:
            return False

        escalation.status = EscalationStatus.DISMISSED
        escalation.resolution = f"Dismissed: {reason}"
        escalation.resolved_at = datetime.now(timezone.utc)

        logger.info(f"Escalation {escalation_id} dismissed: {reason}")
        return True

    def escalate_further(self, escalation_id: str) -> bool:
        """
        Escalate to higher level.

        Args:
            escalation_id: The escalation to escalate.

        Returns:
            True if successful.
        """
        escalation = self.get(escalation_id)
        if not escalation or not escalation.is_open:
            return False

        # Increase level if possible
        if escalation.level.value < EscalationLevel.EMERGENCY.value:
            new_level = EscalationLevel(escalation.level.value + 1)
            escalation.level = new_level
            escalation.status = EscalationStatus.ESCALATED

            # Get new handler
            handler = self.policy.get_handler(escalation)
            if handler:
                escalation.assignee = handler

            logger.warning(f"Escalation {escalation_id} escalated to {new_level.name}")
            return True

        return False

    def check_timeouts(self) -> List[str]:
        """
        Check for timed-out escalations and auto-escalate.

        Returns:
            List of escalation IDs that were auto-escalated.
        """
        auto_escalated = []

        for escalation in self._escalations.values():
            if escalation.is_open and self.policy.should_escalate(escalation):
                if self.escalate_further(escalation.id):
                    auto_escalated.append(escalation.id)

        return auto_escalated

    def get_open_escalations(
        self, level: Optional[EscalationLevel] = None, assignee: Optional[str] = None
    ) -> List[Escalation]:
        """
        Get open escalations with optional filters.

        Args:
            level: Optional level filter.
            assignee: Optional assignee filter.

        Returns:
            List of matching escalations.
        """
        escalations = [e for e in self._escalations.values() if e.is_open]

        if level:
            escalations = [e for e in escalations if e.level == level]

        if assignee:
            escalations = [e for e in escalations if e.assignee == assignee]

        return sorted(
            escalations, key=lambda e: (e.level.value, e.created), reverse=True
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get escalation statistics."""
        all_escalations = list(self._escalations.values())

        by_level = {}
        for level in EscalationLevel:
            by_level[level.name] = len([e for e in all_escalations if e.level == level])

        by_status = {}
        for status in EscalationStatus:
            by_status[status.value] = len(
                [e for e in all_escalations if e.status == status]
            )

        open_escalations = [e for e in all_escalations if e.is_open]
        resolved = [e for e in all_escalations if e.status == EscalationStatus.RESOLVED]

        avg_resolution_time = None
        if resolved:
            total_time = sum(
                (e.resolved_at - e.created).total_seconds()
                for e in resolved
                if e.resolved_at
            )
            avg_resolution_time = total_time / len(resolved)

        return {
            "total": len(all_escalations),
            "open": len(open_escalations),
            "by_level": by_level,
            "by_status": by_status,
            "avg_resolution_seconds": avg_resolution_time,
        }

    def export(self) -> Dict[str, Any]:
        """Export escalation data."""
        return {
            "escalations": [e.to_dict() for e in self._escalations.values()],
            "statistics": self.get_statistics(),
        }


def create_escalation_from_violation(
    violation_result: Any, manager: EscalationManager
) -> Escalation:
    """
    Create an escalation from a verification violation.

    Args:
        violation_result: The violation result (from HybridVerificationResult).
        manager: The escalation manager.

    Returns:
        Created Escalation.
    """
    # Determine level based on violation type
    level = EscalationLevel.VIOLATION

    if hasattr(violation_result, "axiom_result"):
        axiom_result = violation_result.axiom_result
        if axiom_result and not axiom_result.passed:
            # Check for critical axioms
            for result in axiom_result.results:
                if not result.passed:
                    if result.axiom_id.value in ["A4", "A0"]:  # Guardian and SDG
                        level = EscalationLevel.CRITICAL
                        break

    return manager.create_escalation(
        level=level,
        source="verification-system",
        subject=violation_result.event.agent.id
        if hasattr(violation_result, "event")
        else "unknown",
        reason="Verification violation detected",
        evidence=[
            str(violation_result.to_dict())
            if hasattr(violation_result, "to_dict")
            else str(violation_result)
        ],
    )
