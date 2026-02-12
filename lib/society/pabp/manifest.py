"""
Bundle Manifest Schema and Signing.

This module handles manifest creation, validation, and cryptographic signing
for agent bundles.

SDG - Love - Truth - Beauty
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from lib.society.pabp.bundle import AgentBundle
import hashlib
import json

# Try to import cryptographic libraries
try:
    from nacl.signing import SigningKey, VerifyKey

    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


@dataclass
class ComponentChecksum:
    """
    Checksum record for a bundle component.
    
    Attributes:
        path: Relative path within bundle.
        algorithm: Hash algorithm used (sha256).
        checksum: The hash value.
    """
    
    path: str
    algorithm: str = "sha256"
    checksum: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "algorithm": self.algorithm,
            "checksum": self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "ComponentChecksum":
        """Create from dictionary."""
        return cls(
            path=data["path"],
            algorithm=data.get("algorithm", "sha256"),
            checksum=data["checksum"]
        )


@dataclass
class BundleManifest:
    """
    Manifest for an agent bundle.
    
    The manifest contains all metadata and checksums needed to verify
    bundle integrity without loading full content.
    
    Attributes:
        bundle_id: Unique bundle identifier.
        agent_id: ID of the agent.
        agent_name: Human-readable name.
        version: Bundle version (semver).
        created_at: Creation timestamp.
        checksums: List of component checksums.
        bundle_checksum: Overall bundle checksum.
        compatibility: Compatibility requirements.
        signature: Optional Ed25519 signature.
        signer_id: ID of signing agent/authority.
    """
    
    bundle_id: str
    agent_id: str
    agent_name: str
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    checksums: List[ComponentChecksum] = field(default_factory=list)
    bundle_checksum: str = ""
    compatibility: Dict[str, Any] = field(default_factory=dict)
    signature: Optional[str] = None
    signer_id: Optional[str] = None
    
    def calculate_bundle_checksum(self) -> str:
        """
        Calculate bundle checksum from component checksums.
        
        Returns:
            SHA-256 hash of sorted component checksums.
        """
        combined = "".join(sorted(c.checksum for c in self.checksums))
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def get_signable_content(self) -> bytes:
        """
        Get the content that should be signed.
        
        Returns:
            Canonical JSON bytes of manifest (without signature).
        """
        content = {
            "bundle_id": self.bundle_id,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "checksums": [c.to_dict() for c in self.checksums],
            "bundle_checksum": self.bundle_checksum or self.calculate_bundle_checksum(),
            "compatibility": self.compatibility
        }
        return json.dumps(content, sort_keys=True).encode()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary."""
        return {
            "bundle_id": self.bundle_id,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "checksums": [c.to_dict() for c in self.checksums],
            "bundle_checksum": self.bundle_checksum or self.calculate_bundle_checksum(),
            "compatibility": self.compatibility,
            "signature": self.signature,
            "signer_id": self.signer_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BundleManifest":
        """Create manifest from dictionary."""
        return cls(
            bundle_id=data["bundle_id"],
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            version=data.get("version", "1.0.0"),
            created_at=datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else datetime.utcnow(),
            checksums=[ComponentChecksum.from_dict(c) for c in data.get("checksums", [])],
            bundle_checksum=data.get("bundle_checksum", ""),
            compatibility=data.get("compatibility", {}),
            signature=data.get("signature"),
            signer_id=data.get("signer_id")
        )
    
    def verify_checksum(self) -> bool:
        """
        Verify that bundle_checksum matches calculated value.
        
        Returns:
            True if checksum is valid.
        """
        if not self.bundle_checksum:
            return False
        return self.bundle_checksum == self.calculate_bundle_checksum()


def sign_manifest(manifest: BundleManifest, private_key_hex: str, signer_id: str) -> BundleManifest:
    """
    Sign a manifest with Ed25519 private key.
    
    Args:
        manifest: The manifest to sign.
        private_key_hex: Ed25519 private key as hex string.
        signer_id: ID of the signing agent/authority.
        
    Returns:
        Manifest with signature and signer_id set.
        
    Raises:
        ImportError: If PyNaCl is not installed.
    """
    if not CRYPTO_AVAILABLE:
        raise ImportError(
            "Cryptographic signing requires PyNaCl. "
            "Install with: pip install pynacl"
        )
    
    # Ensure bundle checksum is set
    if not manifest.bundle_checksum:
        manifest.bundle_checksum = manifest.calculate_bundle_checksum()
    
    # Sign the content
    signing_key = SigningKey(bytes.fromhex(private_key_hex))
    signed = signing_key.sign(manifest.get_signable_content())
    
    manifest.signature = signed.signature.hex()
    manifest.signer_id = signer_id
    
    return manifest


def verify_manifest_signature(manifest: BundleManifest, public_key_hex: str) -> bool:
    """
    Verify a manifest signature with Ed25519 public key.
    
    Args:
        manifest: The manifest to verify.
        public_key_hex: Ed25519 public key as hex string.
        
    Returns:
        True if signature is valid.
        
    Raises:
        ImportError: If PyNaCl is not installed.
    """
    if not CRYPTO_AVAILABLE:
        raise ImportError(
            "Cryptographic verification requires PyNaCl. "
            "Install with: pip install pynacl"
        )
    
    if not manifest.signature:
        return False
    
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key_hex))
        signature = bytes.fromhex(manifest.signature)
        verify_key.verify(manifest.get_signable_content(), signature)
        return True
    except Exception:
        return False


def create_manifest_from_bundle(bundle: "AgentBundle") -> BundleManifest:
    """
    Create a manifest from an AgentBundle.
    
    Args:
        bundle: The bundle to create manifest for.
        
    Returns:
        BundleManifest with checksums from bundle components.
    """
    # Import here to avoid circular import

    
    checksums = [
        ComponentChecksum(
            path=c.path,
            checksum=c.checksum
        )
        for c in bundle.components
    ]
    
    manifest = BundleManifest(
        bundle_id=bundle.bundle_id,
        agent_id=bundle.agent_id,
        agent_name=bundle.agent_name,
        version=bundle.version,
        created_at=bundle.created_at,
        checksums=checksums,
        compatibility=bundle.compatibility
    )
    
    manifest.bundle_checksum = manifest.calculate_bundle_checksum()
    
    return manifest


@dataclass
class CompatibilityRequirements:
    """
    Compatibility requirements for a bundle.
    
    Attributes:
        min_factory_version: Minimum Factory version required.
        required_skills: Skills that must exist in target.
        required_knowledge: Knowledge files that must exist.
        python_version: Minimum Python version.
        dependencies: Required Python packages.
    """
    
    min_factory_version: str = "1.0.0"
    required_skills: List[str] = field(default_factory=list)
    required_knowledge: List[str] = field(default_factory=list)
    python_version: str = "3.10"
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "min_factory_version": self.min_factory_version,
            "required_skills": self.required_skills,
            "required_knowledge": self.required_knowledge,
            "python_version": self.python_version,
            "dependencies": self.dependencies
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompatibilityRequirements":
        """Create from dictionary."""
        return cls(
            min_factory_version=data.get("min_factory_version", "1.0.0"),
            required_skills=data.get("required_skills", []),
            required_knowledge=data.get("required_knowledge", []),
            python_version=data.get("python_version", "3.10"),
            dependencies=data.get("dependencies", [])
        )
    
    def check_compatibility(self, target_info: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check if requirements are met by target.
        
        Args:
            target_info: Dictionary with target environment info.
            
        Returns:
            Tuple of (compatible, list of missing requirements).
        """
        missing = []
        
        # Check factory version
        target_version = target_info.get("factory_version", "0.0.0")
        if self._version_lt(target_version, self.min_factory_version):
            missing.append(f"Factory version {self.min_factory_version} required (have {target_version})")
        
        # Check skills
        target_skills = set(target_info.get("skills", []))
        for skill in self.required_skills:
            if skill not in target_skills:
                missing.append(f"Required skill: {skill}")
        
        # Check knowledge
        target_knowledge = set(target_info.get("knowledge", []))
        for knowledge in self.required_knowledge:
            if knowledge not in target_knowledge:
                missing.append(f"Required knowledge: {knowledge}")
        
        return len(missing) == 0, missing
    
    @staticmethod
    def _version_lt(v1: str, v2: str) -> bool:
        """Check if v1 < v2 using semver comparison."""
        def parse(v: str) -> tuple[int, ...]:
            return tuple(int(x) for x in v.split(".")[:3])
        try:
            return parse(v1) < parse(v2)
        except (ValueError, IndexError):
            return False
