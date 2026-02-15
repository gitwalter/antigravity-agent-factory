"""
Event Store

Append-only storage for agent events with persistence support.
"""

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import json
import logging
import threading

from lib.society.events.schema import Agent, Action, AgentEvent, AxiomContext
from lib.society.events.chain import HashChain, ChainValidationResult

logger = logging.getLogger(__name__)


@dataclass
class EventQuery:
    """
    Query parameters for filtering events.

    Attributes:
        agent_id: Filter by agent ID.
        action_type: Filter by action type.
        since: Filter by timestamp (events after this time).
        until: Filter by timestamp (events before this time).
        limit: Maximum number of events to return.
        offset: Number of events to skip.
    """

    agent_id: Optional[str] = None
    action_type: Optional[str] = None
    since: Optional[datetime] = None
    until: Optional[datetime] = None
    limit: int = 100
    offset: int = 0


class EventStore:
    """
    Append-only event store with hash chain integrity.

    Features:
    - Immutable event storage
    - Hash chain for tamper detection
    - Optional persistence to JSON file
    - Query methods for event retrieval
    - Thread-safe operations

    Usage:
        store = EventStore()
        event = store.append(agent, action)
        is_valid, error = store.verify()
    """

    def __init__(
        self,
        storage_path: Optional[str] = None,
        signer: Optional[Any] = None,
    ):
        """
        Initialize event store.

        Args:
            storage_path: Optional path for JSON persistence.
            signer: Optional signing service for event signatures.
        """
        self.storage_path = Path(storage_path) if storage_path else None
        self.signer = signer
        self._events: List[AgentEvent] = []
        self._sequence = 0
        self._lock = threading.RLock()
        self._listeners: List[Callable[[AgentEvent], None]] = []

        if self.storage_path and self.storage_path.exists():
            self._load()

    @property
    def events(self) -> List[AgentEvent]:
        """Get all events (read-only copy)."""
        with self._lock:
            return list(self._events)

    @property
    def last_hash(self) -> str:
        """Get hash of the last event."""
        with self._lock:
            if self._events:
                return self._events[-1].hash
            return HashChain.GENESIS_HASH

    @property
    def count(self) -> int:
        """Get number of events in store."""
        with self._lock:
            return len(self._events)

    def append(
        self,
        agent: Agent,
        action: Action,
        axiom_context: Optional[AxiomContext] = None,
        verification_status: Optional[str] = None,
    ) -> AgentEvent:
        """
        Append a new event to the store.

        Args:
            agent: The agent performing the action.
            action: The action being performed.
            axiom_context: Optional axiom alignment declaration.
            verification_status: Optional initial verification status.

        Returns:
            The created event.
        """
        with self._lock:
            self._sequence += 1

            event = AgentEvent.create(
                agent=agent,
                action=action,
                sequence=self._sequence,
                previous_hash=self.last_hash,
                axiom_context=axiom_context,
                signer=self.signer,
            )

            if verification_status:
                event.verification_status = verification_status

            self._events.append(event)

            logger.debug(
                f"Appended event {event.event_id} (seq: {event.sequence}) "
                f"from agent {agent.id}"
            )

            # Persist if storage configured
            if self.storage_path:
                self._save()

            # Notify listeners
            for listener in self._listeners:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(f"Event listener error: {e}")

            return event

    def append_event(self, event: AgentEvent) -> None:
        """
        Append an existing event (for replication/import).

        Args:
            event: The event to append.

        Raises:
            ValueError: If event doesn't chain correctly.
        """
        with self._lock:
            # Verify chain link
            valid, error = HashChain.verify_chain_link(
                event, self._events[-1] if self._events else None
            )

            if not valid:
                raise ValueError(f"Invalid chain link: {error}")

            self._events.append(event)
            self._sequence = event.sequence

            if self.storage_path:
                self._save()

    def get(self, event_id: str) -> Optional[AgentEvent]:
        """
        Get event by ID.

        Args:
            event_id: The event ID to find.

        Returns:
            The event if found, None otherwise.
        """
        with self._lock:
            for event in self._events:
                if event.event_id == event_id:
                    return event
            return None

    def get_by_sequence(self, sequence: int) -> Optional[AgentEvent]:
        """
        Get event by sequence number.

        Args:
            sequence: The sequence number.

        Returns:
            The event if found, None otherwise.
        """
        with self._lock:
            if 1 <= sequence <= len(self._events):
                return self._events[sequence - 1]
            return None

    def query(self, query: EventQuery) -> List[AgentEvent]:
        """
        Query events with filters.

        Args:
            query: Query parameters.

        Returns:
            Matching events.
        """
        with self._lock:
            results = []

            for event in reversed(self._events):
                # Apply filters
                if query.agent_id and event.agent.id != query.agent_id:
                    continue
                if query.action_type and event.action.type.value != query.action_type:
                    continue
                if query.since and event.timestamp < query.since:
                    continue
                if query.until and event.timestamp > query.until:
                    continue

                results.append(event)

                if len(results) >= query.limit + query.offset:
                    break

            return results[query.offset : query.offset + query.limit]

    def get_agent_events(self, agent_id: str, limit: int = 100) -> List[AgentEvent]:
        """
        Get events for a specific agent.

        Args:
            agent_id: The agent ID.
            limit: Maximum events to return.

        Returns:
            Events for the agent.
        """
        return self.query(EventQuery(agent_id=agent_id, limit=limit))

    def get_recent(self, limit: int = 100) -> List[AgentEvent]:
        """
        Get most recent events.

        Args:
            limit: Maximum events to return.

        Returns:
            Recent events (newest first).
        """
        with self._lock:
            return list(reversed(self._events[-limit:]))

    def count_violations(
        self, agent_id: Optional[str] = None, window: timedelta = timedelta(hours=24)
    ) -> int:
        """
        Count violation events within time window.

        Args:
            agent_id: Optional agent ID filter.
            window: Time window to count.

        Returns:
            Number of violations.
        """
        cutoff = datetime.now(timezone.utc) - window
        count = 0

        with self._lock:
            for event in reversed(self._events):
                if event.timestamp < cutoff:
                    break
                if event.verification_status == "violation":
                    if agent_id is None or event.agent.id == agent_id:
                        count += 1

        return count

    def verify(self) -> ChainValidationResult:
        """
        Verify the integrity of the event chain.

        Returns:
            ChainValidationResult with validation status.
        """
        with self._lock:
            return HashChain.verify_chain(self._events)

    def update_verification_status(self, event_id: str, status: str) -> bool:
        """
        Update the verification status of an event.

        Note: This only updates metadata, not the event hash.

        Args:
            event_id: The event ID.
            status: New verification status.

        Returns:
            True if event was found and updated.
        """
        with self._lock:
            for event in self._events:
                if event.event_id == event_id:
                    event.verification_status = status
                    if self.storage_path:
                        self._save()
                    return True
            return False

    def add_listener(self, listener: Callable[[AgentEvent], None]) -> None:
        """
        Add event listener for new events.

        Args:
            listener: Callback function receiving new events.
        """
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[AgentEvent], None]) -> None:
        """
        Remove event listener.

        Args:
            listener: The listener to remove.
        """
        if listener in self._listeners:
            self._listeners.remove(listener)

    def export(self) -> Dict[str, Any]:
        """
        Export store data for serialization.

        Returns:
            Dictionary with sequence and events.
        """
        with self._lock:
            return {
                "sequence": self._sequence,
                "events": [e.to_dict() for e in self._events],
            }

    def _save(self) -> None:
        """Save events to storage file."""
        if not self.storage_path:
            return

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, "w") as f:
            json.dump(self.export(), f, indent=2)

    def _load(self) -> None:
        """Load events from storage file."""
        if not self.storage_path or not self.storage_path.exists():
            return

        with open(self.storage_path, "r") as f:
            data = json.load(f)

        self._sequence = data.get("sequence", 0)
        self._events = [AgentEvent.from_dict(e) for e in data.get("events", [])]
