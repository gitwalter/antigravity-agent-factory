"""
A4 Guardian Verifier

Verifies actions follow the Guardian protocol.
Checks for harm prevention, proper escalation, and user notification.
"""

from lib.society.events.schema import AgentEvent
from lib.society.verification.verifiers.base import AxiomVerifier, AxiomId, AxiomResult


class A4GuardianVerifier(AxiomVerifier):
    """
    Verifies actions follow Guardian protocol (A4: Guardian).

    Guardian Protocol (Wu Wei Levels):
    - Level 0 (Flow): Natural alignment, no intervention
    - Level 1 (Nudge): Subtle self-correction
    - Level 2 (Pause): Pause, explain concern, ask user
    - Level 3 (Block): Stop action, explain with alternatives
    - Level 4 (Protect): Prevent harm immediately, then explain

    Checks for:
    - Harmful actions are prevented
    - Proper escalation for sensitive operations
    - User notification at appropriate levels
    - Alternatives offered when blocking
    """

    # Keywords indicating potentially harmful actions
    HARM_KEYWORDS = [
        "delete",
        "destroy",
        "corrupt",
        "damage",
        "harm",
        "break",
        "remove permanently",
        "drop database",
        "rm -rf",
        "format",
        "wipe",
    ]

    # Keywords indicating proper escalation
    ESCALATION_KEYWORDS = [
        "escalate",
        "notify",
        "alert",
        "warn",
        "confirm",
        "verify with user",
        "ask permission",
    ]

    # Keywords indicating sensitive operations
    SENSITIVE_KEYWORDS = [
        "sensitive",
        "critical",
        "irreversible",
        "production",
        "credential",
        "secret",
        "private",
        "personal data",
    ]

    @property
    def axiom(self) -> AxiomId:
        return AxiomId.A4_GUARDIAN

    @property
    def description(self) -> str:
        return "Verifies actions follow Guardian protocol"

    def verify(self, event: AgentEvent) -> AxiomResult:
        """Check if action follows Guardian protocol."""
        description = event.action.description.lower()
        justification = event.axiom_context.justification.lower()
        payload_str = str(event.action.payload).lower()
        combined_text = f"{description} {justification} {payload_str}"

        # Check for harmful actions
        harm_matches = self._check_keywords(combined_text, self.HARM_KEYWORDS)
        if harm_matches:
            # Harmful action should be escalated
            escalation_matches = self._check_keywords(
                combined_text, self.ESCALATION_KEYWORDS
            )
            if not escalation_matches:
                return self._make_fail(
                    reason=f"Potentially harmful action without escalation: {', '.join(harm_matches)}",
                    confidence=0.8,
                    matched_keywords=harm_matches,
                    pattern="harm_not_escalated",
                )

        # Check for sensitive operations
        sensitive_matches = self._check_keywords(combined_text, self.SENSITIVE_KEYWORDS)
        if sensitive_matches:
            # Coordinators and Guardians are permitted sensitive operations with justification
            from lib.society.events.schema import AgentType

            is_privileged = event.agent.type in [
                AgentType.COORDINATOR,
                AgentType.GUARDIAN,
            ]

            if is_privileged and justification:
                # Privileged agents can perform sensitive operations if they provide justification
                pass
            elif not self._has_proper_escalation(event):
                return self._make_fail(
                    reason=f"Sensitive operation without proper escalation: {', '.join(sensitive_matches)}",
                    confidence=0.7,
                    matched_keywords=sensitive_matches,
                    pattern="sensitive_not_escalated",
                )

        # Check intervention level
        intervention_level = event.action.payload.get("intervention_level", 0)
        if intervention_level >= 2:  # Pause or higher
            if not self._user_notified(event):
                return self._make_fail(
                    reason="Intervention at Pause level or higher without user notification",
                    confidence=0.8,
                    pattern="no_notification",
                    intervention_level=intervention_level,
                )

        # Check for blocked actions without alternatives
        if event.action.payload.get("blocked", False):
            if not event.action.payload.get("alternatives"):
                return self._make_fail(
                    reason="Action blocked without providing alternatives",
                    confidence=0.6,
                    pattern="no_alternatives",
                )

        return self._make_pass(
            reason="Action follows Guardian protocol",
            confidence=0.8,
        )

    def _has_proper_escalation(self, event: AgentEvent) -> bool:
        """Check if event has proper escalation markers."""
        payload = event.action.payload

        # Check for escalation flags
        if payload.get("escalated", False):
            return True
        if payload.get("user_confirmed", False):
            return True
        if payload.get("supervisor_approved", False):
            return True

        # Check description for escalation
        description = event.action.description.lower()
        return any(kw in description for kw in self.ESCALATION_KEYWORDS)

    def _user_notified(self, event: AgentEvent) -> bool:
        """Check if user was notified."""
        payload = event.action.payload

        if payload.get("user_notified", False):
            return True
        if payload.get("notification_sent", False):
            return True

        description = event.action.description.lower()
        return "notify" in description or "informed user" in description
