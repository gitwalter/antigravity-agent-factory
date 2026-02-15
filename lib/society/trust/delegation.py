"""
Trust Delegation

Trust graph and delegation mechanisms for agent relationships.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


@dataclass
class TrustDelegation:
    """
    Trust delegation from one agent to another.

    Attributes:
        delegator: Agent granting trust.
        delegate: Agent receiving trust.
        trust_level: Level of trust (0.0 to 1.0).
        scope: Optional scope/capability restrictions.
        expires: Optional expiration time.
        created: When delegation was created.
    """

    delegator: str
    delegate: str
    trust_level: float
    scope: List[str] = field(default_factory=list)
    expires: Optional[datetime] = None
    created: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_valid(self) -> bool:
        """Check if delegation is still valid."""
        if self.expires and datetime.now(timezone.utc) > self.expires:
            return False
        return self.trust_level > 0

    def covers_scope(self, action: str) -> bool:
        """Check if delegation covers a specific action."""
        if not self.scope:
            return True  # No restrictions = full scope
        return action in self.scope or "*" in self.scope

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "delegator": self.delegator,
            "delegate": self.delegate,
            "trust_level": self.trust_level,
            "scope": self.scope,
            "created": self.created.isoformat(),
        }
        if self.expires:
            result["expires"] = self.expires.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrustDelegation":
        """Create from dictionary."""
        return cls(
            delegator=data["delegator"],
            delegate=data["delegate"],
            trust_level=data["trust_level"],
            scope=data.get("scope", []),
            expires=datetime.fromisoformat(data["expires"])
            if data.get("expires")
            else None,
            created=datetime.fromisoformat(data["created"])
            if "created" in data
            else datetime.now(timezone.utc),
        )


class TrustGraph:
    """
    Manages trust relationships between agents.

    Features:
    - Direct trust delegation
    - Transitive trust computation
    - Trust path analysis
    - Scope-based restrictions

    Usage:
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.8)
        graph.delegate_trust("bob", "charlie", 0.9)

        # Get transitive trust (alice -> charlie via bob)
        trust = graph.get_effective_trust("alice", "charlie")
    """

    # Maximum depth for transitive trust
    MAX_TRUST_DEPTH = 5

    # Decay factor for each hop
    TRANSITIVE_DECAY = 0.9

    def __init__(self):
        """Initialize trust graph."""
        # delegator -> delegate -> TrustDelegation
        self._delegations: Dict[str, Dict[str, TrustDelegation]] = {}

    def delegate_trust(
        self,
        delegator: str,
        delegate: str,
        trust_level: float,
        scope: Optional[List[str]] = None,
        duration: Optional[timedelta] = None,
    ) -> TrustDelegation:
        """
        Create or update a trust delegation.

        Args:
            delegator: Agent granting trust.
            delegate: Agent receiving trust.
            trust_level: Level of trust (0.0 to 1.0).
            scope: Optional scope restrictions.
            duration: Optional duration before expiry.

        Returns:
            The created TrustDelegation.
        """
        if delegator not in self._delegations:
            self._delegations[delegator] = {}

        expires = None
        if duration:
            expires = datetime.now(timezone.utc) + duration

        delegation = TrustDelegation(
            delegator=delegator,
            delegate=delegate,
            trust_level=min(1.0, max(0.0, trust_level)),
            scope=scope or [],
            expires=expires,
        )

        self._delegations[delegator][delegate] = delegation

        logger.info(
            f"Trust delegation: {delegator} -> {delegate} "
            f"(level: {trust_level:.2f}, scope: {scope or 'all'})"
        )

        return delegation

    def revoke_trust(self, delegator: str, delegate: str) -> bool:
        """
        Revoke a trust delegation.

        Args:
            delegator: Agent who granted trust.
            delegate: Agent whose trust is revoked.

        Returns:
            True if delegation was found and revoked.
        """
        if delegator in self._delegations:
            if delegate in self._delegations[delegator]:
                del self._delegations[delegator][delegate]
                logger.info(f"Trust revoked: {delegator} -> {delegate}")
                return True
        return False

    def get_delegation(
        self, delegator: str, delegate: str
    ) -> Optional[TrustDelegation]:
        """Get a specific trust delegation."""
        if delegator in self._delegations:
            return self._delegations[delegator].get(delegate)
        return None

    def get_direct_trust(self, delegator: str, delegate: str) -> float:
        """Get direct trust level between two agents."""
        delegation = self.get_delegation(delegator, delegate)
        if delegation and delegation.is_valid:
            return delegation.trust_level
        return 0.0

    def get_effective_trust(
        self, source: str, target: str, action: Optional[str] = None
    ) -> float:
        """
        Get effective trust level considering transitive trust.

        Args:
            source: Source agent.
            target: Target agent.
            action: Optional action to check scope for.

        Returns:
            Effective trust level (0.0 to 1.0).
        """
        if source == target:
            return 1.0

        # BFS to find best trust path
        visited: Set[str] = {source}
        queue: List[tuple] = [(source, 1.0, 0)]  # (current, trust, depth)
        best_trust = 0.0

        while queue:
            current, accumulated_trust, depth = queue.pop(0)

            if depth >= self.MAX_TRUST_DEPTH:
                continue

            delegates = self._delegations.get(current, {})

            for delegate, delegation in delegates.items():
                if not delegation.is_valid:
                    continue

                # Check scope if action specified
                if action and not delegation.covers_scope(action):
                    continue

                # Calculate trust at this hop
                hop_trust = delegation.trust_level * self.TRANSITIVE_DECAY**depth
                path_trust = accumulated_trust * hop_trust

                if delegate == target:
                    best_trust = max(best_trust, path_trust)
                elif delegate not in visited:
                    visited.add(delegate)
                    queue.append((delegate, path_trust, depth + 1))

        return best_trust

    def find_trust_path(self, source: str, target: str) -> Optional[List[str]]:
        """
        Find the best trust path between agents.

        Args:
            source: Source agent.
            target: Target agent.

        Returns:
            List of agents in the path, or None if no path.
        """
        if source == target:
            return [source]

        visited: Set[str] = {source}
        queue: List[tuple] = [(source, [source], 1.0)]
        best_path = None
        best_trust = 0.0

        while queue:
            current, path, trust = queue.pop(0)

            if len(path) > self.MAX_TRUST_DEPTH + 1:
                continue

            delegates = self._delegations.get(current, {})

            for delegate, delegation in delegates.items():
                if not delegation.is_valid:
                    continue

                new_path = path + [delegate]
                new_trust = trust * delegation.trust_level * self.TRANSITIVE_DECAY

                if delegate == target:
                    if new_trust > best_trust:
                        best_trust = new_trust
                        best_path = new_path
                elif delegate not in visited:
                    visited.add(delegate)
                    queue.append((delegate, new_path, new_trust))

        return best_path

    def get_delegates(self, agent: str) -> List[TrustDelegation]:
        """Get all agents that an agent has delegated trust to."""
        if agent not in self._delegations:
            return []

        return [d for d in self._delegations[agent].values() if d.is_valid]

    def get_delegators(self, agent: str) -> List[TrustDelegation]:
        """Get all agents that have delegated trust to this agent."""
        delegators = []

        for delegator, delegates in self._delegations.items():
            if agent in delegates:
                delegation = delegates[agent]
                if delegation.is_valid:
                    delegators.append(delegation)

        return delegators

    def get_trust_network(self, agent: str, depth: int = 2) -> Dict[str, Any]:
        """
        Get the trust network around an agent.

        Args:
            agent: Central agent.
            depth: How many hops to include.

        Returns:
            Network structure with nodes and edges.
        """
        nodes = {agent}
        edges = []

        to_visit = [(agent, 0)]
        visited = set()

        while to_visit:
            current, current_depth = to_visit.pop(0)
            if current in visited or current_depth > depth:
                continue
            visited.add(current)

            # Outgoing trust
            for delegation in self.get_delegates(current):
                nodes.add(delegation.delegate)
                edges.append(
                    {
                        "from": current,
                        "to": delegation.delegate,
                        "trust": delegation.trust_level,
                        "direction": "outgoing",
                    }
                )
                if current_depth < depth:
                    to_visit.append((delegation.delegate, current_depth + 1))

            # Incoming trust
            for delegation in self.get_delegators(current):
                nodes.add(delegation.delegator)
                edges.append(
                    {
                        "from": delegation.delegator,
                        "to": current,
                        "trust": delegation.trust_level,
                        "direction": "incoming",
                    }
                )
                if current_depth < depth:
                    to_visit.append((delegation.delegator, current_depth + 1))

        return {
            "center": agent,
            "nodes": list(nodes),
            "edges": edges,
        }

    def cleanup_expired(self) -> int:
        """Remove expired delegations."""
        removed = 0
        now = datetime.now(timezone.utc)

        for delegator in list(self._delegations.keys()):
            delegates = self._delegations[delegator]
            expired = [
                d
                for d, delegation in delegates.items()
                if delegation.expires and delegation.expires < now
            ]

            for delegate in expired:
                del delegates[delegate]
                removed += 1

            if not delegates:
                del self._delegations[delegator]

        if removed:
            logger.info(f"Cleaned up {removed} expired trust delegations")

        return removed

    def export(self) -> Dict[str, Any]:
        """Export trust graph data."""
        return {
            delegator: {
                delegate: delegation.to_dict()
                for delegate, delegation in delegates.items()
            }
            for delegator, delegates in self._delegations.items()
        }
