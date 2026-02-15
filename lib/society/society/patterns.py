"""
Society Organizational Patterns

Templates for different society structures with axiom-aligned governance.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class GovernanceModel(Enum):
    """Available governance models."""

    FLAT_DEMOCRACY = "flat_democracy"
    MERITOCRACY = "meritocracy"
    HIERARCHY = "hierarchy"
    FEDERATION = "federation"
    DAO = "dao"


class DecisionType(Enum):
    """Types of decisions in the society."""

    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    CONSTITUTIONAL = "constitutional"
    EMERGENCY = "emergency"


@dataclass
class Role:
    """
    Role within a society.

    Attributes:
        name: Role identifier.
        capabilities: What this role can do.
        responsibilities: What this role must do.
        trust_required: Minimum trust level required.
    """

    name: str
    capabilities: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    trust_required: float = 0.5

    def has_capability(self, capability: str) -> bool:
        """Check if role has a capability."""
        return capability in self.capabilities or "*" in self.capabilities

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "responsibilities": self.responsibilities,
            "trust_required": self.trust_required,
        }


@dataclass
class Proposal:
    """
    Proposal for society decision.

    Attributes:
        id: Unique proposal identifier.
        proposer: Agent who created the proposal.
        type: Type of decision.
        description: What is being proposed.
        created: When proposal was created.
        votes: Votes cast (agent_id -> vote).
        status: Current status.
    """

    id: str
    proposer: str
    type: DecisionType
    description: str
    created: datetime = field(default_factory=datetime.utcnow)
    votes: Dict[str, bool] = field(default_factory=dict)
    status: str = "open"

    @property
    def vote_count(self) -> tuple:
        """Get (yes, no) vote counts."""
        yes_votes = sum(1 for v in self.votes.values() if v)
        no_votes = sum(1 for v in self.votes.values() if not v)
        return (yes_votes, no_votes)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "proposer": self.proposer,
            "type": self.type.value,
            "description": self.description,
            "created": self.created.isoformat(),
            "votes": self.votes,
            "status": self.status,
            "vote_count": self.vote_count,
        }


class SocietyPattern(ABC):
    """
    Abstract base class for society patterns.

    Defines the governance structure and decision-making
    rules for a multi-agent society.
    """

    def __init__(self, name: str = "Society"):
        """Initialize society."""
        self.name = name
        self._members: Set[str] = set()
        self._roles: Dict[str, Role] = {}
        self._member_roles: Dict[str, Set[str]] = {}
        self._proposals: Dict[str, Proposal] = {}

    @property
    @abstractmethod
    def governance_model(self) -> GovernanceModel:
        """Get the governance model type."""
        pass

    @abstractmethod
    def can_vote(self, agent_id: str, proposal: Proposal) -> bool:
        """Check if an agent can vote on a proposal."""
        pass

    @abstractmethod
    def evaluate_proposal(self, proposal: Proposal) -> bool:
        """Evaluate if a proposal passes."""
        pass

    @abstractmethod
    def get_voting_weight(self, agent_id: str) -> float:
        """Get voting weight for an agent."""
        pass

    def add_member(self, agent_id: str) -> None:
        """Add a member to the society."""
        self._members.add(agent_id)
        self._member_roles[agent_id] = set()
        logger.info(f"Added member {agent_id} to {self.name}")

    def remove_member(self, agent_id: str) -> None:
        """Remove a member from the society."""
        self._members.discard(agent_id)
        self._member_roles.pop(agent_id, None)
        logger.info(f"Removed member {agent_id} from {self.name}")

    def define_role(self, role: Role) -> None:
        """Define a role in the society."""
        self._roles[role.name] = role

    def assign_role(self, agent_id: str, role_name: str) -> bool:
        """Assign a role to a member."""
        if agent_id not in self._members:
            return False
        if role_name not in self._roles:
            return False

        if agent_id not in self._member_roles:
            self._member_roles[agent_id] = set()

        self._member_roles[agent_id].add(role_name)
        logger.info(f"Assigned role {role_name} to {agent_id}")
        return True

    def get_member_roles(self, agent_id: str) -> List[Role]:
        """Get roles assigned to a member."""
        role_names = self._member_roles.get(agent_id, set())
        return [self._roles[name] for name in role_names if name in self._roles]

    def has_capability(self, agent_id: str, capability: str) -> bool:
        """Check if agent has a capability through their roles."""
        for role in self.get_member_roles(agent_id):
            if role.has_capability(capability):
                return True
        return False

    def create_proposal(
        self, proposer: str, decision_type: DecisionType, description: str
    ) -> Optional[Proposal]:
        """Create a new proposal."""
        if proposer not in self._members:
            return None

        proposal_id = f"proposal-{len(self._proposals) + 1}"
        proposal = Proposal(
            id=proposal_id,
            proposer=proposer,
            type=decision_type,
            description=description,
        )

        self._proposals[proposal_id] = proposal
        logger.info(f"Proposal created: {proposal_id} by {proposer}")
        return proposal

    def vote(self, proposal_id: str, agent_id: str, in_favor: bool) -> bool:
        """Cast a vote on a proposal."""
        proposal = self._proposals.get(proposal_id)
        if not proposal or proposal.status != "open":
            return False

        if not self.can_vote(agent_id, proposal):
            return False

        proposal.votes[agent_id] = in_favor
        logger.info(
            f"Vote cast: {agent_id} voted {'yes' if in_favor else 'no'} on {proposal_id}"
        )
        return True

    def finalize_proposal(self, proposal_id: str) -> Optional[bool]:
        """Finalize a proposal and return result."""
        proposal = self._proposals.get(proposal_id)
        if not proposal or proposal.status != "open":
            return None

        passed = self.evaluate_proposal(proposal)
        proposal.status = "passed" if passed else "rejected"

        logger.info(f"Proposal {proposal_id} {proposal.status}")
        return passed

    def get_info(self) -> Dict[str, Any]:
        """Get society information."""
        return {
            "name": self.name,
            "governance_model": self.governance_model.value,
            "member_count": len(self._members),
            "roles": [r.to_dict() for r in self._roles.values()],
            "open_proposals": len(
                [p for p in self._proposals.values() if p.status == "open"]
            ),
        }


class FlatDemocracy(SocietyPattern):
    """
    Flat democracy with equal voting rights.

    - Every member has equal vote (1 agent = 1 vote)
    - Simple majority decides
    - All members can propose and vote

    Axiom alignment:
    - A1 Love: Equal consideration for all members
    - A2 Truth: Transparent voting process
    """

    @property
    def governance_model(self) -> GovernanceModel:
        return GovernanceModel.FLAT_DEMOCRACY

    def can_vote(self, agent_id: str, proposal: Proposal) -> bool:
        """All members can vote."""
        return agent_id in self._members

    def evaluate_proposal(self, proposal: Proposal) -> bool:
        """Simple majority wins."""
        yes_votes, no_votes = proposal.vote_count
        return yes_votes > no_votes

    def get_voting_weight(self, agent_id: str) -> float:
        """Equal weight for all members."""
        return 1.0 if agent_id in self._members else 0.0


class Meritocracy(SocietyPattern):
    """
    Merit-based society with reputation-weighted voting.

    - Voting power proportional to reputation
    - Higher trust = more influence
    - Proven competence rewarded

    Axiom alignment:
    - A0 SDG: Rewards sustainable contributions
    - A3 Beauty: Elegance in competence recognition
    """

    def __init__(self, name: str = "Meritocracy", reputation_system=None):
        """Initialize with optional reputation system."""
        super().__init__(name)
        self.reputation_system = reputation_system

    @property
    def governance_model(self) -> GovernanceModel:
        return GovernanceModel.MERITOCRACY

    def can_vote(self, agent_id: str, proposal: Proposal) -> bool:
        """Members with positive reputation can vote."""
        if agent_id not in self._members:
            return False

        if self.reputation_system:
            score = self.reputation_system.get_score(agent_id)
            return score.current_score >= 30.0

        return True

    def evaluate_proposal(self, proposal: Proposal) -> bool:
        """Weighted majority wins."""
        yes_weight = 0.0
        no_weight = 0.0

        for agent_id, in_favor in proposal.votes.items():
            weight = self.get_voting_weight(agent_id)
            if in_favor:
                yes_weight += weight
            else:
                no_weight += weight

        return yes_weight > no_weight

    def get_voting_weight(self, agent_id: str) -> float:
        """Weight based on reputation score."""
        if agent_id not in self._members:
            return 0.0

        if self.reputation_system:
            score = self.reputation_system.get_score(agent_id)
            return score.current_score / 100.0

        return 1.0


class Hierarchy(SocietyPattern):
    """
    Hierarchical society with role-based authority.

    - Clear chain of command
    - Decisions flow down from leadership
    - Role requirements for voting

    Axiom alignment:
    - A4 Guardian: Clear escalation paths
    - A2 Truth: Transparent authority structure
    """

    LEADER_ROLE = "leader"
    MANAGER_ROLE = "manager"
    MEMBER_ROLE = "member"

    def __init__(self, name: str = "Hierarchy"):
        """Initialize with default hierarchy roles."""
        super().__init__(name)

        # Define default hierarchical roles
        self.define_role(
            Role(
                name=self.LEADER_ROLE,
                capabilities=["*"],
                responsibilities=["final_decisions", "strategic_planning"],
                trust_required=0.9,
            )
        )

        self.define_role(
            Role(
                name=self.MANAGER_ROLE,
                capabilities=["operational_decisions", "team_management"],
                responsibilities=["team_coordination", "reporting"],
                trust_required=0.7,
            )
        )

        self.define_role(
            Role(
                name=self.MEMBER_ROLE,
                capabilities=["execute_tasks", "propose_ideas"],
                responsibilities=["task_completion"],
                trust_required=0.5,
            )
        )

    @property
    def governance_model(self) -> GovernanceModel:
        return GovernanceModel.HIERARCHY

    def can_vote(self, agent_id: str, proposal: Proposal) -> bool:
        """Only relevant roles can vote based on decision type."""
        if agent_id not in self._members:
            return False

        roles = self._member_roles.get(agent_id, set())

        # Constitutional: only leaders
        if proposal.type == DecisionType.CONSTITUTIONAL:
            return self.LEADER_ROLE in roles

        # Strategic: leaders and managers
        if proposal.type == DecisionType.STRATEGIC:
            return self.LEADER_ROLE in roles or self.MANAGER_ROLE in roles

        # Operational: managers and members
        if proposal.type == DecisionType.OPERATIONAL:
            return len(roles) > 0

        # Emergency: anyone
        return True

    def evaluate_proposal(self, proposal: Proposal) -> bool:
        """Leader vote has final say, otherwise majority."""
        for agent_id, in_favor in proposal.votes.items():
            roles = self._member_roles.get(agent_id, set())
            if self.LEADER_ROLE in roles:
                return in_favor

        # No leader vote - use majority
        yes_votes, no_votes = proposal.vote_count
        return yes_votes > no_votes

    def get_voting_weight(self, agent_id: str) -> float:
        """Weight based on role."""
        if agent_id not in self._members:
            return 0.0

        roles = self._member_roles.get(agent_id, set())

        if self.LEADER_ROLE in roles:
            return 10.0
        if self.MANAGER_ROLE in roles:
            return 3.0
        if self.MEMBER_ROLE in roles:
            return 1.0

        return 0.5


class Federation(SocietyPattern):
    """
    Federation of semi-autonomous sub-societies.

    - Multiple sub-groups with local autonomy
    - Representative voting for cross-group decisions
    - Subsidiarity principle

    Axiom alignment:
    - A0 SDG: Sustainable local governance
    - A1 Love: Respect for group autonomy
    """

    def __init__(self, name: str = "Federation"):
        """Initialize federation."""
        super().__init__(name)
        self._sub_societies: Dict[str, Set[str]] = {}
        self._representatives: Dict[str, str] = {}  # group -> representative

    @property
    def governance_model(self) -> GovernanceModel:
        return GovernanceModel.FEDERATION

    def create_sub_society(self, group_name: str) -> None:
        """Create a sub-society."""
        self._sub_societies[group_name] = set()
        logger.info(f"Created sub-society: {group_name}")

    def add_to_sub_society(self, agent_id: str, group_name: str) -> bool:
        """Add member to a sub-society."""
        if group_name not in self._sub_societies:
            return False
        if agent_id not in self._members:
            return False

        self._sub_societies[group_name].add(agent_id)
        return True

    def set_representative(self, group_name: str, agent_id: str) -> bool:
        """Set representative for a sub-society."""
        if group_name not in self._sub_societies:
            return False
        if agent_id not in self._sub_societies[group_name]:
            return False

        self._representatives[group_name] = agent_id
        logger.info(f"Set {agent_id} as representative for {group_name}")
        return True

    def get_member_group(self, agent_id: str) -> Optional[str]:
        """Get which sub-society a member belongs to."""
        for group_name, members in self._sub_societies.items():
            if agent_id in members:
                return group_name
        return None

    def can_vote(self, agent_id: str, proposal: Proposal) -> bool:
        """Representatives vote on federation matters."""
        if agent_id not in self._members:
            return False

        # Constitutional: only representatives
        if proposal.type in [DecisionType.CONSTITUTIONAL, DecisionType.STRATEGIC]:
            return agent_id in self._representatives.values()

        # Operational: all members
        return True

    def evaluate_proposal(self, proposal: Proposal) -> bool:
        """Each sub-society gets one vote via representative."""
        group_votes: Dict[str, bool] = {}

        for agent_id, in_favor in proposal.votes.items():
            # Find which group this agent represents
            for group, rep in self._representatives.items():
                if rep == agent_id:
                    group_votes[group] = in_favor
                    break

        yes_votes = sum(1 for v in group_votes.values() if v)
        no_votes = sum(1 for v in group_votes.values() if not v)

        return yes_votes > no_votes

    def get_voting_weight(self, agent_id: str) -> float:
        """Representatives have weight, others have voice."""
        if agent_id in self._representatives.values():
            return 1.0
        if agent_id in self._members:
            return 0.1
        return 0.0


class DAOSociety(SocietyPattern):
    """
    Decentralized Autonomous Organization style governance.

    - Token/stake-based voting
    - Smart contract-like proposals
    - Quorum requirements

    Axiom alignment:
    - A2 Truth: Immutable, transparent governance
    - A4 Guardian: Automated rule enforcement
    """

    DEFAULT_QUORUM = 0.5  # 50% participation required

    def __init__(self, name: str = "DAO"):
        """Initialize DAO."""
        super().__init__(name)
        self._stakes: Dict[str, float] = {}
        self.quorum = self.DEFAULT_QUORUM

    @property
    def governance_model(self) -> GovernanceModel:
        return GovernanceModel.DAO

    def set_stake(self, agent_id: str, stake: float) -> None:
        """Set stake for an agent."""
        if agent_id in self._members:
            self._stakes[agent_id] = max(0.0, stake)

    def get_stake(self, agent_id: str) -> float:
        """Get agent's stake."""
        return self._stakes.get(agent_id, 0.0)

    @property
    def total_stake(self) -> float:
        """Get total staked amount."""
        return sum(self._stakes.values())

    def can_vote(self, agent_id: str, proposal: Proposal) -> bool:
        """Agents with stake can vote."""
        if agent_id not in self._members:
            return False
        return self.get_stake(agent_id) > 0

    def evaluate_proposal(self, proposal: Proposal) -> bool:
        """Stake-weighted voting with quorum requirement."""
        total = self.total_stake
        if total == 0:
            return False

        voted_stake = sum(
            self.get_stake(agent_id) for agent_id in proposal.votes.keys()
        )

        # Check quorum
        if voted_stake / total < self.quorum:
            logger.info(f"Proposal {proposal.id} did not reach quorum")
            return False

        yes_stake = sum(
            self.get_stake(agent_id)
            for agent_id, in_favor in proposal.votes.items()
            if in_favor
        )

        return yes_stake > (voted_stake / 2)

    def get_voting_weight(self, agent_id: str) -> float:
        """Weight is proportional to stake."""
        total = self.total_stake
        if total == 0:
            return 0.0
        return self.get_stake(agent_id) / total


def create_society(
    governance_model: GovernanceModel, name: str = "Society", **kwargs
) -> SocietyPattern:
    """
    Factory function to create society patterns.

    Args:
        governance_model: Type of governance.
        name: Society name.
        **kwargs: Additional parameters for specific patterns.

    Returns:
        Configured SocietyPattern instance.
    """
    patterns = {
        GovernanceModel.FLAT_DEMOCRACY: FlatDemocracy,
        GovernanceModel.MERITOCRACY: Meritocracy,
        GovernanceModel.HIERARCHY: Hierarchy,
        GovernanceModel.FEDERATION: Federation,
        GovernanceModel.DAO: DAOSociety,
    }

    pattern_class = patterns.get(governance_model)
    if not pattern_class:
        raise ValueError(f"Unknown governance model: {governance_model}")

    return pattern_class(name=name, **kwargs)
