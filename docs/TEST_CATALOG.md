# Test Catalog

> **Auto-generated** from test suite on 2026-02-08 23:10.
> Do not edit manually. Run `python scripts/docs/generate_test_catalog.py` to regenerate.

## Overview

The test suite contains **1536 tests** across **52 files**.

### Summary by Category

| Category | Files | Tests |
|----------|-------|-------|
| Unit Tests | 23 | 832 |
| Integration Tests | 6 | 121 |
| Validation Tests | 9 | 186 |
| Guardian Tests | 1 | 9 |
| Memory Tests | 3 | 45 |
| Library Tests | 10 | 343 |
| **Total** | **52** | **1536** |

## Unit Tests

**Directory:** `tests/unit/`
**Files:** 23 | **Tests:** 832

### test_adapters.py

**Purpose:** Unit Tests for Knowledge Source Adapters

**Path:** `tests/unit\test_adapters.py`
**Tests:** 21

| Class | Tests | Description |
|-------|-------|-------------|
| `TestAdapterConfig` | 2 | Tests for AdapterConfig dataclass. |
| `TestUpdateSource` | 2 | Tests for UpdateSource dataclass. |
| `TestKnowledgeChange` | 2 | Tests for KnowledgeChange dataclass. |
| `TestKnowledgeUpdate` | 3 | Tests for KnowledgeUpdate dataclass. |
| `TestUpdatePriority` | 1 | Tests for UpdatePriority enum. |
| `TestTrustLevel` | 1 | Tests for TrustLevel enum. |
| `TestBaseAdapter` | 4 | Tests for BaseAdapter abstract class. |
| `TestGitHubAdapter` | 2 | Tests for GitHub adapter. |
| `TestPyPIAdapter` | 2 | Tests for PyPI adapter. |
| `TestNPMAdapter` | 2 | Tests for NPM adapter. |

### test_adapters_mocked.py

**Purpose:** Comprehensive Unit Tests for Knowledge Source Adapters with HTTP Mocking

**Path:** `tests/unit\test_adapters_mocked.py`
**Tests:** 50

| Class | Tests | Description |
|-------|-------|-------------|
| `TestPyPIAdapterMocked` | 11 | Comprehensive mocked tests for PyPIAdapter. |
| `TestNPMAdapterMocked` | 5 | Comprehensive mocked tests for NPMAdapter. |
| `TestGitHubAdapterMocked` | 11 | Comprehensive mocked tests for GitHubAdapter. |
| `TestDocsAdapterMocked` | 2 | Comprehensive mocked tests for DocsAdapter. |
| `TestFeedbackAdapterMocked` | 15 | Comprehensive mocked tests for FeedbackAdapter. |
| `TestBaseAdapterCaching` | 6 | Tests for BaseAdapter caching functionality. |

### test_backup_manager.py

**Purpose:** Unit tests for scripts/git/backup_manager.py

**Path:** `tests/unit\test_backup_manager.py`
**Tests:** 32

| Class | Tests | Description |
|-------|-------|-------------|
| `TestBackupEntry` | 2 | Tests for BackupEntry dataclass. |
| `TestBackupManifest` | 4 | Tests for BackupManifest dataclass. |
| `TestBackupSession` | 7 | Tests for BackupSession class. |
| `TestBackupManager` | 13 | Tests for BackupManager class. |
| `TestEnsureGitignoreExcludesBackup` | 3 | Tests for ensure_gitignore_excludes_backup function. |
| `TestMainEntry` | 3 | Tests for command-line interface. |

### test_conflict_resolver.py

**Purpose:** Unit tests for scripts/git/conflict_resolver.py

**Path:** `tests/unit\test_conflict_resolver.py`
**Tests:** 91

| Class | Tests | Description |
|-------|-------|-------------|
| `TestConflictType` | 2 | Tests for ConflictType enum. |
| `TestResolutionStrategy` | 2 | Tests for ResolutionStrategy enum. |
| `TestConflict` | 4 | Tests for Conflict dataclass. |
| `TestConflictReport` | 6 | Tests for ConflictReport dataclass. |
| `TestConflictResolverInitialization` | 4 | Tests for ConflictResolver initialization. |
| `TestConflictDetection` | 10 | Tests for conflict detection logic. |
| `TestConflictResolutionStrategies` | 5 | Tests for resolution strategy suggestions. |
| `TestAutoResolution` | 4 | Tests for automatic conflict resolution. |
| `TestConflictResolution` | 10 | Tests for resolving conflicts and producing merged content. |
| `TestHelperMethods` | 6 | Tests for helper methods. |
| `TestEdgeCases` | 20 | Tests for edge cases and error handling. |
| `TestConflictResolutionAdvanced` | 8 | Advanced tests for conflict resolution. |
| `TestConflictReportAdvanced` | 5 | Advanced tests for ConflictReport. |
| `TestPathHelpers` | 3 | Tests for path helper methods. |
| `TestIntegrationScenarios` | 2 | Integration tests for real-world scenarios. |

### test_dependency_validator.py

**Purpose:** Unit tests for DependencyValidator and related classes.

**Path:** `tests/unit\test_dependency_validator.py`
**Tests:** 86

| Class | Tests | Description |
|-------|-------|-------------|
| `TestEdgeType` | 2 | Tests for EdgeType enum. |
| `TestNodeType` | 2 | Tests for NodeType enum. |
| `TestDependencyNode` | 3 | Tests for DependencyNode dataclass. |
| `TestDependencyEdge` | 4 | Tests for DependencyEdge dataclass. |
| `TestValidationResult` | 7 | Tests for ValidationResult dataclass. |
| `TestDependencyValidatorInit` | 1 | Tests for DependencyValidator initialization. |
| `TestDependencyValidatorScanKnowledge` | 6 | Tests for _scan_knowledge_files method. |
| `TestDependencyValidatorScanSkills` | 6 | Tests for _scan_skills method. |
| `TestDependencyValidatorScanAgents` | 4 | Tests for _scan_agents method. |
| `TestDependencyValidatorScanBlueprints` | 7 | Tests for _scan_blueprints method. |
| `TestDependencyValidatorParseFrontmatter` | 4 | Tests for _parse_frontmatter method. |
| `TestDependencyValidatorBuildAdjacency` | 1 | Tests for _build_adjacency method. |
| `TestDependencyValidatorDetectCycles` | 5 | Tests for detect_cycles method. |
| `TestDependencyValidatorFindBrokenRefs` | 3 | Tests for find_broken_refs method. |
| `TestDependencyValidatorFindMissingRefs` | 3 | Tests for find_missing_refs method. |
| `TestDependencyValidatorValidateVersions` | 6 | Tests for validate_versions method. |
| `TestDependencyValidatorValidate` | 5 | Tests for validate method. |
| `TestDependencyValidatorReverseLookup` | 2 | Tests for reverse_lookup method. |
| `TestDependencyValidatorImpactAnalysis` | 4 | Tests for impact_analysis method. |
| `TestDependencyValidatorGetInstallOrder` | 2 | Tests for get_install_order method. |
| `TestDependencyValidatorGetStatistics` | 4 | Tests for get_statistics method. |
| `TestDependencyValidatorExportGraph` | 3 | Tests for export_graph method. |
| `TestDependencyValidatorScanArtifacts` | 2 | Tests for scan_artifacts method. |

### test_factory_cli.py

**Purpose:** Unit tests for cli/factory_cli.py

**Path:** `tests/unit\test_factory_cli.py`
**Tests:** 41

| Class | Tests | Description |
|-------|-------|-------------|
| `TestGetFactoryRoot` | 3 | Tests for get_factory_root function. |
| `TestDisplayWelcome` | 1 | Tests for display_welcome function. |
| `TestDisplayTour` | 1 | Tests for display_tour function. |
| `TestDisplayErrorWithHelp` | 1 | Tests for display_error_with_help function. |
| `TestListBlueprints` | 2 | Tests for list_blueprints function. |
| `TestListPatterns` | 2 | Tests for list_patterns function. |
| `TestRunQuickstart` | 4 | Tests for run_quickstart function. |
| `TestInteractiveMode` | 3 | Tests for interactive_mode function. |
| `TestGenerateFromBlueprint` | 4 | Tests for generate_from_blueprint function. |
| `TestGenerateFromConfigFile` | 2 | Tests for generate_from_config_file function. |
| `TestAnalyzeRepository` | 2 | Tests for analyze_repository function. |
| `TestOnboardRepository` | 3 | Tests for onboard_repository function. |
| `TestRollbackSession` | 2 | Tests for rollback_session function. |
| `TestCreateDefaultConfig` | 1 | Tests for _create_default_config function. |
| `TestInteractiveConflictResolver` | 2 | Tests for _interactive_conflict_resolver function. |
| `TestMain` | 8 | Tests for main function. |

### test_gap_types.py

**Purpose:** Unit tests for gap types and enums in scripts/analysis/knowledge_gap_analyzer.py

**Path:** `tests/unit\test_gap_types.py`
**Tests:** 10

| Class | Tests | Description |
|-------|-------|-------------|
| `TestGapType` | 5 | Tests for GapType enumeration. |
| `TestGapPriority` | 5 | Tests for GapPriority enumeration. |

### test_guardian_axiom_checker.py

**Purpose:** Unit tests for the Guardian Axiom Checker.

**Path:** `tests/unit\test_guardian_axiom_checker.py`
**Tests:** 18

| Class | Tests | Description |
|-------|-------|-------------|
| `TestCheckCommand` | 3 | Tests for shell command checking. |
| `TestCheckFileOperation` | 3 | Tests for file operation checking. |
| `TestCheckContentForClaims` | 1 | Tests for content claim checking (A1 - Verifiability). |
| `TestValidateOperation` | 4 | Tests for the main validation entry point. |
| `TestCheckResultProperties` | 4 | Tests for CheckResult helper properties. |
| `TestAxiomCoverage` | 3 | Tests to ensure all axioms are being checked. |

### test_guardian_secret_scanner.py

**Purpose:** Unit tests for the Guardian Secret Scanner.

**Path:** `tests/unit\test_guardian_secret_scanner.py`
**Tests:** 18

| Class | Tests | Description |
|-------|-------|-------------|
| `TestScanContent` | 6 | Tests for content scanning. |
| `TestRedactSecret` | 2 | Tests for secret redaction. |
| `TestIsFalsePositive` | 1 | Tests for false positive detection. |
| `TestScanDiff` | 2 | Tests for git diff scanning. |
| `TestGetSeverityLevel` | 5 | Tests for severity to Guardian level mapping. |
| `TestScanFile` | 2 | Tests for file scanning. |

### test_install_hooks.py

**Purpose:** Unit tests for scripts/git/install_hooks.py

**Path:** `tests/unit\test_install_hooks.py`
**Tests:** 14

| Class | Tests | Description |
|-------|-------|-------------|
| `TestPreCommitHookContent` | 8 | Tests for the pre-commit hook content. |
| `TestInstallHooks` | 5 | Tests for the install_hooks function. |
| `TestMainEntry` | 1 | Tests for the main entry point. |

### test_knowledge_gap_analyzer.py

**Purpose:** Unit tests for scripts/analysis/knowledge_gap_analyzer.py

**Path:** `tests/unit\test_knowledge_gap_analyzer.py`
**Tests:** 31

| Class | Tests | Description |
|-------|-------|-------------|
| `TestCoverageScore` | 7 | Tests for CoverageScore dataclass. |
| `TestKnowledgeGap` | 3 | Tests for KnowledgeGap dataclass. |
| `TestAnalysisResult` | 6 | Tests for AnalysisResult dataclass. |
| `TestKnowledgeGapAnalyzer` | 13 | Tests for KnowledgeGapAnalyzer class. |
| `TestRunGapAnalysis` | 2 | Tests for run_gap_analysis convenience function. |

### test_pattern_loading.py

**Purpose:** Unit tests for pattern and blueprint loading functionality.

**Path:** `tests/unit\test_pattern_loading.py`
**Tests:** 13

| Class | Tests | Description |
|-------|-------|-------------|
| `TestBlueprintFiles` | 3 | Tests for blueprint file loading. |
| `TestAgentPatternFiles` | 3 | Tests for agent pattern file loading. |
| `TestSkillPatternFiles` | 3 | Tests for skill pattern file loading. |
| `TestKnowledgeFiles` | 2 | Tests for knowledge file loading. |
| `TestPatternConsistency` | 2 | Tests for pattern consistency across the factory. |

### test_pm_adapters.py

**Purpose:** Unit tests for PM adapter JSON files.

**Path:** `tests/unit\test_pm_adapters.py`
**Tests:** 31

| Class | Tests | Description |
|-------|-------|-------------|
| `TestAdapterInterface` | 7 | Tests for adapter-interface.json structure. |
| `TestGitHubAdapter` | 6 | Tests for github-adapter.json mappings. |
| `TestJiraAdapter` | 6 | Tests for jira-adapter.json mappings. |
| `TestAzureDevOpsAdapter` | 5 | Tests for azure-devops-adapter.json mappings. |
| `TestLinearAdapter` | 4 | Tests for linear-adapter.json mappings. |
| `TestAdapterConsistency` | 3 | Cross-adapter consistency tests. |

### test_pm_config.py

**Purpose:** Unit tests for PM configuration fields in ProjectConfig.

**Path:** `tests/unit\test_pm_config.py`
**Tests:** 10

| Class | Tests | Description |
|-------|-------|-------------|
| `TestPMConfigFields` | 4 | Tests for PM fields in ProjectConfig. |
| `TestPMConfigFromDict` | 3 | Tests for from_dict with PM fields. |
| `TestPMAgentSkillExtension` | 3 | Tests for agent/skill lists when PM is enabled. |

### test_project_config.py

**Purpose:** Unit tests for ProjectConfig dataclass.

**Path:** `tests/unit\test_project_config.py`
**Tests:** 19

| Class | Tests | Description |
|-------|-------|-------------|
| `TestProjectConfigInstantiation` | 3 | Tests for direct ProjectConfig instantiation. |
| `TestProjectConfigFromDict` | 5 | Tests for ProjectConfig.from_dict() factory method. |
| `TestProjectConfigFromYaml` | 4 | Tests for ProjectConfig.from_yaml_file() factory method. |
| `TestProjectConfigFromJson` | 5 | Tests for ProjectConfig.from_json_file() factory method. |
| `TestProjectConfigDefaults` | 2 | Tests for default value handling. |

### test_research_first_pattern.py

**Purpose:** Tests for the Research-First Development Pattern.

**Path:** `tests/unit\test_research_first_pattern.py`
**Tests:** 26

| Class | Tests | Description |
|-------|-------|-------------|
| `TestKnowledgeFileStructure` | 4 | Tests for knowledge file schema compliance. |
| `TestWorkflowSteps` | 6 | Tests for required workflow steps. |
| `TestTriggerDefinitions` | 4 | Tests for when the pattern should be applied. |
| `TestBenefitsDocumentation` | 2 | Tests for benefit documentation. |
| `TestAntiPatterns` | 3 | Tests for anti-pattern documentation. |
| `TestIntegrationPoints` | 3 | Tests for integration with agents and skills. |
| `TestExamples` | 2 | Tests for example usage. |
| `TestGeneratedProjectAvailability` | 2 | Tests for availability in generated projects. |

### test_sync_artifacts.py

**Purpose:** Tests for scripts/validation/sync_artifacts.py

**Path:** `tests/unit\test_sync_artifacts.py`
**Tests:** 40

| Class | Tests | Description |
|-------|-------|-------------|
| `TestArtifactScanner` | 5 | Tests for the ArtifactScanner class. |
| `TestCountSyncStrategy` | 4 | Tests for the CountSyncStrategy class. |
| `TestJsonFieldSyncStrategy` | 2 | Tests for the JsonFieldSyncStrategy class. |
| `TestSyncEngine` | 4 | Tests for the SyncEngine class. |
| `TestIntegration` | 6 | Integration tests using actual project files. |
| `TestDirectoryDetection` | 2 | Tests for directory-based sync triggering. |
| `TestCategoryTestCounts` | 2 | Tests for the CategoryTestCounts NamedTuple. |
| `TestGetPythonPath` | 1 | Tests for Python path detection. |
| `TestCollectTestCount` | 5 | Tests for test count collection. |
| `TestExtractDocumentedCounts` | 4 | Tests for extracting counts from TESTING.md content. |
| `TestUpdateTestingMd` | 5 | Tests for updating TESTING.md. |

### test_sync_knowledge_counts.py

**Purpose:** Tests for scripts/validation/sync_knowledge_counts.py

**Path:** `tests/unit\test_sync_knowledge_counts.py`
**Tests:** 21

| Class | Tests | Description |
|-------|-------|-------------|
| `TestCountKnowledgeFiles` | 4 | Tests for counting knowledge files. |
| `TestGetManifestCount` | 3 | Tests for extracting count from manifest.json. |
| `TestGetDocsCount` | 3 | Tests for extracting count from KNOWLEDGE_FILES.md. |
| `TestUpdateManifest` | 3 | Tests for updating manifest.json. |
| `TestUpdateDocs` | 2 | Tests for updating KNOWLEDGE_FILES.md. |
| `TestSyncKnowledgeCounts` | 2 | Tests for the main sync function. |
| `TestIntegration` | 4 | Integration tests using actual project files. |

### test_sync_test_counts.py

**Purpose:** Tests for test count synchronization functionality.

**Path:** `tests/unit\test_sync_test_counts.py`
**Tests:** 23

| Class | Tests | Description |
|-------|-------|-------------|
| `TestCategoryTestCounts` | 3 | Tests for the CategoryTestCounts NamedTuple. |
| `TestGetPythonPath` | 2 | Tests for Python path detection. |
| `TestCollectTestCount` | 5 | Tests for test count collection. |
| `TestExtractDocumentedCounts` | 4 | Tests for extracting counts from TESTING.md content. |
| `TestUpdateTestingMd` | 5 | Tests for updating TESTING.md. |
| `TestIntegration` | 4 | Integration tests using actual project files. |

### test_taxonomy.py

**Purpose:** Unit tests for scripts/taxonomy/__init__.py

**Path:** `tests/unit\test_taxonomy.py`
**Tests:** 21

| Class | Tests | Description |
|-------|-------|-------------|
| `TestTopicNode` | 9 | Tests for TopicNode dataclass. |
| `TestTaxonomyLoader` | 9 | Tests for TaxonomyLoader class. |
| `TestLoadAgentTaxonomy` | 3 | Tests for the load_agent_taxonomy convenience function. |

### test_template_engine.py

**Purpose:** Unit tests for TemplateEngine class and custom filters.

**Path:** `tests/unit\test_template_engine.py`
**Tests:** 63

| Class | Tests | Description |
|-------|-------|-------------|
| `TestSnakeCaseFilter` | 5 | Tests for snake_case filter. |
| `TestPascalCaseFilter` | 4 | Tests for pascal_case filter. |
| `TestCamelCaseFilter` | 3 | Tests for camel_case filter. |
| `TestKebabCaseFilter` | 3 | Tests for kebab_case filter. |
| `TestTitleCaseFilter` | 3 | Tests for title_case filter. |
| `TestPluralizeFilter` | 5 | Tests for pluralize filter. |
| `TestQuoteFilter` | 3 | Tests for quote filter. |
| `TestIndentTextFilter` | 3 | Tests for indent_text filter. |
| `TestWrapCodeFilter` | 2 | Tests for wrap_code filter. |
| `TestDefaultIfEmptyFilter` | 4 | Tests for default_if_empty filter. |
| `TestJoinLinesFilter` | 3 | Tests for join_lines filter. |
| `TestToJsonFilter` | 2 | Tests for to_json filter. |
| `TestToYamlListFilter` | 2 | Tests for to_yaml_list filter. |
| `TestNowGlobal` | 2 | Tests for now() global function. |
| `TestEnvGlobal` | 2 | Tests for env() global function. |
| `TestRangeListGlobal` | 2 | Tests for range_list() global function. |
| `TestTemplateEngineInit` | 4 | Tests for TemplateEngine initialization. |
| `TestTemplateEngineRenderString` | 6 | Tests for render_string method. |
| `TestTemplateEngineRenderFile` | 1 | Tests for render_file method. |
| `TestTemplateEngineAddFilter` | 1 | Tests for add_filter method. |
| `TestTemplateEngineAddGlobal` | 1 | Tests for add_global method. |
| `TestTemplateEngineGetVariables` | 1 | Tests for get_template_variables method. |
| `TestCreateEngine` | 1 | Tests for create_engine convenience function. |

### test_update_engine.py

**Purpose:** Comprehensive unit tests for the scripts/updates/ module.

**Path:** `tests/unit\test_update_engine.py`
**Tests:** 110

| Class | Tests | Description |
|-------|-------|-------------|
| `TestChangelogEntry` | 2 | Tests for ChangelogEntry dataclass. |
| `TestChangelogGeneratorInit` | 2 | Tests for ChangelogGenerator initialization. |
| `TestChangelogGeneratorPaths` | 2 | Tests for changelog path methods. |
| `TestChangelogGeneratorLoadSave` | 3 | Tests for loading and saving changelogs. |
| `TestChangelogGeneratorCreateEntry` | 3 | Tests for creating changelog entries. |
| `TestChangelogGeneratorAppend` | 3 | Tests for appending entries. |
| `TestChangelogGeneratorMarkdown` | 4 | Tests for markdown generation. |
| `TestChangelogGeneratorSummary` | 3 | Tests for summary generation. |
| `TestChangelogGeneratorVersionDiff` | 2 | Tests for version diff functionality. |
| `TestNotification` | 3 | Tests for Notification dataclass. |
| `TestNotificationSystemInit` | 2 | Tests for NotificationSystem initialization. |
| `TestNotificationSystemNotify` | 6 | Tests for notification delivery. |
| `TestNotificationSystemHistory` | 7 | Tests for notification history management. |
| `TestNotificationSystemCallbacks` | 2 | Tests for callback management. |
| `TestNotificationSystemSpecialized` | 8 | Tests for specialized notification methods. |
| `TestSourceHealth` | 1 | Tests for SourceHealth dataclass. |
| `TestAggregationResult` | 5 | Tests for AggregationResult dataclass. |
| `TestSourceAggregatorInit` | 2 | Tests for SourceAggregator initialization. |
| `TestSourceAggregatorGetAdapter` | 2 | Tests for getting adapters. |
| `TestUpdateOperation` | 2 | Tests for UpdateOperation dataclass. |
| `TestUpdateResult` | 1 | Tests for UpdateResult dataclass. |
| `TestBatchUpdateResult` | 2 | Tests for BatchUpdateResult dataclass. |
| `TestUpdateEngineInit` | 2 | Tests for UpdateEngine initialization. |
| `TestUpdateEngineBackup` | 5 | Tests for backup management. |
| `TestUpdateEngineApplyUpdate` | 6 | Tests for applying updates. |
| `TestUpdateEngineMergeStrategies` | 3 | Tests for different merge strategies. |
| `TestUpdateEngineBatch` | 2 | Tests for batch updates. |
| `TestUpdateEngineRollback` | 4 | Tests for rollback functionality. |
| `TestUpdateEngineHistory` | 1 | Tests for update history. |
| `TestUpdateEngineValidation` | 5 | Tests for content validation. |
| `TestChangelogGeneratorEdgeCases` | 4 | Additional edge case tests for ChangelogGenerator. |
| `TestNotificationSystemEdgeCases` | 3 | Additional edge case tests for NotificationSystem. |
| `TestSourceAggregatorEdgeCases` | 2 | Additional edge case tests for SourceAggregator. |
| `TestUpdateEngineEdgeCases` | 6 | Additional edge case tests for UpdateEngine. |

### test_validate_readme.py

**Purpose:** Unit tests for scripts/validation/validate_readme_structure.py

**Path:** `tests/unit\test_validate_readme.py`
**Tests:** 43

| Class | Tests | Description |
|-------|-------|-------------|
| `TestStructureValidatorInit` | 2 | Tests for StructureValidator initialization. |
| `TestShouldIgnore` | 5 | Tests for _should_ignore method. |
| `TestCountFilesByExtension` | 3 | Tests for _count_files_by_extension method. |
| `TestScanAgents` | 2 | Tests for scan_agents method. |
| `TestScanSkills` | 2 | Tests for scan_skills method. |
| `TestScanBlueprints` | 2 | Tests for scan_blueprints method. |
| `TestScanPatterns` | 2 | Tests for scan_patterns method. |
| `TestScanKnowledge` | 2 | Tests for scan_knowledge method. |
| `TestScanTemplates` | 2 | Tests for scan_templates method. |
| `TestScanAll` | 1 | Tests for scan_all method. |
| `TestRoundToThreshold` | 3 | Tests for _round_to_threshold method. |
| `TestGenerateCountsSummary` | 1 | Tests for generate_counts_summary method. |
| `TestExtractReadmeCounts` | 3 | Tests for extract_readme_counts method. |
| `TestValidate` | 2 | Tests for validate method. |
| `TestUpdateReadme` | 3 | Tests for update_readme method. |
| `TestGenerateStructureMarkdown` | 2 | Tests for generate_structure_markdown method. |
| `TestMain` | 6 | Tests for main function. |

## Integration Tests

**Directory:** `tests/integration/`
**Files:** 6 | **Tests:** 121

### test_cli_extension.py

**Purpose:** Integration tests for CLI extension commands.

**Path:** `tests/integration\test_cli_extension.py`
**Tests:** 11

| Class | Tests | Description |
|-------|-------|-------------|
| `TestAnalyzeGapsCommand` | 5 | Tests for --analyze-gaps CLI command. |
| `TestCoverageReportCommand` | 2 | Tests for --coverage-report CLI command. |
| `TestSuggestExtensionsCommand` | 2 | Tests for --suggest-extensions CLI command. |
| `TestHelpExtensionCommands` | 2 | Tests for extension command help. |

### test_cli_pm.py

**Purpose:** Integration tests for PM (Project Management) CLI functionality.

**Path:** `tests/integration\test_cli_pm.py`
**Tests:** 9

| Class | Tests | Description |
|-------|-------|-------------|
| `TestPMHelpOutput` | 4 | Tests for PM help output in CLI. |
| `TestPMBlueprintGeneration` | 3 | Tests for PM-enabled blueprint generation. |
| `TestPMBackendValidation` | 2 | Tests for PM backend and methodology validation. |

### test_gap_analysis_e2e.py

**Purpose:** End-to-end integration tests for gap analysis workflow.

**Path:** `tests/integration\test_gap_analysis_e2e.py`
**Tests:** 13

| Class | Tests | Description |
|-------|-------|-------------|
| `TestGapAnalysisWorkflow` | 5 | End-to-end tests for gap analysis workflow. |
| `TestExtensionCandidates` | 4 | Tests for extension candidate selection. |
| `TestRunGapAnalysisFunction` | 2 | Tests for the run_gap_analysis convenience function. |
| `TestTaxonomyIntegration` | 2 | Tests for taxonomy loading integration. |

### test_society_blueprint_generation.py

**Purpose:** Integration Tests for Society Blueprint Generation.

**Path:** `tests/integration\test_society_blueprint_generation.py`
**Tests:** 25

| Class | Tests | Description |
|-------|-------|-------------|
| `TestBlueprintSocietyIntegration` | 6 | Tests for society integration in blueprints. |
| `TestSocietyTemplatesExist` | 3 | Verify all required society templates exist. |
| `TestASPKnowledgeFilesExist` | 4 | Verify all ASP knowledge files exist. |
| `TestASPSkillsExist` | 3 | Verify all ASP skills exist. |
| `TestASPDocumentationExists` | 3 | Verify ASP documentation is complete. |
| `TestEndToEndSocietyWorkflow` | 4 | End-to-end tests for society functionality. |
| `TestQuantifiedBenefits` | 2 | Tests that verify the quantified benefits claims. |

### test_template_rendering.py

**Purpose:** Integration tests for template rendering with TemplateEngine.

**Path:** `tests/integration\test_template_rendering.py`
**Tests:** 19

| Class | Tests | Description |
|-------|-------|-------------|
| `TestFactoryTemplateRendering` | 3 | Tests for rendering factory templates. |
| `TestTemplateWithFilters` | 3 | Tests for templates using custom filters. |
| `TestTemplateWithLoops` | 4 | Tests for templates with loop constructs. |
| `TestTemplateWithConditionals` | 4 | Tests for templates with conditional constructs. |
| `TestLegacyPlaceholderSupport` | 3 | Tests for backward compatibility with {{UPPERCASE}} placeholders. |
| `TestProjectGeneratorWithTemplates` | 2 | Tests for ProjectGenerator using template engine. |

### test_update_system.py

**Purpose:** Integration tests for Factory Update System.

**Path:** `tests/integration\test_update_system.py`
**Tests:** 44

| Class | Tests | Description |
|-------|-------|-------------|
| `TestUpdatePatternsExist` | 4 | Tests that all update-related pattern files exist in the Factory. |
| `TestUpdateTemplatesExist` | 2 | Tests that update-related template files exist. |
| `TestFactoryUpdatesFeed` | 5 | Tests for factory-updates.json structure and validity. |
| `TestUpdateFiltering` | 5 | Tests for filtering updates by blueprint_id. |
| `TestGeneratorIncludesUpdateComponents` | 3 | Tests that ProjectGenerator includes update components in generated projects. |
| `TestGeneratedProjectUpdateInfrastructure` | 7 | Tests that generated projects include all update infrastructure. |
| `TestUpdateApplicationLogic` | 5 | Tests for applying updates to generated projects. |
| `TestBlueprintsReferenceUpdates` | 5 | Tests that all blueprints properly reference update components. |
| `TestUpdateSystemIntegration` | 2 | Integration tests for the complete update system. |
| `TestRollbackFunctionality` | 2 | Tests for update rollback capability. |
| `TestUpdateSystemSmoke` | 4 | Smoke tests for quick validation of update system. |

## Validation Tests

**Directory:** `tests/validation/`
**Files:** 9 | **Tests:** 186

### test_blueprint_schema.py

**Purpose:** Schema validation tests for blueprint files.

**Path:** `tests/validation\test_blueprint_schema.py`
**Tests:** 6

| Class | Tests | Description |
|-------|-------|-------------|
| `TestBlueprintSchema` | 6 | Tests for blueprint schema validation. |

### test_extension_templates.py

**Purpose:** Validation tests for extension templates and patterns.

**Path:** `tests/validation\test_extension_templates.py`
**Tests:** 20

| Class | Tests | Description |
|-------|-------|-------------|
| `TestKnowledgeTemplate` | 5 | Tests for knowledge file template. |
| `TestSkillTemplate` | 4 | Tests for skill file template. |
| `TestAgentTemplate` | 4 | Tests for agent file template. |
| `TestKnowledgeSchema` | 5 | Tests for knowledge schema pattern. |
| `TestTemplateConsistency` | 2 | Tests for consistency across templates. |

### test_knowledge_schema.py

**Purpose:** Schema validation tests for knowledge files.

**Path:** `tests/validation\test_knowledge_schema.py`
**Tests:** 33

| Class | Tests | Description |
|-------|-------|-------------|
| `TestKnowledgeFilesStructure` | 2 | Tests for knowledge file structure. |
| `TestSkillCatalogSchema` | 5 | Tests for skill catalog schema validation. |
| `TestStackCapabilitiesSchema` | 2 | Tests for stack capabilities file. |
| `TestWorkflowPatternsSchema` | 2 | Tests for workflow patterns file. |
| `TestBestPracticesSchema` | 2 | Tests for best practices file. |
| `TestKnowledgeFileNaming` | 2 | Tests for knowledge file naming conventions. |
| `TestMCPServersCatalogSchema` | 8 | Tests for MCP servers catalog comprehensive structure. |
| `TestMCPSelectionGuideSchema` | 5 | Tests for MCP selection guide structure. |
| `TestAISuiteIntegrationSchema` | 5 | Tests for AISuite integration guide structure. |

### test_pattern_schema.py

**Purpose:** Schema validation tests for pattern files.

**Path:** `tests/validation\test_pattern_schema.py`
**Tests:** 12

| Class | Tests | Description |
|-------|-------|-------------|
| `TestAgentPatternSchema` | 5 | Tests for agent pattern schema validation. |
| `TestSkillPatternSchema` | 5 | Tests for skill pattern schema validation. |
| `TestPatternConsistency` | 2 | Tests for pattern file consistency. |

### test_pm_schema.py

**Purpose:** Schema validation tests for PM system files.

**Path:** `tests/validation\test_pm_schema.py`
**Tests:** 23

| Class | Tests | Description |
|-------|-------|-------------|
| `TestPMProductSchema` | 5 | Tests for PM product schema validation. |
| `TestQuestionnaireSchema` | 4 | Tests for questionnaire schema validation. |
| `TestAdapterInterfaceSchema` | 3 | Tests for adapter interface schema validation. |
| `TestBackendAdaptersSchema` | 4 | Tests for backend adapter schema validation. |
| `TestMethodologyDefaultsSchema` | 3 | Tests for methodology defaults schema validation. |
| `TestMetricsSchema` | 4 | Tests for metrics schema validation. |

### test_readme_structure.py

**Purpose:** README project structure validation tests.

**Path:** `tests/validation\test_readme_structure.py`
**Tests:** 29

| Class | Tests | Description |
|-------|-------|-------------|
| `TestReadmeExists` | 3 | Tests for README.md file existence and basic structure. |
| `TestReadmeStructureCounts` | 7 | Tests for README project structure count accuracy. |
| `TestStructureValidatorFunctionality` | 10 | Tests for StructureValidator class functionality. |
| `TestProjectComponentsExist` | 9 | Tests to verify expected project components exist. |

### test_taxonomy_schema.py

**Purpose:** Validation tests for taxonomy file structure.

**Path:** `tests/validation\test_taxonomy_schema.py`
**Tests:** 12

| Class | Tests | Description |
|-------|-------|-------------|
| `TestAgentTaxonomyStructure` | 8 | Tests for agent taxonomy file structure. |
| `TestTaxonomyMetadata` | 4 | Tests for taxonomy metadata section. |

### test_value_propagation.py

**Purpose:** Value propagation validation tests.

**Path:** `tests/validation\test_value_propagation.py`
**Tests:** 29

| Class | Tests | Description |
|-------|-------|-------------|
| `TestBlueprintCompleteness` | 11 | Tests for blueprint completeness - all required agents and skills. |
| `TestPatternFileExistence` | 10 | Tests for pattern file existence and validity. |
| `TestPatternSchemaValidation` | 3 | Tests for pattern schema validation. |
| `TestGenerationScriptValidation` | 5 | Tests for generation script validation. |

### test_workflow_structure.py

**Purpose:** Workflow structure validation tests.

**Path:** `tests/validation\test_workflow_structure.py`
**Tests:** 22

| Class | Tests | Description |
|-------|-------|-------------|
| `TestWorkflowStructure` | 10 | Tests for workflow markdown structure validation. |
| `TestWorkflowCategories` | 5 | Tests for workflow organization by category. |
| `TestWorkflowContent` | 4 | Tests for workflow content quality. |
| `TestWorkflowIntegration` | 3 | Tests for workflow integration with other components. |

## Guardian Tests

**Directory:** `tests/guardian/`
**Files:** 1 | **Tests:** 9

### test_no_axiom_drift.py

**Purpose:** CRITICAL Regression Tests for Axiom Protection.

**Path:** `tests/guardian\test_no_axiom_drift.py`
**Tests:** 9

| Class | Tests | Description |
|-------|-------|-------------|
| `TestNoAxiomDrift` | 7 | CRITICAL: Regression tests ensuring axioms never change. |
| `TestAxiomIntegrity` | 2 | Additional integrity checks for axiom protection. |

## Memory Tests

**Directory:** `tests/memory/`
**Files:** 3 | **Tests:** 45

### test_embedding_service.py

**Purpose:** Tests for the Embedding Service.

**Path:** `tests/memory\test_embedding_service.py`
**Tests:** 14

| Class | Tests | Description |
|-------|-------|-------------|
| `TestEmbeddingService` | 13 | Tests for EmbeddingService class. |
| `TestEmbeddingServiceSingleton` | 1 | Tests for the singleton pattern. |

### test_induction_engine.py

**Purpose:** Tests for the Induction Engine.

**Path:** `tests/memory\test_induction_engine.py`
**Tests:** 15

| Class | Tests | Description |
|-------|-------|-------------|
| `TestInductionEngine` | 10 | Tests for InductionEngine class. |
| `TestInductionEngineSession` | 4 | Tests for session management. |
| `TestInductionEngineSingleton` | 1 | Tests for the singleton pattern. |

### test_memory_store.py

**Purpose:** Tests for the Memory Store.

**Path:** `tests/memory\test_memory_store.py`
**Tests:** 16

| Class | Tests | Description |
|-------|-------|-------------|
| `TestMemoryStore` | 9 | Tests for MemoryStore class. |
| `TestMemoryProposalOperations` | 6 | Tests for proposal queue operations. |
| `TestMemoryStoreSingleton` | 1 | Tests for the singleton pattern. |

## Library Tests

**Directory:** `tests/lib/`
**Files:** 10 | **Tests:** 343

### test_bundle.py

**Purpose:** Tests for PABP Bundle Creation and Validation.

**Path:** `tests/lib\society\pabp\test_bundle.py`
**Tests:** 33

| Class | Tests | Description |
|-------|-------|-------------|
| `TestBundleComponent` | 5 | Tests for BundleComponent class. |
| `TestAgentBundle` | 10 | Tests for AgentBundle class. |
| `TestBundleManifest` | 3 | Tests for BundleManifest class. |
| `TestBundleTransfer` | 5 | Tests for bundle export/import operations. |
| `TestBundleVerification` | 2 | Tests for bundle verification. |
| `TestBundleMerging` | 3 | Tests for bundle merging operations. |
| `TestIncrementalBundles` | 3 | Tests for incremental bundle creation. |
| `TestTransferConfig` | 2 | Tests for TransferConfig. |

### test_blockchain.py

**Purpose:** Tests for the blockchain module.

**Path:** `tests/lib\society\test_blockchain.py`
**Tests:** 35

| Class | Tests | Description |
|-------|-------|-------------|
| `TestMerkleTree` | 9 | Tests for MerkleTree. |
| `TestLocalAnchor` | 5 | Tests for LocalAnchor. |
| `TestAnchorService` | 6 | Tests for AnchorService. |
| `TestSolanaAnchor` | 4 | Tests for SolanaAnchor (stub mode). |
| `TestCreateSolanaAnchor` | 2 | Tests for create_solana_anchor factory. |
| `TestAttestation` | 3 | Tests for Attestation. |
| `TestAttestationRegistry` | 6 | Tests for AttestationRegistry. |

### test_contracts.py

**Purpose:** Tests for the contracts module.

**Path:** `tests/lib\society\test_contracts.py`
**Tests:** 62

| Class | Tests | Description |
|-------|-------|-------------|
| `TestParty` | 2 | Tests for Party dataclass. |
| `TestCapability` | 1 | Tests for Capability dataclass. |
| `TestObligation` | 1 | Tests for Obligation dataclass. |
| `TestAgentContract` | 8 | Tests for AgentContract dataclass. |
| `TestContractRegistry` | 26 | Tests for ContractRegistry. |
| `TestContractVerifier` | 20 | Tests for ContractVerifier. |
| `TestContractVerificationResult` | 3 | Tests for ContractVerificationResult. |
| `TestViolation` | 1 | Tests for Violation dataclass. |

### test_events.py

**Purpose:** Tests for the events module.

**Path:** `tests/lib\society\test_events.py`
**Tests:** 19

| Class | Tests | Description |
|-------|-------|-------------|
| `TestAgent` | 2 | Tests for Agent dataclass. |
| `TestAction` | 2 | Tests for Action dataclass. |
| `TestAgentEvent` | 4 | Tests for AgentEvent dataclass. |
| `TestHashChain` | 2 | Tests for HashChain. |
| `TestEventStore` | 6 | Tests for EventStore. |
| `TestVerifyChainIntegrity` | 3 | Tests for chain integrity verification. |

### test_hybrid.py

**Purpose:** Tests for the hybrid module.

**Path:** `tests/lib\society\test_hybrid.py`
**Tests:** 31

| Class | Tests | Description |
|-------|-------|-------------|
| `TestSystemConfig` | 3 | Tests for SystemConfig. |
| `TestHybridVerificationResult` | 2 | Tests for HybridVerificationResult. |
| `TestHybridVerificationSystem` | 11 | Tests for HybridVerificationSystem. |
| `TestEscalation` | 3 | Tests for Escalation. |
| `TestDefaultPolicy` | 3 | Tests for DefaultPolicy. |
| `TestEscalationManager` | 9 | Tests for EscalationManager. |

### test_integration.py

**Purpose:** Tests for the integration module.

**Path:** `tests/lib\society\test_integration.py`
**Tests:** 29

| Class | Tests | Description |
|-------|-------|-------------|
| `TestSocietyConfig` | 3 | Tests for SocietyConfig. |
| `TestSocietyContext` | 8 | Tests for SocietyContext. |
| `TestAgentSocietyBridge` | 7 | Tests for AgentSocietyBridge. |
| `TestAgentContractCreation` | 2 | Tests for contract creation via bridges. |
| `TestMessageRouter` | 7 | Tests for MessageRouter. |
| `TestEndToEndCommunication` | 2 | End-to-end tests for agent communication. |

### test_simple_api.py

**Purpose:** Tests for the Simplified Society API.

**Path:** `tests/lib\society\test_simple_api.py`
**Tests:** 35

| Class | Tests | Description |
|-------|-------|-------------|
| `TestSimpleSociety` | 18 | Tests for SimpleSociety class. |
| `TestQuickSend` | 1 | Tests for quick_send convenience function. |
| `TestPresets` | 6 | Tests for society presets. |
| `TestSocietyBuilder` | 4 | Tests for SocietyBuilder fluent API. |
| `TestSendResult` | 3 | Tests for SendResult dataclass. |
| `TestMessageCounting` | 1 | Tests for message counting functionality. |
| `TestIntegration` | 2 | Integration tests for the simplified API. |

### test_society.py

**Purpose:** Tests for the society module.

**Path:** `tests/lib\society\test_society.py`
**Tests:** 37

| Class | Tests | Description |
|-------|-------|-------------|
| `TestRole` | 3 | Tests for Role dataclass. |
| `TestProposal` | 2 | Tests for Proposal dataclass. |
| `TestFlatDemocracy` | 6 | Tests for FlatDemocracy pattern. |
| `TestMeritocracy` | 2 | Tests for Meritocracy pattern. |
| `TestHierarchy` | 4 | Tests for Hierarchy pattern. |
| `TestFederation` | 4 | Tests for Federation pattern. |
| `TestDAOSociety` | 3 | Tests for DAOSociety pattern. |
| `TestCreateSociety` | 5 | Tests for create_society factory function. |
| `TestMessage` | 3 | Tests for Message dataclass. |
| `TestDirectProtocol` | 2 | Tests for DirectProtocol. |
| `TestBroadcastProtocol` | 1 | Tests for BroadcastProtocol. |
| `TestConsensusProtocol` | 1 | Tests for ConsensusProtocol. |
| `TestMessageRouter` | 1 | Tests for MessageRouter. |

### test_trust.py

**Purpose:** Tests for the trust module.

**Path:** `tests/lib\society\test_trust.py`
**Tests:** 40

| Class | Tests | Description |
|-------|-------|-------------|
| `TestKeyPair` | 5 | Tests for KeyPair. |
| `TestAgentIdentity` | 6 | Tests for AgentIdentity. |
| `TestIdentityRegistry` | 4 | Tests for IdentityRegistry. |
| `TestReputationScore` | 5 | Tests for ReputationScore. |
| `TestReputationSystem` | 7 | Tests for ReputationSystem. |
| `TestTrustDelegation` | 4 | Tests for TrustDelegation. |
| `TestTrustGraph` | 9 | Tests for TrustGraph. |

### test_verification.py

**Purpose:** Tests for the verification module.

**Path:** `tests/lib\society\test_verification.py`
**Tests:** 22

| Class | Tests | Description |
|-------|-------|-------------|
| `TestA0SDGVerifier` | 2 | Tests for A0 SDG Verifier. |
| `TestA1LoveVerifier` | 2 | Tests for A1 Love Verifier. |
| `TestA2TruthVerifier` | 2 | Tests for A2 Truth Verifier. |
| `TestA3BeautyVerifier` | 2 | Tests for A3 Beauty Verifier. |
| `TestA4GuardianVerifier` | 3 | Tests for A4 Guardian Verifier. |
| `TestA5MemoryVerifier` | 2 | Tests for A5 Memory Verifier. |
| `TestAxiomComplianceMonitor` | 6 | Tests for AxiomComplianceMonitor. |
| `TestVerificationResult` | 3 | Tests for VerificationResult. |

---

*Part of the Cursor Agent Factory test suite documentation.*
