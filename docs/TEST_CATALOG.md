# Test Catalog

*Generated on 2026-02-09 22:46:02*

## Summary

| Category | Files | Classes | Methods |
|----------|-------|---------|---------|
| general | 3 | 11 | 84 |
| guardian | 1 | 2 | 18 |
| integration | 6 | 35 | 242 |
| knowledge | 1 | 3 | 32 |
| lib | 10 | 76 | 686 |
| memory | 3 | 8 | 90 |
| unit | 23 | 226 | 1664 |
| validation | 9 | 38 | 372 |
| **Total** | **56** | **399** | **3188** |

## General Tests

### tests\test_knowledge_structure.py

*Comprehensive tests for knowledge JSON file structure validation.

Tests validate that all knowledge JSON files have:
- Required fields (id, name, version, category, description)
- patterns object exists
- best_practices array exists
- anti_patterns array exists
- Valid JSON structure*

#### TestKnowledgeFileStructure
*Tests for knowledge file structure and required fields.*

- `test_knowledge_files_exist`
  - Test that knowledge files are found.
- `test_knowledge_files_valid_json`
  - Test that all knowledge files are valid JSON.
- `test_knowledge_files_have_required_fields`
  - Test that knowledge files have required fields: id, name, version, category, description.
- `test_knowledge_id_matches_filename`
  - Test that knowledge file id matches the filename (without extension).
- `test_knowledge_files_have_patterns`
  - Test that knowledge files have a patterns object.
- `test_knowledge_files_have_best_practices`
  - Test that knowledge files have a best_practices array.
- `test_knowledge_files_have_anti_patterns`
  - Test that knowledge files have an anti_patterns array.
- `test_knowledge_version_format`
  - Test that knowledge files have valid version format (semver-like).
- `test_knowledge_category_is_valid`
  - Test that knowledge files have valid category values.

#### TestKnowledgePatternsStructure
*Tests for patterns object structure within knowledge files.*

- `test_patterns_is_not_empty`
  - Test that patterns object is not empty.
- `test_patterns_have_descriptions`
  - Test that patterns have description fields.

#### TestNewKnowledgeFiles
*Tests specifically for new knowledge files.*

- `test_new_knowledge_files_exist`
  - Test that all new knowledge files exist.
- `test_new_knowledge_files_have_valid_structure`
  - Test that all new knowledge files have valid structure.

### tests\test_skills_structure.py

*Comprehensive tests for skill file structure validation.

Tests validate that all skill files have:
- Valid YAML frontmatter with required fields (name, description, type)
- Proper markdown sections (When to Use, Prerequisites, Process, Best Practices)
- Correct file structure and naming conventions*

#### TestSkillFileStructure
*Tests for skill file structure and organization.*

- `test_skill_files_exist`
  - Test that skill files are found.
- `test_skill_files_have_yaml_frontmatter`
  - Test that all skill files have YAML frontmatter.
- `test_skill_frontmatter_has_required_fields`
  - Test that skill frontmatter has required fields: name, description, type.
- `test_skill_frontmatter_type_is_skill`
  - Test that skill frontmatter type field is 'skill'.
- `test_skill_frontmatter_name_matches_directory`
  - Test that skill name matches the directory name.
- `test_skill_frontmatter_valid_yaml`
  - Test that skill frontmatter has valid YAML syntax.

#### TestSkillMarkdownSections
*Tests for required markdown sections in skill files.*

- `test_skill_has_when_to_use_section`
  - Test that skill files have 'When to Use' section.
- `test_skill_has_prerequisites_section`
  - Test that skill files have 'Prerequisites' section.
- `test_skill_has_process_section`
  - Test that skill files have 'Process' section.
- `test_skill_has_best_practices_section`
  - Test that skill files have 'Best Practices' section.
- `test_skill_sections_have_content`
  - Test that skill sections have actual content (not just headers).

#### TestSkillFileNaming
*Tests for skill file naming conventions.*

- `test_skill_files_named_skill_md`
  - Test that skill files are named SKILL.md.
- `test_skill_directories_use_kebab_case`
  - Test that skill directories use kebab-case naming.

#### TestNewSkills
*Tests specifically for the 25 new skills mentioned.*

- `test_new_skills_exist`
  - Test that all new skills exist.
- `test_new_skills_have_valid_structure`
  - Test that all new skills have valid structure.

### tests\test_templates_syntax.py

*Comprehensive tests for Jinja2 template syntax validation.

Tests validate that all Jinja2 templates (.j2 files) have:
- Valid Jinja2 syntax
- Required variables documented (if applicable)
- Proper template structure*

#### TestTemplateSyntax
*Tests for Jinja2 template syntax validation.*

- `test_jinja2_available`
  - Test that Jinja2 is available.
- `test_template_files_exist`
  - Test that template files are found.
- `test_templates_have_valid_syntax`
  - Test that all templates have valid Jinja2 syntax.
- `test_templates_can_be_compiled`
  - Test that all templates can be compiled.
- `test_templates_have_balanced_braces`
  - Test that templates have balanced Jinja2 braces.
- `test_templates_have_valid_filters`
  - Test that templates use valid Jinja2 filters.

#### TestTemplateVariables
*Tests for template variable usage and documentation.*

- `test_templates_extract_undefined_variables`
  - Test that we can extract undefined variables from templates.
- `test_templates_use_default_filter_for_variables`
  - Test that templates use default filter for optional variables.

#### TestTemplateStructure
*Tests for template file structure and organization.*

- `test_templates_have_content`
  - Test that templates are not empty.
- `test_templates_have_reasonable_length`
  - Test that templates have reasonable content length.
- `test_templates_use_j2_extension`
  - Test that all Jinja2 templates use .j2 extension.

#### TestNewTemplates
*Tests specifically for new templates mentioned.*

- `test_new_templates_exist`
  - Test that all new templates exist.
- `test_new_templates_have_valid_syntax`
  - Test that all new templates have valid Jinja2 syntax.
- `test_new_templates_have_required_variables_documented`
  - Test that new templates document required variables (if applicable).

## Guardian Tests

### tests\guardian\test_no_axiom_drift.py

*CRITICAL Regression Tests for Axiom Protection.

These tests ensure that axioms remain IDENTICAL after any number of
learning cycles. This is the most important test in the memory system.*

#### TestNoAxiomDrift
*CRITICAL: Regression tests ensuring axioms never change.

These tests verify that no matter how many observations are made
and proposals are accepted, the core axioms remain unchanged.*

- `test_axioms_unchanged_after_learning`
  - CRITICAL: Verify axioms remain identical after learning cycles.

This test simulates many observation and acceptance cycles and
verifies that no protected files have been modified.
- `test_axiom_files_not_in_mutable_paths`
  - Verify that axiom files are not accidentally in mutable paths.
- `test_guard_blocks_all_layer0_modifications`
  - Verify that ALL Layer 0 paths are blocked.
- `test_guard_blocks_all_layer1_modifications`
  - Verify that ALL Layer 1 paths are blocked.
- `test_guard_blocks_all_layer2_modifications`
  - Verify that ALL Layer 2 paths are blocked.
- `test_induction_engine_respects_guard`
  - Verify that InductionEngine uses the guard correctly.
- `test_memory_store_does_not_touch_protected_files`
  - Verify MemoryStore only writes to its own directory.

#### TestAxiomIntegrity
*Additional integrity checks for axiom protection.*

- `test_core_axioms_file_has_correct_structure`
  - Verify core-axioms.json has the expected structure.
- `test_never_modify_list_includes_critical_files`
  - Verify NEVER_MODIFY list includes all critical files.

## Integration Tests

### tests\integration\test_cli_extension.py

*Integration tests for CLI extension commands.

Tests cover:
- --analyze-gaps command
- --coverage-report command
- --suggest-extensions command*

#### TestAnalyzeGapsCommand
*Tests for --analyze-gaps CLI command.*

- `test_analyze_gaps_exits_successfully`
  - Test that --analyze-gaps exits with code 0.
- `test_analyze_gaps_shows_coverage`
  - Test that --analyze-gaps shows coverage information.
- `test_analyze_gaps_with_scope_domain`
  - Test --analyze-gaps with domain scope.
- `test_analyze_gaps_with_scope_topic`
  - Test --analyze-gaps with topic scope.
- `test_analyze_gaps_shows_gap_types`
  - Test that output shows gap types.

#### TestCoverageReportCommand
*Tests for --coverage-report CLI command.*

- `test_coverage_report_exits_successfully`
  - Test that --coverage-report exits with code 0.
- `test_coverage_report_shows_percentage`
  - Test that coverage report shows percentage.

#### TestSuggestExtensionsCommand
*Tests for --suggest-extensions CLI command.*

- `test_suggest_extensions_exits_successfully`
  - Test that --suggest-extensions exits with code 0.
- `test_suggest_extensions_lists_candidates`
  - Test that suggest-extensions lists extension candidates.

#### TestHelpExtensionCommands
*Tests for extension command help.*

- `test_help_shows_analyze_gaps`
  - Test that help shows --analyze-gaps option.
- `test_help_shows_coverage_report`
  - Test that help shows --coverage-report option.

### tests\integration\test_cli_pm.py

*Integration tests for PM (Project Management) CLI functionality.

Tests cover:
- --help shows PM options
- PM-enabled blueprint generation creates PM artifacts
- PM backend and methodology validation*

#### TestPMHelpOutput
*Tests for PM help output in CLI.*

- `test_help_shows_pm_enabled_flag`
  - Test that --help shows --pm-enabled flag.
- `test_help_shows_pm_backend_flag`
  - Test that --help shows --pm-backend flag.
- `test_help_shows_pm_methodology_flag`
  - Test that --help shows --pm-methodology flag.
- `test_help_shows_pm_doc_backend_flag`
  - Test that --help shows --pm-doc-backend flag.

#### TestPMBlueprintGeneration
*Tests for PM-enabled blueprint generation.*

- `test_pm_enabled_runs_successfully`
  - Test that --pm-enabled runs without errors.
- `test_pm_enabled_config_recognized`
  - Test that PM config is recognized in output.
- `test_pm_disabled_no_pm_artifacts`
  - Test that without --pm-enabled, PM artifacts are not generated.

#### TestPMBackendValidation
*Tests for PM backend and methodology validation.*

- `test_valid_pm_backends_accepted`
  - Test that valid PM backends are accepted.
- `test_valid_pm_methodologies_accepted`
  - Test that valid PM methodologies are accepted.

### tests\integration\test_gap_analysis_e2e.py

*End-to-end integration tests for gap analysis workflow.

Tests cover the complete gap analysis workflow from start to finish.*

#### TestGapAnalysisWorkflow
*End-to-end tests for gap analysis workflow.*

- `test_full_analysis_workflow`
  - Test complete analysis workflow from start to finish.
- `test_analysis_produces_gaps`
  - Test that analysis produces gap findings.
- `test_analysis_identifies_coverage`
  - Test that analysis correctly identifies coverage.
- `test_analysis_with_mock_knowledge`
  - Test analysis with controlled mock knowledge.
- `test_analysis_result_serialization`
  - Test that analysis result can be serialized to JSON.

#### TestExtensionCandidates
*Tests for extension candidate selection.*

- `test_get_candidates_returns_gaps`
  - Test that get_extension_candidates returns gaps.
- `test_candidates_sorted_by_priority`
  - Test that candidates are sorted by priority.
- `test_candidates_respect_max_limit`
  - Test that max_candidates limit is respected.
- `test_candidates_filter_by_priority`
  - Test that candidates can be filtered by minimum priority.

#### TestRunGapAnalysisFunction
*Tests for the run_gap_analysis convenience function.*

- `test_run_gap_analysis_default_dir`
  - Test run_gap_analysis with default knowledge directory.
- `test_run_gap_analysis_custom_dir`
  - Test run_gap_analysis with custom directory.

#### TestTaxonomyIntegration
*Tests for taxonomy loading integration.*

- `test_load_agent_taxonomy_integration`
  - Test loading the default agent taxonomy.
- `test_taxonomy_has_substantial_content`
  - Test that taxonomy has substantial content for analysis.

### tests\integration\test_society_blueprint_generation.py

*Integration Tests for Society Blueprint Generation.

These tests verify that blueprints correctly include society
infrastructure and generated projects work end-to-end.

SDG - Love - Truth - Beauty*

#### TestBlueprintSocietyIntegration
*Tests for society integration in blueprints.*

- `test_mas_blueprint_includes_asp_knowledge`
  - MAS blueprint includes ASP knowledge files.
- `test_mas_blueprint_includes_society_templates`
  - MAS blueprint includes society templates.
- `test_mas_blueprint_includes_asp_skills`
  - MAS blueprint includes ASP skills.
- `test_aidev_blueprint_includes_asp_knowledge`
  - AI-dev blueprint includes ASP knowledge files.
- `test_aidev_blueprint_includes_society_templates`
  - AI-dev blueprint includes society templates.
- `test_aidev_blueprint_includes_asp_skills`
  - AI-dev blueprint includes ASP skills.

#### TestSocietyTemplatesExist
*Verify all required society templates exist.*

- `test_context_template_exists`
  - Society context template exists.
- `test_contracts_template_exists`
  - Society contracts template exists.
- `test_readme_template_exists`
  - Society README template exists.

#### TestASPKnowledgeFilesExist
*Verify all ASP knowledge files exist.*

- `test_asp_knowledge_exists`
  - Agent society protocol knowledge exists.
- `test_tier_matrix_exists`
  - Trust tier decision matrix exists.
- `test_pattern_selection_exists`
  - Coordination pattern selection exists.
- `test_quick_reference_exists`
  - ASP quick reference exists.

#### TestASPSkillsExist
*Verify all ASP skills exist.*

- `test_tier_selection_skill_exists`
  - Society tier selection skill exists.
- `test_export_bundle_skill_exists`
  - Export agent bundle skill exists.
- `test_verified_communication_skill_exists`
  - Verified communication skill exists.

#### TestASPDocumentationExists
*Verify ASP documentation is complete.*

- `test_value_proposition_exists`
  - ASP value proposition document exists.
- `test_integration_guide_exists`
  - Society integration guide exists.
- `test_tier_selection_guide_exists`
  - Trust tier selection guide exists.

#### TestEndToEndSocietyWorkflow
*End-to-end tests for society functionality.*

- `test_create_society_and_send_message`
  - Complete workflow: create society, add agents, send message.
- `test_create_contract_and_check_reputation`
  - Create contract and verify reputation tracking.
- `test_export_and_import_bundle`
  - Export agent bundle and import it back.
- `test_society_stats_and_audit`
  - Verify statistics and audit log work.

#### TestQuantifiedBenefits
*Tests that verify the quantified benefits claims.*

- `test_three_line_setup`
  - Verify the '3-line setup' claim works.
- `test_simplified_vs_full_api_code_reduction`
  - Simplified API requires fewer lines than full API.

### tests\integration\test_template_rendering.py

*Integration tests for template rendering with TemplateEngine.

Tests cover:
- End-to-end template rendering from files
- Factory template rendering
- Template rendering with project generator
- Macro usage in templates*

#### TestFactoryTemplateRendering
*Tests for rendering factory templates.*

- `test_guardian_protocol_template`
  - Test rendering guardian-protocol.json.tmpl.
- `test_agent_template_rendering`
  - Test rendering agent.md.tmpl with Jinja2 features.
- `test_skill_template_rendering`
  - Test rendering skill.md.tmpl with Jinja2 features.

#### TestTemplateWithFilters
*Tests for templates using custom filters.*

- `test_case_conversion_in_template`
  - Test case conversion filters in template context.
- `test_pluralize_in_template`
  - Test pluralize filter in template context.
- `test_code_block_in_template`
  - Test wrap_code filter in template context.

#### TestTemplateWithLoops
*Tests for templates with loop constructs.*

- `test_list_iteration`
  - Test iterating over a list.
- `test_dict_iteration`
  - Test iterating over a dictionary.
- `test_loop_with_index`
  - Test using loop.index.
- `test_table_generation`
  - Test generating a markdown table.

#### TestTemplateWithConditionals
*Tests for templates with conditional constructs.*

- `test_simple_if`
  - Test simple if statement.
- `test_if_else`
  - Test if-else statement.
- `test_if_with_list_check`
  - Test if with list existence check.
- `test_optional_section`
  - Test optional section based on variable presence.

#### TestLegacyPlaceholderSupport
*Tests for backward compatibility with {{UPPERCASE}} placeholders.*

- `test_uppercase_placeholder`
  - Test uppercase placeholder conversion.
- `test_mixed_placeholders`
  - Test mixing legacy and Jinja2 syntax.
- `test_curly_brace_placeholder`
  - Test single-curly-brace placeholders in context.

#### TestProjectGeneratorWithTemplates
*Tests for ProjectGenerator using template engine.*

- `test_generator_has_template_engine`
  - Test that generator initializes template engine.
- `test_build_template_context`
  - Test building template context from config.

### tests\integration\test_update_system.py

*Integration tests for Factory Update System.

Tests the complete update flow from Factory -> Generated Projects:
1. Project generation includes update infrastructure
2. project-info.json is correctly generated  
3. factory-updates agent is included
4. receive-updates skill is included
5. Update detection and application works

These tests are CRITICAL for verifying the update system works end-to-end.

Author: Cursor Agent Factory
Version: 1.0.0*

#### TestUpdatePatternsExist
*Tests that all update-related pattern files exist in the Factory.*

- `test_factory_updates_agent_pattern_exists`
  - Test factory-updates agent pattern exists.
- `test_factory_updates_agent_pattern_valid_json`
  - Test factory-updates agent pattern is valid JSON.
- `test_receive_updates_skill_pattern_exists`
  - Test receive-updates skill pattern exists.
- `test_receive_updates_skill_pattern_valid_json`
  - Test receive-updates skill pattern is valid JSON.

#### TestUpdateTemplatesExist
*Tests that update-related template files exist.*

- `test_project_info_template_exists`
  - Test project-info.json.tmpl template exists.
- `test_project_info_template_contains_placeholders`
  - Test project-info.json.tmpl contains required placeholders.

#### TestFactoryUpdatesFeed
*Tests for factory-updates.json structure and validity.*

- `test_factory_updates_json_exists`
  - Test that factory-updates.json exists in Factory.
- `test_factory_updates_json_valid_structure`
  - Test factory-updates.json has valid structure.
- `test_factory_updates_has_update_channels`
  - Test factory-updates.json has update_channels defined.
- `test_factory_updates_has_feed_url`
  - Test factory-updates.json has feed_url for remote access.
- `test_all_updates_have_required_fields`
  - Test all updates in feed have required fields.

#### TestUpdateFiltering
*Tests for filtering updates by blueprint_id.*

- `test_filter_updates_by_specific_blueprint`
  - Test that updates are correctly filtered by specific blueprint_id.
- `test_filter_updates_excludes_other_blueprints`
  - Test that updates for other blueprints are excluded.
- `test_filter_updates_web_blueprint`
  - Test filtering for web blueprints.
- `test_filter_by_channel`
  - Test filtering by update channel.
- `test_filter_handles_all_keyword`
  - Test that 'all' keyword matches any blueprint.

#### TestGeneratorIncludesUpdateComponents
*Tests that ProjectGenerator includes update components in generated projects.*

- `test_generator_has_factory_updates_in_standard_agents`
  - Test that factory-updates is referenced in standard_agents or default generation.
- `test_generator_has_receive_updates_in_standard_skills`
  - Test that receive-updates is referenced in standard_skills or default generation.
- `test_generator_has_project_info_generation`
  - Test that generator has method to generate project-info.json.

#### TestGeneratedProjectUpdateInfrastructure
*Tests that generated projects include all update infrastructure.*
**Markers:** integration

- `test_project_info_json_generated`
  - Test that project-info.json is generated in the project.
- `test_project_info_contains_factory_origin`
  - Test project-info.json has factory_origin section.
- `test_project_info_blueprint_id_matches`
  - Test project-info.json blueprint_id matches configuration.
- `test_factory_updates_agent_generated`
  - Test that factory-updates agent is generated.
- `test_factory_updates_agent_content`
  - Test factory-updates agent has required content.
- `test_receive_updates_skill_generated`
  - Test that receive-updates skill is generated.
- `test_receive_updates_skill_content`
  - Test receive-updates skill has required content.

#### TestUpdateApplicationLogic
*Tests for applying updates to generated projects.*

- `test_create_if_missing_creates_new_file`
  - Test create_if_missing action creates file when missing.
- `test_create_if_missing_skips_existing_file`
  - Test create_if_missing action skips existing files.
- `test_update_or_create_updates_existing`
  - Test update_or_create action updates existing file.
- `test_backup_before_update`
  - Test backup is created before applying updates.
- `test_installed_updates_tracking`
  - Test that applied updates are tracked in project-info.json.

#### TestBlueprintsReferenceUpdates
*Tests that all blueprints properly reference update components.*

- `test_all_blueprints_exist`
  - Test that blueprint files exist.
- `test_blueprints_have_agents_section`
  - Test all blueprints have agents section.
- `test_blueprints_have_skills_section`
  - Test all blueprints have skills section.
- `test_blueprints_reference_factory_updates_agent`
  - Test all blueprints reference factory-updates agent.
- `test_blueprints_reference_receive_updates_skill`
  - Test all blueprints reference receive-updates skill.

#### TestUpdateSystemIntegration
*Integration tests for the complete update system.*
**Markers:** integration

- `test_factory_updates_json_is_fetchable`
  - Test that factory-updates.json is valid and can be parsed.
- `test_update_files_referenced_in_feed_exist`
  - Test that files referenced in updates actually exist in Factory.

#### TestRollbackFunctionality
*Tests for update rollback capability.*

- `test_rollback_restores_original_file`
  - Test that rollback restores original file content.
- `test_rollback_updates_installed_updates_list`
  - Test that rollback removes update from installed_updates list.

#### TestUpdateSystemSmoke
*Smoke tests for quick validation of update system.*
**Markers:** integration

- `test_smoke_patterns_exist`
  - Quick check that update patterns exist.
- `test_smoke_templates_exist`
  - Quick check that update templates exist.
- `test_smoke_feed_exists`
  - Quick check that update feed exists.
- `test_smoke_feed_parseable`
  - Quick check that update feed is valid JSON.

## Knowledge Tests

### tests\knowledge\test_tier_selection.py

*Tests for Trust Tier Decision Matrix Knowledge.

This test suite verifies that the tier selection knowledge file
provides correct guidance for all scenarios.

SDG - Love - Truth - Beauty*

#### TestTierSelectionKnowledge
*Tests for trust-tier-decision-matrix.json.*

- `test_knowledge_structure`
  - Knowledge file has required structure.
- `test_all_tiers_defined`
  - All five tiers are defined.
- `test_tier_attributes`
  - Each tier has required attributes.
- `test_selection_algorithm_steps`
  - Selection algorithm has ordered steps.
- `test_escalation_triggers`
  - Escalation triggers are defined.
- `test_de_escalation_defined`
  - De-escalation path is defined.
- `test_cost_benefit_analysis`
  - Cost-benefit analysis is provided.

#### TestCoordinationPatternKnowledge
*Tests for coordination-pattern-selection.json.*

- `test_knowledge_structure`
  - Knowledge file has required structure.
- `test_core_patterns_defined`
  - Core coordination patterns are defined.
- `test_pattern_attributes`
  - Each pattern has required attributes.
- `test_anti_patterns_documented`
  - Anti-patterns are documented.

#### TestQuickReferenceKnowledge
*Tests for asp-quick-reference.json.*

- `test_knowledge_structure`
  - Quick reference has required sections.
- `test_quick_start_examples`
  - Quick start includes runnable examples.
- `test_api_reference_complete`
  - API reference covers main classes.
- `test_message_types_documented`
  - All message types are documented.
- `test_troubleshooting_guidance`
  - Common issues have solutions.

## Lib Tests

### tests\lib\society\pabp\test_bundle.py

*Tests for PABP Bundle Creation and Validation.

This test suite verifies bundle creation, integrity verification,
and component management for portable agent behavior transfer.

SDG - Love - Truth - Beauty*

#### TestBundleComponent
*Tests for BundleComponent class.*

- `test_component_creation`
  - Component can be created with basic attributes.
- `test_component_checksum_calculation`
  - Checksum is calculated correctly.
- `test_component_integrity_verification`
  - Integrity verification detects tampering.
- `test_component_to_dict`
  - Component serializes to dictionary.
- `test_component_from_dict`
  - Component deserializes from dictionary.

#### TestAgentBundle
*Tests for AgentBundle class.*

- `test_bundle_creation`
  - Bundle can be created with create_bundle.
- `test_add_skill`
  - Skills can be added to bundle.
- `test_add_knowledge`
  - Knowledge can be added to bundle.
- `test_add_workflow`
  - Workflows can be added to bundle.
- `test_method_chaining`
  - Add methods support chaining.
- `test_get_components_by_type`
  - Components can be filtered by type.
- `test_verify_all_components`
  - All components can be verified at once.
- `test_bundle_checksum`
  - Bundle checksum is deterministic.
- `test_to_manifest_dict`
  - Bundle can export manifest (without content).
- `test_to_dict_and_from_dict`
  - Bundle round-trips through serialization.

#### TestBundleManifest
*Tests for BundleManifest class.*

- `test_manifest_creation`
  - Manifest can be created from bundle.
- `test_manifest_checksum_verification`
  - Manifest checksum can be verified.
- `test_compatibility_requirements`
  - Compatibility requirements can be checked.

#### TestBundleTransfer
*Tests for bundle export/import operations.*

- `test_export_to_directory`
  - Bundle can be exported to directory.
- `test_export_to_zip`
  - Bundle can be exported to zip file.
- `test_import_from_directory`
  - Bundle can be imported from directory.
- `test_import_from_zip`
  - Bundle can be imported from zip file.
- `test_round_trip_preserves_content`
  - Export then import preserves all content.

#### TestBundleVerification
*Tests for bundle verification.*

- `test_verify_valid_bundle`
  - Valid bundle passes verification.
- `test_verify_tampered_bundle`
  - Tampered bundle fails verification.

#### TestBundleMerging
*Tests for bundle merging operations.*

- `test_merge_bundles`
  - Two bundles can be merged.
- `test_merge_with_overlay_conflict`
  - Overlay wins on conflict.
- `test_merge_with_base_conflict`
  - Base wins on conflict when specified.

#### TestIncrementalBundles
*Tests for incremental bundle creation.*

- `test_incremental_detects_new`
  - Incremental bundle includes new components.
- `test_incremental_detects_changed`
  - Incremental bundle includes changed components.
- `test_incremental_tracks_removed`
  - Incremental bundle tracks removed components.

#### TestTransferConfig
*Tests for TransferConfig.*

- `test_config_defaults`
  - Config has sensible defaults.
- `test_config_serialization`
  - Config round-trips through dict.

### tests\lib\society\test_blockchain.py

*Tests for the blockchain module.

Tests Merkle trees, anchoring, and attestations.*

#### TestMerkleTree
*Tests for MerkleTree.*

- `test_empty_tree`
  - Test empty tree.
- `test_single_leaf`
  - Test tree with single leaf.
- `test_multiple_leaves`
  - Test tree with multiple leaves.
- `test_deterministic_root`
  - Test that same data produces same root.
- `test_different_data_different_root`
  - Test that different data produces different root.
- `test_get_proof`
  - Test getting Merkle proof.
- `test_verify_proof`
  - Test verifying Merkle proof.
- `test_verify_proof_fails_for_wrong_data`
  - Test that proof verification fails for wrong data.
- `test_cannot_add_after_build`
  - Test that adding after build raises error.

#### TestLocalAnchor
*Tests for LocalAnchor.*

- `test_submit_anchor`
  - Test submitting an anchor.
- `test_verify_anchor`
  - Test verifying an anchor.
- `test_verify_fails_wrong_root`
  - Test that verification fails for wrong root.
- `test_get_anchor_status`
  - Test getting anchor status.
- `test_unknown_transaction`
  - Test status for unknown transaction.

#### TestAnchorService
*Tests for AnchorService.*

- `test_add_event`
  - Test adding events.
- `test_create_anchor`
  - Test creating an anchor.
- `test_submit_anchor`
  - Test submitting an anchor.
- `test_get_proof`
  - Test getting event proof.
- `test_verify_event`
  - Test verifying an event.
- `test_auto_anchor_on_threshold`
  - Test auto-anchoring when threshold is reached.

#### TestSolanaAnchor
*Tests for SolanaAnchor (stub mode).*

- `test_create_with_config`
  - Test creating with configuration.
- `test_connect`
  - Test connecting (stub mode).
- `test_submit_and_verify`
  - Test submitting and verifying (stub mode).
- `test_get_stats`
  - Test getting statistics.

#### TestCreateSolanaAnchor
*Tests for create_solana_anchor factory.*

- `test_create_devnet`
  - Test creating devnet anchor.
- `test_create_testnet`
  - Test creating testnet anchor.

#### TestAttestation
*Tests for Attestation.*

- `test_create_attestation`
  - Test creating an attestation.
- `test_is_valid`
  - Test validity checking.
- `test_compute_hash`
  - Test hash computation.

#### TestAttestationRegistry
*Tests for AttestationRegistry.*

- `test_create_attestation`
  - Test creating attestation through registry.
- `test_get_attestation`
  - Test getting attestation.
- `test_get_for_subject`
  - Test getting attestations by subject.
- `test_verify_attestation`
  - Test verifying attestation.
- `test_verify_expired_attestation`
  - Test verifying expired attestation.
- `test_create_and_fulfill_request`
  - Test attestation request workflow.

### tests\lib\society\test_contracts.py

*Tests for the contracts module.

Tests contract schema, registry, and verification.*

#### TestParty
*Tests for Party dataclass.*

- `test_create_party`
  - Test creating a party.
- `test_party_to_dict`
  - Test party serialization.

#### TestCapability
*Tests for Capability dataclass.*

- `test_create_capability`
  - Test creating a capability.

#### TestObligation
*Tests for Obligation dataclass.*

- `test_create_obligation`
  - Test creating an obligation.

#### TestAgentContract
*Tests for AgentContract dataclass.*

- `test_create_contract`
  - Test creating a contract.
- `test_is_active`
  - Test contract active status.
- `test_get_party`
  - Test getting party by agent ID.
- `test_get_role`
  - Test getting party role.
- `test_has_capability`
  - Test checking capability.
- `test_is_prohibited`
  - Test checking prohibition.
- `test_contract_to_dict`
  - Test contract serialization.
- `test_contract_compute_hash`
  - Test contract hash computation.

#### TestContractRegistry
*Tests for ContractRegistry.*

- `test_add_and_get_contract`
  - Test adding and retrieving contracts.
- `test_remove_contract`
  - Test removing contracts.
- `test_find_contracts_by_agent`
  - Test finding contracts by agent using find_contracts().
- `test_contracts_property`
  - Test getting all contracts via contracts property.
- `test_persistence`
  - Test automatic persistence via storage_path.
- `test_active_contracts_property`
  - Test active_contracts property returns only signed contracts.
- `test_remove_contract_not_found`
  - Test removing a contract that doesn't exist.
- `test_remove_contract_with_storage`
  - Test removing contract triggers save when storage_path is set.
- `test_create_contract`
  - Test create_contract method.
- `test_sign_contract_success`
  - Test signing a contract successfully.
- `test_sign_contract_not_found`
  - Test signing a contract that doesn't exist.
- `test_sign_contract_not_party`
  - Test signing a contract when agent is not a party.
- `test_sign_contract_fully_signed`
  - Test signing completes contract when all parties sign.
- `test_sign_contract_with_storage`
  - Test signing triggers save when storage_path is set.
- `test_find_contracts_active_only_filtering`
  - Test find_contracts filters by active_only parameter.
- `test_find_contracts_agent_b_not_party`
  - Test find_contracts when agent_b is not a party.
- `test_find_by_role`
  - Test find_by_role method.
- `test_find_by_role_active_only`
  - Test find_by_role with active_only filtering.
- `test_get_agent_roles`
  - Test get_agent_roles method.
- `test_get_agent_roles_not_in_contracts`
  - Test get_agent_roles when agent is not in any contracts.
- `test_cleanup_expired`
  - Test cleanup_expired removes expired contracts.
- `test_cleanup_expired_no_expired`
  - Test cleanup_expired when no contracts are expired.
- `test_cleanup_expired_with_storage`
  - Test cleanup_expired triggers save when storage_path is set.
- `test_save_no_storage_path`
  - Test _save() does nothing when storage_path is None.
- `test_load_no_storage_path`
  - Test _load() does nothing when storage_path is None.
- `test_load_file_not_exists`
  - Test _load() handles non-existent file gracefully.

#### TestContractVerifier
*Tests for ContractVerifier.*

- `test_verify_allowed_action`
  - Test verifying allowed action.
- `test_verify_prohibited_action`
  - Test verifying prohibited action.
- `test_verify_unauthorized_action`
  - Test verifying unauthorized action.
- `test_verify_non_party_action`
  - Test verifying action by non-party.
- `test_verify_message_no_contract`
  - Test verify_message when no contract exists.
- `test_verify_message_allowed_action`
  - Test verify_message with allowed action.
- `test_verify_message_prohibited_action`
  - Test verify_message with prohibited action.
- `test_verify_message_lacks_capability`
  - Test verify_message when agent lacks capability.
- `test_verify_message_multiple_contracts`
  - Test verify_message when multiple contracts exist.
- `test_track_obligation`
  - Test tracking an obligation trigger.
- `test_track_obligation_multiple_triggers`
  - Test tracking multiple obligation triggers.
- `test_fulfill_obligation_success`
  - Test fulfilling an obligation successfully.
- `test_fulfill_obligation_no_contract`
  - Test fulfilling obligation when contract doesn't exist.
- `test_fulfill_obligation_not_party`
  - Test fulfilling obligation when agent is not a party.
- `test_fulfill_obligation_no_matching_action`
  - Test fulfilling obligation when action doesn't match.
- `test_check_pending_obligations_no_contract`
  - Test checking pending obligations when contract doesn't exist.
- `test_check_pending_obligations_not_party`
  - Test checking pending obligations when agent is not a party.
- `test_check_pending_obligations_timeout_exceeded`
  - Test checking pending obligations when timeout is exceeded.
- `test_check_pending_obligations_within_timeout`
  - Test checking pending obligations when still within timeout.
- `test_check_pending_obligations_default_timeout`
  - Test checking pending obligations with default timeout.

#### TestContractVerificationResult
*Tests for ContractVerificationResult.*

- `test_no_violations_when_empty`
  - Test no violations when empty.
- `test_has_violations_when_present`
  - Test has_violations when violations present.
- `test_to_dict`
  - Test ContractVerificationResult.to_dict() method.

#### TestViolation
*Tests for Violation dataclass.*

- `test_to_dict`
  - Test Violation.to_dict() method.

### tests\lib\society\test_events.py

*Tests for the events module.

Tests event sourcing, hash chains, and event storage.*

#### TestAgent
*Tests for Agent dataclass.*

- `test_create_agent`
  - Test creating an agent.
- `test_agent_to_dict`
  - Test agent serialization.

#### TestAction
*Tests for Action dataclass.*

- `test_create_action`
  - Test creating an action.
- `test_action_to_dict`
  - Test action serialization.

#### TestAgentEvent
*Tests for AgentEvent dataclass.*

- `test_create_event`
  - Test creating an event.
- `test_event_to_canonical_json`
  - Test canonical JSON serialization.
- `test_event_compute_hash`
  - Test event hash computation.
- `test_event_different_hash_for_different_events`
  - Test that different events have different hashes.

#### TestHashChain
*Tests for HashChain.*

- `test_compute_event_hash`
  - Test computing event hash.
- `test_verify_chain_link`
  - Test verifying chain links.

#### TestEventStore
*Tests for EventStore.*

- `test_append_event`
  - Test appending events using store.append().
- `test_append_sets_sequence`
  - Test that append sets sequence numbers (starting from 1).
- `test_append_sets_previous_hash`
  - Test that append sets previous hash for chain linking.
- `test_query_by_agent`
  - Test querying events by agent using EventQuery.
- `test_chain_integrity`
  - Test chain integrity via verify_chain_integrity function.
- `test_persistence`
  - Test automatic persistence via storage_path.

#### TestVerifyChainIntegrity
*Tests for chain integrity verification.*

- `test_verify_empty_chain`
  - Test verifying empty chain.
- `test_verify_single_event`
  - Test verifying single event chain (sequence=1 for genesis).
- `test_verify_valid_chain`
  - Test verifying valid chain using EventStore which handles chaining.

### tests\lib\society\test_hybrid.py

*Tests for the hybrid module.

Tests unified verification system and escalation management.*

#### TestSystemConfig
*Tests for SystemConfig.*

- `test_default_config`
  - Test default configuration.
- `test_custom_config`
  - Test custom configuration.
- `test_to_dict`
  - Test config serialization.

#### TestHybridVerificationResult
*Tests for HybridVerificationResult.*

- `test_create_result`
  - Test creating a result.
- `test_to_dict`
  - Test result serialization.

#### TestHybridVerificationSystem
*Tests for HybridVerificationSystem.*

- `test_create_default`
  - Test creating default system.
- `test_create_with_blockchain`
  - Test creating system with blockchain.
- `test_record_event_basic`
  - Test recording event with basic verification.
- `test_record_event_standard`
  - Test recording event with standard verification.
- `test_record_event_full`
  - Test recording event with full verification.
- `test_clean_event_passes`
  - Test that clean events pass verification.
- `test_is_trusted`
  - Test trust checking.
- `test_delegate_trust`
  - Test trust delegation.
- `test_get_stats`
  - Test getting statistics.
- `test_get_agent_profile`
  - Test getting agent profile.
- `test_violation_handler`
  - Test violation handler callback.

#### TestEscalation
*Tests for Escalation.*

- `test_create_escalation`
  - Test creating an escalation.
- `test_is_open`
  - Test is_open property.
- `test_to_dict`
  - Test serialization.

#### TestDefaultPolicy
*Tests for DefaultPolicy.*

- `test_add_handlers`
  - Test adding handlers.
- `test_get_handler_for_level`
  - Test getting handler based on level.
- `test_timeout_varies_by_level`
  - Test that timeout varies by level.

#### TestEscalationManager
*Tests for EscalationManager.*

- `test_create_escalation`
  - Test creating an escalation.
- `test_acknowledge`
  - Test acknowledging an escalation.
- `test_resolve`
  - Test resolving an escalation.
- `test_dismiss`
  - Test dismissing an escalation.
- `test_escalate_further`
  - Test escalating to higher level.
- `test_get_open_escalations`
  - Test getting open escalations.
- `test_get_statistics`
  - Test getting statistics.
- `test_notification_handler`
  - Test notification handler is called.
- `test_level_handler`
  - Test level-specific handler is called.

### tests\lib\society\test_integration.py

*Tests for the integration module.

Tests SocietyContext, AgentSocietyBridge, and MessageRouter.*

#### TestSocietyConfig
*Tests for SocietyConfig.*

- `test_default_config`
  - Test default configuration.
- `test_custom_config`
  - Test custom configuration.
- `test_to_dict`
  - Test config serialization.

#### TestSocietyContext
*Tests for SocietyContext.*

- `test_create_default`
  - Test creating default context.
- `test_create_with_name`
  - Test creating context with custom name.
- `test_create_with_persistence`
  - Test creating context with persistence path.
- `test_get_stats`
  - Test getting statistics.
- `test_record_verification`
  - Test recording verification statistics.
- `test_record_message`
  - Test recording message statistics.
- `test_get_agent_status`
  - Test getting agent status.
- `test_export`
  - Test exporting context state.

#### TestAgentSocietyBridge
*Tests for AgentSocietyBridge.*

- `test_create_bridge`
  - Test creating a bridge.
- `test_initial_reputation`
  - Test initial reputation score.
- `test_send_message`
  - Test sending a message.
- `test_send_message_verified`
  - Test that clean messages pass verification.
- `test_send_decision`
  - Test recording a decision.
- `test_message_handler`
  - Test adding message handler.
- `test_get_status`
  - Test getting agent status.

#### TestAgentContractCreation
*Tests for contract creation via bridges.*

- `test_create_contract`
  - Test creating a contract between agents.
- `test_sign_contract`
  - Test signing a contract.

#### TestMessageRouter
*Tests for MessageRouter.*

- `test_register_agent`
  - Test registering an agent.
- `test_unregister_agent`
  - Test unregistering an agent.
- `test_route_to_registered_agent`
  - Test routing to a registered agent.
- `test_queue_for_offline_agent`
  - Test queuing messages for offline agents.
- `test_deliver_queued_on_registration`
  - Test that queued messages are delivered on registration.
- `test_get_stats`
  - Test getting router statistics.
- `test_delivery_handler`
  - Test delivery handler callback.

#### TestEndToEndCommunication
*End-to-end tests for agent communication.*

- `test_two_agents_communicate`
  - Test two agents communicating through the system.
- `test_contract_enforced_communication`
  - Test that contracts are checked during communication.

### tests\lib\society\test_simple_api.py

*Tests for the Simplified Society API.

This test suite verifies the simplified API for multi-agent coordination,
ensuring 3-line setup works correctly with proper verification.

SDG - Love - Truth - Beauty*

#### TestSimpleSociety
*Tests for SimpleSociety class.*

- `test_create_society_minimal`
  - Society can be created with just a name.
- `test_create_society_with_agents`
  - Society can be created with initial agents.
- `test_create_society_with_preset`
  - Society respects preset configuration.
- `test_add_agent`
  - Agents can be added after creation.
- `test_add_agent_idempotent`
  - Adding same agent twice is idempotent.
- `test_remove_agent`
  - Agents can be removed from society.
- `test_send_message_between_agents`
  - Messages can be sent between registered agents.
- `test_send_message_unregistered_sender`
  - Sending from unregistered agent returns error.
- `test_send_message_unregistered_receiver`
  - Sending to unregistered agent returns error.
- `test_broadcast_message`
  - Broadcast sends to all agents except sender.
- `test_broadcast_with_exclude`
  - Broadcast can exclude specific agents.
- `test_message_handler_registration`
  - Message handlers can be registered.
- `test_get_reputation`
  - Reputation can be retrieved for agents.
- `test_get_trust_level`
  - Trust level can be retrieved for agents.
- `test_get_agent_status`
  - Full agent status can be retrieved.
- `test_create_contract`
  - Contracts can be created between agents.
- `test_get_stats`
  - Society statistics can be retrieved.
- `test_export_audit_log`
  - Audit log can be exported.

#### TestQuickSend
*Tests for quick_send convenience function.*

- `test_quick_send_creates_temporary_society`
  - quick_send creates a temporary society for one-off messages.

#### TestPresets
*Tests for society presets.*

- `test_supervisor_worker_society`
  - Supervisor-worker pattern creates correct structure.
- `test_peer_society`
  - Peer society creates equal agents.
- `test_pipeline_society`
  - Pipeline society creates sequential stages.
- `test_hierarchical_society`
  - Hierarchical society creates correct structure.
- `test_get_preset_config`
  - Preset configurations can be retrieved.
- `test_list_presets`
  - All presets can be listed.

#### TestSocietyBuilder
*Tests for SocietyBuilder fluent API.*

- `test_builder_basic`
  - Builder creates society with defaults.
- `test_builder_with_preset`
  - Builder respects preset.
- `test_builder_with_agents`
  - Builder adds agents.
- `test_builder_fluent_chaining`
  - Builder supports fluent chaining.

#### TestSendResult
*Tests for SendResult dataclass.*

- `test_send_result_success`
  - SendResult correctly reports success.
- `test_send_result_failure`
  - SendResult correctly reports failure.
- `test_send_result_with_violations`
  - SendResult includes violations.

#### TestMessageCounting
*Tests for message counting functionality.*

- `test_message_count_increments`
  - Message counts increment on send.

#### TestIntegration
*Integration tests for the simplified API.*

- `test_full_workflow`
  - Complete workflow from creation to message to stats.
- `test_three_line_setup`
  - Verify the 3-line setup claim works.

### tests\lib\society\test_society.py

*Tests for the society module.

Tests organizational patterns and communication protocols.*

#### TestRole
*Tests for Role dataclass.*

- `test_create_role`
  - Test creating a role.
- `test_has_capability`
  - Test capability checking.
- `test_wildcard_capability`
  - Test wildcard capability.

#### TestProposal
*Tests for Proposal dataclass.*

- `test_create_proposal`
  - Test creating a proposal.
- `test_vote_count`
  - Test vote counting.

#### TestFlatDemocracy
*Tests for FlatDemocracy pattern.*

- `test_governance_model`
  - Test governance model type.
- `test_add_member`
  - Test adding members.
- `test_equal_voting_weight`
  - Test that all members have equal weight.
- `test_create_proposal`
  - Test creating proposals.
- `test_vote_on_proposal`
  - Test voting on proposals.
- `test_evaluate_proposal_majority`
  - Test majority wins.

#### TestMeritocracy
*Tests for Meritocracy pattern.*

- `test_governance_model`
  - Test governance model type.
- `test_reputation_weighted_voting`
  - Test reputation-weighted voting.

#### TestHierarchy
*Tests for Hierarchy pattern.*

- `test_governance_model`
  - Test governance model type.
- `test_default_roles`
  - Test default roles are created.
- `test_role_voting_weight`
  - Test role-based voting weight.
- `test_leader_has_final_say`
  - Test that leader's vote decides.

#### TestFederation
*Tests for Federation pattern.*

- `test_governance_model`
  - Test governance model type.
- `test_create_sub_society`
  - Test creating sub-societies.
- `test_add_to_sub_society`
  - Test adding members to sub-societies.
- `test_representative_voting`
  - Test that representatives vote for groups.

#### TestDAOSociety
*Tests for DAOSociety pattern.*

- `test_governance_model`
  - Test governance model type.
- `test_stake_based_voting`
  - Test stake-based voting weight.
- `test_quorum_requirement`
  - Test quorum requirement.

#### TestCreateSociety
*Tests for create_society factory function.*

- `test_create_flat_democracy`
  - Test creating flat democracy.
- `test_create_meritocracy`
  - Test creating meritocracy.
- `test_create_hierarchy`
  - Test creating hierarchy.
- `test_create_federation`
  - Test creating federation.
- `test_create_dao`
  - Test creating DAO.

#### TestMessage
*Tests for Message dataclass.*

- `test_create_message`
  - Test creating a message.
- `test_is_broadcast`
  - Test broadcast detection.
- `test_compute_hash`
  - Test message hash computation.

#### TestDirectProtocol
*Tests for DirectProtocol.*

- `test_send_and_receive`
  - Test sending and receiving messages.
- `test_receive_clears_queue`
  - Test that receive clears the queue.

#### TestBroadcastProtocol
*Tests for BroadcastProtocol.*

- `test_subscribe_and_receive`
  - Test subscribing and receiving broadcasts.

#### TestConsensusProtocol
*Tests for ConsensusProtocol.*

- `test_propose_and_vote`
  - Test proposing and voting.

#### TestMessageRouter
*Tests for MessageRouter.*

- `test_register_and_route`
  - Test registering protocols and routing.

### tests\lib\society\test_trust.py

*Tests for the trust module.

Tests identity, reputation, and trust delegation.*

#### TestKeyPair
*Tests for KeyPair.*

- `test_generate_keypair`
  - Test generating a key pair.
- `test_sign_and_verify`
  - Test signing and verifying a message.
- `test_verify_fails_for_wrong_message`
  - Test that verification fails for wrong message.
- `test_to_dict_without_private`
  - Test serialization without private key.
- `test_to_dict_with_private`
  - Test serialization with private key.

#### TestAgentIdentity
*Tests for AgentIdentity.*

- `test_create_identity`
  - Test creating an agent identity.
- `test_sign_message`
  - Test signing a message.
- `test_verify_signature`
  - Test verifying a signature.
- `test_sign_json`
  - Test signing JSON data.
- `test_to_public_dict`
  - Test public serialization.
- `test_save_and_load`
  - Test saving and loading identity.

#### TestIdentityRegistry
*Tests for IdentityRegistry.*

- `test_register_identity`
  - Test registering an identity.
- `test_get_public_key`
  - Test getting public key.
- `test_verify_signature`
  - Test verifying signature through registry.
- `test_list_agents`
  - Test listing registered agents.

#### TestReputationScore
*Tests for ReputationScore.*

- `test_initial_score`
  - Test initial reputation score.
- `test_add_positive_event`
  - Test adding positive reputation event.
- `test_add_negative_event`
  - Test adding negative reputation event.
- `test_score_bounds`
  - Test that score stays within bounds.
- `test_trust_levels`
  - Test trust level thresholds.

#### TestReputationSystem
*Tests for ReputationSystem.*

- `test_get_score_creates_default`
  - Test that get_score creates default for new agents.
- `test_record_compliance`
  - Test recording compliance.
- `test_record_violation`
  - Test recording violation.
- `test_record_contract_event`
  - Test recording contract event.
- `test_record_endorsement`
  - Test recording endorsement.
- `test_get_trusted_agents`
  - Test getting trusted agents.
- `test_get_rankings`
  - Test getting rankings.

#### TestTrustDelegation
*Tests for TrustDelegation.*

- `test_create_delegation`
  - Test creating a trust delegation.
- `test_is_valid`
  - Test validity checking.
- `test_covers_scope`
  - Test scope coverage.
- `test_wildcard_scope`
  - Test wildcard scope.

#### TestTrustGraph
*Tests for TrustGraph.*

- `test_delegate_trust`
  - Test delegating trust.
- `test_get_direct_trust`
  - Test getting direct trust.
- `test_revoke_trust`
  - Test revoking trust.
- `test_effective_trust_direct`
  - Test effective trust for direct delegation.
- `test_effective_trust_transitive`
  - Test transitive trust computation.
- `test_find_trust_path`
  - Test finding trust path.
- `test_get_delegates`
  - Test getting delegates.
- `test_get_delegators`
  - Test getting delegators.
- `test_get_trust_network`
  - Test getting trust network.

### tests\lib\society\test_verification.py

*Tests for the verification module.

Tests axiom verifiers and compliance monitoring.*

#### TestA0SDGVerifier
*Tests for A0 SDG Verifier.*

- `test_passes_sustainable_action`
  - Test that sustainable actions pass.
- `test_fails_wasteful_action`
  - Test that wasteful actions fail.

#### TestA1LoveVerifier
*Tests for A1 Love Verifier.*

- `test_passes_user_beneficial_action`
  - Test that user-beneficial actions pass.
- `test_fails_manipulative_action`
  - Test that manipulative actions fail.

#### TestA2TruthVerifier
*Tests for A2 Truth Verifier.*

- `test_passes_transparent_action`
  - Test that transparent actions pass.
- `test_fails_deceptive_action`
  - Test that deceptive actions fail.

#### TestA3BeautyVerifier
*Tests for A3 Beauty Verifier.*

- `test_passes_simple_action`
  - Test that simple actions pass.
- `test_flags_complex_action`
  - Test that unnecessarily complex actions are flagged.

#### TestA4GuardianVerifier
*Tests for A4 Guardian Verifier.*

- `test_passes_safe_action`
  - Test that safe actions pass.
- `test_fails_harmful_action`
  - Test that harmful actions fail.
- `test_requires_escalation_for_risky_action`
  - Test that risky actions require escalation.

#### TestA5MemoryVerifier
*Tests for A5 Memory Verifier.*

- `test_passes_consented_memory`
  - Test that consented memory operations pass.
- `test_fails_unconsented_semantic_memory`
  - Test that semantic memory without consent fails.

#### TestAxiomComplianceMonitor
*Tests for AxiomComplianceMonitor.*

- `test_verify_with_all_verifiers`
  - Test verification with applicable verifiers.
- `test_verify_passes_clean_event`
  - Test that clean events pass verification.
- `test_verify_fails_violating_event`
  - Test that violating events fail verification.
- `test_violation_tracking`
  - Test that violations are tracked.
- `test_register_custom_verifier`
  - Test registering a custom verifier.
- `test_violation_handler`
  - Test violation handler is triggered.

#### TestVerificationResult
*Tests for VerificationResult.*

- `test_passed_when_all_pass`
  - Test that result passes when all verifiers pass.
- `test_failed_when_any_fails`
  - Test that result fails when any verifier fails.
- `test_violations_property`
  - Test get_violations returns failed results.

## Memory Tests

### tests\memory\test_embedding_service.py

*Tests for the Embedding Service.

Tests local embedding functionality using sentence-transformers.*

#### TestEmbeddingService
*Tests for EmbeddingService class.*

- `test_service_initialization`
  - Test that service initializes correctly with lazy loading.
- `test_embedding_produces_vectors`
  - Verify embeddings are generated correctly.
- `test_embedding_multiple_texts`
  - Test embedding multiple texts at once.
- `test_embedding_single_text`
  - Test embed_single method.
- `test_similar_texts_have_high_similarity`
  - Verify semantic similarity works for similar texts.
- `test_dissimilar_texts_have_low_similarity`
  - Verify dissimilar content is distinguished.
- `test_similarity_with_multiple_candidates`
  - Test similarity against multiple candidates.
- `test_most_similar_returns_top_k`
  - Test most_similar method returns correct number of results.
- `test_most_similar_with_threshold`
  - Test most_similar with threshold filtering.
- `test_is_similar_returns_boolean`
  - Test is_similar method.
- `test_empty_input_handling`
  - Test handling of empty inputs.
- `test_batch_similarity`
  - Test batch similarity matrix.
- `test_get_status`
  - Test status reporting.

#### TestEmbeddingServiceSingleton
*Tests for the singleton pattern.*

- `test_get_embedding_service_returns_same_instance`
  - Test singleton returns same instance.

### tests\memory\test_induction_engine.py

*Tests for the Induction Engine.

Tests user-validated learning and proposal workflow.*

#### TestInductionEngine
*Tests for InductionEngine class.*

- `test_engine_initialization`
  - Test that engine initializes correctly.
- `test_observe_creates_proposal`
  - Test that observation creates a proposal.
- `test_observe_returns_none_for_short_content`
  - Test that short content is rejected.
- `test_proposal_requires_user_approval`
  - Verify memories are not stored without approval.
- `test_accepted_proposal_is_stored`
  - Verify accepted proposals are stored correctly.
- `test_rejected_proposal_not_re_proposed`
  - Verify rejected memories are not proposed again.
- `test_edit_and_accept_proposal`
  - Test editing a proposal before accepting.
- `test_different_observation_types`
  - Test different types of observations.
- `test_get_status`
  - Test status reporting.
- `test_get_status_message`
  - Test human-readable status message.

#### TestInductionEngineSession
*Tests for session management.*

- `test_start_session`
  - Test starting a new session.
- `test_session_tracks_observations`
  - Test that observations are tracked in session.
- `test_end_session_stores_episodic`
  - Test ending session stores episodic memories.
- `test_end_session_clears_observations`
  - Test ending session clears observation list.

#### TestInductionEngineSingleton
*Tests for the singleton pattern.*

- `test_get_induction_engine_returns_instance`
  - Test singleton returns an instance.

### tests\memory\test_memory_store.py

*Tests for the Memory Store.

Tests hybrid storage functionality with ChromaDB and proposal queue.*

#### TestMemoryStore
*Tests for MemoryStore class.*

- `test_store_initialization`
  - Test that store initializes correctly.
- `test_add_and_search_memory`
  - Test adding and searching memories.
- `test_add_memory_to_different_types`
  - Test adding memories to different collections.
- `test_get_memory_by_id`
  - Test retrieving a specific memory.
- `test_delete_memory`
  - Test deleting a memory.
- `test_search_with_threshold`
  - Test search with similarity threshold.
- `test_get_relevant_context`
  - Test getting formatted context.
- `test_status_message`
  - Test status message generation.
- `test_clear_episodic`
  - Test clearing episodic memories.

#### TestMemoryProposalOperations
*Tests for proposal queue operations.*

- `test_add_pending_proposal`
  - Test adding a pending proposal.
- `test_accept_proposal`
  - Test accepting a proposal moves it to semantic.
- `test_accept_proposal_with_edit`
  - Test accepting with edited content.
- `test_reject_proposal`
  - Test rejecting a proposal moves it to rejected.
- `test_is_similar_to_rejected`
  - Test similarity check against rejected proposals.
- `test_proposal_format_for_user`
  - Test proposal formatting for display.

#### TestMemoryStoreSingleton
*Tests for the singleton pattern.*

- `test_get_memory_store_returns_same_instance`
  - Test singleton returns same instance.

## Unit Tests

### tests\unit\test_adapters.py

*Unit Tests for Knowledge Source Adapters

Tests the source adapters including:
- Base adapter functionality
- GitHub adapter
- PyPI adapter
- NPM adapter

Author: Antigravity Agent FactoryVersion: 1.0.0*

#### TestAdapterConfig
*Tests for AdapterConfig dataclass.*

- `test_default_values`
  - Test default configuration values.
- `test_custom_values`
  - Test custom configuration values.

#### TestUpdateSource
*Tests for UpdateSource dataclass.*

- `test_creation`
  - Test creating an update source.
- `test_default_timestamp`
  - Test that timestamp is set automatically.

#### TestKnowledgeChange
*Tests for KnowledgeChange dataclass.*

- `test_creation`
  - Test creating a knowledge change.
- `test_with_values`
  - Test change with old and new values.

#### TestKnowledgeUpdate
*Tests for KnowledgeUpdate dataclass.*

- `test_creation`
  - Test creating a knowledge update.
- `test_checksum_generation`
  - Test that checksum is generated for proposed content.
- `test_to_dict`
  - Test serialization to dictionary.

#### TestUpdatePriority
*Tests for UpdatePriority enum.*

- `test_priority_ordering`
  - Test that priorities are correctly ordered.

#### TestTrustLevel
*Tests for TrustLevel enum.*

- `test_trust_levels`
  - Test trust level values.

#### TestBaseAdapter
*Tests for BaseAdapter abstract class.*

- `test_concrete_implementation`
  - Test that concrete implementation works.
- `test_create_source`
  - Test create_source helper method.
- `test_caching`
  - Test cache methods.
- `test_repr`
  - Test string representation.

#### TestGitHubAdapter
*Tests for GitHub adapter.*

- `test_import`
  - Test that GitHub adapter can be imported.
- `test_tracked_repos`
  - Test that tracked repos are defined.

#### TestPyPIAdapter
*Tests for PyPI adapter.*

- `test_import`
  - Test that PyPI adapter can be imported.
- `test_tracked_packages`
  - Test that tracked packages are defined.

#### TestNPMAdapter
*Tests for NPM adapter.*

- `test_import`
  - Test that NPM adapter can be imported.
- `test_tracked_packages`
  - Test that tracked packages are defined.

### tests\unit\test_adapters_mocked.py

*Comprehensive Unit Tests for Knowledge Source Adapters with HTTP Mocking

This module provides comprehensive mocked tests for all adapters in scripts/adapters/:
- PyPI Adapter (29% coverage target)
- NPM Adapter (31% coverage target)
- GitHub Adapter (35% coverage target)
- Community Adapter (36% coverage target)
- Docs Adapter (37% coverage target)
- Feedback Adapter (26% coverage target)

All HTTP requests are mocked using unittest.mock to avoid external dependencies.

Author: Cursor Agent Factory
Version: 1.0.0*

#### TestPyPIAdapterMocked
*Comprehensive mocked tests for PyPIAdapter.*

- `test_analyze_version_change_major_version`
  - Test version change analysis for major version.
- `test_analyze_version_change_deprecation`
  - Test detection of deprecation notices.
- `test_analyze_version_change_python_requires`
  - Test detection of Python version requirements.
- `test_determine_priority_security`
  - Test priority determination for security changes.
- `test_determine_priority_breaking`
  - Test priority determination for breaking changes.
- `test_is_breaking_version`
  - Test breaking version detection.
- `test_suggest_knowledge_version`
  - Test knowledge version suggestion.
- `test_analyze_version_change_no_version_parts`
  - Test version analysis with invalid version string.
- `test_analyze_version_change_empty_description`
  - Test version analysis with empty description.
- `test_determine_priority_deprecation`
  - Test priority determination for deprecations.
- `test_is_breaking_version_edge_cases`
  - Test breaking version detection edge cases.

#### TestNPMAdapterMocked
*Comprehensive mocked tests for NPMAdapter.*

- `test_analyze_package_version_update`
  - Test package analysis for version updates.
- `test_analyze_package_node_requirement`
  - Test detection of Node.js requirements.
- `test_determine_priority_major_version`
  - Test priority for major version.
- `test_is_major_version`
  - Test major version detection.
- `test_suggest_version`
  - Test version suggestion.

#### TestGitHubAdapterMocked
*Comprehensive mocked tests for GitHubAdapter.*

- `test_parse_release_notes_added`
  - Test parsing release notes for added features.
- `test_parse_release_notes_breaking`
  - Test parsing release notes for breaking changes.
- `test_parse_release_notes_security`
  - Test parsing release notes for security fixes.
- `test_determine_priority_security`
  - Test priority determination for security releases.
- `test_determine_priority_breaking`
  - Test priority determination for breaking releases.
- `test_is_breaking`
  - Test breaking change detection.
- `test_suggest_version`
  - Test version suggestion from release tag.
- `test_parse_release_notes_empty`
  - Test parsing empty release notes.
- `test_parse_release_notes_multiple_patterns`
  - Test parsing release notes with multiple change types.
- `test_determine_priority_major_version_tag`
  - Test priority for major version tag.
- `test_suggest_version_invalid_tag`
  - Test version suggestion with invalid tag.

#### TestDocsAdapterMocked
*Comprehensive mocked tests for DocsAdapter.*

- `test_suggest_version`
  - Test version suggestion.
- `test_suggest_version_edge_cases`
  - Test version suggestion edge cases.

#### TestFeedbackAdapterMocked
*Comprehensive mocked tests for FeedbackAdapter.*

- `test_record_feedback`
  - Test recording feedback.
- `test_analyze_feedback_common_issues`
  - Test feedback analysis for common issues.
- `test_analyze_feedback_suggestions`
  - Test feedback analysis for suggestions.
- `test_patterns_to_changes`
  - Test converting patterns to changes.
- `test_load_feedback_empty_dir`
  - Test loading feedback from empty directory.
- `test_load_feedback_invalid_json`
  - Test loading feedback with invalid JSON.
- `test_load_feedback_missing_fields`
  - Test loading feedback with missing fields.
- `test_analyze_feedback_no_issues`
  - Test feedback analysis with no issues.
- `test_analyze_feedback_below_threshold`
  - Test feedback analysis with issues below threshold.
- `test_analyze_feedback_multiple_knowledge_files`
  - Test feedback analysis with multiple knowledge files.
- `test_patterns_to_changes_empty`
  - Test converting empty patterns to changes.
- `test_patterns_to_changes_unknown_type`
  - Test converting patterns with unknown type.
- `test_record_feedback_creates_file`
  - Test that recording feedback creates a file.
- `test_analyze_feedback_suggestion_threshold`
  - Test that suggestions need at least 2 occurrences.
- `test_record_feedback_overwrites_existing`
  - Test that recording feedback overwrites existing file.

#### TestBaseAdapterCaching
*Tests for BaseAdapter caching functionality.*

- `test_cache_refresh_needed_initially`
  - Test that cache refresh is needed initially.
- `test_cache_set_and_get`
  - Test setting and getting cached data.
- `test_cache_expiration`
  - Test cache expiration after TTL.
- `test_cache_different_keys`
  - Test that different cache keys are independent.
- `test_cache_get_nonexistent`
  - Test getting nonexistent cache key.
- `test_cache_with_custom_ttl`
  - Test cache with custom TTL.

### tests\unit\test_backup_manager.py

*Unit tests for scripts/git/backup_manager.py

Tests backup creation, manifest management, and rollback functionality.*

#### TestBackupEntry
*Tests for BackupEntry dataclass.*

- `test_backup_entry_creation`
  - Test creating a BackupEntry.
- `test_backup_entry_was_new_default`
  - Test BackupEntry default was_new value.

#### TestBackupManifest
*Tests for BackupManifest dataclass.*

- `test_manifest_creation`
  - Test creating a BackupManifest.
- `test_manifest_to_dict`
  - Test converting manifest to dictionary.
- `test_manifest_from_dict`
  - Test creating manifest from dictionary.
- `test_manifest_roundtrip`
  - Test that manifest survives to_dict/from_dict roundtrip.

#### TestBackupSession
*Tests for BackupSession class.*

- `test_session_creation`
  - Test creating a backup session.
- `test_backup_file_existing`
  - Test backing up an existing file.
- `test_backup_file_marked_as_new`
  - Test marking a file as newly created.
- `test_backup_directory`
  - Test backing up a directory.
- `test_rollback_restores_files`
  - Test that rollback restores original file content.
- `test_rollback_deletes_new_files`
  - Test that rollback deletes newly created files.
- `test_complete_marks_session_complete`
  - Test that complete() marks session as completed.

#### TestBackupManager
*Tests for BackupManager class.*

- `test_manager_creation`
  - Test creating a BackupManager.
- `test_create_session`
  - Test creating a backup session.
- `test_list_sessions_empty`
  - Test listing sessions when none exist.
- `test_list_sessions_returns_manifests`
  - Test listing sessions returns manifest objects.
- `test_get_session_by_id`
  - Test retrieving a session by ID.
- `test_get_session_not_found`
  - Test retrieving non-existent session returns None.
- `test_rollback_session`
  - Test rolling back a session by ID.
- `test_rollback_session_not_found`
  - Test rolling back non-existent session fails.
- `test_rollback_already_rolled_back`
  - Test rolling back already rolled back session fails.
- `test_cleanup_old_sessions`
  - Test cleaning up old sessions.
- `test_get_backup_size_empty`
  - Test getting backup size when empty.
- `test_get_backup_size_with_files`
  - Test getting backup size with backed up files.
- `test_format_backup_size`
  - Test formatting backup size.

#### TestEnsureGitignoreExcludesBackup
*Tests for ensure_gitignore_excludes_backup function.*

- `test_creates_gitignore_if_missing`
  - Test that function creates .gitignore if it doesn't exist.
- `test_appends_to_existing_gitignore`
  - Test that function appends to existing .gitignore.
- `test_does_not_duplicate_entry`
  - Test that function doesn't add duplicate entries.

#### TestMainEntry
*Tests for command-line interface.*

- `test_main_list_command`
  - Test main with list command by importing and calling the module code.
- `test_main_size_command`
  - Test backup size calculation.
- `test_format_backup_size_units`
  - Test format_backup_size with various sizes.

### tests\unit\test_conflict_resolver.py

*Unit tests for scripts/git/conflict_resolver.py

Tests conflict detection, resolution strategies, and conflict reporting
for knowledge evolution merges.

Author: Cursor Agent Factory
Version: 1.0.0*

#### TestConflictType
*Tests for ConflictType enum.*

- `test_conflict_type_values`
  - Test that all conflict types have correct values.
- `test_all_conflict_types_present`
  - Test that all expected conflict types exist.

#### TestResolutionStrategy
*Tests for ResolutionStrategy enum.*

- `test_resolution_strategy_values`
  - Test that all resolution strategies have correct values.
- `test_all_strategies_present`
  - Test that all expected strategies exist.

#### TestConflict
*Tests for Conflict dataclass.*

- `test_conflict_creation`
  - Test creating a Conflict with all fields.
- `test_conflict_defaults`
  - Test Conflict with default values.
- `test_conflict_to_dict`
  - Test converting Conflict to dictionary.
- `test_conflict_to_dict_truncates_long_values`
  - Test that to_dict truncates long values.

#### TestConflictReport
*Tests for ConflictReport dataclass.*

- `test_conflict_report_creation`
  - Test creating a ConflictReport.
- `test_conflict_report_with_conflicts`
  - Test ConflictReport with conflicts.
- `test_has_conflicts_property`
  - Test has_conflicts property.
- `test_has_unresolved_property`
  - Test has_unresolved property.
- `test_to_markdown_no_conflicts`
  - Test markdown generation with no conflicts.
- `test_to_markdown_with_conflicts`
  - Test markdown generation with conflicts.

#### TestConflictResolverInitialization
*Tests for ConflictResolver initialization.*

- `test_default_initialization`
  - Test ConflictResolver with default parameters.
- `test_custom_initialization`
  - Test ConflictResolver with custom parameters.
- `test_user_customization_paths`
  - Test that USER_CUSTOMIZATION_PATHS is defined.
- `test_always_update_paths`
  - Test that ALWAYS_UPDATE_PATHS is defined.

#### TestConflictDetection
*Tests for conflict detection logic.*

- `test_no_conflict_same_values`
  - Test that identical values produce no conflicts.
- `test_simple_value_difference`
  - Test detection of simple value differences.
- `test_type_mismatch`
  - Test detection of type mismatches.
- `test_nested_dict_conflicts`
  - Test detection of conflicts in nested dictionaries.
- `test_new_keys_no_conflict`
  - Test that new keys don't create conflicts.
- `test_removed_keys_create_conflict`
  - Test that removed keys create conflicts.
- `test_list_differences`
  - Test detection of list differences.
- `test_list_same_content_no_conflict`
  - Test that lists with same content (different order) don't conflict.
- `test_metadata_paths_no_conflict_on_removal`
  - Test that metadata path removals create conflicts (but can be auto-resolved).
- `test_complex_nested_structure`
  - Test conflict detection in complex nested structures.

#### TestConflictResolutionStrategies
*Tests for resolution strategy suggestions.*

- `test_version_path_uses_incoming`
  - Test that version paths suggest USE_INCOMING.
- `test_metadata_paths_use_incoming`
  - Test that metadata paths suggest USE_INCOMING.
- `test_user_customization_paths_keep_existing`
  - Test that user customization paths suggest KEEP_EXISTING.
- `test_user_customization_disabled`
  - Test that disabling preserve_user_changes changes suggestion.
- `test_type_mismatch_requires_user_decision`
  - Test that type mismatches require user decision.

#### TestAutoResolution
*Tests for automatic conflict resolution.*

- `test_auto_resolve_metadata`
  - Test that metadata conflicts are auto-resolved.
- `test_auto_resolve_user_customization_preservation`
  - Test that user customization preservation is auto-resolved.
- `test_no_auto_resolve_when_disabled`
  - Test that auto-resolution is disabled when flag is False.
- `test_user_decision_not_auto_resolved`
  - Test that USER_DECISION conflicts are never auto-resolved.

#### TestConflictResolution
*Tests for resolving conflicts and producing merged content.*

- `test_resolve_no_conflicts`
  - Test resolution with no conflicts.
- `test_resolve_keep_existing`
  - Test resolution with KEEP_EXISTING strategy.
- `test_resolve_use_incoming`
  - Test resolution with USE_INCOMING strategy.
- `test_resolve_merge_values_lists`
  - Test resolution with MERGE_VALUES strategy for lists.
- `test_resolve_merge_values_dicts`
  - Test resolution with MERGE_VALUES strategy for dicts.
- `test_resolve_skip`
  - Test resolution with SKIP strategy.
- `test_resolve_user_decision_without_input`
  - Test that USER_DECISION without user input keeps existing.
- `test_resolve_nested_conflicts`
  - Test resolution of nested conflicts.
- `test_resolve_preserves_unrelated_data`
  - Test that resolution preserves unrelated data.
- `test_resolve_does_not_modify_original`
  - Test that resolution doesn't modify original dictionaries.

#### TestHelperMethods
*Tests for helper methods.*

- `test_is_metadata_path`
  - Test _is_metadata_path helper.
- `test_is_user_customization_path`
  - Test _is_user_customization_path helper.
- `test_find_conflict`
  - Test _find_conflict helper.
- `test_merge_values_lists`
  - Test _merge_values for lists.
- `test_merge_values_dicts`
  - Test _merge_values for dictionaries.
- `test_merge_values_other_types`
  - Test _merge_values for non-list/dict types defaults to incoming.

#### TestEdgeCases
*Tests for edge cases and error handling.*

- `test_empty_dicts`
  - Test conflict detection with empty dictionaries.
- `test_empty_vs_populated`
  - Test conflict detection with empty vs populated dict.
- `test_populated_vs_empty`
  - Test conflict detection with populated vs empty dict.
- `test_empty_lists`
  - Test conflict detection with empty lists.
- `test_none_values`
  - Test conflict detection with None values.
- `test_boolean_values`
  - Test conflict detection with boolean values.
- `test_numeric_types`
  - Test conflict detection with different numeric types.
- `test_numeric_types_different_values`
  - Test conflict detection with different numeric types and values.
- `test_very_deep_nesting`
  - Test conflict detection with very deep nesting.
- `test_large_lists`
  - Test conflict detection with large lists.
- `test_special_characters_in_paths`
  - Test conflict detection with special characters in keys.
- `test_list_with_duplicates`
  - Test conflict detection with lists containing duplicates.
- `test_dict_to_list_type_change`
  - Test conflict detection when dict changes to list.
- `test_list_to_dict_type_change`
  - Test conflict detection when list changes to dict.
- `test_string_to_number_type_change`
  - Test conflict detection when string changes to number.
- `test_multiple_conflicts_same_level`
  - Test detection of multiple conflicts at the same level.
- `test_nested_list_conflicts`
  - Test conflict detection with nested lists.
- `test_empty_string_vs_none`
  - Test conflict detection between empty string and None.
- `test_zero_vs_false`
  - Test that 0 and False are considered equal (Python semantics).
- `test_one_vs_true`
  - Test that 1 and True are considered equal (Python semantics).

#### TestConflictResolutionAdvanced
*Advanced tests for conflict resolution.*

- `test_resolve_multiple_conflicts_mixed_strategies`
  - Test resolving multiple conflicts with different strategies.
- `test_resolve_with_partial_user_decisions`
  - Test resolution when only some conflicts have user decisions.
- `test_resolve_merge_nested_dicts`
  - Test merging nested dictionaries.
- `test_resolve_list_merge_preserves_order`
  - Test that list merging preserves order from existing.
- `test_resolve_empty_list_merge`
  - Test merging when existing list is empty.
- `test_resolve_empty_dict_merge`
  - Test merging when existing dict is empty.
- `test_resolve_with_no_conflicts_applies_all_changes`
  - Test that resolution applies all changes when no conflicts.
- `test_resolve_skips_removed_keys`
  - Test that SKIP strategy skips removed keys.

#### TestConflictReportAdvanced
*Advanced tests for ConflictReport.*

- `test_report_timestamp_is_datetime`
  - Test that timestamp is a datetime object.
- `test_report_categorization`
  - Test that conflicts are properly categorized.
- `test_markdown_with_long_values`
  - Test markdown generation with long values.
- `test_markdown_empty_auto_resolved`
  - Test markdown when auto_resolved is empty.
- `test_markdown_empty_requires_user`
  - Test markdown when requires_user is empty.

#### TestPathHelpers
*Tests for path helper methods.*

- `test_is_metadata_path_variations`
  - Test _is_metadata_path with various path formats.
- `test_is_user_customization_path_variations`
  - Test _is_user_customization_path with various formats.
- `test_suggest_for_path_edge_cases`
  - Test _suggest_for_path with edge cases.

#### TestIntegrationScenarios
*Integration tests for real-world scenarios.*

- `test_knowledge_file_update_scenario`
  - Test a realistic knowledge file update scenario.
- `test_complex_merge_scenario`
  - Test a complex merge scenario with multiple conflict types.

### tests\unit\test_dependency_validator.py

*Unit tests for DependencyValidator and related classes.

Tests cover:
- EdgeType and NodeType enums
- DependencyNode, DependencyEdge, ValidationResult dataclasses
- DependencyValidator class with all methods
- File system mocking using tmp_path fixture
- Graph operations (cycles, broken refs, impact analysis, etc.)*

#### TestEdgeType
*Tests for EdgeType enum.*

- `test_edge_type_values`
  - Test EdgeType enum values.
- `test_edge_type_enumeration`
  - Test that all edge types are present.

#### TestNodeType
*Tests for NodeType enum.*

- `test_node_type_values`
  - Test NodeType enum values.
- `test_node_type_enumeration`
  - Test that all node types are present.

#### TestDependencyNode
*Tests for DependencyNode dataclass.*

- `test_minimal_node`
  - Test creating a minimal DependencyNode.
- `test_full_node`
  - Test creating a DependencyNode with all fields.
- `test_node_metadata_isolation`
  - Test that metadata dicts are isolated between instances.

#### TestDependencyEdge
*Tests for DependencyEdge dataclass.*

- `test_minimal_edge`
  - Test creating a minimal DependencyEdge.
- `test_edge_with_version_constraint`
  - Test creating an edge with version constraint.
- `test_edge_hash`
  - Test that edges are hashable.
- `test_edge_equality`
  - Test edge equality comparison.

Note: The __eq__ implementation has a bug where it checks
self.from_node == self.to_node == other.to_node instead of
properly comparing both from_node and to_node. This test reflects
the actual (buggy) behavior.

#### TestValidationResult
*Tests for ValidationResult dataclass.*

- `test_empty_result`
  - Test creating an empty ValidationResult.
- `test_result_with_cycles`
  - Test ValidationResult with cycles.
- `test_result_with_broken_refs`
  - Test ValidationResult with broken references.
- `test_result_with_warnings`
  - Test ValidationResult with warnings.
- `test_result_with_version_errors`
  - Test ValidationResult with version errors.
- `test_result_is_valid_property`
  - Test is_valid property logic.
- `test_result_has_warnings_property`
  - Test has_warnings property logic.

#### TestDependencyValidatorInit
*Tests for DependencyValidator initialization.*

- `test_init`
  - Test DependencyValidator initialization.

#### TestDependencyValidatorScanKnowledge
*Tests for _scan_knowledge_files method.*

- `test_scan_knowledge_no_manifest`
  - Test scanning when manifest.json doesn't exist.
- `test_scan_knowledge_empty_manifest`
  - Test scanning with empty manifest.
- `test_scan_knowledge_simple_dependencies`
  - Test scanning knowledge files with simple dependencies.
- `test_scan_knowledge_complex_dependencies`
  - Test scanning knowledge files with complex dependencies.
- `test_scan_knowledge_dependencies_with_filename_key`
  - Test scanning knowledge files with 'filename' key in dependencies.
- `test_scan_knowledge_invalid_json`
  - Test scanning with invalid JSON manifest.

#### TestDependencyValidatorScanSkills
*Tests for _scan_skills method.*

- `test_scan_skills_no_directory`
  - Test scanning when skills directory doesn't exist.
- `test_scan_skills_without_frontmatter`
  - Test scanning skills without YAML frontmatter.
- `test_scan_skills_with_frontmatter`
  - Test scanning skills with YAML frontmatter.
- `test_scan_skills_knowledge_with_json_extension`
  - Test scanning skills with knowledge dependencies that already have .json extension.
- `test_scan_skills_nested_directory`
  - Test scanning nested skill directories (e.g., pm/).
- `test_scan_skills_duplicate_prevention`
  - Test that duplicate skills are not registered.

#### TestDependencyValidatorScanAgents
*Tests for _scan_agents method.*

- `test_scan_agents_no_directory`
  - Test scanning when agents directory doesn't exist.
- `test_scan_agents_without_frontmatter`
  - Test scanning agents without frontmatter (should skip).
- `test_scan_agents_with_frontmatter`
  - Test scanning agents with frontmatter.
- `test_scan_agents_knowledge_with_json_extension`
  - Test scanning agents with knowledge dependencies that already have .json extension.

#### TestDependencyValidatorScanBlueprints
*Tests for _scan_blueprints method.*

- `test_scan_blueprints_no_directory`
  - Test scanning when blueprints directory doesn't exist.
- `test_scan_blueprints_valid`
  - Test scanning valid blueprints.
- `test_scan_blueprints_no_pattern_id`
  - Test scanning blueprints with missing patternId.
- `test_scan_blueprints_no_filename`
  - Test scanning blueprints with missing filename.
- `test_scan_blueprints_no_json_file`
  - Test scanning blueprint directory without blueprint.json.
- `test_scan_blueprints_invalid_json`
  - Test scanning with invalid JSON blueprint.
- `test_scan_blueprints_uses_directory_name`
  - Test that blueprint uses directory name when blueprintId is missing.

#### TestDependencyValidatorParseFrontmatter
*Tests for _parse_frontmatter method.*

- `test_parse_frontmatter_valid`
  - Test parsing valid YAML frontmatter.
- `test_parse_frontmatter_no_frontmatter`
  - Test parsing file without frontmatter.
- `test_parse_frontmatter_invalid_yaml`
  - Test parsing file with invalid YAML.
- `test_parse_frontmatter_nonexistent_file`
  - Test parsing nonexistent file.

#### TestDependencyValidatorBuildAdjacency
*Tests for _build_adjacency method.*

- `test_build_adjacency`
  - Test building adjacency lists.

#### TestDependencyValidatorDetectCycles
*Tests for detect_cycles method.*

- `test_detect_cycles_none`
  - Test cycle detection with no cycles.
- `test_detect_cycles_simple_cycle`
  - Test detecting a simple cycle.
- `test_detect_cycles_ignores_references`
  - Test that REFERENCES edges don't create cycles.
- `test_detect_cycles_three_node_cycle`
  - Test detecting a cycle with three nodes.
- `test_detect_cycles_with_extends`
  - Test that EXTENDS edges create cycles.

#### TestDependencyValidatorFindBrokenRefs
*Tests for find_broken_refs method.*

- `test_find_broken_refs_none`
  - Test finding broken refs when none exist.
- `test_find_broken_refs_exists`
  - Test finding broken references.
- `test_find_broken_refs_ignores_references`
  - Test that REFERENCES edges don't create broken refs.

#### TestDependencyValidatorFindMissingRefs
*Tests for find_missing_refs method.*

- `test_find_missing_refs_none`
  - Test finding missing refs when none exist.
- `test_find_missing_refs_exists`
  - Test finding missing references (warnings).
- `test_find_missing_refs_ignores_requires`
  - Test that REQUIRES edges don't create missing ref warnings.

#### TestDependencyValidatorValidateVersions
*Tests for validate_versions method.*

- `test_validate_versions_no_packaging`
  - Test version validation when packaging is not available.
- `test_validate_versions_valid`
  - Test version validation with valid versions.
- `test_validate_versions_invalid`
  - Test version validation with invalid versions.
- `test_validate_versions_no_constraint`
  - Test version validation with no constraint.
- `test_validate_versions_no_target_version`
  - Test version validation when target node has no version.
- `test_validate_versions_invalid_specifier`
  - Test version validation with invalid version specifier.

#### TestDependencyValidatorValidate
*Tests for validate method.*

- `test_validate_valid_graph`
  - Test validation of a valid graph.
- `test_validate_with_cycles`
  - Test validation with cycles.
- `test_validate_with_broken_refs`
  - Test validation with broken references.
- `test_validate_with_all_issues`
  - Test validation with cycles, broken refs, and warnings.
- `test_validate_calls_all_methods`
  - Test that validate() calls all validation methods.

#### TestDependencyValidatorReverseLookup
*Tests for reverse_lookup method.*

- `test_reverse_lookup`
  - Test reverse lookup of dependents.
- `test_reverse_lookup_no_dependents`
  - Test reverse lookup with no dependents.

#### TestDependencyValidatorImpactAnalysis
*Tests for impact_analysis method.*

- `test_impact_analysis_direct`
  - Test impact analysis for direct dependents.
- `test_impact_analysis_transitive`
  - Test impact analysis for transitive dependents.
- `test_impact_analysis_no_dependents`
  - Test impact analysis with no dependents.
- `test_impact_analysis_multiple_levels`
  - Test impact analysis with multiple dependency levels.

#### TestDependencyValidatorGetInstallOrder
*Tests for get_install_order method.*

- `test_get_install_order`
  - Test getting installation order.
- `test_get_install_order_with_cycle`
  - Test getting installation order with cycle raises error.

#### TestDependencyValidatorGetStatistics
*Tests for get_statistics method.*

- `test_get_statistics`
  - Test getting graph statistics.
- `test_get_statistics_empty_graph`
  - Test getting statistics for empty graph.
- `test_get_statistics_all_node_types`
  - Test statistics with all node types.
- `test_get_statistics_all_edge_types`
  - Test statistics with all edge types.

#### TestDependencyValidatorExportGraph
*Tests for export_graph method.*

- `test_export_graph`
  - Test exporting graph to JSON.
- `test_export_graph_with_none_values`
  - Test exporting graph with None values.
- `test_export_graph_path_conversion`
  - Test that Path objects are converted to strings in export.

#### TestDependencyValidatorScanArtifacts
*Tests for scan_artifacts method.*

- `test_scan_artifacts_full`
  - Test scanning all artifacts.
- `test_scan_artifacts_builds_adjacency`
  - Test that scan_artifacts builds adjacency lists.

### tests\unit\test_factory_cli.py

*Unit tests for cli/factory_cli.py

Tests the CLI interface for the Antigravity Agent Factory.*

#### TestGetFactoryRoot
*Tests for get_factory_root function.*

- `test_returns_path`
  - Test that get_factory_root returns a Path.
- `test_path_exists`
  - Test that returned path exists.
- `test_contains_blueprints`
  - Test that factory root contains blueprints directory.

#### TestDisplayWelcome
*Tests for display_welcome function.*

- `test_prints_welcome_message`
  - Test that welcome message is printed.

#### TestDisplayTour
*Tests for display_tour function.*

- `test_prints_tour_info`
  - Test that tour information is printed.

#### TestDisplayErrorWithHelp
*Tests for display_error_with_help function.*

- `test_prints_error_and_suggestion`
  - Test that error and suggestion are printed.

#### TestListBlueprints
*Tests for list_blueprints function.*

- `test_lists_available_blueprints`
  - Test that blueprints are listed.
- `test_shows_blueprint_details`
  - Test that blueprint details are shown.

#### TestListPatterns
*Tests for list_patterns function.*

- `test_lists_available_patterns`
  - Test that patterns are listed.
- `test_shows_pattern_categories`
  - Test that pattern categories are shown.

#### TestRunQuickstart
*Tests for run_quickstart function.*

- `test_quickstart_with_default_output`
  - Test quickstart with default output directory.
- `test_quickstart_with_custom_blueprint`
  - Test quickstart with custom blueprint.
- `test_quickstart_handles_generation_failure`
  - Test quickstart handles generation failure.
- `test_quickstart_handles_exception`
  - Test quickstart handles exceptions.

#### TestInteractiveMode
*Tests for interactive_mode function.*

- `test_interactive_mode_basic_flow`
  - Test basic interactive mode flow.
- `test_interactive_mode_cancel`
  - Test cancelling interactive mode.
- `test_interactive_mode_with_pm_enabled`
  - Test interactive mode with PM system enabled.

#### TestGenerateFromBlueprint
*Tests for generate_from_blueprint function.*

- `test_generate_from_valid_blueprint`
  - Test generating from a valid blueprint.
- `test_generate_from_invalid_blueprint`
  - Test generating from non-existent blueprint.
- `test_generate_with_project_name`
  - Test generating with custom project name.
- `test_generate_with_pm_enabled`
  - Test generating with PM system enabled.

#### TestGenerateFromConfigFile
*Tests for generate_from_config_file function.*

- `test_generate_from_json_config`
  - Test generating from JSON config file.
- `test_generate_from_nonexistent_config`
  - Test generating from non-existent config file.

#### TestAnalyzeRepository
*Tests for analyze_repository function.*

- `test_analyze_valid_repository`
  - Test analyzing a valid repository.
- `test_analyze_with_artifacts`
  - Test analyzing repository with existing artifacts.

#### TestOnboardRepository
*Tests for onboard_repository function.*

- `test_onboard_fresh_repository`
  - Test onboarding a fresh repository.
- `test_onboard_with_blueprint`
  - Test onboarding with specific blueprint.
- `test_onboard_dry_run`
  - Test onboarding in dry run mode.

#### TestRollbackSession
*Tests for rollback_session function.*

- `test_rollback_no_sessions`
  - Test rollback when no sessions exist.
- `test_rollback_with_sessions_quit`
  - Test rollback session list and quit.

#### TestCreateDefaultConfig
*Tests for _create_default_config function.*

- `test_creates_config_from_inventory`
  - Test creating config from inventory.

#### TestInteractiveConflictResolver
*Tests for _interactive_conflict_resolver function.*

- `test_resolver_returns_recommendation_on_empty_input`
  - Test resolver returns recommendation on empty input.
- `test_resolver_returns_selected_option`
  - Test resolver returns selected option.

#### TestMain
*Tests for main function.*

- `test_main_no_args_shows_help`
  - Test main with no arguments shows help.
- `test_main_list_blueprints`
  - Test main with --list-blueprints.
- `test_main_list_patterns`
  - Test main with --list-patterns.
- `test_main_analyze`
  - Test main with --analyze.
- `test_main_quickstart`
  - Test main with --quickstart.
- `test_main_blueprint_without_output_fails`
  - Test main with --blueprint but no --output fails.
- `test_main_blueprint_with_output`
  - Test main with --blueprint and --output.
- `test_main_version`
  - Test main with --version.

### tests\unit\test_gap_types.py

*Unit tests for gap types and enums in scripts/analysis/knowledge_gap_analyzer.py

Tests for GapType and GapPriority enumerations.*

#### TestGapType
*Tests for GapType enumeration.*

- `test_all_gap_types_defined`
  - Test that all expected gap types are defined.
- `test_gap_type_values`
  - Test gap type string values.
- `test_gap_type_from_value`
  - Test creating GapType from value.
- `test_gap_type_invalid_value`
  - Test that invalid value raises error.
- `test_gap_type_iteration`
  - Test iterating over all gap types.

#### TestGapPriority
*Tests for GapPriority enumeration.*

- `test_all_priorities_defined`
  - Test that all expected priorities are defined.
- `test_priority_values`
  - Test priority numeric values.
- `test_priority_ordering`
  - Test that priorities can be compared.
- `test_priority_sorting`
  - Test sorting priorities by value.
- `test_priority_from_value`
  - Test creating GapPriority from value.

### tests\unit\test_guardian_axiom_checker.py

*Unit tests for the Guardian Axiom Checker.

These tests verify that the axiom checker correctly identifies
potentially harmful operations according to the core axioms.*

#### TestCheckCommand
*Tests for shell command checking.*

- `test_level_4_critical_commands`
  - Critical commands should trigger Level 4 (Protect).
- `test_sensitive_file_access`
  - Access to sensitive files should trigger pause.
- `test_safe_commands`
  - Safe commands should pass without intervention.

#### TestCheckFileOperation
*Tests for file operation checking.*

- `test_critical_path_deletion`
  - Deletion of critical system paths should be blocked.
- `test_sensitive_file_deletion`
  - Deletion of sensitive files should require confirmation.
- `test_normal_file_operations`
  - Normal file operations should pass.

#### TestCheckContentForClaims
*Tests for content claim checking (A1 - Verifiability).*

- `test_claim_detection`
  - Claims should be detected for verification.

#### TestValidateOperation
*Tests for the main validation entry point.*

- `test_command_validation`
  - Command validation should work through main entry point.
- `test_file_write_validation`
  - File write validation should work through main entry point.
- `test_file_delete_validation`
  - File delete validation should work through main entry point.
- `test_content_validation`
  - Content validation should work through main entry point.

#### TestCheckResultProperties
*Tests for CheckResult helper properties.*

- `test_requires_user_level_0`
  - Level 0 should not require user.
- `test_requires_user_level_2`
  - Level 2+ should require user.
- `test_is_emergency_level_3`
  - Level 3 should not be emergency.
- `test_is_emergency_level_4`
  - Level 4 should be emergency.

#### TestAxiomCoverage
*Tests to ensure all axioms are being checked.*

- `test_a1_verifiability_checked`
  - A1 (Verifiability) should be checked in content.
- `test_a4_non_harm_checked`
  - A4 (Non-Harm) should be checked in commands.
- `test_a4_non_harm_in_files`
  - A4 (Non-Harm) should be checked in file operations.

### tests\unit\test_guardian_secret_scanner.py

*Unit tests for the Guardian Secret Scanner.

These tests verify that the secret scanner correctly identifies
credentials and secrets in content to prevent accidental exposure.*

#### TestScanContent
*Tests for content scanning.*

- `test_high_severity_api_keys`
  - High severity API keys should be detected.
- `test_private_keys`
  - Private keys should be detected as high severity.
- `test_database_connection_strings`
  - Database connection strings should be detected.
- `test_medium_severity_patterns`
  - Medium severity patterns should be detected.
- `test_false_positives_filtered`
  - Placeholder values should not be detected as secrets.
- `test_multiline_content`
  - Scanner should handle multiline content correctly.

#### TestRedactSecret
*Tests for secret redaction.*

- `test_short_secret`
  - Short secrets should be fully redacted.
- `test_long_secret`
  - Long secrets should show first and last 4 chars.

#### TestIsFalsePositive
*Tests for false positive detection.*

- `test_false_positive_patterns`
  - False positive patterns should be correctly identified.

#### TestScanDiff
*Tests for git diff scanning.*

- `test_only_added_lines_checked`
  - Only added lines (starting with +) should be checked.
- `test_removed_lines_ignored`
  - Removed lines (starting with -) should not be checked.

#### TestGetSeverityLevel
*Tests for severity to Guardian level mapping.*

- `test_no_matches`
  - No matches should return Level 0.
- `test_high_severity`
  - High severity should return Level 4.
- `test_medium_severity`
  - Medium severity should return Level 3.
- `test_low_severity`
  - Low severity should return Level 2.
- `test_mixed_severity`
  - Mixed severity should return highest level.

#### TestScanFile
*Tests for file scanning.*

- `test_scan_nonexistent_file`
  - Scanning nonexistent file should return empty list.
- `test_skip_binary_files`
  - Binary files should be skipped.

### tests\unit\test_install_hooks.py

*Unit tests for scripts/git/install_hooks.py

Tests the Git hook installation functionality.*

#### TestPreCommitHookContent
*Tests for the pre-commit hook content.*

- `test_unix_hook_has_shebang`
  - Test that Unix hook starts with shebang.
- `test_windows_hook_has_shebang`
  - Test that Windows hook starts with shebang.
- `test_unix_hook_runs_version_sync`
  - Test that Unix hook syncs versions.

Note: validate_readme_structure.py was removed from the hook for speed.
The hook now focuses on: secrets, JSON syntax, version sync.
- `test_windows_hook_runs_version_sync`
  - Test that Windows hook syncs versions.

Note: validate_readme_structure.py was removed from the hook for speed.
The hook now focuses on: secrets, JSON syntax, version sync.
- `test_unix_hook_stages_readme`
  - Test that Unix hook stages README.md.
- `test_windows_hook_stages_readme`
  - Test that Windows hook stages README.md.
- `test_unix_hook_exits_cleanly`
  - Test that Unix hook exits with 0.
- `test_windows_hook_checks_multiple_python_paths`
  - Test that Windows hook tries multiple Python paths.

#### TestInstallHooks
*Tests for the install_hooks function.*

- `test_install_hooks_no_git_directory`
  - Test that install_hooks fails gracefully without .git directory.
- `test_install_hooks_creates_hook_file`
  - Test that install_hooks creates the pre-commit hook.
- `test_install_hooks_asks_before_overwrite`
  - Test that install_hooks asks before overwriting existing hook.
- `test_install_hooks_overwrites_when_confirmed`
  - Test that install_hooks overwrites when user confirms.
- `test_install_hooks_makes_executable_on_unix`
  - Test that install_hooks makes hook executable on Unix.

#### TestMainEntry
*Tests for the main entry point.*

- `test_main_calls_install_hooks`
  - Test that __main__ calls install_hooks.

### tests\unit\test_knowledge_gap_analyzer.py

*Unit tests for scripts/analysis/knowledge_gap_analyzer.py

Tests for CoverageScore, KnowledgeGap, AnalysisResult, and KnowledgeGapAnalyzer.*

#### TestCoverageScore
*Tests for CoverageScore dataclass.*

- `test_create_coverage_score`
  - Test creating a basic CoverageScore.
- `test_coverage_ratio_calculation`
  - Test coverage_ratio property calculation.
- `test_coverage_ratio_capped_at_one`
  - Test coverage_ratio doesn't exceed 1.0.
- `test_is_adequate_true`
  - Test is_adequate when coverage meets requirement.
- `test_is_adequate_false`
  - Test is_adequate when coverage below requirement.
- `test_is_adequate_exact_match`
  - Test is_adequate when coverage exactly meets requirement.
- `test_zero_required_depth`
  - Test coverage_ratio with zero required depth.

#### TestKnowledgeGap
*Tests for KnowledgeGap dataclass.*

- `test_create_gap`
  - Test creating a KnowledgeGap.
- `test_to_dict_serialization`
  - Test to_dict produces serializable output.
- `test_gap_with_related_files`
  - Test gap with related files.

#### TestAnalysisResult
*Tests for AnalysisResult dataclass.*

- `test_coverage_percentage`
  - Test coverage_percentage calculation.
- `test_coverage_percentage_zero_topics`
  - Test coverage_percentage with zero topics.
- `test_gaps_by_priority`
  - Test gaps_by_priority grouping.
- `test_gaps_by_type`
  - Test gaps_by_type grouping.
- `test_get_top_gaps`
  - Test get_top_gaps returns highest priority first.
- `test_to_dict`
  - Test to_dict produces complete serializable output.

#### TestKnowledgeGapAnalyzer
*Tests for KnowledgeGapAnalyzer class.*

- `test_init`
  - Test analyzer initialization.
- `test_analyze_returns_result`
  - Test analyze returns AnalysisResult.
- `test_load_knowledge_files`
  - Test loading knowledge files into cache.
- `test_load_knowledge_files_skips_invalid`
  - Test that invalid JSON files are skipped.
- `test_flatten_content_string`
  - Test flattening string content.
- `test_flatten_content_dict`
  - Test flattening dictionary content.
- `test_flatten_content_list`
  - Test flattening list content.
- `test_determine_depth_no_mentions`
  - Test depth determination with no mentions.
- `test_determine_depth_basic_mention`
  - Test depth determination with basic mentions.
- `test_determine_depth_with_examples`
  - Test depth determination with examples.
- `test_determine_depth_comprehensive`
  - Test depth determination with all criteria.
- `test_get_extension_candidates`
  - Test getting extension candidates.
- `test_save_report`
  - Test saving analysis report.

#### TestRunGapAnalysis
*Tests for run_gap_analysis convenience function.*

- `test_run_with_defaults`
  - Test running gap analysis with defaults.
- `test_run_with_custom_taxonomy`
  - Test running gap analysis with custom taxonomy.

### tests\unit\test_pattern_loading.py

*Unit tests for pattern and blueprint loading functionality.

Tests cover:
- Loading all existing blueprints
- Loading all existing agent patterns
- Loading all existing skill patterns
- Pattern structure validation*

#### TestBlueprintFiles
*Tests for blueprint file loading.*

- `test_all_blueprints_are_valid_json`
  - Test that all blueprint.json files are valid JSON.
- `test_blueprints_have_required_fields`
  - Test that blueprints have required metadata and stack fields.
- `test_python_fastapi_blueprint_exists`
  - Test that python-fastapi blueprint exists and is valid.

#### TestAgentPatternFiles
*Tests for agent pattern file loading.*

- `test_all_agent_patterns_are_valid_json`
  - Test that all agent pattern files are valid JSON.
- `test_agent_patterns_have_required_fields`
  - Test that agent patterns (not schema files) have required structure.
- `test_code_reviewer_pattern_exists`
  - Test that code-reviewer pattern exists and is valid.

#### TestSkillPatternFiles
*Tests for skill pattern file loading.*

- `test_all_skill_patterns_are_valid_json`
  - Test that all skill pattern files are valid JSON.
- `test_skill_patterns_have_required_fields`
  - Test that skill patterns (not schema files) have required structure.
- `test_bugfix_workflow_pattern_exists`
  - Test that bugfix-workflow pattern exists and is valid.

#### TestKnowledgeFiles
*Tests for knowledge file loading.*

- `test_all_knowledge_files_are_valid_json`
  - Test that all knowledge files are valid JSON.
- `test_skill_catalog_exists`
  - Test that skill-catalog.json exists and has skills.

#### TestPatternConsistency
*Tests for pattern consistency across the factory.*

- `test_blueprint_agent_references_exist`
  - Test that agents referenced in blueprints have corresponding patterns.
- `test_blueprint_skill_references_exist`
  - Test that skills referenced in blueprints exist in patterns or skill catalog.

Some skills are stack-specific and implemented in external repos,
so we also check the skill catalog for known skills.

### tests\unit\test_pm_adapters.py

*Unit tests for PM adapter JSON files.

Tests cover:
- Adapter interface structure validation
- Adapter-specific mappings (GitHub, Jira, Azure DevOps, Linear)
- Cross-adapter consistency checks*

#### TestAdapterInterface
*Tests for adapter-interface.json structure.*

- `test_interface_file_exists`
  - Test that adapter-interface.json exists.
- `test_interface_is_valid_json`
  - Test that adapter-interface.json is valid JSON.
- `test_interface_defines_work_item_operations`
  - Test that interface defines work item operations.
- `test_interface_defines_planning_operations`
  - Test that interface defines planning operations.
- `test_interface_defines_board_operations`
  - Test that interface defines board operations.
- `test_interface_defines_metrics_operations`
  - Test that interface defines metrics operations.
- `test_interface_defines_documentation_operations`
  - Test that interface defines documentation operations.

#### TestGitHubAdapter
*Tests for github-adapter.json mappings.*

- `test_github_adapter_exists`
  - Test that github-adapter.json exists.
- `test_github_adapter_is_valid_json`
  - Test that github-adapter.json is valid JSON.
- `test_github_epic_mapping`
  - Test GitHub epic mapping (Epic → Issue with label).
- `test_github_story_mapping`
  - Test GitHub story mapping.
- `test_github_sprint_mapping`
  - Test GitHub sprint mapping (Sprint → Milestone).
- `test_github_board_mapping`
  - Test GitHub board mapping (Board → Project v2).

#### TestJiraAdapter
*Tests for jira-adapter.json mappings.*

- `test_jira_adapter_exists`
  - Test that jira-adapter.json exists.
- `test_jira_adapter_is_valid_json`
  - Test that jira-adapter.json is valid JSON.
- `test_jira_epic_mapping`
  - Test Jira epic mapping.
- `test_jira_story_mapping`
  - Test Jira story mapping.
- `test_jira_sprint_mapping`
  - Test Jira sprint mapping.
- `test_jira_has_jql_patterns`
  - Test that Jira adapter has JQL patterns.

#### TestAzureDevOpsAdapter
*Tests for azure-devops-adapter.json mappings.*

- `test_azure_adapter_exists`
  - Test that azure-devops-adapter.json exists.
- `test_azure_adapter_is_valid_json`
  - Test that azure-devops-adapter.json is valid JSON.
- `test_azure_epic_mapping`
  - Test Azure DevOps epic mapping.
- `test_azure_sprint_mapping`
  - Test Azure DevOps sprint mapping (Sprint → Iteration).
- `test_azure_has_wiql_patterns`
  - Test that Azure DevOps adapter has WIQL patterns.

#### TestLinearAdapter
*Tests for linear-adapter.json mappings.*

- `test_linear_adapter_exists`
  - Test that linear-adapter.json exists.
- `test_linear_adapter_is_valid_json`
  - Test that linear-adapter.json is valid JSON.
- `test_linear_epic_mapping`
  - Test Linear epic mapping (Epic → Project).
- `test_linear_sprint_mapping`
  - Test Linear sprint mapping (Sprint → Cycle).

#### TestAdapterConsistency
*Cross-adapter consistency tests.*

- `test_all_adapters_implement_create_epic`
  - Test that all adapters implement createEpic operation.
- `test_all_adapters_implement_create_story`
  - Test that all adapters implement createStory operation.
- `test_all_adapters_implement_create_sprint`
  - Test that all adapters implement createSprint operation.

### tests\unit\test_pm_config.py

*Unit tests for PM configuration fields in ProjectConfig.

Tests cover:
- PM field defaults and validation
- from_dict() with PM fields
- Agent/skill extension when PM is enabled*

#### TestPMConfigFields
*Tests for PM fields in ProjectConfig.*

- `test_pm_enabled_default_false`
  - Test that pm_enabled defaults to False.
- `test_pm_backend_accepts_valid_values`
  - Test that pm_backend accepts valid backend values.
- `test_pm_doc_backend_accepts_valid_values`
  - Test that pm_doc_backend accepts valid backend values.
- `test_pm_methodology_accepts_valid_values`
  - Test that pm_methodology accepts valid methodology values.

#### TestPMConfigFromDict
*Tests for from_dict with PM fields.*

- `test_from_dict_with_pm_enabled`
  - Test from_dict with pm_enabled set to True.
- `test_from_dict_with_full_pm_config`
  - Test from_dict with complete PM configuration.
- `test_from_dict_pm_disabled_by_default`
  - Test that PM is disabled by default when not specified.

#### TestPMAgentSkillExtension
*Tests for agent/skill lists when PM is enabled.*

- `test_pm_agents_added_when_enabled`
  - Test that PM agents are added when PM is enabled.
- `test_pm_skills_added_when_enabled`
  - Test that PM skills are added when PM is enabled.
- `test_agents_unchanged_when_pm_disabled`
  - Test that agents list is unchanged when PM is disabled.

### tests\unit\test_project_config.py

*Unit tests for ProjectConfig dataclass.

Tests cover:
- Direct instantiation with various parameter combinations
- from_dict() factory method with valid/partial/empty data
- from_yaml_file() with valid and invalid YAML files
- from_json_file() with valid and invalid JSON files
- Default value handling*

#### TestProjectConfigInstantiation
*Tests for direct ProjectConfig instantiation.*

- `test_minimal_instantiation`
  - Test creating ProjectConfig with only required field.
- `test_full_instantiation`
  - Test creating ProjectConfig with all fields.
- `test_mutable_default_isolation`
  - Test that mutable defaults are isolated between instances.

#### TestProjectConfigFromDict
*Tests for ProjectConfig.from_dict() factory method.*

- `test_from_dict_valid_full`
  - Test from_dict with complete valid dictionary.
- `test_from_dict_minimal`
  - Test from_dict with minimal dictionary.
- `test_from_dict_empty`
  - Test from_dict with empty dictionary uses defaults.
- `test_from_dict_partial`
  - Test from_dict with partial dictionary.
- `test_from_dict_extra_fields_ignored`
  - Test that extra fields in dictionary are ignored.

#### TestProjectConfigFromYaml
*Tests for ProjectConfig.from_yaml_file() factory method.*

- `test_from_yaml_file_valid`
  - Test from_yaml_file with valid YAML.
- `test_from_yaml_file_minimal`
  - Test from_yaml_file with minimal YAML content.
- `test_from_yaml_file_not_found`
  - Test from_yaml_file with non-existent file.
- `test_from_yaml_file_invalid_yaml`
  - Test from_yaml_file with invalid YAML syntax.

#### TestProjectConfigFromJson
*Tests for ProjectConfig.from_json_file() factory method.*

- `test_from_json_file_valid`
  - Test from_json_file with valid JSON.
- `test_from_json_file_minimal`
  - Test from_json_file with minimal JSON content.
- `test_from_json_file_not_found`
  - Test from_json_file with non-existent file.
- `test_from_json_file_invalid_json`
  - Test from_json_file with invalid JSON syntax.
- `test_from_json_file_empty`
  - Test from_json_file with empty JSON object.

#### TestProjectConfigDefaults
*Tests for default value handling.*

- `test_default_values_consistency`
  - Test that default values are consistent across creation methods.
- `test_none_vs_empty_handling`
  - Test handling of None vs empty values.

### tests\unit\test_research_first_pattern.py

*Tests for the Research-First Development Pattern.

These tests verify that the research-first development pattern is properly
defined, documented, and available for use in generated projects.

Test Categories:
1. Knowledge file structure and schema
2. Required workflow steps
3. Trigger definitions
4. Integration with agents and skills
5. Availability in generated projects*

#### TestKnowledgeFileStructure
*Tests for knowledge file schema compliance.*

- `test_knowledge_file_exists`
  - Research-first pattern knowledge file should exist.
- `test_has_required_top_level_fields`
  - Knowledge file should have required top-level fields.
- `test_has_axiom_alignment`
  - Knowledge file should document axiom alignment.
- `test_valid_json_schema`
  - Knowledge file should have valid JSON schema reference.

#### TestWorkflowSteps
*Tests for required workflow steps.*

- `test_has_workflow_definition`
  - Pattern should define a workflow.
- `test_workflow_includes_research_step`
  - Workflow should include a research step.
- `test_workflow_includes_document_step`
  - Workflow should include a documentation step.
- `test_workflow_includes_test_step`
  - Workflow should include a test step.
- `test_workflow_includes_build_step`
  - Workflow should include a build/implementation step.
- `test_workflow_order_is_research_before_build`
  - Research should come before build in workflow order.

#### TestTriggerDefinitions
*Tests for when the pattern should be applied.*

- `test_has_trigger_definitions`
  - Pattern should define when to apply research-first approach.
- `test_triggers_include_performance_optimization`
  - Performance optimization should trigger research-first.
- `test_triggers_include_security`
  - Security implementations should trigger research-first.
- `test_has_counter_indicators`
  - Pattern should define when NOT to apply research-first.

#### TestBenefitsDocumentation
*Tests for benefit documentation.*

- `test_has_benefits_section`
  - Pattern should document its benefits.
- `test_documents_multiplied_value`
  - Pattern should explain multiplied value concept.

#### TestAntiPatterns
*Tests for anti-pattern documentation.*

- `test_has_anti_patterns`
  - Pattern should document anti-patterns to avoid.
- `test_warns_against_not_invented_here`
  - Should warn against 'not invented here' syndrome.
- `test_warns_against_analysis_paralysis`
  - Should warn against analysis paralysis.

#### TestIntegrationPoints
*Tests for integration with agents and skills.*

- `test_references_related_patterns`
  - Pattern should reference related patterns.
- `test_defines_agent_integration`
  - Pattern should define how agents should use it.
- `test_knowledge_file_is_listed_in_manifest`
  - Knowledge file should be discoverable via manifest or directory.

#### TestExamples
*Tests for example usage.*

- `test_has_examples`
  - Pattern should include examples of application.
- `test_reactive_indexing_example`
  - Should include reactive indexing as an example.

#### TestGeneratedProjectAvailability
*Tests for availability in generated projects.*

- `test_pattern_can_be_serialized`
  - Pattern should be serializable for inclusion in generated projects.
- `test_no_absolute_paths`
  - Pattern should not contain absolute paths.

### tests\unit\test_sync_artifacts.py

*Tests for scripts/validation/sync_artifacts.py

Comprehensive tests for the unified artifact sync system including:
- Configuration loading from sync_config.json
- Artifact scanning with inclusion/exclusion logic
- Sync strategies (count, json_field, category_counts, tree_annotation)
- Directory-based triggers for CI optimization
- Integration with actual project files

### Why This Matters
Artifact synchronization ensures that the factory's documentation (README, guides, catalogs) 
stays perfectly in sync with the actual code and data (agents, skills, tests). 
This prevents documentation rot, provides accurate metrics to users, and ensures 
that generated catalogs always reflect the current capabilities of the factory.
In CI, these tests prevent pushing changes that would leave documentation in an 
inconsistent state.*

#### TestArtifactScanner
*Tests for the ArtifactScanner class.*

- `test_scan_finds_matching_files`
  - Verify that the scanner correctly identifies files matching a glob pattern.

How: Creates a dummy directory structure with matching and non-matching files,
then runs the scanner with a specific glob pattern.
Why: Ensures the core scanning logic can distinguish between artifacts and 
other files in the source directory.
- `test_scan_respects_exclusions`
  - Verify that the scanner respects the exclusion list in the configuration.

How: Creates a directory structure with a subdirectory that should be excluded,
then runs the scanner with an exclusion pattern.
Why: Allows users to skip certain files or directories (like templates or
internal metadata) when scanning for artifacts.
- `test_scan_recursive`
  - Verify that the scanner can perform recursive searches when configured.

How: Creates separate levels of directories and files, then runs the scanner
with recursive=True and a broad pattern.
Why: Essential for artifacts that may be nested deep within a directory
structure, such as workflow definitions or multi-level skills.
- `test_scan_parent_dir_id_extractor`
  - Verify that artifact IDs can be extracted from their parent directory names.

How: Places a file in a named subdirectory and runs the scanner with
id_extractor='parent_dir_name'.
Why: Supports artifacts where the folder name is the primary identifier
(e.g., skill or blueprint folders containing a standardized SKILL.md file).
- `test_scan_returns_empty_for_missing_dir`
  - Verify that the scanner handles non-existent source directories gracefully.

How: Configures a scan for a directory that does not exist in the filesystem.
Why: Prevents the sync engine from crashing if a configured directory is 
missing or has been renamed, returning an empty set of artifacts instead.

#### TestCountSyncStrategy
*Tests for the CountSyncStrategy class.*

- `test_detects_out_of_sync_count`
  - Verify that the count strategy correctly identifies a mismatch in numbers.

How: Provides a file with a specific count and compares it against a 
different actual count.
Why: The primary mechanism for ensuring that README footers or guide
summaries accurately reflect the current file counts in the repo.
- `test_reports_in_sync_when_matched`
  - Verify that the count strategy reports no changes when the numbers match.

How: Provides a file with a count that perfectly matches the actual count.
Why: Ensures that the sync process is idempotent and doesn't perform
unnecessary file writes when the state is already correct.
- `test_dry_run_does_not_modify_file`
  - Verify that dry-run mode correctly avoids any filesystem modifications.

How: Runs the sync logic with dry_run=True and then checks the file content
remains identical to the original.
Why: Critical for CI validation where we want to detect drift without
actually changing the files in the checkout.
- `test_updates_file_when_sync`
  - Verify that the strategy correctly updates the file content when syncing.

How: Runs the sync logic with dry_run=False and then checks the file content
has been updated with the new count.
Why: Ensures the auto-fix capability of the sync script actually works
and correctly applies the regex-based replacement.

#### TestJsonFieldSyncStrategy
*Tests for the JsonFieldSyncStrategy class.*

- `test_updates_nested_json_field`
  - Verify that the JSON strategy can update values deep within a nested structure.

How: Creates a JSON file with nested property and runs sync with dot-walk path.
Why: Many project meta-files (like manifest.json) use nested objects for 
organization, and we must be able to target them precisely.
- `test_creates_missing_nested_structure`
  - Verify that the JSON strategy creates missing parent objects if they don't exist.

How: Targets a nested path in an empty JSON object.
Why: Simplifies configuration by allowing the sync process to initialize
statistics or metadata structures if they are missing from a new file.

#### TestSyncEngine
*Tests for the SyncEngine class.*

- `test_loads_config_from_file`
  - Verify that the SyncEngine correctly parses the main sync_config.json file.

How: Creates a valid mock config file and initializes the engine with it.
Why: The entire sync system is drive by this configuration; failure to 
parse it correctly would break all synchronization tasks.
- `test_get_directory_triggers`
  - Verify that the engine correctly maps source directories to artifact types.

How: Configures directory triggers and checks the returned mapping.
Why: Used by CI to determine which documentation files need re-syncing
based on which code directories were modified in a pull request.
- `test_get_artifacts_for_dirs`
  - Verify that the engine identifies the correct artifacts impacted by changed dirs.

How: Provided a list of changed paths and checks if the corresponding 
artifacts are returned.
Why: Critical for 'smart sync' where we only run expensive validation and
sync tasks for components that actually changed.
- `test_sync_artifact_unknown_returns_error`
  - Verify that requesting a sync for a non-existent artifact returns an error.

How: Calls sync_artifact with an ID that is not in the configuration.
Why: Ensures the API provides feedback when invalid artifact types are 
requested, rather than failing silently or with a generic error.

#### TestIntegration
*Integration tests using actual project files.*

- `test_config_file_exists`
  - Sanity check that the actual production sync_config.json exists in the repo.

How: Checks for the existence of the config file relative to factory root.
Why: The entire validation suite relies on this file; its absence would 
be a critical repository misconfiguration.
- `test_config_is_valid_json`
  - Verify that the production sync_config.json is valid and readable JSON.

How: Attempts to load the actual config file with the json library.
Why: Prevents accidental syntax errors in the JSON config from breaking
the CI pipeline.
- `test_config_has_all_artifact_types`
  - Verify that all core factory artifacts are defined in the sync configuration.

How: Checks the artifact list against the expected set of factory types.
Why: Ensures developers don't forget to add documentation sync rules 
when new artifact types are added to the system.
- `test_engine_loads_successfully`
  - Verify that the SyncEngine can initialize with the real production config.

How: Initializes a new SyncEngine instance pointing to the repo root.
Why: Validates that the production config is not only valid JSON but 
also logically correct for the defined SyncEngine schema.
- `test_sync_all_dry_run_succeeds`
  - Perform a full dry-run sync across all artifacts in the actual repository.

How: Runs engine.sync_all(dry_run=True) and checks for errors in the results.
Why: This is the definitive integration test for the Entire Repo's 
documentation state. It ensures every sync target is valid and reachable.
- `test_artifacts_are_currently_synced`
  - Verify that the repository documentation is currently in a perfectly synced state.

How: Runs sync_all and asserts that zero 'changed' status items are returned.
Why: Used as a CI gate to ensure PRs don't introduce documentation drift.
If this fails, the developer must run 'sync_artifacts.py --sync' locally.

#### TestDirectoryDetection
*Tests for directory-based sync triggering.*

- `test_detects_agents_dir`
  - Verify that changes to the agents directory trigger a sync for that artifact.

How: Simulates a change to an agent file and checks if the 'agents' 
artifact type is correctly identified.
Why: Documentation for agents (like README counts) must be updated 
whenever an agent is added, removed, or changed.
- `test_detects_nested_path`
  - Verify that nested file changes correctly trigger parent artifact syncs.

How: Simulates a change to a deeply nested file within a trigger directory.
Why: Ensures that changes to sub-components (like a specific skill's 
internal logic) still trigger the high-level artifact sync.

#### TestCategoryTestCounts
*Tests for the CategoryTestCounts NamedTuple.*

- `test_creates_valid_namedtuple`
  - Should create a valid CategoryTestCounts instance.
- `test_counts_are_immutable`
  - CategoryTestCounts should be immutable.

#### TestGetPythonPath
*Tests for Python path detection.*

- `test_returns_current_interpreter`
  - Verify that get_python_path returns the current active Python interpreter.

How: Compares the function result against sys.executable.
Why: Ensures that sync scripts run by the factory use the same 
environment/interpreter as the factory itself, avoiding dependency issues.

#### TestCollectTestCount
*Tests for test count collection.*

- `test_returns_integer`
  - Verify that collect_test_count returns the number of tests as an integer.

How: Mocks the subprocess call to return a standard pytest collection 
output and checks if the correct number is parsed.
Why: Core helper for the 'tests' artifact count target.
- `test_handles_subprocess_timeout`
  - Verify that the collector handles subprocess timeouts gracefully by returning 0.

How: Simulates a TimeoutExpired exception in the mocked subprocess.run call.
Why: Prevents the entire sync process from hanging if pytest takes too long
to collect tests (e.g., due to extreme recursion in test generators).
- `test_handles_missing_directory`
  - Verify that the collector returns 0 when the target test directory is missing.

How: Attempts to collect tests from a non-existent path.
Why: Ensures that if a test category is renamed or deleted, the sync 
script doesn't crash, but instead reports 0 tests.
- `test_parses_plural_tests`
  - Verify that the parser correctly extracts counts when multiple tests are found.

How: Provides '100 tests collected' string to the parser.
Why: Pytest uses plural 'tests' when count > 1.
- `test_parses_singular_test`
  - Verify that the parser correctly extracts counts when exactly one test is found.

How: Provides '1 test collected' string to the parser.
Why: Ensure the regex handles the singular 'test' case which has different 
output formatting in pytest.

#### TestExtractDocumentedCounts
*Tests for extracting counts from TESTING.md content.*

- `test_extracts_total_count`
  - Should extract total test count.
- `test_extracts_category_counts`
  - Should extract all category counts.
- `test_handles_missing_total`
  - Verify that the extractor returns 0 for the total if it's not found in content.

How: Provides a string that does not match the 'consists of **X tests**' pattern.
Why: Robustness against malformed or missing documentation sections.
- `test_handles_missing_categories`
  - Verify that the extractor returns 0 for categories missing from the table.

How: Provides a string with a total count but no category table.
Why: Ensures the sync script doesn't crash if only the total count exists
but the category breakdown is missing.

#### TestUpdateTestingMd
*Tests for updating TESTING.md.*

- `test_detects_out_of_sync_total`
  - Should detect when total count is out of sync.
- `test_dry_run_does_not_modify_file`
  - Verify that update_testing_md respects the dry_run flag.

How: Calls the function with dry_run=True and checks that the file 
remains unchanged despite being out of sync.
Why: Safety mechanism for validation-only runs.
- `test_sync_updates_file`
  - Should update file when dry_run=False.
- `test_reports_missing_file`
  - Verify that update_testing_md handles the absence of the target file.

How: Calls the function when TESTING.md hasn't been created yet.
Why: Ensures the sync script provides helpful error messages instead of 
crashing if a target file is missing.
- `test_no_changes_when_synced`
  - Verify that update_testing_md returns zero changes when counts match EXACTLY.

How: Provides a file with counts that match the 'actual' parameter.
Why: Confirms idempotency of the high-level sync operation.

### tests\unit\test_sync_knowledge_counts.py

*Tests for scripts/validation/sync_knowledge_counts.py

Ensures the knowledge count sync script correctly:
- Counts knowledge files in knowledge/ directory
- Extracts counts from manifest.json and KNOWLEDGE_FILES.md
- Updates files when counts differ*

#### TestCountKnowledgeFiles
*Tests for counting knowledge files.*

- `test_counts_json_files`
  - Should count all .json files in knowledge/.
- `test_excludes_underscore_prefixed`
  - Should exclude files starting with underscore.
- `test_excludes_subdirectories`
  - Should not count files in subdirectories.
- `test_returns_zero_for_missing_dir`
  - Should return 0 if knowledge/ doesn't exist.

#### TestGetManifestCount
*Tests for extracting count from manifest.json.*

- `test_extracts_total_files`
  - Should extract statistics.total_files from manifest.
- `test_returns_zero_for_missing_manifest`
  - Should return 0 if manifest doesn't exist.
- `test_returns_zero_for_missing_statistics`
  - Should return 0 if statistics key is missing.

#### TestGetDocsCount
*Tests for extracting count from KNOWLEDGE_FILES.md.*

- `test_extracts_count_from_docs`
  - Should extract count from KNOWLEDGE_FILES.md.
- `test_returns_zero_for_missing_file`
  - Should return 0 if file doesn't exist.
- `test_returns_zero_for_no_match`
  - Should return 0 if pattern doesn't match.

#### TestUpdateManifest
*Tests for updating manifest.json.*

- `test_dry_run_does_not_modify`
  - Should not modify file when dry_run=True.
- `test_updates_count`
  - Should update count when dry_run=False.
- `test_returns_false_when_synced`
  - Should return False when counts match.

#### TestUpdateDocs
*Tests for updating KNOWLEDGE_FILES.md.*

- `test_dry_run_does_not_modify`
  - Should not modify file when dry_run=True.
- `test_updates_count`
  - Should update count when dry_run=False.

#### TestSyncKnowledgeCounts
*Tests for the main sync function.*

- `test_detects_out_of_sync`
  - Should detect when counts are out of sync.
- `test_reports_synced_when_matched`
  - Should report synced when all counts match.

#### TestIntegration
*Integration tests using actual project files.*

- `test_knowledge_dir_exists`
  - knowledge/ directory should exist.
- `test_manifest_exists`
  - knowledge/manifest.json should exist.
- `test_knowledge_files_md_exists`
  - docs/reference/KNOWLEDGE_FILES.md should exist.
- `test_counts_are_currently_synced`
  - Current knowledge counts should be in sync.

### tests\unit\test_sync_test_counts.py

*Tests for test count synchronization functionality.

Tests the unified sync_artifacts.py test count capabilities:
- Collects test counts from pytest
- Extracts documented counts from TESTING.md
- Updates TESTING.md when counts differ

Note: The deprecated sync_test_counts.py is a thin wrapper that re-exports
these functions for backward compatibility.*

#### TestCategoryTestCounts
*Tests for the CategoryTestCounts NamedTuple.*

- `test_creates_valid_namedtuple`
  - Should create a valid CategoryTestCounts instance.
- `test_counts_are_immutable`
  - CategoryTestCounts should be immutable.
- `test_deprecated_alias_works`
  - CountsByCategory alias from deprecated module should work.

#### TestGetPythonPath
*Tests for Python path detection.*

- `test_returns_string`
  - Should return a string path.
- `test_returns_current_interpreter`
  - Should return the current Python interpreter.

#### TestCollectTestCount
*Tests for test count collection.*

- `test_returns_integer`
  - Should return an integer count.
- `test_handles_subprocess_timeout`
  - Should return 0 on timeout.
- `test_handles_missing_directory`
  - Should return 0 for non-existent directory.
- `test_parses_plural_tests`
  - Should parse 'tests collected' output.
- `test_parses_singular_test`
  - Should parse '1 test collected' output.

#### TestExtractDocumentedCounts
*Tests for extracting counts from TESTING.md content.*

- `test_extracts_total_count`
  - Should extract total test count.
- `test_extracts_category_counts`
  - Should extract all category counts.
- `test_handles_missing_total`
  - Should return 0 for missing total.
- `test_handles_missing_categories`
  - Should return 0 for missing categories.

#### TestUpdateTestingMd
*Tests for updating TESTING.md.*

- `test_detects_out_of_sync_total`
  - Should detect when total count is out of sync.
- `test_dry_run_does_not_modify_file`
  - Should not modify file when dry_run=True.
- `test_sync_updates_file`
  - Should update file when dry_run=False.
- `test_reports_missing_file`
  - Should report when TESTING.md is missing.
- `test_no_changes_when_synced`
  - Should return empty changes when counts match.

#### TestIntegration
*Integration tests using actual project files.*

- `test_testing_md_exists`
  - docs/TESTING.md should exist.
- `test_testing_md_has_expected_structure`
  - TESTING.md should have the expected structure for parsing.
- `test_can_extract_counts_from_real_file`
  - Should be able to extract counts from actual TESTING.md.
- `test_counts_are_currently_synced`
  - Current test counts should match documentation.

Note: This test respects A2 Truth - test counts are environment-dependent.
When TESTING.md uses approximate counts (e.g., "1300+ tests"), exact sync
is not enforced. The measure of success is that tests pass, not the count.

### tests\unit\test_taxonomy.py

*Unit tests for scripts/taxonomy/__init__.py

Tests for TopicNode, TaxonomyLoader, and load_agent_taxonomy functionality.*

#### TestTopicNode
*Tests for TopicNode dataclass.*

- `test_create_topic_node`
  - Test creating a basic TopicNode.
- `test_create_topic_node_with_keywords`
  - Test creating a TopicNode with keywords.
- `test_get_all_keywords_no_subtopics`
  - Test get_all_keywords with no subtopics.
- `test_get_all_keywords_with_subtopics`
  - Test get_all_keywords includes subtopic keywords.
- `test_get_leaf_topics_no_children`
  - Test get_leaf_topics when node has no children.
- `test_get_leaf_topics_with_children`
  - Test get_leaf_topics returns only leaves.
- `test_count_topics_single`
  - Test count_topics for single node.
- `test_count_topics_with_subtopics`
  - Test count_topics includes subtopics.
- `test_nested_subtopics_deep`
  - Test deeply nested subtopics.

#### TestTaxonomyLoader
*Tests for TaxonomyLoader class.*

- `test_init_default_directory`
  - Test TaxonomyLoader uses default directory.
- `test_init_custom_directory`
  - Test TaxonomyLoader with custom directory.
- `test_load_taxonomy_success`
  - Test successful taxonomy loading.
- `test_load_taxonomy_file_not_found`
  - Test loading non-existent taxonomy raises error.
- `test_load_taxonomy_invalid_json`
  - Test loading invalid JSON raises error.
- `test_cache_works`
  - Test that taxonomy is cached after first load.
- `test_get_available_taxonomies`
  - Test getting list of available taxonomies.
- `test_get_all_topics_flat`
  - Test flattening all topics from taxonomy.
- `test_parse_topic_with_subtopics`
  - Test parsing topics with nested subtopics key.

#### TestLoadAgentTaxonomy
*Tests for the load_agent_taxonomy convenience function.*

- `test_load_default_taxonomy`
  - Test loading the default agent taxonomy.
- `test_taxonomy_has_domains`
  - Test that taxonomy has expected domains.
- `test_taxonomy_topics_have_keywords`
  - Test that taxonomy topics have keywords defined.

### tests\unit\test_template_engine.py

*Unit tests for TemplateEngine class and custom filters.

Tests cover:
- Filter functions (snake_case, pascal_case, etc.)
- TemplateEngine initialization
- Template rendering with Jinja2 syntax
- Legacy placeholder support
- Custom globals (now(), env())
- Template variable extraction*

#### TestSnakeCaseFilter
*Tests for snake_case filter.*

- `test_from_pascal_case`
  - Test conversion from PascalCase.
- `test_from_camel_case`
  - Test conversion from camelCase.
- `test_from_kebab_case`
  - Test conversion from kebab-case.
- `test_with_spaces`
  - Test conversion from space-separated words.
- `test_empty_and_none`
  - Test with empty string.

#### TestPascalCaseFilter
*Tests for pascal_case filter.*

- `test_from_snake_case`
  - Test conversion from snake_case.
- `test_from_kebab_case`
  - Test conversion from kebab-case.
- `test_from_spaces`
  - Test conversion from space-separated words.
- `test_empty`
  - Test with empty string.

#### TestCamelCaseFilter
*Tests for camel_case filter.*

- `test_from_snake_case`
  - Test conversion from snake_case.
- `test_from_kebab_case`
  - Test conversion from kebab-case.
- `test_empty`
  - Test with empty string.

#### TestKebabCaseFilter
*Tests for kebab_case filter.*

- `test_from_pascal_case`
  - Test conversion from PascalCase.
- `test_from_snake_case`
  - Test conversion from snake_case.
- `test_empty`
  - Test with empty string.

#### TestTitleCaseFilter
*Tests for title_case filter.*

- `test_from_snake_case`
  - Test conversion from snake_case.
- `test_from_kebab_case`
  - Test conversion from kebab-case.
- `test_empty`
  - Test with empty string.

#### TestPluralizeFilter
*Tests for pluralize filter.*

- `test_regular_plurals`
  - Test regular plural forms.
- `test_special_endings`
  - Test words with special endings.
- `test_count_one`
  - Test with count=1 (should not pluralize).
- `test_irregulars`
  - Test irregular plurals.
- `test_empty`
  - Test with empty string.

#### TestQuoteFilter
*Tests for quote filter.*

- `test_double_quotes`
  - Test double quote style.
- `test_single_quotes`
  - Test single quote style.
- `test_backticks`
  - Test backtick style.

#### TestIndentTextFilter
*Tests for indent_text filter.*

- `test_basic_indent`
  - Test basic indentation.
- `test_indent_first_line`
  - Test with first line indented.
- `test_empty`
  - Test with empty string.

#### TestWrapCodeFilter
*Tests for wrap_code filter.*

- `test_with_language`
  - Test with language specified.
- `test_without_language`
  - Test without language.

#### TestDefaultIfEmptyFilter
*Tests for default_if_empty filter.*

- `test_with_value`
  - Test with non-empty value.
- `test_with_empty_string`
  - Test with empty string.
- `test_with_none`
  - Test with None.
- `test_with_empty_list`
  - Test with empty list.

#### TestJoinLinesFilter
*Tests for join_lines filter.*

- `test_basic_join`
  - Test basic joining.
- `test_custom_separator`
  - Test with custom separator.
- `test_empty_list`
  - Test with empty list.

#### TestToJsonFilter
*Tests for to_json filter.*

- `test_dict`
  - Test with dictionary.
- `test_list`
  - Test with list.

#### TestToYamlListFilter
*Tests for to_yaml_list filter.*

- `test_basic_list`
  - Test basic list.
- `test_empty_list`
  - Test with empty list.

#### TestNowGlobal
*Tests for now() global function.*

- `test_default_format`
  - Test default format.
- `test_custom_format`
  - Test custom format.

#### TestEnvGlobal
*Tests for env() global function.*

- `test_existing_variable`
  - Test with existing environment variable.
- `test_missing_variable`
  - Test with missing variable and default.

#### TestRangeListGlobal
*Tests for range_list() global function.*

- `test_basic_range`
  - Test basic range.
- `test_with_step`
  - Test with step.

#### TestTemplateEngineInit
*Tests for TemplateEngine initialization.*

- `test_init_basic`
  - Test basic initialization.
- `test_init_with_dirs`
  - Test initialization with template directories.
- `test_filters_registered`
  - Test that custom filters are registered.
- `test_globals_registered`
  - Test that custom globals are registered.

#### TestTemplateEngineRenderString
*Tests for render_string method.*

- `test_simple_variable`
  - Test simple variable substitution.
- `test_filter_in_template`
  - Test using filter in template.
- `test_conditional`
  - Test conditional in template.
- `test_loop`
  - Test loop in template.
- `test_legacy_placeholder_uppercase`
  - Test legacy {{UPPERCASE}} placeholder conversion.
- `test_global_now_in_template`
  - Test using now() in template.

#### TestTemplateEngineRenderFile
*Tests for render_file method.*

- `test_render_from_file`
  - Test rendering from a file path.

#### TestTemplateEngineAddFilter
*Tests for add_filter method.*

- `test_add_custom_filter`
  - Test adding a custom filter.

#### TestTemplateEngineAddGlobal
*Tests for add_global method.*

- `test_add_custom_global`
  - Test adding a custom global.

#### TestTemplateEngineGetVariables
*Tests for get_template_variables method.*

- `test_extract_variables`
  - Test extracting variables from template.

#### TestCreateEngine
*Tests for create_engine convenience function.*

- `test_create_with_defaults`
  - Test creating engine with default settings.

### tests\unit\test_update_engine.py

*Comprehensive unit tests for the scripts/updates/ module.

Tests cover:
- ChangelogGenerator: changelog creation, markdown generation, version diffs
- NotificationSystem: notification delivery, filtering, history management
- SourceAggregator: update aggregation, deduplication, health monitoring
- UpdateEngine: update application, merge strategies, backup management

Author: Cursor Agent Factory
Version: 1.0.0*

#### TestChangelogEntry
*Tests for ChangelogEntry dataclass.*

- `test_changelog_entry_creation`
  - Test creating a ChangelogEntry.
- `test_changelog_entry_defaults`
  - Test ChangelogEntry with default values.

#### TestChangelogGeneratorInit
*Tests for ChangelogGenerator initialization.*

- `test_init_creates_directory`
  - Test that initialization creates changelog directory.
- `test_init_existing_directory`
  - Test initialization with existing directory.

#### TestChangelogGeneratorPaths
*Tests for changelog path methods.*

- `test_get_changelog_path`
  - Test getting changelog path for a knowledge file.
- `test_get_changelog_path_with_path_object`
  - Test getting changelog path with Path object.

#### TestChangelogGeneratorLoadSave
*Tests for loading and saving changelogs.*

- `test_load_nonexistent_changelog`
  - Test loading a changelog that doesn't exist.
- `test_load_existing_changelog`
  - Test loading an existing changelog.
- `test_save_changelog`
  - Test saving a changelog.

#### TestChangelogGeneratorCreateEntry
*Tests for creating changelog entries.*

- `test_create_entry_from_update_result`
  - Test creating entry from UpdateResult.
- `test_create_entry_from_knowledge_update`
  - Test creating entry from KnowledgeUpdate.
- `test_create_entry_removes_empty_categories`
  - Test that empty change categories are removed.

#### TestChangelogGeneratorAppend
*Tests for appending entries.*

- `test_append_entry_new_changelog`
  - Test appending to a new changelog.
- `test_append_entry_existing_changelog`
  - Test appending to existing changelog.
- `test_append_entry_with_migration_notes`
  - Test appending entry with migration notes.

#### TestChangelogGeneratorMarkdown
*Tests for markdown generation.*

- `test_generate_markdown_empty`
  - Test generating markdown for empty changelog.
- `test_generate_markdown_with_entries`
  - Test generating markdown with entries.
- `test_generate_markdown_with_max_entries`
  - Test generating markdown with max entries limit.
- `test_generate_markdown_breaking_changes`
  - Test markdown generation with breaking changes.

#### TestChangelogGeneratorSummary
*Tests for summary generation.*

- `test_generate_summary_no_files`
  - Test generating summary with no changelog files.
- `test_generate_summary_with_files`
  - Test generating summary with changelog files.
- `test_generate_summary_with_filter`
  - Test generating summary with file filter.

#### TestChangelogGeneratorVersionDiff
*Tests for version diff functionality.*

- `test_get_version_diff`
  - Test getting changes between versions.
- `test_get_version_diff_no_matches`
  - Test version diff with no matching versions.

#### TestNotification
*Tests for Notification dataclass.*

- `test_notification_creation`
  - Test creating a notification.
- `test_notification_to_dict`
  - Test converting notification to dictionary.
- `test_notification_format_console`
  - Test console formatting.

#### TestNotificationSystemInit
*Tests for NotificationSystem initialization.*

- `test_init_default_config`
  - Test initialization with default config.
- `test_init_custom_config`
  - Test initialization with custom config.

#### TestNotificationSystemNotify
*Tests for notification delivery.*

- `test_notify_basic`
  - Test basic notification.
- `test_notify_quiet_mode`
  - Test notification in quiet mode.
- `test_notify_min_level`
  - Test notification filtering by minimum level.
- `test_notify_file_output`
  - Test notification file output.
- `test_notify_callback`
  - Test notification callbacks.
- `test_notify_callback_error_handling`
  - Test that callback errors don't break notification.

#### TestNotificationSystemHistory
*Tests for notification history management.*

- `test_get_history`
  - Test getting notification history.
- `test_get_history_filtered_by_level`
  - Test filtering history by level.
- `test_get_history_unread_only`
  - Test getting only unread notifications.
- `test_mark_read`
  - Test marking notification as read.
- `test_mark_all_read`
  - Test marking all notifications as read.
- `test_clear_history`
  - Test clearing notification history.
- `test_history_max_limit`
  - Test that history respects max limit.

#### TestNotificationSystemCallbacks
*Tests for callback management.*

- `test_register_callback`
  - Test registering a callback.
- `test_unregister_callback`
  - Test unregistering a callback.

#### TestNotificationSystemSpecialized
*Tests for specialized notification methods.*

- `test_notify_updates_available_empty`
  - Test notifying about empty updates.
- `test_notify_updates_available_with_updates`
  - Test notifying about available updates.
- `test_notify_update_applied_success`
  - Test notifying about successful update.
- `test_notify_update_applied_failure`
  - Test notifying about failed update.
- `test_notify_batch_complete_success`
  - Test notifying about successful batch.
- `test_notify_rollback_success`
  - Test notifying about successful rollback.
- `test_generate_digest`
  - Test generating notification digest.
- `test_generate_digest_empty`
  - Test generating digest with no unread notifications.

#### TestSourceHealth
*Tests for SourceHealth dataclass.*

- `test_source_health_creation`
  - Test creating SourceHealth.

#### TestAggregationResult
*Tests for AggregationResult dataclass.*

- `test_aggregation_result_creation`
  - Test creating AggregationResult.
- `test_aggregation_result_by_priority`
  - Test grouping updates by priority.
- `test_aggregation_result_by_file`
  - Test grouping updates by file.
- `test_aggregation_result_filter_subscriptions`
  - Test filtering by subscription patterns.
- `test_aggregation_result_filter_all`
  - Test filtering with wildcard pattern.

#### TestSourceAggregatorInit
*Tests for SourceAggregator initialization.*

- `test_init_initializes_adapters`
  - Test that initialization sets up adapters.
  - Markers: patch
- `test_get_enabled_adapters`
  - Test getting enabled adapters.

#### TestSourceAggregatorGetAdapter
*Tests for getting adapters.*

- `test_get_adapter_exists`
  - Test getting an existing adapter.
- `test_get_adapter_not_exists`
  - Test getting a non-existent adapter.

#### TestUpdateOperation
*Tests for UpdateOperation dataclass.*

- `test_update_operation_creation`
  - Test creating an UpdateOperation.
- `test_update_operation_to_dict`
  - Test converting operation to dictionary.

#### TestUpdateResult
*Tests for UpdateResult dataclass.*

- `test_update_result_creation`
  - Test creating an UpdateResult.

#### TestBatchUpdateResult
*Tests for BatchUpdateResult dataclass.*

- `test_batch_update_result_creation`
  - Test creating a BatchUpdateResult.
- `test_batch_update_result_auto_id`
  - Test that batch ID is auto-generated.

#### TestUpdateEngineInit
*Tests for UpdateEngine initialization.*

- `test_init_creates_directories`
  - Test that initialization creates directories.
- `test_init_custom_backup_dir`
  - Test initialization with custom backup directory.

#### TestUpdateEngineBackup
*Tests for backup management.*

- `test_create_backup`
  - Test creating a backup.
- `test_rotate_backups`
  - Test backup rotation.
- `test_restore_backup`
  - Test restoring from backup.
- `test_list_backups`
  - Test listing backups.
- `test_list_backups_filtered`
  - Test listing backups filtered by file.

#### TestUpdateEngineApplyUpdate
*Tests for applying updates.*

- `test_apply_update_new_file`
  - Test applying update to a new file.
- `test_apply_update_existing_file`
  - Test applying update to existing file.
- `test_apply_update_with_backup`
  - Test applying update creates backup.
- `test_apply_update_without_backup`
  - Test applying update without backup.
- `test_apply_update_validation_error`
  - Test applying update with validation error.
- `test_apply_update_exception_handling`
  - Test exception handling during update.

#### TestUpdateEngineMergeStrategies
*Tests for different merge strategies.*

- `test_merge_conservative`
  - Test conservative merge strategy.
- `test_merge_balanced`
  - Test balanced merge strategy.
- `test_merge_aggressive`
  - Test aggressive merge strategy.

#### TestUpdateEngineBatch
*Tests for batch updates.*

- `test_apply_batch`
  - Test applying batch of updates.
- `test_apply_batch_partial_failure`
  - Test batch with partial failures.

#### TestUpdateEngineRollback
*Tests for rollback functionality.*

- `test_rollback_single_file`
  - Test rolling back a single file.
- `test_rollback_nonexistent_backup`
  - Test rolling back with non-existent backup.
- `test_rollback_batch`
  - Test rolling back a batch.
- `test_rollback_batch_not_found`
  - Test rolling back non-existent batch.

#### TestUpdateEngineHistory
*Tests for update history.*

- `test_get_history`
  - Test getting update history.

#### TestUpdateEngineValidation
*Tests for content validation.*

- `test_validate_content_valid`
  - Test validation of valid content.
- `test_validate_content_missing_version`
  - Test validation with missing version.
- `test_validate_content_invalid_version`
  - Test validation with invalid version format.
- `test_validate_content_not_dict`
  - Test validation with non-dict content.
- `test_is_valid_version`
  - Test version format validation.

#### TestChangelogGeneratorEdgeCases
*Additional edge case tests for ChangelogGenerator.*

- `test_create_entry_empty_operations`
  - Test creating entry with no operations.
- `test_create_entry_unknown_operation_type`
  - Test handling unknown operation types.
- `test_generate_markdown_empty_changes`
  - Test markdown generation with empty changes.
- `test_get_changelog_path_nested`
  - Test changelog path with nested file path.

#### TestNotificationSystemEdgeCases
*Additional edge case tests for NotificationSystem.*

- `test_notify_file_write_error`
  - Test handling file write errors.
- `test_notify_updates_available_with_details_disabled`
  - Test notify_updates_available with show_details=False.
- `test_notify_update_applied_with_changelog_disabled`
  - Test notify_update_applied with show_changelog=False.

#### TestSourceAggregatorEdgeCases
*Additional edge case tests for SourceAggregator.*

- `test_deduplicate_updates_same_priority`
  - Test deduplication when updates have same priority.
- `test_filter_subscriptions_empty_patterns`
  - Test filter_subscriptions with empty patterns list.

#### TestUpdateEngineEdgeCases
*Additional edge case tests for UpdateEngine.*

- `test_apply_update_with_checksum`
  - Test applying update with checksum.
- `test_apply_update_without_proposed_content`
  - Test applying update without proposed_content.
- `test_deep_merge_nested_structures`
  - Test deep merge with nested structures.
- `test_merge_conservative_preserves_existing`
  - Test conservative merge preserves existing values.
- `test_rollback_invalid_backup_name`
  - Test rollback with invalid backup filename format.
- `test_list_backups_nonexistent_stem`
  - Test listing backups for non-existent file.

### tests\unit\test_validate_readme.py

*Unit tests for scripts/validation/validate_readme_structure.py

Tests README structure validation and update functionality.*

#### TestStructureValidatorInit
*Tests for StructureValidator initialization.*

- `test_init_with_default_path`
  - Test initialization with default path.
- `test_init_with_custom_path`
  - Test initialization with custom path.

#### TestShouldIgnore
*Tests for _should_ignore method.*

- `test_ignores_pycache`
  - Test that __pycache__ is ignored.
- `test_ignores_git`
  - Test that .git is ignored.
- `test_ignores_dotfiles`
  - Test that dotfiles are ignored.
- `test_ignores_pyc_files`
  - Test that .pyc files are ignored.
- `test_does_not_ignore_valid_dir`
  - Test that valid directories are not ignored.

#### TestCountFilesByExtension
*Tests for _count_files_by_extension method.*

- `test_counts_json_files`
  - Test counting JSON files.
- `test_counts_in_subdirectories`
  - Test counting files in subdirectories.
- `test_excludes_pycache`
  - Test that __pycache__ files are excluded.

#### TestScanAgents
*Tests for scan_agents method.*

- `test_scan_no_agents_dir`
  - Test scanning when agents directory doesn't exist.
- `test_scan_with_agents`
  - Test scanning with agents present.

#### TestScanSkills
*Tests for scan_skills method.*

- `test_scan_no_skills_dir`
  - Test scanning when skills directory doesn't exist.
- `test_scan_with_skills`
  - Test scanning with skills present.

#### TestScanBlueprints
*Tests for scan_blueprints method.*

- `test_scan_no_blueprints_dir`
  - Test scanning when blueprints directory doesn't exist.
- `test_scan_with_blueprints`
  - Test scanning with blueprints present.

#### TestScanPatterns
*Tests for scan_patterns method.*

- `test_scan_no_patterns_dir`
  - Test scanning when patterns directory doesn't exist.
- `test_scan_with_patterns`
  - Test scanning with patterns present.

#### TestScanKnowledge
*Tests for scan_knowledge method.*

- `test_scan_no_knowledge_dir`
  - Test scanning when knowledge directory doesn't exist.
- `test_scan_with_knowledge`
  - Test scanning with knowledge files present.

#### TestScanTemplates
*Tests for scan_templates method.*

- `test_scan_no_templates_dir`
  - Test scanning when templates directory doesn't exist.
- `test_scan_with_templates`
  - Test scanning with templates present.

#### TestScanAll
*Tests for scan_all method.*

- `test_scan_all_returns_all_sections`
  - Test that scan_all returns all sections.

#### TestRoundToThreshold
*Tests for _round_to_threshold method.*

- `test_round_small_numbers`
  - Test rounding small numbers.
- `test_round_medium_numbers`
  - Test rounding medium numbers.
- `test_round_large_numbers`
  - Test rounding large numbers.

#### TestGenerateCountsSummary
*Tests for generate_counts_summary method.*

- `test_returns_all_counts`
  - Test that all counts are returned.

#### TestExtractReadmeCounts
*Tests for extract_readme_counts method.*

- `test_no_readme`
  - Test when README doesn't exist.
- `test_extract_exact_counts`
  - Test extracting exact counts from README.
- `test_extract_threshold_counts`
  - Test extracting threshold counts (50+ files).

#### TestValidate
*Tests for validate method.*

- `test_validate_matching_counts`
  - Test validation with matching counts.
- `test_validate_threshold_passing`
  - Test validation with threshold counts that pass.

#### TestUpdateReadme
*Tests for update_readme method.*

- `test_update_no_readme`
  - Test update when README doesn't exist.
- `test_update_with_structure_section`
  - Test updating README with existing structure section.
- `test_update_no_structure_section`
  - Test updating README without structure section.

#### TestGenerateStructureMarkdown
*Tests for generate_structure_markdown method.*

- `test_generates_markdown`
  - Test that markdown is generated.
- `test_includes_counts`
  - Test that counts are included in markdown.

#### TestMain
*Tests for main function.*

- `test_main_check_mode`
  - Test main with --check.
- `test_main_generate_mode`
  - Test main with --generate.
- `test_main_json_mode`
  - Test main with --json.
- `test_main_update_mode`
  - Test main with --update.
- `test_main_with_custom_root`
  - Test main with --root argument.
- `test_main_default_is_check`
  - Test that default mode is --check.

## Validation Tests

### tests\validation\test_blueprint_schema.py

*Schema validation tests for blueprint files.

Tests validate that all blueprint.json files conform to expected structure.*

#### TestBlueprintSchema
*Tests for blueprint schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_all_blueprints_valid`
  - Test that all blueprint.json files are valid against schema.
- `test_python_fastapi_blueprint_valid`
  - Test that python-fastapi blueprint is valid.
- `test_blueprint_ids_match_directory_names`
  - Test that blueprintId matches the directory name.
- `test_blueprint_has_valid_language`
  - Test that blueprints have valid primary language.
- `test_blueprint_agent_references_format`
  - Test that agent references have correct format.

### tests\validation\test_extension_templates.py

*Validation tests for extension templates and patterns.

Tests validate that extension templates and schemas are properly structured.*

#### TestKnowledgeTemplate
*Tests for knowledge file template.*

- `test_template_exists`
  - Test that knowledge template exists.
- `test_template_has_placeholders`
  - Test that template has placeholder variables.
- `test_template_has_required_placeholders`
  - Test that template has required placeholders.
- `test_template_valid_json_structure`
  - Test that template represents valid JSON structure.
- `test_template_has_patterns_array`
  - Test that template includes patterns array.

#### TestSkillTemplate
*Tests for skill file template.*

- `test_skill_template_exists`
  - Test that skill template exists.
- `test_skill_template_has_frontmatter`
  - Test that skill template has YAML frontmatter.
- `test_skill_template_has_required_frontmatter`
  - Test that skill template has required frontmatter fields.
- `test_skill_template_has_sections`
  - Test that skill template has standard sections.

#### TestAgentTemplate
*Tests for agent file template.*

- `test_agent_template_exists`
  - Test that agent template exists.
- `test_agent_template_has_frontmatter`
  - Test that agent template has YAML frontmatter.
- `test_agent_template_has_required_frontmatter`
  - Test that agent template has required frontmatter fields.
- `test_agent_template_has_sections`
  - Test that agent template has standard sections.

#### TestKnowledgeSchema
*Tests for knowledge schema pattern.*

- `test_schema_exists`
  - Test that knowledge schema exists.
- `test_schema_valid_json`
  - Test that schema is valid JSON.
- `test_schema_has_required_fields`
  - Test that schema has required fields defined.
- `test_schema_has_validation_rules`
  - Test that schema has validation rules.
- `test_schema_has_naming_convention`
  - Test that schema defines naming convention.

#### TestTemplateConsistency
*Tests for consistency across templates.*

- `test_all_factory_templates_exist`
  - Test that all expected factory templates exist.
- `test_templates_use_consistent_placeholder_style`
  - Test that templates use consistent placeholder style.

Templates can use either:
- Jinja2 style: {{ lowercase_variable }}
- Legacy style: {{UPPERCASE_PLACEHOLDER}}

### tests\validation\test_knowledge_schema.py

*Schema validation tests for knowledge files.

Tests validate that knowledge JSON files conform to expected structure.*

#### TestKnowledgeFilesStructure
*Tests for knowledge file structure.*

- `test_all_knowledge_files_valid_json`
  - Test that all knowledge files are valid JSON.
- `test_knowledge_files_have_content`
  - Test that knowledge files are not empty.

#### TestSkillCatalogSchema
*Tests for skill catalog schema validation.*

- `test_skill_catalog_exists`
  - Test that skill-catalog.json exists.
- `test_skill_catalog_valid`
  - Test that skill catalog is valid against schema.
- `test_skill_catalog_has_skills`
  - Test that skill catalog has skills defined.
- `test_skill_ids_match_keys`
  - Test that skill IDs match their dictionary keys.
- `test_skills_have_categories`
  - Test that all skills have valid categories.

#### TestStackCapabilitiesSchema
*Tests for stack capabilities file.*

- `test_stack_capabilities_exists`
  - Test that stack-capabilities.json exists.
- `test_stack_capabilities_valid_json`
  - Test that stack capabilities is valid JSON.

#### TestWorkflowPatternsSchema
*Tests for workflow patterns file.*

- `test_workflow_patterns_exists`
  - Test that workflow-patterns.json exists.
- `test_workflow_patterns_valid_json`
  - Test that workflow patterns is valid JSON.

#### TestBestPracticesSchema
*Tests for best practices file.*

- `test_best_practices_exists`
  - Test that best-practices.json exists.
- `test_best_practices_valid_json`
  - Test that best practices is valid JSON.

#### TestKnowledgeFileNaming
*Tests for knowledge file naming conventions.*

- `test_knowledge_files_use_kebab_case`
  - Test that knowledge files use kebab-case naming.
- `test_knowledge_files_have_json_extension`
  - Test that knowledge files have .json extension.

#### TestMCPServersCatalogSchema
*Tests for MCP servers catalog comprehensive structure.*

- `test_mcp_catalog_exists`
  - Test that mcp-servers-catalog.json exists.
- `test_mcp_catalog_valid_json`
  - Test that MCP catalog is valid JSON.
- `test_mcp_catalog_has_servers`
  - Test that MCP catalog has servers defined.
- `test_mcp_catalog_has_categories`
  - Test that MCP catalog defines categories.
- `test_mcp_catalog_has_starter_packs`
  - Test that MCP catalog has starter packs.
- `test_mcp_catalog_servers_have_required_fields`
  - Test that MCP servers have required fields.
- `test_mcp_catalog_server_categories_are_valid`
  - Test that all server categories reference defined categories.
- `test_mcp_catalog_has_role_based_recommendations`
  - Test that MCP catalog has role-based server recommendations.

#### TestMCPSelectionGuideSchema
*Tests for MCP selection guide structure.*

- `test_selection_guide_exists`
  - Test that mcp-selection-guide.json exists.
- `test_selection_guide_valid_json`
  - Test that selection guide is valid JSON.
- `test_selection_guide_has_flow`
  - Test that selection guide has selection flow defined.
- `test_selection_guide_has_role_mappings`
  - Test that selection guide has role-to-server mappings.
- `test_selection_guide_has_category_descriptions`
  - Test that selection guide has category descriptions.

#### TestAISuiteIntegrationSchema
*Tests for AISuite integration guide structure.*

- `test_aisuite_integration_exists`
  - Test that aisuite-integration.json exists.
- `test_aisuite_integration_valid_json`
  - Test that AISuite integration is valid JSON.
- `test_aisuite_integration_has_overview`
  - Test that AISuite integration has overview section.
- `test_aisuite_integration_has_providers`
  - Test that AISuite integration lists supported providers.
- `test_aisuite_integration_has_mcp_section`
  - Test that AISuite integration documents MCP client support.

### tests\validation\test_pattern_schema.py

*Schema validation tests for pattern files.

Tests validate that agent and skill patterns conform to expected structure.*

#### TestAgentPatternSchema
*Tests for agent pattern schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_all_agent_patterns_valid`
  - Test that all agent patterns are valid against schema.
- `test_code_reviewer_pattern_valid`
  - Test that code-reviewer pattern is valid.
- `test_agent_pattern_ids_are_kebab_case`
  - Test that agent pattern IDs use kebab-case.
- `test_agent_frontmatter_type_is_agent`
  - Test that agent frontmatter type is 'agent'.

#### TestSkillPatternSchema
*Tests for skill pattern schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_all_skill_patterns_valid`
  - Test that all skill patterns are valid against schema.
- `test_bugfix_workflow_pattern_valid`
  - Test that bugfix-workflow pattern is valid.
- `test_skill_pattern_ids_are_kebab_case`
  - Test that skill pattern IDs use kebab-case.
- `test_skill_frontmatter_type_is_skill`
  - Test that skill frontmatter type is 'skill'.

#### TestPatternConsistency
*Tests for pattern file consistency.*

- `test_pattern_id_matches_filename`
  - Test that patternId matches the filename.
- `test_frontmatter_name_matches_pattern_id`
  - Test that frontmatter name matches pattern ID.

### tests\validation\test_pm_schema.py

*Schema validation tests for PM system files.

Tests validate that PM product, questionnaire, adapters, defaults, and metrics
files conform to expected structure.*

#### TestPMProductSchema
*Tests for PM product schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_product_json_is_valid_json`
  - Test that product.json is valid JSON.
- `test_product_has_required_fields`
  - Test that product.json has all required fields.
- `test_backends_are_valid_list`
  - Test that backends field is a valid list.
- `test_methodologies_are_valid_list`
  - Test that methodologies field is a valid list.

#### TestQuestionnaireSchema
*Tests for questionnaire schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_questionnaire_is_valid_json`
  - Test that questionnaire.json is valid JSON.
- `test_questionnaire_has_questions`
  - Test that questionnaire has questions field.
- `test_questions_have_required_fields`
  - Test that all questions have required fields.

#### TestAdapterInterfaceSchema
*Tests for adapter interface schema validation.*

- `test_interface_is_valid_json`
  - Test that adapter-interface.json is valid JSON.
- `test_interface_has_operations`
  - Test that interface defines all required operations.
- `test_operations_have_parameters`
  - Test that operations have parameters defined in schema.

#### TestBackendAdaptersSchema
*Tests for backend adapter schema validation.*

- `test_schema_is_valid`
  - Test that the backend adapter schema itself is valid.
- `test_all_adapters_valid_json`
  - Test that all adapter files are valid JSON.
- `test_adapters_have_mappings`
  - Test that all adapters define mappings.
- `test_adapters_implement_interface_operations`
  - Test that adapters define mappings for all required interface operations.

#### TestMethodologyDefaultsSchema
*Tests for methodology defaults schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_all_defaults_valid_json`
  - Test that all defaults files are valid JSON.
- `test_defaults_have_required_fields`
  - Test that all defaults have required fields.

#### TestMetricsSchema
*Tests for metrics schema validation.*

- `test_schema_is_valid`
  - Test that the schema itself is valid.
- `test_metrics_is_valid_json`
  - Test that pm-metrics.json is valid JSON.
- `test_metrics_have_required_fields`
  - Test that all metrics have required fields.
- `test_all_categories_covered`
  - Test that all metric categories are covered.

### tests\validation\test_readme_structure.py

*README project structure validation tests.

Tests validate that the project structure documented in README.md
accurately reflects the actual filesystem structure.

This ensures documentation stays synchronized with the codebase
as the project evolves, catching drift before it reaches production.*

#### TestReadmeExists
*Tests for README.md file existence and basic structure.*

- `test_readme_exists`
  - Test that README.md exists in project root.
- `test_readme_has_content`
  - Test that README.md has content.
- `test_readme_has_project_structure_section`
  - Test that README.md has a Project Structure section.

#### TestReadmeStructureCounts
*Tests for README project structure count accuracy.*

- `test_readme_structure_counts_match_filesystem`
  - Test that all README counts match actual filesystem.
- `test_readme_agents_count`
  - Test that agents count in README matches filesystem.
- `test_readme_skills_count`
  - Test that skills count in README matches filesystem.
- `test_readme_blueprints_count`
  - Test that blueprints count in README matches filesystem.
- `test_readme_patterns_count`
  - Test that patterns count in README matches filesystem.
- `test_readme_knowledge_count`
  - Test that knowledge files count in README matches filesystem.
- `test_readme_templates_count`
  - Test that templates count in README matches filesystem.

#### TestStructureValidatorFunctionality
*Tests for StructureValidator class functionality.*

- `test_scan_agents_returns_dict`
  - Test that scan_agents returns expected structure.
- `test_scan_skills_returns_dict`
  - Test that scan_skills returns expected structure.
- `test_scan_blueprints_returns_dict`
  - Test that scan_blueprints returns expected structure.
- `test_scan_patterns_returns_dict`
  - Test that scan_patterns returns expected structure.
- `test_scan_knowledge_returns_dict`
  - Test that scan_knowledge returns expected structure.
- `test_scan_templates_returns_dict`
  - Test that scan_templates returns expected structure.
- `test_scan_all_returns_complete_structure`
  - Test that scan_all returns all component categories.
- `test_generate_counts_summary`
  - Test that generate_counts_summary returns integer counts.
- `test_extract_readme_counts`
  - Test that extract_readme_counts parses README correctly.
- `test_validate_returns_tuple`
  - Test that validate returns expected tuple structure.

#### TestProjectComponentsExist
*Tests to verify expected project components exist.*

- `test_agents_directory_exists`
  - Test that .agent/agents directory exists.
- `test_skills_directory_exists`
  - Test that .agent/skills directory exists.
- `test_blueprints_directory_exists`
  - Test that blueprints directory exists.
- `test_patterns_directory_exists`
  - Test that patterns directory exists.
- `test_knowledge_directory_exists`
  - Test that knowledge directory exists.
- `test_templates_directory_exists`
  - Test that templates directory exists.
- `test_has_minimum_agents`
  - Test that project has at least some agents defined.
- `test_has_minimum_skills`
  - Test that project has at least some skills defined.
- `test_has_minimum_blueprints`
  - Test that project has at least some blueprints defined.

### tests\validation\test_taxonomy_schema.py

*Validation tests for taxonomy file structure.

Tests validate that taxonomy JSON files conform to expected structure.*

#### TestAgentTaxonomyStructure
*Tests for agent taxonomy file structure.*

- `test_taxonomy_file_exists`
  - Test that agent_taxonomy.json exists.
- `test_taxonomy_valid_json`
  - Test that taxonomy file is valid JSON.
- `test_has_required_fields`
  - Test that taxonomy has required top-level fields.
- `test_has_domains`
  - Test that taxonomy has domains defined.
- `test_domains_have_topics`
  - Test that domains have topics or subtopics.
- `test_topics_have_required_depth`
  - Test that topics define required_depth.
- `test_keywords_are_lists`
  - Test that keywords fields are lists of strings.
- `test_knowledge_files_are_lists`
  - Test that knowledge_files fields are lists of strings.

#### TestTaxonomyMetadata
*Tests for taxonomy metadata section.*

- `test_has_version`
  - Test that taxonomy has version field.
- `test_has_metadata`
  - Test that taxonomy has metadata section.
- `test_has_coverage_scale`
  - Test that metadata defines coverage scale.
- `test_coverage_scale_has_levels`
  - Test that coverage scale defines levels 0-3.

### tests\validation\test_value_propagation.py

*Value propagation validation tests.

Tests validate that value propagation features are correctly implemented:
- All blueprints have required standard agents and skills
- Pattern files exist and are valid
- Pattern schemas are correct
- Generation script includes standard lists and checks*

#### TestBlueprintCompleteness
*Tests for blueprint completeness - all required agents and skills.*

- `test_all_blueprints_have_knowledge_extender_agent`
  - Test that all 27 blueprints have knowledge-extender agent.
- `test_all_blueprints_have_knowledge_evolution_agent`
  - Test that all 27 blueprints have knowledge-evolution agent.
- `test_all_blueprints_have_debug_conductor_project_agent`
  - Test that all 27 blueprints have debug-conductor-project agent.
- `test_all_blueprints_have_grounding_verification_skill`
  - Test that all 27 blueprints have grounding-verification skill.
- `test_all_blueprints_have_alignment_check_skill`
  - Test that all 27 blueprints have alignment-check skill.
- `test_all_blueprints_have_research_first_project_skill`
  - Test that all 27 blueprints have research-first-project skill.
- `test_all_blueprints_have_ci_monitor_project_skill`
  - Test that all 27 blueprints have ci-monitor-project skill.
- `test_all_blueprints_have_pipeline_error_fix_project_skill`
  - Test that all 27 blueprints have pipeline-error-fix-project skill.
- `test_all_blueprints_have_pm_integration_section`
  - Test that all 27 blueprints have pmIntegration section.
- `test_all_blueprints_have_all_standard_agents`
  - Test that all blueprints have all standard agents.
- `test_all_blueprints_have_all_standard_skills`
  - Test that all blueprints have all standard skills.

#### TestPatternFileExistence
*Tests for pattern file existence and validity.*

- `test_debug_conductor_project_pattern_exists`
  - Test that patterns/agents/debug-conductor-project.json exists and is valid JSON.
- `test_knowledge_extender_pattern_exists`
  - Test that patterns/agents/knowledge-extender.json exists and is valid JSON.
- `test_knowledge_evolution_pattern_exists`
  - Test that patterns/agents/knowledge-evolution.json exists and is valid JSON.
- `test_grounding_verification_pattern_exists`
  - Test that patterns/skills/grounding-verification.json exists and is valid JSON.
- `test_alignment_check_pattern_exists`
  - Test that patterns/skills/alignment-check.json exists and is valid JSON.
- `test_research_first_project_pattern_exists`
  - Test that patterns/skills/research-first-project.json exists and is valid JSON.
- `test_ci_monitor_project_pattern_exists`
  - Test that patterns/skills/ci-monitor-project.json exists and is valid JSON.
- `test_pipeline_error_fix_project_pattern_exists`
  - Test that patterns/skills/pipeline-error-fix-project.json exists and is valid JSON.
- `test_all_agent_patterns_exist`
  - Test that all expected agent pattern files exist and are valid JSON.
- `test_all_skill_patterns_exist`
  - Test that all expected skill pattern files exist and are valid JSON.

#### TestPatternSchemaValidation
*Tests for pattern schema validation.*

- `test_patterns_have_required_metadata`
  - Test that each pattern has required metadata fields.
- `test_patterns_have_frontmatter_with_name_and_description`
  - Test that each pattern has frontmatter with name and description.
- `test_patterns_have_sections`
  - Test that each pattern has sections.

#### TestGenerationScriptValidation
*Tests for generation script validation.*

- `test_generate_project_includes_standard_agents_list`
  - Test that scripts/core/generate_project.py includes standard_agents list.
- `test_generate_project_includes_standard_skills_list`
  - Test that scripts/core/generate_project.py includes standard_skills list.
- `test_generate_project_checks_pm_integration_enabled`
  - Test that scripts/core/generate_project.py checks pmIntegration.enabled.
- `test_generate_project_adds_standard_agents`
  - Test that generate_project.py adds standard agents to agents list.
- `test_generate_project_adds_standard_skills`
  - Test that generate_project.py adds standard skills to skills list.

### tests\validation\test_workflow_structure.py

*Workflow structure validation tests.

Tests validate that workflow markdown files follow the established structure
with proper sections, phases, and documentation.*

#### TestWorkflowStructure
*Tests for workflow markdown structure validation.*

- `test_workflows_directory_exists`
  - Test that workflows directory exists.
- `test_workflow_files_exist`
  - Test that workflow files exist.
- `test_minimum_workflow_count`
  - Test that we have the expected minimum number of workflows.
- `test_all_workflows_have_title`
  - Test that all workflows have a markdown title.
- `test_all_workflows_have_overview`
  - Test that all workflows have an Overview section.
- `test_all_workflows_have_trigger_conditions`
  - Test that all workflows have Trigger Conditions section.
- `test_all_workflows_have_phases`
  - Test that all workflows have Phases section.
- `test_all_workflows_have_decision_points`
  - Test that all workflows have Decision Points section.
- `test_all_workflows_have_example_session`
  - Test that all workflows have an Example Session section.
- `test_workflow_naming_convention`
  - Test that workflow files use kebab-case naming.

#### TestWorkflowCategories
*Tests for workflow organization by category.*

- `test_universal_workflows_exist`
  - Test that universal workflows exist.
- `test_quality_workflows_exist`
  - Test that quality workflows exist.
- `test_agile_workflows_exist`
  - Test that agile workflows exist.
- `test_operations_workflows_exist`
  - Test that operations workflows exist.
- `test_domain_workflows_exist`
  - Test that domain-specific workflow directories exist.

#### TestWorkflowContent
*Tests for workflow content quality.*

- `test_workflows_have_version`
  - Test that workflows declare a version.
- `test_workflows_have_trigger_examples`
  - Test that workflows provide trigger examples.
- `test_workflows_have_fallback_procedures`
  - Test that workflows have fallback procedures.
- `test_no_broken_internal_links`
  - Test that workflows don't have obviously broken links.

#### TestWorkflowIntegration
*Tests for workflow integration with other components.*

- `test_workflow_patterns_json_exists`
  - Test that workflow-patterns.json exists and is valid JSON.
- `test_workflow_patterns_reference_workflows`
  - Test that workflow patterns reference existing workflows.
- `test_workflow_patterns_doc_exists`
  - Test that WORKFLOW_PATTERNS.md documentation exists.
