"""
Society Context

Shared context for multi-agent society operations.

Provides a unified container for all verification infrastructure
components that agents share when participating in the society.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import logging

from lib.society.events import EventStore
from lib.society.verification import AxiomComplianceMonitor, create_default_monitor
from lib.society.contracts import ContractRegistry, ContractVerifier
from lib.society.trust import ReputationSystem, TrustGraph, IdentityRegistry
from lib.society.hybrid import VerificationLevel

logger = logging.getLogger(__name__)


@dataclass
class SocietyConfig:
    """
    Configuration for the society context.
    
    Attributes:
        name: Human-readable name for this society.
        verification_level: Default verification depth.
        event_store_path: Optional path for event persistence.
        contract_store_path: Optional path for contract persistence.
        auto_persist: Whether to auto-save changes.
        escalation_threshold: Violations before escalation.
    """
    name: str = "Factory Agent Society"
    verification_level: VerificationLevel = VerificationLevel.STANDARD
    event_store_path: Optional[str] = None
    contract_store_path: Optional[str] = None
    auto_persist: bool = True
    escalation_threshold: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "verification_level": self.verification_level.value,
            "event_store_path": self.event_store_path,
            "contract_store_path": self.contract_store_path,
            "auto_persist": self.auto_persist,
            "escalation_threshold": self.escalation_threshold,
        }


class SocietyContext:
    """
    Shared context for multi-agent society.
    
    Provides centralized access to:
    - Event store for recording agent actions
    - Axiom compliance monitor for verification
    - Contract registry and verifier
    - Trust and reputation system
    - Identity registry for agent authentication
    
    This is the "glue" that connects all verification infrastructure.
    
    Usage:
        # Create default context
        context = SocietyContext.create_default()
        
        # Access components
        context.event_store.append(agent, action)
        result = context.axiom_monitor.verify(event)
        
        # Get system statistics
        stats = context.get_stats()
    
    SDG - Love - Truth - Beauty
    """
    
    def __init__(
        self,
        config: Optional[SocietyConfig] = None,
        event_store: Optional[EventStore] = None,
        axiom_monitor: Optional[AxiomComplianceMonitor] = None,
        contract_registry: Optional[ContractRegistry] = None,
        reputation_system: Optional[ReputationSystem] = None,
        trust_graph: Optional[TrustGraph] = None,
        identity_registry: Optional[IdentityRegistry] = None,
    ):
        """
        Initialize society context.
        
        Args:
            config: Society configuration.
            event_store: Event storage component.
            axiom_monitor: Axiom compliance monitor.
            contract_registry: Contract registry.
            reputation_system: Reputation tracking.
            trust_graph: Trust relationships.
            identity_registry: Agent identity management.
        """
        self.config = config or SocietyConfig()
        
        # Core components
        self.event_store = event_store or EventStore(
            storage_path=self.config.event_store_path
        )
        self.axiom_monitor = axiom_monitor or create_default_monitor(
            escalation_threshold=self.config.escalation_threshold
        )
        self.contract_registry = contract_registry or ContractRegistry(
            storage_path=self.config.contract_store_path
        )
        self.contract_verifier = ContractVerifier(self.contract_registry)
        self.reputation_system = reputation_system or ReputationSystem()
        self.trust_graph = trust_graph or TrustGraph()
        self.identity_registry = identity_registry or IdentityRegistry()
        
        # Event listeners
        self._event_listeners: List[Callable[[Any], None]] = []
        self._message_listeners: List[Callable[[Any], None]] = []
        
        # Statistics
        self._created_at = datetime.now(timezone.utc)
        self._stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "verifications_passed": 0,
            "verifications_failed": 0,
        }
        
        logger.info(f"Society context initialized: {self.config.name}")
    
    @classmethod
    def create_default(
        cls,
        name: str = "Factory Agent Society",
        persist_path: Optional[str] = None,
    ) -> "SocietyContext":
        """
        Create context with sensible defaults.
        
        Args:
            name: Society name.
            persist_path: Optional base path for persistence.
            
        Returns:
            Configured SocietyContext.
        """
        config = SocietyConfig(name=name)
        
        if persist_path:
            base = Path(persist_path)
            config.event_store_path = str(base / "events.json")
            config.contract_store_path = str(base / "contracts.json")
        
        return cls(config=config)
    
    @classmethod
    def create_with_blockchain(
        cls,
        name: str = "Factory Agent Society",
        persist_path: Optional[str] = None,
    ) -> "SocietyContext":
        """
        Create context with blockchain anchoring enabled.
        
        Args:
            name: Society name.
            persist_path: Optional base path for persistence.
            
        Returns:
            Configured SocietyContext with blockchain support.
        """
        context = cls.create_default(name=name, persist_path=persist_path)
        
        # Import blockchain components
        from lib.society.blockchain import AnchorService, LocalAnchor, AttestationRegistry
        
        context.anchor_service = AnchorService(LocalAnchor())
        context.attestation_registry = AttestationRegistry(context.anchor_service)
        
        return context
    
    def add_event_listener(self, listener: Callable[[Any], None]) -> None:
        """Add listener for new events."""
        self._event_listeners.append(listener)
        self.event_store.add_listener(listener)
    
    def add_message_listener(self, listener: Callable[[Any], None]) -> None:
        """Add listener for routed messages."""
        self._message_listeners.append(listener)
    
    def notify_message(self, message: Any) -> None:
        """Notify listeners of a routed message."""
        for listener in self._message_listeners:
            try:
                listener(message)
            except Exception as e:
                logger.error(f"Message listener error: {e}")
    
    def record_verification(self, passed: bool) -> None:
        """Record verification result for statistics."""
        if passed:
            self._stats["verifications_passed"] += 1
        else:
            self._stats["verifications_failed"] += 1
    
    def record_message(self, sent: bool = True) -> None:
        """Record message for statistics."""
        if sent:
            self._stats["messages_sent"] += 1
        else:
            self._stats["messages_received"] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        return {
            "name": self.config.name,
            "created_at": self._created_at.isoformat(),
            "uptime_seconds": (datetime.now(timezone.utc) - self._created_at).total_seconds(),
            **self._stats,
            "event_count": self.event_store.count,
            "contract_count": len(self.contract_registry.contracts),
            "registered_agents": len(self.identity_registry.list_agents()),
            "trusted_agents": len(self.reputation_system.get_trusted_agents()),
        }
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get status summary for an agent.
        
        Args:
            agent_id: The agent ID.
            
        Returns:
            Dictionary with agent status information.
        """
        reputation = self.reputation_system.get_score(agent_id)
        contracts = self.contract_registry.find_contracts(agent_id, active_only=False)
        events = self.event_store.get_agent_events(agent_id, limit=10)
        violations = self.axiom_monitor.get_violation_count(agent_id)
        
        return {
            "agent_id": agent_id,
            "reputation": {
                "score": reputation.current_score,
                "level": reputation.trust_level,
                "is_trusted": reputation.is_trusted,
            },
            "contracts": [c.contract_id for c in contracts],
            "recent_events": len(events),
            "violation_count": violations,
            "is_registered": agent_id in self.identity_registry.list_agents(),
        }
    
    def export(self) -> Dict[str, Any]:
        """Export context state for persistence/debugging."""
        return {
            "config": self.config.to_dict(),
            "stats": self.get_stats(),
            "events": self.event_store.export(),
            "contracts": self.contract_registry.export(),
            "reputation": self.reputation_system.export(),
            "trust_graph": self.trust_graph.export(),
        }
