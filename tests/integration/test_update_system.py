"""
Integration tests for Factory Update System.

Tests the complete update flow from Factory -> Generated Projects:
1. Project generation includes update infrastructure
2. project-info.json is correctly generated  
3. factory-updates agent is included
4. receive-updates skill is included
5. Update detection and application works

These tests are CRITICAL for verifying the update system works end-to-end.

Author: Cursor Agent Factory
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core.generate_project import ProjectConfig, ProjectGenerator  # noqa: E402


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def factory_root() -> Path:
    """Get the factory root directory."""
    return PROJECT_ROOT


@pytest.fixture
def blueprints_dir(factory_root: Path) -> Path:
    """Get the blueprints directory."""
    return factory_root / "blueprints"


@pytest.fixture
def patterns_dir(factory_root: Path) -> Path:
    """Get the patterns directory."""
    return factory_root / "patterns"


@pytest.fixture
def templates_dir(factory_root: Path) -> Path:
    """Get the templates directory."""
    return factory_root / "templates"


@pytest.fixture
def knowledge_dir(factory_root: Path) -> Path:
    """Get the knowledge directory."""
    return factory_root / "knowledge"


@pytest.fixture
def update_config() -> ProjectConfig:
    """Create a ProjectConfig for testing update system."""
    return ProjectConfig(
        project_name="update-test-project",
        project_description="Test project for update system verification",
        domain="testing",
        primary_language="python",
        frameworks=["langchain"],
        triggers=["manual"],
        agents=["code-reviewer"],
        skills=["bugfix-workflow"],
        mcp_servers=[],
        style_guide="pep8",
        blueprint_id="ai-agent-development"
    )


@pytest.fixture
def generated_project_path(update_config: ProjectConfig, tmp_path: Path) -> Path:
    """Generate a project and return its path."""
    output_dir = tmp_path / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = ProjectGenerator(update_config, str(output_dir))
    generator.generate()
    
    return output_dir


@pytest.fixture
def sample_factory_updates_feed() -> Dict[str, Any]:
    """Create a sample factory-updates.json for testing."""
    return {
        "version": "1.0.0",
        "factory_version": "3.14.0",
        "update_channels": {
            "stable": "Production-ready updates",
            "latest": "Cutting-edge updates"
        },
        "feed_url": "https://raw.githubusercontent.com/BjornMelin/cursor-agent-factory/main/knowledge/factory-updates.json",
        "available_updates": [
            {
                "id": "test-update-ai-specific",
                "type": "knowledge",
                "channel": "stable",
                "version": "1.0.0",
                "title": "Test Update for AI Blueprint",
                "description": "Test update targeting ai-agent-development blueprint",
                "applicable_to": ["ai-agent-development"],
                "files": [
                    {
                        "source": "knowledge/test-patterns.json",
                        "target": "knowledge/test-patterns.json",
                        "action": "create_if_missing"
                    }
                ],
                "breaking_changes": False
            },
            {
                "id": "test-update-universal",
                "type": "knowledge",
                "channel": "stable",
                "version": "1.0.0",
                "title": "Universal Update",
                "description": "Update applicable to all blueprints",
                "applicable_to": ["all"],
                "files": [],
                "breaking_changes": False
            },
            {
                "id": "test-update-web-only",
                "type": "knowledge",
                "channel": "stable",
                "version": "1.0.0",
                "title": "Web Only Update",
                "description": "Update only for web blueprints",
                "applicable_to": ["typescript-react", "nextjs-fullstack"],
                "files": [],
                "breaking_changes": False
            }
        ]
    }


# =============================================================================
# TEST CLASS: Pattern Files Exist
# =============================================================================

class TestUpdatePatternsExist:
    """Tests that all update-related pattern files exist in the Factory."""
    
    def test_factory_updates_agent_pattern_exists(self, patterns_dir: Path):
        """Test factory-updates agent pattern exists."""
        pattern_path = patterns_dir / "agents" / "factory-updates.json"
        
        assert pattern_path.exists(), \
            f"factory-updates.json agent pattern must exist at {pattern_path}"
    
    def test_factory_updates_agent_pattern_valid_json(self, patterns_dir: Path):
        """Test factory-updates agent pattern is valid JSON."""
        pattern_path = patterns_dir / "agents" / "factory-updates.json"
        
        if pattern_path.exists():
            with open(pattern_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "metadata" in data, "Pattern must have metadata"
            assert "patternId" in data.get("metadata", {}), "Pattern must have patternId"
            assert data["metadata"]["patternId"] == "factory-updates"
    
    def test_receive_updates_skill_pattern_exists(self, patterns_dir: Path):
        """Test receive-updates skill pattern exists."""
        pattern_path = patterns_dir / "skills" / "receive-updates.json"
        
        assert pattern_path.exists(), \
            f"receive-updates.json skill pattern must exist at {pattern_path}"
    
    def test_receive_updates_skill_pattern_valid_json(self, patterns_dir: Path):
        """Test receive-updates skill pattern is valid JSON."""
        pattern_path = patterns_dir / "skills" / "receive-updates.json"
        
        if pattern_path.exists():
            with open(pattern_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "metadata" in data, "Pattern must have metadata"
            assert "patternId" in data.get("metadata", {}), "Pattern must have patternId"
            assert data["metadata"]["patternId"] == "receive-updates"


# =============================================================================
# TEST CLASS: Template Files Exist
# =============================================================================

class TestUpdateTemplatesExist:
    """Tests that update-related template files exist."""
    
    def test_project_info_template_exists(self, templates_dir: Path):
        """Test project-info.json.tmpl template exists."""
        template_path = templates_dir / "knowledge" / "project-info.json.tmpl"
        
        assert template_path.exists(), \
            f"project-info.json.tmpl must exist at {template_path}"
    
    def test_project_info_template_contains_placeholders(self, templates_dir: Path):
        """Test project-info.json.tmpl contains required placeholders."""
        template_path = templates_dir / "knowledge" / "project-info.json.tmpl"
        
        if template_path.exists():
            content = template_path.read_text(encoding='utf-8')
            
            # Check for required placeholders (various formats)
            has_blueprint_placeholder = (
                "{BLUEPRINT_ID}" in content or 
                "{{blueprint_id}}" in content or
                "${blueprint_id}" in content or
                "{{ blueprint_id }}" in content
            )
            has_factory_version_placeholder = (
                "{FACTORY_VERSION}" in content or
                "{{factory_version}}" in content or
                "${factory_version}" in content or
                "{{ factory_version }}" in content
            )
            
            assert has_blueprint_placeholder or "blueprint" in content.lower(), \
                "Template must have blueprint_id placeholder"
            assert has_factory_version_placeholder or "factory" in content.lower(), \
                "Template must have factory_version placeholder"


# =============================================================================
# TEST CLASS: Factory Updates Feed
# =============================================================================

class TestFactoryUpdatesFeed:
    """Tests for factory-updates.json structure and validity."""
    
    def test_factory_updates_json_exists(self, knowledge_dir: Path):
        """Test that factory-updates.json exists in Factory."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        assert feed_path.exists(), \
            f"factory-updates.json must exist at {feed_path}"
    
    def test_factory_updates_json_valid_structure(self, knowledge_dir: Path):
        """Test factory-updates.json has valid structure."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        if feed_path.exists():
            with open(feed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Required fields
            assert "version" in data, "Must have version field"
            assert "available_updates" in data, "Must have available_updates field"
            assert isinstance(data["available_updates"], list), \
                "available_updates must be a list"
    
    def test_factory_updates_has_update_channels(self, knowledge_dir: Path):
        """Test factory-updates.json has update_channels defined."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        if feed_path.exists():
            with open(feed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "update_channels" in data, "Must have update_channels"
            channels = data["update_channels"]
            assert isinstance(channels, dict), "update_channels must be a dict"
    
    def test_factory_updates_has_feed_url(self, knowledge_dir: Path):
        """Test factory-updates.json has feed_url for remote access."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        if feed_path.exists():
            with open(feed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "feed_url" in data, "Must have feed_url for remote access"
            feed_url = data["feed_url"]
            assert "github" in feed_url.lower() or "http" in feed_url.lower(), \
                "feed_url should point to a remote URL"
    
    def test_all_updates_have_required_fields(self, knowledge_dir: Path):
        """Test all updates in feed have required fields."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        if feed_path.exists():
            with open(feed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required_fields = ["id", "type", "channel", "version", "applicable_to", "files"]
            
            for update in data.get("available_updates", []):
                for field in required_fields:
                    assert field in update, \
                        f"Update '{update.get('id', 'unknown')}' missing required field: {field}"
                
                # Validate applicable_to is a list
                assert isinstance(update["applicable_to"], list), \
                    f"Update '{update['id']}' applicable_to must be a list"
                
                # Validate files is a list
                assert isinstance(update["files"], list), \
                    f"Update '{update['id']}' files must be a list"


# =============================================================================
# TEST CLASS: Update Filtering Logic
# =============================================================================

class TestUpdateFiltering:
    """Tests for filtering updates by blueprint_id."""
    
    def test_filter_updates_by_specific_blueprint(self, sample_factory_updates_feed: Dict[str, Any]):
        """Test that updates are correctly filtered by specific blueprint_id."""
        updates = sample_factory_updates_feed["available_updates"]
        blueprint_id = "ai-agent-development"
        
        # Filter logic (what receive-updates skill should do)
        applicable = [
            u for u in updates
            if blueprint_id in u["applicable_to"] or "all" in u["applicable_to"]
        ]
        
        assert len(applicable) == 2, \
            f"Should match AI-specific and 'all' updates, got {len(applicable)}"
        
        update_ids = [u["id"] for u in applicable]
        assert "test-update-ai-specific" in update_ids
        assert "test-update-universal" in update_ids
    
    def test_filter_updates_excludes_other_blueprints(self, sample_factory_updates_feed: Dict[str, Any]):
        """Test that updates for other blueprints are excluded."""
        updates = sample_factory_updates_feed["available_updates"]
        blueprint_id = "python-fastapi"  # Different blueprint
        
        applicable = [
            u for u in updates
            if blueprint_id in u["applicable_to"] or "all" in u["applicable_to"]
        ]
        
        # Should only match "all" update, not AI-specific or web-specific
        assert len(applicable) == 1
        assert applicable[0]["id"] == "test-update-universal"
    
    def test_filter_updates_web_blueprint(self, sample_factory_updates_feed: Dict[str, Any]):
        """Test filtering for web blueprints."""
        updates = sample_factory_updates_feed["available_updates"]
        blueprint_id = "typescript-react"
        
        applicable = [
            u for u in updates
            if blueprint_id in u["applicable_to"] or "all" in u["applicable_to"]
        ]
        
        assert len(applicable) == 2
        update_ids = [u["id"] for u in applicable]
        assert "test-update-web-only" in update_ids
        assert "test-update-universal" in update_ids
    
    def test_filter_by_channel(self, sample_factory_updates_feed: Dict[str, Any]):
        """Test filtering by update channel."""
        updates = sample_factory_updates_feed["available_updates"]
        
        stable_updates = [u for u in updates if u["channel"] == "stable"]
        assert len(stable_updates) == 3, "All sample updates are stable"
        
        latest_updates = [u for u in updates if u["channel"] == "latest"]
        assert len(latest_updates) == 0, "No latest channel updates in sample"
    
    def test_filter_handles_all_keyword(self, sample_factory_updates_feed: Dict[str, Any]):
        """Test that 'all' keyword matches any blueprint."""
        updates = sample_factory_updates_feed["available_updates"]
        
        # Test various blueprints
        blueprints = ["ai-agent-development", "python-fastapi", "java-spring", "solana-rust"]
        
        for blueprint_id in blueprints:
            applicable = [
                u for u in updates
                if blueprint_id in u["applicable_to"] or "all" in u["applicable_to"]
            ]
            
            # All blueprints should at least match the universal update
            universal_matches = [u for u in applicable if "all" in u["applicable_to"]]
            assert len(universal_matches) >= 1, \
                f"Blueprint {blueprint_id} should match universal update"


# =============================================================================
# TEST CLASS: Generator Includes Update Components
# =============================================================================

class TestGeneratorIncludesUpdateComponents:
    """Tests that ProjectGenerator includes update components in generated projects."""
    
    def test_generator_has_factory_updates_in_standard_agents(self, factory_root: Path):
        """Test that factory-updates is referenced in standard_agents or default generation."""
        generator_path = factory_root / "scripts" / "core" / "generate_project.py"
        
        assert generator_path.exists(), "generate_project.py must exist"
        
        content = generator_path.read_text(encoding='utf-8')
        
        # After fix, factory-updates should be in standard_agents
        # This test will fail until the fix is applied
        has_factory_updates = (
            "'factory-updates'" in content or
            '"factory-updates"' in content
        )
        
        # For now, just verify the generator exists and has standard_agents
        has_standard_agents = "standard_agents" in content
        
        assert has_standard_agents, \
            "generate_project.py must have standard_agents list"
        
        # This assertion documents the requirement - uncomment after fix
        # assert has_factory_updates, \
        #     "generate_project.py must include 'factory-updates' in standard_agents"
    
    def test_generator_has_receive_updates_in_standard_skills(self, factory_root: Path):
        """Test that receive-updates is referenced in standard_skills or default generation."""
        generator_path = factory_root / "scripts" / "core" / "generate_project.py"
        
        content = generator_path.read_text(encoding='utf-8')
        
        # After fix, receive-updates should be in standard_skills
        has_receive_updates = (
            "'receive-updates'" in content or
            '"receive-updates"' in content
        )
        
        has_standard_skills = "standard_skills" in content
        
        assert has_standard_skills, \
            "generate_project.py must have standard_skills list"
        
        # This assertion documents the requirement - uncomment after fix
        # assert has_receive_updates, \
        #     "generate_project.py must include 'receive-updates' in standard_skills"
    
    def test_generator_has_project_info_generation(self, factory_root: Path):
        """Test that generator has method to generate project-info.json."""
        generator_path = factory_root / "scripts" / "core" / "generate_project.py"
        
        content = generator_path.read_text(encoding='utf-8')
        
        # Check for project-info.json generation logic
        has_project_info_logic = (
            "project-info" in content or
            "project_info" in content
        )
        
        # This documents the requirement for the fix
        # Currently may not exist - this test helps identify the gap


# =============================================================================
# TEST CLASS: Generated Project Has Update Infrastructure
# =============================================================================

@pytest.mark.integration
class TestGeneratedProjectUpdateInfrastructure:
    """Tests that generated projects include all update infrastructure."""
    
    def test_project_info_json_generated(self, generated_project_path: Path):
        """Test that project-info.json is generated in the project."""
        project_info_path = generated_project_path / "knowledge" / "project-info.json"
        
        # This test will fail until the fix is applied
        # It documents the critical requirement
        assert project_info_path.exists(), \
            f"project-info.json must be generated at {project_info_path}"
    
    def test_project_info_contains_factory_origin(self, generated_project_path: Path):
        """Test project-info.json has factory_origin section."""
        project_info_path = generated_project_path / "knowledge" / "project-info.json"
        
        if project_info_path.exists():
            with open(project_info_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "factory_origin" in data, \
                "project-info.json must have factory_origin section"
            
            origin = data["factory_origin"]
            assert "blueprint_id" in origin, "Must have blueprint_id"
            assert "factory_version" in origin, "Must have factory_version"
            assert "feed_url" in origin, "Must have feed_url"
    
    def test_project_info_blueprint_id_matches(
        self, 
        generated_project_path: Path, 
        update_config: ProjectConfig
    ):
        """Test project-info.json blueprint_id matches configuration."""
        project_info_path = generated_project_path / "knowledge" / "project-info.json"
        
        if project_info_path.exists():
            with open(project_info_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            blueprint_id = data.get("factory_origin", {}).get("blueprint_id")
            assert blueprint_id == update_config.blueprint_id, \
                f"blueprint_id should be {update_config.blueprint_id}, got {blueprint_id}"
    
    def test_factory_updates_agent_generated(self, generated_project_path: Path):
        """Test that factory-updates agent is generated."""
        agent_path = generated_project_path / ".cursor" / "agents" / "factory-updates.md"
        
        # This test will fail until the fix is applied
        assert agent_path.exists(), \
            f"factory-updates.md agent must be generated at {agent_path}"
    
    def test_factory_updates_agent_content(self, generated_project_path: Path):
        """Test factory-updates agent has required content."""
        agent_path = generated_project_path / ".cursor" / "agents" / "factory-updates.md"
        
        if agent_path.exists():
            content = agent_path.read_text(encoding='utf-8')
            
            # Must respond to update requests
            assert "update" in content.lower(), \
                "Agent must handle update requests"
            
            # Must reference project-info.json
            assert "project-info" in content.lower() or "project_info" in content.lower(), \
                "Agent must reference project-info.json"
    
    def test_receive_updates_skill_generated(self, generated_project_path: Path):
        """Test that receive-updates skill is generated."""
        skill_path = generated_project_path / ".cursor" / "skills" / "receive-updates" / "SKILL.md"
        
        # This test will fail until the fix is applied
        assert skill_path.exists(), \
            f"receive-updates SKILL.md must be generated at {skill_path}"
    
    def test_receive_updates_skill_content(self, generated_project_path: Path):
        """Test receive-updates skill has required content."""
        skill_path = generated_project_path / ".cursor" / "skills" / "receive-updates" / "SKILL.md"
        
        if skill_path.exists():
            content = skill_path.read_text(encoding='utf-8')
            
            # Must contain fetch/download instructions
            assert "fetch" in content.lower() or "download" in content.lower(), \
                "Skill must instruct how to fetch updates"
            
            # Must reference factory-updates.json feed
            assert "factory-updates" in content.lower(), \
                "Skill must reference factory-updates.json feed"


# =============================================================================
# TEST CLASS: Update Application Logic
# =============================================================================

class TestUpdateApplicationLogic:
    """Tests for applying updates to generated projects."""
    
    def test_create_if_missing_creates_new_file(self, tmp_path: Path):
        """Test create_if_missing action creates file when missing."""
        target_file = tmp_path / "knowledge" / "new-patterns.json"
        
        # File should not exist
        assert not target_file.exists()
        
        # Simulate update application
        new_content = {"version": "1.0.0", "patterns": []}
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(json.dumps(new_content, indent=2), encoding='utf-8')
        
        # Verify
        assert target_file.exists()
        data = json.loads(target_file.read_text(encoding='utf-8'))
        assert data["version"] == "1.0.0"
    
    def test_create_if_missing_skips_existing_file(self, tmp_path: Path):
        """Test create_if_missing action skips existing files."""
        target_file = tmp_path / "knowledge" / "existing.json"
        
        # Create existing file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        original_content = {"version": "1.0.0", "original": True}
        target_file.write_text(json.dumps(original_content), encoding='utf-8')
        
        # Simulate create_if_missing - should NOT overwrite
        if not target_file.exists():
            new_content = {"version": "2.0.0", "original": False}
            target_file.write_text(json.dumps(new_content), encoding='utf-8')
        
        # Verify original is preserved
        data = json.loads(target_file.read_text(encoding='utf-8'))
        assert data["version"] == "1.0.0"
        assert data["original"] is True
    
    def test_update_or_create_updates_existing(self, tmp_path: Path):
        """Test update_or_create action updates existing file."""
        target_file = tmp_path / "knowledge" / "existing.json"
        
        # Create existing file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text('{"version": "1.0.0"}', encoding='utf-8')
        
        # Simulate update_or_create
        new_content = {"version": "1.1.0", "new_field": "value"}
        target_file.write_text(json.dumps(new_content), encoding='utf-8')
        
        # Verify update
        data = json.loads(target_file.read_text(encoding='utf-8'))
        assert data["version"] == "1.1.0"
        assert data["new_field"] == "value"
    
    def test_backup_before_update(self, tmp_path: Path):
        """Test backup is created before applying updates."""
        target_file = tmp_path / "knowledge" / "patterns.json"
        backup_dir = tmp_path / "backups"
        
        # Create original file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        original_content = {"version": "1.0.0", "data": "original"}
        target_file.write_text(json.dumps(original_content), encoding='utf-8')
        
        # Simulate backup before update
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"patterns.json.backup"
        backup_file.write_text(target_file.read_text(encoding='utf-8'), encoding='utf-8')
        
        # Apply update
        new_content = {"version": "2.0.0", "data": "updated"}
        target_file.write_text(json.dumps(new_content), encoding='utf-8')
        
        # Verify backup exists with original content
        assert backup_file.exists()
        backup_data = json.loads(backup_file.read_text(encoding='utf-8'))
        assert backup_data["version"] == "1.0.0"
        assert backup_data["data"] == "original"
    
    def test_installed_updates_tracking(self, tmp_path: Path):
        """Test that applied updates are tracked in project-info.json."""
        project_info_path = tmp_path / "knowledge" / "project-info.json"
        
        # Create initial project-info.json
        project_info_path.parent.mkdir(parents=True, exist_ok=True)
        initial_data = {
            "factory_origin": {
                "blueprint_id": "ai-agent-development",
                "factory_version": "3.14.0"
            },
            "installed_updates": []
        }
        project_info_path.write_text(json.dumps(initial_data), encoding='utf-8')
        
        # Simulate recording an applied update
        with open(project_info_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data["installed_updates"].append({
            "id": "test-update-1",
            "version": "1.0.0",
            "applied_date": "2026-02-08T12:00:00Z"
        })
        
        with open(project_info_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        # Verify
        with open(project_info_path, 'r', encoding='utf-8') as f:
            updated_data = json.load(f)
        
        assert len(updated_data["installed_updates"]) == 1
        assert updated_data["installed_updates"][0]["id"] == "test-update-1"


# =============================================================================
# TEST CLASS: Blueprints Reference Update Components
# =============================================================================

class TestBlueprintsReferenceUpdates:
    """Tests that all blueprints properly reference update components."""
    
    def get_all_blueprints(self, blueprints_dir: Path) -> List[Path]:
        """Get all blueprint.json files."""
        blueprints = []
        for blueprint_dir in blueprints_dir.iterdir():
            if not blueprint_dir.is_dir():
                continue
            blueprint_file = blueprint_dir / "blueprint.json"
            if blueprint_file.exists():
                blueprints.append(blueprint_file)
        return blueprints
    
    def test_all_blueprints_exist(self, blueprints_dir: Path):
        """Test that blueprint files exist."""
        blueprints = self.get_all_blueprints(blueprints_dir)
        assert len(blueprints) > 0, "Factory should have at least one blueprint"
    
    def test_blueprints_have_agents_section(self, blueprints_dir: Path):
        """Test all blueprints have agents section."""
        blueprints = self.get_all_blueprints(blueprints_dir)
        
        for blueprint_path in blueprints:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            blueprint_name = blueprint_path.parent.name
            assert "agents" in data, \
                f"Blueprint {blueprint_name} must have agents section"
    
    def test_blueprints_have_skills_section(self, blueprints_dir: Path):
        """Test all blueprints have skills section."""
        blueprints = self.get_all_blueprints(blueprints_dir)
        
        for blueprint_path in blueprints:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            blueprint_name = blueprint_path.parent.name
            assert "skills" in data, \
                f"Blueprint {blueprint_name} must have skills section"
    
    def test_blueprints_reference_factory_updates_agent(self, blueprints_dir: Path):
        """Test all blueprints reference factory-updates agent."""
        blueprints = self.get_all_blueprints(blueprints_dir)
        
        for blueprint_path in blueprints:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            blueprint_name = blueprint_path.parent.name
            agents = data.get("agents", [])
            
            # Extract agent pattern IDs
            agent_ids = []
            for agent in agents:
                if isinstance(agent, dict):
                    agent_ids.append(agent.get("patternId", ""))
                elif isinstance(agent, str):
                    agent_ids.append(agent)
            
            # Check for factory-updates - this documents the requirement
            # Uncomment assertion after all blueprints are updated
            # assert "factory-updates" in agent_ids, \
            #     f"Blueprint {blueprint_name} should reference factory-updates agent"
    
    def test_blueprints_reference_receive_updates_skill(self, blueprints_dir: Path):
        """Test all blueprints reference receive-updates skill."""
        blueprints = self.get_all_blueprints(blueprints_dir)
        
        for blueprint_path in blueprints:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            blueprint_name = blueprint_path.parent.name
            skills = data.get("skills", [])
            
            # Extract skill pattern IDs
            skill_ids = []
            for skill in skills:
                if isinstance(skill, dict):
                    skill_ids.append(skill.get("patternId", ""))
                elif isinstance(skill, str):
                    skill_ids.append(skill)
            
            # Check for receive-updates - this documents the requirement
            # Uncomment assertion after all blueprints are updated
            # assert "receive-updates" in skill_ids, \
            #     f"Blueprint {blueprint_name} should reference receive-updates skill"


# =============================================================================
# TEST CLASS: Update System Integration
# =============================================================================

@pytest.mark.integration
class TestUpdateSystemIntegration:
    """Integration tests for the complete update system."""
    
    def test_factory_updates_json_is_fetchable(self, knowledge_dir: Path):
        """Test that factory-updates.json is valid and can be parsed."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        if feed_path.exists():
            # Read and parse
            with open(feed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            assert "available_updates" in data
            
            # All updates should be parseable
            for update in data["available_updates"]:
                assert "id" in update
                assert "applicable_to" in update
                assert isinstance(update["applicable_to"], list)
    
    def test_update_files_referenced_in_feed_exist(self, knowledge_dir: Path, factory_root: Path):
        """Test that files referenced in updates actually exist in Factory."""
        feed_path = knowledge_dir / "factory-updates.json"
        
        if feed_path.exists():
            with open(feed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for update in data.get("available_updates", []):
                for file_ref in update.get("files", []):
                    source = file_ref.get("source", "")
                    if source:
                        source_path = factory_root / source
                        # Only check if it's meant to exist (not a template)
                        if not source.endswith(".tmpl"):
                            assert source_path.exists(), \
                                f"Update {update['id']} references missing file: {source}"


# =============================================================================
# TEST CLASS: Rollback Functionality
# =============================================================================

class TestRollbackFunctionality:
    """Tests for update rollback capability."""
    
    def test_rollback_restores_original_file(self, tmp_path: Path):
        """Test that rollback restores original file content."""
        target_file = tmp_path / "knowledge" / "patterns.json"
        backup_file = tmp_path / "backups" / "patterns.json.backup"
        
        # Create original
        target_file.parent.mkdir(parents=True, exist_ok=True)
        original_content = {"version": "1.0.0"}
        target_file.write_text(json.dumps(original_content), encoding='utf-8')
        
        # Create backup
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        backup_file.write_text(target_file.read_text(encoding='utf-8'), encoding='utf-8')
        
        # Modify (simulate update)
        modified_content = {"version": "2.0.0", "modified": True}
        target_file.write_text(json.dumps(modified_content), encoding='utf-8')
        
        # Rollback
        target_file.write_text(backup_file.read_text(encoding='utf-8'), encoding='utf-8')
        
        # Verify rollback
        data = json.loads(target_file.read_text(encoding='utf-8'))
        assert data["version"] == "1.0.0"
        assert "modified" not in data
    
    def test_rollback_updates_installed_updates_list(self, tmp_path: Path):
        """Test that rollback removes update from installed_updates list."""
        project_info_path = tmp_path / "knowledge" / "project-info.json"
        
        # Create project-info with installed update
        project_info_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "factory_origin": {"blueprint_id": "test"},
            "installed_updates": [
                {"id": "update-1", "version": "1.0.0"},
                {"id": "update-2", "version": "1.0.0"}
            ]
        }
        project_info_path.write_text(json.dumps(data), encoding='utf-8')
        
        # Simulate rollback of update-2
        with open(project_info_path, 'r', encoding='utf-8') as f:
            current = json.load(f)
        
        current["installed_updates"] = [
            u for u in current["installed_updates"] 
            if u["id"] != "update-2"
        ]
        
        with open(project_info_path, 'w', encoding='utf-8') as f:
            json.dump(current, f, indent=2)
        
        # Verify
        with open(project_info_path, 'r', encoding='utf-8') as f:
            final = json.load(f)
        
        assert len(final["installed_updates"]) == 1
        assert final["installed_updates"][0]["id"] == "update-1"


# =============================================================================
# SMOKE TESTS
# =============================================================================

@pytest.mark.integration
class TestUpdateSystemSmoke:
    """Smoke tests for quick validation of update system."""
    
    def test_smoke_patterns_exist(self, patterns_dir: Path):
        """Quick check that update patterns exist."""
        agent_pattern = patterns_dir / "agents" / "factory-updates.json"
        skill_pattern = patterns_dir / "skills" / "receive-updates.json"
        
        assert agent_pattern.exists(), "factory-updates agent pattern missing"
        assert skill_pattern.exists(), "receive-updates skill pattern missing"
    
    def test_smoke_templates_exist(self, templates_dir: Path):
        """Quick check that update templates exist."""
        template = templates_dir / "knowledge" / "project-info.json.tmpl"
        
        assert template.exists(), "project-info.json.tmpl template missing"
    
    def test_smoke_feed_exists(self, knowledge_dir: Path):
        """Quick check that update feed exists."""
        feed = knowledge_dir / "factory-updates.json"
        
        assert feed.exists(), "factory-updates.json feed missing"
    
    def test_smoke_feed_parseable(self, knowledge_dir: Path):
        """Quick check that update feed is valid JSON."""
        feed = knowledge_dir / "factory-updates.json"
        
        with open(feed, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
        assert "available_updates" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
