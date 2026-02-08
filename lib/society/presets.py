"""
Pre-configured Society Presets for Common Scenarios.

This module provides ready-to-use society configurations for different
deployment scenarios and use cases.

Value Proposition:
- Zero-config for common scenarios
- Best practices built-in
- Easy upgrade path to custom configuration

SDG - Love - Truth - Beauty
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

from lib.society.simple import SimpleSociety, SocietyPreset, create_agent_society


class TrustTier(Enum):
    """Trust verification tiers from the Tiered Trust Architecture."""
    
    L0_LOCAL = "L0_local"          # Local cryptographic verification
    L1_ATTESTED = "L1_attested"    # Merkle root anchoring
    L2_CONTRACTED = "L2_contracted" # Smart contract enforcement
    L3_CONSENSUS = "L3_consensus"   # Multi-party consensus
    L4_ECONOMIC = "L4_economic"     # Stake-based trust


@dataclass
class PresetConfig:
    """Configuration for a society preset."""
    
    name: str
    description: str
    trust_tier: TrustTier
    axiom_verification: bool
    event_logging: bool
    reputation_tracking: bool
    contract_enforcement: bool
    blockchain_anchoring: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "trust_tier": self.trust_tier.value,
            "axiom_verification": self.axiom_verification,
            "event_logging": self.event_logging,
            "reputation_tracking": self.reputation_tracking,
            "contract_enforcement": self.contract_enforcement,
            "blockchain_anchoring": self.blockchain_anchoring
        }


# Pre-defined configurations
PRESETS = {
    SocietyPreset.DEVELOPMENT: PresetConfig(
        name="Development",
        description="Fast iteration with minimal overhead. Local verification only.",
        trust_tier=TrustTier.L0_LOCAL,
        axiom_verification=True,
        event_logging=True,
        reputation_tracking=True,
        contract_enforcement=False,
        blockchain_anchoring=False
    ),
    SocietyPreset.TESTING: PresetConfig(
        name="Testing",
        description="Speed-optimized for test suites. Minimal verification.",
        trust_tier=TrustTier.L0_LOCAL,
        axiom_verification=False,
        event_logging=False,
        reputation_tracking=False,
        contract_enforcement=False,
        blockchain_anchoring=False
    ),
    SocietyPreset.PRODUCTION: PresetConfig(
        name="Production",
        description="Full verification with audit trail. Ready for deployment.",
        trust_tier=TrustTier.L1_ATTESTED,
        axiom_verification=True,
        event_logging=True,
        reputation_tracking=True,
        contract_enforcement=True,
        blockchain_anchoring=True
    ),
    SocietyPreset.ENTERPRISE: PresetConfig(
        name="Enterprise",
        description="Maximum security with smart contract enforcement.",
        trust_tier=TrustTier.L2_CONTRACTED,
        axiom_verification=True,
        event_logging=True,
        reputation_tracking=True,
        contract_enforcement=True,
        blockchain_anchoring=True
    )
}


def get_preset_config(preset: SocietyPreset) -> PresetConfig:
    """
    Get the configuration for a preset.
    
    Args:
        preset: The SocietyPreset to get configuration for.
        
    Returns:
        PresetConfig with all settings for that preset.
    """
    return PRESETS.get(preset, PRESETS[SocietyPreset.DEVELOPMENT])


def list_presets() -> List[Dict]:
    """
    List all available presets with their configurations.
    
    Returns:
        List of preset configurations as dictionaries.
    """
    return [config.to_dict() for config in PRESETS.values()]


# Convenience functions for common patterns

def create_supervisor_worker_society(
    name: str,
    supervisor_id: str = "supervisor",
    worker_ids: Optional[List[str]] = None,
    preset: SocietyPreset = SocietyPreset.DEVELOPMENT
) -> SimpleSociety:
    """
    Create a supervisor-worker pattern society.
    
    This is the most common multi-agent pattern where a central supervisor
    delegates tasks to specialized workers.
    
    Args:
        name: Society name.
        supervisor_id: ID for the supervisor agent.
        worker_ids: List of worker agent IDs (defaults to ["worker_1", "worker_2"]).
        preset: Society configuration preset.
        
    Returns:
        SimpleSociety configured for supervisor-worker pattern.
        
    Example:
        society = create_supervisor_worker_society(
            "CodeAnalysis",
            supervisor_id="orchestrator",
            worker_ids=["syntax_checker", "style_checker", "security_checker"]
        )
    """
    workers = worker_ids or ["worker_1", "worker_2"]
    all_agents = [supervisor_id] + workers
    
    society = create_agent_society(name, all_agents, preset)
    
    # Add supervisor with supervisor type
    society._bridges[supervisor_id]._agent_type = "supervisor"
    
    # Add workers with executor type
    for worker_id in workers:
        society._bridges[worker_id]._agent_type = "executor"
    
    return society


def create_peer_society(
    name: str,
    peer_ids: List[str],
    preset: SocietyPreset = SocietyPreset.DEVELOPMENT
) -> SimpleSociety:
    """
    Create a peer-to-peer collaborative society.
    
    All agents have equal authority and communicate through consensus.
    
    Args:
        name: Society name.
        peer_ids: List of peer agent IDs.
        preset: Society configuration preset.
        
    Returns:
        SimpleSociety configured for peer collaboration.
        
    Example:
        society = create_peer_society(
            "ReviewBoard",
            peer_ids=["reviewer_1", "reviewer_2", "reviewer_3"]
        )
    """
    society = create_agent_society(name, peer_ids, preset)
    
    # Set all as peer type
    for peer_id in peer_ids:
        society._bridges[peer_id]._agent_type = "peer"
    
    return society


def create_pipeline_society(
    name: str,
    stage_ids: List[str],
    preset: SocietyPreset = SocietyPreset.DEVELOPMENT
) -> SimpleSociety:
    """
    Create a sequential pipeline society.
    
    Agents process in sequence, each building on the previous output.
    
    Args:
        name: Society name.
        stage_ids: Ordered list of stage agent IDs.
        preset: Society configuration preset.
        
    Returns:
        SimpleSociety configured for pipeline processing.
        
    Example:
        society = create_pipeline_society(
            "DataPipeline",
            stage_ids=["extractor", "transformer", "loader"]
        )
    """
    society = create_agent_society(name, stage_ids, preset)
    
    # Set stage types based on position
    for i, stage_id in enumerate(stage_ids):
        if i == 0:
            society._bridges[stage_id]._agent_type = "pipeline_source"
        elif i == len(stage_ids) - 1:
            society._bridges[stage_id]._agent_type = "pipeline_sink"
        else:
            society._bridges[stage_id]._agent_type = "pipeline_stage"
    
    return society


def create_hierarchical_society(
    name: str,
    hierarchy: Dict[str, List[str]],
    preset: SocietyPreset = SocietyPreset.DEVELOPMENT
) -> SimpleSociety:
    """
    Create a hierarchical society with team leads and specialists.
    
    Args:
        name: Society name.
        hierarchy: Dictionary mapping manager IDs to their report IDs.
        preset: Society configuration preset.
        
    Returns:
        SimpleSociety configured for hierarchical coordination.
        
    Example:
        society = create_hierarchical_society(
            "EngineeringOrg",
            hierarchy={
                "cto": ["backend_lead", "frontend_lead"],
                "backend_lead": ["api_dev", "db_dev"],
                "frontend_lead": ["ui_dev", "ux_dev"]
            }
        )
    """
    # Collect all agents
    all_agents = set()
    for manager, reports in hierarchy.items():
        all_agents.add(manager)
        all_agents.update(reports)
    
    society = create_agent_society(name, list(all_agents), preset)
    
    # Set types based on hierarchy position
    all_reports = set()
    for reports in hierarchy.values():
        all_reports.update(reports)
    
    for agent_id in all_agents:
        if agent_id in hierarchy:
            # This agent manages others
            if agent_id not in all_reports:
                society._bridges[agent_id]._agent_type = "executive"
            else:
                society._bridges[agent_id]._agent_type = "manager"
        else:
            society._bridges[agent_id]._agent_type = "specialist"
    
    return society


# Factory for custom configurations

class SocietyBuilder:
    """
    Builder pattern for creating custom society configurations.
    
    Use this when presets don't fit your needs.
    
    Example:
        society = (SocietyBuilder("CustomProject")
            .with_trust_tier(TrustTier.L1_ATTESTED)
            .with_axiom_verification(True)
            .with_agents(["agent1", "agent2"])
            .build())
    """
    
    def __init__(self, name: str):
        """Initialize the builder with a society name."""
        self._name = name
        self._preset = SocietyPreset.DEVELOPMENT
        self._agents: List[str] = []
        self._config_overrides: Dict = {}
    
    def with_preset(self, preset: SocietyPreset) -> "SocietyBuilder":
        """Start from a preset configuration."""
        self._preset = preset
        return self
    
    def with_trust_tier(self, tier: TrustTier) -> "SocietyBuilder":
        """Set the trust verification tier."""
        self._config_overrides["trust_tier"] = tier
        return self
    
    def with_axiom_verification(self, enabled: bool) -> "SocietyBuilder":
        """Enable or disable axiom verification."""
        self._config_overrides["axiom_verification"] = enabled
        return self
    
    def with_blockchain_anchoring(self, enabled: bool) -> "SocietyBuilder":
        """Enable or disable blockchain anchoring."""
        self._config_overrides["blockchain_anchoring"] = enabled
        return self
    
    def with_contract_enforcement(self, enabled: bool) -> "SocietyBuilder":
        """Enable or disable contract enforcement."""
        self._config_overrides["contract_enforcement"] = enabled
        return self
    
    def with_agents(self, agent_ids: List[str]) -> "SocietyBuilder":
        """Add agents to the society."""
        self._agents.extend(agent_ids)
        return self
    
    def build(self) -> SimpleSociety:
        """Build and return the configured society."""
        society = create_agent_society(self._name, self._agents, self._preset)
        # Note: Config overrides would be applied to context here
        # For now, the preset determines base behavior
        return society
