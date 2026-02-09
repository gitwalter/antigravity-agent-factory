"""
Portable Agent Behavior Protocol (PABP) Implementation.

This module enables transferring agent capabilities, knowledge, and workflows
between projects through a standardized bundle format.

Value Proposition:
- Build once, deploy everywhere
- 100% agent reuse across projects
- Reputation portability with trust decay
- Verified bundle integrity

Bundle Format:
    AgentBundle/
    ├── manifest.json       # Version, checksums, signatures
    ├── identity/           # Agent identity and keys
    ├── skills/             # SKILL.md files
    ├── knowledge/          # Knowledge JSON files
    ├── workflows/          # Workflow definitions
    └── attestations/       # Verifiable credentials

SDG - Love - Truth - Beauty
"""

from lib.society.pabp.bundle import AgentBundle, BundleComponent, create_bundle
from lib.society.pabp.manifest import BundleManifest, ComponentChecksum, sign_manifest
from lib.society.pabp.transfer import (
    export_bundle,
    import_bundle,
    verify_bundle,
    TransferMode,
    TransferResult
)
from lib.society.pabp.adapters import (
    PlatformAdapter,
    AntigravityAdapter,
    CursorAdapter,
    GenericAdapter,
    detect_platform,
    get_adapter
)
from lib.society.pabp.client import PABPClient, UpdateResult

__all__ = [
    # Bundle
    "AgentBundle",
    "BundleComponent",
    "create_bundle",
    # Manifest
    "BundleManifest",
    "ComponentChecksum",
    "sign_manifest",
    # Transfer
    "export_bundle",
    "import_bundle",
    "verify_bundle",
    "TransferMode",
    "TransferResult",
    # Adapters
    "PlatformAdapter",
    "AntigravityAdapter",
    "CursorAdapter",
    "GenericAdapter",
    "detect_platform",
    "get_adapter",
    # Client
    "PABPClient",
    "UpdateResult",
]
