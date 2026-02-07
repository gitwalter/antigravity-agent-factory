# Changelog

All notable changes to the Antigravity Agent Factory will be documented in this file.

## [2.1.0] - 2026-02-07

### Added - AI Agent Enrichment

#### Knowledge Files
- **ml-agent-frameworks.json**: Comprehensive patterns for PyTorch, TensorFlow, Hugging Face Transformers, and AgentTorch
- **advanced-agent-architectures.json**: Cutting-edge patterns including ReAct, Reflection, Tree of Thoughts, Plan-and-Execute, BabyAGI, AutoGPT, and CAMEL-AI
- **deepagent-patterns.json**: DeepAgent framework patterns with memory folding, task planning, and subagent delegation
- **github-agent-templates.json**: Curated GitHub repositories and resources for AI agent development

#### Production-Ready Templates
- **LangChain**: `react_agent_template.py` - Complete ReAct agent with tool integration (260 lines)
- **LangGraph**: `supervisor_pattern_template.py` - Multi-agent supervisor pattern with state management (220 lines)
- **CrewAI**: `hierarchical_crew_template.py` - Hierarchical crew with manager and workers (180 lines)
- **Anthropic**: `mcp_server_template.py` - Model Context Protocol server implementation (200 lines)
- **DeepAgent**: `task_planning_agent_template.py` - Task planning with progress tracking (280 lines)

#### Skills & Workflows
- **ai-agent-dev/SKILL.md**: Comprehensive AI agent development skill with patterns, best practices, and troubleshooting
- **build-langchain-agent.md**: Step-by-step workflow for building LangChain agents

### Added - Google Agent Support
#### Google Agent System
- **New Blueprint**: `google-agent-system` utilizing `google-generativeai` SDK
- **Templates**: Complete agent implementation with structured output, tools, and config
- **Patterns**: `knowledge/google-generative-ai-patterns.json` covering setup, safety, and system instructions
- **Documentation**: New `docs/google_agent_sdk.md` guide

### Added - Comprehensive Version Management

#### Version Tracking
- **Python packages** (23): LangChain 1.2.9, LangGraph 1.0.8, CrewAI 1.9.3, AutoGen 0.10.5, PyTorch, TensorFlow 2.20.0, Transformers 5.1.0, Anthropic 0.78.0, OpenAI 2.17.0, and more
- **npm packages** (6): n8n 2.6.4, MCP SDK 1.26.0, TypeScript 5.9.3, Next.js 16.1.6, React 19.2.4, Vite 7.3.1
- **Databases** (9): PostgreSQL 17.2, MongoDB 8.0, Redis 7.4, SQLite 3.47.0, ChromaDB, Pinecone, Qdrant, Weaviate
- **Dev tools** (9): Docker 27.4.0, Node 22.12.0 LTS, Python 3.13.1, Git 2.48.0, Go, Rust, Java, .NET
- **Cloud services** (5): AWS CLI, Azure CLI, gcloud, Terraform, Kubernetes
- **LLM models**: GPT-5.2, GPT-5.3-Codex, Claude Opus 4.6, Gemini 3 Pro, Llama 3.3, Qwen 2.5

#### Automation
- **scripts/update_blueprint_versions.py**: Enhanced to track all entity types (Python, npm, databases, tools, cloud, LLMs)
- **scripts/pre_commit_version_check.py**: Weekly execution wrapper for version checks
- **.pre-commit-config.yaml**: Pre-commit hook configuration with weekly version updates
- **docs/BLUEPRINT_VERSION_MANAGEMENT.md**: Comprehensive documentation for version management system

### Changed

#### Blueprint Updates
- Updated 9/27 blueprints with latest framework versions:
  - ai-agent-development
  - multi-agent-systems
  - python-multi-agent
  - python-rag-system
  - python-streamlit
  - python-fastapi
  - python-deep-learning
  - quantitative-trading
  - starter-chatbot
  - starter-rag

#### Framework Version Updates
- LangChain: 0.3+ → 1.2+ (latest: 1.2.9)
- LangGraph: 0.2+ → 1.0+ (latest: 1.0.8 LTS)
- CrewAI: 0.50+ → 1.9+ (latest: 1.9.3)
- AutoGen: 0.2+ → 0.10+ (latest: 0.10.5)
- Streamlit: 1.30+ → 1.54+ (latest: 1.54.0)
- FastAPI: 0.100+ → 0.128+ (latest: 0.128.4)
- Pydantic: 2.0+ → 2.12+ (latest: 2.12.5)

#### LLM Model Updates
- **Added**: GPT-5.2, GPT-5.3-Codex, o1, o1-mini, Claude Opus 4.6, Claude 3.5 Sonnet/Haiku (dated versions), Gemini 3 Pro/Flash, Llama 3.3, Qwen 2.5
- **Removed**: Deprecated models (GPT-4, GPT-3.5-turbo, older Claude 3 variants)

### Technical Details

- **Total new files**: 12
- **Total lines of code**: ~3,400+
- **Frameworks covered**: 8+ (LangChain, LangGraph, CrewAI, AutoGen, Anthropic, PyTorch, TensorFlow, Transformers)
- **Patterns documented**: 15+ (ReAct, Reflection, ToT, Plan-Execute, BabyAGI, AutoGPT, CAMEL, Memory Folding, Task Planning, etc.)
- **Version entities tracked**: 52+ across 5 categories

### Quality Assurance

- All templates are production-ready with comprehensive documentation
- Full type annotations and error handling
- Working examples included in every template
- Async/await support where applicable
- Best practices enforced throughout

## [2.0.0] - 2026-02-07
- Rebranding to Antigravity Agent Factory
- Simplified repository structure
- Leaner documentation and artifacts
