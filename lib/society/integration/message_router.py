"""
Message Router

Routes verified messages between agents in the society.

Provides:
- Agent registration and discovery
- Message routing with verification
- Broadcast messaging to multiple agents
- Message queue management
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from lib.society.integration.context import SocietyContext

import logging
import uuid

from lib.society.events import AgentEvent, ActionType
from lib.society.integration.agent_bridge import AgentSocietyBridge

logger = logging.getLogger(__name__)


class RouteStatus(Enum):
    """Status of a routed message."""

    DELIVERED = "delivered"
    QUEUED = "queued"
    FAILED = "failed"
    NO_RECIPIENT = "no_recipient"
    VERIFICATION_FAILED = "verification_failed"


@dataclass
class RoutedMessage:
    """
    A message that has been routed through the system.

    Attributes:
        message_id: Unique message identifier.
        event: The underlying AgentEvent.
        sender: Sender agent ID.
        recipient: Recipient agent ID (or "broadcast").
        status: Delivery status.
        delivered_at: When message was delivered.
        error: Error message if failed.
    """

    message_id: str
    event: AgentEvent
    sender: str
    recipient: str
    status: RouteStatus
    delivered_at: Optional[datetime] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "event_id": self.event.event_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "status": self.status.value,
            "delivered_at": self.delivered_at.isoformat()
            if self.delivered_at
            else None,
            "error": self.error,
        }


class MessageRouter:
    """
    Routes messages between verified agents.

    Features:
    - Register/unregister agent bridges
    - Route messages to specific agents
    - Broadcast messages to all agents
    - Message queue for offline agents
    - Delivery confirmation

    Usage:
        # Create router with shared context
        router = MessageRouter(context)

        # Register agents
        router.register(bridge_a)
        router.register(bridge_b)

        # Route happens automatically when bridges send messages
        # Or manually route an event:
        result = router.route(event)

    SDG - Love - Truth - Beauty
    """

    def __init__(self, context: "SocietyContext"):
        """
        Initialize message router.

        Args:
            context: Shared society context.
        """
        self.context = context

        # Registered bridges
        self._bridges: Dict[str, AgentSocietyBridge] = {}

        # Message queues for offline agents
        self._queues: Dict[str, List[RoutedMessage]] = {}

        # Message history
        self._history: List[RoutedMessage] = []
        self._max_history = 1000

        # Delivery handlers
        self._delivery_handlers: List[Callable[[RoutedMessage], None]] = []

        # Subscribe to context events
        self.context.add_message_listener(self._on_message_event)

        logger.info("Message router initialized")

    def register(self, bridge: AgentSocietyBridge) -> None:
        """
        Register an agent bridge with the router.

        Args:
            bridge: The agent's bridge to register.
        """
        self._bridges[bridge.agent_id] = bridge

        # Deliver any queued messages
        if bridge.agent_id in self._queues:
            queued = self._queues.pop(bridge.agent_id)
            for msg in queued:
                self._deliver(msg, bridge)
            logger.info(f"Delivered {len(queued)} queued messages to {bridge.agent_id}")

        logger.debug(f"Agent registered with router: {bridge.agent_id}")

    def unregister(self, agent_id: str) -> None:
        """
        Unregister an agent from the router.

        Args:
            agent_id: The agent ID to unregister.
        """
        if agent_id in self._bridges:
            del self._bridges[agent_id]
            logger.debug(f"Agent unregistered from router: {agent_id}")

    def is_registered(self, agent_id: str) -> bool:
        """Check if an agent is registered."""
        return agent_id in self._bridges

    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent IDs."""
        return list(self._bridges.keys())

    def _on_message_event(self, event: AgentEvent) -> None:
        """Handle message events from the context."""
        if event.action.type != ActionType.MESSAGE:
            return

        # Route the message
        self.route(event)

    def route(self, event: AgentEvent) -> RoutedMessage:
        """
        Route an event to its target.

        Args:
            event: The event to route.

        Returns:
            RoutedMessage with delivery status.
        """
        sender = event.agent.id
        target = event.action.target

        if not target:
            return self._create_failed_message(
                event, sender, "unknown", "No target specified"
            )

        message_id = str(uuid.uuid4())

        # Check if target is registered
        if target not in self._bridges:
            # Queue for later delivery
            routed_msg = RoutedMessage(
                message_id=message_id,
                event=event,
                sender=sender,
                recipient=target,
                status=RouteStatus.QUEUED,
            )

            if target not in self._queues:
                self._queues[target] = []
            self._queues[target].append(routed_msg)

            logger.debug(f"Message queued for offline agent: {target}")
            self._add_to_history(routed_msg)
            return routed_msg

        # Deliver immediately
        bridge = self._bridges[target]
        routed_msg = RoutedMessage(
            message_id=message_id,
            event=event,
            sender=sender,
            recipient=target,
            status=RouteStatus.DELIVERED,
            delivered_at=datetime.now(timezone.utc),
        )

        self._deliver(routed_msg, bridge)
        self._add_to_history(routed_msg)

        return routed_msg

    def broadcast(
        self,
        event: AgentEvent,
        exclude: Optional[Set[str]] = None,
    ) -> List[RoutedMessage]:
        """
        Broadcast an event to all registered agents.

        Args:
            event: The event to broadcast.
            exclude: Optional set of agent IDs to exclude.

        Returns:
            List of RoutedMessage results.
        """
        exclude = exclude or set()
        exclude.add(event.agent.id)  # Don't send to self

        results = []

        for agent_id, bridge in self._bridges.items():
            if agent_id in exclude:
                continue

            message_id = str(uuid.uuid4())
            routed_msg = RoutedMessage(
                message_id=message_id,
                event=event,
                sender=event.agent.id,
                recipient=agent_id,
                status=RouteStatus.DELIVERED,
                delivered_at=datetime.now(timezone.utc),
            )

            self._deliver(routed_msg, bridge)
            self._add_to_history(routed_msg)
            results.append(routed_msg)

        logger.info(f"Broadcast message to {len(results)} agents")
        return results

    def _deliver(self, message: RoutedMessage, bridge: AgentSocietyBridge) -> None:
        """Deliver a message to a bridge."""
        try:
            bridge.handle_incoming(message.event)
            message.status = RouteStatus.DELIVERED
            message.delivered_at = datetime.now(timezone.utc)

            # Notify delivery handlers
            for handler in self._delivery_handlers:
                try:
                    handler(message)
                except Exception as e:
                    logger.error(f"Delivery handler error: {e}")

        except Exception as e:
            message.status = RouteStatus.FAILED
            message.error = str(e)
            logger.error(f"Message delivery failed: {e}")

    def _create_failed_message(
        self,
        event: AgentEvent,
        sender: str,
        recipient: str,
        error: str,
    ) -> RoutedMessage:
        """Create a failed message record."""
        msg = RoutedMessage(
            message_id=str(uuid.uuid4()),
            event=event,
            sender=sender,
            recipient=recipient,
            status=RouteStatus.FAILED,
            error=error,
        )
        self._add_to_history(msg)
        return msg

    def _add_to_history(self, message: RoutedMessage) -> None:
        """Add message to history (with size limit)."""
        self._history.append(message)

        # Trim history if needed
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history :]

    def add_delivery_handler(
        self,
        handler: Callable[[RoutedMessage], None],
    ) -> None:
        """Add handler for message deliveries."""
        self._delivery_handlers.append(handler)

    def get_queue_size(self, agent_id: str) -> int:
        """Get number of queued messages for an agent."""
        return len(self._queues.get(agent_id, []))

    def get_history(
        self,
        limit: int = 100,
        agent_id: Optional[str] = None,
    ) -> List[RoutedMessage]:
        """
        Get message history.

        Args:
            limit: Maximum messages to return.
            agent_id: Optional filter by sender or recipient.

        Returns:
            List of recent messages.
        """
        history = self._history

        if agent_id:
            history = [
                m for m in history if m.sender == agent_id or m.recipient == agent_id
            ]

        return history[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics."""
        delivered = sum(1 for m in self._history if m.status == RouteStatus.DELIVERED)
        failed = sum(1 for m in self._history if m.status == RouteStatus.FAILED)
        queued = sum(len(q) for q in self._queues.values())

        return {
            "registered_agents": len(self._bridges),
            "total_messages": len(self._history),
            "delivered": delivered,
            "failed": failed,
            "queued": queued,
            "agents": list(self._bridges.keys()),
        }
