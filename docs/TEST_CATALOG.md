# Antigravity Agent Factory - Automated Test Catalog

This catalog is automatically generated and maintained by the unified artifact synchronization system. 
It provides a comprehensive list of all test cases in the repository, their locations, and their documented purposes.

> [!NOTE]
> Do not edit the content between the SYNC markers manually, as it will be overwritten 
> the next time `scripts/validation/sync_artifacts.py --sync` is run.

## Test Cases

<!-- SYNC_START -->
| File | Class | Test Case | Description |
| --- | --- | --- | --- |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_agentrules_is_protected` | CRITICAL: Verify .agentrules cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_axiom_zero_is_protected` | CRITICAL: Verify axiom-zero.json cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_axioms_are_protected` | CRITICAL: Verify Layer 0 (Axioms) cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_blueprints_are_mutable` | Verify blueprints can be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_data_directory_is_mutable` | Verify data directory can be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_enforcement_patterns_are_protected` | CRITICAL: Verify enforcement patterns cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_get_all_protected_paths` | Test getting all protected paths. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_get_layer_info` | Test getting layer information. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_get_protection_summary` | Test getting protection summary. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_knowledge_files_are_mutable` | Verify knowledge files can be extended. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_path_with_backslashes` | Test Windows-style paths are handled. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_path_with_dot_prefix` | Test paths with ./ prefix are handled. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_principles_are_protected` | CRITICAL: Verify Layer 2 (Principles) cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_purpose_is_protected` | CRITICAL: Verify Layer 1 (Purpose) cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_purpose_patterns_are_protected` | CRITICAL: Verify patterns/purpose/ cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_quality_standards_are_protected` | CRITICAL: Verify quality standards cannot be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_stack_patterns_are_mutable` | Verify stack patterns can be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_templates_are_mutable` | Verify templates can be modified. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_valid_modification_passes` | Test that valid modifications pass. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_validate_modification_checks_content` | Test that content is validated for violations. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuard | `test_validate_modification_checks_path_first` | Test that path is checked before content. |
| [test_mutability_guard.py](file:///tests/guardian/test_mutability_guard.py) | TestMutabilityGuardSingleton | `test_get_mutability_guard_returns_instance` | Test singleton returns an instance. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestAxiomIntegrity | `test_core_axioms_file_has_correct_structure` | Verify core-axioms.json has the expected structure. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestAxiomIntegrity | `test_never_modify_list_includes_critical_files` | Verify NEVER_MODIFY list includes all critical files. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_axiom_files_not_in_mutable_paths` | Verify that axiom files are not accidentally in mutable paths. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_axioms_unchanged_after_learning` | CRITICAL: Verify axioms remain identical after learning cycles. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_guard_blocks_all_layer0_modifications` | Verify that ALL Layer 0 paths are blocked. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_guard_blocks_all_layer1_modifications` | Verify that ALL Layer 1 paths are blocked. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_guard_blocks_all_layer2_modifications` | Verify that ALL Layer 2 paths are blocked. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_induction_engine_respects_guard` | Verify that InductionEngine uses the guard correctly. |
| [test_no_axiom_drift.py](file:///tests/guardian/test_no_axiom_drift.py) | TestNoAxiomDrift | `test_memory_store_does_not_touch_protected_files` | Verify MemoryStore only writes to its own directory. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestBlueprintGeneration | `test_blueprint_generation_invalid_blueprint` | Test that invalid blueprint ID fails. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestBlueprintGeneration | `test_blueprint_generation_requires_output` | Test that --blueprint without --output fails. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestBlueprintGeneration | `test_blueprint_generation_success` | Test successful blueprint generation. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestBlueprintGeneration | `test_blueprint_generation_with_name` | Test blueprint generation with custom project name. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestCLIErrorHandling | `test_conflicting_arguments` | Test handling of conflicting arguments (blueprint and config together). |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestCLIErrorHandling | `test_no_arguments_shows_help` | Test that running without arguments shows help. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestCLIHelp | `test_help_exits_successfully` | Test that --help exits with code 0. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestCLIHelp | `test_help_shows_commands` | Test that --help shows available commands. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestCLIHelp | `test_version_shows_version` | Test that --version shows version information. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestConfigGeneration | `test_config_generation_from_json` | Test generation from JSON config file. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestConfigGeneration | `test_config_generation_from_yaml` | Test generation from YAML config file. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestConfigGeneration | `test_config_generation_missing_file` | Test that missing config file fails. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestConfigGeneration | `test_config_generation_requires_output` | Test that --config without --output fails. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListBlueprints | `test_list_blueprints_exits_successfully` | Test that --list-blueprints exits with code 0. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListBlueprints | `test_list_blueprints_shows_all_blueprints` | Test that multiple blueprints are shown. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListBlueprints | `test_list_blueprints_shows_metadata` | Test that blueprint metadata is shown. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListBlueprints | `test_list_blueprints_shows_python_fastapi` | Test that python-fastapi blueprint is listed. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListPatterns | `test_list_patterns_exits_successfully` | Test that --list-patterns exits with code 0. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListPatterns | `test_list_patterns_shows_categories` | Test that pattern categories are shown. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestListPatterns | `test_list_patterns_shows_patterns` | Test that individual patterns are listed. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_help_shows_quickstart_option` | Test that --help shows the --quickstart option. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_creates_agentrules` | Test that --quickstart creates .agentrules file. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_creates_agents_directory` | Test that --quickstart creates .agent/agents/ directory. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_creates_readme` | Test that --quickstart creates README.md file. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_creates_skills_directory` | Test that --quickstart creates .agent/skills/ directory. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_default_output_directory` | Test that --quickstart uses ./quickstart-demo as default output. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_exits_successfully` | Test that --quickstart generates a project successfully. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_shows_congratulations` | Test that --quickstart shows celebration message on success. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_shows_next_steps` | Test that --quickstart shows guidance for next steps. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_shows_welcome_message` | Test that --quickstart shows warm welcome message. |
| [test_cli.py](file:///tests/integration/test_cli.py) | TestQuickStart | `test_quickstart_with_custom_blueprint` | Test that --quickstart-blueprint overrides default blueprint. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestAnalyzeGapsCommand | `test_analyze_gaps_exits_successfully` | Test that --analyze-gaps exits with code 0. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestAnalyzeGapsCommand | `test_analyze_gaps_shows_coverage` | Test that --analyze-gaps shows coverage information. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestAnalyzeGapsCommand | `test_analyze_gaps_shows_gap_types` | Test that output shows gap types. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestAnalyzeGapsCommand | `test_analyze_gaps_with_scope_domain` | Test --analyze-gaps with domain scope. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestAnalyzeGapsCommand | `test_analyze_gaps_with_scope_topic` | Test --analyze-gaps with topic scope. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestCoverageReportCommand | `test_coverage_report_exits_successfully` | Test that --coverage-report exits with code 0. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestCoverageReportCommand | `test_coverage_report_shows_percentage` | Test that coverage report shows percentage. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestHelpExtensionCommands | `test_help_shows_analyze_gaps` | Test that help shows --analyze-gaps option. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestHelpExtensionCommands | `test_help_shows_coverage_report` | Test that help shows --coverage-report option. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestSuggestExtensionsCommand | `test_suggest_extensions_exits_successfully` | Test that --suggest-extensions exits with code 0. |
| [test_cli_extension.py](file:///tests/integration/test_cli_extension.py) | TestSuggestExtensionsCommand | `test_suggest_extensions_lists_candidates` | Test that suggest-extensions lists extension candidates. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMBackendValidation | `test_valid_pm_backends_accepted` | Test that valid PM backends are accepted. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMBackendValidation | `test_valid_pm_methodologies_accepted` | Test that valid PM methodologies are accepted. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMBlueprintGeneration | `test_pm_disabled_no_pm_artifacts` | Test that without --pm-enabled, PM artifacts are not generated. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMBlueprintGeneration | `test_pm_enabled_config_recognized` | Test that PM config is recognized in output. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMBlueprintGeneration | `test_pm_enabled_runs_successfully` | Test that --pm-enabled runs without errors. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMHelpOutput | `test_help_shows_pm_backend_flag` | Test that --help shows --pm-backend flag. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMHelpOutput | `test_help_shows_pm_doc_backend_flag` | Test that --help shows --pm-doc-backend flag. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMHelpOutput | `test_help_shows_pm_enabled_flag` | Test that --help shows --pm-enabled flag. |
| [test_cli_pm.py](file:///tests/integration/test_cli_pm.py) | TestPMHelpOutput | `test_help_shows_pm_methodology_flag` | Test that --help shows --pm-methodology flag. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestExtensionCandidates | `test_candidates_filter_by_priority` | Test that candidates can be filtered by minimum priority. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestExtensionCandidates | `test_candidates_respect_max_limit` | Test that max_candidates limit is respected. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestExtensionCandidates | `test_candidates_sorted_by_priority` | Test that candidates are sorted by priority. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestExtensionCandidates | `test_get_candidates_returns_gaps` | Test that get_extension_candidates returns gaps. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestGapAnalysisWorkflow | `test_analysis_identifies_coverage` | Test that analysis correctly identifies coverage. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestGapAnalysisWorkflow | `test_analysis_produces_gaps` | Test that analysis produces gap findings. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestGapAnalysisWorkflow | `test_analysis_result_serialization` | Test that analysis result can be serialized to JSON. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestGapAnalysisWorkflow | `test_analysis_with_mock_knowledge` | Test analysis with controlled mock knowledge. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestGapAnalysisWorkflow | `test_full_analysis_workflow` | Test complete analysis workflow from start to finish. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestRunGapAnalysisFunction | `test_run_gap_analysis_custom_dir` | Test run_gap_analysis with custom directory. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestRunGapAnalysisFunction | `test_run_gap_analysis_default_dir` | Test run_gap_analysis with default knowledge directory. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestTaxonomyIntegration | `test_load_agent_taxonomy_integration` | Test loading the default agent taxonomy. |
| [test_gap_analysis_e2e.py](file:///tests/integration/test_gap_analysis_e2e.py) | TestTaxonomyIntegration | `test_taxonomy_has_substantial_content` | Test that taxonomy has substantial content for analysis. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestBlueprintGeneration | `test_blueprint_generates_knowledge_files` | Test that knowledge files are copied from factory. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestBlueprintGeneration | `test_python_fastapi_blueprint_generation` | Test generation from python-fastapi blueprint. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFileTracking | `test_all_files_tracked` | Test that all generated files are tracked. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFileTracking | `test_file_count_matches_tracked` | Test that file count matches tracked files. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFullProjectGeneration | `test_generate_creates_agentrules` | Test that .agentrules is created with correct content. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFullProjectGeneration | `test_generate_creates_agents` | Test that agent files are created when specified. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFullProjectGeneration | `test_generate_creates_complete_structure` | Test that generation creates complete directory structure. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFullProjectGeneration | `test_generate_creates_readme` | Test that README.md is created with correct content. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestFullProjectGeneration | `test_generate_creates_skills` | Test that skill files are created when specified. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestGeneratedContentValidation | `test_agent_markdown_has_frontmatter` | Test that generated agent files have YAML frontmatter. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestGeneratedContentValidation | `test_agentrules_has_mcp_section_when_configured` | Test that .agentrules has MCP section when servers configured. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestGeneratedContentValidation | `test_skill_markdown_has_process_section` | Test that generated skill files have process section. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestGeneratedContentValidation | `test_templates_are_created` | Test that template files are created. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestGenerationErrors | `test_missing_agent_pattern_warning` | Test that missing agent patterns are handled gracefully. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestGenerationErrors | `test_missing_skill_pattern_warning` | Test that missing skill patterns are handled gracefully. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestWorkflowGeneration | `test_bugfix_workflow_created_with_jira_trigger` | Test that bugfix workflow is created when jira trigger is specified. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestWorkflowGeneration | `test_feature_workflow_created_with_confluence_trigger` | Test that feature workflow is created when confluence trigger is specified. |
| [test_generation.py](file:///tests/integration/test_generation.py) | TestWorkflowGeneration | `test_workflows_readme_created` | Test that workflows README is created. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianAxiomAlignment | `test_consistency_a5_flagged` | A5 (Consistency) violations should be identified. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianAxiomAlignment | `test_non_harm_a4_flagged` | A4 (Non-Harm) violations should be clearly identified. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianAxiomAlignment | `test_transparency_a3_flagged` | A3 (Transparency) violations should be identified. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianAxiomAlignment | `test_verifiability_a1_flagged` | A1 (Verifiability) violations should be identified. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntegrationPoints | `test_check_result_has_required_fields` | CheckResult should have all fields needed for UI. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntegrationPoints | `test_comprehensive_check_combines_all` | Comprehensive check should find issues from all sources. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_0_normal_file_operations_continue` | Normal file operations should continue without intervention. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_0_safe_command_returns_flow` | Safe commands should return Level 0 (Flow) - no intervention. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_2_caution_file_modifications_pause` | Modifying caution-worthy files should pause. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_2_sensitive_file_pauses` | Accessing sensitive files should pause and ask user. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_3_harmful_content_blocks` | Content with harmful patterns should block with explanation. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_3_medium_secrets_require_confirmation` | Medium severity secrets should block and require confirmation. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_4_destructive_commands_protect` | Destructive commands must be prevented immediately. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianIntendedBehavior | `test_level_4_high_severity_secrets_protect` | High severity secrets (API keys) must be prevented. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianMessaging | `test_block_messages_include_explanation` | Block (Level 3) should explain what was detected. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianMessaging | `test_block_messages_include_recommendations` | Block (Level 3) should provide guidance, not just reject. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianMessaging | `test_caution_messages_are_informative` | Caution (Level 2) messages should explain the concern. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianNoFalsePositives | `test_documentation_examples_not_blocked` | Documentation with example secrets should not be blocked. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianNoFalsePositives | `test_drop_table_if_exists_safer` | DROP TABLE IF EXISTS is safer than raw DROP. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianNoFalsePositives | `test_rm_with_specific_file_not_blocked` | 'rm' with specific safe file should not trigger Level 4. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianNoFalsePositives | `test_test_files_not_blocked` | Test files with example secrets should not be blocked. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianRealWorldScenarios | `test_accidental_env_commit_detected` | Scenario: Developer about to commit .env file content. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianRealWorldScenarios | `test_copy_paste_secret_detected` | Scenario: Developer pastes API key directly in code. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianRealWorldScenarios | `test_dangerous_sql_detected` | Scenario: Dangerous SQL in code review. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianRealWorldScenarios | `test_safe_placeholder_not_blocked` | Scenario: Developer uses placeholder correctly. |
| [test_guardian_behavior.py](file:///tests/integration/test_guardian_behavior.py) | TestGuardianRealWorldScenarios | `test_safe_sql_passes` | Scenario: Safe SQL with proper filtering. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianActuallyPreventsHarm | `test_guardian_allows_safe_operations` | Guardian must ALLOW safe operations to proceed. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianActuallyPreventsHarm | `test_guardian_blocks_even_with_user_confirmation` | Level 4 actions are blocked even if user tries to confirm. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianActuallyPreventsHarm | `test_guardian_blocks_rm_rf_root` | CRITICAL: Guardian must BLOCK 'rm -rf /' - not just detect it. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianActuallyPreventsHarm | `test_guardian_blocks_secret_in_file_write` | Guardian must BLOCK writing files containing secrets. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianEndToEnd | `test_developer_workflow_with_guardian` | Simulate a typical developer workflow with Guardian protection. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianPauseRequiresConfirmation | `test_agentrules_modification_requires_confirmation` | Modifying .agentrules requires confirmation. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianPauseRequiresConfirmation | `test_sensitive_file_requires_confirmation` | Accessing .env requires user confirmation to proceed. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianPreCommitScenario | `test_commit_with_secrets_blocked` | Commit containing secrets should be BLOCKED. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianPreCommitScenario | `test_commit_without_secrets_allowed` | Clean commit should be ALLOWED. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianPreCommitScenario | `test_env_file_in_commit_blocked` | Committing .env content should be blocked. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianStatistics | `test_guardian_blocking_rate` | Measure what percentage of harmful actions are blocked. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianStatistics | `test_guardian_false_positive_rate` | Measure false positive rate on safe actions. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianWithRealFiles | `test_safe_file_creation_allowed` | Test that creating safe files is allowed. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianWithRealFiles | `test_secret_file_creation_blocked` | Test that creating a file with secrets is blocked. |
| [test_guardian_real_effect.py](file:///tests/integration/test_guardian_real_effect.py) | TestGuardianWithRealFiles | `test_would_have_deleted_critical_file` | Verify Guardian would prevent critical file deletion. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestFactoryTemplateRendering | `test_agent_template_rendering` | Test rendering agent.md.tmpl with Jinja2 features. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestFactoryTemplateRendering | `test_guardian_protocol_template` | Test rendering guardian-protocol.json.tmpl. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestFactoryTemplateRendering | `test_skill_template_rendering` | Test rendering skill.md.tmpl with Jinja2 features. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestLegacyPlaceholderSupport | `test_curly_brace_placeholder` | Test single-curly-brace placeholders in context. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestLegacyPlaceholderSupport | `test_mixed_placeholders` | Test mixing legacy and Jinja2 syntax. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestLegacyPlaceholderSupport | `test_uppercase_placeholder` | Test uppercase placeholder conversion. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestProjectGeneratorWithTemplates | `test_build_template_context` | Test building template context from config. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestProjectGeneratorWithTemplates | `test_generator_has_template_engine` | Test that generator initializes template engine. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithConditionals | `test_if_else` | Test if-else statement. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithConditionals | `test_if_with_list_check` | Test if with list existence check. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithConditionals | `test_optional_section` | Test optional section based on variable presence. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithConditionals | `test_simple_if` | Test simple if statement. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithFilters | `test_case_conversion_in_template` | Test case conversion filters in template context. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithFilters | `test_code_block_in_template` | Test wrap_code filter in template context. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithFilters | `test_pluralize_in_template` | Test pluralize filter in template context. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithLoops | `test_dict_iteration` | Test iterating over a dictionary. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithLoops | `test_list_iteration` | Test iterating over a list. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithLoops | `test_loop_with_index` | Test using loop.index. |
| [test_template_rendering.py](file:///tests/integration/test_template_rendering.py) | TestTemplateWithLoops | `test_table_generation` | Test generating a markdown table. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestAxiomConsistency | `test_all_five_axioms_present` | Test that all 5 core axioms are present in .agentrules. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestAxiomConsistency | `test_axiom_meanings_present` | Test that axiom meanings are explained. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestAxiomConsistency | `test_guardian_protocol_axioms_match` | Test that guardian-protocol.json axioms match .agentrules. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_agentrules_has_axiom_zero` | Test that generated .agentrules contains Axiom Zero. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_agentrules_has_eternal_values` | Test that generated .agentrules contains eternal values. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_agentrules_has_wu_wei` | Test that generated .agentrules contains Wu Wei protocol. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_generated_project_is_complete` | Test that generated project has all required components. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_guardian_protocol_has_daily_intention` | Test that guardian-protocol.json contains daily intention. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_guardian_protocol_has_unity` | Test that guardian-protocol.json contains unity statement. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_guardian_protocol_has_values` | Test that guardian-protocol.json contains eternal values. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestValueTransmission | `test_values_are_not_empty_strings` | Test that value descriptions are meaningful, not empty. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestWuWeiProtocol | `test_five_levels_present` | Test that all 5 Wu Wei levels are present. |
| [test_value_transmission.py](file:///tests/integration/test_value_transmission.py) | TestWuWeiProtocol | `test_wu_wei_in_guardian_protocol` | Test that Wu Wei is in guardian-protocol.json. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_batch_similarity` | Test batch similarity matrix. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_dissimilar_texts_have_low_similarity` | Verify dissimilar content is distinguished. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_embedding_multiple_texts` | Test embedding multiple texts at once. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_embedding_produces_vectors` | Verify embeddings are generated correctly. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_embedding_single_text` | Test embed_single method. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_empty_input_handling` | Test handling of empty inputs. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_get_status` | Test status reporting. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_is_similar_returns_boolean` | Test is_similar method. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_most_similar_returns_top_k` | Test most_similar method returns correct number of results. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_most_similar_with_threshold` | Test most_similar with threshold filtering. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_service_initialization` | Test that service initializes correctly with lazy loading. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_similar_texts_have_high_similarity` | Verify semantic similarity works for similar texts. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingService | `test_similarity_with_multiple_candidates` | Test similarity against multiple candidates. |
| [test_embedding_service.py](file:///tests/memory/test_embedding_service.py) | TestEmbeddingServiceSingleton | `test_get_embedding_service_returns_same_instance` | Test singleton returns same instance. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_accepted_proposal_is_stored` | Verify accepted proposals are stored correctly. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_different_observation_types` | Test different types of observations. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_edit_and_accept_proposal` | Test editing a proposal before accepting. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_engine_initialization` | Test that engine initializes correctly. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_get_status` | Test status reporting. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_get_status_message` | Test human-readable status message. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_observe_creates_proposal` | Test that observation creates a proposal. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_observe_returns_none_for_short_content` | Test that short content is rejected. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_proposal_requires_user_approval` | Verify memories are not stored without approval. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngine | `test_rejected_proposal_not_re_proposed` | Verify rejected memories are not proposed again. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngineSession | `test_end_session_clears_observations` | Test ending session clears observation list. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngineSession | `test_end_session_stores_episodic` | Test ending session stores episodic memories. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngineSession | `test_session_tracks_observations` | Test that observations are tracked in session. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngineSession | `test_start_session` | Test starting a new session. |
| [test_induction_engine.py](file:///tests/memory/test_induction_engine.py) | TestInductionEngineSingleton | `test_get_induction_engine_returns_instance` | Test singleton returns an instance. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryProposalOperations | `test_accept_proposal` | Test accepting a proposal moves it to semantic. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryProposalOperations | `test_accept_proposal_with_edit` | Test accepting with edited content. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryProposalOperations | `test_add_pending_proposal` | Test adding a pending proposal. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryProposalOperations | `test_is_similar_to_rejected` | Test similarity check against rejected proposals. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryProposalOperations | `test_proposal_format_for_user` | Test proposal formatting for display. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryProposalOperations | `test_reject_proposal` | Test rejecting a proposal moves it to rejected. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_add_and_search_memory` | Test adding and searching memories. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_add_memory_to_different_types` | Test adding memories to different collections. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_clear_episodic` | Test clearing episodic memories. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_delete_memory` | Test deleting a memory. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_get_memory_by_id` | Test retrieving a specific memory. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_get_relevant_context` | Test getting formatted context. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_search_with_threshold` | Test search with similarity threshold. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_status_message` | Test status message generation. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStore | `test_store_initialization` | Test that store initializes correctly. |
| [test_memory_store.py](file:///tests/memory/test_memory_store.py) | TestMemoryStoreSingleton | `test_get_memory_store_returns_same_instance` | Test singleton returns same instance. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestAdapterConfig | `test_custom_values` | Test custom configuration values. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestAdapterConfig | `test_default_values` | Test default configuration values. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestBaseAdapter | `test_caching` | Test cache methods. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestBaseAdapter | `test_concrete_implementation` | Test that concrete implementation works. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestBaseAdapter | `test_create_source` | Test create_source helper method. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestBaseAdapter | `test_repr` | Test string representation. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestGitHubAdapter | `test_import` | Test that GitHub adapter can be imported. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestGitHubAdapter | `test_tracked_repos` | Test that tracked repos are defined. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestKnowledgeChange | `test_creation` | Test creating a knowledge change. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestKnowledgeChange | `test_with_values` | Test change with old and new values. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestKnowledgeUpdate | `test_checksum_generation` | Test that checksum is generated for proposed content. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestKnowledgeUpdate | `test_creation` | Test creating a knowledge update. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestKnowledgeUpdate | `test_to_dict` | Test serialization to dictionary. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestNPMAdapter | `test_import` | Test that NPM adapter can be imported. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestNPMAdapter | `test_tracked_packages` | Test that tracked packages are defined. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestPyPIAdapter | `test_import` | Test that PyPI adapter can be imported. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestPyPIAdapter | `test_tracked_packages` | Test that tracked packages are defined. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestTrustLevel | `test_trust_levels` | Test trust level values. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestUpdatePriority | `test_priority_ordering` | Test that priorities are correctly ordered. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestUpdateSource | `test_creation` | Test creating an update source. |
| [test_adapters.py](file:///tests/unit/test_adapters.py) | TestUpdateSource | `test_default_timestamp` | Test that timestamp is set automatically. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupEntry | `test_backup_entry_creation` | Test creating a BackupEntry. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupEntry | `test_backup_entry_was_new_default` | Test BackupEntry default was_new value. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_cleanup_old_sessions` | Test cleaning up old sessions. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_create_session` | Test creating a backup session. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_format_backup_size` | Test formatting backup size. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_get_backup_size_empty` | Test getting backup size when empty. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_get_backup_size_with_files` | Test getting backup size with backed up files. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_get_session_by_id` | Test retrieving a session by ID. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_get_session_not_found` | Test retrieving non-existent session returns None. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_list_sessions_empty` | Test listing sessions when none exist. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_list_sessions_returns_manifests` | Test listing sessions returns manifest objects. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_manager_creation` | Test creating a BackupManager. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_rollback_already_rolled_back` | Test rolling back already rolled back session fails. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_rollback_session` | Test rolling back a session by ID. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManager | `test_rollback_session_not_found` | Test rolling back non-existent session fails. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManifest | `test_manifest_creation` | Test creating a BackupManifest. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManifest | `test_manifest_from_dict` | Test creating manifest from dictionary. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManifest | `test_manifest_roundtrip` | Test that manifest survives to_dict/from_dict roundtrip. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupManifest | `test_manifest_to_dict` | Test converting manifest to dictionary. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_backup_directory` | Test backing up a directory. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_backup_file_existing` | Test backing up an existing file. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_backup_file_marked_as_new` | Test marking a file as newly created. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_complete_marks_session_complete` | Test that complete() marks session as completed. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_rollback_deletes_new_files` | Test that rollback deletes newly created files. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_rollback_restores_files` | Test that rollback restores original file content. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestBackupSession | `test_session_creation` | Test creating a backup session. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestEnsureGitignoreExcludesBackup | `test_appends_to_existing_gitignore` | Test that function appends to existing .gitignore. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestEnsureGitignoreExcludesBackup | `test_creates_gitignore_if_missing` | Test that function creates .gitignore if it doesn't exist. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestEnsureGitignoreExcludesBackup | `test_does_not_duplicate_entry` | Test that function doesn't add duplicate entries. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestMainEntry | `test_format_backup_size_units` | Test format_backup_size with various sizes. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestMainEntry | `test_main_list_command` | Test main with list command by importing and calling the module code. |
| [test_backup_manager.py](file:///tests/unit/test_backup_manager.py) | TestMainEntry | `test_main_size_command` | Test backup size calculation. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerGetSet | `test_get_nested_value` | Test getting a nested configuration value. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerGetSet | `test_get_simple_value` | Test getting a simple configuration value. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerGetSet | `test_get_with_default` | Test getting a non-existent value with default. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerGetSet | `test_set_creates_path` | Test that set creates missing path components. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerGetSet | `test_set_value` | Test setting a configuration value. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerInitialization | `test_creates_default_settings` | Test that default settings are created when none exist. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerInitialization | `test_factory_root_detection` | Test that factory root is correctly detected. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerInitialization | `test_platform_detection` | Test that platform is detected. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestConfigManagerInitialization | `test_singleton_pattern` | Test that ConfigManager follows singleton pattern. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestCredentialManagement | `test_get_credential_resolves_env` | Test getting a credential resolves environment variable. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestCredentialManagement | `test_get_missing_credential_returns_none` | Test getting a missing credential returns None. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestEnvironmentVariableResolution | `test_missing_env_var_returns_empty` | Test that missing env vars resolve to empty string. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestEnvironmentVariableResolution | `test_partial_env_var_resolution` | Test resolving env var in a larger string. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestEnvironmentVariableResolution | `test_resolves_env_var` | Test that ${VAR} syntax is resolved. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestKnowledgeEvolutionConfig | `test_get_knowledge_evolution_config` | Test getting knowledge evolution configuration. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestKnowledgeEvolutionConfig | `test_knowledge_evolution_sources` | Test knowledge evolution sources configuration. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestLegacyMigration | `test_migrates_legacy_tools` | Test migration from legacy tools.json format. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestSettingsValidation | `test_validate_invalid_channel` | Test that invalid update channel is caught. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestSettingsValidation | `test_validate_invalid_mode` | Test that invalid mode is caught. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestSettingsValidation | `test_validate_valid_settings` | Test validating correct settings returns no errors. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestToolPathResolution | `test_get_tool_path_from_config` | Test tool path resolution from explicit config. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestToolPathResolution | `test_get_tool_path_from_env` | Test tool path resolution from environment variable. |
| [test_config_manager.py](file:///tests/unit/test_config_manager.py) | TestToolPathResolution | `test_get_tool_path_returns_none_for_unknown` | Test that unknown tool returns None. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestAnalyzeRepository | `test_analyze_valid_repository` | Test analyzing a valid repository. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestAnalyzeRepository | `test_analyze_with_artifacts` | Test analyzing repository with existing artifacts. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestCreateDefaultConfig | `test_creates_config_from_inventory` | Test creating config from inventory. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestDisplayErrorWithHelp | `test_prints_error_and_suggestion` | Test that error and suggestion are printed. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestDisplayTour | `test_prints_tour_info` | Test that tour information is printed. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestDisplayWelcome | `test_prints_welcome_message` | Test that welcome message is printed. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGenerateFromBlueprint | `test_generate_from_invalid_blueprint` | Test generating from non-existent blueprint. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGenerateFromBlueprint | `test_generate_from_valid_blueprint` | Test generating from a valid blueprint. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGenerateFromBlueprint | `test_generate_with_pm_enabled` | Test generating with PM system enabled. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGenerateFromBlueprint | `test_generate_with_project_name` | Test generating with custom project name. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGenerateFromConfigFile | `test_generate_from_json_config` | Test generating from JSON config file. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGenerateFromConfigFile | `test_generate_from_nonexistent_config` | Test generating from non-existent config file. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGetFactoryRoot | `test_contains_blueprints` | Test that factory root contains blueprints directory. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGetFactoryRoot | `test_path_exists` | Test that returned path exists. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestGetFactoryRoot | `test_returns_path` | Test that get_factory_root returns a Path. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestInteractiveConflictResolver | `test_resolver_returns_recommendation_on_empty_input` | Test resolver returns recommendation on empty input. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestInteractiveConflictResolver | `test_resolver_returns_selected_option` | Test resolver returns selected option. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestInteractiveMode | `test_interactive_mode_basic_flow` | Test basic interactive mode flow. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestInteractiveMode | `test_interactive_mode_cancel` | Test cancelling interactive mode. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestInteractiveMode | `test_interactive_mode_with_pm_enabled` | Test interactive mode with PM system enabled. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestListBlueprints | `test_lists_available_blueprints` | Test that blueprints are listed. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestListBlueprints | `test_shows_blueprint_details` | Test that blueprint details are shown. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestListPatterns | `test_lists_available_patterns` | Test that patterns are listed. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestListPatterns | `test_shows_pattern_categories` | Test that pattern categories are shown. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_analyze` | Test main with --analyze. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_blueprint_with_output` | Test main with --blueprint and --output. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_blueprint_without_output_fails` | Test main with --blueprint but no --output fails. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_list_blueprints` | Test main with --list-blueprints. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_list_patterns` | Test main with --list-patterns. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_no_args_shows_help` | Test main with no arguments shows help. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_quickstart` | Test main with --quickstart. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestMain | `test_main_version` | Test main with --version. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestOnboardRepository | `test_onboard_dry_run` | Test onboarding in dry run mode. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestOnboardRepository | `test_onboard_fresh_repository` | Test onboarding a fresh repository. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestOnboardRepository | `test_onboard_with_blueprint` | Test onboarding with specific blueprint. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestRollbackSession | `test_rollback_no_sessions` | Test rollback when no sessions exist. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestRollbackSession | `test_rollback_with_sessions_quit` | Test rollback session list and quit. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestRunQuickstart | `test_quickstart_handles_exception` | Test quickstart handles exceptions. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestRunQuickstart | `test_quickstart_handles_generation_failure` | Test quickstart handles generation failure. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestRunQuickstart | `test_quickstart_with_custom_blueprint` | Test quickstart with custom blueprint. |
| [test_factory_cli.py](file:///tests/unit/test_factory_cli.py) | TestRunQuickstart | `test_quickstart_with_default_output` | Test quickstart with default output directory. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapPriority | `test_all_priorities_defined` | Test that all expected priorities are defined. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapPriority | `test_priority_from_value` | Test creating GapPriority from value. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapPriority | `test_priority_ordering` | Test that priorities can be compared. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapPriority | `test_priority_sorting` | Test sorting priorities by value. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapPriority | `test_priority_values` | Test priority numeric values. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapType | `test_all_gap_types_defined` | Test that all expected gap types are defined. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapType | `test_gap_type_from_value` | Test creating GapType from value. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapType | `test_gap_type_invalid_value` | Test that invalid value raises error. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapType | `test_gap_type_iteration` | Test iterating over all gap types. |
| [test_gap_types.py](file:///tests/unit/test_gap_types.py) | TestGapType | `test_gap_type_values` | Test gap type string values. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestAxiomCoverage | `test_a1_verifiability_checked` | A1 (Verifiability) should be checked in content. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestAxiomCoverage | `test_a4_non_harm_checked` | A4 (Non-Harm) should be checked in commands. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestAxiomCoverage | `test_a4_non_harm_in_files` | A4 (Non-Harm) should be checked in file operations. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckCommand | `test_level_4_critical_commands` | Critical commands should trigger Level 4 (Protect). |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckCommand | `test_safe_commands` | Safe commands should pass without intervention. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckCommand | `test_sensitive_file_access` | Access to sensitive files should trigger pause. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckContentForClaims | `test_claim_detection` | Claims should be detected for verification. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckFileOperation | `test_critical_path_deletion` | Deletion of critical system paths should be blocked. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckFileOperation | `test_normal_file_operations` | Normal file operations should pass. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckFileOperation | `test_sensitive_file_deletion` | Deletion of sensitive files should require confirmation. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckResultProperties | `test_is_emergency_level_3` | Level 3 should not be emergency. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckResultProperties | `test_is_emergency_level_4` | Level 4 should be emergency. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckResultProperties | `test_requires_user_level_0` | Level 0 should not require user. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestCheckResultProperties | `test_requires_user_level_2` | Level 2+ should require user. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestValidateOperation | `test_command_validation` | Command validation should work through main entry point. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestValidateOperation | `test_content_validation` | Content validation should work through main entry point. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestValidateOperation | `test_file_delete_validation` | File delete validation should work through main entry point. |
| [test_guardian_axiom_checker.py](file:///tests/unit/test_guardian_axiom_checker.py) | TestValidateOperation | `test_file_write_validation` | File write validation should work through main entry point. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeCommand | `test_dangerous_command` | Dangerous commands should produce unsafe report. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeCommand | `test_safe_command` | Safe commands should produce safe report. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeContent | `test_content_with_secrets` | Content with secrets should be flagged. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeContent | `test_harmful_patterns` | Harmful content patterns should be flagged. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeContent | `test_safe_content` | Normal content should be safe. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeFileOperation | `test_agentrules_modification` | Modifying Agentrules should trigger caution. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeFileOperation | `test_cicd_modification` | Modifying CI/CD files should trigger caution. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeFileOperation | `test_dockerfile_modification` | Modifying Dockerfile should trigger caution. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeFileOperation | `test_env_file_write` | Writing to .env should trigger caution. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeFileOperation | `test_file_with_secrets` | File content with secrets should be flagged. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAnalyzeFileOperation | `test_normal_file_write` | Writing to normal file should be safe. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAxiomAlignment | `test_a1_verifiability` | A1: Claims should be flagged for verification. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAxiomAlignment | `test_a3_transparency` | A3: Hidden logic should be flagged. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAxiomAlignment | `test_a4_non_harm` | A4: Harmful actions should be blocked. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestAxiomAlignment | `test_a5_consistency` | A5: Instruction override attempts should be flagged. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestComprehensiveCheck | `test_all_safe` | All safe inputs should produce safe report. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestComprehensiveCheck | `test_combined_check` | Combined check should find highest severity. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestComprehensiveCheck | `test_command_only` | Command-only check should work. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestComprehensiveCheck | `test_content_only` | Content-only check should work. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestComprehensiveCheck | `test_file_only` | File-only check should work. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestComprehensiveCheck | `test_nothing_to_check` | Empty check should return safe. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestHarmReport | `test_safe_report_str` | Safe report string representation. |
| [test_guardian_harm_detector.py](file:///tests/unit/test_guardian_harm_detector.py) | TestHarmReport | `test_unsafe_report_str` | Unsafe report string representation. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestGetSeverityLevel | `test_high_severity` | High severity should return Level 4. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestGetSeverityLevel | `test_low_severity` | Low severity should return Level 2. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestGetSeverityLevel | `test_medium_severity` | Medium severity should return Level 3. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestGetSeverityLevel | `test_mixed_severity` | Mixed severity should return highest level. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestGetSeverityLevel | `test_no_matches` | No matches should return Level 0. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestIsFalsePositive | `test_false_positive_patterns` | False positive patterns should be correctly identified. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestRedactSecret | `test_long_secret` | Long secrets should show first and last 4 chars. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestRedactSecret | `test_short_secret` | Short secrets should be fully redacted. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanContent | `test_database_connection_strings` | Database connection strings should be detected. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanContent | `test_false_positives_filtered` | Placeholder values should not be detected as secrets. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanContent | `test_high_severity_api_keys` | High severity API keys should be detected. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanContent | `test_medium_severity_patterns` | Medium severity patterns should be detected. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanContent | `test_multiline_content` | Scanner should handle multiline content correctly. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanContent | `test_private_keys` | Private keys should be detected as high severity. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanDiff | `test_only_added_lines_checked` | Only added lines (starting with +) should be checked. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanDiff | `test_removed_lines_ignored` | Removed lines (starting with -) should not be checked. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanFile | `test_scan_nonexistent_file` | Scanning nonexistent file should return empty list. |
| [test_guardian_secret_scanner.py](file:///tests/unit/test_guardian_secret_scanner.py) | TestScanFile | `test_skip_binary_files` | Binary files should be skipped. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestInstallHooks | `test_install_hooks_asks_before_overwrite` | Test that install_hooks asks before overwriting existing hook. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestInstallHooks | `test_install_hooks_creates_hook_file` | Test that install_hooks creates the pre-commit hook. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestInstallHooks | `test_install_hooks_makes_executable_on_unix` | Test that install_hooks makes hook executable on Unix. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestInstallHooks | `test_install_hooks_no_git_directory` | Test that install_hooks fails gracefully without .git directory. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestInstallHooks | `test_install_hooks_overwrites_when_confirmed` | Test that install_hooks overwrites when user confirms. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestMainEntry | `test_main_calls_install_hooks` | Test that __main__ calls install_hooks. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_unix_hook_exits_cleanly` | Test that Unix hook exits with 0. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_unix_hook_has_shebang` | Test that Unix hook starts with shebang. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_unix_hook_runs_version_sync` | Test that Unix hook syncs versions. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_unix_hook_stages_readme` | Test that Unix hook stages README.md. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_windows_hook_checks_multiple_python_paths` | Test that Windows hook tries multiple Python paths. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_windows_hook_has_shebang` | Test that Windows hook starts with shebang. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_windows_hook_runs_version_sync` | Test that Windows hook syncs versions. |
| [test_install_hooks.py](file:///tests/unit/test_install_hooks.py) | TestPreCommitHookContent | `test_windows_hook_stages_readme` | Test that Windows hook stages README.md. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestAnalysisResult | `test_coverage_percentage` | Test coverage_percentage calculation. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestAnalysisResult | `test_coverage_percentage_zero_topics` | Test coverage_percentage with zero topics. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestAnalysisResult | `test_gaps_by_priority` | Test gaps_by_priority grouping. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestAnalysisResult | `test_gaps_by_type` | Test gaps_by_type grouping. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestAnalysisResult | `test_get_top_gaps` | Test get_top_gaps returns highest priority first. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestAnalysisResult | `test_to_dict` | Test to_dict produces complete serializable output. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_coverage_ratio_calculation` | Test coverage_ratio property calculation. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_coverage_ratio_capped_at_one` | Test coverage_ratio doesn't exceed 1.0. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_create_coverage_score` | Test creating a basic CoverageScore. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_is_adequate_exact_match` | Test is_adequate when coverage exactly meets requirement. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_is_adequate_false` | Test is_adequate when coverage below requirement. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_is_adequate_true` | Test is_adequate when coverage meets requirement. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestCoverageScore | `test_zero_required_depth` | Test coverage_ratio with zero required depth. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGap | `test_create_gap` | Test creating a KnowledgeGap. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGap | `test_gap_with_related_files` | Test gap with related files. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGap | `test_to_dict_serialization` | Test to_dict produces serializable output. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_analyze_returns_result` | Test analyze returns AnalysisResult. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_determine_depth_basic_mention` | Test depth determination with basic mentions. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_determine_depth_comprehensive` | Test depth determination with all criteria. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_determine_depth_no_mentions` | Test depth determination with no mentions. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_determine_depth_with_examples` | Test depth determination with examples. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_flatten_content_dict` | Test flattening dictionary content. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_flatten_content_list` | Test flattening list content. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_flatten_content_string` | Test flattening string content. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_get_extension_candidates` | Test getting extension candidates. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_init` | Test analyzer initialization. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_load_knowledge_files` | Test loading knowledge files into cache. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_load_knowledge_files_skips_invalid` | Test that invalid JSON files are skipped. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestKnowledgeGapAnalyzer | `test_save_report` | Test saving analysis report. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestRunGapAnalysis | `test_run_with_custom_taxonomy` | Test running gap analysis with custom taxonomy. |
| [test_knowledge_gap_analyzer.py](file:///tests/unit/test_knowledge_gap_analyzer.py) | TestRunGapAnalysis | `test_run_with_defaults` | Test running gap analysis with defaults. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestArtifactType | `test_artifact_type_values` | Test artifact type values. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestConflict | `test_conflict_creation` | Test creating a Conflict. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestConflict | `test_get_existing_content` | Test reading existing file content. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestConflict | `test_get_existing_content_nonexistent` | Test reading non-existent file returns empty string. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestConflictPrompt | `test_format_prompt` | Test formatting a conflict prompt. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestConflictResolution | `test_resolution_values` | Test that all resolutions have correct values. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDeepMerge | `test_merge_flat_dicts` | Test merging flat dictionaries. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDeepMerge | `test_merge_lists` | Test merging lists without duplicates. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDeepMerge | `test_merge_nested_dicts` | Test merging nested dictionaries. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDeepMerge | `test_overlay_takes_precedence` | Test that overlay values take precedence. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDefaultStrategies | `test_agent_strategy` | Test default strategy for agents. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDefaultStrategies | `test_agentrules_strategy` | Test default strategy for agentrules. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDefaultStrategies | `test_command_strategy` | Test default strategy for commands (user custom). |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestDefaultStrategies | `test_purpose_strategy` | Test default strategy for PURPOSE.md (user custom). |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_detect_agent_conflict` | Test detecting agent conflict. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_detect_agentrules_conflict` | Test detecting agentrules conflict. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_detect_mcp_conflict` | Test detecting MCP configuration conflict. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_detect_skill_conflict` | Test detecting skill conflict. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_engine_creation` | Test creating a MergeEngine. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_get_conflict_prompt_agentrules` | Test getting prompt for agentrules conflict. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_get_conflict_prompt_command` | Test getting prompt for command conflict (user custom). |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_get_renamed_name_with_extension` | Test getting renamed name for file with extension. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_get_renamed_name_without_extension` | Test getting renamed name for file without extension. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_no_conflict_when_different_content_is_same` | Test no conflict when content is identical. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_set_and_get_resolution` | Test setting and getting a resolution. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_should_rename_artifact` | Test checking if artifact should be renamed. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeEngine | `test_should_skip_artifact` | Test checking if artifact should be skipped. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeJsonFiles | `test_merge_arrays_no_duplicates` | Test merging arrays without duplicates. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeJsonFiles | `test_merge_invalid_json` | Test merging invalid JSON returns error. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeJsonFiles | `test_merge_nested_objects` | Test deep merging nested objects. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeJsonFiles | `test_merge_overlapping_keys` | Test merging with overlapping keys (new takes precedence). |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeJsonFiles | `test_merge_simple_objects` | Test merging simple JSON objects. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeJsonFiles | `test_shallow_merge` | Test shallow merge replaces nested objects. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeResult | `test_failed_result` | Test creating a failed merge result. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeResult | `test_successful_result` | Test creating a successful merge result. |
| [test_merge_strategy.py](file:///tests/unit/test_merge_strategy.py) | TestMergeStrategy | `test_strategy_values` | Test merge strategy values. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestAgentPatternFiles | `test_agent_patterns_have_required_fields` | Test that agent patterns (not schema files) have required structure. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestAgentPatternFiles | `test_all_agent_patterns_are_valid_json` | Test that all agent pattern files are valid JSON. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestAgentPatternFiles | `test_code_reviewer_pattern_exists` | Test that code-reviewer pattern exists and is valid. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestBlueprintFiles | `test_all_blueprints_are_valid_json` | Test that all blueprint.json files are valid JSON. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestBlueprintFiles | `test_blueprints_have_required_fields` | Test that blueprints have required metadata and stack fields. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestBlueprintFiles | `test_python_fastapi_blueprint_exists` | Test that python-fastapi blueprint exists and is valid. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestKnowledgeFiles | `test_all_knowledge_files_are_valid_json` | Test that all knowledge files are valid JSON. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestKnowledgeFiles | `test_skill_catalog_exists` | Test that skill-catalog.json exists and has skills. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestPatternConsistency | `test_blueprint_agent_references_exist` | Test that agents referenced in blueprints have corresponding patterns. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestPatternConsistency | `test_blueprint_skill_references_exist` | Test that skills referenced in blueprints exist in patterns or skill catalog. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestSkillPatternFiles | `test_all_skill_patterns_are_valid_json` | Test that all skill pattern files are valid JSON. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestSkillPatternFiles | `test_bugfix_workflow_pattern_exists` | Test that bugfix-workflow pattern exists and is valid. |
| [test_pattern_loading.py](file:///tests/unit/test_pattern_loading.py) | TestSkillPatternFiles | `test_skill_patterns_have_required_fields` | Test that skill patterns (not schema files) have required structure. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterConsistency | `test_all_adapters_implement_create_epic` | Test that all adapters implement createEpic operation. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterConsistency | `test_all_adapters_implement_create_sprint` | Test that all adapters implement createSprint operation. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterConsistency | `test_all_adapters_implement_create_story` | Test that all adapters implement createStory operation. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_defines_board_operations` | Test that interface defines board operations. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_defines_documentation_operations` | Test that interface defines documentation operations. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_defines_metrics_operations` | Test that interface defines metrics operations. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_defines_planning_operations` | Test that interface defines planning operations. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_defines_work_item_operations` | Test that interface defines work item operations. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_file_exists` | Test that adapter-interface.json exists. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAdapterInterface | `test_interface_is_valid_json` | Test that adapter-interface.json is valid JSON. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAzureDevOpsAdapter | `test_azure_adapter_exists` | Test that azure-devops-adapter.json exists. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAzureDevOpsAdapter | `test_azure_adapter_is_valid_json` | Test that azure-devops-adapter.json is valid JSON. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAzureDevOpsAdapter | `test_azure_epic_mapping` | Test Azure DevOps epic mapping. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAzureDevOpsAdapter | `test_azure_has_wiql_patterns` | Test that Azure DevOps adapter has WIQL patterns. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestAzureDevOpsAdapter | `test_azure_sprint_mapping` | Test Azure DevOps sprint mapping (Sprint → Iteration). |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestGitHubAdapter | `test_github_adapter_exists` | Test that github-adapter.json exists. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestGitHubAdapter | `test_github_adapter_is_valid_json` | Test that github-adapter.json is valid JSON. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestGitHubAdapter | `test_github_board_mapping` | Test GitHub board mapping (Board → Project v2). |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestGitHubAdapter | `test_github_epic_mapping` | Test GitHub epic mapping (Epic → Issue with label). |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestGitHubAdapter | `test_github_sprint_mapping` | Test GitHub sprint mapping (Sprint → Milestone). |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestGitHubAdapter | `test_github_story_mapping` | Test GitHub story mapping. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestJiraAdapter | `test_jira_adapter_exists` | Test that jira-adapter.json exists. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestJiraAdapter | `test_jira_adapter_is_valid_json` | Test that jira-adapter.json is valid JSON. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestJiraAdapter | `test_jira_epic_mapping` | Test Jira epic mapping. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestJiraAdapter | `test_jira_has_jql_patterns` | Test that Jira adapter has JQL patterns. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestJiraAdapter | `test_jira_sprint_mapping` | Test Jira sprint mapping. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestJiraAdapter | `test_jira_story_mapping` | Test Jira story mapping. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestLinearAdapter | `test_linear_adapter_exists` | Test that linear-adapter.json exists. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestLinearAdapter | `test_linear_adapter_is_valid_json` | Test that linear-adapter.json is valid JSON. |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestLinearAdapter | `test_linear_epic_mapping` | Test Linear epic mapping (Epic → Project). |
| [test_pm_adapters.py](file:///tests/unit/test_pm_adapters.py) | TestLinearAdapter | `test_linear_sprint_mapping` | Test Linear sprint mapping (Sprint → Cycle). |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMAgentSkillExtension | `test_agents_unchanged_when_pm_disabled` | Test that agents list is unchanged when PM is disabled. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMAgentSkillExtension | `test_pm_agents_added_when_enabled` | Test that PM agents are added when PM is enabled. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMAgentSkillExtension | `test_pm_skills_added_when_enabled` | Test that PM skills are added when PM is enabled. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFields | `test_pm_backend_accepts_valid_values` | Test that pm_backend accepts valid backend values. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFields | `test_pm_doc_backend_accepts_valid_values` | Test that pm_doc_backend accepts valid backend values. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFields | `test_pm_enabled_default_false` | Test that pm_enabled defaults to False. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFields | `test_pm_methodology_accepts_valid_values` | Test that pm_methodology accepts valid methodology values. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFromDict | `test_from_dict_pm_disabled_by_default` | Test that PM is disabled by default when not specified. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFromDict | `test_from_dict_with_full_pm_config` | Test from_dict with complete PM configuration. |
| [test_pm_config.py](file:///tests/unit/test_pm_config.py) | TestPMConfigFromDict | `test_from_dict_with_pm_enabled` | Test from_dict with pm_enabled set to True. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigDefaults | `test_default_values_consistency` | Test that default values are consistent across creation methods. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigDefaults | `test_none_vs_empty_handling` | Test handling of None vs empty values. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromDict | `test_from_dict_empty` | Test from_dict with empty dictionary uses defaults. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromDict | `test_from_dict_extra_fields_ignored` | Test that extra fields in dictionary are ignored. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromDict | `test_from_dict_minimal` | Test from_dict with minimal dictionary. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromDict | `test_from_dict_partial` | Test from_dict with partial dictionary. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromDict | `test_from_dict_valid_full` | Test from_dict with complete valid dictionary. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromJson | `test_from_json_file_empty` | Test from_json_file with empty JSON object. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromJson | `test_from_json_file_invalid_json` | Test from_json_file with invalid JSON syntax. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromJson | `test_from_json_file_minimal` | Test from_json_file with minimal JSON content. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromJson | `test_from_json_file_not_found` | Test from_json_file with non-existent file. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromJson | `test_from_json_file_valid` | Test from_json_file with valid JSON. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromYaml | `test_from_yaml_file_invalid_yaml` | Test from_yaml_file with invalid YAML syntax. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromYaml | `test_from_yaml_file_minimal` | Test from_yaml_file with minimal YAML content. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromYaml | `test_from_yaml_file_not_found` | Test from_yaml_file with non-existent file. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigFromYaml | `test_from_yaml_file_valid` | Test from_yaml_file with valid YAML. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigInstantiation | `test_full_instantiation` | Test creating ProjectConfig with all fields. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigInstantiation | `test_minimal_instantiation` | Test creating ProjectConfig with only required field. |
| [test_project_config.py](file:///tests/unit/test_project_config.py) | TestProjectConfigInstantiation | `test_mutable_default_isolation` | Test that mutable defaults are isolated between instances. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestAgentRendering | `test_render_agent_basic_structure` | Test that rendered agent has correct markdown structure. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestAgentRendering | `test_render_agent_contains_rules` | Test that rendered agent contains important rules. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestAgentRendering | `test_render_agent_contains_skills_section` | Test that rendered agent contains skills used section. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestAgentrulesGeneration | `test_agentrules_no_placeholder_remnants` | Test that no unreplaced placeholders remain. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestAgentrulesGeneration | `test_agentrules_variable_substitution` | Test that variables are correctly substituted. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestBlueprintLoading | `test_load_blueprint_missing` | Test loading a non-existent blueprint returns None. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestBlueprintLoading | `test_load_blueprint_none_when_not_specified` | Test that None is returned when no blueprint specified. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestBlueprintLoading | `test_load_blueprint_valid` | Test loading a valid blueprint. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestDirectoryCreation | `test_create_directories_idempotent` | Test that calling _create_directories twice doesn't cause errors. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestDirectoryCreation | `test_create_directories_structure` | Test that all expected directories are created. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFileWriting | `test_write_file_creates_file` | Test that _write_file creates the file. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFileWriting | `test_write_file_creates_parent_dirs` | Test that _write_file creates parent directories. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFileWriting | `test_write_file_tracks_files` | Test that written files are tracked. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFileWriting | `test_write_file_utf8_encoding` | Test that files are written with UTF-8 encoding. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFullGeneration | `test_generate_creates_expected_files` | Test that generate() creates expected files. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFullGeneration | `test_generate_returns_result_dict` | Test that generate() returns proper result dictionary. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestFullGeneration | `test_generate_tracks_all_files` | Test that all generated files are tracked. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestMcpServerSection | `test_mcp_section_table_format` | Test that MCP section uses markdown table format. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestMcpServerSection | `test_mcp_section_with_servers` | Test MCP section generation when servers are configured. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestPatternLoading | `test_load_pattern_agent_valid` | Test loading a valid agent pattern. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestPatternLoading | `test_load_pattern_invalid_type` | Test loading from invalid pattern type returns None. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestPatternLoading | `test_load_pattern_missing` | Test loading a non-existent pattern returns None. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestPatternLoading | `test_load_pattern_skill_valid` | Test loading a valid skill pattern. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestProjectGeneratorInit | `test_init_basic` | Test basic initialization. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestProjectGeneratorInit | `test_init_factory_root` | Test factory root is correctly determined. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestSkillRendering | `test_render_skill_basic_structure` | Test that rendered skill has correct markdown structure. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestSkillRendering | `test_render_skill_contains_fallback` | Test that rendered skill contains fallback procedures. |
| [test_project_generator.py](file:///tests/unit/test_project_generator.py) | TestSkillRendering | `test_render_skill_contains_mcp_tools` | Test that rendered skill contains MCP tools references. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestCacheStructure | `test_artifact_entry_has_count_and_hash` | Each artifact entry should have count and hash fields. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestCacheStructure | `test_cache_has_required_fields` | Cache JSON should have schema_version, updated_at, and artifacts. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestCacheStructure | `test_tests_artifact_has_breakdown` | Tests artifact should include category breakdown. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestDirectoryTriggers | `test_known_directories_map_correctly` | Known directories should map to correct artifact types. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestDirectoryTriggers | `test_nested_path_triggers_parent` | Nested paths should trigger parent directory's artifacts. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestFastFileCounting | `test_count_test_functions_by_subdirectory` | Should count tests in specific subdirectory only. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestFastFileCounting | `test_count_test_functions_finds_simple_tests` | Should count simple test functions correctly. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestFastFileCounting | `test_count_test_functions_handles_async_tests` | Should count async test functions. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestFastFileCounting | `test_count_test_functions_handles_subdirectories` | Should recursively count tests in subdirectories. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestFastFileCounting | `test_count_test_functions_ignores_non_test_files` | Should only count tests in test_*.py files. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestIndexUpdates | `test_update_for_file_identifies_artifact_type` | Should correctly identify artifact type from file path. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestIndexUpdates | `test_update_only_affects_relevant_section` | Updating one artifact type should not modify others. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestPerformance | `test_file_based_counting_is_fast` | File-based counting should complete in under 1 second. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestPrecommitIntegration | `test_precommit_reads_from_cache_when_fresh` | Pre-commit should use cached values when cache is fresh. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestPrecommitIntegration | `test_precommit_rebuilds_when_stale` | Pre-commit should rebuild when cache is stale. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestStalenessDetection | `test_cache_is_fresh_within_threshold` | Cache should be considered fresh within time threshold. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestStalenessDetection | `test_cache_is_stale_beyond_threshold` | Cache should be considered stale beyond time threshold. |
| [test_reactive_index.py](file:///tests/unit/test_reactive_index.py) | TestStalenessDetection | `test_missing_cache_is_stale` | Missing cache file should trigger rebuild. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestAgentruleAnalysis | `test_default_values` | Test default values for AgentruleAnalysis. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestGetFileHash | `test_hash_different_content_different_hash` | Test that different content produces different hash. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestGetFileHash | `test_hash_existing_file` | Test hashing an existing file. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestGetFileHash | `test_hash_nonexistent_file` | Test hashing a non-existent file returns empty string. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestGetFileHash | `test_hash_same_content_same_hash` | Test that same content produces same hash. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestMainEntry | `test_analyzer_provides_complete_summary` | Test that analyzer provides complete summary. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestMainEntry | `test_main_with_valid_path` | Test analyzing a valid repository path. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestMcpAnalysis | `test_default_values` | Test default values for McpAnalysis. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestOnboardingScenario | `test_scenario_values` | Test that all scenarios have correct values. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_agentrules` | Test that analyzer detects Agentrules file. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_agents` | Test that analyzer detects agent files. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_factory_marker` | Test that analyzer detects factory marker in agentrules. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_git_repo` | Test that analyzer detects .git directory. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_knowledge_files` | Test that analyzer detects knowledge files. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_mcp_config` | Test that analyzer detects MCP configuration. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_purpose_md` | Test that analyzer detects PURPOSE.md. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_detects_skills` | Test that analyzer detects skill directories. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyze_fresh_repo` | Test analyzing a fresh repository with no artifacts. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyzer_creation` | Test creating a RepoAnalyzer. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_analyzer_nonexistent_path_raises` | Test that non-existent path raises ValueError. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_detect_tech_stack_java_spring` | Test tech stack detection for Java Spring project. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_detect_tech_stack_python` | Test tech stack detection for Python project. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_detect_tech_stack_typescript_react` | Test tech stack detection for TypeScript React project. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_determine_scenario_complete` | Test scenario determination for complete setup. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_determine_scenario_minimal` | Test scenario determination for minimal setup. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_determine_scenario_partial` | Test scenario determination for partial setup. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoAnalyzer | `test_determine_scenario_upgrade` | Test scenario determination for upgrade scenario. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoInventory | `test_creation_with_path` | Test creating RepoInventory with a path. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoInventory | `test_get_summary_fresh_repo` | Test get_summary for a fresh repository. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestRepoInventory | `test_get_summary_with_artifacts` | Test get_summary with some artifacts. |
| [test_repo_analyzer.py](file:///tests/unit/test_repo_analyzer.py) | TestTechStackDetection | `test_default_values` | Test default values for TechStackDetection. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestAntiPatterns | `test_has_anti_patterns` | Pattern should document anti-patterns to avoid. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestAntiPatterns | `test_warns_against_analysis_paralysis` | Should warn against analysis paralysis. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestAntiPatterns | `test_warns_against_not_invented_here` | Should warn against 'not invented here' syndrome. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestBenefitsDocumentation | `test_documents_multiplied_value` | Pattern should explain multiplied value concept. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestBenefitsDocumentation | `test_has_benefits_section` | Pattern should document its benefits. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestExamples | `test_has_examples` | Pattern should include examples of application. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestExamples | `test_reactive_indexing_example` | Should include reactive indexing as an example. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestGeneratedProjectAvailability | `test_no_absolute_paths` | Pattern should not contain absolute paths. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestGeneratedProjectAvailability | `test_pattern_can_be_serialized` | Pattern should be serializable for inclusion in generated projects. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestIntegrationPoints | `test_defines_agent_integration` | Pattern should define how agents should use it. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestIntegrationPoints | `test_knowledge_file_is_listed_in_manifest` | Knowledge file should be discoverable via manifest or directory. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestIntegrationPoints | `test_references_related_patterns` | Pattern should reference related patterns. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestKnowledgeFileStructure | `test_has_axiom_alignment` | Knowledge file should document axiom alignment. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestKnowledgeFileStructure | `test_has_required_top_level_fields` | Knowledge file should have required top-level fields. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestKnowledgeFileStructure | `test_knowledge_file_exists` | Research-first pattern knowledge file should exist. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestKnowledgeFileStructure | `test_valid_json_schema` | Knowledge file should have valid JSON schema reference. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestTriggerDefinitions | `test_has_counter_indicators` | Pattern should define when NOT to apply research-first. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestTriggerDefinitions | `test_has_trigger_definitions` | Pattern should define when to apply research-first approach. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestTriggerDefinitions | `test_triggers_include_performance_optimization` | Performance optimization should trigger research-first. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestTriggerDefinitions | `test_triggers_include_security` | Security implementations should trigger research-first. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestWorkflowSteps | `test_has_workflow_definition` | Pattern should define a workflow. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestWorkflowSteps | `test_workflow_includes_build_step` | Workflow should include a build/implementation step. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestWorkflowSteps | `test_workflow_includes_document_step` | Workflow should include a documentation step. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestWorkflowSteps | `test_workflow_includes_research_step` | Workflow should include a research step. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestWorkflowSteps | `test_workflow_includes_test_step` | Workflow should include a test step. |
| [test_research_first_pattern.py](file:///tests/unit/test_research_first_pattern.py) | TestWorkflowSteps | `test_workflow_order_is_research_before_build` | Research should come before build in workflow order. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestArtifactScanner | `test_scan_finds_matching_files` | Verify that the scanner correctly identifies files matching a glob pattern. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestArtifactScanner | `test_scan_parent_dir_id_extractor` | Verify that artifact IDs can be extracted from their parent directory names. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestArtifactScanner | `test_scan_recursive` | Verify that the scanner can perform recursive searches when configured. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestArtifactScanner | `test_scan_respects_exclusions` | Verify that the scanner respects the exclusion list in the configuration. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestArtifactScanner | `test_scan_returns_empty_for_missing_dir` | Verify that the scanner handles non-existent source directories gracefully. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCategoryTestCounts | `test_counts_are_immutable` | CategoryTestCounts should be immutable. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCategoryTestCounts | `test_creates_valid_namedtuple` | Should create a valid CategoryTestCounts instance. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCollectTestCount | `test_handles_missing_directory` | Verify that the collector returns 0 when the target test directory is missing. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCollectTestCount | `test_handles_subprocess_timeout` | Verify that the collector handles subprocess timeouts gracefully by returning 0. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCollectTestCount | `test_parses_plural_tests` | Verify that the parser correctly extracts counts when multiple tests are found. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCollectTestCount | `test_parses_singular_test` | Verify that the parser correctly extracts counts when exactly one test is found. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCollectTestCount | `test_returns_integer` | Verify that collect_test_count returns the number of tests as an integer. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCountSyncStrategy | `test_detects_out_of_sync_count` | Verify that the count strategy correctly identifies a mismatch in numbers. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCountSyncStrategy | `test_dry_run_does_not_modify_file` | Verify that dry-run mode correctly avoids any filesystem modifications. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCountSyncStrategy | `test_reports_in_sync_when_matched` | Verify that the count strategy reports no changes when the numbers match. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestCountSyncStrategy | `test_updates_file_when_sync` | Verify that the strategy correctly updates the file content when syncing. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestDirectoryDetection | `test_detects_agents_dir` | Verify that changes to the agents directory trigger a sync for that artifact. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestDirectoryDetection | `test_detects_nested_path` | Verify that nested file changes correctly trigger parent artifact syncs. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestExtractDocumentedCounts | `test_extracts_category_counts` | Should extract all category counts. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestExtractDocumentedCounts | `test_extracts_total_count` | Should extract total test count. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestExtractDocumentedCounts | `test_handles_missing_categories` | Verify that the extractor returns 0 for categories missing from the table. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestExtractDocumentedCounts | `test_handles_missing_total` | Verify that the extractor returns 0 for the total if it's not found in content. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestGetPythonPath | `test_returns_current_interpreter` | Verify that get_python_path returns the current active Python interpreter. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestIntegration | `test_artifacts_are_currently_synced` | Verify that the repository documentation is currently in a perfectly synced state. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestIntegration | `test_config_file_exists` | Sanity check that the actual production sync_config.json exists in the repo. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestIntegration | `test_config_has_all_artifact_types` | Verify that all core factory artifacts are defined in the sync configuration. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestIntegration | `test_config_is_valid_json` | Verify that the production sync_config.json is valid and readable JSON. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestIntegration | `test_engine_loads_successfully` | Verify that the SyncEngine can initialize with the real production config. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestIntegration | `test_sync_all_dry_run_succeeds` | Perform a full dry-run sync across all artifacts in the actual repository. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestJsonFieldSyncStrategy | `test_creates_missing_nested_structure` | Verify that the JSON strategy creates missing parent objects if they don't exist. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestJsonFieldSyncStrategy | `test_updates_nested_json_field` | Verify that the JSON strategy can update values deep within a nested structure. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestSyncEngine | `test_get_artifacts_for_dirs` | Verify that the engine identifies the correct artifacts impacted by changed dirs. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestSyncEngine | `test_get_directory_triggers` | Verify that the engine correctly maps source directories to artifact types. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestSyncEngine | `test_loads_config_from_file` | Verify that the SyncEngine correctly parses the main sync_config.json file. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestSyncEngine | `test_sync_artifact_unknown_returns_error` | Verify that requesting a sync for a non-existent artifact returns an error. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestUpdateTestingMd | `test_detects_out_of_sync_total` | Should detect when total count is out of sync. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestUpdateTestingMd | `test_dry_run_does_not_modify_file` | Verify that update_testing_md respects the dry_run flag. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestUpdateTestingMd | `test_no_changes_when_synced` | Verify that update_testing_md returns zero changes when counts match EXACTLY. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestUpdateTestingMd | `test_reports_missing_file` | Verify that update_testing_md handles the absence of the target file. |
| [test_sync_artifacts.py](file:///tests/unit/test_sync_artifacts.py) | TestUpdateTestingMd | `test_sync_updates_file` | Should update file when dry_run=False. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetChangelogVersion | `test_extracts_version_from_valid_changelog` | Should extract the first version header from CHANGELOG.md. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetChangelogVersion | `test_handles_changelog_without_version` | Should return 0.0.0 if no version header found. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetChangelogVersion | `test_handles_missing_changelog` | Should return 0.0.0 if CHANGELOG.md doesn't exist. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersion | `test_extracts_version_from_valid_json` | Should extract version from JSON file. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersion | `test_returns_none_for_invalid_json` | Should return None for invalid JSON. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersion | `test_returns_none_for_missing_file` | Should return None if file doesn't exist. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersion | `test_returns_none_for_missing_version` | Should return None if no version field. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersionGeneric | `test_extracts_version_with_valid_pattern` | Should extract version matching the pattern. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersionGeneric | `test_returns_none_for_missing_file` | Should return None if file doesn't exist. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestGetFileVersionGeneric | `test_returns_none_for_no_match` | Should return None if pattern doesn't match. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestIntegration | `test_changelog_exists_and_has_version` | CHANGELOG.md should exist and have a valid version. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestIntegration | `test_current_state_is_synced` | Current factory state should be version-synced. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestIntegration | `test_version_locations_files_exist` | All files in VERSION_LOCATIONS should exist. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestSyncFileVersion | `test_dry_run_does_not_modify_file` | Should not modify file when dry_run=True. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestSyncFileVersion | `test_returns_false_for_missing_file` | Should return False if file doesn't exist. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestSyncFileVersion | `test_returns_false_for_no_pattern_match` | Should return False if pattern doesn't match. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestSyncFileVersion | `test_sync_updates_file` | Should update file when dry_run=False. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestSyncManifest | `test_detects_out_of_sync_factory_version` | Should detect when factory_version is out of sync. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestSyncManifest | `test_reports_synced_when_all_match` | Should report all synced when versions match. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestVersionLocations | `test_all_locations_have_required_keys` | All VERSION_LOCATIONS entries should have required keys. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestVersionLocations | `test_all_patterns_are_valid_regex` | All patterns should be valid regex. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestVersionLocations | `test_replacement_functions_are_callable` | All replacement functions should be callable. |
| [test_sync_manifest_versions.py](file:///tests/unit/test_sync_manifest_versions.py) | TestVersionLocations | `test_replacement_functions_produce_valid_strings` | Replacement functions should return strings with version. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestLoadAgentTaxonomy | `test_load_default_taxonomy` | Test loading the default agent taxonomy. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestLoadAgentTaxonomy | `test_taxonomy_has_domains` | Test that taxonomy has expected domains. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestLoadAgentTaxonomy | `test_taxonomy_topics_have_keywords` | Test that taxonomy topics have keywords defined. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_cache_works` | Test that taxonomy is cached after first load. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_get_all_topics_flat` | Test flattening all topics from taxonomy. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_get_available_taxonomies` | Test getting list of available taxonomies. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_init_custom_directory` | Test TaxonomyLoader with custom directory. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_init_default_directory` | Test TaxonomyLoader uses default directory. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_load_taxonomy_file_not_found` | Test loading non-existent taxonomy raises error. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_load_taxonomy_invalid_json` | Test loading invalid JSON raises error. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_load_taxonomy_success` | Test successful taxonomy loading. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTaxonomyLoader | `test_parse_topic_with_subtopics` | Test parsing topics with nested subtopics key. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_count_topics_single` | Test count_topics for single node. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_count_topics_with_subtopics` | Test count_topics includes subtopics. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_create_topic_node` | Test creating a basic TopicNode. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_create_topic_node_with_keywords` | Test creating a TopicNode with keywords. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_get_all_keywords_no_subtopics` | Test get_all_keywords with no subtopics. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_get_all_keywords_with_subtopics` | Test get_all_keywords includes subtopic keywords. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_get_leaf_topics_no_children` | Test get_leaf_topics when node has no children. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_get_leaf_topics_with_children` | Test get_leaf_topics returns only leaves. |
| [test_taxonomy.py](file:///tests/unit/test_taxonomy.py) | TestTopicNode | `test_nested_subtopics_deep` | Test deeply nested subtopics. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestCamelCaseFilter | `test_empty` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestCamelCaseFilter | `test_from_kebab_case` | Test conversion from kebab-case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestCamelCaseFilter | `test_from_snake_case` | Test conversion from snake_case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestCreateEngine | `test_create_with_defaults` | Test creating engine with default settings. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestDefaultIfEmptyFilter | `test_with_empty_list` | Test with empty list. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestDefaultIfEmptyFilter | `test_with_empty_string` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestDefaultIfEmptyFilter | `test_with_none` | Test with None. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestDefaultIfEmptyFilter | `test_with_value` | Test with non-empty value. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestEnvGlobal | `test_existing_variable` | Test with existing environment variable. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestEnvGlobal | `test_missing_variable` | Test with missing variable and default. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestIndentTextFilter | `test_basic_indent` | Test basic indentation. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestIndentTextFilter | `test_empty` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestIndentTextFilter | `test_indent_first_line` | Test with first line indented. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestJoinLinesFilter | `test_basic_join` | Test basic joining. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestJoinLinesFilter | `test_custom_separator` | Test with custom separator. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestJoinLinesFilter | `test_empty_list` | Test with empty list. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestKebabCaseFilter | `test_empty` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestKebabCaseFilter | `test_from_pascal_case` | Test conversion from PascalCase. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestKebabCaseFilter | `test_from_snake_case` | Test conversion from snake_case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestNowGlobal | `test_custom_format` | Test custom format. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestNowGlobal | `test_default_format` | Test default format. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPascalCaseFilter | `test_empty` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPascalCaseFilter | `test_from_kebab_case` | Test conversion from kebab-case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPascalCaseFilter | `test_from_snake_case` | Test conversion from snake_case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPascalCaseFilter | `test_from_spaces` | Test conversion from space-separated words. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPluralizeFilter | `test_count_one` | Test with count=1 (should not pluralize). |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPluralizeFilter | `test_empty` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPluralizeFilter | `test_irregulars` | Test irregular plurals. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPluralizeFilter | `test_regular_plurals` | Test regular plural forms. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestPluralizeFilter | `test_special_endings` | Test words with special endings. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestQuoteFilter | `test_backticks` | Test backtick style. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestQuoteFilter | `test_double_quotes` | Test double quote style. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestQuoteFilter | `test_single_quotes` | Test single quote style. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestRangeListGlobal | `test_basic_range` | Test basic range. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestRangeListGlobal | `test_with_step` | Test with step. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestSnakeCaseFilter | `test_empty_and_none` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestSnakeCaseFilter | `test_from_camel_case` | Test conversion from camelCase. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestSnakeCaseFilter | `test_from_kebab_case` | Test conversion from kebab-case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestSnakeCaseFilter | `test_from_pascal_case` | Test conversion from PascalCase. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestSnakeCaseFilter | `test_with_spaces` | Test conversion from space-separated words. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineAddFilter | `test_add_custom_filter` | Test adding a custom filter. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineAddGlobal | `test_add_custom_global` | Test adding a custom global. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineGetVariables | `test_extract_variables` | Test extracting variables from template. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineInit | `test_filters_registered` | Test that custom filters are registered. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineInit | `test_globals_registered` | Test that custom globals are registered. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineInit | `test_init_basic` | Test basic initialization. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineInit | `test_init_with_dirs` | Test initialization with template directories. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderFile | `test_render_from_file` | Test rendering from a file path. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderString | `test_conditional` | Test conditional in template. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderString | `test_filter_in_template` | Test using filter in template. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderString | `test_global_now_in_template` | Test using now() in template. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderString | `test_legacy_placeholder_uppercase` | Test legacy {{UPPERCASE}} placeholder conversion. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderString | `test_loop` | Test loop in template. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTemplateEngineRenderString | `test_simple_variable` | Test simple variable substitution. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTitleCaseFilter | `test_empty` | Test with empty string. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTitleCaseFilter | `test_from_kebab_case` | Test conversion from kebab-case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestTitleCaseFilter | `test_from_snake_case` | Test conversion from snake_case. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestToJsonFilter | `test_dict` | Test with dictionary. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestToJsonFilter | `test_list` | Test with list. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestToYamlListFilter | `test_basic_list` | Test basic list. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestToYamlListFilter | `test_empty_list` | Test with empty list. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestWrapCodeFilter | `test_with_language` | Test with language specified. |
| [test_template_engine.py](file:///tests/unit/test_template_engine.py) | TestWrapCodeFilter | `test_without_language` | Test without language. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestCountFilesByExtension | `test_counts_in_subdirectories` | Test counting files in subdirectories. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestCountFilesByExtension | `test_counts_json_files` | Test counting JSON files. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestCountFilesByExtension | `test_excludes_pycache` | Test that __pycache__ files are excluded. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestExtractReadmeCounts | `test_extract_exact_counts` | Test extracting exact counts from README. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestExtractReadmeCounts | `test_extract_threshold_counts` | Test extracting threshold counts (50+ files). |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestExtractReadmeCounts | `test_no_readme` | Test when README doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestGenerateCountsSummary | `test_returns_all_counts` | Test that all counts are returned. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestGenerateStructureMarkdown | `test_generates_markdown` | Test that markdown is generated. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestGenerateStructureMarkdown | `test_includes_counts` | Test that counts are included in markdown. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestMain | `test_main_check_mode` | Test main with --check. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestMain | `test_main_default_is_check` | Test that default mode is --check. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestMain | `test_main_generate_mode` | Test main with --generate. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestMain | `test_main_json_mode` | Test main with --json. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestMain | `test_main_update_mode` | Test main with --update. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestMain | `test_main_with_custom_root` | Test main with --root argument. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestRoundToThreshold | `test_round_large_numbers` | Test rounding large numbers. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestRoundToThreshold | `test_round_medium_numbers` | Test rounding medium numbers. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestRoundToThreshold | `test_round_small_numbers` | Test rounding small numbers. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanAgents | `test_scan_no_agents_dir` | Test scanning when agents directory doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanAgents | `test_scan_with_agents` | Test scanning with agents present. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanAll | `test_scan_all_returns_all_sections` | Test that scan_all returns all sections. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanBlueprints | `test_scan_no_blueprints_dir` | Test scanning when blueprints directory doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanBlueprints | `test_scan_with_blueprints` | Test scanning with blueprints present. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanKnowledge | `test_scan_no_knowledge_dir` | Test scanning when knowledge directory doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanKnowledge | `test_scan_with_knowledge` | Test scanning with knowledge files present. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanPatterns | `test_scan_no_patterns_dir` | Test scanning when patterns directory doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanPatterns | `test_scan_with_patterns` | Test scanning with patterns present. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanSkills | `test_scan_no_skills_dir` | Test scanning when skills directory doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanSkills | `test_scan_with_skills` | Test scanning with skills present. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanTemplates | `test_scan_no_templates_dir` | Test scanning when templates directory doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestScanTemplates | `test_scan_with_templates` | Test scanning with templates present. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestShouldIgnore | `test_does_not_ignore_valid_dir` | Test that valid directories are not ignored. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestShouldIgnore | `test_ignores_dotfiles` | Test that dotfiles are ignored. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestShouldIgnore | `test_ignores_git` | Test that .git is ignored. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestShouldIgnore | `test_ignores_pyc_files` | Test that .pyc files are ignored. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestShouldIgnore | `test_ignores_pycache` | Test that __pycache__ is ignored. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestStructureValidatorInit | `test_init_with_custom_path` | Test initialization with custom path. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestStructureValidatorInit | `test_init_with_default_path` | Test initialization with default path. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestUpdateReadme | `test_update_no_readme` | Test update when README doesn't exist. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestUpdateReadme | `test_update_no_structure_section` | Test updating README without structure section. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestUpdateReadme | `test_update_with_structure_section` | Test updating README with existing structure section. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestValidate | `test_validate_matching_counts` | Test validation with matching counts. |
| [test_validate_readme.py](file:///tests/unit/test_validate_readme.py) | TestValidate | `test_validate_threshold_passing` | Test validation with threshold counts that pass. |
| [test_blueprint_schema.py](file:///tests/validation/test_blueprint_schema.py) | TestBlueprintSchema | `test_all_blueprints_valid` | Test that all blueprint.json files are valid against schema. |
| [test_blueprint_schema.py](file:///tests/validation/test_blueprint_schema.py) | TestBlueprintSchema | `test_blueprint_agent_references_format` | Test that agent references have correct format. |
| [test_blueprint_schema.py](file:///tests/validation/test_blueprint_schema.py) | TestBlueprintSchema | `test_blueprint_has_valid_language` | Test that blueprints have valid primary language. |
| [test_blueprint_schema.py](file:///tests/validation/test_blueprint_schema.py) | TestBlueprintSchema | `test_blueprint_ids_match_directory_names` | Test that blueprintId matches the directory name. |
| [test_blueprint_schema.py](file:///tests/validation/test_blueprint_schema.py) | TestBlueprintSchema | `test_python_fastapi_blueprint_valid` | Test that python-fastapi blueprint is valid. |
| [test_blueprint_schema.py](file:///tests/validation/test_blueprint_schema.py) | TestBlueprintSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestAgentTemplate | `test_agent_template_exists` | Test that agent template exists. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestAgentTemplate | `test_agent_template_has_frontmatter` | Test that agent template has YAML frontmatter. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestAgentTemplate | `test_agent_template_has_required_frontmatter` | Test that agent template has required frontmatter fields. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestAgentTemplate | `test_agent_template_has_sections` | Test that agent template has standard sections. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeSchema | `test_schema_exists` | Test that knowledge schema exists. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeSchema | `test_schema_has_naming_convention` | Test that schema defines naming convention. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeSchema | `test_schema_has_required_fields` | Test that schema has required fields defined. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeSchema | `test_schema_has_validation_rules` | Test that schema has validation rules. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeSchema | `test_schema_valid_json` | Test that schema is valid JSON. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeTemplate | `test_template_exists` | Test that knowledge template exists. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeTemplate | `test_template_has_patterns_array` | Test that template includes patterns array. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeTemplate | `test_template_has_placeholders` | Test that template has placeholder variables. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeTemplate | `test_template_has_required_placeholders` | Test that template has required placeholders. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestKnowledgeTemplate | `test_template_valid_json_structure` | Test that template represents valid JSON structure. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestSkillTemplate | `test_skill_template_exists` | Test that skill template exists. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestSkillTemplate | `test_skill_template_has_frontmatter` | Test that skill template has YAML frontmatter. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestSkillTemplate | `test_skill_template_has_required_frontmatter` | Test that skill template has required frontmatter fields. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestSkillTemplate | `test_skill_template_has_sections` | Test that skill template has standard sections. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestTemplateConsistency | `test_all_factory_templates_exist` | Test that all expected factory templates exist. |
| [test_extension_templates.py](file:///tests/validation/test_extension_templates.py) | TestTemplateConsistency | `test_templates_use_consistent_placeholder_style` | Test that templates use consistent placeholder style. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestAISuiteIntegrationSchema | `test_aisuite_integration_exists` | Test that aisuite-integration.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestAISuiteIntegrationSchema | `test_aisuite_integration_has_mcp_section` | Test that AISuite integration documents MCP client support. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestAISuiteIntegrationSchema | `test_aisuite_integration_has_overview` | Test that AISuite integration has overview section. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestAISuiteIntegrationSchema | `test_aisuite_integration_has_providers` | Test that AISuite integration lists supported providers. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestAISuiteIntegrationSchema | `test_aisuite_integration_valid_json` | Test that AISuite integration is valid JSON. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestBestPracticesSchema | `test_best_practices_exists` | Test that best-practices.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestBestPracticesSchema | `test_best_practices_valid_json` | Test that best practices is valid JSON. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestKnowledgeFileNaming | `test_knowledge_files_have_json_extension` | Test that knowledge files have .json extension. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestKnowledgeFileNaming | `test_knowledge_files_use_kebab_case` | Test that knowledge files use kebab-case naming. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestKnowledgeFilesStructure | `test_all_knowledge_files_valid_json` | Test that all knowledge files are valid JSON. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestKnowledgeFilesStructure | `test_knowledge_files_have_content` | Test that knowledge files are not empty. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPSelectionGuideSchema | `test_selection_guide_exists` | Test that mcp-selection-guide.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPSelectionGuideSchema | `test_selection_guide_has_category_descriptions` | Test that selection guide has category descriptions. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPSelectionGuideSchema | `test_selection_guide_has_flow` | Test that selection guide has selection flow defined. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPSelectionGuideSchema | `test_selection_guide_has_role_mappings` | Test that selection guide has role-to-server mappings. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPSelectionGuideSchema | `test_selection_guide_valid_json` | Test that selection guide is valid JSON. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_exists` | Test that mcp-servers-catalog.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_has_categories` | Test that MCP catalog defines categories. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_has_role_based_recommendations` | Test that MCP catalog has role-based server recommendations. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_has_servers` | Test that MCP catalog has servers defined. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_has_starter_packs` | Test that MCP catalog has starter packs. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_server_categories_are_valid` | Test that all server categories reference defined categories. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_servers_have_required_fields` | Test that MCP servers have required fields. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestMCPServersCatalogSchema | `test_mcp_catalog_valid_json` | Test that MCP catalog is valid JSON. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestSkillCatalogSchema | `test_skill_catalog_exists` | Test that skill-catalog.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestSkillCatalogSchema | `test_skill_catalog_has_skills` | Test that skill catalog has skills defined. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestSkillCatalogSchema | `test_skill_catalog_valid` | Test that skill catalog is valid against schema. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestSkillCatalogSchema | `test_skill_ids_match_keys` | Test that skill IDs match their dictionary keys. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestSkillCatalogSchema | `test_skills_have_categories` | Test that all skills have valid categories. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestStackCapabilitiesSchema | `test_stack_capabilities_exists` | Test that stack-capabilities.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestStackCapabilitiesSchema | `test_stack_capabilities_valid_json` | Test that stack capabilities is valid JSON. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestWorkflowPatternsSchema | `test_workflow_patterns_exists` | Test that workflow-patterns.json exists. |
| [test_knowledge_schema.py](file:///tests/validation/test_knowledge_schema.py) | TestWorkflowPatternsSchema | `test_workflow_patterns_valid_json` | Test that workflow patterns is valid JSON. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestAgentPatternSchema | `test_agent_frontmatter_type_is_agent` | Test that agent frontmatter type is 'agent'. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestAgentPatternSchema | `test_agent_pattern_ids_are_kebab_case` | Test that agent pattern IDs use kebab-case. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestAgentPatternSchema | `test_all_agent_patterns_valid` | Test that all agent patterns are valid against schema. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestAgentPatternSchema | `test_code_reviewer_pattern_valid` | Test that code-reviewer pattern is valid. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestAgentPatternSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestPatternConsistency | `test_frontmatter_name_matches_pattern_id` | Test that frontmatter name matches pattern ID. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestPatternConsistency | `test_pattern_id_matches_filename` | Test that patternId matches the filename. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestSkillPatternSchema | `test_all_skill_patterns_valid` | Test that all skill patterns are valid against schema. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestSkillPatternSchema | `test_bugfix_workflow_pattern_valid` | Test that bugfix-workflow pattern is valid. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestSkillPatternSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestSkillPatternSchema | `test_skill_frontmatter_type_is_skill` | Test that skill frontmatter type is 'skill'. |
| [test_pattern_schema.py](file:///tests/validation/test_pattern_schema.py) | TestSkillPatternSchema | `test_skill_pattern_ids_are_kebab_case` | Test that skill pattern IDs use kebab-case. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestAdapterInterfaceSchema | `test_interface_has_operations` | Test that interface defines all required operations. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestAdapterInterfaceSchema | `test_interface_is_valid_json` | Test that adapter-interface.json is valid JSON. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestAdapterInterfaceSchema | `test_operations_have_parameters` | Test that operations have parameters defined in schema. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestBackendAdaptersSchema | `test_adapters_have_mappings` | Test that all adapters define mappings. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestBackendAdaptersSchema | `test_adapters_implement_interface_operations` | Test that adapters define mappings for all required interface operations. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestBackendAdaptersSchema | `test_all_adapters_valid_json` | Test that all adapter files are valid JSON. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestBackendAdaptersSchema | `test_schema_is_valid` | Test that the backend adapter schema itself is valid. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMethodologyDefaultsSchema | `test_all_defaults_valid_json` | Test that all defaults files are valid JSON. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMethodologyDefaultsSchema | `test_defaults_have_required_fields` | Test that all defaults have required fields. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMethodologyDefaultsSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMetricsSchema | `test_all_categories_covered` | Test that all metric categories are covered. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMetricsSchema | `test_metrics_have_required_fields` | Test that all metrics have required fields. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMetricsSchema | `test_metrics_is_valid_json` | Test that pm-metrics.json is valid JSON. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestMetricsSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestPMProductSchema | `test_backends_are_valid_list` | Test that backends field is a valid list. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestPMProductSchema | `test_methodologies_are_valid_list` | Test that methodologies field is a valid list. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestPMProductSchema | `test_product_has_required_fields` | Test that product.json has all required fields. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestPMProductSchema | `test_product_json_is_valid_json` | Test that product.json is valid JSON. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestPMProductSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestQuestionnaireSchema | `test_questionnaire_has_questions` | Test that questionnaire has questions field. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestQuestionnaireSchema | `test_questionnaire_is_valid_json` | Test that questionnaire.json is valid JSON. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestQuestionnaireSchema | `test_questions_have_required_fields` | Test that all questions have required fields. |
| [test_pm_schema.py](file:///tests/validation/test_pm_schema.py) | TestQuestionnaireSchema | `test_schema_is_valid` | Test that the schema itself is valid. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_agents_directory_exists` | Test that .agent/agents directory exists. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_blueprints_directory_exists` | Test that blueprints directory exists. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_has_minimum_agents` | Test that project has at least some agents defined. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_has_minimum_blueprints` | Test that project has at least some blueprints defined. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_has_minimum_skills` | Test that project has at least some skills defined. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_knowledge_directory_exists` | Test that knowledge directory exists. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_patterns_directory_exists` | Test that patterns directory exists. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_skills_directory_exists` | Test that .agent/skills directory exists. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestProjectComponentsExist | `test_templates_directory_exists` | Test that templates directory exists. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeExists | `test_readme_exists` | Test that README.md exists in project root. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeExists | `test_readme_has_content` | Test that README.md has content. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeExists | `test_readme_has_project_structure_section` | Test that README.md has a Project Structure section. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_agents_count` | Test that agents count in README matches filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_blueprints_count` | Test that blueprints count in README matches filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_knowledge_count` | Test that knowledge files count in README matches filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_patterns_count` | Test that patterns count in README matches filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_skills_count` | Test that skills count in README matches filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_structure_counts_match_filesystem` | Test that all README counts match actual filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestReadmeStructureCounts | `test_readme_templates_count` | Test that templates count in README matches filesystem. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_extract_readme_counts` | Test that extract_readme_counts parses README correctly. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_generate_counts_summary` | Test that generate_counts_summary returns integer counts. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_agents_returns_dict` | Test that scan_agents returns expected structure. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_all_returns_complete_structure` | Test that scan_all returns all component categories. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_blueprints_returns_dict` | Test that scan_blueprints returns expected structure. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_knowledge_returns_dict` | Test that scan_knowledge returns expected structure. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_patterns_returns_dict` | Test that scan_patterns returns expected structure. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_skills_returns_dict` | Test that scan_skills returns expected structure. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_scan_templates_returns_dict` | Test that scan_templates returns expected structure. |
| [test_readme_structure.py](file:///tests/validation/test_readme_structure.py) | TestStructureValidatorFunctionality | `test_validate_returns_tuple` | Test that validate returns expected tuple structure. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_domains_have_topics` | Test that domains have topics or subtopics. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_has_domains` | Test that taxonomy has domains defined. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_has_required_fields` | Test that taxonomy has required top-level fields. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_keywords_are_lists` | Test that keywords fields are lists of strings. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_knowledge_files_are_lists` | Test that knowledge_files fields are lists of strings. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_taxonomy_file_exists` | Test that agent_taxonomy.json exists. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_taxonomy_valid_json` | Test that taxonomy file is valid JSON. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestAgentTaxonomyStructure | `test_topics_have_required_depth` | Test that topics define required_depth. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestTaxonomyMetadata | `test_coverage_scale_has_levels` | Test that coverage scale defines levels 0-3. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestTaxonomyMetadata | `test_has_coverage_scale` | Test that metadata defines coverage scale. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestTaxonomyMetadata | `test_has_metadata` | Test that taxonomy has metadata section. |
| [test_taxonomy_schema.py](file:///tests/validation/test_taxonomy_schema.py) | TestTaxonomyMetadata | `test_has_version` | Test that taxonomy has version field. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_alignment_check_skill` | Test that all 27 blueprints have alignment-check skill. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_all_standard_agents` | Test that all blueprints have all standard agents. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_all_standard_skills` | Test that all blueprints have all standard skills. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_ci_monitor_project_skill` | Test that all 27 blueprints have ci-monitor-project skill. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_debug_conductor_project_agent` | Test that all 27 blueprints have debug-conductor-project agent. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_grounding_verification_skill` | Test that all 27 blueprints have grounding-verification skill. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_knowledge_evolution_agent` | Test that all 27 blueprints have knowledge-evolution agent. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_knowledge_extender_agent` | Test that all 27 blueprints have knowledge-extender agent. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_pipeline_error_fix_project_skill` | Test that all 27 blueprints have pipeline-error-fix-project skill. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_pm_integration_section` | Test that all 27 blueprints have pmIntegration section. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestBlueprintCompleteness | `test_all_blueprints_have_research_first_project_skill` | Test that all 27 blueprints have research-first-project skill. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestGenerationScriptValidation | `test_generate_project_adds_standard_agents` | Test that generate_project.py adds standard agents to agents list. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestGenerationScriptValidation | `test_generate_project_adds_standard_skills` | Test that generate_project.py adds standard skills to skills list. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestGenerationScriptValidation | `test_generate_project_checks_pm_integration_enabled` | Test that scripts/core/generate_project.py checks pmIntegration.enabled. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestGenerationScriptValidation | `test_generate_project_includes_standard_agents_list` | Test that scripts/core/generate_project.py includes standard_agents list. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestGenerationScriptValidation | `test_generate_project_includes_standard_skills_list` | Test that scripts/core/generate_project.py includes standard_skills list. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_alignment_check_pattern_exists` | Test that patterns/skills/alignment-check.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_all_agent_patterns_exist` | Test that all expected agent pattern files exist and are valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_all_skill_patterns_exist` | Test that all expected skill pattern files exist and are valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_ci_monitor_project_pattern_exists` | Test that patterns/skills/ci-monitor-project.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_debug_conductor_project_pattern_exists` | Test that patterns/agents/debug-conductor-project.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_grounding_verification_pattern_exists` | Test that patterns/skills/grounding-verification.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_knowledge_evolution_pattern_exists` | Test that patterns/agents/knowledge-evolution.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_knowledge_extender_pattern_exists` | Test that patterns/agents/knowledge-extender.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_pipeline_error_fix_project_pattern_exists` | Test that patterns/skills/pipeline-error-fix-project.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternFileExistence | `test_research_first_project_pattern_exists` | Test that patterns/skills/research-first-project.json exists and is valid JSON. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternSchemaValidation | `test_patterns_have_frontmatter_with_name_and_description` | Test that each pattern has frontmatter with name and description. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternSchemaValidation | `test_patterns_have_required_metadata` | Test that each pattern has required metadata fields. |
| [test_value_propagation.py](file:///tests/validation/test_value_propagation.py) | TestPatternSchemaValidation | `test_patterns_have_sections` | Test that each pattern has sections. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowCategories | `test_agile_workflows_exist` | Test that agile workflows exist. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowCategories | `test_domain_workflows_exist` | Test that domain-specific workflow directories exist. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowCategories | `test_operations_workflows_exist` | Test that operations workflows exist. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowCategories | `test_quality_workflows_exist` | Test that quality workflows exist. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowCategories | `test_universal_workflows_exist` | Test that universal workflows exist. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowContent | `test_no_broken_internal_links` | Test that workflows don't have obviously broken links. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowContent | `test_workflows_have_fallback_procedures` | Test that workflows have fallback procedures. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowContent | `test_workflows_have_trigger_examples` | Test that workflows provide trigger examples. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowContent | `test_workflows_have_version` | Test that workflows declare a version. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowIntegration | `test_workflow_patterns_doc_exists` | Test that WORKFLOW_PATTERNS.md documentation exists. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowIntegration | `test_workflow_patterns_json_exists` | Test that workflow-patterns.json exists and is valid JSON. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowIntegration | `test_workflow_patterns_reference_workflows` | Test that workflow patterns reference existing workflows. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_all_workflows_have_decision_points` | Test that all workflows have Decision Points section. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_all_workflows_have_example_session` | Test that all workflows have an Example Session section. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_all_workflows_have_overview` | Test that all workflows have an Overview section. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_all_workflows_have_phases` | Test that all workflows have Phases section. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_all_workflows_have_title` | Test that all workflows have a markdown title. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_all_workflows_have_trigger_conditions` | Test that all workflows have Trigger Conditions section. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_minimum_workflow_count` | Test that we have the expected minimum number of workflows. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_workflow_files_exist` | Test that workflow files exist. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_workflow_naming_convention` | Test that workflow files use kebab-case naming. |
| [test_workflow_structure.py](file:///tests/validation/test_workflow_structure.py) | TestWorkflowStructure | `test_workflows_directory_exists` | Test that workflows directory exists. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestAllProjectFilesValid | `test_all_agent_files_have_valid_yaml` | Test that all agent files have valid YAML frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestAllProjectFilesValid | `test_all_docs_have_valid_yaml` | Test that all doc files have valid YAML frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestAllProjectFilesValid | `test_all_markdown_files_valid` | Comprehensive test: all markdown files in standard locations are valid. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestAllProjectFilesValid | `test_all_skill_files_have_valid_yaml` | Test that all skill files have valid YAML frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestEdgeCases | `test_empty_frontmatter` | Test handling of empty frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestEdgeCases | `test_frontmatter_with_comments` | Test that YAML comments are handled. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestEdgeCases | `test_frontmatter_with_nested_objects` | Test handling of nested YAML objects. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestEdgeCases | `test_unreadable_file` | Test handling of file read errors. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFileValidation | `test_validate_file_with_invalid_frontmatter` | Test validation of file with invalid frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFileValidation | `test_validate_file_with_valid_frontmatter` | Test validation of file with valid frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFileValidation | `test_validate_file_without_frontmatter` | Test validation of file without frontmatter (should pass). |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFindMarkdownFiles | `test_find_markdown_files_all_are_md` | Test that all found files are markdown files. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFindMarkdownFiles | `test_find_markdown_files_includes_agents` | Test that agent files are included. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFindMarkdownFiles | `test_find_markdown_files_includes_skills` | Test that skill files are included. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFindMarkdownFiles | `test_find_markdown_files_returns_list` | Test that find_markdown_files returns a list. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFrontmatterExtraction | `test_extract_frontmatter_only_at_start` | Test that frontmatter must be at the start of the file. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFrontmatterExtraction | `test_extract_multiline_frontmatter` | Test extraction of multiline frontmatter values. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFrontmatterExtraction | `test_extract_no_frontmatter` | Test extraction when no frontmatter exists. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestFrontmatterExtraction | `test_extract_valid_frontmatter` | Test extraction of valid frontmatter. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestYamlSyntaxValidation | `test_invalid_comma_separated_strings` | Test detection of comma-separated quoted strings (common error). |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestYamlSyntaxValidation | `test_invalid_tab_indentation` | Test detection of tab characters. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestYamlSyntaxValidation | `test_unbalanced_quotes` | Test detection of unbalanced quotes. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestYamlSyntaxValidation | `test_valid_simple_yaml` | Test that valid simple YAML passes. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestYamlSyntaxValidation | `test_valid_yaml_with_array` | Test that valid YAML array syntax passes. |
| [test_yaml_frontmatter.py](file:///tests/validation/test_yaml_frontmatter.py) | TestYamlSyntaxValidation | `test_valid_yaml_with_special_chars` | Test that valid YAML with special characters passes. |
<!-- SYNC_END -->

## Methodology

Every test case starting with `test_` in the `tests/` directory is scanned using Python's AST (Abstract Syntax Tree) module. 
The first line of the function's docstring is extracted as the description. 
This ensures that our test documentation is always "live" and reflects the actual source code.
