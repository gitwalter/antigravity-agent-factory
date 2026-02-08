#!/usr/bin/env python3
"""
Antigravity Agent Factory - Project Generation Engine

This module generates complete Antigravity agent development systems based onrequirements configuration and blueprint templates.

Supports two modes:
1. Fresh generation: Create new project from scratch
2. Onboarding: Integrate into existing repository non-destructively

Usage:
    from scripts.core.generate_project import ProjectGenerator
    
    # Fresh generation
    generator = ProjectGenerator(config, target_dir)
    generator.generate()
    
    # Onboarding existing repo
    generator = ProjectGenerator(config, target_dir, onboarding_mode=True)
    generator.generate()

Author: Antigravity Agent FactoryVersion: 2.0.0
"""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Import template engine
try:
    from scripts.core.template_engine import TemplateEngine, create_engine
    TEMPLATE_ENGINE_AVAILABLE = True
except ImportError:
    TEMPLATE_ENGINE_AVAILABLE = False

# Import onboarding components
try:
    from scripts.analysis.repo_analyzer import RepoAnalyzer, RepoInventory, OnboardingScenario
    from scripts.git.merge_strategy import (
        MergeEngine, ArtifactType, ConflictResolution, Conflict, ConflictPrompt
    )
    from scripts.git.backup_manager import BackupManager, BackupSession
    ONBOARDING_AVAILABLE = True
except ImportError:
    ONBOARDING_AVAILABLE = False


# =============================================================================
# QUICKSTART CONFIGURATION
# Pre-defined configuration for zero-config quick start experience
# =============================================================================

QUICKSTART_CONFIG = {
    "project_name": "TaskMaster Demo",
    "project_description": "AI-powered task management API - a demo project showcasing Antigravity Agent Factory capabilities",    "domain": "web, productivity, api",
    "primary_language": "python",
    "frameworks": ["fastapi", "sqlalchemy", "pydantic"],
    "triggers": ["jira", "confluence", "manual"],
    "agents": ["code-reviewer", "test-generator", "explorer"],
    "skills": ["bugfix-workflow", "feature-workflow", "tdd", "grounding"],
    "mcp_servers": [
        {
            "name": "atlassian",
            "url": "https://mcp.atlassian.com/v1/sse",
            "purpose": "Jira/Confluence integration for tickets and specs"
        }
    ],
    "style_guide": "pep8",
    "blueprint_id": "python-fastapi",
    "team_context": "Demo project for learning Antigravity Agent Factory"}


def create_quickstart_config() -> 'ProjectConfig':
    """Create a ProjectConfig with sensible quickstart defaults.
    
    This configuration is designed to demonstrate the full capabilities
    of Antigravity Agent Factory with zero user input required.    
    Returns:
        ProjectConfig instance with demo project settings.
    """
    return ProjectConfig.from_dict(QUICKSTART_CONFIG)


@dataclass
class ProjectConfig:
    """Configuration for project generation.
    
    Attributes:
        project_name: Name of the project (used for directory and documentation).
        project_description: Brief description of the project.
        domain: Industry/domain context.
        primary_language: Main programming language.
        frameworks: List of frameworks to use.
        triggers: Workflow trigger sources (jira, confluence, github, etc.).
        agents: List of agent pattern IDs to include.
        skills: List of skill pattern IDs to include.
        mcp_servers: List of MCP server configurations.
        style_guide: Coding style guide preference.
        blueprint_id: Optional blueprint to use as base.
        team_context: Team size and experience context.
        pm_enabled: Whether to enable project management system.
        pm_backend: PM backend (github, jira, azure-devops, linear).
        pm_doc_backend: Documentation backend (github-wiki, confluence, azure-wiki, none).
        pm_methodology: PM methodology (scrum, kanban, hybrid, waterfall).
    """
    project_name: str
    project_description: str = ""
    domain: str = "general"
    primary_language: str = "python"
    frameworks: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    mcp_servers: List[Dict[str, Any]] = field(default_factory=list)
    style_guide: str = "default"
    blueprint_id: Optional[str] = None
    team_context: str = ""
    pm_enabled: bool = False
    pm_backend: Optional[str] = None
    pm_doc_backend: Optional[str] = None
    pm_methodology: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectConfig':
        """Create ProjectConfig from dictionary.
        
        Args:
            data: Dictionary containing configuration values.
            
        Returns:
            ProjectConfig instance.
        """
        return cls(
            project_name=data.get('project_name', 'new-project'),
            project_description=data.get('project_description', ''),
            domain=data.get('domain', 'general'),
            primary_language=data.get('primary_language', 'python'),
            frameworks=data.get('frameworks', []),
            triggers=data.get('triggers', []),
            agents=data.get('agents', []),
            skills=data.get('skills', []),
            mcp_servers=data.get('mcp_servers', []),
            style_guide=data.get('style_guide', 'default'),
            blueprint_id=data.get('blueprint_id'),
            team_context=data.get('team_context', ''),
            pm_enabled=data.get('pm_enabled', False),
            pm_backend=data.get('pm_backend'),
            pm_doc_backend=data.get('pm_doc_backend'),
            pm_methodology=data.get('pm_methodology')
        )
    
    def get_all_agents(self) -> List[str]:
        """Get all agents including PM agents if PM is enabled.
        
        Returns:
            List of all agent IDs to include.
        """
        agents = list(self.agents)
        if self.pm_enabled:
            pm_agents = ['product-owner', 'sprint-master', 'task-manager', 'reporting-agent']
            for agent in pm_agents:
                if agent not in agents:
                    agents.append(agent)
        return agents
    
    def get_all_skills(self) -> List[str]:
        """Get all skills including PM skills if PM is enabled.
        
        Returns:
            List of all skill IDs to include.
        """
        skills = list(self.skills)
        if self.pm_enabled:
            pm_skills = [
                'create-epic', 'create-story', 'create-task', 'estimate-task',
                'run-standup', 'plan-sprint', 'close-sprint', 'generate-burndown', 'health-check'
            ]
            for skill in pm_skills:
                if skill not in skills:
                    skills.append(skill)
        return skills
    
    @classmethod
    def from_yaml_file(cls, filepath: str) -> 'ProjectConfig':
        """Load configuration from YAML file.
        
        Args:
            filepath: Path to YAML configuration file.
            
        Returns:
            ProjectConfig instance.
        """
        import yaml
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'ProjectConfig':
        """Load configuration from JSON file.
        
        Args:
            filepath: Path to JSON configuration file.
            
        Returns:
            ProjectConfig instance.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


class ProjectGenerator:
    """Generates complete Antigravity agent projects.
    
    This class orchestrates the generation of a complete Antigravity agent    development system based on configuration and patterns.
    
    Supports two modes:
    1. Fresh generation (default): Create complete project from scratch
    2. Onboarding mode: Integrate into existing repository non-destructively
    
    Attributes:
        config: Project configuration.
        target_dir: Target directory for generated project.
        factory_root: Root directory of the factory.
        onboarding_mode: Whether to use non-destructive onboarding.
        dry_run: If True, preview changes without making them.
        conflict_resolver: Callback for resolving conflicts interactively.
    """
    
    def __init__(
        self,
        config: ProjectConfig,
        target_dir: str,
        onboarding_mode: bool = False,
        dry_run: bool = False,
        conflict_resolver: Optional[Callable[[ConflictPrompt], ConflictResolution]] = None    ):
        """Initialize the generator.
        
        Args:
            config: Project configuration.
            target_dir: Target directory for generated project.
            onboarding_mode: If True, use non-destructive onboarding.
            dry_run: If True, preview changes without making them.
            conflict_resolver: Optional callback for resolving conflicts.
                If not provided, uses default recommendations.
        """
        self.config = config
        self.target_dir = Path(target_dir)
        self.factory_root = Path(__file__).parent.parent.parent
        self.generated_files: List[str] = []
        self.errors: List[str] = []
        
        # Onboarding settings
        self.onboarding_mode = onboarding_mode
        self.dry_run = dry_run
        self.conflict_resolver = conflict_resolver
        
        # Onboarding state (populated during onboarding)
        self.inventory: Optional[RepoInventory] = None
        self.merge_engine: Optional[MergeEngine] = None
        self.backup_session: Optional[BackupSession] = None
        self.skipped_artifacts: List[str] = []
        self.merged_artifacts: List[str] = []
        
        # Initialize template engine
        self.template_engine: Optional[TemplateEngine] = None
        if TEMPLATE_ENGINE_AVAILABLE:
            try:
                self.template_engine = create_engine(self.factory_root)
            except Exception:
                pass  # Fall back to string replacement
        
    def generate(self) -> Dict[str, Any]:
        """Generate the complete project.
        
        In onboarding mode, this method:
        1. Analyzes existing repository
        2. Detects conflicts
        3. Resolves conflicts (interactively or with defaults)
        4. Creates backup before modifications
        5. Generates only missing/approved artifacts
        
        Returns:
            Dictionary with generation results including:
            - success: Boolean indicating success.
            - target_dir: Path to generated project.
            - files_created: List of created files.
            - errors: List of any errors encountered.
            - scenario: Onboarding scenario (if onboarding mode).
            - skipped: List of skipped artifacts (if onboarding mode).
            - merged: List of merged artifacts (if onboarding mode).
        """
        print(f"Generating project: {self.config.project_name}")
        print(f"Target directory: {self.target_dir}")
        
        # Handle onboarding mode
        if self.onboarding_mode:
            return self._generate_onboarding()
        
        try:
            # Create directory structure
            self._create_directories()
            
            # Load blueprint if specified
            blueprint = self._load_blueprint()
            
            # Generate .agentrules
            self._generate_cursorrules(blueprint)            
            # Generate agents
            self._generate_agents(blueprint)
            
            # Generate skills
            self._generate_skills(blueprint)
            
            # Generate knowledge files
            self._generate_knowledge(blueprint)
            
            # Generate templates
            self._generate_templates(blueprint)
            
            # Generate workflows
            self._generate_workflows(blueprint)
            
            # Generate README
            self._generate_readme()
            
            # Generate diagrams folder with README
            self._generate_diagrams()
            
            '.agent/agents',
            '.agent/skills',            'knowledge',
            'templates',
            'workflows',
            'scripts',
            'diagrams',
            'docs',
            'src',
            'proofs'        ]
        
        for dir_path in directories:
            full_path = self.target_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            
        print(f"Created directory structure in {self.target_dir}")
    
    def _load_blueprint(self) -> Optional[Dict[str, Any]]:
        """Load blueprint configuration if specified.
        
        Returns:
            Blueprint configuration dictionary or None.
        """
        if not self.config.blueprint_id:
            return None
            
        blueprint_path = self.factory_root / 'blueprints' / self.config.blueprint_id / 'blueprint.json'
        
        if not blueprint_path.exists():
            print(f"Warning: Blueprint {self.config.blueprint_id} not found")
            return None
            
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_pattern(self, pattern_type: str, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Load a pattern file.
        
        Args:
            pattern_type: Type of pattern (agents, skills, etc.).
            pattern_id: Pattern identifier.
            
        Returns:
            Pattern dictionary or None.
        """
        pattern_path = self.factory_root / 'patterns' / pattern_type / f'{pattern_id}.json'
        
        if not pattern_path.exists():
            return None
            
        with open(pattern_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _generate_cursorrules(self, blueprint: Optional[Dict[str, Any]]) -> None:
        """Generate the .agentrules file.        
        Args:
            blueprint: Optional blueprint configuration.
        """
        template = self._load_cursorrules_template()        
        # Build template context
        context = self._build_template_context(blueprint)
        
        # Add computed sections to context
        context['mcp_servers_section'] = self._generate_mcp_section() if self.config.mcp_servers else ''
        context['agents_list'] = self._generate_agents_list_section()
        context['skills_list'] = self._generate_skills_list_section()
        
        # Render using template engine if available, otherwise fall back to replace
        if self.template_engine:
            content = self.template_engine.render_string(template, context)
        else:
            # Legacy fallback using string replacement
            content = template.replace('{PROJECT_NAME}', self.config.project_name)
            content = content.replace('{PROJECT_DESCRIPTION}', self.config.project_description)
            content = content.replace('{PRIMARY_LANGUAGE}', self.config.primary_language)
            content = content.replace('{STYLE_GUIDE}', self.config.style_guide)
            content = content.replace('{DOMAIN}', self.config.domain)
            content = content.replace('{GENERATED_DATE}', datetime.now().strftime('%Y-%m-%d'))
            content = content.replace('{MCP_SERVERS}', context['mcp_servers_section'])
            content = content.replace('{AGENTS_LIST}', context['agents_list'])
            content = content.replace('{SKILLS_LIST}', context['skills_list'])
        
        output_path = self.target_dir / '.agentrules'        self._write_file(output_path, content)
    
    def _build_template_context(self, blueprint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build a context dictionary for template rendering.
        
        Args:
            blueprint: Optional blueprint configuration.
            
        Returns:
            Dictionary with all template variables.
        """
        context = {
            # Project info
            'project_name': self.config.project_name,
            'project_description': self.config.project_description,
            'primary_language': self.config.primary_language,
            'style_guide': self.config.style_guide,
            'domain': self.config.domain,
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'generated_datetime': datetime.now().isoformat(),
            
            # Lists
            'frameworks': self.config.frameworks,
            'triggers': self.config.triggers,
            'agents': self.config.agents,
            'skills': self.config.skills,
            'mcp_servers': self.config.mcp_servers,
            
            # Blueprint info
            'blueprint_id': self.config.blueprint_id,
            'blueprint': blueprint,
            
            # Team context
            'team_context': self.config.team_context,
        }
        
        # Add blueprint metadata if available
        if blueprint:
            metadata = blueprint.get('metadata', {})
            context['blueprint_name'] = metadata.get('blueprintName', '')
            context['blueprint_version'] = metadata.get('version', '')
            context['blueprint_description'] = metadata.get('description', '')
        
        return context
    
    def _load_cursorrules_template(self) -> str:
        """Load the cursorrules template.        
        Returns:
            Template content string.
        """
        template_path = self.factory_root / 'templates' / 'factory' / 'cursorrules-template.md'        
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Default template
        return '''# {PROJECT_NAME} - LLM Agent Instructions

## Project Context

{PROJECT_DESCRIPTION}

**Domain:** {DOMAIN}
**Primary Language:** {PRIMARY_LANGUAGE}
**Style Guide:** {STYLE_GUIDE}

## Configuration Variables

```
PYTHON_PATH = C:\\App\\Anaconda\\python.exe
```

## Available Agents

{AGENTS_LIST}

## Available Skills

{SKILLS_LIST}

## MCP Server Integration

{MCP_SERVERS}

## Autonomous Behavior Rules

### Rule 1: Ticket Handling
When user mentions a ticket ID:
- Fetch ticket details using MCP tools
- Summarize and extract relevant information
- Proceed with appropriate workflow

### Rule 2: Code Review
After implementation:
- Invoke code reviewer agent
- Apply style guide rules
- Generate review report

### Rule 3: Data Verification
Before implementation:
- Verify data structures and assumptions
- Use grounding skill if available
- Ask user for confirmation if uncertain

## Response Behavior

- Be proactive with tool usage
- Provide specific references and line numbers
- Create actionable checklists
- Document all assumptions

---

*Generated by Antigravity Agent Factory on {GENERATED_DATE}*'''
    
    def _generate_mcp_section(self) -> str:
        """Generate MCP servers configuration section.
        
        Returns:
            Formatted MCP section string.
        """
        lines = ['| Server | Purpose | URL |', '|--------|---------|-----|']
        for server in self.config.mcp_servers:
            name = server.get('name', 'unknown')
            purpose = server.get('purpose', '')
            url = server.get('url', '')
            lines.append(f"| `{name}` | {purpose} | {url} |")
        return '\n'.join(lines)
    
    def _generate_agents_list_section(self) -> str:
        """Generate agents list section.
        
        Returns:
            Formatted agents section string.
        """
        lines = ['| Agent | Purpose |', '|-------|---------|']
        for agent_id in self.config.agents:
            pattern = self._load_pattern('agents', agent_id)
            if pattern:
                name = pattern.get('frontmatter', {}).get('name', agent_id)
                desc = pattern.get('metadata', {}).get('description', '')
                lines.append(f"| `{name}` | {desc} |")
            else:
                lines.append(f"| `{agent_id}` | Custom agent |")
        return '\n'.join(lines)
    
    def _generate_skills_list_section(self) -> str:
        """Generate skills list section.
        
        Returns:
            Formatted skills section string.
        """
        lines = ['| Skill | Description |', '|-------|-------------|']
        for skill_id in self.config.skills:
            pattern = self._load_pattern('skills', skill_id)
            if pattern:
                name = pattern.get('frontmatter', {}).get('name', skill_id)
                desc = pattern.get('metadata', {}).get('description', '')
                lines.append(f"| `{name}` | {desc} |")
            else:
                lines.append(f"| `{skill_id}` | Custom skill |")
        return '\n'.join(lines)
    
    def _generate_agents(self, blueprint: Optional[Dict[str, Any]]) -> None:
        """Generate agent files.
        
        Args:
            blueprint: Optional blueprint configuration.
        """
        agents_dir = self.target_dir / '.agent' / 'agents'        
        # Collect all agents to generate
        agents_to_generate = list(self.config.agents)
        
        # Add standard patterns that should be included in all projects
        standard_agents = [
            'debug-conductor-project',
            'factory-updates',  # Enable receiving updates from Factory
        ]        for agent_id in standard_agents:
            if agent_id not in agents_to_generate:
                agents_to_generate.append(agent_id)
        
        # Add PM agents if PM integration is enabled in blueprint
        if blueprint and blueprint.get('pmIntegration', {}).get('enabled', False):
            pm_integration = blueprint.get('pmIntegration', {})
            pm_agents = pm_integration.get('agents', [])
            for pm_agent in pm_agents:
                agent_pattern_id = pm_agent.get('patternId') if isinstance(pm_agent, dict) else pm_agent
                if agent_pattern_id and agent_pattern_id not in agents_to_generate:
                    agents_to_generate.append(agent_pattern_id)
        
        # Generate all agents
        for agent_id in agents_to_generate:
            pattern = self._load_pattern('agents', agent_id)
            if pattern:
                content = self._render_agent_from_pattern(pattern)
                name = pattern.get('frontmatter', {}).get('name', agent_id)
                output_path = agents_dir / f'{name}.md'
                self._write_file(output_path, content)
            else:
                print(f"Warning: Agent pattern {agent_id} not found")
    
    def _render_agent_from_pattern(self, pattern: Dict[str, Any]) -> str:
        """Render agent markdown from pattern.
        
        Args:
            pattern: Agent pattern dictionary.
            
        Returns:
            Rendered markdown content.
        """
        frontmatter = pattern.get('frontmatter', {})
        sections = pattern.get('sections', {})
        
        lines = ['---']
        for key, value in frontmatter.items():
            if isinstance(value, list):
                lines.append(f"{key}: {json.dumps(value)}")
            else:
                lines.append(f"{key}: {value}")
        lines.append('---')
        lines.append('')
        
        # Title
        title = sections.get('title', frontmatter.get('name', 'Agent'))
        lines.append(f"# {title}")
        lines.append('')
        
        # Purpose
        if 'purpose' in sections:
            lines.append('## Purpose')
            lines.append('')
            lines.append(sections['purpose'])
            lines.append('')
        
        # When Activated
        if 'whenActivated' in sections:
            lines.append('## When Activated')
            lines.append('')
            for item in sections['whenActivated']:
                lines.append(f"- {item}")
            lines.append('')
        
        # Workflow
        if 'workflow' in sections:
            lines.append('## Workflow')
            lines.append('')
            for step in sections['workflow']:
                lines.append(f"### Step {step.get('step', '')}: {step.get('name', '')}")
                lines.append('')
                lines.append(step.get('description', ''))
                if 'actions' in step:
                    lines.append('')
                    for action in step['actions']:
                        lines.append(f"- {action}")
                lines.append('')
        
        # Skills Used
        if 'skillsUsed' in sections:
            lines.append('## Skills Used')
            lines.append('')
            lines.append('| Skill | Purpose |')
            lines.append('|-------|---------|')
            for skill in sections['skillsUsed']:
                lines.append(f"| `{skill.get('skill', '')}` | {skill.get('purpose', '')} |")
            lines.append('')
        
        # Important Rules
        if 'importantRules' in sections:
            lines.append('## Important Rules')
            lines.append('')
            for i, rule in enumerate(sections['importantRules'], 1):
                lines.append(f"{i}. {rule}")
            lines.append('')
        
        return '\n'.join(lines)
    
    def _generate_skills(self, blueprint: Optional[Dict[str, Any]]) -> None:
        """Generate skill files.
        
        Args:
            blueprint: Optional blueprint configuration.
        """
        # Collect all skills to generate
        skills_to_generate = list(self.config.skills)
        
        # Add standard patterns that should be included in all projects
        standard_skills = [
            'grounding-verification',
            'alignment-check',
            'research-first-project',
            'ci-monitor-project',
            'pipeline-error-fix-project',
                skill_dir = self.target_dir / '.agent' / 'skills' / name                skill_dir.mkdir(parents=True, exist_ok=True)
                output_path = skill_dir / 'SKILL.md'
                self._write_file(output_path, content)
            else:
                print(f"Warning: Skill pattern {skill_id} not found")
    
    def _render_skill_from_pattern(self, pattern: Dict[str, Any]) -> str:
        """Render skill markdown from pattern.
        
        Args:
            pattern: Skill pattern dictionary.
            
        Returns:
            Rendered markdown content.
        """
        frontmatter = pattern.get('frontmatter', {})
        sections = pattern.get('sections', {})
        
        lines = ['---']
        for key, value in frontmatter.items():
            if isinstance(value, list):
                lines.append(f"{key}: {json.dumps(value)}")
            else:
                lines.append(f"{key}: {value}")
        lines.append('---')
        lines.append('')
        
        # Title
        title = sections.get('title', frontmatter.get('name', 'Skill'))
        lines.append(f"# {title}")
        lines.append('')
        
        # Introduction
        if 'introduction' in sections:
            lines.append(sections['introduction'])
            lines.append('')
        
        # When to Use
        if 'whenToUse' in sections:
            lines.append('## When to Use')
            lines.append('')
            for item in sections['whenToUse']:
                lines.append(f"- {item}")
            lines.append('')
        
        # Process
        if 'process' in sections:
            lines.append('## Process')
            lines.append('')
            for step in sections['process']:
                lines.append(f"### Step {step.get('step', '')}: {step.get('name', '')}")
                lines.append('')
                lines.append(step.get('description', ''))
                if 'actions' in step:
                    lines.append('')
                    for action in step['actions']:
                        lines.append(f"- {action}")
                if 'mcpTools' in step:
                    lines.append('')
                    lines.append('**MCP Tools:** ' + ', '.join(f"`{t}`" for t in step['mcpTools']))
                lines.append('')
        
        # Fallback Procedures
        if 'fallbackProcedures' in sections:
            lines.append('## Fallback Procedures')
            lines.append('')
            for proc in sections['fallbackProcedures']:
                lines.append(f"- **{proc.get('condition', '')}**: {proc.get('action', '')}")
            lines.append('')
        
        # Important Rules
        if 'importantRules' in sections:
            lines.append('## Important Rules')
            lines.append('')
            for i, rule in enumerate(sections['importantRules'], 1):
                lines.append(f"{i}. {rule}")
            lines.append('')
        
        return '\n'.join(lines)
    
    def _generate_knowledge(self, blueprint: Optional[Dict[str, Any]]) -> None:
        """Generate knowledge files.
        
        Args:
            blueprint: Optional blueprint configuration.
        """
        knowledge_dir = self.target_dir / 'knowledge'
        
        # Generate guardian-protocol.json from template
        self._generate_guardian_protocol(knowledge_dir)
        
        # Copy selected knowledge files from factory (not all)
        source_knowledge = self.factory_root / 'knowledge'
        
        # Files to copy to generated projects
        # Core values and wisdom files that carry the essence forward
        files_to_copy = [
            'best-practices.json',
            'workflow-patterns.json',
            'workflow-entities.json',
            'design-patterns.json',
            'architecture-patterns.json',
            'security-patterns.json',
            'research-first-development.json',
            'debug-patterns.json',
            'cicd-patterns.json',
        ]
        
        # Add stack-specific knowledge based on primary language
        stack_files = {
            'python': ['fastapi-patterns.json', 'langchain-patterns.json'],
            'typescript': ['nextjs-patterns.json'],
            'java': ['spring-patterns.json'],
            'csharp': ['dotnet-patterns.json'],
        }
        
        lang = self.config.primary_language.lower()
        if lang in stack_files:
            files_to_copy.extend(stack_files[lang])
        
        # Add PM knowledge if PM integration is enabled
        if blueprint and blueprint.get('pmIntegration', {}).get('enabled', False):
            files_to_copy.append('pm-metrics.json')
        
        if source_knowledge.exists():
            for filename in files_to_copy:
                src_file = source_knowledge / filename
                if src_file.exists():
                    dest = knowledge_dir / filename
                    shutil.copy2(src_file, dest)
                    self.generated_files.append(str(dest))
    def _generate_project_info(
        self, 
        knowledge_dir: Path, 
        blueprint: Optional[Dict[str, Any]]
    ) -> None:
        """Generate the project-info.json file for Factory update system.
        
        This file enables generated projects to receive updates from the Factory.
        It tracks the Factory origin, blueprint used, and installed updates.
        
        Args:
            knowledge_dir: Path to knowledge directory.
            blueprint: Optional blueprint configuration.
        """
        template_path = self.factory_root / 'templates' / 'knowledge' / 'project-info.json.tmpl'
        
        if not template_path.exists():
            print("Warning: project-info.json.tmpl not found")
            return
        
        # Get blueprint ID
        blueprint_id = "custom"
        if self.config.blueprint_id:
            blueprint_id = self.config.blueprint_id
        elif blueprint:
            blueprint_id = blueprint.get('metadata', {}).get('blueprintId', 'custom')
        
        # Get Factory version from manifest
        factory_version = self._get_factory_version()
        
        # Read template and substitute placeholders
        template_content = template_path.read_text(encoding='utf-8')
        
        now = datetime.now()
        
        # Replace placeholders (template uses {PLACEHOLDER} format)
        replacements = {
            '{PROJECT_NAME}': self.config.project_name,
            '{PROJECT_DESCRIPTION}': self.config.project_description or '',
            '{CREATED_DATE}': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
            '{GENERATED_DATE}': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
            '{FACTORY_VERSION}': factory_version,
            '{BLUEPRINT_ID}': blueprint_id,
        }
        
        content = template_content
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        output_path = knowledge_dir / 'project-info.json'
        self._write_file(output_path, content)
    
    def _get_factory_version(self) -> str:
        """Get the Factory version from manifest.json.
        
        Returns:
            Factory version string, or '0.0.0' if not found.
        """
        manifest_path = self.factory_root / 'knowledge' / 'manifest.json'
        
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
                return manifest.get('factory_version', '0.0.0')
            except (json.JSONDecodeError, IOError):
                pass
        
        return '0.0.0'
        def _render_template_file(
        self,
        template_path: Path,
        context: Dict[str, Any]
    ) -> str:
        """Render a template file with the given context.
        
        Uses Jinja2 template engine if available, falls back to string replacement.
        
        Args:
            template_path: Path to the template file.
            context: Dictionary of variables for rendering.
            
        Returns:
            Rendered content string.
        """
        template_content = template_path.read_text(encoding='utf-8')
        
        if self.template_engine:
            return self.template_engine.render_string(template_content, context)
        else:
            # Legacy fallback: simple string replacement
            content = template_content
            for key, value in context.items():
                if isinstance(value, str):
                    # Support both {KEY} and {{KEY}} patterns
                    content = content.replace(f'{{{key.upper()}}}', value)
                    content = content.replace(f'{{{{{key.upper()}}}}}', value)
            return content
    
    def _generate_templates(self, blueprint: Optional[Dict[str, Any]]) -> None:
        """Generate template files.
        
        Args:
            blueprint: Optional blueprint configuration.
        """
        templates_dir = self.target_dir / 'templates'
        
        # Create document templates
        docs_templates = [
            ('implementation_plan.md', self._get_implementation_plan_template()),
            ('technical_spec.md', self._get_technical_spec_template()),
            ('test_plan.md', self._get_test_plan_template())
        ]
        
        for filename, content in docs_templates:
            output_path = templates_dir / filename
            self._write_file(output_path, content)
    
    def _get_implementation_plan_template(self) -> str:
        """Get implementation plan template content.
        
        Returns:
            Template content string.
        """
        return '''# Implementation Plan: {TICKET_ID}

## References

| Type | Link |
|------|------|
| Ticket | [{TICKET_ID}]({TICKET_URL}) |
| Specification | [{SPEC_NAME}]({SPEC_URL}) |

## Problem Summary

{PROBLEM_DESCRIPTION}

## Solution Approach

{SOLUTION_DESCRIPTION}

## Data Model Verification

| Structure | Field | Verified? | Source |
|-----------|-------|-----------|--------|
| {STRUCTURE} | {FIELD} | Yes/No | {SOURCE} |

## Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| {FILE_PATH} | Modify/Create | {DESCRIPTION} |

## Implementation Steps

### Phase 1: Preparation
- [ ] Review requirements
- [ ] Verify data model
- [ ] Create backup

### Phase 2: Implementation
- [ ] {STEP_1}
- [ ] {STEP_2}
- [ ] {STEP_3}

### Phase 3: Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Regression tests

## Code Changes

### {FILE_NAME}

**Before:**
```{LANGUAGE}
{ORIGINAL_CODE}
```

**After:**
```{LANGUAGE}
{MODIFIED_CODE}
```

---
*Generated by Antigravity Agent System*'''
    
    def _get_technical_spec_template(self) -> str:
        """Get technical specification template content.
        
        Returns:
            Template content string.
        """
        return '''# Technical Specification: {FEATURE_NAME}

## Overview

{FEATURE_DESCRIPTION}

## Requirements Reference

- Specification: [{SPEC_NAME}]({SPEC_URL})

## Architecture

### Component Diagram

```
{COMPONENT_DIAGRAM}
```

### Data Model

| Entity | Fields | Description |
|--------|--------|-------------|
| {ENTITY} | {FIELDS} | {DESCRIPTION} |

## Interface Design

### API Endpoints / Methods

| Endpoint/Method | Parameters | Returns | Description |
|-----------------|------------|---------|-------------|
| {NAME} | {PARAMS} | {RETURNS} | {DESCRIPTION} |

## Implementation Details

### {COMPONENT_NAME}

{IMPLEMENTATION_DETAILS}

## Error Handling

| Error Condition | Handling |
|-----------------|----------|
| {CONDITION} | {HANDLING} |

## Testing Strategy

{TESTING_APPROACH}

---
*Generated by Antigravity Agent System*'''
    
    def _get_test_plan_template(self) -> str:
        """Get test plan template content.
        
        Returns:
            Template content string.
        """
        return '''# Test Plan: {FEATURE_NAME}

## Overview

{TEST_SCOPE}

## Test Cases

### Unit Tests

| ID | Description | Input | Expected Output | Status |
|----|-------------|-------|-----------------|--------|
| UT-001 | {DESCRIPTION} | {INPUT} | {OUTPUT} | ⬜ |

### Integration Tests

| ID | Scenario | Steps | Expected Result | Status |
|----|----------|-------|-----------------|--------|
| IT-001 | {SCENARIO} | {STEPS} | {RESULT} | ⬜ |

### Regression Tests

- [ ] {EXISTING_FUNCTION_1} still works
- [ ] {EXISTING_FUNCTION_2} still works

## Test Data

{TEST_DATA_REQUIREMENTS}

## Environment

{TEST_ENVIRONMENT}

---
*Generated by Antigravity Agent System*'''
    
    def _generate_workflows(self, blueprint: Optional[Dict[str, Any]]) -> None:
        """Generate workflow documentation.
        
        Args:
            blueprint: Optional blueprint configuration.
        """
        workflows_dir = self.target_dir / 'workflows'
        
        # Create README
        readme_content = self._get_workflows_readme()
        self._write_file(workflows_dir / 'README.md', readme_content)
        
        # Copy workflow templates from Factory based on blueprint or triggers
        self._copy_workflow_templates(blueprint, workflows_dir)
        
        # Create basic workflow files based on triggers (fallback)
        if 'jira' in self.config.triggers:
            bugfix_path = workflows_dir / 'bugfix_workflow.md'
            if not bugfix_path.exists():
                self._write_file(bugfix_path, self._get_bugfix_workflow_template())
        
        if 'confluence' in self.config.triggers:
            feature_path = workflows_dir / 'feature_workflow.md'
            if not feature_path.exists():
                self._write_file(feature_path, self._get_feature_workflow_template())
    
    def _copy_workflow_templates(
        self, 
        blueprint: Optional[Dict[str, Any]], 
        workflows_dir: Path
    ) -> None:
        """Copy and customize workflow templates from Factory.
        
        Args:
            blueprint: Optional blueprint configuration.
            workflows_dir: Target workflows directory.
        """
        # Agent workflow templates from Factory
        agent_templates = self.factory_root / 'templates' / 'workflows' / 'agent'
        
        if not agent_templates.exists():
            return
        
        # Determine which workflows to include
        workflows_to_copy = []
        
        # Default workflows for all projects
        default_workflows = ['code-review-workflow.md.tmpl']
        workflows_to_copy.extend(default_workflows)
        
        # Add TDD workflow if project has test focus
        if any(skill in self.config.skills for skill in ['tdd', 'test-generator']):
            workflows_to_copy.append('tdd-workflow.md.tmpl')
        
        # Add BDD workflow if using BDD
        if 'bdd' in self.config.skills:
            workflows_to_copy.append('bdd-workflow.md.tmpl')
        
        # Add documentation workflow
        if 'documentation' in self.config.triggers or 'confluence' in self.config.triggers:
            workflows_to_copy.append('documentation-workflow.md.tmpl')
        
        # Add feature workflow for feature-oriented projects
        workflows_to_copy.append('feature-development-workflow.md.tmpl')
        
        # Add refactoring workflow
        workflows_to_copy.append('refactoring-workflow.md.tmpl')
        
        # Copy and render templates
        context = self._build_template_context(blueprint)
        
        for template_name in workflows_to_copy:
            template_path = agent_templates / template_name
            if template_path.exists():
                # Render template
                if self.template_engine:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                    content = self.template_engine.render_string(template_content, context)
                else:
                    # Simple placeholder replacement
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = content.replace('{{PROJECT_NAME}}', self.config.project_name)
                    content = content.replace('{{STACK}}', self.config.primary_language)
                    content = content.replace('{{METHODOLOGY}}', 'agile')
                
                # Write with .md extension (remove .tmpl)
                output_name = template_name.replace('.tmpl', '')
                output_path = workflows_dir / output_name
                self._write_file(output_path, content)
    
    def _get_workflows_readme(self) -> str:
        """Get workflows README content.
        
        Returns:
            README content string.
        """
        return f'''# Workflows

## Overview

This directory contains workflow documentation for {self.config.project_name}.

Workflows orchestrate complex multi-step tasks by combining phases, skills, MCP tools, 
and decision points into coherent processes.

## Workflow System Architecture

```
Workflow
├── Phases (ordered groups of steps)
│   ├── Steps (atomic operations)
│   │   ├── Skills (reusable capabilities)
│   │   ├── MCP Servers (external tools)
│   │   └── Knowledge (reference data)
│   └── Decision Points (branching logic)
├── Escalation Paths (when things go wrong)
├── Learning Hooks (continuous improvement)
└── Output Artifacts (what gets created)
```

## Available Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| Bugfix | Ticket mention | Fix bugs from issue tracker |
| Feature | Specification | Implement new features |
| Code Review | PR/MR request | Review code quality |
| TDD | Test request | Test-driven development |
| Refactoring | Cleanup request | Improve code structure |

## Workflow Lifecycle States

| State | Description |
|-------|-------------|
| `draft` | Being designed, not executable |
| `active` | Ready for execution |
| `executing` | Currently running |
| `paused` | Awaiting input or resources |
| `completed` | Successfully finished |
| `failed` | Terminated with errors |
| `learning` | Post-execution analysis |

## Quick Start

1. Mention a ticket ID to start bugfix workflow
2. Reference a specification page for feature workflow
3. Request code review for PR review workflow
4. Ask for TDD approach for test-driven development

## Extending Workflows

Use the `workflow-architect` agent to:
- Create new workflows from patterns
- Extend existing workflows
- Add learning hooks for improvement

## Related Documentation

- `knowledge/workflow-patterns.json` - Common workflow patterns
- `knowledge/workflow-entities.json` - Entity definitions
- `.agent/skills/extend-workflow/SKILL.md` - Workflow extension skill

---
*Generated by Antigravity Agent Factory v3.5.0*'''
    
    def _get_bugfix_workflow_template(self) -> str:
        """Get bugfix workflow template.
        
        Returns:
            Workflow template string.
        """
        return '''# Bugfix Workflow

## Trigger

Ticket ID mentioned (e.g., {PROJECT}-123)

## Steps

1. **Read Ticket** - Fetch ticket details
2. **Fetch Source** - Get relevant source code
3. **Analyze** - Find root cause
4. **Plan** - Create implementation plan
5. **Implement** - Make code changes
6. **Update** - Update ticket status

## Artifacts

- `docs/{TICKET_ID}_plan.md` - Implementation plan
- Code changes

---
*Generated by Antigravity Agent Factory*'''
    
    def _get_feature_workflow_template(self) -> str:
        """Get feature workflow template.
        
        Returns:
            Workflow template string.
        """
        return '''# Feature Workflow

## Trigger

Specification page referenced

## Steps

1. **Read Requirements** - Analyze specification
2. **Design** - Create technical design
3. **Plan** - Create implementation plan
4. **Implement** - Write code
5. **Test** - Run tests
6. **Document** - Update documentation

## Artifacts

- Technical specification
- Implementation plan
- Test plan
- Code

---
*Generated by Antigravity Agent Factory*'''
    
    def _generate_readme(self) -> None:
        """Generate project README."""
        content = f'''# {self.config.project_name}

{self.config.project_description}

## Overview

This is a Antigravity agent development system generated by the Antigravity Agent Factory.
**Domain:** {self.config.domain}  
**Primary Language:** {self.config.primary_language}  
**Style Guide:** {self.config.style_guide}

## Project Structure

```
{self.config.project_name}/
├── .agent/│   ├── agents/           # AI agent definitions
│   └── skills/           # Reusable skill definitions
├── knowledge/            # Structured reference data
├── templates/            # Code and document templates
├── workflows/            # Workflow documentation
├── scripts/              # Utility scripts
├── diagrams/             # Architecture diagrams
├── docs/                 # Documentation
├── src/                  # Source code
├── .agentrules          # LLM agent behavior rules└── README.md             # This file
```

## Quick Start

1. Open this project in Antigravity IDE
2. The `.agentrules` file will configure agent behavior3. Start by mentioning a ticket or requesting a workflow

## Available Agents

{self._generate_agents_list_section()}

## Available Skills

{self._generate_skills_list_section()}

## Workflows

See `workflows/README.md` for available workflows.

---

*Generated by Antigravity Agent Factory on {datetime.now().strftime('%Y-%m-%d')}*'''
        
        self._write_file(self.target_dir / 'README.md', content)
    
    def _generate_diagrams(self) -> None:
        """Generate diagrams folder with README."""
        diagrams_dir = self.target_dir / 'diagrams'
        
        readme_content = '''# Diagrams

This directory contains architecture and workflow diagrams.

## Creating Diagrams

Use Mermaid syntax in `.mmd` files:

```mermaid
flowchart LR
    A[Start] --> B[Process] --> C[End]
```

## Rendering

To render diagrams to PNG, use a Mermaid CLI tool or the diagram rendering script.
'''
        
        self._write_file(diagrams_dir / 'README.md', readme_content)
    
        This method integrates Antigravity Agent Factory into an existing        repository without destroying existing artifacts.
        
        Returns:
            Dictionary with generation results.
        """
        if not ONBOARDING_AVAILABLE:
            return {
                'success': False,
                'target_dir': str(self.target_dir),
                'files_created': [],
                'errors': ['Onboarding modules not available. Ensure repo_analyzer.py, '
                          'merge_strategy.py, and backup_manager.py exist.'],
            }
        
        print("\n=== ONBOARDING MODE ===")
        print(f"Analyzing existing repository: {self.target_dir}\n")
        
        try:
            # Step 1: Analyze repository
            analyzer = RepoAnalyzer(self.target_dir, self.factory_root)
            self.inventory = analyzer.analyze()
            
            print(f"Scenario detected: {self.inventory.scenario.value.upper()}")
            print(f"Existing agents: {len(self.inventory.existing_agents)}")
            print(f"Existing skills: {len(self.inventory.existing_skills)}")
            print(f"Tech stack: {', '.join(self.inventory.tech_stack.languages)}")
            
            if self.inventory.tech_stack.suggested_blueprint:
                print(f"Suggested blueprint: {self.inventory.tech_stack.suggested_blueprint}")
            
            # Step 2: Handle different scenarios
            if self.inventory.scenario == OnboardingScenario.COMPLETE:
                print("\nRepository is already fully configured.")
                return {
                    'success': True,
                    'target_dir': str(self.target_dir),
                    'files_created': [],
                    'errors': [],
                    'scenario': self.inventory.scenario.value,
                    'skipped': [],
                    'merged': [],
                    'message': 'Repository already fully configured. No changes needed.',
                }
            
            # Step 3: Detect conflicts
            self.merge_engine = MergeEngine(self.inventory, self.factory_root)
            conflicts = self.merge_engine.detect_conflicts(
                desired_agents=self.config.agents,
                desired_skills=self.config.skills,
                desired_knowledge=[f"{k}.json" for k in ['best-practices', 'design-patterns']],
            )
            
            # Step 4: Resolve conflicts
            if conflicts:
                print(f"\nFound {len(conflicts)} conflict(s) to resolve:")
                for conflict in conflicts:
                    self._resolve_conflict(conflict)
            
            # Step 5: Create backup (unless dry run)
            if not self.dry_run:
                backup_manager = BackupManager(self.target_dir)
                self.backup_session = backup_manager.create_session(
                    f"Onboarding with blueprint: {self.config.blueprint_id or 'custom'}"
                )
                print(f"\nBackup session created: {self.backup_session.session_id}")
            
            # Step 6: Generate artifacts
            self._onboard_directories()
            self._onboard_cursorrules()            self._onboard_agents()
            self._onboard_skills()
            self._onboard_knowledge()
            self._onboard_templates()
            self._onboard_workflows()
            
            # Only generate README if it doesn't exist
            if not self.inventory.has_readme:
                self._generate_readme()
            
            # Step 7: Complete backup session
            if self.backup_session and not self.dry_run:
                self.backup_session.complete()
                print(f"\nBackup session completed. Rollback available with session ID: "
                      f"{self.backup_session.session_id}")
            
            return {
                'success': len(self.errors) == 0,
                'target_dir': str(self.target_dir),
                'files_created': self.generated_files,
                'errors': self.errors,
                'scenario': self.inventory.scenario.value,
                'skipped': self.skipped_artifacts,
                'merged': self.merged_artifacts,
            }
            
        except Exception as e:
            self.errors.append(f"Onboarding failed: {str(e)}")
            
            # Rollback on failure
            if self.backup_session and not self.dry_run:
                print("\nRolling back changes due to error...")
                self.backup_session.rollback()
            
            return {
                'success': False,
                'target_dir': str(self.target_dir),
                'files_created': self.generated_files,
                'errors': self.errors,
                'scenario': getattr(self.inventory, 'scenario', 'unknown'),
                'skipped': self.skipped_artifacts,
                'merged': self.merged_artifacts,
            }
    
    def _resolve_conflict(self, conflict: Conflict) -> None:
        """Resolve a single conflict.
        
        Args:
            conflict: The conflict to resolve.
        """
        prompt = self.merge_engine.get_conflict_prompt(conflict)
        
        if self.conflict_resolver:
            # Use provided resolver callback
            resolution = self.conflict_resolver(prompt)
        else:
            # Use default recommendation
            print(f"\n  {conflict.artifact_type.value}: {conflict.artifact_name}")
            print(f"    → Using default: {prompt.recommendation.value} ({prompt.reason})")
            resolution = prompt.recommendation
        
        self.merge_engine.set_resolution(conflict, resolution)
        
        if resolution in (ConflictResolution.KEEP_EXISTING, ConflictResolution.SKIP):
            self.skipped_artifacts.append(
                f"{conflict.artifact_type.value}:{conflict.artifact_name}"
            )
        elif resolution == ConflictResolution.MERGE:
            self.merged_artifacts.append(
                f"{conflict.artifact_type.value}:{conflict.artifact_name}"
            )
    
    def _onboard_directories(self) -> None:
        """Create directory structure for onboarding (only missing dirs)."""
        directories = [
            '.agent/agents',
            '.agent/skills',            'knowledge',
            'templates',
            'workflows',
            'diagrams',
            'docs',
        ]
        
        for dir_path in directories:
            full_path = self.target_dir / dir_path
            if not full_path.exists():
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {full_path}")
    
    def _onboard_cursorrules(self) -> None:
        """Handle .agentrules in onboarding mode."""
        if self.merge_engine.should_skip_artifact(ArtifactType.CURSORRULES, ".agentrules"):
            print("Skipping .agentrules (user choice)")
            return
        
        cursorrules_path = self.target_dir / ".agentrules"
        
        if self.inventory.agentrules.exists:
            # Backup existing
            if self.backup_session:
                self.backup_session.backup_file(cursorrules_path)
            
            # Check if merge was requested
            resolution = self.merge_engine.get_resolution(
                Conflict(ArtifactType.CURSORRULES, ".agentrules", cursorrules_path, "")            )
            
            if resolution == ConflictResolution.MERGE:
                # Merge existing with new sections
                new_content = self._merge_cursorrules()
                self._write_file(cursorrules_path, new_content)
                print("Merged .agentrules with factory sections")
                return
            elif resolution == ConflictResolution.KEEP_EXISTING:
                print("Keeping existing .agentrules")                return
        
        # Generate new (for FRESH scenario or REPLACE resolution)
        blueprint = self._load_blueprint()
        self._generate_cursorrules(blueprint)
    
    def _merge_cursorrules(self) -> str:
        """Merge existing .agentrules with factory sections.        
        Returns:
            Merged content.
        """
        existing = self.inventory.agentrules.content or ""        
        # Factory marker
        factory_marker = f"""

# ═══════════════════════════════════════════════════════════════════════════════
# CURSOR AGENT FACTORY INTEGRATION
# Generated: {datetime.now().strftime('%Y-%m-%d')}
# Blueprint: {self.config.blueprint_id or 'custom'}
# Factory Version: 4.1.0# ═══════════════════════════════════════════════════════════════════════════════

"""
        
        # Check if factory marker already exists
        if "CURSOR AGENT FACTORY INTEGRATION" in existing:
            # Update existing factory section
            import re
            pattern = r'# ═+\s*\n# CURSOR AGENT FACTORY INTEGRATION.*?# ═+\s*END FACTORY INTEGRATION\s*═+\s*\n'            if re.search(pattern, existing, re.DOTALL):
                # Remove old factory section
                existing = re.sub(pattern, '', existing, flags=re.DOTALL)
        
        # Add new agents/skills sections
        agents_section = self._generate_agents_list_section()
        skills_section = self._generate_skills_list_section()
        
        factory_content = f"""{factory_marker}
## Factory-Injected Agents

{agents_section}

## Factory-Injected Skills

{skills_section}

# ═══════════════════════════════════════════════════════════════════════════════
# END FACTORY INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════
"""
        
        return existing.rstrip() + "\n" + factory_content
    
    def _onboard_agents(self) -> None:
        """Generate agents in onboarding mode (skip existing)."""
        agents_dir = self.target_dir / '.agent' / 'agents'        
        for agent_id in self.config.agents:
            # Check if should skip
            if agent_id in self.inventory.existing_agents:
                if self.merge_engine.should_skip_artifact(ArtifactType.AGENT, agent_id):
                    print(f"Skipping agent: {agent_id} (exists)")
                    continue
                
                # Backup existing if replacing
                agent_path = agents_dir / f"{agent_id}.md"
                if self.backup_session and agent_path.exists():
                    self.backup_session.backup_file(agent_path)
                
                # Check for rename
                if self.merge_engine.should_rename_artifact(ArtifactType.AGENT, agent_id):
                    agent_id = self.merge_engine.get_renamed_name(agent_id)
            
            # Generate agent
            pattern = self._load_pattern('agents', agent_id.replace('-factory', ''))
            if pattern:
                content = self._render_agent_from_pattern(pattern)
                name = pattern.get('frontmatter', {}).get('name', agent_id)
                if '-factory' in agent_id:
                    name = f"{name}-factory"
                output_path = agents_dir / f'{name}.md'
                
                if self.backup_session and not output_path.exists():
                    self.backup_session.backup_file(output_path, mark_as_new=True)
                
                self._write_file(output_path, content)
    
    def _onboard_skills(self) -> None:
        """Generate skills in onboarding mode (skip existing)."""
        for skill_id in self.config.skills:
            # Check if should skip
            if skill_id in self.inventory.existing_skills:
                if self.merge_engine.should_skip_artifact(ArtifactType.SKILL, skill_id):
                    print(f"Skipping skill: {skill_id} (exists)")
                    continue
                
                # Backup existing if replacing
                skill_path = self.target_dir / '.agent' / 'skills' / skill_id / 'SKILL.md'                if self.backup_session and skill_path.exists():
                    self.backup_session.backup_file(skill_path)
                
                # Check for rename
                if self.merge_engine.should_rename_artifact(ArtifactType.SKILL, skill_id):
                    skill_id = self.merge_engine.get_renamed_name(skill_id)
            
            # Generate skill
            pattern = self._load_pattern('skills', skill_id.replace('-factory', ''))
            if pattern:
                content = self._render_skill_from_pattern(pattern)
                name = pattern.get('frontmatter', {}).get('name', skill_id)
                if '-factory' in skill_id:
                    name = f"{name}-factory"
                skill_dir = self.target_dir / '.agent' / 'skills' / name                
                if not self.dry_run:
                    skill_dir.mkdir(parents=True, exist_ok=True)
                
                output_path = skill_dir / 'SKILL.md'
                
                if self.backup_session and not output_path.exists():
                    self.backup_session.backup_file(output_path, mark_as_new=True)
                
                self._write_file(output_path, content)
    
    def _onboard_knowledge(self) -> None:
        """Generate knowledge files in onboarding mode."""
        _blueprint = self._load_blueprint()  # Reserved for future use
        
        # Only copy knowledge files that don't exist
        source_knowledge = self.factory_root / 'knowledge'
        target_knowledge = self.target_dir / 'knowledge'
        
        if source_knowledge.exists():
            for file in source_knowledge.glob('*.json'):
                if file.name not in self.inventory.existing_knowledge:
                    dest = target_knowledge / file.name
                    
                    if self.backup_session:
                        self.backup_session.backup_file(dest, mark_as_new=True)
                    
                    if not self.dry_run:
                        shutil.copy2(file, dest)
                    
                    self.generated_files.append(str(dest))
                    print(f"Added knowledge: {file.name}")
                else:
                    print(f"Skipping knowledge: {file.name} (exists)")
    
    def _onboard_templates(self) -> None:
        """Generate templates in onboarding mode."""
        blueprint = self._load_blueprint()
        
        # Only create templates if templates directory was empty
        if not self.inventory.existing_templates:
            self._generate_templates(blueprint)
        else:
            print("Skipping templates (directory not empty)")
    
    def _onboard_workflows(self) -> None:
        """Generate workflows in onboarding mode."""
        blueprint = self._load_blueprint()
        
        # Only create workflows that don't exist
        if not self.inventory.existing_workflows:
            self._generate_workflows(blueprint)
        else:
            print("Skipping workflows (directory not empty)")


def generate_from_config(config_path: str, target_dir: str) -> Dict[str, Any]:
    """Generate project from configuration file.
    
    Args:
        config_path: Path to configuration file (YAML or JSON).
        target_dir: Target directory for generated project.
        
    Returns:
        Generation result dictionary.
    """
    if config_path.endswith('.yaml') or config_path.endswith('.yml'):
        config = ProjectConfig.from_yaml_file(config_path)
    else:
        config = ProjectConfig.from_json_file(config_path)
    
    generator = ProjectGenerator(config, target_dir)
    return generator.generate()


if __name__ == '__main__':
    # Example usage
    config = ProjectConfig(
        project_name='example-project',
        project_description='An example Antigravity agent project',        primary_language='python',
        agents=['code-reviewer', 'test-generator'],
        skills=['bugfix-workflow', 'feature-workflow', 'tdd'],
        triggers=['jira', 'confluence']
    )
    
    generator = ProjectGenerator(config, './example-output')
    result = generator.generate()
    print(f"Generation result: {result}")
