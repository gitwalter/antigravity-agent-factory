"""
A0 SDG Verifier

Verifies actions support Sustainable Development Goals.
Checks for resource efficiency, environmental impact, and long-term sustainability.
"""

from lib.society.events.schema import AgentEvent
from lib.society.verification.verifiers.base import AxiomVerifier, AxiomId, AxiomResult


class A0SDGVerifier(AxiomVerifier):
    """
    Verifies actions support sustainable development (A0: SDG).

    Checks for:
    - Resource efficiency (computational, memory, energy)
    - Environmental impact awareness
    - Long-term sustainability considerations
    - Avoidance of wasteful patterns
    """

    # Keywords indicating potential resource waste
    WASTE_KEYWORDS = [
        "infinite loop",
        "memory leak",
        "unbounded",
        "excessive",
        "redundant",
        "duplicate",
        "wasteful",
        "inefficient",
    ]

    # Keywords indicating sustainability concerns
    SUSTAINABILITY_KEYWORDS = [
        "deprecated",
        "obsolete",
        "legacy",
        "technical debt",
        "short-term hack",
        "temporary workaround",
    ]

    @property
    def axiom(self) -> AxiomId:
        return AxiomId.A0_SDG

    @property
    def description(self) -> str:
        return "Verifies actions support sustainable development"

    def verify(self, event: AgentEvent) -> AxiomResult:
        """Check if action supports sustainable development."""
        description = event.action.description.lower()
        payload_str = str(event.action.payload).lower()
        combined_text = f"{description} {payload_str}"

        # Check for resource waste indicators
        waste_matches = self._check_keywords(combined_text, self.WASTE_KEYWORDS)
        if waste_matches:
            return self._make_fail(
                reason=f"Action may waste resources: {', '.join(waste_matches)}",
                confidence=0.7,
                matched_keywords=waste_matches,
                pattern="resource_waste",
            )

        # Check for sustainability concerns
        sustainability_matches = self._check_keywords(
            combined_text, self.SUSTAINABILITY_KEYWORDS
        )
        if sustainability_matches:
            return self._make_fail(
                reason=f"Action may harm long-term sustainability: {', '.join(sustainability_matches)}",
                confidence=0.6,
                matched_keywords=sustainability_matches,
                pattern="sustainability_concern",
            )

        # Check payload for resource-intensive operations
        payload = event.action.payload
        if self._is_resource_intensive(payload):
            # COORDINATORS and GUARDIANS can run intensive tasks with justification
            from lib.society.events.schema import AgentType

            is_privileged = event.agent.type in [
                AgentType.COORDINATOR,
                AgentType.GUARDIAN,
            ]

            if is_privileged and event.axiom_context.justification:
                pass
            else:
                return self._make_fail(
                    reason="Action appears resource-intensive without justification",
                    confidence=0.5,
                    pattern="resource_intensive",
                )

        return self._make_pass(
            reason="Action appears sustainable",
            confidence=0.8,
        )

    def _is_resource_intensive(self, payload: dict) -> bool:
        """Check if payload indicates resource-intensive operation."""
        # Check for large batch sizes without limits
        if "batch_size" in payload:
            batch_size = payload.get("batch_size", 0)
            if isinstance(batch_size, int) and batch_size > 10000:
                return True

        # Check for unlimited iterations
        if payload.get("iterations") == -1 or payload.get("limit") == -1:
            return True

        # Check for no timeout
        if payload.get("timeout") == 0 or payload.get("timeout") == -1:
            return True

        return False
