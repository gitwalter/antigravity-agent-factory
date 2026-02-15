"""
A5 Memory Verifier

Verifies memory operations respect consent requirements.
Checks for user consent and layer immutability.
"""

from lib.society.events.schema import AgentEvent, ActionType
from lib.society.verification.verifiers.base import AxiomVerifier, AxiomId, AxiomResult


class A5MemoryVerifier(AxiomVerifier):
    """
    Verifies memory operations respect consent (A5: Memory).

    Memory System Rules:
    - Semantic memories require explicit user consent
    - Layer 0-2 (Axioms, Purpose, Principles) are immutable
    - Layer 3-4 (Methodology, Technical) are configurable

    Checks for:
    - User consent for semantic memory creation
    - Layer immutability protection
    - Proper memory classification
    """

    # Immutable layers (cannot be modified)
    IMMUTABLE_LAYERS = [0, 1, 2]  # Axioms, Purpose, Principles

    # Memory types requiring consent
    CONSENT_REQUIRED_TYPES = ["semantic", "permanent", "learned"]

    @property
    def axiom(self) -> AxiomId:
        return AxiomId.A5_MEMORY

    @property
    def description(self) -> str:
        return "Verifies memory operations respect consent requirements"

    def applies_to(self, event: AgentEvent) -> bool:
        """Only apply to memory-related actions."""
        memory_actions = [
            ActionType.STATE_CHANGE,
        ]

        if event.action.type in memory_actions:
            return True

        # Check if payload mentions memory
        payload = event.action.payload
        if "memory" in str(payload).lower():
            return True
        if "layer" in payload:
            return True

        description = event.action.description.lower()
        return "memory" in description or "layer" in description

    def verify(self, event: AgentEvent) -> AxiomResult:
        """Check if memory operation respects consent requirements."""
        payload = event.action.payload

        # Check for layer modification
        target_layer = payload.get("target_layer")
        if target_layer is not None:
            if target_layer in self.IMMUTABLE_LAYERS:
                return self._make_fail(
                    reason=f"Attempt to modify immutable layer {target_layer}",
                    confidence=1.0,  # This is definitive
                    pattern="layer_violation",
                    target_layer=target_layer,
                )

        # Check for semantic memory creation
        memory_type = payload.get("memory_type", "")
        if memory_type in self.CONSENT_REQUIRED_TYPES:
            if not self._has_user_consent(event):
                return self._make_fail(
                    reason=f"Creating {memory_type} memory without user consent",
                    confidence=0.9,
                    pattern="consent_missing",
                    memory_type=memory_type,
                )

        # Check for memory-related keywords without consent
        description = event.action.description.lower()
        if self._creates_memory(description) and not self._has_user_consent(event):
            return self._make_fail(
                reason="Memory creation detected without consent confirmation",
                confidence=0.7,
                pattern="possible_consent_missing",
            )

        return self._make_pass(
            reason="Memory operation respects consent requirements",
            confidence=0.8,
        )

    def _has_user_consent(self, event: AgentEvent) -> bool:
        """Check if user consent was obtained."""
        payload = event.action.payload

        # Check explicit consent flags
        if payload.get("user_consented", False):
            return True
        if payload.get("consent_obtained", False):
            return True
        if payload.get("user_approved", False):
            return True

        # Check for ephemeral memory (doesn't need consent)
        if payload.get("memory_type") == "ephemeral":
            return True
        if payload.get("memory_type") == "working":
            return True

        # Check description
        description = event.action.description.lower()
        consent_phrases = [
            "with consent",
            "user approved",
            "user consented",
            "with permission",
        ]
        return any(phrase in description for phrase in consent_phrases)

    def _creates_memory(self, description: str) -> bool:
        """Check if action creates persistent memory."""
        memory_creation_phrases = [
            "store memory",
            "save memory",
            "create memory",
            "persist",
            "remember",
            "learn from",
            "store preference",
        ]
        return any(phrase in description for phrase in memory_creation_phrases)
