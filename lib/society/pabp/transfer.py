"""
Bundle Transfer Operations.

This module handles exporting, importing, and verifying agent bundles
for portable behavior transfer between projects.

SDG - Love - Truth - Beauty
"""

from __future__ import annotations
from dataclasses import dataclass, field

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import zipfile
import tempfile


from lib.society.pabp.bundle import (
    AgentBundle,
    create_bundle,
    load_bundle_from_directory,
    save_bundle_to_directory,
)
from lib.society.pabp.manifest import (
    create_manifest_from_bundle,
    verify_manifest_signature,
    CompatibilityRequirements,
)


class TransferMode(Enum):
    """Modes for bundle transfer."""

    FULL = "full"  # Complete bundle transfer
    SELECTIVE = "selective"  # Specific components only
    INCREMENTAL = "incremental"  # Delta from previous version
    REFERENCE_ONLY = "reference"  # Metadata only, no content


@dataclass
class TransferResult:
    """
    Result of a transfer operation.

    Attributes:
        success: Whether transfer completed successfully.
        bundle_id: ID of the transferred bundle.
        components_transferred: Number of components transferred.
        warnings: Non-fatal issues encountered.
        errors: Fatal errors that prevented transfer.
        verification_passed: Whether integrity verification passed.
    """

    success: bool
    bundle_id: str = ""
    components_transferred: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    verification_passed: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "bundle_id": self.bundle_id,
            "components_transferred": self.components_transferred,
            "warnings": self.warnings,
            "errors": self.errors,
            "verification_passed": self.verification_passed,
        }


def export_bundle(
    bundle: AgentBundle,
    output_path: Path,
    mode: TransferMode = TransferMode.FULL,
    compress: bool = True,
    sign_key: Optional[str] = None,
    signer_id: Optional[str] = None,
) -> TransferResult:
    """
    Export an agent bundle to a file or directory.

    Args:
        bundle: The bundle to export.
        output_path: Destination path (.zip for compressed, directory otherwise).
        mode: Transfer mode (full, selective, etc.).
        compress: Whether to create a zip file.
        sign_key: Optional Ed25519 private key for signing.
        signer_id: ID of the signer.

    Returns:
        TransferResult with export status.

    Example:
        result = export_bundle(bundle, Path("agent.zip"))
        if result.success:
            print(f"Exported {result.components_transferred} components")
    """
    result = TransferResult(success=False)

    try:
        # Create manifest
        manifest = create_manifest_from_bundle(bundle)

        # Sign if key provided
        if sign_key and signer_id:
            try:
                from lib.society.pabp.manifest import sign_manifest

                manifest = sign_manifest(manifest, sign_key, signer_id)
            except ImportError as e:
                result.warnings.append(f"Signing skipped: {e}")

        # Update bundle with signature
        bundle.signature = manifest.signature

        if compress:
            # Export as zip
            _export_zip(bundle, output_path)
        else:
            # Export as directory
            save_bundle_to_directory(bundle, output_path)

        result.success = True
        result.bundle_id = bundle.bundle_id
        result.components_transferred = len(bundle.components)

    except Exception as e:
        result.errors.append(str(e))

    return result


def _export_zip(bundle: AgentBundle, output_path: Path) -> None:
    """Export bundle as a zip file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "bundle"
        save_bundle_to_directory(bundle, temp_path)

        # Create zip
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in temp_path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_path)
                    zf.write(file_path, arcname)


def import_bundle(
    source_path: Path,
    target_directory: Optional[Path] = None,
    verify_signature: bool = True,
    public_key: Optional[str] = None,
    check_compatibility: bool = True,
    target_info: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[AgentBundle], TransferResult]:
    """
    Import an agent bundle from a file or directory.

    Args:
        source_path: Source path (.zip file or directory).
        target_directory: Optional directory to extract to.
        verify_signature: Whether to verify bundle signature.
        public_key: Ed25519 public key for signature verification.
        check_compatibility: Whether to check compatibility requirements.
        target_info: Target environment info for compatibility check.

    Returns:
        Tuple of (AgentBundle or None, TransferResult).

    Example:
        bundle, result = import_bundle(Path("agent.zip"))
        if result.success:
            for skill in bundle.get_components_by_type(ComponentType.SKILL):
                print(f"Imported skill: {skill.name}")
    """
    result = TransferResult(success=False)
    bundle = None

    try:
        # Extract or load
        if source_path.suffix == ".zip":
            bundle = _import_zip(source_path, target_directory)
        else:
            bundle = load_bundle_from_directory(source_path)

        result.bundle_id = bundle.bundle_id
        result.components_transferred = len(bundle.components)

        # Verify integrity
        valid, invalid = bundle.verify_all_components()
        if not valid:
            result.warnings.append(f"Invalid components: {invalid}")
            result.verification_passed = False

        # Verify signature if requested
        if verify_signature and bundle.signature and public_key:
            manifest = create_manifest_from_bundle(bundle)
            manifest.signature = bundle.signature
            if not verify_manifest_signature(manifest, public_key):
                result.warnings.append("Signature verification failed")
                result.verification_passed = False

        # Check compatibility
        if check_compatibility and bundle.compatibility:
            compat_req = CompatibilityRequirements.from_dict(bundle.compatibility)
            target = target_info or {}
            compatible, missing = compat_req.check_compatibility(target)
            if not compatible:
                result.warnings.extend(missing)

        result.success = True

    except Exception as e:
        result.errors.append(str(e))

    return bundle, result


def _import_zip(source_path: Path, target_directory: Optional[Path]) -> AgentBundle:
    """Import bundle from a zip file."""
    extract_dir = target_directory or Path(tempfile.mkdtemp())

    with zipfile.ZipFile(source_path, "r") as zf:
        zf.extractall(extract_dir)

    return load_bundle_from_directory(extract_dir)


def verify_bundle(
    bundle: AgentBundle, public_key: Optional[str] = None, strict: bool = False
) -> TransferResult:
    """
    Verify a bundle's integrity and optionally its signature.

    Args:
        bundle: The bundle to verify.
        public_key: Optional Ed25519 public key for signature verification.
        strict: If True, fail on any warning.

    Returns:
        TransferResult with verification status.

    Example:
        result = verify_bundle(bundle, public_key="abc123...")
        if result.verification_passed:
            print("Bundle integrity verified")
    """
    result = TransferResult(success=True, bundle_id=bundle.bundle_id)

    # Verify component integrity
    valid, invalid = bundle.verify_all_components()
    if not valid:
        result.warnings.append(f"Invalid component checksums: {invalid}")
        result.verification_passed = False

    # Verify signature if provided
    if public_key and bundle.signature:
        manifest = create_manifest_from_bundle(bundle)
        manifest.signature = bundle.signature
        if not verify_manifest_signature(manifest, public_key):
            result.warnings.append("Signature verification failed")
            result.verification_passed = False

    if strict and result.warnings:
        result.success = False
        result.errors.extend(result.warnings)

    result.components_transferred = len(bundle.components)

    return result


def merge_bundles(
    base: AgentBundle, overlay: AgentBundle, conflict_strategy: str = "overlay_wins"
) -> AgentBundle:
    """
    Merge two bundles together.

    Args:
        base: The base bundle.
        overlay: The bundle to merge on top.
        conflict_strategy: How to handle conflicts ("overlay_wins" or "base_wins").

    Returns:
        New merged AgentBundle.
    """
    merged = create_bundle(
        agent_id=overlay.agent_id,
        agent_name=overlay.agent_name,
        version=overlay.version,
    )

    # Index by path
    base_components = {c.path: c for c in base.components}
    overlay_components = {c.path: c for c in overlay.components}

    # Merge
    all_paths = set(base_components.keys()) | set(overlay_components.keys())

    for path in all_paths:
        if path in overlay_components and path in base_components:
            # Conflict
            if conflict_strategy == "overlay_wins":
                merged.add_component(overlay_components[path])
            else:
                merged.add_component(base_components[path])
        elif path in overlay_components:
            merged.add_component(overlay_components[path])
        else:
            merged.add_component(base_components[path])

    return merged


def create_incremental_bundle(
    current: AgentBundle, previous: AgentBundle
) -> AgentBundle:
    """
    Create an incremental bundle with only changed components.

    Args:
        current: The current bundle.
        previous: The previous version bundle.

    Returns:
        New bundle containing only changed/added components.
    """
    delta = create_bundle(
        agent_id=current.agent_id,
        agent_name=current.agent_name,
        version=current.version,
    )

    # Index previous by path
    prev_checksums = {c.path: c.checksum for c in previous.components}

    # Find changed/new components
    for component in current.components:
        prev_checksum = prev_checksums.get(component.path)
        if prev_checksum is None or prev_checksum != component.checksum:
            delta.add_component(component)

    # Add metadata about what was removed
    delta.compatibility["removed_components"] = [
        path
        for path in prev_checksums
        if path not in {c.path for c in current.components}
    ]
    delta.compatibility["base_version"] = previous.version

    return delta


@dataclass
class TransferConfig:
    """
    Configuration for bundle transfers.

    Attributes:
        verify_signatures: Whether to verify signatures.
        check_compatibility: Whether to check compatibility.
        allow_unsigned: Whether to allow unsigned bundles.
        reputation_decay: Decay factor for reputation (0.8 = 20% decay).
        max_bundle_size_mb: Maximum bundle size in MB.
    """

    verify_signatures: bool = True
    check_compatibility: bool = True
    allow_unsigned: bool = True
    reputation_decay: float = 0.8
    max_bundle_size_mb: int = 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "verify_signatures": self.verify_signatures,
            "check_compatibility": self.check_compatibility,
            "allow_unsigned": self.allow_unsigned,
            "reputation_decay": self.reputation_decay,
            "max_bundle_size_mb": self.max_bundle_size_mb,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransferConfig":
        """Create from dictionary."""
        return cls(
            verify_signatures=data.get("verify_signatures", True),
            check_compatibility=data.get("check_compatibility", True),
            allow_unsigned=data.get("allow_unsigned", True),
            reputation_decay=data.get("reputation_decay", 0.8),
            max_bundle_size_mb=data.get("max_bundle_size_mb", 100),
        )
