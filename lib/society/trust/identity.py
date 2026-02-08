"""
Agent Identity

Cryptographic identity management for agents using Ed25519 signatures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import secrets

logger = logging.getLogger(__name__)


def _base64_encode(data: bytes) -> str:
    """Encode bytes as base64 string."""
    import base64
    return base64.b64encode(data).decode("utf-8")


def _base64_decode(data: str) -> bytes:
    """Decode base64 string to bytes."""
    import base64
    return base64.b64decode(data.encode("utf-8"))


@dataclass
class KeyPair:
    """
    Ed25519 key pair for agent signing.
    
    Note: This is a simplified implementation using HMAC for demonstration.
    In production, use a proper Ed25519 library like nacl/pynacl.
    
    Attributes:
        private_key: Base64-encoded private key (keep secret!).
        public_key: Base64-encoded public key (share freely).
        created: When the key pair was created.
    """
    private_key: str
    public_key: str
    created: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def generate(cls) -> "KeyPair":
        """Generate a new key pair."""
        # Simplified: Using random bytes as keys
        # In production, use nacl.signing.SigningKey
        private = secrets.token_bytes(32)
        public = hashlib.sha256(private).digest()
        
        return cls(
            private_key=_base64_encode(private),
            public_key=_base64_encode(public),
        )
    
    def sign(self, message: bytes) -> str:
        """
        Sign a message.
        
        Args:
            message: The message to sign.
            
        Returns:
            Base64-encoded signature.
        """
        import hmac
        
        # Simplified: Using HMAC-SHA256 for demonstration
        # In production, use Ed25519 signing
        private_bytes = _base64_decode(self.private_key)
        signature = hmac.new(private_bytes, message, hashlib.sha256).digest()
        return _base64_encode(signature)
    
    def verify(self, message: bytes, signature: str) -> bool:
        """
        Verify a signature.
        
        Args:
            message: The original message.
            signature: The signature to verify.
            
        Returns:
            True if signature is valid.
        """
        expected = self.sign(message)
        return hmac.compare_digest(expected, signature)
    
    def to_dict(self, include_private: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "public_key": self.public_key,
            "created": self.created.isoformat(),
        }
        if include_private:
            result["private_key"] = self.private_key
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KeyPair":
        """Create from dictionary."""
        return cls(
            private_key=data.get("private_key", ""),
            public_key=data["public_key"],
            created=datetime.fromisoformat(data["created"]) if "created" in data else datetime.utcnow(),
        )


@dataclass
class AgentIdentity:
    """
    Complete agent identity with keys and metadata.
    
    Attributes:
        agent_id: Unique identifier (derived from public key).
        name: Human-readable name.
        keypair: Cryptographic key pair.
        metadata: Additional identity metadata.
        created: Identity creation time.
    """
    agent_id: str
    name: str
    keypair: KeyPair
    metadata: Dict[str, Any] = field(default_factory=dict)
    created: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def public_key(self) -> str:
        """Get the public key."""
        return self.keypair.public_key
    
    @classmethod
    def create(
        cls,
        name: str,
        agent_type: str = "worker",
        **metadata
    ) -> "AgentIdentity":
        """
        Create a new agent identity with generated keys.
        
        Args:
            name: Human-readable name.
            agent_type: Type of agent.
            **metadata: Additional metadata.
            
        Returns:
            New AgentIdentity.
        """
        keypair = KeyPair.generate()
        
        # Derive agent ID from public key
        public_bytes = _base64_decode(keypair.public_key)
        agent_id = hashlib.sha256(public_bytes).hexdigest()[:16]
        
        return cls(
            agent_id=agent_id,
            name=name,
            keypair=keypair,
            metadata={"type": agent_type, **metadata},
        )
    
    def sign(self, message: str) -> str:
        """
        Sign a message.
        
        Args:
            message: Message string to sign.
            
        Returns:
            Base64-encoded signature.
        """
        return self.keypair.sign(message.encode("utf-8"))
    
    def verify(self, message: str, signature: str) -> bool:
        """
        Verify a signature.
        
        Args:
            message: Original message string.
            signature: Signature to verify.
            
        Returns:
            True if signature is valid.
        """
        return self.keypair.verify(message.encode("utf-8"), signature)
    
    def sign_json(self, data: Dict[str, Any]) -> str:
        """
        Sign JSON data.
        
        Args:
            data: Data to sign.
            
        Returns:
            Signature.
        """
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return self.sign(canonical)
    
    def to_dict(self, include_private: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "keypair": self.keypair.to_dict(include_private),
            "metadata": self.metadata,
            "created": self.created.isoformat(),
        }
    
    def to_public_dict(self) -> Dict[str, Any]:
        """Convert to public-only dictionary (no private key)."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "public_key": self.public_key,
            "metadata": self.metadata,
            "created": self.created.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentIdentity":
        """Create from dictionary."""
        return cls(
            agent_id=data["agent_id"],
            name=data["name"],
            keypair=KeyPair.from_dict(data["keypair"]),
            metadata=data.get("metadata", {}),
            created=datetime.fromisoformat(data["created"]) if "created" in data else datetime.utcnow(),
        )
    
    def save(self, path: str) -> None:
        """Save identity to file (includes private key!)."""
        filepath = Path(path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(self.to_dict(include_private=True), f, indent=2)
        
        logger.info(f"Saved identity {self.agent_id} to {path}")
    
    @classmethod
    def load(cls, path: str) -> "AgentIdentity":
        """Load identity from file."""
        with open(path, "r") as f:
            data = json.load(f)
        
        identity = cls.from_dict(data)
        logger.info(f"Loaded identity {identity.agent_id} from {path}")
        return identity


class IdentityRegistry:
    """
    Registry for managing agent identities.
    
    Stores public identity information for verification.
    """
    
    def __init__(self):
        """Initialize registry."""
        self._identities: Dict[str, AgentIdentity] = {}
    
    def register(self, identity: AgentIdentity) -> None:
        """Register an identity."""
        self._identities[identity.agent_id] = identity
        logger.info(f"Registered identity: {identity.agent_id} ({identity.name})")
    
    def get(self, agent_id: str) -> Optional[AgentIdentity]:
        """Get identity by agent ID."""
        return self._identities.get(agent_id)
    
    def get_public_key(self, agent_id: str) -> Optional[str]:
        """Get public key for an agent."""
        identity = self.get(agent_id)
        return identity.public_key if identity else None
    
    def verify_signature(
        self,
        agent_id: str,
        message: str,
        signature: str
    ) -> bool:
        """
        Verify a signature from an agent.
        
        Args:
            agent_id: The signing agent.
            message: The original message.
            signature: The signature to verify.
            
        Returns:
            True if signature is valid.
        """
        identity = self.get(agent_id)
        if not identity:
            logger.warning(f"Unknown agent: {agent_id}")
            return False
        
        return identity.verify(message, signature)
    
    def list_agents(self) -> List[str]:
        """Get list of registered agent IDs."""
        return list(self._identities.keys())
    
    def export_public(self) -> Dict[str, Dict[str, Any]]:
        """Export all public identity information."""
        return {
            agent_id: identity.to_public_dict()
            for agent_id, identity in self._identities.items()
        }


# Compatibility import for HMAC
try:
    import hmac
except ImportError:
    hmac = None
