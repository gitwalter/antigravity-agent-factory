# Blueprint Version Management

This document describes the automated version management system for Antigravity Agent Factory blueprints.

## Overview

The blueprint version updater automatically keeps framework and LLM model versions up-to-date by querying official package registries and tracking the latest stable releases.

## Components

### 1. Version Update Script
**Location**: `scripts/maintenance/update_blueprint_versions.py`

Automatically updates:
- **Python Frameworks**: LangChain, LangGraph, CrewAI, AutoGen, Streamlit, FastAPI, Pydantic
- **Development Tools**: pytest, ruff, mypy, poetry
- **Databases**: ChromaDB, FAISS
- **LLM Models**: OpenAI (GPT-5.x, GPT-4o, o1), Anthropic (Claude Opus 4.6, Claude 3.5), Google (Gemini 3), Ollama (Llama 3.3, Qwen 2.5)

**Usage**:
```bash
# Update all blueprints
python scripts/maintenance/update_blueprint_versions.py

# Update specific blueprint
python scripts/maintenance/update_blueprint_versions.py --blueprint ai-agent-development

# Dry run (preview changes without applying)
python scripts/maintenance/update_blueprint_versions.py --dry-run
```

### 2. Pre-commit Integration
**Location**: `.pre-commit-config.yaml`

The version checker runs automatically via pre-commit hooks, but only **once per week** to avoid excessive API calls.

**Setup**:
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Manual run
pre-commit run blueprint-version-check --all-files
```

### 3. Weekly Execution Control
**Location**: `scripts/git/pre_commit_version_check.py`

Tracks last execution time in `.last_version_check` file. Only runs if 7+ days have passed since last check.

## Latest Versions (as of Feb 2026)

### Frameworks
- **LangChain**: 1.2.9 → Blueprint: `1.2+`
- **LangGraph**: 1.0.8 (LTS) → Blueprint: `1.0+`
- **CrewAI**: 1.9.3 → Blueprint: `1.9+`
- **AutoGen**: 0.10.5 → Blueprint: `0.10+`
- **Streamlit**: 1.54.0 → Blueprint: `1.54+`
- **FastAPI**: 0.128.4 → Blueprint: `0.128+`
- **Pydantic**: 2.12.5 → Blueprint: `2.12+`

### LLM Models

**OpenAI**:
- `gpt-5.2` - Latest GPT-5 series (Dec 2025)
- `gpt-5.3-codex` - Latest coding model (Feb 2026)
- `gpt-4o` - GPT-4 Optimized
- `gpt-4o-mini` - GPT-4 Optimized Mini
- `o1` - OpenAI o1 reasoning
- `o1-mini` - OpenAI o1 mini

**Anthropic**:
- `claude-opus-4.6` - Latest Opus (Feb 2026)
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-5-haiku-20241022` - Claude 3.5 Haiku

**Google**:
- `gemini-3-pro` - Gemini 3 Pro (Feb 2026)
- `gemini-3-flash` - Gemini 3 Flash (Feb 2026)
- `gemini-2.5-flash` - Gemini 2.5 Flash
- `gemini-2.0-flash-exp` - Gemini 2.0 Flash Experimental

**Ollama** (Local):
- `llama3.3` - Llama 3.3
- `llama3.2` - Llama 3.2
- `qwen2.5` - Qwen 2.5
- `mistral` - Mistral
- `codellama` - Code Llama

## How It Works

### Version Detection
1. **PyPI Packages**: Queries `https://pypi.org/pypi/{package}/json` for latest version
2. **LLM Models**: Manually curated based on official announcements and documentation
3. **Version Format**: Extracts major.minor version (e.g., `1.2.9` → `1.2+`)

### Update Process
1. Reads blueprint JSON files
2. Compares current versions with latest versions
3. Updates framework versions to `{major}.{minor}+` format
4. Adds new LLM models, removes deprecated ones
5. Writes updated JSON back to file

### Weekly Execution
1. Pre-commit hook triggers on every commit
2. Wrapper script checks `.last_version_check` timestamp
3. If < 7 days, exits immediately (no API calls)
4. If ≥ 7 days, runs version updater
5. Updates timestamp file after successful run

## Maintenance

### Adding New Frameworks
Edit `scripts/maintenance/update_blueprint_versions.py`:

```python
python_packages = {
    'new-package': 'new-package',  # PyPI name
    # ...
}
```

### Updating LLM Models
Edit the `versions['llm_models']` dictionary in `get_latest_versions()`:

```python
versions['llm_models'] = {
    'openai': {
        'new-model': 'Description',
        # ...
    }
}
```

### Forcing Manual Update
```bash
# Delete timestamp to force next run
rm .last_version_check

# Or run script directly
python scripts/maintenance/update_blueprint_versions.py
```

## Benefits

✅ **Always Up-to-Date**: Blueprints use latest stable versions
✅ **Automated**: No manual version tracking needed
✅ **Efficient**: Weekly checks avoid excessive API calls
✅ **Safe**: Dry-run mode for previewing changes
✅ **Integrated**: Runs automatically via pre-commit hooks
✅ **Transparent**: Detailed logging of all changes

## Troubleshooting

### Version check not running
```bash
# Check timestamp
cat .last_version_check

# Force update
rm .last_version_check
pre-commit run blueprint-version-check --all-files
```

### API errors
The script gracefully handles API failures and won't block commits. Check logs for warnings.

### Incorrect versions
LLM model versions are manually curated. Update `scripts/update_blueprint_versions.py` if models are incorrect.
