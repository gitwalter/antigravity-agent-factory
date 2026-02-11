"""
Agent Society Bridge

Connects individual Factory agents to the verification system.

Provides a clean interface for agents to:
- Send verified messages to other agents
- Receive verified messages from the society
- Participate in contracts
- Build and check reputation
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging
import uuid

from lib.society.events import (
    Agent,
    AgentType,
    Action,
    ActionType,
    AxiomContext,
    AgentEvent,
)
from lib.society.verification import VerificationResult, VerificationStatus
from lib.society.contracts import (
    AgentContract,
    Party,
    Capability,
    ContractVerificationResult,
    ContractStatus,
)
from lib.society.trust import AgentIdentity

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of inter-agent messages."""
    REQUEST = "request"
    INFORM = "inform"
    PROPOSE = "propose"
    ACCEPT = "accept"
    REJECT = "reject"
    QUERY = "query"
    CONFIRM = "confirm"


@dataclass
class BridgeResult:
    """
    Result of a bridge operation.
    
    Attributes:
        success: Whether the operation succeeded.
        verified: Whether verification passed.
        event_id: ID of the created event (if any).
        event: The created AgentEvent (if any).
        axiom_result: Result of axiom verification.
        contract_result: Result of contract verification.
        violations: List of violation descriptions.
        message: Human-readable result message.
    """
    success: bool
    verified: bool = False
    event_id: Optional[str] = None
    event: Optional[AgentEvent] = None
    axiom_result: Optional[VerificationResult] = None
    contract_result: Optional[ContractVerificationResult] = None
    violations: List[str] = field(default_factory=list)
    message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "verified": self.verified,
            "event_id": self.event_id,
            "violations": self.violations,
            "message": self.message,
        }


class AgentSocietyBridge:
    """
    Bridge connecting a Factory agent to the verification system.
    
    Provides:
    - Identity management with cryptographic keys
    - Verified message sending to other agents
    - Message receiving from the society
    - Contract participation (sign, verify actions)
    - Reputation tracking
    
    Usage:
        # Create bridge for an agent
        bridge = AgentSocietyBridge(
            agent_id="knowledge-manager",
            agent_type="coordinator",
            context=society_context,
        )
        
        # Send verified message
        result = await bridge.send_message(
            target="template-generator",
            message_type=MessageType.PROPOSE,
            payload={"update": "new-knowledge"},
            justification="Proposing knowledge update for user benefit",
        )
        
        # Check trust level
        if bridge.is_trusted():
            # Perform privileged operation
            pass
    
    SDG - Love - Truth - Beauty
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        context: "SocietyContext",
        name: Optional[str] = None,
        auto_register: bool = True,
    ):
        """
        Initialize agent bridge.
        
        Args:
            agent_id: Unique agent identifier.
            agent_type: Type of agent (worker, coordinator, guardian, etc.).
            context: Shared society context.
            name: Optional human-readable name.
            auto_register: Whether to auto-register identity.
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.context = context
        self.name = name or agent_id
        
        # Create or load identity
        self.identity = AgentIdentity.create(
            name=self.name,
            agent_type=self.agent_type,
        )
        # Override the generated ID with our agent_id for consistency
        self.identity._agent_id = agent_id
        
        # Create Agent object for event creation
        self._agent = Agent(
            id=self.agent_id,
            type=self._parse_agent_type(agent_type),
            public_key=self.identity.public_key,
            name=self.name,
        )
        
        # Register with society
        if auto_register:
            self._register()
        
        # Message handlers
        self._message_handlers: List[Callable[[AgentEvent], None]] = []
        
        logger.info(f"Bridge created for agent: {self.agent_id} ({self.agent_type})")
    
    def _parse_agent_type(self, type_str: str) -> AgentType:
        """Parse agent type string to enum."""
        type_map = {
            "coordinator": AgentType.COORDINATOR,
            "supervisor": AgentType.SUPERVISOR,
            "executor": AgentType.WORKER,
            "worker": AgentType.WORKER,
            "specialist": AgentType.SPECIALIST,
            "analyst": AgentType.SPECIALIST,
            "guardian": AgentType.GUARDIAN,
        }
        return type_map.get(type_str.lower(), AgentType.WORKER)
    
    def _register(self) -> None:
        """Register agent with the society."""
        self.context.identity_registry.register(self.identity)
        logger.debug(f"Agent registered: {self.agent_id}")
    
    @property
    def public_key(self) -> str:
        """Get agent's public key."""
        return self.identity.public_key
    
    @property
    def reputation_score(self) -> float:
        """Get current reputation score."""
        return self.context.reputation_system.get_score(self.agent_id).current_score
    
    @property
    def trust_level(self) -> str:
        """Get current trust level (high, medium, low, untrusted)."""
        return self.context.reputation_system.get_score(self.agent_id).trust_level
    
    def is_trusted(self, min_score: float = 50.0) -> bool:
        """Check if agent is trusted."""
        return self.reputation_score >= min_score
    
    def send_message(
        self,
        target: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        justification: str = "",
        axiom_alignment: Optional[List[str]] = None,
    ) -> BridgeResult:
        """
        Send a verified message to another agent.
        
        Args:
            target: Target agent ID.
            message_type: Type of message.
            payload: Message content.
            justification: Explanation of why this action serves the axioms.
            axiom_alignment: Declared axiom alignment (default: ["A1", "A2"]).
            
        Returns:
            BridgeResult with verification status and event details.
        """
        # Create action
        action = Action(
            type=ActionType.MESSAGE,
            description=f"Send {message_type.value} message to {target}",
            payload={
                "message_type": message_type.value,
                "target": target,
                "content": payload,
            },
            target=target,
        )
        
        # Create axiom context
        axiom_context = AxiomContext(
            declared_alignment=axiom_alignment or ["A1", "A2"],
            justification=justification or f"Message sent for legitimate communication with {target}",
        )
        
        # Store event and verify
        try:
            event = self.context.event_store.append(
                agent=self._agent,
                action=action,
                axiom_context=axiom_context,
            )
            
            # Verify axiom compliance
            verification_result = self.context.axiom_monitor.verify(event)
            
            # Check contract (if exists between agents)
            contract_result = self.context.contract_verifier.verify_action(
                self.agent_id,
                message_type.value,
            )
            
            # Determine overall success
            axiom_passed = not verification_result.has_violations()
            contract_ok = contract_result.status in [
                ContractStatus.VERIFIED,
                ContractStatus.NO_CONTRACT,
            ]
            verified = axiom_passed and contract_ok
            
            # Update reputation
            self.context.reputation_system.record_compliance(
                self.agent_id,
                axiom_passed,
                f"Message to {target}",
            )
            
            # Record statistics
            self.context.record_verification(verified)
            self.context.record_message(sent=True)
            
            # Collect violations
            violations = []
            if verification_result.has_violations():
                violations.extend([
                    f"{v.axiom.value}: {v.reason}"
                    for v in verification_result.get_violations()
                ])
            if contract_result.has_violations():
                violations.extend([
                    f"Contract: {v.message}"
                    for v in contract_result.violations
                ])
            
            # Notify message listeners
            if verified:
                self.context.notify_message(event)
            
            return BridgeResult(
                success=True,
                verified=verified,
                event_id=event.event_id,
                event=event,
                axiom_result=verification_result,
                contract_result=contract_result,
                violations=violations,
                message="Message sent and verified" if verified else "Message sent with violations",
            )
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return BridgeResult(
                success=False,
                verified=False,
                violations=[str(e)],
                message=f"Failed to send message: {e}",
            )
    
    def send_decision(
        self,
        description: str,
        payload: Dict[str, Any],
        justification: str = "",
        axiom_alignment: Optional[List[str]] = None,
    ) -> BridgeResult:
        """
        Record a verified decision.
        
        Args:
            description: Description of the decision.
            payload: Decision details.
            justification: Axiom justification.
            axiom_alignment: Declared axiom alignment.
            
        Returns:
            BridgeResult with verification status.
        """
        action = Action(
            type=ActionType.DECISION,
            description=description,
            payload=payload,
        )
        
        axiom_context = AxiomContext(
            declared_alignment=axiom_alignment or ["A1", "A2", "A3"],
            justification=justification or "Decision made for user benefit",
        )
        
        try:
            event = self.context.event_store.append(
                agent=self._agent,
                action=action,
                axiom_context=axiom_context,
            )
            
            verification_result = self.context.axiom_monitor.verify(event)
            verified = not verification_result.has_violations()
            
            self.context.reputation_system.record_compliance(
                self.agent_id, verified, description[:50]
            )
            self.context.record_verification(verified)
            
            violations = [
                f"{v.axiom.value}: {v.reason}"
                for v in verification_result.get_violations()
            ] if verification_result.has_violations() else []
            
            return BridgeResult(
                success=True,
                verified=verified,
                event_id=event.event_id,
                event=event,
                axiom_result=verification_result,
                violations=violations,
                message="Decision recorded" if verified else "Decision recorded with violations",
            )
            
        except Exception as e:
            logger.error(f"Failed to record decision: {e}")
            return BridgeResult(
                success=False,
                verified=False,
                violations=[str(e)],
                message=f"Failed to record decision: {e}",
            )
    
    def add_message_handler(self, handler: Callable[[AgentEvent], None]) -> None:
        """
        Add handler for incoming messages.
        
        Args:
            handler: Callback receiving AgentEvent for messages to this agent.
        """
        self._message_handlers.append(handler)
    
    def handle_incoming(self, event: AgentEvent) -> None:
        """
        Handle an incoming message event.
        
        Args:
            event: The incoming message event.
        """
        if event.action.target != self.agent_id:
            return
        
        self.context.record_message(sent=False)
        
        for handler in self._message_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Message handler error: {e}")
    
    def sign_contract(self, contract: AgentContract) -> bool:
        """
        Sign a contract as a party.
        
        Args:
            contract: The contract to sign.
            
        Returns:
            True if successfully signed.
        """
        if not contract.get_party(self.agent_id):
            logger.error(f"Agent {self.agent_id} is not a party to this contract")
            return False
        
        # Sign the contract hash
        signature = self.identity.sign(contract.compute_hash())
        contract.signatures[self.agent_id] = signature
        
        logger.info(f"Agent {self.agent_id} signed contract {contract.contract_id}")
        return True
    
    def create_contract_with(
        self,
        other_agent_id: str,
        other_role: str,
        my_role: str,
        my_capabilities: List[str],
        other_capabilities: List[str],
        **kwargs,
    ) -> AgentContract:
        """
        Create a contract with another agent.
        
        Args:
            other_agent_id: The other agent's ID.
            other_role: Role for the other agent.
            my_role: Role for this agent.
            my_capabilities: Actions this agent can perform.
            other_capabilities: Actions the other agent can perform.
            **kwargs: Additional contract parameters.
            
        Returns:
            The created (but not yet signed) contract.
        """
        # Get other agent's public key if registered
        other_key = self.context.identity_registry.get_public_key(other_agent_id)
        if not other_key:
            other_key = "pending_registration"
        
        parties = [
            Party(
                agent_id=self.agent_id,
                role=my_role,
                public_key=self.public_key,
                name=self.name,
            ),
            Party(
                agent_id=other_agent_id,
                role=other_role,
                public_key=other_key,
            ),
        ]
        
        capabilities = {
            my_role: [Capability(action=a) for a in my_capabilities],
            other_role: [Capability(action=a) for a in other_capabilities],
        }
        
        contract = AgentContract.create(
            parties=parties,
            capabilities=capabilities,
            **kwargs,
        )
        
        # Register contract
        self.context.contract_registry.add(contract)
        
        # Sign our part
        self.sign_contract(contract)
        
        logger.info(f"Contract created: {contract.contract_id}")
        return contract
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status for this agent."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "name": self.name,
            "public_key": self.public_key[:16] + "...",
            "reputation": {
                "score": self.reputation_score,
                "level": self.trust_level,
                "is_trusted": self.is_trusted(),
            },
            **self.context.get_agent_status(self.agent_id),
        }
