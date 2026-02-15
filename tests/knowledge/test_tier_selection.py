"""
Tests for Trust Tier Decision Matrix Knowledge.

This test suite verifies that the tier selection knowledge file
provides correct guidance for all scenarios.

SDG - Love - Truth - Beauty
"""

import pytest
import json
from pathlib import Path


class TestTierSelectionKnowledge:
    """Tests for trust-tier-decision-matrix.json."""
    
    @pytest.fixture
    def tier_knowledge(self):
        """Load the tier selection knowledge file."""
        knowledge_path = Path(__file__).parent.parent.parent / ".agent" / "knowledge" / "trust-tier-decision-matrix.json"
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def test_knowledge_structure(self, tier_knowledge):
        """Knowledge file has required structure."""
        assert "metadata" in tier_knowledge
        assert "decision_matrix" in tier_knowledge
        assert "selection_algorithm" in tier_knowledge
        assert "escalation_triggers" in tier_knowledge
    
    def test_all_tiers_defined(self, tier_knowledge):
        """All five tiers are defined."""
        tiers = tier_knowledge["decision_matrix"]["tiers"]
        
        assert "L0_local" in tiers
        assert "L1_attested" in tiers
        assert "L2_contracted" in tiers
        assert "L3_consensus" in tiers
        assert "L4_economic" in tiers
    
    def test_tier_attributes(self, tier_knowledge):
        """Each tier has required attributes."""
        required_attrs = ["name", "mechanism", "latency", "cost", "guarantees", "select_when", "examples"]
        
        for tier_id, tier in tier_knowledge["decision_matrix"]["tiers"].items():
            for attr in required_attrs:
                assert attr in tier, f"Tier {tier_id} missing {attr}"
    
    def test_selection_algorithm_steps(self, tier_knowledge):
        """Selection algorithm has ordered steps."""
        steps = tier_knowledge["selection_algorithm"]["steps"]
        
        assert len(steps) >= 5
        
        for i, step in enumerate(steps):
            assert step["step"] == i + 1
            assert "question" in step
    
    def test_escalation_triggers(self, tier_knowledge):
        """Escalation triggers are defined."""
        triggers = tier_knowledge["escalation_triggers"]["triggers"]
        
        assert len(triggers) >= 3
        
        for trigger in triggers:
            assert "condition" in trigger
            assert "escalation" in trigger
    
    def test_de_escalation_defined(self, tier_knowledge):
        """De-escalation path is defined."""
        de_escalation = tier_knowledge["escalation_triggers"]["de_escalation"]
        
        assert "condition" in de_escalation
        assert "period" in de_escalation
        assert "action" in de_escalation
    
    def test_cost_benefit_analysis(self, tier_knowledge):
        """Cost-benefit analysis is provided."""
        cba = tier_knowledge["cost_benefit_analysis"]
        
        for tier_id in ["L0_local", "L1_attested", "L2_contracted", "L3_consensus", "L4_economic"]:
            assert tier_id in cba
            assert "setup_cost" in cba[tier_id]
            assert "operational_cost" in cba[tier_id]
            assert "security_level" in cba[tier_id]


class TestCoordinationPatternKnowledge:
    """Tests for coordination-pattern-selection.json."""
    
    @pytest.fixture
    def pattern_knowledge(self):
        """Load the pattern selection knowledge file."""
        knowledge_path = Path(__file__).parent.parent.parent / ".agent" / "knowledge" / "coordination-pattern-selection.json"
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def test_knowledge_structure(self, pattern_knowledge):
        """Knowledge file has required structure."""
        assert "metadata" in pattern_knowledge
        assert "patterns" in pattern_knowledge
        assert "selection_algorithm" in pattern_knowledge
        assert "anti_patterns" in pattern_knowledge
    
    def test_core_patterns_defined(self, pattern_knowledge):
        """Core coordination patterns are defined."""
        patterns = pattern_knowledge["patterns"]
        
        assert "supervisor_worker" in patterns
        assert "hierarchical" in patterns
        assert "collaborative" in patterns
        assert "sequential" in patterns
        assert "broadcast" in patterns
    
    def test_pattern_attributes(self, pattern_knowledge):
        """Each pattern has required attributes."""
        required_attrs = ["name", "description", "structure", "select_when", "advantages", "disadvantages", "implementation"]
        
        for pattern_id, pattern in pattern_knowledge["patterns"].items():
            for attr in required_attrs:
                assert attr in pattern, f"Pattern {pattern_id} missing {attr}"
    
    def test_anti_patterns_documented(self, pattern_knowledge):
        """Anti-patterns are documented."""
        anti_patterns = pattern_knowledge["anti_patterns"]
        
        assert len(anti_patterns) >= 3
        
        for ap in anti_patterns:
            assert "name" in ap
            assert "problem" in ap
            assert "fix" in ap


class TestQuickReferenceKnowledge:
    """Tests for asp-quick-reference.json."""
    
    @pytest.fixture
    def quick_ref(self):
        """Load the quick reference knowledge file."""
        knowledge_path = Path(__file__).parent.parent.parent / ".agent" / "knowledge" / "asp-quick-reference.json"
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def test_knowledge_structure(self, quick_ref):
        """Quick reference has required sections."""
        assert "quick_start" in quick_ref
        assert "api_reference" in quick_ref
        assert "message_types" in quick_ref
        assert "trust_tiers" in quick_ref
        assert "coordination_patterns" in quick_ref
        assert "troubleshooting" in quick_ref
    
    def test_quick_start_examples(self, quick_ref):
        """Quick start includes runnable examples."""
        quick_start = quick_ref["quick_start"]
        
        assert "minimal_society" in quick_start
        assert "code" in quick_start["minimal_society"]
    
    def test_api_reference_complete(self, quick_ref):
        """API reference covers main classes."""
        api = quick_ref["api_reference"]
        
        assert "SimpleSociety" in api
        assert "presets" in api
        assert "pabp" in api
    
    def test_message_types_documented(self, quick_ref):
        """All message types are documented."""
        message_types = quick_ref["message_types"]
        
        required_types = ["REQUEST", "RESPONSE", "INFORM", "PROPOSE", "ACCEPT", "REJECT"]
        for msg_type in required_types:
            assert msg_type in message_types
    
    def test_troubleshooting_guidance(self, quick_ref):
        """Common issues have solutions."""
        troubleshooting = quick_ref["troubleshooting"]
        
        assert len(troubleshooting) >= 3
        
        for issue, solution in troubleshooting.items():
            assert len(solution) > 0
