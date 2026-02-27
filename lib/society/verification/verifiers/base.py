"""
Base Axiom Verifier

Abstract base class for all axiom verifiers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from lib.society.events.schema import AgentEvent


class AxiomId(Enum):
    """Foundational axioms of the Antigravity Agent Factory."""

    A0_SDG = "A0"  # Sustainable Development Goals
    A1_LOVE = "A1"  # Love - prioritize user wellbeing
    A2_TRUTH = "A2"  # Truth - honesty and transparency
    A3_BEAUTY = "A3"  # Beauty - simplicity and elegance
    A4_GUARDIAN = "A4"  # Guardian protocol
    A5_MEMORY = "A5"  # Memory consent requirements


@dataclass
class AxiomResult:
    """
    Result of a single axiom verification.

    Attributes:
        axiom: The axiom that was checked.
        passed: Whether the action passed verification.
        reason: Explanation of the result.
        confidence: Confidence score (0.0 to 1.0).
        details: Additional details about the verification.
    """

    axiom: AxiomId
    passed: bool
    reason: str = ""
    confidence: float = 1.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "axiom": self.axiom.value,
            "passed": self.passed,
            "reason": self.reason,
            "confidence": self.confidence,
            "details": self.details,
        }


class AxiomVerifier(ABC):
    """
    Abstract base class for axiom verifiers.

    Each axiom (A0-A5) has its own verifier implementation
    that checks agent events for compliance.

    Subclasses must implement:
    - axiom property: Returns the AxiomId being verified
    - verify method: Checks an event and returns AxiomResult

    Optionally override:
    - applies_to: Filter which events to check
    """

    @property
    @abstractmethod
    def axiom(self) -> AxiomId:
        """The axiom this verifier checks."""
        pass

    @property
    def name(self) -> str:
        """Human-readable name for this verifier."""
        return f"{self.axiom.value} Verifier"

    @property
    def description(self) -> str:
        """Description of what this verifier checks."""
        return f"Verifies compliance with {self.axiom.name}"

    @abstractmethod
    def verify(self, event: AgentEvent) -> AxiomResult:
        """
        Verify an event against this axiom.

        Args:
            event: The agent event to verify.

        Returns:
            AxiomResult indicating pass/fail with explanation.
        """
        pass

    def applies_to(self, event: AgentEvent) -> bool:
        """
        Check if this verifier applies to the given event.

        Override this to skip verification for certain event types.

        Args:
            event: The event to check.

        Returns:
            True if this verifier should check the event.
        """
        return True

    def _check_keywords(
        self, text: str, keywords: List[str], case_sensitive: bool = False
    ) -> List[str]:
        """
        Helper to check for keywords in text.

        Args:
            text: The text to search.
            keywords: Keywords to look for.
            case_sensitive: Whether matching is case-sensitive.

        Returns:
            List of matched keywords.
        """
        if not case_sensitive:
            text = text.lower()
            keywords = [k.lower() for k in keywords]

        return [k for k in keywords if k in text]

    def _make_pass(
        self, reason: str = "", confidence: float = 1.0, **details
    ) -> AxiomResult:
        """Helper to create a passing result."""
        return AxiomResult(
            axiom=self.axiom,
            passed=True,
            reason=reason or f"Action complies with {self.axiom.name}",
            confidence=confidence,
            details=details,
        )

    def _make_fail(
        self, reason: str, confidence: float = 1.0, **details
    ) -> AxiomResult:
        """Helper to create a failing result."""
        return AxiomResult(
            axiom=self.axiom,
            passed=False,
            reason=reason,
            confidence=confidence,
            details=details,
        )
