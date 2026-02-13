"""
Contract Schema

Dataclasses for agent contracts with deontic logic support.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
import json
import uuid


class DisputeMethod(Enum):
    """Methods for resolving contract disputes."""
    ESCALATE_TO_SUPERVISOR = "escalate_to_supervisor"
    CONSENSUS_VOTE = "consensus_vote"
    HUMAN_REVIEW = "human_review"
    BLOCKCHAIN_ARBITRATION = "blockchain_arbitration"


@dataclass
class Party:
    """
    Contract party (agent).
    
    Attributes:
        agent_id: Unique agent identifier.
        role: Role in the contract (e.g., service_provider, service_consumer).
        public_key: Ed25519 public key for signature verification.
        name: Optional human-readable name.
    """
    agent_id: str
    role: str
    public_key: str
    name: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "agent_id": self.agent_id,
            "role": self.role,
            "public_key": self.public_key,
        }
        if self.name:
            result["name"] = self.name
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Party":
        """Create from dictionary."""
        return cls(
            agent_id=data["agent_id"],
            role=data["role"],
            public_key=data["public_key"],
            name=data.get("name"),
        )


@dataclass
class Capability:
    """
    Action that a role is permitted to perform.
    
    Attributes:
        action: The permitted action name.
        parameters: Optional constraints on the action.
    """
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action": self.action,
            "parameters": self.parameters,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Capability":
        """Create from dictionary."""
        if isinstance(data, str):
            return cls(action=data)
        return cls(
            action=data["action"],
            parameters=data.get("parameters", {}),
        )


@dataclass
class Obligation:
    """
    Action that a role must perform when triggered.
    
    Attributes:
        trigger: Event that activates this obligation.
        action: Required action when triggered.
        parameters: Action-specific parameters (e.g., timeout_ms).
    """
    trigger: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "trigger": self.trigger,
            "action": self.action,
            "parameters": self.parameters,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Obligation":
        """Create from dictionary."""
        return cls(
            trigger=data["trigger"],
            action=data["action"],
            parameters=data.get("parameters", {}),
        )


@dataclass
class Prohibition:
    """
    Action that is forbidden.
    
    Attributes:
        action: The forbidden action.
        reason: Why this action is prohibited.
    """
    action: str
    reason: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action": self.action,
            "reason": self.reason,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prohibition":
        """Create from dictionary."""
        if isinstance(data, str):
            return cls(action=data)
        return cls(
            action=data["action"],
            reason=data.get("reason", ""),
        )


@dataclass
class DisputeResolution:
    """
    Configuration for dispute resolution.
    
    Attributes:
        method: Primary resolution method.
        timeout_ms: Time allowed before escalation.
        fallback: Fallback method if primary fails.
    """
    method: DisputeMethod
    timeout_ms: int = 30000
    fallback: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize data."""
        if isinstance(self.method, str):
            self.method = DisputeMethod(self.method)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "method": self.method.value,
            "timeout_ms": self.timeout_ms,
        }
        if self.fallback:
            result["fallback"] = self.fallback
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DisputeResolution":
        """Create from dictionary."""
        return cls(
            method=DisputeMethod(data["method"]),
            timeout_ms=data.get("timeout_ms", 30000),
            fallback=data.get("fallback"),
        )


@dataclass
class AxiomRequirements:
    """
    Axiom alignment declarations for the contract.
    
    Attributes:
        A0_sdg: How contract serves sustainable development.
        A1_love: How contract prioritizes user wellbeing.
        A2_truth: How contract ensures honesty and transparency.
        A3_beauty: How contract maintains simplicity and elegance.
        A4_guardian: How contract supports guardian protocol.
        A5_memory: How contract respects memory consent requirements.
    """
    A0_sdg: Optional[str] = None
    A1_love: Optional[str] = None
    A2_truth: Optional[str] = None
    A3_beauty: Optional[str] = None
    A4_guardian: Optional[str] = None
    A5_memory: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding None values)."""
        result = {}
        if self.A0_sdg:
            result["A0_sdg"] = self.A0_sdg
        if self.A1_love:
            result["A1_love"] = self.A1_love
        if self.A2_truth:
            result["A2_truth"] = self.A2_truth
        if self.A3_beauty:
            result["A3_beauty"] = self.A3_beauty
        if self.A4_guardian:
            result["A4_guardian"] = self.A4_guardian
        if self.A5_memory:
            result["A5_memory"] = self.A5_memory
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AxiomRequirements":
        """Create from dictionary."""
        return cls(
            A0_sdg=data.get("A0_sdg"),
            A1_love=data.get("A1_love"),
            A2_truth=data.get("A2_truth"),
            A3_beauty=data.get("A3_beauty"),
            A4_guardian=data.get("A4_guardian"),
            A5_memory=data.get("A5_memory"),
        )


@dataclass
class AgentContract:
    """
    Formal agreement between agents.
    
    Based on deontic logic:
    - Capabilities: What agents are permitted to do
    - Obligations: What agents must do
    - Prohibitions: What agents cannot do
    
    Attributes:
        contract_id: Unique contract identifier.
        version: Semantic version of the contract.
        created: Creation timestamp.
        expires: Optional expiration timestamp.
        parties: Agents participating in the contract.
        capabilities: Actions each role can perform.
        obligations: Actions each role must perform.
        prohibitions: Actions that are forbidden.
        axiom_requirements: Axiom alignment declarations.
        dispute_resolution: How disputes are resolved.
        signatures: Cryptographic signatures from parties.
        metadata: Additional contract metadata.
    """
    contract_id: str
    version: str
    created: datetime
    parties: List[Party]
    capabilities: Dict[str, List[Capability]]
    obligations: Dict[str, List[Obligation]] = field(default_factory=dict)
    prohibitions: Dict[str, List[Prohibition]] = field(default_factory=dict)
    axiom_requirements: AxiomRequirements = field(default_factory=AxiomRequirements)
    dispute_resolution: Optional[DisputeResolution] = None
    signatures: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    expires: Optional[datetime] = None
    
    @property
    def is_active(self) -> bool:
        """Check if contract is currently active."""
        if not self.is_fully_signed:
            return False
        if self.expires and datetime.now(timezone.utc) > self.expires:
            return False
        return True
    
    @property
    def is_fully_signed(self) -> bool:
        """Check if all parties have signed."""
        party_ids = {p.agent_id for p in self.parties}
        signed_ids = set(self.signatures.keys())
        return party_ids == signed_ids
    
    def get_party(self, agent_id: str) -> Optional[Party]:
        """Get party by agent ID."""
        for party in self.parties:
            if party.agent_id == agent_id:
                return party
        return None
    
    def get_role(self, agent_id: str) -> Optional[str]:
        """Get role of an agent in this contract."""
        party = self.get_party(agent_id)
        return party.role if party else None
    
    def has_capability(self, agent_id: str, action: str) -> bool:
        """Check if agent has capability to perform action."""
        role = self.get_role(agent_id)
        if not role:
            return False
        
        role_capabilities = self.capabilities.get(role, [])
        return any(c.action == action for c in role_capabilities)
    
    def is_prohibited(self, agent_id: str, action: str) -> bool:
        """Check if action is prohibited for agent."""
        role = self.get_role(agent_id)
        
        # Check role-specific prohibitions
        if role:
            role_prohibitions = self.prohibitions.get(role, [])
            if any(p.action == action for p in role_prohibitions):
                return True
        
        # Check global prohibitions
        all_prohibitions = self.prohibitions.get("all_parties", [])
        return any(p.action == action for p in all_prohibitions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "contract_id": self.contract_id,
            "version": self.version,
            "created": self.created.isoformat(),
            "parties": [p.to_dict() for p in self.parties],
            "capabilities": {
                role: [c.to_dict() if hasattr(c, 'to_dict') else c for c in caps]
                for role, caps in self.capabilities.items()
            },
            "obligations": {
                role: [o.to_dict() for o in obls]
                for role, obls in self.obligations.items()
            },
            "prohibitions": {
                role: [p.to_dict() if hasattr(p, 'to_dict') else p for p in probs]
                for role, probs in self.prohibitions.items()
            },
            "axiom_requirements": self.axiom_requirements.to_dict(),
            "signatures": self.signatures,
            "metadata": self.metadata,
        }
        
        if self.expires:
            result["expires"] = self.expires.isoformat()
        if self.dispute_resolution:
            result["dispute_resolution"] = self.dispute_resolution.to_dict()
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)
    
    def to_canonical_json(self) -> str:
        """Convert to canonical JSON for signing (excludes signatures)."""
        data = self.to_dict()
        data.pop("signatures", None)
        return json.dumps(data, sort_keys=True, separators=(",", ":"))
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of contract."""
        canonical = self.to_canonical_json()
        hash_bytes = hashlib.sha256(canonical.encode()).hexdigest()
        return f"sha256:{hash_bytes}"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentContract":
        """Create from dictionary."""
        # Parse capabilities
        capabilities = {}
        for role, caps in data.get("capabilities", {}).items():
            capabilities[role] = [
                Capability.from_dict(c) if isinstance(c, dict) else Capability(action=c)
                for c in caps
            ]
        
        # Parse obligations
        obligations = {}
        for role, obls in data.get("obligations", {}).items():
            obligations[role] = [Obligation.from_dict(o) for o in obls]
        
        # Parse prohibitions
        prohibitions = {}
        for role, probs in data.get("prohibitions", {}).items():
            prohibitions[role] = [
                Prohibition.from_dict(p) if isinstance(p, dict) else Prohibition(action=p)
                for p in probs
            ]
        
        return cls(
            contract_id=data["contract_id"],
            version=data["version"],
            created=datetime.fromisoformat(data["created"]),
            expires=datetime.fromisoformat(data["expires"]) if data.get("expires") else None,
            parties=[Party.from_dict(p) for p in data["parties"]],
            capabilities=capabilities,
            obligations=obligations,
            prohibitions=prohibitions,
            axiom_requirements=AxiomRequirements.from_dict(
                data.get("axiom_requirements", {})
            ),
            dispute_resolution=DisputeResolution.from_dict(data["dispute_resolution"])
                if data.get("dispute_resolution") else None,
            signatures=data.get("signatures", {}),
            metadata=data.get("metadata", {}),
        )
    
    @classmethod
    def create(
        cls,
        parties: List[Party],
        capabilities: Dict[str, List[str]],
        version: str = "1.0.0",
        **kwargs
    ) -> "AgentContract":
        """
        Create a new contract.
        
        Args:
            parties: Contract parties.
            capabilities: Role -> action list mapping.
            version: Contract version.
            **kwargs: Additional contract attributes.
            
        Returns:
            New AgentContract.
        """
        # Convert simple capability strings to Capability objects
        parsed_capabilities = {}
        for role, caps in capabilities.items():
            parsed_capabilities[role] = [
                Capability(action=c) if isinstance(c, str) else c
                for c in caps
            ]
        
        return cls(
            contract_id=str(uuid.uuid4()),
            version=version,
            created=datetime.now(timezone.utc),
            parties=parties,
            capabilities=parsed_capabilities,
            **kwargs,
        )
