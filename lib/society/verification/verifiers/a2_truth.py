"""
A2 Truth Verifier

Verifies actions are honest and transparent.
Checks for deception, hidden effects, and truthful communication.
"""

from lib.society.events.schema import AgentEvent
from lib.society.verification.verifiers.base import AxiomVerifier, AxiomId, AxiomResult


class A2TruthVerifier(AxiomVerifier):
    """
    Verifies actions are honest and transparent (A2: Truth).

    Checks for:
    - Absence of deceptive patterns
    - No hidden side effects
    - Truthful communication
    - Transparency in operations
    """

    # Keywords indicating deception
    DECEPTION_KEYWORDS = [
        "hide",
        "conceal",
        "mislead",
        "false",
        "fake",
        "pretend",
        "disguise",
        "obfuscate",
        "deceive",
        "lie",
        "fabricate",
    ]

    # Keywords indicating hidden behavior
    HIDDEN_KEYWORDS = [
        "secretly",
        "silently",
        "without telling",
        "without informing",
        "hidden",
        "undisclosed",
        "covert",
        "stealth",
    ]

    @property
    def axiom(self) -> AxiomId:
        return AxiomId.A2_TRUTH

    @property
    def description(self) -> str:
        return "Verifies actions are honest and transparent"

    def verify(self, event: AgentEvent) -> AxiomResult:
        """Check if action is honest and transparent."""
        description = event.action.description.lower()
        justification = event.axiom_context.justification.lower()
        payload_str = str(event.action.payload).lower()
        combined_text = f"{description} {justification} {payload_str}"

        # Check for deception patterns
        deception_matches = self._check_keywords(combined_text, self.DECEPTION_KEYWORDS)
        if deception_matches:
            return self._make_fail(
                reason=f"Action may contain deception: {', '.join(deception_matches)}",
                confidence=0.8,
                matched_keywords=deception_matches,
                pattern="deception",
            )

        # Check for hidden behavior
        hidden_matches = self._check_keywords(combined_text, self.HIDDEN_KEYWORDS)
        if hidden_matches:
            return self._make_fail(
                reason=f"Action may have hidden effects: {', '.join(hidden_matches)}",
                confidence=0.7,
                matched_keywords=hidden_matches,
                pattern="hidden_effects",
            )

        # Check for external effects without disclosure
        if self._has_undisclosed_effects(event):
            # COORDINATORS and GUARDIANS can have undisclosed effects if justified for system integrity
            from lib.society.events.schema import AgentType

            is_privileged = event.agent.type in [
                AgentType.COORDINATOR,
                AgentType.GUARDIAN,
            ]

            if is_privileged and justification:
                pass
            else:
                return self._make_fail(
                    reason="Action has external effects not mentioned in description",
                    confidence=0.6,
                    pattern="undisclosed_effects",
                )

        return self._make_pass(
            reason="Action appears honest and transparent",
            confidence=0.8,
        )

    def _has_undisclosed_effects(self, event: AgentEvent) -> bool:
        """Check for undisclosed side effects."""
        # External effect actions should mention what they affect
        if event.action.type.value == "external_effect":
            description = event.action.description.lower()
            if "effect" not in description and "change" not in description:
                return True

        # State changes should be explicit
        if event.action.type.value == "state_change":
            payload = event.action.payload
            if payload.get("silent", False):
                return True

        return False
