# Memory Persistence Architecture: SSGM Dual Substrate

## Overview
Based on the **Stability and Safety-Governed Memory (SSGM)** framework, the Antigravity Agent Factory implements a dual-layered memory architecture to balance high-speed learning with long-term stability and safety.

## 1. Dual Memory Substrate

| Layer | Type | Location | Persistence | Tooling |
| :--- | :--- | :--- | :--- | :--- |
| **Episodic Log** | Immutable / Trace | `logs/memory/` | Local Only | `episodic_logger.py` |
| **Active Graph** | Mutable / Selective | Memory MCP | Live Graph | `mcp_memory` tools |
| **Vector Store** | Cache / Optimized | `data/memory/` | Local Only | `memory_store.py` |
| **Permanent Knowledge** | Verified / Patterns | `.agent/knowledge/` | Git Committed | `InductionEngine` |

## 2. Governance Gates
All memory operations are governed by middleware gates located in `scripts/memory/governance_gates.py`:

- **Read Filtering Gate**: Applies Weibull decay and intent-alignment to prioritize relevant memories and prevent interference.
- **Write Validation Gate**: Checks for axiom violations and internal consistency before allowing state transitions.

## 3. Reconciliation & Synchronization
- **Reconciliation**: Periodically runs `reconcile_memory.py` to batch-process episodic logs into semantic patterns.
- **MCP Sync Bridge**: Uses `mcp_sync_bridge.py` to propagate approved semantic memories from the local vector store to the global Memory MCP graph.

## 4. Git Governance Policy
- **DO NOT COMMIT**: episodic logs, raw vector databases, or machine-specific caches.
- **COMMIT**: Only structured `.json` files in `.agent/knowledge/` that have passed the Write Validation Gate and user review.
