"""
Communication Protocols

Inter-agent communication patterns with axiom compliance.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of inter-agent messages."""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    CONSENSUS = "consensus"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    EMERGENCY = 5


@dataclass
class Message:
    """
    Inter-agent message.
    
    Attributes:
        id: Unique message identifier.
        type: Type of message.
        sender: Sending agent.
        recipients: Target agents (empty = broadcast).
        content: Message payload.
        priority: Message priority.
        timestamp: When message was created.
        reply_to: Optional message this replies to.
        signature: Sender's cryptographic signature.
    """
    id: str
    type: MessageType
    sender: str
    content: Dict[str, Any]
    recipients: List[str] = field(default_factory=list)
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reply_to: Optional[str] = None
    signature: Optional[str] = None
    
    @property
    def is_broadcast(self) -> bool:
        """Check if this is a broadcast message."""
        return len(self.recipients) == 0
    
    def compute_hash(self) -> str:
        """Compute message hash for verification."""
        data = {
            "id": self.id,
            "type": self.type.value,
            "sender": self.sender,
            "recipients": sorted(self.recipients),
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "reply_to": self.reply_to,
        }
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "sender": self.sender,
            "recipients": self.recipients,
            "content": self.content,
            "priority": self.priority.value,
            "timestamp": self.timestamp.isoformat(),
            "reply_to": self.reply_to,
            "signature": self.signature,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            type=MessageType(data["type"]),
            sender=data["sender"],
            recipients=data.get("recipients", []),
            content=data.get("content", {}),
            priority=MessagePriority(data.get("priority", 2)),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            reply_to=data.get("reply_to"),
            signature=data.get("signature"),
        )


MessageHandler = Callable[[Message], Optional[Message]]


class CommunicationProtocol(ABC):
    """
    Abstract base class for communication protocols.
    
    Defines how agents communicate within the society.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Protocol name."""
        pass
    
    @abstractmethod
    def send(self, message: Message) -> bool:
        """Send a message."""
        pass
    
    @abstractmethod
    def receive(self, agent_id: str) -> List[Message]:
        """Receive pending messages for an agent."""
        pass
    
    @abstractmethod
    def register_handler(
        self,
        agent_id: str,
        message_type: MessageType,
        handler: MessageHandler
    ) -> None:
        """Register a message handler."""
        pass


class DirectProtocol(CommunicationProtocol):
    """
    Direct point-to-point messaging protocol.
    
    Features:
    - Direct agent-to-agent communication
    - Message queuing
    - Priority-based delivery
    
    Axiom alignment:
    - A2 Truth: Direct, transparent communication
    """
    
    def __init__(self):
        """Initialize protocol."""
        # agent_id -> list of pending messages
        self._queues: Dict[str, List[Message]] = {}
        # agent_id -> message_type -> handlers
        self._handlers: Dict[str, Dict[MessageType, List[MessageHandler]]] = {}
    
    @property
    def name(self) -> str:
        return "direct"
    
    def register_agent(self, agent_id: str) -> None:
        """Register an agent with the protocol."""
        if agent_id not in self._queues:
            self._queues[agent_id] = []
            self._handlers[agent_id] = {}
    
    def send(self, message: Message) -> bool:
        """Send a message to specified recipients."""
        if not message.recipients:
            logger.warning(f"Direct protocol requires recipients for message {message.id}")
            return False
        
        delivered = 0
        for recipient in message.recipients:
            if recipient in self._queues:
                self._queues[recipient].append(message)
                delivered += 1
                
                # Trigger handlers
                self._trigger_handlers(recipient, message)
        
        logger.debug(f"Delivered message {message.id} to {delivered} recipients")
        return delivered > 0
    
    def receive(self, agent_id: str) -> List[Message]:
        """Receive and clear pending messages."""
        if agent_id not in self._queues:
            return []
        
        messages = sorted(
            self._queues[agent_id],
            key=lambda m: (m.priority.value, m.timestamp),
            reverse=True
        )
        self._queues[agent_id] = []
        
        return messages
    
    def peek(self, agent_id: str) -> List[Message]:
        """Peek at pending messages without clearing."""
        if agent_id not in self._queues:
            return []
        return self._queues[agent_id].copy()
    
    def register_handler(
        self,
        agent_id: str,
        message_type: MessageType,
        handler: MessageHandler
    ) -> None:
        """Register a message handler."""
        self.register_agent(agent_id)
        
        if message_type not in self._handlers[agent_id]:
            self._handlers[agent_id][message_type] = []
        
        self._handlers[agent_id][message_type].append(handler)
    
    def _trigger_handlers(self, agent_id: str, message: Message) -> None:
        """Trigger registered handlers for a message."""
        handlers = self._handlers.get(agent_id, {}).get(message.type, [])
        
        for handler in handlers:
            try:
                response = handler(message)
                if response:
                    self.send(response)
            except Exception as e:
                logger.error(f"Handler error for {agent_id}: {e}")


class BroadcastProtocol(CommunicationProtocol):
    """
    Broadcast messaging protocol.
    
    Features:
    - Topic-based pub/sub
    - Filtered broadcasts
    - Message history
    
    Axiom alignment:
    - A2 Truth: Open information sharing
    - A1 Love: Inclusive communication
    """
    
    def __init__(self, history_limit: int = 100):
        """Initialize protocol."""
        self._subscribers: Dict[str, Set[str]] = {}  # topic -> agents
        self._history: List[Message] = []
        self._agent_topics: Dict[str, Set[str]] = {}  # agent -> topics
        self._handlers: Dict[str, Dict[MessageType, List[MessageHandler]]] = {}
        self.history_limit = history_limit
    
    @property
    def name(self) -> str:
        return "broadcast"
    
    def subscribe(self, agent_id: str, topic: str = "*") -> None:
        """Subscribe agent to a topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = set()
        self._subscribers[topic].add(agent_id)
        
        if agent_id not in self._agent_topics:
            self._agent_topics[agent_id] = set()
        self._agent_topics[agent_id].add(topic)
    
    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """Unsubscribe agent from a topic."""
        if topic in self._subscribers:
            self._subscribers[topic].discard(agent_id)
        if agent_id in self._agent_topics:
            self._agent_topics[agent_id].discard(topic)
    
    def send(self, message: Message) -> bool:
        """Broadcast a message."""
        topic = message.content.get("topic", "*")
        
        # Get all subscribers for this topic and wildcard
        recipients: Set[str] = set()
        recipients.update(self._subscribers.get(topic, set()))
        recipients.update(self._subscribers.get("*", set()))
        
        # Don't send back to sender
        recipients.discard(message.sender)
        
        # Store in history
        self._history.append(message)
        if len(self._history) > self.history_limit:
            self._history = self._history[-self.history_limit:]
        
        # Trigger handlers for all recipients
        for recipient in recipients:
            self._trigger_handlers(recipient, message)
        
        logger.debug(f"Broadcast message {message.id} to {len(recipients)} subscribers on topic '{topic}'")
        return len(recipients) > 0
    
    def receive(self, agent_id: str) -> List[Message]:
        """Get recent broadcasts relevant to agent."""
        topics = self._agent_topics.get(agent_id, {"*"})
        
        messages = []
        for msg in self._history:
            msg_topic = msg.content.get("topic", "*")
            if msg_topic in topics or "*" in topics:
                if msg.sender != agent_id:
                    messages.append(msg)
        
        return messages[-20:]  # Last 20 relevant messages
    
    def register_handler(
        self,
        agent_id: str,
        message_type: MessageType,
        handler: MessageHandler
    ) -> None:
        """Register a message handler."""
        if agent_id not in self._handlers:
            self._handlers[agent_id] = {}
        
        if message_type not in self._handlers[agent_id]:
            self._handlers[agent_id][message_type] = []
        
        self._handlers[agent_id][message_type].append(handler)
    
    def _trigger_handlers(self, agent_id: str, message: Message) -> None:
        """Trigger registered handlers."""
        handlers = self._handlers.get(agent_id, {}).get(message.type, [])
        
        for handler in handlers:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Broadcast handler error for {agent_id}: {e}")


@dataclass
class ConsensusRound:
    """
    Consensus round state.
    
    Attributes:
        id: Round identifier.
        topic: What is being decided.
        proposer: Agent who initiated.
        proposal: The proposed value.
        votes: Votes received.
        status: Current status.
    """
    id: str
    topic: str
    proposer: str
    proposal: Any
    votes: Dict[str, bool] = field(default_factory=dict)
    status: str = "open"
    created: datetime = field(default_factory=datetime.utcnow)


class ConsensusProtocol(CommunicationProtocol):
    """
    Consensus-based communication protocol.
    
    Features:
    - Multi-phase consensus
    - Quorum-based decisions
    - Byzantine fault tolerance (simplified)
    
    Axiom alignment:
    - A2 Truth: Collective agreement on truth
    - A4 Guardian: Safe decision making
    """
    
    DEFAULT_QUORUM = 0.67  # 2/3 majority
    
    def __init__(self, quorum: float = DEFAULT_QUORUM):
        """Initialize protocol."""
        self._participants: Set[str] = set()
        self._rounds: Dict[str, ConsensusRound] = {}
        self._handlers: Dict[str, Dict[MessageType, List[MessageHandler]]] = {}
        self.quorum = quorum
    
    @property
    def name(self) -> str:
        return "consensus"
    
    def add_participant(self, agent_id: str) -> None:
        """Add a consensus participant."""
        self._participants.add(agent_id)
    
    def remove_participant(self, agent_id: str) -> None:
        """Remove a participant."""
        self._participants.discard(agent_id)
    
    def propose(self, proposer: str, topic: str, value: Any) -> Optional[str]:
        """
        Initiate a consensus round.
        
        Args:
            proposer: Agent proposing.
            topic: Topic of consensus.
            value: Proposed value.
            
        Returns:
            Round ID if successful.
        """
        if proposer not in self._participants:
            return None
        
        round_id = f"consensus-{len(self._rounds) + 1}"
        
        self._rounds[round_id] = ConsensusRound(
            id=round_id,
            topic=topic,
            proposer=proposer,
            proposal=value,
        )
        
        logger.info(f"Consensus round started: {round_id} by {proposer}")
        return round_id
    
    def vote(self, round_id: str, agent_id: str, accept: bool) -> bool:
        """
        Vote on a consensus round.
        
        Args:
            round_id: The consensus round.
            agent_id: Voting agent.
            accept: Whether to accept proposal.
            
        Returns:
            True if vote was recorded.
        """
        round_data = self._rounds.get(round_id)
        if not round_data or round_data.status != "open":
            return False
        
        if agent_id not in self._participants:
            return False
        
        round_data.votes[agent_id] = accept
        
        # Check if we have quorum
        self._check_consensus(round_id)
        
        return True
    
    def _check_consensus(self, round_id: str) -> None:
        """Check if consensus is reached."""
        round_data = self._rounds.get(round_id)
        if not round_data:
            return
        
        total = len(self._participants)
        votes = len(round_data.votes)
        accepts = sum(1 for v in round_data.votes.values() if v)
        
        # Check quorum
        if votes >= total * self.quorum:
            if accepts >= votes * self.quorum:
                round_data.status = "accepted"
                logger.info(f"Consensus reached: {round_id} accepted")
            else:
                round_data.status = "rejected"
                logger.info(f"Consensus reached: {round_id} rejected")
    
    def get_result(self, round_id: str) -> Optional[tuple]:
        """
        Get result of a consensus round.
        
        Returns:
            (status, proposal) if round exists.
        """
        round_data = self._rounds.get(round_id)
        if not round_data:
            return None
        return (round_data.status, round_data.proposal)
    
    def send(self, message: Message) -> bool:
        """Send consensus message."""
        if message.type != MessageType.CONSENSUS:
            return False
        
        # Process based on content
        action = message.content.get("action")
        
        if action == "propose":
            round_id = self.propose(
                message.sender,
                message.content.get("topic", ""),
                message.content.get("value"),
            )
            return round_id is not None
        
        elif action == "vote":
            return self.vote(
                message.content.get("round_id", ""),
                message.sender,
                message.content.get("accept", False),
            )
        
        return False
    
    def receive(self, agent_id: str) -> List[Message]:
        """Get pending consensus messages for agent."""
        messages = []
        
        for round_data in self._rounds.values():
            if round_data.status == "open":
                if agent_id not in round_data.votes:
                    # Create a consensus request message
                    msg = Message(
                        id=f"consensus-request-{round_data.id}",
                        type=MessageType.CONSENSUS,
                        sender=round_data.proposer,
                        content={
                            "action": "request_vote",
                            "round_id": round_data.id,
                            "topic": round_data.topic,
                            "proposal": round_data.proposal,
                        },
                        recipients=[agent_id],
                    )
                    messages.append(msg)
        
        return messages
    
    def register_handler(
        self,
        agent_id: str,
        message_type: MessageType,
        handler: MessageHandler
    ) -> None:
        """Register a message handler."""
        if agent_id not in self._handlers:
            self._handlers[agent_id] = {}
        
        if message_type not in self._handlers[agent_id]:
            self._handlers[agent_id][message_type] = []
        
        self._handlers[agent_id][message_type].append(handler)


class MessageRouter:
    """
    Routes messages through appropriate protocols.
    
    Provides a unified interface for multi-protocol communication.
    """
    
    def __init__(self):
        """Initialize router."""
        self._protocols: Dict[str, CommunicationProtocol] = {}
        self._default_protocol: Optional[str] = None
    
    def register_protocol(
        self,
        protocol: CommunicationProtocol,
        default: bool = False
    ) -> None:
        """Register a communication protocol."""
        self._protocols[protocol.name] = protocol
        
        if default or self._default_protocol is None:
            self._default_protocol = protocol.name
    
    def get_protocol(self, name: str) -> Optional[CommunicationProtocol]:
        """Get a protocol by name."""
        return self._protocols.get(name)
    
    def route(self, message: Message, protocol_name: Optional[str] = None) -> bool:
        """
        Route a message through the appropriate protocol.
        
        Args:
            message: Message to route.
            protocol_name: Optional specific protocol.
            
        Returns:
            True if message was routed successfully.
        """
        name = protocol_name or self._default_protocol
        if not name:
            logger.error("No protocol specified and no default set")
            return False
        
        protocol = self._protocols.get(name)
        if not protocol:
            logger.error(f"Unknown protocol: {name}")
            return False
        
        return protocol.send(message)
    
    def create_default_router(self) -> "MessageRouter":
        """Create router with default protocols."""
        self.register_protocol(DirectProtocol(), default=True)
        self.register_protocol(BroadcastProtocol())
        self.register_protocol(ConsensusProtocol())
        return self


def create_message(
    sender: str,
    content: Dict[str, Any],
    message_type: MessageType = MessageType.REQUEST,
    recipients: Optional[List[str]] = None,
    priority: MessagePriority = MessagePriority.NORMAL,
    reply_to: Optional[str] = None
) -> Message:
    """
    Factory function to create messages.
    
    Args:
        sender: Sending agent ID.
        content: Message content.
        message_type: Type of message.
        recipients: Target agents.
        priority: Message priority.
        reply_to: Optional message being replied to.
        
    Returns:
        Configured Message instance.
    """
    import uuid
    
    return Message(
        id=str(uuid.uuid4()),
        type=message_type,
        sender=sender,
        recipients=recipients or [],
        content=content,
        priority=priority,
        reply_to=reply_to,
    )
