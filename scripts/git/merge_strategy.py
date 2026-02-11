#!/usr/bin/env python3
"""
Antigravity Agent Factory - Merge Strategy Engine
Defines merge strategies, conflict detection, and resolution mechanisms
for onboarding existing repositories.

Usage:
    from scripts.git.merge_strategy import MergeEngine, ConflictResolution
    
    engine = MergeEngine(inventory, desired_config)
    conflicts = engine.detect_conflicts()
    engine.resolve_conflict(conflict, ConflictResolution.KEEP_EXISTING)

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import difflib
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from scripts.analysis.repo_analyzer import RepoInventory, get_file_hash


class ConflictResolution(Enum):
    """Options for resolving a conflict between existing and new artifacts.
    
    Attributes:
        KEEP_EXISTING: Preserve the existing file, skip the new one.
        REPLACE: Replace the existing file with the new one.
        MERGE: Attempt to intelligently merge the two files.
        RENAME_NEW: Create the new file with a suffix (e.g., -factory).
        SKIP: Skip this artifact entirely (don't create or modify).
    """
    KEEP_EXISTING = "keep"
    REPLACE = "replace"
    MERGE = "merge"
    RENAME_NEW = "rename"
    SKIP = "skip"


class ArtifactType(Enum):
    """Types of artifacts that can be managed.
    
    Attributes:
        CURSORRULES: The .agentrules file.
        AGENT: Agent definition in .agent/agents/.
        SKILL: Skill definition in .agent/skills/.
        COMMAND: Custom command in .agent/commands/.
        RULE: Custom rule in .agent/rules/.
        MCP_CONFIG: MCP configuration in .agent/mcp.json.        KNOWLEDGE: Knowledge file in knowledge/.
        TEMPLATE: Template file in templates/.
        WORKFLOW: Workflow file in workflows/.
        PURPOSE: PURPOSE.md file.
        PRACTICES: practices.yaml file.
        METHODOLOGY: workflows/methodology.yaml file.
    """
    CURSORRULES = "cursorrules"
    AGENT = "agent"
    SKILL = "skill"
    COMMAND = "command"
    RULE = "rule"
    MCP_CONFIG = "mcp_config"
    KNOWLEDGE = "knowledge"
    TEMPLATE = "template"
    WORKFLOW = "workflow"
    PURPOSE = "purpose"
    PRACTICES = "practices"
    METHODOLOGY = "methodology"


class MergeStrategy(Enum):
    """Default merge strategies for different artifact types.
    
    Attributes:
        MERGE: Attempt to merge existing and new content.
        ADD: Add new items without modifying existing ones.
        PRESERVE: Never modify, only inform user.
        REPLACE: Replace existing with new (use with caution).
    """
    MERGE = "merge"
    ADD = "add"
    PRESERVE = "preserve"
    REPLACE = "replace"


# Default strategies for each artifact type
DEFAULT_STRATEGIES: Dict[ArtifactType, MergeStrategy] = {
    ArtifactType.CURSORRULES: MergeStrategy.MERGE,    ArtifactType.AGENT: MergeStrategy.ADD,
    ArtifactType.SKILL: MergeStrategy.ADD,
    ArtifactType.COMMAND: MergeStrategy.PRESERVE,  # User custom
    ArtifactType.RULE: MergeStrategy.PRESERVE,     # User custom
    ArtifactType.MCP_CONFIG: MergeStrategy.MERGE,
    ArtifactType.KNOWLEDGE: MergeStrategy.MERGE,
    ArtifactType.TEMPLATE: MergeStrategy.ADD,
    ArtifactType.WORKFLOW: MergeStrategy.ADD,
    ArtifactType.PURPOSE: MergeStrategy.PRESERVE,  # User custom
    ArtifactType.PRACTICES: MergeStrategy.PRESERVE,
    ArtifactType.METHODOLOGY: MergeStrategy.PRESERVE,
}


@dataclass
class Conflict:
    """Represents a conflict between existing and new artifact.
    
    Attributes:
        artifact_type: Type of the artifact (agent, skill, etc.).
        artifact_name: Name of the artifact.
        existing_path: Path to the existing file.
        new_content: Content that would be written.
        existing_hash: MD5 hash of existing content.
        new_hash: MD5 hash of new content.
        diff_summary: Human-readable summary of differences.
        diff_lines: Detailed diff output.
    """
    artifact_type: ArtifactType
    artifact_name: str
    existing_path: Path
    new_content: str
    existing_hash: str = ""
    new_hash: str = ""
    diff_summary: str = ""
    diff_lines: List[str] = field(default_factory=list)
    
    def get_existing_content(self) -> str:
        """Read the existing file content.
        
        Returns:
            Content of the existing file, or empty string if not readable.
        """
        if not self.existing_path.exists():
            return ""
        try:
            return self.existing_path.read_text(encoding="utf-8")
        except Exception:
            return ""


@dataclass
class ConflictPrompt:
    """Prompt for user to resolve a conflict.
    
    Attributes:
        conflict: The conflict to resolve.
        options: Available resolution options.
        recommendation: Recommended resolution.
        reason: Explanation for the recommendation.
    """
    conflict: Conflict
    options: List[ConflictResolution]
    recommendation: ConflictResolution
    reason: str
    
    def format_prompt(self) -> str:
        """Format the conflict as a user-friendly prompt.
        
        Returns:
            Formatted string for display to user.
        """
        lines = [
            f"=== CONFLICT: {self.conflict.artifact_type.value} '{self.conflict.artifact_name}' ===",
            "",
            f"Existing file: {self.conflict.existing_path}",
            "",
            "Differences:",
        ]
        
        if self.conflict.diff_summary:
            lines.append(self.conflict.diff_summary)
        else:
            lines.append("  (No detailed diff available)")
        
        lines.extend([
            "",
            f"Recommendation: {self.recommendation.value} - {self.reason}",
            "",
            "Options:",
        ])
        
        for i, option in enumerate(self.options, 1):
            marker = "*" if option == self.recommendation else " "
            lines.append(f"  {marker} [{i}] {option.value}")
        
        return "\n".join(lines)


@dataclass 
class MergeResult:
    """Result of a merge operation.
    
    Attributes:
        success: Whether the merge was successful.
        content: The merged content (if successful).
        message: Status message or error description.
        backup_created: Whether a backup was created.
        backup_path: Path to the backup file (if created).
    """
    success: bool
    content: str = ""
    message: str = ""
    backup_created: bool = False
    backup_path: Optional[Path] = None


class MergeEngine:
    """Engine for detecting and resolving conflicts during onboarding.
    
    This class handles the comparison of existing repository artifacts
    with desired factory configurations, detecting conflicts, and
    applying user-selected resolutions.
    
    Attributes:
        inventory: Analysis of the existing repository.
        factory_root: Path to the factory root.
        resolutions: User-selected resolutions for each conflict.
    """
    
    def __init__(
        self,
        inventory: RepoInventory,
        factory_root: Optional[Path] = None
    ):
        """Initialize the merge engine.
        
        Args:
            inventory: Repository inventory from analysis.
            factory_root: Path to factory root directory.
        """
        self.inventory = inventory
        self.factory_root = factory_root or Path(__file__).parent.parent.parent
        self.resolutions: Dict[str, ConflictResolution] = {}
        self._conflicts: List[Conflict] = []
    
    def detect_conflicts(
        self,
        desired_agents: List[str],
        desired_skills: List[str],
        desired_knowledge: List[str],
        new_cursorrules: Optional[str] = None,        new_mcp_servers: Optional[Dict[str, Any]] = None,
    ) -> List[Conflict]:
        """Detect all conflicts between existing and desired artifacts.
        
        Args:
            desired_agents: List of agent names to generate.
            desired_skills: List of skill names to generate.
            desired_knowledge: List of knowledge file names to generate.
            new_cursorrules: New .agentrules content (if generating).            new_mcp_servers: New MCP server configurations (if any).
            
        Returns:
            List of detected conflicts.
        """
        conflicts: List[Conflict] = []
        
        # Check .agentrules conflict
        if new_cursorrules and self.inventory.agentrules.exists:
            conflict = self._create_cursorrules_conflict(new_cursorrules)
            if conflict:
                conflicts.append(conflict)
        
        # Check agent conflicts
        for agent_name in desired_agents:
            if agent_name in self.inventory.existing_agents:
                conflict = self._create_agent_conflict(agent_name)
                if conflict:
                    conflicts.append(conflict)
        
        # Check skill conflicts
        for skill_name in desired_skills:
            if skill_name in self.inventory.existing_skills:
                conflict = self._create_skill_conflict(skill_name)
                if conflict:
                    conflicts.append(conflict)
        
        # Check knowledge file conflicts
        for knowledge_name in desired_knowledge:
            if knowledge_name in self.inventory.existing_knowledge:
                conflict = self._create_knowledge_conflict(knowledge_name)
                if conflict:
                    conflicts.append(conflict)
        
        # Check MCP config conflicts
        if new_mcp_servers and self.inventory.mcp.exists:
            conflict = self._create_mcp_conflict(new_mcp_servers)
            if conflict:
                conflicts.append(conflict)
        
        self._conflicts = conflicts
        return conflicts
    
    def _create_cursorrules_conflict(self, new_content: str) -> Optional[Conflict]:
        """Create a conflict for .agentrules if content differs.
        
        Args:
            new_content: The new .agentrules content.            
        Returns:
            Conflict if files differ, None otherwise.
        """
        existing_path = self.inventory.path / ".agentrules"
        existing_content = self.inventory.agentrules.content or ""        
        existing_hash = get_file_hash(existing_path)
        import hashlib
        new_hash = hashlib.md5(new_content.encode()).hexdigest()
        
        if existing_hash == new_hash:
            return None
        
        diff_lines = list(difflib.unified_diff(
            existing_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile="existing/.agentrules",
            tofile="new/.agentrules",            lineterm=""
        ))
        
        # Create summary
        additions = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
        deletions = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
        diff_summary = f"+{additions} lines, -{deletions} lines"
        
        return Conflict(
            artifact_type=ArtifactType.CURSORRULES,
            artifact_name=".agentrules",            existing_path=existing_path,
            new_content=new_content,
            existing_hash=existing_hash,
            new_hash=new_hash,
            diff_summary=diff_summary,
            diff_lines=diff_lines,
        )
    
    def _create_agent_conflict(self, agent_name: str) -> Optional[Conflict]:
        """Create a conflict for an agent if it exists.
        
        Args:
            agent_name: Name of the agent.
            
        Returns:
            Conflict if agent exists with different content, None otherwise.
        """
        existing_path = self.inventory.path / ".agent" / "agents" / f"{agent_name}.md"        
        if not existing_path.exists():
            return None
        
        # Load the factory pattern for comparison
        pattern_path = self.factory_root / "patterns" / "agents" / f"{agent_name}.json"
        if not pattern_path.exists():
            return None  # No factory pattern to compare
        
        existing_hash = get_file_hash(existing_path)
        
        return Conflict(
            artifact_type=ArtifactType.AGENT,
            artifact_name=agent_name,
            existing_path=existing_path,
            new_content="",  # Will be generated later
            existing_hash=existing_hash,
            diff_summary="Agent already exists with custom configuration",
        )
    
    def _create_skill_conflict(self, skill_name: str) -> Optional[Conflict]:
        """Create a conflict for a skill if it exists.
        
        Args:
            skill_name: Name of the skill.
            
        Returns:
            Conflict if skill exists with different content, None otherwise.
        """
        existing_path = self.inventory.path / ".agent" / "skills" / skill_name / "SKILL.md"        
        if not existing_path.exists():
            return None
        
        existing_hash = get_file_hash(existing_path)
        
        return Conflict(
            artifact_type=ArtifactType.SKILL,
            artifact_name=skill_name,
            existing_path=existing_path,
            new_content="",  # Will be generated later
            existing_hash=existing_hash,
            diff_summary="Skill already exists with custom configuration",
        )
    
    def _create_knowledge_conflict(self, knowledge_name: str) -> Optional[Conflict]:
        """Create a conflict for a knowledge file if it exists.
        
        Args:
            knowledge_name: Name of the knowledge file.
            
        Returns:
            Conflict if file exists with different content, None otherwise.
        """
        existing_path = self.inventory.path / "knowledge" / knowledge_name
        
        if not existing_path.exists():
            return None
        
        existing_hash = get_file_hash(existing_path)
        
        return Conflict(
            artifact_type=ArtifactType.KNOWLEDGE,
            artifact_name=knowledge_name,
            existing_path=existing_path,
            new_content="",  # Will be generated later
            existing_hash=existing_hash,
            diff_summary="Knowledge file already exists",
        )
    
    def _create_mcp_conflict(self, new_servers: Dict[str, Any]) -> Optional[Conflict]:
        """Create a conflict for MCP configuration if servers overlap.
        
        Args:
            new_servers: New MCP server configurations.
            
        Returns:
            Conflict if there are overlapping server names, None otherwise.
        """
        existing_path = self.inventory.path / ".agent" / "mcp.json"        
        overlapping = set(new_servers.keys()) & set(self.inventory.mcp.servers)
        
        if not overlapping:
            return None  # No conflicts, can merge
        
        existing_hash = get_file_hash(existing_path)
        
        return Conflict(
            artifact_type=ArtifactType.MCP_CONFIG,
            artifact_name="mcp.json",
            existing_path=existing_path,
            new_content=json.dumps({"mcpServers": new_servers}, indent=2),
            existing_hash=existing_hash,
            diff_summary=f"Overlapping servers: {', '.join(overlapping)}",
        )
    
    def get_conflict_prompt(self, conflict: Conflict) -> ConflictPrompt:
        """Generate a prompt for resolving a conflict.
        
        Args:
            conflict: The conflict to create a prompt for.
            
        Returns:
            ConflictPrompt with options and recommendation.
        """
        # Determine available options based on artifact type
        if conflict.artifact_type in (ArtifactType.COMMAND, ArtifactType.RULE):
            # User custom artifacts - only inform, don't offer to replace
            options = [ConflictResolution.KEEP_EXISTING, ConflictResolution.SKIP]
            recommendation = ConflictResolution.KEEP_EXISTING
            reason = "Custom user artifact - preserving original"
        elif conflict.artifact_type == ArtifactType.CURSORRULES:
            options = [
                ConflictResolution.KEEP_EXISTING,
                ConflictResolution.REPLACE,
                ConflictResolution.MERGE,
            ]
            recommendation = ConflictResolution.MERGE
            reason = "Merge preserves existing customizations while adding new sections"
        elif conflict.artifact_type == ArtifactType.MCP_CONFIG:
            options = [
                ConflictResolution.KEEP_EXISTING,
                ConflictResolution.MERGE,
                ConflictResolution.REPLACE,
            ]
            recommendation = ConflictResolution.MERGE
            reason = "Merge adds new servers without removing existing ones"
        elif conflict.artifact_type == ArtifactType.KNOWLEDGE:
            options = [
                ConflictResolution.KEEP_EXISTING,
                ConflictResolution.MERGE,
                ConflictResolution.REPLACE,
            ]
            recommendation = ConflictResolution.MERGE
            reason = "Merge combines knowledge from both sources"
        else:
            # Agents, skills, templates, workflows
            options = [
                ConflictResolution.KEEP_EXISTING,
                ConflictResolution.REPLACE,
                ConflictResolution.RENAME_NEW,
            ]
            recommendation = ConflictResolution.KEEP_EXISTING
            reason = "Preserve existing customizations"
        
        return ConflictPrompt(
            conflict=conflict,
            options=options,
            recommendation=recommendation,
            reason=reason,
        )
    
    def set_resolution(self, conflict: Conflict, resolution: ConflictResolution) -> None:
        """Record a resolution for a conflict.
        
        Args:
            conflict: The conflict being resolved.
            resolution: The chosen resolution.
        """
        key = f"{conflict.artifact_type.value}:{conflict.artifact_name}"
        self.resolutions[key] = resolution
    
    def get_resolution(self, conflict: Conflict) -> Optional[ConflictResolution]:
        """Get the recorded resolution for a conflict.
        
        Args:
            conflict: The conflict to look up.
            
        Returns:
            The resolution if set, None otherwise.
        """
        key = f"{conflict.artifact_type.value}:{conflict.artifact_name}"
        return self.resolutions.get(key)
    
    def should_skip_artifact(
        self,
        artifact_type: ArtifactType,
        artifact_name: str
    ) -> bool:
        """Check if an artifact should be skipped based on resolutions.
        
        Args:
            artifact_type: Type of the artifact.
            artifact_name: Name of the artifact.
            
        Returns:
            True if the artifact should be skipped.
        """
        key = f"{artifact_type.value}:{artifact_name}"
        resolution = self.resolutions.get(key)
        
        if resolution is None:
            return False
        
        return resolution in (
            ConflictResolution.KEEP_EXISTING,
            ConflictResolution.SKIP
        )
    
    def should_rename_artifact(
        self,
        artifact_type: ArtifactType,
        artifact_name: str
    ) -> bool:
        """Check if an artifact should be renamed based on resolutions.
        
        Args:
            artifact_type: Type of the artifact.
            artifact_name: Name of the artifact.
            
        Returns:
            True if the artifact should be renamed.
        """
        key = f"{artifact_type.value}:{artifact_name}"
        resolution = self.resolutions.get(key)
        return resolution == ConflictResolution.RENAME_NEW
    
    def get_renamed_name(self, artifact_name: str) -> str:
        """Get the renamed version of an artifact name.
        
        Args:
            artifact_name: Original artifact name.
            
        Returns:
            Renamed artifact name with '-factory' suffix.
        """
        if "." in artifact_name:
            name, ext = artifact_name.rsplit(".", 1)
            return f"{name}-factory.{ext}"
        return f"{artifact_name}-factory"


def merge_json_files(
    existing_content: str,
    new_content: str,
    strategy: str = "deep"
) -> MergeResult:
    """Merge two JSON files.
    
    Args:
        existing_content: Content of the existing file.
        new_content: Content of the new file.
        strategy: Merge strategy ('deep' or 'shallow').
        
    Returns:
        MergeResult with merged content.
    """
    try:
        existing_data = json.loads(existing_content)
        new_data = json.loads(new_content)
        
        if strategy == "deep":
            merged = _deep_merge(existing_data, new_data)
        else:
            merged = {**existing_data, **new_data}
        
        return MergeResult(
            success=True,
            content=json.dumps(merged, indent=2),
            message="Successfully merged JSON files",
        )
    except json.JSONDecodeError as e:
        return MergeResult(
            success=False,
            message=f"JSON parsing error: {e}",
        )
    except Exception as e:
        return MergeResult(
            success=False,
            message=f"Merge error: {e}",
        )


def _deep_merge(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries.
    
    Args:
        base: Base dictionary.
        overlay: Dictionary to overlay on base.
        
    Returns:
        Merged dictionary with overlay values taking precedence.
    """
    result = base.copy()
    
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        elif key in result and isinstance(result[key], list) and isinstance(value, list):
            # Merge lists without duplicates
            existing_set = set(str(item) for item in result[key])
            for item in value:
                if str(item) not in existing_set:
                    result[key].append(item)
        else:
            result[key] = value
    
    return result


if __name__ == "__main__":
    print("Merge Strategy Engine - Use via import")
    print("Example:")
    print("  from scripts.git.merge_strategy import MergeEngine")
    print("  engine = MergeEngine(inventory)")
    print("  conflicts = engine.detect_conflicts(...)")
