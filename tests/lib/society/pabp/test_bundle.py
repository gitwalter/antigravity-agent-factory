"""
Tests for PABP Bundle Creation and Validation.

This test suite verifies bundle creation, integrity verification,
and component management for portable agent behavior transfer.

SDG - Love - Truth - Beauty
"""

import tempfile
from pathlib import Path

from lib.society.pabp.bundle import (
    AgentBundle,
    BundleComponent,
    ComponentType,
    create_bundle,
    save_bundle_to_directory,
)
from lib.society.pabp.manifest import (
    BundleManifest,
    ComponentChecksum,
    create_manifest_from_bundle,
    CompatibilityRequirements,
)
from lib.society.pabp.transfer import (
    export_bundle,
    import_bundle,
    verify_bundle,
    merge_bundles,
    create_incremental_bundle,
    TransferConfig,
)


class TestBundleComponent:
    """Tests for BundleComponent class."""

    def test_component_creation(self):
        """Component can be created with basic attributes."""
        component = BundleComponent(
            component_type=ComponentType.SKILL,
            name="test-skill",
            path="skills/test-skill/SKILL.md",
            content="# Test Skill\n\nThis is a test.",
        )

        assert component.component_type == ComponentType.SKILL
        assert component.name == "test-skill"
        assert component.path == "skills/test-skill/SKILL.md"
        assert len(component.checksum) == 64  # SHA-256 hex

    def test_component_checksum_calculation(self):
        """Checksum is calculated correctly."""
        component1 = BundleComponent(
            component_type=ComponentType.SKILL,
            name="skill1",
            path="skills/skill1.md",
            content="content",
        )

        component2 = BundleComponent(
            component_type=ComponentType.SKILL,
            name="skill2",
            path="skills/skill2.md",
            content="content",
        )

        # Same content = same checksum
        assert component1.checksum == component2.checksum

    def test_component_integrity_verification(self):
        """Integrity verification detects tampering."""
        component = BundleComponent(
            component_type=ComponentType.SKILL,
            name="skill",
            path="skills/skill.md",
            content="original content",
        )

        assert component.verify_integrity()

        # Tamper with content
        component.content = "modified content"

        assert not component.verify_integrity()

    def test_component_to_dict(self):
        """Component serializes to dictionary."""
        component = BundleComponent(
            component_type=ComponentType.KNOWLEDGE,
            name="patterns",
            path="knowledge/patterns.json",
            content={"patterns": []},
            metadata={"version": "1.0.0"},
        )

        data = component.to_dict()

        assert data["component_type"] == "knowledge"
        assert data["name"] == "patterns"
        assert data["metadata"]["version"] == "1.0.0"

    def test_component_from_dict(self):
        """Component deserializes from dictionary."""
        data = {
            "component_type": "skill",
            "name": "test",
            "path": "skills/test.md",
            "checksum": "abc123",
            "metadata": {},
        }

        component = BundleComponent.from_dict(data, "content")

        assert component.component_type == ComponentType.SKILL
        assert component.content == "content"


class TestAgentBundle:
    """Tests for AgentBundle class."""

    def test_bundle_creation(self):
        """Bundle can be created with create_bundle."""
        bundle = create_bundle(
            agent_id="test-agent", agent_name="Test Agent", version="1.0.0"
        )

        assert bundle.agent_id == "test-agent"
        assert bundle.agent_name == "Test Agent"
        assert bundle.version == "1.0.0"
        assert len(bundle.bundle_id) > 0

    def test_add_skill(self):
        """Skills can be added to bundle."""
        bundle = create_bundle("agent", "Agent")

        bundle.add_skill("analyze", "# Analyze\n\nSkill content")

        assert len(bundle.components) == 1
        assert bundle.components[0].component_type == ComponentType.SKILL
        assert bundle.components[0].name == "analyze"

    def test_add_knowledge(self):
        """Knowledge can be added to bundle."""
        bundle = create_bundle("agent", "Agent")

        bundle.add_knowledge("patterns", {"patterns": [1, 2, 3]})

        assert len(bundle.components) == 1
        assert bundle.components[0].component_type == ComponentType.KNOWLEDGE

    def test_add_workflow(self):
        """Workflows can be added to bundle."""
        bundle = create_bundle("agent", "Agent")

        bundle.add_workflow("main", "name: main\nsteps:\n  - do_thing")

        assert len(bundle.components) == 1
        assert bundle.components[0].component_type == ComponentType.WORKFLOW

    def test_method_chaining(self):
        """Add methods support chaining."""
        bundle = (
            create_bundle("agent", "Agent")
            .add_skill("skill1", "content1")
            .add_skill("skill2", "content2")
            .add_knowledge("knowledge", {"data": "value"})
        )

        assert len(bundle.components) == 3

    def test_get_components_by_type(self):
        """Components can be filtered by type."""
        bundle = (
            create_bundle("agent", "Agent")
            .add_skill("skill1", "content")
            .add_skill("skill2", "content")
            .add_knowledge("knowledge", {})
        )

        skills = bundle.get_components_by_type(ComponentType.SKILL)

        assert len(skills) == 2

    def test_verify_all_components(self):
        """All components can be verified at once."""
        bundle = (
            create_bundle("agent", "Agent")
            .add_skill("skill1", "content1")
            .add_skill("skill2", "content2")
        )

        valid, invalid = bundle.verify_all_components()

        assert valid
        assert len(invalid) == 0

    def test_bundle_checksum(self):
        """Bundle checksum is deterministic."""
        bundle1 = create_bundle("agent", "Agent").add_skill("skill", "content")

        bundle2 = create_bundle("agent", "Agent").add_skill("skill", "content")

        assert bundle1.get_bundle_checksum() == bundle2.get_bundle_checksum()

    def test_to_manifest_dict(self):
        """Bundle can export manifest (without content)."""
        bundle = create_bundle("agent", "Agent").add_skill("skill", "content")

        manifest = bundle.to_manifest_dict()

        assert manifest["agent_id"] == "agent"
        assert len(manifest["components"]) == 1
        assert "content" not in manifest["components"][0]

    def test_to_dict_and_from_dict(self):
        """Bundle round-trips through serialization."""
        original = (
            create_bundle("agent", "Agent", "1.0.0")
            .add_skill("skill", "skill content")
            .add_knowledge("knowledge", {"key": "value"})
        )

        data = original.to_dict()
        restored = AgentBundle.from_dict(data)

        assert restored.agent_id == original.agent_id
        assert len(restored.components) == len(original.components)
        assert restored.get_bundle_checksum() == original.get_bundle_checksum()


class TestBundleManifest:
    """Tests for BundleManifest class."""

    def test_manifest_creation(self):
        """Manifest can be created from bundle."""
        bundle = create_bundle("agent", "Agent").add_skill("skill", "content")

        manifest = create_manifest_from_bundle(bundle)

        assert manifest.bundle_id == bundle.bundle_id
        assert len(manifest.checksums) == 1

    def test_manifest_checksum_verification(self):
        """Manifest checksum can be verified."""
        manifest = BundleManifest(
            bundle_id="test", agent_id="agent", agent_name="Agent"
        )
        manifest.checksums = [
            ComponentChecksum("path1", checksum="abc123"),
            ComponentChecksum("path2", checksum="def456"),
        ]
        manifest.bundle_checksum = manifest.calculate_bundle_checksum()

        assert manifest.verify_checksum()

    def test_compatibility_requirements(self):
        """Compatibility requirements can be checked."""
        requirements = CompatibilityRequirements(
            min_factory_version="1.0.0",
            required_skills=["base-skill"],
            python_version="3.10",
        )

        # Compatible target
        compatible, missing = requirements.check_compatibility(
            {"factory_version": "1.1.0", "skills": ["base-skill", "other-skill"]}
        )

        assert compatible
        assert len(missing) == 0

        # Incompatible target
        compatible, missing = requirements.check_compatibility(
            {"factory_version": "0.9.0", "skills": []}
        )

        assert not compatible
        assert len(missing) >= 2


class TestBundleTransfer:
    """Tests for bundle export/import operations."""

    def test_export_to_directory(self):
        """Bundle can be exported to directory."""
        bundle = create_bundle("agent", "Agent").add_skill(
            "skill", "# Skill\n\nContent"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "bundle"

            result = export_bundle(bundle, output_path, compress=False)

            assert result.success
            assert (output_path / "manifest.json").exists()
            assert (output_path / "skills" / "skill" / "SKILL.md").exists()

    def test_export_to_zip(self):
        """Bundle can be exported to zip file."""
        bundle = create_bundle("agent", "Agent").add_skill("skill", "content")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "bundle.zip"

            result = export_bundle(bundle, output_path, compress=True)

            assert result.success
            assert output_path.exists()
            assert result.components_transferred == 1

    def test_import_from_directory(self):
        """Bundle can be imported from directory."""
        original = create_bundle("agent", "Agent").add_skill("skill", "content")

        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_path = Path(tmpdir) / "bundle"
            save_bundle_to_directory(original, bundle_path)

            imported, result = import_bundle(bundle_path)

            assert result.success
            assert imported.agent_id == original.agent_id

    def test_import_from_zip(self):
        """Bundle can be imported from zip file."""
        original = (
            create_bundle("agent", "Agent")
            .add_skill("skill", "content")
            .add_knowledge("data", {"key": "value"})
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "bundle.zip"
            export_bundle(original, zip_path)

            imported, result = import_bundle(zip_path)

            assert result.success
            assert len(imported.components) == 2

    def test_round_trip_preserves_content(self):
        """Export then import preserves all content."""
        original = (
            create_bundle("agent", "Agent", "1.0.0")
            .add_skill("skill", "skill content here")
            .add_knowledge("data", {"nested": {"value": 123}})
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "bundle.zip"
            export_bundle(original, zip_path)
            imported, _ = import_bundle(zip_path)

            assert imported.get_bundle_checksum() == original.get_bundle_checksum()


class TestBundleVerification:
    """Tests for bundle verification."""

    def test_verify_valid_bundle(self):
        """Valid bundle passes verification."""
        bundle = create_bundle("agent", "Agent").add_skill("skill", "content")

        result = verify_bundle(bundle)

        assert result.success
        assert result.verification_passed

    def test_verify_tampered_bundle(self):
        """Tampered bundle fails verification."""
        bundle = create_bundle("agent", "Agent").add_skill("skill", "original")

        # Tamper with content
        bundle.components[0].content = "modified"

        result = verify_bundle(bundle)

        assert not result.verification_passed
        assert len(result.warnings) > 0


class TestBundleMerging:
    """Tests for bundle merging operations."""

    def test_merge_bundles(self):
        """Two bundles can be merged."""
        bundle1 = create_bundle("agent1", "Agent 1").add_skill("skill1", "content1")

        bundle2 = create_bundle("agent2", "Agent 2").add_skill("skill2", "content2")

        merged = merge_bundles(bundle1, bundle2)

        assert len(merged.components) == 2

    def test_merge_with_overlay_conflict(self):
        """Overlay wins on conflict."""
        base = create_bundle("agent", "Base").add_skill("shared", "base content")

        overlay = create_bundle("agent", "Overlay").add_skill(
            "shared", "overlay content"
        )

        merged = merge_bundles(base, overlay, conflict_strategy="overlay_wins")

        assert len(merged.components) == 1
        assert merged.components[0].content == "overlay content"

    def test_merge_with_base_conflict(self):
        """Base wins on conflict when specified."""
        base = create_bundle("agent", "Base").add_skill("shared", "base content")

        overlay = create_bundle("agent", "Overlay").add_skill(
            "shared", "overlay content"
        )

        merged = merge_bundles(base, overlay, conflict_strategy="base_wins")

        assert merged.components[0].content == "base content"


class TestIncrementalBundles:
    """Tests for incremental bundle creation."""

    def test_incremental_detects_new(self):
        """Incremental bundle includes new components."""
        previous = create_bundle("agent", "Agent", "1.0.0").add_skill(
            "skill1", "content1"
        )

        current = (
            create_bundle("agent", "Agent", "1.1.0")
            .add_skill("skill1", "content1")
            .add_skill("skill2", "content2")
        )

        delta = create_incremental_bundle(current, previous)

        assert len(delta.components) == 1
        assert delta.components[0].name == "skill2"

    def test_incremental_detects_changed(self):
        """Incremental bundle includes changed components."""
        previous = create_bundle("agent", "Agent", "1.0.0").add_skill(
            "skill1", "original"
        )

        current = create_bundle("agent", "Agent", "1.1.0").add_skill(
            "skill1", "modified"
        )

        delta = create_incremental_bundle(current, previous)

        assert len(delta.components) == 1

    def test_incremental_tracks_removed(self):
        """Incremental bundle tracks removed components."""
        previous = (
            create_bundle("agent", "Agent", "1.0.0")
            .add_skill("skill1", "content")
            .add_skill("skill2", "content")
        )

        current = create_bundle("agent", "Agent", "1.1.0").add_skill(
            "skill1", "content"
        )

        delta = create_incremental_bundle(current, previous)

        assert "skill2" in str(delta.compatibility.get("removed_components", []))


class TestTransferConfig:
    """Tests for TransferConfig."""

    def test_config_defaults(self):
        """Config has sensible defaults."""
        config = TransferConfig()

        assert config.verify_signatures is True
        assert config.reputation_decay == 0.8
        assert config.max_bundle_size_mb == 100

    def test_config_serialization(self):
        """Config round-trips through dict."""
        original = TransferConfig(verify_signatures=False, reputation_decay=0.9)

        data = original.to_dict()
        restored = TransferConfig.from_dict(data)

        assert restored.verify_signatures == original.verify_signatures
        assert restored.reputation_decay == original.reputation_decay
