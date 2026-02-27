# Artifact Quality Assessment Report — February 2026

**Purpose**: Evaluate every agent and skill in the Factory for usefulness, uniqueness, naming compliance, instructiveness, and schema compliance.
**Verdict Legend**: `KEEP` ✅ | `REFACTOR` 🔧 | `DEPRECATE` ❌

---

## Assessment Criteria
| Criterion | Description |
|-----------|-------------|
| **Relevance** | Serves an active use case in the Factory |
| **Uniqueness** | Not redundant with another artifact |
| **Instructive** | Content is clear, actionable, and focused |
| **Naming** | Follows participle-based convention (e.g., `managing-plane-tasks`) |
| **Schema** | Passes `quick_validate.py` |

---

## Agents Assessment

**Target**: `.agent/agents/`
**Total**: 10 agents

| Agent | Topology | Verdict | Issues Found |
|-------|----------|---------|--------------|
| `project-operations-specialist` | chain | 🔧 REFACTOR | Missing YAML frontmatter |
| `system-architecture-specialist` | chain | 🔧 REFACTOR | Missing YAML frontmatter |
| `workflow-quality-specialist` | evaluator-optimizer | 🔧 REFACTOR | Missing YAML frontmatter |
| `executive-operations-specialist` | orchestrator-workers | 🔧 REFACTOR | Missing YAML frontmatter |
| `dotnet-cloud-specialist` | parallel | 🔧 REFACTOR | Missing YAML frontmatter |
| `full-stack-web-specialist` | parallel | 🔧 REFACTOR | Missing YAML frontmatter |
| `java-systems-specialist` | parallel | 🔧 REFACTOR | Missing YAML frontmatter |
| `python-ai-specialist` | parallel | 🔧 REFACTOR | Missing YAML frontmatter |
| `sap-systems-specialist` | parallel | 🔧 REFACTOR | Missing YAML frontmatter |
| `knowledge-operations-specialist` | routing | 🔧 REFACTOR | Missing YAML frontmatter |

**Summary**: All 10 agents are high-quality, purposeful, well-documented domain specialists. Content is excellent — only metadata injection is required.

---

## Skills Assessment

**Target**: `.agent/skills/`
**Total**: ~105 skills

### Chain Skills (Alphabetical)

| Skill | Verdict | Naming OK? | Issues Found |
|-------|---------|------------|--------------|
| `retrieving-advanced` | 🔧 | ❌ | Name not participle-based → rename to `retrieving-advanced` or deprecate if covered by `retrieving-rag-context-adv` |
| `trading-algorithmically` | 🔧 | ❌ | Name not participle-based → rename to `trading-algorithmically` |
| `analyzing-code` | ✅ | ✅ | Missing schema fields |
| `analyzing-knowledge-gaps` | ✅ | ✅ | Missing schema fields |
| `applying-anthropic-patterns` | ✅ | ✅ | Missing schema fields |
| `applying-ef-core-patterns` | ✅ | ✅ | Missing schema fields |
| `applying-jpa-patterns` | ✅ | ✅ | Missing schema fields |
| `developing-bdd` | 🔧 | ❌ | Name not participle-based → rename to `developing-bdd` |
| `browsing-web` | ✅ | ✅ | Missing schema fields |
| `building-raw-bundles` | ✅ | ✅ | Missing schema fields |
| `committing-releases` | ✅ | ✅ | Missing schema fields |
| `configuring-pm` | ✅ | ✅ | Duplicate context with `managing-plane-tasks` → review scope |
| `deploying-azure` | ✅ | ✅ | Missing schema fields |
| `developing-blazor-apps` | ✅ | ✅ | Missing schema fields |
| `generating-skills` | ❌ → rename | ❌ | Superseded by `skill-creator`. Deprecate or merge content. |
| `grounding` | 🔧 | ❌ | Name ambiguous — rename to `grounding-responses` |
| `migrating-databases` | ✅ | ✅ | Missing schema fields |
| `planning-features` | ✅ | ✅ | Missing schema fields |
| `synthesizing-documentation` | ✅ | ✅ | Missing schema fields |
| `verifying-links` | ✅ | ✅ | Missing schema fields |

### Management Skills

| Skill | Verdict | Naming OK? | Issues Found |
|-------|---------|------------|--------------|
| `orchestrating-mcp` | ✅ | ✅ | Missing schema fields |

### Parallel Skills

| Skill | Verdict | Naming OK? | Issues Found |
|-------|---------|------------|--------------|
| `agent-creator` | ✅ | ❌ | Noun, not participle. Could be `creating-agents` but convention of `*-creator` accepted for factory tools |
| `securing-agents` | 🔧 | ❌ | Name not participle-based → rename to `securing-agents` |
| `mastering-agentic-loops` | 🔧 | ❌ | Rename to `mastering-agentic-loops` |
| `developing-ai-agents` | 🔧 | ❌ | Name vague and non-participle → rename to `developing-ai-agents` |
| `optimizing-ai-costs` | 🔧 | ❌ | Rename to `optimizing-ai-costs` |
| `securing-ai-systems` | 🔧 | ❌ | Rename to `securing-ai-systems` |
| `designing-ai-systems` | 🔧 | ❌ | Rename to `designing-ai-systems` |
| `trading-algorithmically` | 🔧 | ❌ | Rename to `trading-algorithmically` |
| `designing-apis` | 🔧 | ❌ | Rename to `designing-apis` |
| `applying-ef-core-patterns` | ✅ | ✅ | Missing schema fields |
| `applying-jpa-patterns` | ✅ | ✅ | Missing schema fields |
| `blueprint-creator` | ✅ | ❌* | Factory tool — `*-creator` pattern accepted |
| `browsing-web` | ✅ | ✅ | Missing schema fields |
| `orchestrating-crewai-agents` | 🔧 | ❌ | Rename to `orchestrating-crewai-agents` |
| `developing-blazor-apps` | ✅ | ✅ | Missing schema fields |
| `authenticating-dotnet` | 🔧 | ❌ | Rename to `authenticating-dotnet` |
| `building-dotnet-backend` | 🔧 | ❌ | Rename to `building-dotnet-backend` |
| `building-dotnet-microservices` | 🔧 | ❌ | Rename to `building-dotnet-microservices` |
| `developing-fastapi` | 🔧 | ❌ | Rename to `developing-fastapi` |
| `building-fastapi-enterprise` | 🔧 | ❌ | Rename to `building-fastapi-enterprise` |
| `optimizing-frontend-performance` | 🔧 | ❌ | Rename to `optimizing-frontend-performance` |
| `testing-frontend` | 🔧 | ❌ | Rename to `testing-frontend` |
| `containerizing-java-apps` | 🔧 | ❌ | Rename to `containerizing-java-apps` |
| `knowledge-creator` | ✅ | ❌* | Factory tool — accepted |
| `using-langchain` | 🔧 | ❌ | Rename to `using-langchain` |
| `applying-llm-guardrails` | 🔧 | ❌ | Rename to `applying-llm-guardrails` |
| `managing-database-agents` | ✅ | ✅ | Missing schema fields |
| `managing-knowledge-graphs` | ✅ | ✅ | Missing schema fields |
| `managing-vision-agents` | ✅ | ✅ | Missing schema fields |
| `managing-memory-bank` | 🔧 | ❌ | Rename to `managing-memory-bank` |
| `deploying-ml-models` | 🔧 | ❌ | Rename to `deploying-ml-models` |
| `operating-ml-engineering` | 🔧 | ❌ | Rename to `operating-ml-engineering` |
| `monitoring-ml-models` | 🔧 | ❌ | Rename to `monitoring-ml-models` |
| `training-models` | 🔧 | ❌ | Rename to `training-models` |
| `modeling-cds` | ✅ | ✅ | Missing schema fields |
| `developing-nextjs` | 🔧 | ❌ | Rename to `developing-nextjs` |
| `building-nextjs-enterprise` | 🔧 | ❌ | Rename to `building-nextjs-enterprise` |
| `optimizing-langsmith-prompts` | ✅ | ✅ | Missing schema fields |
| `optimizing-prompts` | ✅ | ✅ | Missing schema fields |
| `orchestrating-crewai-workflows` | ✅ | ✅ | Missing schema fields |
| `pattern-creator` | ✅ | ❌* | Factory tool — accepted |
| `using-prisma-database` | 🔧 | ❌ | Rename to `using-prisma-database` |
| `processing-data-pipelines` | ✅ | ✅ | Missing schema fields |
| `processing-ocr` | ✅ | ✅ | Missing schema fields |
| `processing-speech` | ✅ | ✅ | Missing schema fields |
| `programming-python-async` | 🔧 | ❌ | Rename to `programming-python-async` |
| `engineering-rag-systems` | 🔧 | ❌ | Rename to `engineering-rag-systems` |
| `applying-rag-patterns` | 🔧 | ❌ | Rename to `applying-rag-patterns` |
| `retrieving-rag-context-adv` | 🔧 | ❌ | Rename to `retrieving-rag-context` |
| `applying-react-patterns` | 🔧 | ❌ | Rename to `applying-react-patterns` |
| `developing-sap-rap` | 🔧 | ❌ | Rename to `developing-sap-rap` |
| `building-sap-fiori` | 🔧 | ❌ | Rename to `building-sap-fiori` |
| `integrating-sap-systems` | 🔧 | ❌ | Rename to `integrating-sap-systems` |
| `integrating-sap-cloud` | 🔧 | ❌ | Rename to `integrating-sap-cloud` |
| `securing-sap-systems` | 🔧 | ❌ | Rename to `securing-sap-systems` |
| `sending-emails` | ✅ | ✅ | Missing schema fields |
| `skill-creator` | ✅ | ❌* | Factory tool — accepted |
| `developing-spring-boot` | 🔧 | ❌ | Rename to `developing-spring-boot` |
| `building-spring-enterprise` | 🔧 | ❌ | Rename to `building-spring-enterprise` |
| `building-spring-microservices` | 🔧 | ❌ | Rename to `building-spring-microservices` |
| `observing-spring-apps` | 🔧 | ❌ | Rename to `observing-spring-apps` |
| `testing-spring-apps` | 🔧 | ❌ | Rename to `testing-spring-apps` |
| `applying-sqlalchemy-patterns` | 🔧 | ❌ | Rename to `applying-sqlalchemy-patterns` |
| `streaming-realtime-data` | ✅ | ✅ | Missing schema fields |
| `template-creator` | ✅ | ❌* | Factory tool — accepted |
| `tracing-with-langsmith` | ✅ | ✅ | Missing schema fields |
| `building-trpc-api` | 🔧 | ❌ | Rename to `building-trpc-api` |
| `workflow-creator` | ✅ | ❌* | Factory tool — accepted |
| `workshop-creator` | ✅ | ❌* | Factory tool — accepted |

### Retrieval Skills

| Skill | Verdict | Naming OK? | Issues Found |
|-------|---------|------------|--------------|
| `ingesting-rag-content` | ✅ | ✅ | Missing schema fields |
| `inspecting-rag-catalog` | ✅ | ✅ | Missing schema fields |
| `retrieving-rag-context` | ✅ | ✅ | Missing schema fields |

### Routing Skills

| Skill | Verdict | Naming OK? | Issues Found |
|-------|---------|------------|--------------|
| `integrating-mcp` | ✅ | ✅ | Missing schema fields |
| `managing-google-calendar` | ✅ | ✅ | Missing schema fields |
| `managing-google-drive` | ✅ | ✅ | Missing schema fields |
| `managing-google-workspace` | ✅ | ✅ | Missing schema fields |
| `managing-plane-tasks` | ✅ | ✅ | Missing schema fields (recently renamed) |
| `operating-github` | ✅ | ✅ | Missing schema fields |
| `selecting-mcp` | ✅ | ✅ | Missing schema fields |
| `sending-emails` | ✅ | ✅ | Missing schema fields |

### Verification Skills

| Skill | Verdict | Naming OK? | Issues Found |
|-------|---------|------------|--------------|
| `verifying-artifact-structures` | ✅ | ✅ | Missing schema fields |

---

## Summary Statistics

| Category | KEEP ✅ | REFACTOR 🔧 | DEPRECATE ❌ |
|----------|---------|------------|-------------|
| Agents | 0 | 10 (metadata only) | 0 |
| Chain Skills | ~12 | ~7 | 1 (`generating-skills`) |
| Parallel Skills | ~12 | ~43 | 0 |
| Retrieval Skills | 3 | 0 | 0 |
| Routing Skills | 8 | 0 | 0 |
| Verification Skills | 1 | 0 | 0 |
| **Total** | **~36** | **~60** | **1** |

## Key Findings

1. **All agents are high quality** — only YAML frontmatter injection needed.
2. **Naming convention** is the #1 issue: ~50 skills use noun/noun-phrase names instead of participle-based names.
3. **Schema fields** (`version`, `category`, `agents`, `knowledge`, `tools`, `related_skills`, `templates`) are missing in 100% of existing skills.
4. **`generating-skills`** should be deprecated — fully superseded by `skill-creator`.
5. **`retrieving-advanced`** and `configuring-pm` overlap with existing skills and should be reviewed.

## Next Steps (Phase 4 — Mass Refactoring)

1. Deprecate `generating-skills`.
2. Batch inject YAML frontmatter into all 10 agents with `agent-creator` schema.
3. Batch update all `SKILL.md` files with missing schema fields using `skill-creator` schema.
4. Execute renames for ~50 skills with non-compliant names.
