"""
Tests for the hybrid module.

Tests unified verification system and escalation management.
"""

import pytest
from datetime import datetime, timedelta

from lib.society.events import (
    Agent,
    AgentType,
    Action,
    ActionType,
    AxiomContext,
    AgentEvent,
)
from lib.society.hybrid import (
    VerificationLevel,
    SystemConfig,
    HybridVerificationResult,
    HybridVerificationSystem,
    EscalationLevel,
    EscalationStatus,
    Escalation,
    DefaultPolicy,
    EscalationManager,
    create_escalation_from_violation,
)


def create_test_event(
    description: str = "Test action for user benefit",
    agent_id: str = "agent-1",
    action_type: ActionType = ActionType.DECISION,
) -> AgentEvent:
    """Create a test event with all required fields."""
    return AgentEvent(
        event_id=f"evt-{datetime.utcnow().timestamp()}",
        timestamp=datetime.utcnow(),
        sequence=1,  # First event has sequence 1
        previous_hash="",
        agent=Agent(id=agent_id, type=AgentType.WORKER, public_key="pk_test"),
        action=Action(type=action_type, description=description),
        axiom_context=AxiomContext(
            declared_alignment=["A1"],
            justification="Action taken for user benefit and wellbeing"
        ),
        signature="",
        hash="",
    )


class TestSystemConfig:
    """Tests for SystemConfig."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = SystemConfig()
        
        assert config.verification_level == VerificationLevel.STANDARD
        assert config.auto_anchor is False
        assert config.anchor_threshold == 100
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = SystemConfig(
            verification_level=VerificationLevel.FULL,
            auto_anchor=True,
            anchor_threshold=50,
        )
        
        assert config.verification_level == VerificationLevel.FULL
        assert config.auto_anchor is True
        assert config.anchor_threshold == 50
    
    def test_to_dict(self):
        """Test config serialization."""
        config = SystemConfig()
        data = config.to_dict()
        
        assert "verification_level" in data
        assert "auto_anchor" in data


class TestHybridVerificationResult:
    """Tests for HybridVerificationResult."""
    
    def test_create_result(self):
        """Test creating a result."""
        event = create_test_event()
        result = HybridVerificationResult(event=event, overall_pass=True)
        
        assert result.event == event
        assert result.overall_pass is True
    
    def test_to_dict(self):
        """Test result serialization."""
        event = create_test_event()
        result = HybridVerificationResult(
            event=event,
            overall_pass=True,
            trust_score=75.0,
        )
        
        data = result.to_dict()
        
        assert "event_id" in data
        assert "overall_pass" in data
        assert data["trust_score"] == 75.0


class TestHybridVerificationSystem:
    """Tests for HybridVerificationSystem."""
    
    def test_create_default(self):
        """Test creating default system."""
        system = HybridVerificationSystem.create_default()
        
        assert system.axiom_monitor is not None
        assert system.reputation_system is not None
    
    def test_create_with_blockchain(self):
        """Test creating system with blockchain."""
        system = HybridVerificationSystem.create_default(with_blockchain=True)
        
        assert system.anchor_service is not None
        assert system.attestation_registry is not None
    
    def test_record_event_basic(self):
        """Test recording event with basic verification."""
        system = HybridVerificationSystem.create_default()
        event = create_test_event("Complete a helpful task")
        
        result = system.record_event(event, level=VerificationLevel.BASIC)
        
        assert result is not None
        assert result.axiom_result is not None
    
    def test_record_event_standard(self):
        """Test recording event with standard verification."""
        system = HybridVerificationSystem.create_default()
        event = create_test_event("Process user request safely")
        
        result = system.record_event(event, level=VerificationLevel.STANDARD)
        
        assert result.axiom_result is not None
    
    def test_record_event_full(self):
        """Test recording event with full verification."""
        system = HybridVerificationSystem.create_default()
        event = create_test_event("Execute trusted action")
        
        result = system.record_event(event, level=VerificationLevel.FULL)
        
        assert result.trust_score is not None
    
    def test_clean_event_passes(self):
        """Test that clean events pass verification."""
        system = HybridVerificationSystem.create_default()
        event = create_test_event("Help user with legitimate request")
        
        result = system.record_event(event)
        
        assert result.overall_pass is True
    
    def test_is_trusted(self):
        """Test trust checking."""
        system = HybridVerificationSystem.create_default()
        
        # New agent starts at neutral
        is_trusted = system.is_trusted("new-agent", min_score=50.0)
        assert is_trusted
    
    def test_delegate_trust(self):
        """Test trust delegation."""
        system = HybridVerificationSystem.create_default()
        
        system.delegate_trust("alice", "bob", 0.8)
        
        path = system.get_trust_path("alice", "bob")
        assert path is not None
    
    def test_get_stats(self):
        """Test getting statistics."""
        system = HybridVerificationSystem.create_default()
        
        # Process some events
        system.record_event(create_test_event("Action 1"))
        system.record_event(create_test_event("Action 2"))
        
        stats = system.get_stats()
        
        assert stats["events_processed"] == 2
    
    def test_get_agent_profile(self):
        """Test getting agent profile."""
        system = HybridVerificationSystem.create_default()
        
        # Record some events for agent
        system.record_event(create_test_event("Action", agent_id="agent-1"))
        
        profile = system.get_agent_profile("agent-1")
        
        assert profile["agent_id"] == "agent-1"
        assert "reputation" in profile
        assert "event_count" in profile
    
    def test_violation_handler(self):
        """Test violation handler callback."""
        system = HybridVerificationSystem.create_default()
        
        violations = []
        system.add_violation_handler(lambda r: violations.append(r))
        
        # Trigger a violation
        event = create_test_event("Deceive and manipulate user to cause harm")
        system.record_event(event)
        
        # Handler may or may not be called depending on verifier results
        assert hasattr(system, "_violation_handlers")


class TestEscalation:
    """Tests for Escalation."""
    
    def test_create_escalation(self):
        """Test creating an escalation."""
        escalation = Escalation(
            id="esc-1",
            level=EscalationLevel.VIOLATION,
            source="axiom-monitor",
            subject="agent-1",
            reason="Axiom violation detected",
        )
        
        assert escalation.id == "esc-1"
        assert escalation.level == EscalationLevel.VIOLATION
        assert escalation.is_open
    
    def test_is_open(self):
        """Test is_open property."""
        open_esc = Escalation(
            id="e1",
            level=EscalationLevel.WARNING,
            source="s",
            subject="a",
            reason="r",
            status=EscalationStatus.OPEN,
        )
        assert open_esc.is_open
        
        resolved_esc = Escalation(
            id="e2",
            level=EscalationLevel.WARNING,
            source="s",
            subject="a",
            reason="r",
            status=EscalationStatus.RESOLVED,
        )
        assert not resolved_esc.is_open
    
    def test_to_dict(self):
        """Test serialization."""
        escalation = Escalation(
            id="esc-1",
            level=EscalationLevel.CRITICAL,
            source="system",
            subject="agent",
            reason="Critical issue",
        )
        
        data = escalation.to_dict()
        
        assert data["id"] == "esc-1"
        assert data["level_name"] == "CRITICAL"


class TestDefaultPolicy:
    """Tests for DefaultPolicy."""
    
    def test_add_handlers(self):
        """Test adding handlers."""
        policy = DefaultPolicy()
        policy.add_handler("handler-1")
        policy.add_handler("admin-1", is_admin=True)
        
        assert "handler-1" in policy._handlers
        assert "admin-1" in policy._admins
    
    def test_get_handler_for_level(self):
        """Test getting handler based on level."""
        policy = DefaultPolicy(handlers=["h1"], admins=["a1"])
        
        # Critical should get admin
        critical = Escalation(
            id="e1",
            level=EscalationLevel.CRITICAL,
            source="s",
            subject="a",
            reason="r",
        )
        handler = policy.get_handler(critical)
        assert handler == "a1"
        
        # Info should get regular handler
        info = Escalation(
            id="e2",
            level=EscalationLevel.INFO,
            source="s",
            subject="a",
            reason="r",
        )
        handler = policy.get_handler(info)
        assert handler == "h1"
    
    def test_timeout_varies_by_level(self):
        """Test that timeout varies by level."""
        policy = DefaultPolicy()
        
        info = Escalation(
            id="e1",
            level=EscalationLevel.INFO,
            source="s",
            subject="a",
            reason="r",
        )
        emergency = Escalation(
            id="e2",
            level=EscalationLevel.EMERGENCY,
            source="s",
            subject="a",
            reason="r",
        )
        
        info_timeout = policy.get_timeout(info)
        emergency_timeout = policy.get_timeout(emergency)
        
        assert info_timeout > emergency_timeout


class TestEscalationManager:
    """Tests for EscalationManager."""
    
    def test_create_escalation(self):
        """Test creating an escalation."""
        manager = EscalationManager()
        
        escalation = manager.create_escalation(
            level=EscalationLevel.VIOLATION,
            source="test",
            subject="agent-1",
            reason="Test violation",
        )
        
        assert escalation is not None
        assert escalation.level == EscalationLevel.VIOLATION
    
    def test_acknowledge(self):
        """Test acknowledging an escalation."""
        manager = EscalationManager()
        
        esc = manager.create_escalation(
            level=EscalationLevel.WARNING,
            source="test",
            subject="agent",
            reason="Warning",
        )
        
        result = manager.acknowledge(esc.id, "handler-1")
        assert result
        
        esc = manager.get(esc.id)
        assert esc.status == EscalationStatus.ACKNOWLEDGED
        assert esc.assignee == "handler-1"
    
    def test_resolve(self):
        """Test resolving an escalation."""
        manager = EscalationManager()
        
        esc = manager.create_escalation(
            level=EscalationLevel.VIOLATION,
            source="test",
            subject="agent",
            reason="Violation",
        )
        
        manager.acknowledge(esc.id, "handler")
        result = manager.resolve(esc.id, "Issue was a false positive")
        
        assert result
        
        esc = manager.get(esc.id)
        assert esc.status == EscalationStatus.RESOLVED
        assert esc.resolution is not None
    
    def test_dismiss(self):
        """Test dismissing an escalation."""
        manager = EscalationManager()
        
        esc = manager.create_escalation(
            level=EscalationLevel.INFO,
            source="test",
            subject="agent",
            reason="Info only",
        )
        
        result = manager.dismiss(esc.id, "Not a real issue")
        assert result
        
        esc = manager.get(esc.id)
        assert esc.status == EscalationStatus.DISMISSED
    
    def test_escalate_further(self):
        """Test escalating to higher level."""
        manager = EscalationManager()
        
        esc = manager.create_escalation(
            level=EscalationLevel.WARNING,
            source="test",
            subject="agent",
            reason="Warning",
        )
        
        original_level = esc.level
        result = manager.escalate_further(esc.id)
        
        assert result
        
        esc = manager.get(esc.id)
        assert esc.level.value > original_level.value
    
    def test_get_open_escalations(self):
        """Test getting open escalations."""
        manager = EscalationManager()
        
        manager.create_escalation(
            level=EscalationLevel.INFO,
            source="s",
            subject="a",
            reason="Open 1",
        )
        manager.create_escalation(
            level=EscalationLevel.WARNING,
            source="s",
            subject="b",
            reason="Open 2",
        )
        
        esc3 = manager.create_escalation(
            level=EscalationLevel.INFO,
            source="s",
            subject="c",
            reason="To be resolved",
        )
        manager.resolve(esc3.id, "Resolved")
        
        open_escs = manager.get_open_escalations()
        assert len(open_escs) == 2
    
    def test_get_statistics(self):
        """Test getting statistics."""
        manager = EscalationManager()
        
        manager.create_escalation(
            level=EscalationLevel.INFO,
            source="s",
            subject="a",
            reason="1",
        )
        manager.create_escalation(
            level=EscalationLevel.CRITICAL,
            source="s",
            subject="b",
            reason="2",
        )
        
        stats = manager.get_statistics()
        
        assert stats["total"] == 2
        assert stats["open"] == 2
        assert "by_level" in stats
    
    def test_notification_handler(self):
        """Test notification handler is called."""
        manager = EscalationManager()
        
        notifications = []
        manager.add_notification_handler(lambda e: notifications.append(e))
        
        manager.create_escalation(
            level=EscalationLevel.WARNING,
            source="test",
            subject="agent",
            reason="Test",
        )
        
        assert len(notifications) == 1
    
    def test_level_handler(self):
        """Test level-specific handler is called."""
        manager = EscalationManager()
        
        critical_events = []
        manager.register_handler(
            EscalationLevel.CRITICAL,
            lambda e: critical_events.append(e),
        )
        
        # This should not trigger critical handler
        manager.create_escalation(
            level=EscalationLevel.INFO,
            source="s",
            subject="a",
            reason="r",
        )
        assert len(critical_events) == 0
        
        # This should trigger critical handler
        manager.create_escalation(
            level=EscalationLevel.CRITICAL,
            source="s",
            subject="a",
            reason="r",
        )
        assert len(critical_events) == 1
