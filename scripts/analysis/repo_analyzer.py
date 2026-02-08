#!/usr/bin/env python3
"""
Antigravity Agent Factory - Repository Analyzer

Analyzes existing repositories to detect Antigravity artifacts, tech stack,and determine the appropriate onboarding scenario.

Usage:
    from scripts.analysis.repo_analyzer import RepoAnalyzer
    
    analyzer = RepoAnalyzer(repo_path)
    inventory = analyzer.analyze()
    print(inventory.scenario)

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

import json
import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union


class OnboardingScenario(Enum):
    """Scenarios for repository onboarding.
    
    Attributes:
        FRESH: No Antigravity artifacts exist - full generation needed.
        MINIMAL: Only .agentrules exists - augment with agents, skills, etc.        PARTIAL: Some artifacts exist but others are missing.
        UPGRADE: Old factory version detected - offer upgrade.
        COMPLETE: Fully configured repository - report status only.
    """
    FRESH = "fresh"
    MINIMAL = "minimal"
    PARTIAL = "partial"
    UPGRADE = "upgrade"
    COMPLETE = "complete"


@dataclass
class AntigravityruleAnalysis:
    """Analysis of an existing .agentrules file.    
    Attributes:
        exists: Whether the file exists.
        content: Raw content of the file.
        version: Factory version if present (from marker comment).
        layers_present: Which layers (0-4) are detected in the file.
        has_factory_marker: Whether the file has factory generation marker.
        line_count: Number of lines in the file.
    """
    exists: bool = False
    content: Optional[str] = None
    version: Optional[str] = None
    layers_present: List[int] = field(default_factory=list)
    has_factory_marker: bool = False
    line_count: int = 0


@dataclass
class McpAnalysis:
    """Analysis of MCP configuration.
    
    Attributes:
        exists: Whether mcp.json exists.
        servers: List of configured server names.
        server_details: Full server configuration details.
    """
    exists: bool = False
    servers: List[str] = field(default_factory=list)
    server_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TechStackDetection:
    """Detected technology stack from repository.
    
    Attributes:
        languages: Detected programming languages.
        frameworks: Detected frameworks.
        databases: Detected database technologies.
        suggested_blueprint: Best matching blueprint ID.
        confidence: Confidence score (0.0 to 1.0).
    """
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    suggested_blueprint: Optional[str] = None
    confidence: float = 0.0


@dataclass
class RepoInventory:
    """Complete inventory of Antigravity artifacts in a repository.    
    This dataclass contains all information gathered during repository
    analysis, including existing artifacts, detected tech stack, and
    the determined onboarding scenario.
    
    Attributes:
        path: Path to the repository.
        scenario: Detected onboarding scenario.
        cursorrules: Analysis of .agentrules file.
        mcp: Analysis of MCP configuration.
        tech_stack: Detected technology stack.
        existing_agents: Agent names from .agent/agents/.
        existing_skills: Skill names from .agent/skills/.
        existing_commands: Command names from .agent/commands/.
        existing_rules: Rule file names from .agent/rules/.        existing_knowledge: Knowledge file names from knowledge/.
        existing_templates: Template file names from templates/.
        existing_workflows: Workflow file names from workflows/.
        has_purpose_md: Whether PURPOSE.md exists.
        has_practices_yaml: Whether practices.yaml exists.
        has_methodology_yaml: Whether workflows/methodology.yaml exists.
        has_readme: Whether README.md exists.
        is_git_repo: Whether repository is git initialized.
    """
    path: Path
    scenario: OnboardingScenario = OnboardingScenario.FRESH
    
    # Detailed analysis
    cursorrules: AntigravityruleAnalysis = field(default_factory=AntigravityruleAnalysis)
    mcp: McpAnalysis = field(default_factory=McpAnalysis)
    tech_stack: TechStackDetection = field(default_factory=TechStackDetection)
    
    # .agent/ folder contents    existing_agents: List[str] = field(default_factory=list)
    existing_skills: List[str] = field(default_factory=list)
    existing_commands: List[str] = field(default_factory=list)
    existing_rules: List[str] = field(default_factory=list)
    
    # Project-level artifacts
    existing_knowledge: List[str] = field(default_factory=list)
    existing_templates: List[str] = field(default_factory=list)
    existing_workflows: List[str] = field(default_factory=list)
    
    # Special files
    has_purpose_md: bool = False
    has_practices_yaml: bool = False
    has_methodology_yaml: bool = False
    has_readme: bool = False
    is_git_repo: bool = False
    
    def get_summary(self) -> str:
        """Generate a human-readable summary of the inventory.
        
        Returns:
            Formatted string summarizing the repository state.
        """
        lines = [
            f"Repository: {self.path}",
            f"Scenario: {self.scenario.value.upper()}",
            "",
            "=== Antigravity Artifacts ===",
            f".agentrules: {'Yes' if self.agentrules.exists else 'No'}",
        ]
        
        if self.agentrules.exists:
            lines.append(f"  - Lines: {self.agentrules.line_count}")
            lines.append(f"  - Layers: {self.agentrules.layers_present}")
            lines.append(f"  - Factory version: {self.agentrules.version or 'Unknown'}")        
        lines.extend([
            f"Agents: {len(self.existing_agents)} ({', '.join(self.existing_agents) or 'None'})",
            f"Skills: {len(self.existing_skills)} ({', '.join(self.existing_skills) or 'None'})",
            f"Commands: {len(self.existing_commands)} ({', '.join(self.existing_commands) or 'None'})",
            f"Rules: {len(self.existing_rules)} ({', '.join(self.existing_rules) or 'None'})",
            f"MCP Servers: {len(self.mcp.servers)} ({', '.join(self.mcp.servers) or 'None'})",
            "",
            "=== Project Artifacts ===",
            f"Knowledge files: {len(self.existing_knowledge)}",
            f"Templates: {len(self.existing_templates)}",
            f"Workflows: {len(self.existing_workflows)}",
            f"PURPOSE.md: {'Yes' if self.has_purpose_md else 'No'}",
            f"practices.yaml: {'Yes' if self.has_practices_yaml else 'No'}",
            f"methodology.yaml: {'Yes' if self.has_methodology_yaml else 'No'}",
            "",
            "=== Tech Stack ===",
            f"Languages: {', '.join(self.tech_stack.languages) or 'Unknown'}",
            f"Frameworks: {', '.join(self.tech_stack.frameworks) or 'Unknown'}",
            f"Suggested Blueprint: {self.tech_stack.suggested_blueprint or 'None'}",
        ])
        
        return "\n".join(lines)


class RepoAnalyzer:
    """Analyzes existing repositories for Antigravity artifacts and tech stack.
    
    This class scans a repository to detect existing Antigravity Agent Factory    artifacts, determine the technology stack, and recommend an onboarding
    scenario.
    
    Attributes:
        repo_path: Path to the repository to analyze.
        factory_root: Path to the factory root (for blueprint matching).
    
    Example:
        >>> analyzer = RepoAnalyzer(Path("C:/Projects/my-repo"))
        >>> inventory = analyzer.analyze()
        >>> print(inventory.scenario)
        OnboardingScenario.PARTIAL
    """
    
    # Blueprint matching configuration
    BLUEPRINT_MATCHERS = {
        "python-fastapi": {
            "languages": ["python"],
            "frameworks": ["fastapi"],
            "indicators": ["requirements.txt", "pyproject.toml"],
        },
        "typescript-react": {
            "languages": ["typescript"],
            "frameworks": ["react"],
            "indicators": ["package.json", "tsconfig.json"],
        },
        "java-spring": {
            "languages": ["java"],
            "frameworks": ["spring"],
            "indicators": ["pom.xml", "build.gradle"],
        },
        "kotlin-spring": {
            "languages": ["kotlin"],
            "frameworks": ["spring"],
            "indicators": ["build.gradle.kts"],
        },
        "csharp-dotnet": {
            "languages": ["csharp"],
            "frameworks": ["dotnet", "aspnet"],
            "indicators": ["*.csproj", "*.sln"],
        },
        "sap-abap": {
            "languages": ["abap"],
            "frameworks": [],
            "indicators": [],
        },
        "sap-cpi-pi": {
            "languages": ["groovy"],
            "frameworks": ["cpi"],
            "indicators": ["iflow", "*.iflw"],
        },
    }
    
    # File extension to language mapping
    LANGUAGE_EXTENSIONS = {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".java": "java",
        ".kt": "kotlin",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".groovy": "groovy",
    }
    
    # Factory version pattern in .agentrules
    FACTORY_VERSION_PATTERN = re.compile(
        r"Generated by[:\s]+Antigravity Agent Factory.*?v?(\d+\.\d+(?:\.\d+)?)",        re.IGNORECASE
    )
    
    # Layer detection patterns
    LAYER_PATTERNS = {
        0: re.compile(r"Layer\s*0|LAYER\s*0|Integrity|Axioms?", re.IGNORECASE),
        1: re.compile(r"Layer\s*1|LAYER\s*1|Purpose", re.IGNORECASE),
        2: re.compile(r"Layer\s*2|LAYER\s*2|Principles?", re.IGNORECASE),
        3: re.compile(r"Layer\s*3|LAYER\s*3|Methodology", re.IGNORECASE),
        4: re.compile(r"Layer\s*4|LAYER\s*4|Technical", re.IGNORECASE),
    }
    
    def __init__(self, repo_path: Union[str, Path], factory_root: Optional[Path] = None):
        """Initialize the analyzer.
        
        Args:
            repo_path: Path to the repository to analyze.
            factory_root: Optional path to factory root for blueprint matching.
        """
        self.repo_path = Path(repo_path)
        self.factory_root = factory_root or Path(__file__).parent.parent.parent
        
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
    
    def analyze(self) -> RepoInventory:
        """Perform complete analysis of the repository.
        
        Returns:
            RepoInventory containing all detected artifacts and recommendations.
        """
        inventory = RepoInventory(path=self.repo_path)
        
        # Check git status
        inventory.is_git_repo = (self.repo_path / ".git").exists()
        
        # Analyze .agentrules
        inventory.agentrules = self._analyze_cursorrules()
        
        # Analyze .agent/ folder
        self._analyze_cursor_folder(inventory)        
        # Analyze project-level artifacts
        self._analyze_project_artifacts(inventory)
        
        # Detect tech stack
        inventory.tech_stack = self._detect_tech_stack()
        
        # Determine scenario
        inventory.scenario = self._determine_scenario(inventory)
        
        return inventory
    
    def _analyze_cursorrules(self) -> AntigravityruleAnalysis:
        """Analyze the .agentrules file if it exists.
        
        Returns:
            AntigravityruleAnalysis with file details.
        """
        analysis = AntigravityruleAnalysis()
        cursorrules_path = self.repo_path / ".agentrules"
        
        if not cursorrules_path.exists():            return analysis
        
        analysis.exists = True
        
        try:
            content = cursorrules_path.read_text(encoding="utf-8")            analysis.content = content
            analysis.line_count = len(content.splitlines())
            
            # Check for factory marker
            analysis.has_factory_marker = "Antigravity Agent Factory" in content            
            # Extract version
            version_match = self.FACTORY_VERSION_PATTERN.search(content)
            if version_match:
                analysis.version = version_match.group(1)
            
            # Detect layers
            for layer_num, pattern in self.LAYER_PATTERNS.items():
                if pattern.search(content):
                    analysis.layers_present.append(layer_num)
            
            analysis.layers_present.sort()
            
        except Exception as e:
            print(f"Warning: Could not read .agentrules: {e}")
        
        return analysis
    
    def _analyze_cursor_folder(self, inventory: RepoInventory) -> None:
        """Analyze the .agent/ folder contents.        
        Args:
            inventory: RepoInventory to populate with findings.
        """
        cursor_path = self.repo_path / ".agent"
        
        if not cursor_path.exists():
            return
        
        # Analyze agents
        agents_path = cursor_path / "agents"        if agents_path.exists():
            inventory.existing_agents = [
                f.stem for f in agents_path.glob("*.md")
            ]
        
        # Analyze skills
        skills_path = cursor_path / "skills"        if skills_path.exists():
            inventory.existing_skills = [
                d.name for d in skills_path.iterdir()
                if d.is_dir() and (d / "SKILL.md").exists()
            ]
        
        # Analyze commands
        commands_path = cursor_path / "commands"        if commands_path.exists():
            inventory.existing_commands = [
                f.stem for f in commands_path.glob("*.md")
            ]
        
        # Analyze rules
        rules_path = cursor_path / "rules"        if rules_path.exists():
            inventory.existing_rules = [
                f.name for f in rules_path.glob("*.mdc")
            ]
        
        # Analyze MCP configuration
        mcp_path = cursor_path / "mcp.json"        if mcp_path.exists():
            inventory.mcp = self._analyze_mcp(mcp_path)
    
    def _analyze_mcp(self, mcp_path: Path) -> McpAnalysis:
        """Analyze the MCP configuration file.
        
        Args:
            mcp_path: Path to mcp.json file.
            
        Returns:
            McpAnalysis with server details.
        """
        analysis = McpAnalysis(exists=True)
        
        try:
            with open(mcp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            servers = data.get("mcpServers", {})
            analysis.servers = list(servers.keys())
            analysis.server_details = servers
            
        except Exception as e:
            print(f"Warning: Could not parse mcp.json: {e}")
        
        return analysis
    
    def _analyze_project_artifacts(self, inventory: RepoInventory) -> None:
        """Analyze project-level artifacts.
        
        Args:
            inventory: RepoInventory to populate with findings.
        """
        # Knowledge files
        knowledge_path = self.repo_path / "knowledge"
        if knowledge_path.exists():
            inventory.existing_knowledge = [
                f.name for f in knowledge_path.glob("*.json")
            ]
        
        # Templates
        templates_path = self.repo_path / "templates"
        if templates_path.exists():
            inventory.existing_templates = [
                str(f.relative_to(templates_path))
                for f in templates_path.rglob("*")
                if f.is_file()
            ]
        
        # Workflows
        workflows_path = self.repo_path / "workflows"
        if workflows_path.exists():
            inventory.existing_workflows = [
                f.name for f in workflows_path.glob("*")
                if f.is_file()
            ]
        
        # Special files
        inventory.has_purpose_md = (self.repo_path / "PURPOSE.md").exists()
        inventory.has_practices_yaml = (self.repo_path / "practices.yaml").exists()
        inventory.has_methodology_yaml = (
            self.repo_path / "workflows" / "methodology.yaml"
        ).exists()
        inventory.has_readme = (self.repo_path / "README.md").exists()
    
    def _detect_tech_stack(self) -> TechStackDetection:
        """Detect the technology stack from repository files.
        
        Returns:
            TechStackDetection with languages, frameworks, and blueprint.
        """
        detection = TechStackDetection()
        
        # Detect languages from file extensions
        languages: Set[str] = set()
        for ext, lang in self.LANGUAGE_EXTENSIONS.items():
            if list(self.repo_path.rglob(f"*{ext}")):
                languages.add(lang)
        detection.languages = sorted(languages)
        
        # Detect frameworks from config files
        frameworks: Set[str] = set()
        
        # Python frameworks
        if self._file_contains("requirements.txt", "fastapi"):
            frameworks.add("fastapi")
        if self._file_contains("requirements.txt", "django"):
            frameworks.add("django")
        if self._file_contains("requirements.txt", "flask"):
            frameworks.add("flask")
        if self._file_contains("pyproject.toml", "fastapi"):
            frameworks.add("fastapi")
        
        # JavaScript/TypeScript frameworks
        if self._file_contains("package.json", "react"):
            frameworks.add("react")
        if self._file_contains("package.json", "next"):
            frameworks.add("nextjs")
        if self._file_contains("package.json", "vue"):
            frameworks.add("vue")
        if self._file_contains("package.json", "angular"):
            frameworks.add("angular")
        
        # Java/Kotlin frameworks
        if self._file_contains("pom.xml", "spring"):
            frameworks.add("spring")
        if self._file_contains("build.gradle", "spring"):
            frameworks.add("spring")
        if self._file_contains("build.gradle.kts", "spring"):
            frameworks.add("spring")
        
        # .NET frameworks
        if list(self.repo_path.rglob("*.csproj")):
            frameworks.add("dotnet")
            if self._any_file_contains("*.csproj", "Microsoft.AspNetCore"):
                frameworks.add("aspnet")
        
        detection.frameworks = sorted(frameworks)
        
        # Match to blueprint
        detection.suggested_blueprint, detection.confidence = self._match_blueprint(
            detection.languages, detection.frameworks
        )
        
        return detection
    
    def _file_contains(self, filename: str, search_text: str) -> bool:
        """Check if a file contains specific text.
        
        Args:
            filename: Name of file to check.
            search_text: Text to search for (case-insensitive).
            
        Returns:
            True if file exists and contains the text.
        """
        file_path = self.repo_path / filename
        if not file_path.exists():
            return False
        
        try:
            content = file_path.read_text(encoding="utf-8").lower()
            return search_text.lower() in content
        except Exception:
            return False
    
    def _any_file_contains(self, pattern: str, search_text: str) -> bool:
        """Check if any file matching pattern contains specific text.
        
        Args:
            pattern: Glob pattern for files.
            search_text: Text to search for (case-insensitive).
            
        Returns:
            True if any matching file contains the text.
        """
        for file_path in self.repo_path.rglob(pattern):
            try:
                content = file_path.read_text(encoding="utf-8").lower()
                if search_text.lower() in content:
                    return True
            except Exception:
                continue
        return False
    
    def _match_blueprint(
        self, languages: List[str], frameworks: List[str]
    ) -> tuple[Optional[str], float]:
        """Match detected stack to a blueprint.
        
        Args:
            languages: Detected programming languages.
            frameworks: Detected frameworks.
            
        Returns:
            Tuple of (blueprint_id, confidence_score).
        """
        best_match: Optional[str] = None
        best_score = 0.0
        
        for blueprint_id, matcher in self.BLUEPRINT_MATCHERS.items():
            score = 0.0
            
            # Check languages
            lang_matches = set(languages) & set(matcher["languages"])
            if lang_matches:
                score += len(lang_matches) * 0.4
            
            # Check frameworks
            framework_matches = set(frameworks) & set(matcher["frameworks"])
            if framework_matches:
                score += len(framework_matches) * 0.6
            
            if score > best_score:
                best_score = score
                best_match = blueprint_id
        
        return best_match, min(best_score, 1.0)
    
    def _determine_scenario(self, inventory: RepoInventory) -> OnboardingScenario:
        """Determine the onboarding scenario based on inventory.
        
        Args:
            inventory: Completed inventory of the repository.
            
        Returns:
            Appropriate OnboardingScenario.
        """
        has_cursorrules = inventory.agentrules.exists
        has_cursor_folder = bool(            inventory.existing_agents or
            inventory.existing_skills or
            inventory.existing_commands or
            inventory.existing_rules or
            inventory.mcp.exists
        )
        has_project_artifacts = bool(
            inventory.existing_knowledge or
            inventory.has_purpose_md or
            inventory.has_practices_yaml or
            inventory.has_methodology_yaml
        )
        
        # FRESH: No Antigravity artifacts at all
        if not has_cursorrules and not has_cursor_folder and not has_project_artifacts:
            return OnboardingScenario.FRESH
        
        # MINIMAL: Only .agentrules exists
        if has_cursorrules and not has_cursor_folder and not has_project_artifacts:
            return OnboardingScenario.MINIMAL
        
        # Check for UPGRADE scenario
        if inventory.agentrules.has_factory_marker:
            # If there's a version and it's old, suggest upgrade
            if inventory.agentrules.version:
                try:
                    major = int(inventory.agentrules.version.split(".")[0])                    if major < 2:  # Current version is 2.x
                        return OnboardingScenario.UPGRADE
                except ValueError:
                    pass
        
        # COMPLETE: Has all major components
        complete_indicators = [
            has_cursorrules,            len(inventory.existing_agents) >= 3,
            len(inventory.existing_skills) >= 3,
            inventory.has_purpose_md,
            inventory.has_practices_yaml or inventory.has_methodology_yaml,
        ]
        
        if all(complete_indicators):
            return OnboardingScenario.COMPLETE
        
        # PARTIAL: Has some but not all artifacts
        return OnboardingScenario.PARTIAL


def get_file_hash(file_path: Path) -> str:
    """Calculate MD5 hash of a file's contents.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        MD5 hash string.
    """
    if not file_path.exists():
        return ""
    
    try:
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()
    except Exception:
        return ""


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python repo_analyzer.py <repository_path>")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1])
    
    try:
        analyzer = RepoAnalyzer(repo_path)
        inventory = analyzer.analyze()
        print(inventory.get_summary())
    except Exception as e:
        print(f"Error analyzing repository: {e}")
        sys.exit(1)
