"""
PABP Platform Adapters.

This module provides adapters for translating PABP components between
different platform conventions (e.g., Cursor vs Antigravity).

SDG - Love - Truth - Beauty
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type
import re
import shutil


class PlatformAdapter(ABC):
    """
    Abstract base class for platform adapters.
    
    Adapters handle the translation of canonical PABP component names
    to platform-specific filesystem paths and conventions.
    """
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Unique platform identifier."""
        pass
    
    @abstractmethod
    def skill_path(self, name: str) -> Path:
        """Return relative path for a skill."""
        pass
    
    @abstractmethod
    def agent_path(self, name: str) -> Path:
        """Return relative path for an agent definition."""
        pass
    
    @abstractmethod
    def knowledge_path(self, name: str) -> Path:
        """Return relative path for a knowledge file."""
        pass
    
    @abstractmethod
    def workflow_path(self, name: str) -> Path:
        """Return relative path for a workflow definition."""
        pass
    
    @abstractmethod
    def template_path(self, name: str) -> Path:
        """Return relative path for a template."""
        pass
    
    @abstractmethod
    def protocol_path(self, name: str) -> Path:
        """Return relative path for a protocol document."""
        pass
        
    @abstractmethod
    def script_path(self, name: str) -> Path:
        """Return relative path for a script."""
        pass
    
    @abstractmethod
    def rules_path(self) -> Path:
        """Return relative path for the rules file."""
        pass
    
    @abstractmethod
    def lib_path(self) -> Path:
        """Return relative path for the library directory."""
        pass
    
    def path_rewrite_rules(self) -> Dict[str, str]:
        """
        Return regex patterns for rewriting paths in content.
        Maps source platform patterns to this platform's patterns.
        """
        return {}
    
    def platform_term_rewrites(self) -> Dict[str, str]:
        """
        Return dictionary of term replacements.
        Maps source platform terms to this platform's terms.
        """
        return {}
    
    def foreign_artifact_patterns(self) -> List[str]:
        """Return list of file patterns belonging to other platforms."""
        return []

    def transform_content(self, content: str, source_adapter: "PlatformAdapter") -> str:
        """
        Transform content strings to match this platform's conventions.
        
        Applies path rewrites and term replacements.
        """
        if self.platform_name == source_adapter.platform_name:
            return content
            
        transformed = content
        
        # Apply path rewrites
        for pattern, replacement in self.path_rewrite_rules().items():
            transformed = re.sub(pattern, replacement, transformed)
            
        # Apply term rewrites
        for term, replacement in self.platform_term_rewrites().items():
            transformed = transformed.replace(term, replacement)
            
        return transformed

    def translate_rules(self, source_content: str, source_adapter: "PlatformAdapter") -> str:
        """
        Translate rules file content.
        Can be overridden for structural changes (e.g. 5-layer format).
        """
        return self.transform_content(source_content, source_adapter)

    def cleanup_foreign_artifacts(self, project_root: Path) -> List[Path]:
        """Remove artifacts from other platforms."""
        removed = []
        for pattern in self.foreign_artifact_patterns():
            target = project_root / pattern
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
                removed.append(target)
        return removed


class AntigravityAdapter(PlatformAdapter):
    """Adapter for Antigravity IDE conventions."""
    
    @property
    def platform_name(self) -> str:
        return "antigravity"
    
    def skill_path(self, name: str) -> Path:
        return Path(f".agent/skills/{name}/SKILL.md")
    
    def agent_path(self, name: str) -> Path:
        return Path(f".agent/agents/{name}.md")
    
    def knowledge_path(self, name: str) -> Path:
        return Path(f".agent/knowledge/{name}.json")
    
    def workflow_path(self, name: str) -> Path:
        return Path(f".agent/workflows/{name}.md")
    
    def template_path(self, name: str) -> Path:
        return Path(f".agent/templates/{name}")
    
    def protocol_path(self, name: str) -> Path:
        return Path(f"docs/protocol/{name}.md")
        
    def script_path(self, name: str) -> Path:
        return Path(f".agent/scripts/{name}")
    
    def rules_path(self) -> Path:
        return Path(".agentrules")
    
    def lib_path(self) -> Path:
        return Path("lib")
    
    def path_rewrite_rules(self) -> Dict[str, str]:
        return {
            r'\.cursor/skills/': '.agent/skills/',
            r'\.cursor/agents/': '.agent/agents/',
            r'\.cursor/config/': '.agent/config/',
            r'\.cursor/rules/': '.agent/rules/',
            r'\.cursor/': '.agent/',
            r'\.cursorrules': '.agentrules',
        }
    
    def platform_term_rewrites(self) -> Dict[str, str]:
        return {
            'Cursor Agent Factory': 'Antigravity Agent Factory',
            'Cursor IDE': 'Antigravity IDE',
            'Cursor agent system': 'agent system',
            'Cursor agent': 'agent',
        }
    
    def foreign_artifact_patterns(self) -> List[str]:
        return [".cursor", ".cursorrules"]
    
    def translate_rules(self, source_content: str, source_adapter: "PlatformAdapter") -> str:
        transformed = self.transform_content(source_content, source_adapter)
        
        # Ensure 5-layer header for Antigravity
        if not transformed.startswith("# Antigravity Agent System Rules"):
            header = (
                "# Antigravity Agent System Rules\n"
                "# Translated from source format via PABP\n\n"
            )
            # If source was flat, we might want to wrap it in a layer or just prepend header
            # For now, just prepend header to ensure validity
            transformed = header + transformed
            
        return transformed


class GenericAdapter(PlatformAdapter):
    """Adapter for generic/neutral platform."""
    
    @property
    def platform_name(self) -> str:
        return "generic"
    
    @property
    def skills_dir(self) -> Path:
        return Path("skills")
    
    @property
    def agents_dir(self) -> Path:
        return Path("agents")
    
    @property
    def knowledge_dir(self) -> Path:
        return Path("knowledge")
    
    @property
    def workflows_dir(self) -> Path:
        return Path("workflows")
    
    def skill_path(self, name: str) -> Path:
        return self.skills_dir / name / "SKILL.md"
    
    def agent_path(self, name: str) -> Path:
        return self.agents_dir / f"{name}.md"
    
    def knowledge_path(self, name: str) -> Path:
        return self.knowledge_dir / f"{name}.json"
    
    def workflow_path(self, name: str) -> Path:
        return self.workflows_dir / f"{name}.yaml"
    
    def template_path(self, name: str) -> Path:
        return Path(f"templates/{name}")
    
    def protocol_path(self, name: str) -> Path:
        return Path(f"docs/protocol/{name}.md")
        
    def script_path(self, name: str) -> Path:
        return Path(f"scripts/{name}")
    
    def rules_path(self) -> Path:
        return Path("rules/agentrules")
    
    def lib_path(self) -> Path:
        return Path("lib")
    
    def path_rewrite_rules(self) -> Dict[str, str]:
        return {
            r'\.cursor/skills/': 'skills/',
            r'\.cursor/agents/': 'agents/',
            r'\.cursor/': '',
            r'\.cursorrules': 'rules/agentrules',
            r'\.agent/skills/': 'skills/',
            r'\.agent/agents/': 'agents/',
            r'\.agent/': '',
            r'\.agentrules': 'rules/agentrules',
        }
    
    def platform_term_rewrites(self) -> Dict[str, str]:
        return {
            'Cursor Agent Factory': 'Agent Factory',
            'Cursor IDE': 'IDE',
            'Antigravity IDE': 'IDE',
        }
    
    def foreign_artifact_patterns(self) -> List[str]:
        return [".cursor", ".cursorrules", ".agent", ".agentrules"]


class CursorAdapter(PlatformAdapter):
    """Adapter for Cursor IDE (Canonical Source)."""
    
    @property
    def platform_name(self) -> str:
        return "cursor"
    
    @property
    def skills_dir(self) -> Path:
        return Path(".cursor/skills")
    
    @property
    def agents_dir(self) -> Path:
        return Path(".cursor/agents")
    
    @property
    def knowledge_dir(self) -> Path:
        return Path("knowledge")
    
    @property
    def workflows_dir(self) -> Path:
        return Path(".agent/patterns/workflows")
    
    def skill_path(self, name: str) -> Path:
        return self.skills_dir / name / "SKILL.md"
    
    def agent_path(self, name: str) -> Path:
        return self.agents_dir / f"{name}.md"
    
    def knowledge_path(self, name: str) -> Path:
        return self.knowledge_dir / f"{name}.json"
    
    def workflow_path(self, name: str) -> Path:
        return self.workflows_dir / f"{name}.json"
    
    def template_path(self, name: str) -> Path:
        return Path(f"templates/{name}")
    
    def protocol_path(self, name: str) -> Path:
        return Path(f"docs/protocol/{name}.md")
        
    def script_path(self, name: str) -> Path:
        return Path(f"scripts/{name}")
    
    def rules_path(self) -> Path:
        return Path(".cursorrules")
    
    def lib_path(self) -> Path:
        return Path("lib")
        
    def foreign_artifact_patterns(self) -> List[str]:
        return [".agent", ".agentrules"]


# Registry
_ADAPTERS: Dict[str, Type[PlatformAdapter]] = {
    "antigravity": AntigravityAdapter,
    "cursor": CursorAdapter,
    "generic": GenericAdapter,
}

def register_adapter(name: str, adapter_cls: Type[PlatformAdapter]) -> None:
    """Register a new platform adapter."""
    _ADAPTERS[name] = adapter_cls

def get_adapter(name: str) -> PlatformAdapter:
    """Get adapter by name."""
    adapter_cls = _ADAPTERS.get(name)
    if not adapter_cls:
        raise ValueError(f"Unknown platform adapter: {name}")
    return adapter_cls()

def detect_platform(project_root: Path) -> PlatformAdapter:
    """
    Detect platform from project structure.
    
    Priority:
    1. .agent/ directory (Antigravity)
    2. .cursor/ directory (Cursor)
    3. Fallback (Generic)
    """
    if (project_root / ".agent").exists():
        return AntigravityAdapter()
    elif (project_root / ".cursor").exists():
        return CursorAdapter()
    else:
        return GenericAdapter()
