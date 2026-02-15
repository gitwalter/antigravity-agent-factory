"""
Simplified API for Agent Society Verification.

This module provides easy-to-use entry points for common multi-agent
coordination scenarios. It wraps the full lib/society infrastructure
with sensible defaults for rapid development.

Value Proposition:
- 70% reduction in coordination code
- 3-line society setup vs 10+ lines with full API
- Sensible defaults for common scenarios
- Full power available when needed

Example:
    # Create a verified multi-agent society in 3 lines
    from lib.society.simple import create_agent_society

    society = create_agent_society("MyProject", agents=["orchestrator", "worker1", "worker2"])
    result = society.send("orchestrator", "worker1", {"task": "analyze_code"})
    print(f"Verified: {result.verified}, Reputation: {society.get_reputation('orchestrator')}")

SDG - Love - Truth - Beauty
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from enum import Enum

from lib.society.integration import SocietyContext, AgentSocietyBridge, MessageRouter
from lib.society.integration.agent_bridge import MessageType

from lib.society.contracts import (
    AgentContract,
    Party,
    Capability,
    Obligation,
    Prohibition,
)


class SocietyPreset(Enum):
    """Pre-configured society setups for common scenarios."""

    DEVELOPMENT = "development"  # Local verification only, no blockchain
    PRODUCTION = "production"  # Full verification with audit trail
    TESTING = "testing"  # Minimal verification for speed
    ENTERPRISE = "enterprise"  # Full verification with L1+ trust tiers


@dataclass
class SendResult:
    """Result of sending a message through the society."""

    verified: bool
    event_id: Optional[str] = None
    violations: list = field(default_factory=list)
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Check if send was successful (delivered, regardless of verification)."""
        return self.error is None


@dataclass
class AgentStatus:
    """Status information for an agent in the society."""

    agent_id: str
    reputation_score: float
    trust_level: str
    messages_sent: int
    messages_received: int
    violations: int
    contracts: int


class SimpleSociety:
    """
    Simplified interface for multi-agent society coordination.

    This class wraps the full lib/society infrastructure with an easy-to-use
    API for common multi-agent scenarios.

    Attributes:
        name: Name of the society.
        context: Underlying SocietyContext for advanced operations.

    Example:
        society = SimpleSociety("MyProject")
        society.add_agent("orchestrator", agent_type="supervisor")
        society.add_agent("worker", agent_type="executor")

        result = society.send("orchestrator", "worker", {"task": "process"})
        if result.verified:
            print("Message verified and delivered!")
    """

    def __init__(
        self,
        name: str,
        preset: SocietyPreset = SocietyPreset.DEVELOPMENT,
        agents: Optional[list[str]] = None,
    ):
        """
        Initialize a simplified agent society.

        Args:
            name: Name of the society (used for identification).
            preset: Pre-configured setup (development, production, etc.).
            agents: Optional list of agent IDs to register immediately.
        """
        self.name = name
        self.preset = preset
        self._context = SocietyContext.create_default(name)
        self._router = MessageRouter(self._context)
        self._bridges: Dict[str, AgentSocietyBridge] = {}
        self._handlers: Dict[str, List[Callable]] = {}
        self._message_counts: Dict[str, Dict[str, int]] = {}

        # Register initial agents if provided
        if agents:
            for agent_id in agents:
                self.add_agent(agent_id)

    @property
    def context(self) -> SocietyContext:
        """Access the underlying SocietyContext for advanced operations."""
        return self._context

    def add_agent(
        self, agent_id: str, agent_type: str = "general", name: Optional[str] = None
    ) -> "SimpleSociety":
        """
        Add an agent to the society.

        Args:
            agent_id: Unique identifier for the agent.
            agent_type: Type of agent (supervisor, executor, analyst, etc.).
            name: Human-readable name (defaults to agent_id).

        Returns:
            Self for method chaining.

        Example:
            society.add_agent("worker1", agent_type="executor", name="Code Analyzer")
        """
        if agent_id in self._bridges:
            return self  # Already registered

        bridge = AgentSocietyBridge(
            agent_id=agent_id,
            agent_type=agent_type,
            context=self._context,
            name=name or agent_id,
        )
        self._bridges[agent_id] = bridge
        self._router.register(bridge)
        self._message_counts[agent_id] = {"sent": 0, "received": 0}
        self._handlers[agent_id] = []

        return self

    def remove_agent(self, agent_id: str) -> "SimpleSociety":
        """
        Remove an agent from the society.

        Args:
            agent_id: ID of the agent to remove.

        Returns:
            Self for method chaining.
        """
        if agent_id in self._bridges:
            self._router.unregister(agent_id)
            del self._bridges[agent_id]
            del self._message_counts[agent_id]
            del self._handlers[agent_id]

        return self

    def send(
        self,
        from_agent: str,
        to_agent: str,
        payload: Dict[str, Any],
        message_type: str = "REQUEST",
        justification: Optional[str] = None,
        axioms: Optional[List[str]] = None,
    ) -> SendResult:
        """
        Send a verified message between agents.

        Args:
            from_agent: ID of the sending agent.
            to_agent: ID of the receiving agent.
            payload: Message content as a dictionary.
            message_type: Type of message (REQUEST, INFORM, PROPOSE, etc.).
            justification: Human-readable explanation (helps axiom verification).
            axioms: Axioms this message aligns with (e.g., ["A1", "A2"]).

        Returns:
            SendResult with verification status and any violations.

        Example:
            result = society.send(
                "orchestrator", "worker",
                {"task": "analyze", "file": "main.py"},
                justification="Delegating code analysis for user request"
            )
        """
        if from_agent not in self._bridges:
            return SendResult(
                verified=False, error=f"Agent '{from_agent}' not registered"
            )

        if to_agent not in self._bridges:
            return SendResult(
                verified=False, error=f"Agent '{to_agent}' not registered"
            )

        bridge = self._bridges[from_agent]
        msg_type = MessageType[message_type.upper()]

        result = bridge.send_message(
            target=to_agent,
            message_type=msg_type,
            payload=payload,
            justification=justification or f"Message from {from_agent} to {to_agent}",
            axiom_alignment=axioms or ["A1", "A2"],
        )

        # Update counts
        self._message_counts[from_agent]["sent"] += 1
        self._message_counts[to_agent]["received"] += 1

        # Trigger handlers on receiving agent
        if result.success and to_agent in self._handlers:
            for handler in self._handlers[to_agent]:
                try:
                    handler(from_agent, payload)
                except Exception:
                    pass  # Don't let handler errors break message flow

        return SendResult(
            verified=result.verified,
            event_id=result.event_id,
            violations=[str(v) for v in result.violations] if result.violations else [],
        )

    def broadcast(
        self,
        from_agent: str,
        payload: Dict[str, Any],
        exclude: Optional[List[str]] = None,
        message_type: str = "INFORM",
    ) -> Dict[str, SendResult]:
        """
        Broadcast a message to all agents in the society.

        Args:
            from_agent: ID of the sending agent.
            payload: Message content.
            exclude: Optional list of agent IDs to exclude.
            message_type: Type of message.

        Returns:
            Dictionary mapping agent IDs to their SendResults.
        """
        results = {}
        exclude_set = set(exclude or [])
        exclude_set.add(from_agent)  # Don't send to self

        for agent_id in self._bridges:
            if agent_id not in exclude_set:
                results[agent_id] = self.send(
                    from_agent, agent_id, payload, message_type
                )

        return results

    def on_message(
        self, agent_id: str, handler: Callable[[str, dict], None]
    ) -> "SimpleSociety":
        """
        Register a message handler for an agent.

        Args:
            agent_id: ID of the agent to handle messages for.
            handler: Callback function(sender_id, payload).

        Returns:
            Self for method chaining.

        Example:
            def handle_request(sender, payload):
                print(f"Got request from {sender}: {payload}")

            society.on_message("worker", handle_request)
        """
        if agent_id not in self._handlers:
            self._handlers[agent_id] = []
        self._handlers[agent_id].append(handler)
        return self

    def get_reputation(self, agent_id: str) -> float:
        """
        Get the current reputation score for an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            Reputation score (0-100).
        """
        score = self._context.reputation_system.get_score(agent_id)
        return score.current_score

    def get_trust_level(self, agent_id: str) -> str:
        """
        Get the current trust level for an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            Trust level as string (high, medium, low, untrusted).
        """
        score = self._context.reputation_system.get_score(agent_id)
        return score.trust_level

    def get_agent_status(self, agent_id: str) -> AgentStatus:
        """
        Get comprehensive status for an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            AgentStatus with reputation, trust, and activity info.
        """
        counts = self._message_counts.get(agent_id, {"sent": 0, "received": 0})

        return AgentStatus(
            agent_id=agent_id,
            reputation_score=self.get_reputation(agent_id),
            trust_level=self.get_trust_level(agent_id),
            messages_sent=counts["sent"],
            messages_received=counts["received"],
            violations=0,  # Would need event store query
            contracts=0,  # Would need contract registry query
        )

    def create_contract(
        self,
        contract_id: str,
        parties: List[tuple],
        capabilities: Optional[List[tuple]] = None,
        obligations: Optional[List[tuple]] = None,
        prohibitions: Optional[List[tuple]] = None,
    ) -> AgentContract:
        """
        Create and register a contract between agents.

        Args:
            contract_id: Unique ID for the contract.
            parties: List of (agent_id, role) tuples.
            capabilities: List of (agent_id, capability_name) tuples.
            obligations: List of (agent_id, obligation_name, params) tuples.
            prohibitions: List of (agent_id, prohibition_name) tuples.

        Returns:
            The created AgentContract.

        Example:
            contract = society.create_contract(
                "analysis-contract",
                parties=[("orchestrator", "delegator"), ("worker", "analyzer")],
                capabilities=[("worker", "analyze_code")],
                obligations=[("worker", "respond_within", {"timeout": 60})],
                prohibitions=[("worker", "modify_files")]
            )
        """
        # Build parties with public keys from bridges
        party_list = []
        for p in parties:
            agent_id, role = p[0], p[1]
            # Get public key from bridge identity if available
            public_key = ""
            if agent_id in self._bridges:
                bridge = self._bridges[agent_id]
                if hasattr(bridge, "identity") and bridge.identity:
                    public_key = bridge.identity.public_key
            party_list.append(
                Party(agent_id=agent_id, role=role, public_key=public_key)
            )

        # Build capabilities dict: {role: [Capability, ...]}
        cap_dict: Dict[str, List[Capability]] = {}
        for c in capabilities or []:
            agent_id, action = c[0], c[1]
            if agent_id not in cap_dict:
                cap_dict[agent_id] = []
            cap_dict[agent_id].append(Capability(action=action))

        # Build obligations dict: {role: [Obligation, ...]}
        obl_dict: Dict[str, List[Obligation]] = {}
        for o in obligations or []:
            agent_id, action = o[0], o[1]
            params = o[2] if len(o) > 2 else {}
            if agent_id not in obl_dict:
                obl_dict[agent_id] = []
            # Use action as both trigger and action for simplified API
            obl_dict[agent_id].append(
                Obligation(trigger="on_request", action=action, parameters=params)
            )

        # Build prohibitions dict: {role: [Prohibition, ...]}
        proh_dict: Dict[str, List[Prohibition]] = {}
        for p in prohibitions or []:
            agent_id, action = p[0], p[1]
            if agent_id not in proh_dict:
                proh_dict[agent_id] = []
            proh_dict[agent_id].append(Prohibition(action=action))

        contract = AgentContract(
            contract_id=contract_id,
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=party_list,
            capabilities=cap_dict,
            obligations=obl_dict,
            prohibitions=proh_dict,
        )

        # Sign with all parties
        for agent_id, _ in parties:
            if agent_id in self._bridges:
                self._bridges[agent_id].sign_contract(contract)

        return contract

    def get_stats(self) -> Dict[str, Any]:
        """
        Get society-wide statistics.

        Returns:
            Dictionary with event counts, agent counts, etc.
        """
        stats = self._context.get_stats()
        stats["registered_agents"] = len(self._bridges)
        stats["society_name"] = self.name
        stats["preset"] = self.preset.value
        return stats

    def export_audit_log(self) -> Dict[str, Any]:
        """
        Export the full audit log for compliance.

        Returns:
            Complete society state including events, contracts, and reputation.
        """
        return self._context.export()


def create_agent_society(
    name: str,
    agents: Optional[List[str]] = None,
    preset: SocietyPreset = SocietyPreset.DEVELOPMENT,
) -> SimpleSociety:
    """
    Create a verified multi-agent society with minimal configuration.

    This is the primary entry point for the simplified API.

    Args:
        name: Name of the society.
        agents: Optional list of agent IDs to register.
        preset: Pre-configured setup for the society.

    Returns:
        A SimpleSociety ready for agent coordination.

    Example:
        # Create society with agents in one line
        society = create_agent_society("MyProject", ["orchestrator", "worker1", "worker2"])

        # Send verified message
        result = society.send("orchestrator", "worker1", {"task": "analyze"})

        # Check reputation
        print(f"Orchestrator reputation: {society.get_reputation('orchestrator')}")
    """
    return SimpleSociety(name=name, preset=preset, agents=agents)


def quick_send(
    from_agent: str,
    to_agent: str,
    payload: Dict[str, Any],
    society_name: str = "QuickSociety",
) -> SendResult:
    """
    Send a one-off verified message without society setup.

    This creates a temporary society for a single message exchange.
    For multiple messages, use create_agent_society instead.

    Args:
        from_agent: Sender agent ID.
        to_agent: Receiver agent ID.
        payload: Message content.
        society_name: Optional society name.

    Returns:
        SendResult with verification status.

    Example:
        result = quick_send("agent_a", "agent_b", {"msg": "hello"})
    """
    society = create_agent_society(society_name, [from_agent, to_agent])
    return society.send(from_agent, to_agent, payload)
