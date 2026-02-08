"""
Event Schema

Dataclasses for agent events with cryptographic signing support.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
import json
import uuid


class ActionType(Enum):
    """Types of agent actions."""
    MESSAGE = "message"
    DECISION = "decision"
    STATE_CHANGE = "state_change"
    EXTERNAL_EFFECT = "external_effect"
    CONTRACT_CREATION = "contract_creation"
    CONTRACT_SIGNATURE = "contract_signature"
    VIOLATION_REPORT = "violation_report"


class AgentType(Enum):
    """Types of agents in the society."""
    GUARDIAN = "guardian"
    WORKER = "worker"
    COORDINATOR = "coordinator"
    SUPERVISOR = "supervisor"
    SPECIALIST = "specialist"


@dataclass
class Agent:
    """
    Agent identity with cryptographic key.
    
    Attributes:
        id: Unique agent identifier (UUID).
        type: Role of the agent in the society.
        public_key: Ed25519 public key for signature verification.
        name: Optional human-readable name.
    """
    id: str
    type: AgentType
    public_key: str
    name: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize agent data."""
        if isinstance(self.type, str):
            self.type = AgentType(self.type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "id": self.id,
            "type": self.type.value,
            "public_key": self.public_key,
        }
        if self.name:
            result["name"] = self.name
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Agent":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            type=AgentType(data["type"]),
            public_key=data["public_key"],
            name=data.get("name"),
        )
    
    @classmethod
    def create(
        cls,
        agent_type: AgentType,
        public_key: str,
        name: Optional[str] = None
    ) -> "Agent":
        """Create a new agent with generated ID."""
        return cls(
            id=str(uuid.uuid4()),
            type=agent_type,
            public_key=public_key,
            name=name,
        )


@dataclass
class Action:
    """
    Agent action record.
    
    Attributes:
        type: Type of action performed.
        description: Human-readable description.
        payload: Action-specific data.
        target: Optional target agent ID for directed actions.
    """
    type: ActionType
    description: str
    payload: Dict[str, Any] = field(default_factory=dict)
    target: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize action data."""
        if isinstance(self.type, str):
            self.type = ActionType(self.type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "type": self.type.value,
            "description": self.description,
            "payload": self.payload,
        }
        if self.target:
            result["target"] = self.target
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        """Create from dictionary."""
        return cls(
            type=ActionType(data["type"]),
            description=data["description"],
            payload=data.get("payload", {}),
            target=data.get("target"),
        )


@dataclass
class AxiomContext:
    """
    Axiom alignment declaration for an action.
    
    Attributes:
        declared_alignment: List of axiom IDs this action aligns with.
        justification: Explanation of how action serves declared axioms.
    """
    declared_alignment: List[str] = field(default_factory=list)
    justification: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "declared_alignment": self.declared_alignment,
            "justification": self.justification,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AxiomContext":
        """Create from dictionary."""
        return cls(
            declared_alignment=data.get("declared_alignment", []),
            justification=data.get("justification", ""),
        )


@dataclass
class AgentEvent:
    """
    Immutable record of an agent action with hash chain linking.
    
    Each event includes:
    - Unique ID and timestamp
    - Sequence number for ordering
    - Previous hash for chain linking
    - Agent and action details
    - Axiom context for compliance tracking
    - Cryptographic signature and hash
    
    Attributes:
        event_id: Unique event identifier (UUID).
        timestamp: When the event was created.
        sequence: Monotonically increasing sequence number.
        previous_hash: SHA-256 hash of previous event in chain.
        agent: The agent that performed the action.
        action: The action that was performed.
        axiom_context: Declared axiom alignment.
        signature: Ed25519 signature of canonical JSON.
        hash: SHA-256 hash of complete event.
        verification_status: Current verification status.
    """
    event_id: str
    timestamp: datetime
    sequence: int
    previous_hash: str
    agent: Agent
    action: Action
    axiom_context: AxiomContext
    signature: str
    hash: str
    verification_status: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "sequence": self.sequence,
            "previous_hash": self.previous_hash,
            "agent": self.agent.to_dict(),
            "action": self.action.to_dict(),
            "axiom_context": self.axiom_context.to_dict(),
            "signature": self.signature,
            "hash": self.hash,
            "verification_status": self.verification_status,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)
    
    def to_canonical_json(self) -> str:
        """
        Convert to canonical JSON for signing/hashing.
        
        Excludes signature and hash fields.
        """
        data = self.to_dict()
        data.pop("signature", None)
        data.pop("hash", None)
        data.pop("verification_status", None)
        return json.dumps(data, sort_keys=True, separators=(",", ":"))
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentEvent":
        """Create from dictionary."""
        return cls(
            event_id=data["event_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            sequence=data["sequence"],
            previous_hash=data["previous_hash"],
            agent=Agent.from_dict(data["agent"]),
            action=Action.from_dict(data["action"]),
            axiom_context=AxiomContext.from_dict(data.get("axiom_context", {})),
            signature=data.get("signature", ""),
            hash=data.get("hash", ""),
            verification_status=data.get("verification_status"),
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "AgentEvent":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def create(
        cls,
        agent: Agent,
        action: Action,
        sequence: int,
        previous_hash: str,
        axiom_context: Optional[AxiomContext] = None,
        signer: Optional[Any] = None,
    ) -> "AgentEvent":
        """
        Create a new event with generated ID, timestamp, and hash.
        
        Args:
            agent: The agent performing the action.
            action: The action being performed.
            sequence: Sequence number in the chain.
            previous_hash: Hash of previous event.
            axiom_context: Optional axiom alignment declaration.
            signer: Optional signing service for signature.
            
        Returns:
            New AgentEvent with computed hash.
        """
        event = cls(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            sequence=sequence,
            previous_hash=previous_hash,
            agent=agent,
            action=action,
            axiom_context=axiom_context or AxiomContext(),
            signature="",
            hash="",
        )
        
        # Compute signature if signer provided
        if signer:
            canonical = event.to_canonical_json()
            event.signature = signer.sign(canonical.encode())
        
        # Compute hash
        event.hash = event.compute_hash()
        
        return event
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of the event."""
        # Include signature in hash computation
        data = self.to_dict()
        data.pop("hash", None)
        data.pop("verification_status", None)
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        hash_bytes = hashlib.sha256(canonical.encode()).hexdigest()
        return f"sha256:{hash_bytes}"
    
    def verify_hash(self) -> bool:
        """Verify that the stored hash matches computed hash."""
        return self.hash == self.compute_hash()
