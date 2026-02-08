"""
Hybrid Verification System

Combines all verification approaches into a unified system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging

from lib.society.events import AgentEvent, EventStore
from lib.society.verification import AxiomComplianceMonitor, VerificationResult
from lib.society.contracts import AgentContract, ContractRegistry, ContractVerifier
from lib.society.trust import ReputationSystem, TrustGraph, AgentIdentity
from lib.society.blockchain import AnchorService, LocalAnchor, AttestationRegistry

logger = logging.getLogger(__name__)


class VerificationLevel(Enum):
    """Verification depth levels."""
    BASIC = "basic"        # Just axiom compliance
    STANDARD = "standard"  # Axiom + contracts
    FULL = "full"          # All checks including trust
    ANCHORED = "anchored"  # Full + blockchain anchoring


@dataclass
class SystemConfig:
    """
    Hybrid system configuration.
    
    Attributes:
        verification_level: Default verification depth.
        auto_anchor: Whether to auto-anchor verified events.
        anchor_threshold: Minimum events before anchoring.
        reputation_decay: Whether to decay reputation over time.
        trust_transitivity: Whether to compute transitive trust.
    """
    verification_level: VerificationLevel = VerificationLevel.STANDARD
    auto_anchor: bool = False
    anchor_threshold: int = 100
    reputation_decay: bool = True
    trust_transitivity: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "verification_level": self.verification_level.value,
            "auto_anchor": self.auto_anchor,
            "anchor_threshold": self.anchor_threshold,
            "reputation_decay": self.reputation_decay,
            "trust_transitivity": self.trust_transitivity,
        }


@dataclass
class HybridVerificationResult:
    """
    Result from hybrid verification.
    
    Attributes:
        event: The verified event.
        timestamp: When verification occurred.
        axiom_result: Result of axiom compliance check.
        contract_violations: Any contract violations.
        trust_score: Trust score of the acting agent.
        overall_pass: Whether all checks passed.
        anchored: Whether event was anchored.
        anchor_id: Anchor ID if anchored.
    """
    event: AgentEvent
    timestamp: datetime = field(default_factory=datetime.utcnow)
    axiom_result: Optional[VerificationResult] = None
    contract_violations: List[Any] = field(default_factory=list)
    trust_score: Optional[float] = None
    overall_pass: bool = False
    anchored: bool = False
    anchor_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_id": self.event.event_id,
            "timestamp": self.timestamp.isoformat(),
            "axiom_passed": self.axiom_result.passed if self.axiom_result else None,
            "axiom_violations": [
                r.axiom_id.value for r in self.axiom_result.results
                if not r.passed
            ] if self.axiom_result else [],
            "contract_violations": len(self.contract_violations),
            "trust_score": self.trust_score,
            "overall_pass": self.overall_pass,
            "anchored": self.anchored,
            "anchor_id": self.anchor_id,
        }


class HybridVerificationSystem:
    """
    Unified verification system combining all approaches.
    
    Integrates:
    - Event sourcing with hash chains
    - Axiom compliance verification
    - Contract verification
    - Trust and reputation
    - Blockchain anchoring
    
    Usage:
        system = HybridVerificationSystem.create_default()
        
        # Record and verify an event
        result = system.record_event(event)
        
        if result.overall_pass:
            print("Event verified successfully")
        else:
            print(f"Verification failed: {result.axiom_result}")
        
        # Check agent trust
        if system.is_trusted("agent-123"):
            # Allow privileged operation
    
    SDG - Love - Truth - Beauty
    """
    
    def __init__(
        self,
        config: Optional[SystemConfig] = None,
        event_store: Optional[EventStore] = None,
        axiom_monitor: Optional[AxiomComplianceMonitor] = None,
        contract_registry: Optional[ContractRegistry] = None,
        contract_verifier: Optional[ContractVerifier] = None,
        reputation_system: Optional[ReputationSystem] = None,
        trust_graph: Optional[TrustGraph] = None,
        anchor_service: Optional[AnchorService] = None,
        attestation_registry: Optional[AttestationRegistry] = None
    ):
        """
        Initialize hybrid verification system.
        
        Args:
            config: System configuration.
            event_store: Event storage.
            axiom_monitor: Axiom compliance monitor.
            contract_registry: Contract registry.
            contract_verifier: Contract verifier.
            reputation_system: Reputation tracking.
            trust_graph: Trust relationships.
            anchor_service: Blockchain anchoring.
            attestation_registry: Attestation management.
        """
        self.config = config or SystemConfig()
        
        # Core components
        self.event_store = event_store or EventStore()
        self.axiom_monitor = axiom_monitor
        self.contract_registry = contract_registry or ContractRegistry()
        self.contract_verifier = contract_verifier
        self.reputation_system = reputation_system or ReputationSystem(
            decay_enabled=self.config.reputation_decay
        )
        self.trust_graph = trust_graph or TrustGraph()
        self.anchor_service = anchor_service
        self.attestation_registry = attestation_registry
        
        # Create contract verifier if needed
        if not self.contract_verifier and self.contract_registry:
            self.contract_verifier = ContractVerifier(self.contract_registry)
        
        # Verification handlers
        self._violation_handlers: List[Callable[[HybridVerificationResult], None]] = []
        
        # Statistics
        self._stats = {
            "events_processed": 0,
            "events_passed": 0,
            "events_failed": 0,
            "events_anchored": 0,
        }
    
    @classmethod
    def create_default(
        cls,
        config: Optional[SystemConfig] = None,
        with_blockchain: bool = False
    ) -> "HybridVerificationSystem":
        """
        Create system with default components.
        
        Args:
            config: Optional configuration.
            with_blockchain: Whether to enable blockchain anchoring.
            
        Returns:
            Configured HybridVerificationSystem.
        """
        from lib.society.verification import create_default_monitor
        
        anchor_service = None
        attestation_registry = None
        
        if with_blockchain:
            anchor_service = AnchorService(LocalAnchor())
            attestation_registry = AttestationRegistry(anchor_service)
        
        return cls(
            config=config,
            axiom_monitor=create_default_monitor(),
            anchor_service=anchor_service,
            attestation_registry=attestation_registry,
        )
    
    def record_event(
        self,
        event: AgentEvent,
        level: Optional[VerificationLevel] = None
    ) -> HybridVerificationResult:
        """
        Record and verify an event.
        
        Args:
            event: The event to record and verify.
            level: Optional override for verification level.
            
        Returns:
            HybridVerificationResult with all verification outcomes.
        """
        level = level or self.config.verification_level
        
        result = HybridVerificationResult(event=event)
        overall_pass = True
        
        # Step 1: Store event (use agent and action from the event)
        stored_event = self.event_store.append(
            event.agent,
            event.action,
            event.axiom_context,
        )
        # Update the event reference to the properly stored event
        result.event = stored_event
        event = stored_event
        
        # Step 2: Axiom compliance (all levels)
        if self.axiom_monitor:
            result.axiom_result = self.axiom_monitor.verify(event)
            if result.axiom_result.has_violations():
                overall_pass = False
                self._update_reputation(event.agent.id, False, "axiom_violation")
        
        # Step 3: Contract verification (standard+)
        if level.value in ["standard", "full", "anchored"]:
            if self.contract_verifier:
                verification = self.contract_verifier.verify_action(
                    event.agent.id,
                    event.action.type.value,
                )
                result.contract_violations = verification.violations
                if verification.has_violations():
                    overall_pass = False
                    self._update_reputation(event.agent.id, False, "contract_violation")
        
        # Step 4: Trust check (full+)
        if level.value in ["full", "anchored"]:
            result.trust_score = self.reputation_system.get_score(
                event.agent.id
            ).current_score
            
            if result.trust_score < 30.0:
                logger.warning(f"Low trust agent: {event.agent.id} ({result.trust_score})")
        
        # Step 5: Blockchain anchoring (anchored only)
        if level == VerificationLevel.ANCHORED and self.anchor_service:
            self.anchor_service.add_event(event.compute_hash())
            
            # Auto-anchor if threshold reached
            if self.anchor_service.get_pending_count() >= self.config.anchor_threshold:
                anchor = self.anchor_service.create_anchor()
                if anchor:
                    self.anchor_service.submit_anchor(anchor.anchor_id)
                    result.anchored = True
                    result.anchor_id = anchor.anchor_id
        
        # Finalize result
        result.overall_pass = overall_pass
        
        # Update stats
        self._stats["events_processed"] += 1
        if overall_pass:
            self._stats["events_passed"] += 1
            self._update_reputation(event.agent.id, True, "event_passed")
        else:
            self._stats["events_failed"] += 1
            self._trigger_violation_handlers(result)
        
        if result.anchored:
            self._stats["events_anchored"] += 1
        
        return result
    
    def verify_event(self, event: AgentEvent) -> VerificationResult:
        """
        Verify an event without recording it.
        
        Args:
            event: The event to verify.
            
        Returns:
            Axiom verification result.
        """
        if self.axiom_monitor:
            return self.axiom_monitor.verify(event)
        
        # Return passing result if no monitor
        return VerificationResult(results=[], passed=True)
    
    def register_contract(self, contract: AgentContract) -> None:
        """Register a contract."""
        self.contract_registry.add(contract)
    
    def delegate_trust(
        self,
        delegator: str,
        delegate: str,
        trust_level: float,
        scope: Optional[List[str]] = None
    ) -> None:
        """Delegate trust between agents."""
        self.trust_graph.delegate_trust(delegator, delegate, trust_level, scope)
    
    def is_trusted(self, agent_id: str, min_score: float = 50.0) -> bool:
        """
        Check if an agent is trusted.
        
        Args:
            agent_id: The agent to check.
            min_score: Minimum required score.
            
        Returns:
            True if agent meets trust threshold.
        """
        score = self.reputation_system.get_score(agent_id)
        return score.current_score >= min_score
    
    def get_trust_path(self, source: str, target: str) -> Optional[List[str]]:
        """Get trust delegation path between agents."""
        return self.trust_graph.find_trust_path(source, target)
    
    def add_violation_handler(
        self,
        handler: Callable[[HybridVerificationResult], None]
    ) -> None:
        """Add a violation handler."""
        self._violation_handlers.append(handler)
    
    def _update_reputation(
        self,
        agent_id: str,
        positive: bool,
        reason: str
    ) -> None:
        """Update agent reputation."""
        self.reputation_system.record_compliance(agent_id, positive, reason)
    
    def _trigger_violation_handlers(self, result: HybridVerificationResult) -> None:
        """Trigger violation handlers."""
        for handler in self._violation_handlers:
            try:
                handler(result)
            except Exception as e:
                logger.error(f"Violation handler error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            **self._stats,
            "event_store_size": self.event_store.count,
            "contract_count": len(self.contract_registry.contracts),
            "trusted_agents": len(self.reputation_system.get_trusted_agents()),
        }
    
    def get_agent_profile(self, agent_id: str) -> Dict[str, Any]:
        """
        Get complete profile for an agent.
        
        Args:
            agent_id: The agent ID.
            
        Returns:
            Profile with events, contracts, reputation, trust.
        """
        from lib.society.events import EventQuery
        
        reputation = self.reputation_system.get_score(agent_id)
        contracts = self.contract_registry.find_contracts(agent_id, active_only=False)
        events = self.event_store.query(EventQuery(agent_id=agent_id))
        trust_network = self.trust_graph.get_trust_network(agent_id, depth=1)
        
        return {
            "agent_id": agent_id,
            "reputation": reputation.to_dict(),
            "contracts": [c.contract_id for c in contracts],
            "event_count": len(events),
            "trust_network": trust_network,
        }
    
    def flush_anchors(self) -> Optional[str]:
        """
        Force anchor creation for pending events.
        
        Returns:
            Anchor ID if created.
        """
        if not self.anchor_service:
            return None
        
        if self.anchor_service.get_pending_count() == 0:
            return None
        
        anchor = self.anchor_service.create_anchor()
        if anchor:
            self.anchor_service.submit_anchor(anchor.anchor_id)
            self._stats["events_anchored"] += anchor.event_count
            return anchor.anchor_id
        
        return None
    
    def export(self) -> Dict[str, Any]:
        """Export system state."""
        return {
            "config": self.config.to_dict(),
            "stats": self.get_stats(),
            "reputation": self.reputation_system.export(),
            "trust_graph": self.trust_graph.export(),
            "contracts": self.contract_registry.export(),
        }
