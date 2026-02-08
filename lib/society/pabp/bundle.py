"""
Agent Bundle Creation and Management.

This module provides the core data structures and functions for creating,
validating, and managing agent bundles for portable behavior transfer.

SDG - Love - Truth - Beauty
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import hashlib
import json


class ComponentType(Enum):
    """Types of components that can be included in a bundle."""
    
    IDENTITY = "identity"
    SKILL = "skill"
    KNOWLEDGE = "knowledge"
    WORKFLOW = "workflow"
    CONTRACT = "contract"
    ATTESTATION = "attestation"


@dataclass
class BundleComponent:
    """
    A single component within an agent bundle.
    
    Attributes:
        component_type: Type of component (skill, knowledge, etc.).
        name: Human-readable name.
        path: Relative path within the bundle.
        content: The actual content (string or dict).
        checksum: SHA-256 checksum of content.
        metadata: Additional component metadata.
    """
    
    component_type: ComponentType
    name: str
    path: str
    content: Union[str, Dict[str, Any]]
    checksum: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate checksum if not provided."""
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """Calculate SHA-256 checksum of content."""
        if isinstance(self.content, dict):
            content_str = json.dumps(self.content, sort_keys=True)
        else:
            content_str = str(self.content)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify that content matches stored checksum."""
        return self.checksum == self._calculate_checksum()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "component_type": self.component_type.value,
            "name": self.name,
            "path": self.path,
            "checksum": self.checksum,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], content: Union[str, Dict]) -> "BundleComponent":
        """Create from dictionary with separate content."""
        return cls(
            component_type=ComponentType(data["component_type"]),
            name=data["name"],
            path=data["path"],
            content=content,
            checksum=data.get("checksum", ""),
            metadata=data.get("metadata", {})
        )


@dataclass
class AgentBundle:
    """
    Complete bundle for portable agent behavior transfer.
    
    Attributes:
        bundle_id: Unique identifier for this bundle.
        agent_id: ID of the agent this bundle represents.
        agent_name: Human-readable agent name.
        version: Bundle version (semver).
        created_at: Bundle creation timestamp.
        components: List of bundle components.
        reputation_snapshot: Optional reputation state at export time.
        compatibility: Compatibility requirements.
        signature: Optional Ed25519 signature of manifest.
    """
    
    bundle_id: str
    agent_id: str
    agent_name: str
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    components: List[BundleComponent] = field(default_factory=list)
    reputation_snapshot: Optional[Dict[str, Any]] = None
    compatibility: Dict[str, Any] = field(default_factory=dict)
    signature: Optional[str] = None
    
    def add_component(self, component: BundleComponent) -> "AgentBundle":
        """
        Add a component to the bundle.
        
        Args:
            component: The component to add.
            
        Returns:
            Self for method chaining.
        """
        self.components.append(component)
        return self
    
    def add_skill(self, name: str, content: str, metadata: Optional[Dict] = None) -> "AgentBundle":
        """
        Add a skill component.
        
        Args:
            name: Skill name.
            content: SKILL.md content.
            metadata: Optional metadata.
            
        Returns:
            Self for method chaining.
        """
        component = BundleComponent(
            component_type=ComponentType.SKILL,
            name=name,
            path=f"skills/{name}/SKILL.md",
            content=content,
            metadata=metadata or {}
        )
        return self.add_component(component)
    
    def add_knowledge(self, name: str, content: Dict[str, Any]) -> "AgentBundle":
        """
        Add a knowledge component.
        
        Args:
            name: Knowledge file name (without .json).
            content: Knowledge file content.
            
        Returns:
            Self for method chaining.
        """
        component = BundleComponent(
            component_type=ComponentType.KNOWLEDGE,
            name=name,
            path=f"knowledge/{name}.json",
            content=content
        )
        return self.add_component(component)
    
    def add_workflow(self, name: str, content: str) -> "AgentBundle":
        """
        Add a workflow component.
        
        Args:
            name: Workflow name.
            content: Workflow definition content.
            
        Returns:
            Self for method chaining.
        """
        component = BundleComponent(
            component_type=ComponentType.WORKFLOW,
            name=name,
            path=f"workflows/{name}.yaml",
            content=content
        )
        return self.add_component(component)
    
    def get_components_by_type(self, component_type: ComponentType) -> List[BundleComponent]:
        """
        Get all components of a specific type.
        
        Args:
            component_type: Type to filter by.
            
        Returns:
            List of matching components.
        """
        return [c for c in self.components if c.component_type == component_type]
    
    def verify_all_components(self) -> "tuple[bool, List[str]]":
        """
        Verify integrity of all components.
        
        Returns:
            Tuple of (all_valid, list of invalid component names).
        """
        invalid = []
        for component in self.components:
            if not component.verify_integrity():
                invalid.append(component.name)
        return len(invalid) == 0, invalid
    
    def get_bundle_checksum(self) -> str:
        """
        Calculate overall bundle checksum from all component checksums.
        
        Returns:
            SHA-256 hash of concatenated component checksums.
        """
        combined = "".join(sorted(c.checksum for c in self.components))
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def to_manifest_dict(self) -> Dict[str, Any]:
        """
        Convert to manifest dictionary (without component content).
        
        Returns:
            Manifest as dictionary.
        """
        return {
            "bundle_id": self.bundle_id,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "bundle_checksum": self.get_bundle_checksum(),
            "components": [c.to_dict() for c in self.components],
            "reputation_snapshot": self.reputation_snapshot,
            "compatibility": self.compatibility,
            "signature": self.signature
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to full dictionary including content.
        
        Returns:
            Complete bundle as dictionary.
        """
        result = self.to_manifest_dict()
        result["component_contents"] = {
            c.path: c.content for c in self.components
        }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentBundle":
        """
        Create bundle from dictionary.
        
        Args:
            data: Bundle data from to_dict().
            
        Returns:
            Reconstructed AgentBundle.
        """
        contents = data.get("component_contents", {})
        components = [
            BundleComponent.from_dict(c_data, contents.get(c_data["path"], ""))
            for c_data in data.get("components", [])
        ]
        
        return cls(
            bundle_id=data["bundle_id"],
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            version=data.get("version", "1.0.0"),
            created_at=datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else datetime.utcnow(),
            components=components,
            reputation_snapshot=data.get("reputation_snapshot"),
            compatibility=data.get("compatibility", {}),
            signature=data.get("signature")
        )


def create_bundle(
    agent_id: str,
    agent_name: str,
    version: str = "1.0.0",
    reputation_snapshot: Optional[Dict[str, Any]] = None
) -> AgentBundle:
    """
    Create a new agent bundle.
    
    Args:
        agent_id: Unique agent identifier.
        agent_name: Human-readable name.
        version: Bundle version.
        reputation_snapshot: Optional reputation state.
        
    Returns:
        New AgentBundle ready for component addition.
        
    Example:
        bundle = create_bundle("code-analyzer", "Code Analyzer Agent")
        bundle.add_skill("analyze", skill_content)
        bundle.add_knowledge("patterns", patterns_json)
    """
    import uuid
    
    return AgentBundle(
        bundle_id=str(uuid.uuid4()),
        agent_id=agent_id,
        agent_name=agent_name,
        version=version,
        reputation_snapshot=reputation_snapshot
    )


def load_bundle_from_directory(path: Path) -> AgentBundle:
    """
    Load a bundle from a directory structure.
    
    Args:
        path: Path to the bundle directory.
        
    Returns:
        Loaded AgentBundle.
        
    Raises:
        FileNotFoundError: If manifest.json doesn't exist.
    """
    manifest_path = path / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest.json found in {path}")
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Load component contents from files
    component_contents = {}
    for comp_data in manifest.get("components", []):
        comp_path = path / comp_data["path"]
        if comp_path.exists():
            with open(comp_path, "r", encoding="utf-8") as f:
                if comp_path.suffix == ".json":
                    component_contents[comp_data["path"]] = json.load(f)
                else:
                    component_contents[comp_data["path"]] = f.read()
    
    manifest["component_contents"] = component_contents
    return AgentBundle.from_dict(manifest)


def save_bundle_to_directory(bundle: AgentBundle, path: Path) -> None:
    """
    Save a bundle to a directory structure.
    
    Args:
        bundle: The bundle to save.
        path: Target directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    
    # Save manifest
    manifest_path = path / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(bundle.to_manifest_dict(), f, indent=2)
    
    # Save component contents
    for component in bundle.components:
        comp_path = path / component.path
        comp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(comp_path, "w", encoding="utf-8") as f:
            if isinstance(component.content, dict):
                json.dump(component.content, f, indent=2)
            else:
                f.write(str(component.content))
