"""
Hash Chain Management

Provides hash chain validation and integrity verification for event streams.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


from lib.society.events.schema import AgentEvent


@dataclass
class ChainValidationResult:
    """
    Result of chain validation.
    
    Attributes:
        valid: Whether the chain is valid.
        error_message: Description of error if invalid.
        error_index: Index of first invalid event.
        events_validated: Number of events validated.
    """
    valid: bool
    error_message: Optional[str] = None
    error_index: Optional[int] = None
    events_validated: int = 0


class HashChain:
    """
    Manages hash chain for event integrity.
    
    Each event's hash includes the previous event's hash,
    creating a tamper-evident chain. Any modification to
    a past event will break the chain.
    """
    
    GENESIS_HASH = ""  # Empty string for first event
    
    @staticmethod
    def compute_event_hash(event: AgentEvent) -> str:
        """
        Compute the hash for an event.
        
        Args:
            event: The event to hash.
            
        Returns:
            SHA-256 hash prefixed with 'sha256:'.
        """
        return event.compute_hash()
    
    @staticmethod
    def verify_event_hash(event: AgentEvent) -> bool:
        """
        Verify an event's hash is correct.
        
        Args:
            event: The event to verify.
            
        Returns:
            True if hash matches computed value.
        """
        return event.verify_hash()
    
    @staticmethod
    def verify_chain_link(
        current: AgentEvent,
        previous: Optional[AgentEvent]
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify the chain link between two events.
        
        Args:
            current: The current event.
            previous: The previous event (None for genesis).
            
        Returns:
            Tuple of (is_valid, error_message).
        """
        # Check previous hash reference
        if previous is None:
            # First event should have empty previous hash
            if current.previous_hash != HashChain.GENESIS_HASH:
                return False, "Genesis event has non-empty previous hash"
        else:
            # Subsequent events should reference previous hash
            if current.previous_hash != previous.hash:
                return False, (
                    f"Hash chain broken: expected {previous.hash}, "
                    f"got {current.previous_hash}"
                )
        
        # Check sequence number
        expected_sequence = 1 if previous is None else previous.sequence + 1
        if current.sequence != expected_sequence:
            return False, (
                f"Sequence mismatch: expected {expected_sequence}, "
                f"got {current.sequence}"
            )
        
        # Verify event's own hash
        if not HashChain.verify_event_hash(current):
            return False, "Event hash verification failed"
        
        return True, None
    
    @staticmethod
    def verify_chain(events: List[AgentEvent]) -> ChainValidationResult:
        """
        Verify the integrity of an entire event chain.
        
        Args:
            events: List of events in sequence order.
            
        Returns:
            ChainValidationResult with validation status.
        """
        if not events:
            return ChainValidationResult(valid=True, events_validated=0)
        
        for i, event in enumerate(events):
            previous = events[i - 1] if i > 0 else None
            valid, error = HashChain.verify_chain_link(event, previous)
            
            if not valid:
                return ChainValidationResult(
                    valid=False,
                    error_message=error,
                    error_index=i,
                    events_validated=i,
                )
        
        return ChainValidationResult(
            valid=True,
            events_validated=len(events),
        )
    
    @staticmethod
    def find_tampering(events: List[AgentEvent]) -> List[int]:
        """
        Find all tampered events in a chain.
        
        Args:
            events: List of events to check.
            
        Returns:
            List of indices where tampering was detected.
        """
        tampered = []
        
        for i, event in enumerate(events):
            # Check hash
            if not HashChain.verify_event_hash(event):
                tampered.append(i)
                continue
            
            # Check chain link
            if i > 0 and event.previous_hash != events[i - 1].hash:
                tampered.append(i)
        
        return tampered


def verify_chain_integrity(events: List[AgentEvent]) -> ChainValidationResult:
    """
    Convenience function to verify chain integrity.
    
    Args:
        events: List of events in sequence order.
        
    Returns:
        ChainValidationResult with validation status.
    """
    return HashChain.verify_chain(events)
