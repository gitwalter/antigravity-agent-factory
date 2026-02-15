"""
Integration Module

Bridges Factory agents to the verification system.

This module provides:
- AgentSocietyBridge: Connect individual agents to the society
- MessageRouter: Route messages between verified agents
- SocietyContext: Shared context for multi-agent interactions

Usage:
    from lib.society.integration import (
        AgentSocietyBridge,
        MessageRouter,
        SocietyContext,
    )

    # Create shared society context
    context = SocietyContext.create_default()

    # Create bridge for an agent
    bridge = AgentSocietyBridge(
        agent_id="knowledge-manager",
        agent_type="coordinator",
        context=context,
    )

    # Send verified message
    result = await bridge.send_message(
        target="template-generator",
        message_type="propose",
        payload={"update": "new-knowledge"},
    )

    if result.verified:
        print(f"Message sent: {result.event_id}")
    else:
        print(f"Verification failed: {result.violations}")

SDG - Love - Truth - Beauty
"""

from lib.society.integration.context import SocietyContext
from lib.society.integration.agent_bridge import AgentSocietyBridge, BridgeResult
from lib.society.integration.message_router import MessageRouter, RoutedMessage

__all__ = [
    "SocietyContext",
    "AgentSocietyBridge",
    "BridgeResult",
    "MessageRouter",
    "RoutedMessage",
]
