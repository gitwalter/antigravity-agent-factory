#!/usr/bin/env python3
"""
Workshop Export Script

Exports a workshop to a standalone learning project with all necessary artifacts
for maximum AI-assisted learning experience.

Usage:
    python export_workshop.py L1_ethereum_fundamentals c:/App/learning/ethereum-workshop
    python export_workshop.py L7_langchain_fundamentals c:/learning/langchain-workshop

Artifacts Generated:
    - Project scaffolding (directories, config files)
    - Antigravity rules (.agentrules, .agent/rules/)
    - Knowledge files (copied from factory)
    - Starter code and examples
    - Exercise templates with hints
    - README with workshop instructions
    - Package management (package.json, requirements.txt)
"""

import json
import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkshopConfig:
    """Configuration for a workshop export."""
    workshop_id: str
    target_dir: Path
    factory_root: Path
    workshop_data: Dict[str, Any]


# Technology stack configurations
STACK_CONFIGS = {
    "blockchain": {
        "ethereum": {
            "package_manager": "npm",
            "main_language": "solidity",
            "test_framework": "hardhat",
            "file_extensions": [".sol", ".js", ".ts"],
            "directories": ["contracts", "test", "scripts", "artifacts", "cache"],
            "dependencies": {
                "dev": ["hardhat", "@nomicfoundation/hardhat-toolbox"],
                "prod": ["@openzeppelin/contracts"]
            },
            "config_files": ["hardhat.config.js"],
            "gitignore_patterns": [
                "node_modules/", "cache/", "artifacts/", "typechain/",
                "coverage/", ".env", "*.log"
            ]
        },
        "solana": {
            "package_manager": "cargo",
            "main_language": "rust",
            "test_framework": "anchor",
            "file_extensions": [".rs", ".ts"],
            "directories": ["programs", "tests", "target"],
            "config_files": ["Anchor.toml", "Cargo.toml"],
            "gitignore_patterns": ["target/", "node_modules/", ".anchor/", "*.log"]
        },
        "bitcoin": {
            "package_manager": "npm",
            "main_language": "javascript",
            "file_extensions": [".js", ".ts"],
            "directories": ["src", "test", "scripts"],
            "dependencies": {"dev": [], "prod": ["bitcoinjs-lib"]},
            "gitignore_patterns": ["node_modules/", "*.log"]
        }
    },
    "ai": {
        "langchain": {
            "package_manager": "pip",
            "main_language": "python",
            "test_framework": "pytest",
            "file_extensions": [".py"],
            "directories": ["src", "tests", "notebooks", "data"],
            "dependencies": {
                "prod": ["langchain", "langchain-openai", "python-dotenv"],
                "dev": ["pytest", "pytest-asyncio", "black", "mypy"]
            },
            "config_files": ["pyproject.toml"],
            "gitignore_patterns": [
                "__pycache__/", "*.pyc", ".env", ".venv/", "venv/",
                ".pytest_cache/", "*.egg-info/"
            ]
        },
        "langgraph": {
            "package_manager": "pip",
            "main_language": "python",
            "test_framework": "pytest",
            "file_extensions": [".py"],
            "directories": ["src", "tests", "notebooks", "graphs"],
            "dependencies": {
                "prod": ["langgraph", "langchain", "langchain-openai"],
                "dev": ["pytest", "pytest-asyncio"]
            },
            "config_files": ["pyproject.toml"],
            "gitignore_patterns": ["__pycache__/", "*.pyc", ".env", ".venv/"]
        },
        "crewai": {
            "package_manager": "pip",
            "main_language": "python",
            "file_extensions": [".py"],
            "directories": ["src", "crews", "agents", "tasks", "tests"],
            "dependencies": {
                "prod": ["crewai", "crewai-tools"],
                "dev": ["pytest"]
            },
            "gitignore_patterns": ["__pycache__/", "*.pyc", ".env", ".venv/"]
        },
        "huggingface": {
            "package_manager": "pip",
            "main_language": "python",
            "file_extensions": [".py"],
            "directories": ["src", "models", "data", "notebooks", "tests"],
            "dependencies": {
                "prod": ["transformers", "datasets", "torch", "accelerate"],
                "dev": ["pytest", "jupyter"]
            },
            "gitignore_patterns": [
                "__pycache__/", "*.pyc", ".env", ".venv/",
                "models/", "*.pt", "*.bin"
            ]
        },
        "rag": {
            "package_manager": "pip",
            "main_language": "python",
            "file_extensions": [".py"],
            "directories": ["src", "data", "vectorstore", "tests", "notebooks"],
            "dependencies": {
                "prod": ["langchain", "chromadb", "sentence-transformers"],
                "dev": ["pytest"]
            },
            "gitignore_patterns": [
                "__pycache__/", "*.pyc", ".env", ".venv/",
                "vectorstore/", "*.pkl"
            ]
        }
    },
    "web": {
        "react": {
            "package_manager": "npm",
            "main_language": "typescript",
            "file_extensions": [".tsx", ".ts", ".css"],
            "directories": ["src", "public", "tests"],
            "dependencies": {
                "prod": ["react", "react-dom"],
                "dev": ["@types/react", "typescript", "vite"]
            },
            "gitignore_patterns": ["node_modules/", "dist/", ".env"]
        },
        "nextjs": {
            "package_manager": "npm",
            "main_language": "typescript",
            "file_extensions": [".tsx", ".ts"],
            "directories": ["app", "components", "lib", "public"],
            "dependencies": {
                "prod": ["next", "react", "react-dom"],
                "dev": ["@types/react", "typescript"]
            },
            "gitignore_patterns": ["node_modules/", ".next/", ".env"]
        },
        "fastapi": {
            "package_manager": "pip",
            "main_language": "python",
            "test_framework": "pytest",
            "file_extensions": [".py"],
            "directories": ["app", "tests", "alembic"],
            "dependencies": {
                "prod": ["fastapi", "uvicorn", "pydantic", "sqlalchemy"],
                "dev": ["pytest", "httpx", "pytest-asyncio"]
            },
            "gitignore_patterns": ["__pycache__/", "*.pyc", ".env", ".venv/"]
        }
    },
    "cloud": {
        "docker": {
            "package_manager": None,
            "main_language": "dockerfile",
            "file_extensions": [".dockerfile", ".yaml", ".yml"],
            "directories": ["app", "config", "scripts"],
            "config_files": ["Dockerfile", "docker-compose.yml"],
            "gitignore_patterns": ["*.log", ".env"]
        },
        "kubernetes": {
            "package_manager": None,
            "main_language": "yaml",
            "file_extensions": [".yaml", ".yml"],
            "directories": ["manifests", "charts", "scripts"],
            "gitignore_patterns": ["*.log", ".env", "secrets/"]
        }
    },
    "ml": {
        "pytorch": {
            "package_manager": "pip",
            "main_language": "python",
            "file_extensions": [".py"],
            "directories": ["src", "models", "data", "notebooks", "tests"],
            "dependencies": {
                "prod": ["torch", "torchvision", "numpy", "matplotlib"],
                "dev": ["pytest", "jupyter", "tensorboard"]
            },
            "gitignore_patterns": [
                "__pycache__/", "*.pyc", ".env", ".venv/",
                "models/*.pt", "data/", "runs/"
            ]
        },
        "finetuning": {
            "package_manager": "pip",
            "main_language": "python",
            "file_extensions": [".py"],
            "directories": ["src", "data", "models", "configs", "tests"],
            "dependencies": {
                "prod": ["transformers", "datasets", "peft", "trl", "accelerate"],
                "dev": ["pytest", "wandb"]
            },
            "gitignore_patterns": [
                "__pycache__/", "*.pyc", ".env", ".venv/",
                "models/", "outputs/"
            ]
        }
    }
}


def get_stack_config(technology: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Get the stack configuration based on workshop technology."""
    category = technology.get("category", "").lower()
    stack = technology.get("stack", "").lower()
    
    # Map common stack names to config keys
    stack_mapping = {
        "ethereum + hardhat": "ethereum",
        "solana + anchor": "solana",
        "bitcoin + lightning": "bitcoin",
        "langchain + langgraph": "langchain",
        "langchain": "langchain",
        "langgraph": "langgraph",
        "crewai": "crewai",
        "hugging face": "huggingface",
        "huggingface": "huggingface",
        "langchain + vector db": "rag",
        "react 18+": "react",
        "next.js 14+": "nextjs",
        "fastapi": "fastapi",
        "docker": "docker",
        "kubernetes": "kubernetes",
        "pytorch 2.0+": "pytorch",
        "pytorch": "pytorch",
        "huggingface + peft": "finetuning"
    }
    
    stack_key = stack_mapping.get(stack, stack.split()[0].lower() if stack else None)
    
    if category in STACK_CONFIGS and stack_key in STACK_CONFIGS[category]:
        return STACK_CONFIGS[category][stack_key]
    
    # Try to find in any category
    for cat_name, cat_configs in STACK_CONFIGS.items():
        if stack_key in cat_configs:
            return cat_configs[stack_key]
    
    return None


def load_workshop(factory_root: Path, workshop_id: str) -> Dict[str, Any]:
    """Load workshop definition from JSON file."""
    workshop_path = factory_root / "patterns" / "workshops" / f"{workshop_id}.json"
    if not workshop_path.exists():
        raise FileNotFoundError(f"Workshop not found: {workshop_path}")
    
    with open(workshop_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_knowledge_file(factory_root: Path, filename: str) -> Optional[Dict[str, Any]]:
    """Load a knowledge file from the factory."""
    knowledge_path = factory_root / "knowledge" / filename
    if not knowledge_path.exists():
        return None
    
    with open(knowledge_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_directory_structure(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Create the project directory structure."""
    target = config.target_dir
    
    # Create main directories
    directories = stack_config.get("directories", ["src", "tests"])
    for dir_name in directories:
        (target / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Create .agent/rules directory
    (target / ".agent" / "rules").mkdir(parents=True, exist_ok=True)
    
    print(f"  Created directories: {', '.join(directories)}")


def generate_gitignore(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate .gitignore file."""
    patterns = stack_config.get("gitignore_patterns", [])
    
    # Add common patterns
    common_patterns = [
        "# IDE",
        ".vscode/",
        ".idea/",
        "",
        "# OS",
        ".DS_Store",
        "Thumbs.db",
        "",
        "# Environment",
        ".env",
        ".env.local",
        ""
    ]
    
    content = "# Auto-generated for workshop\n\n"
    content += "\n".join(common_patterns)
    content += "\n# Project-specific\n"
    content += "\n".join(patterns)
    
    gitignore_path = config.target_dir / ".gitignore"
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  Generated .gitignore")


def generate_package_json(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate package.json for npm-based projects."""
    workshop = config.workshop_data
    deps = stack_config.get("dependencies", {})
    
    package = {
        "name": config.workshop_id.lower().replace("_", "-") + "-workshop",
        "version": "1.0.0",
        "description": f"{workshop.get('name', 'Workshop')} - Learning Project",
        "main": "index.js",
        "scripts": {
            "test": "echo \"Tests not yet configured\" && exit 0"
        },
        "keywords": [workshop.get("technology", {}).get("category", "workshop")],
        "license": "MIT"
    }
    
    # Add framework-specific scripts
    if "hardhat" in str(stack_config):
        package["scripts"] = {
            "compile": "npx hardhat compile",
            "test": "npx hardhat test",
            "test:gas": "REPORT_GAS=true npx hardhat test",
            "deploy:local": "npx hardhat run scripts/deploy.js --network localhost",
            "node": "npx hardhat node",
            "clean": "npx hardhat clean",
            "console": "npx hardhat console"
        }
    
    package_path = config.target_dir / "package.json"
    with open(package_path, 'w', encoding='utf-8') as f:
        json.dump(package, f, indent=2)
    
    print("  Generated package.json")


def generate_requirements_txt(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate requirements.txt for pip-based projects."""
    deps = stack_config.get("dependencies", {})
    
    lines = [
        f"# Requirements for {config.workshop_data.get('name', 'Workshop')}",
        f"# Generated: {datetime.now().strftime('%Y-%m-%d')}",
        ""
    ]
    
    # Production dependencies
    if deps.get("prod"):
        lines.append("# Core dependencies")
        lines.extend(deps["prod"])
        lines.append("")
    
    # Dev dependencies
    if deps.get("dev"):
        lines.append("# Development dependencies")
        lines.extend(deps["dev"])
    
    req_path = config.target_dir / "requirements.txt"
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print("  Generated requirements.txt")


def generate_agentrules(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate .agentrules file for the project."""
    workshop = config.workshop_data
    technology = workshop.get("technology", {})
    
    content = f"""# {workshop.get('name', 'Workshop')} Rules

## Project Context
This is a learning project for the {workshop.get('workshopId', '')} Workshop.
Goal: Learn {technology.get('stack', 'this technology')} through hands-on exercises.

## Technology Stack
- Language: {technology.get('language', 'Unknown')}
- Framework: {technology.get('stack', 'Unknown')}
- Version: {technology.get('version', 'Latest')}

## Learning Objectives
"""
    
    # Add learning objectives
    for obj in workshop.get("learning_objectives", []):
        content += f"- {obj.get('objective', '')}\n"
    
    content += """
## Core Principles

### When Writing Code
1. Start simple, add complexity gradually
2. Write tests for every feature
3. Document as you learn
4. Ask questions when stuck

### When Stuck
1. Re-read the exercise description
2. Check the hints provided
3. Review the concept phase material
4. Ask the AI assistant for guidance

## Workshop Phases
"""
    
    # Add phase info
    for phase in workshop.get("phases", []):
        content += f"- **{phase.get('name', '')}** ({phase.get('duration_minutes', 0)} min): {phase.get('description', '')}\n"
    
    content += """
## Commands
"""
    
    # Add relevant commands based on stack
    if stack_config.get("package_manager") == "npm":
        content += """
```bash
npm install          # Install dependencies
npm test             # Run tests
npm run compile      # Compile (if applicable)
```
"""
    elif stack_config.get("package_manager") == "pip":
        content += """
```bash
pip install -r requirements.txt  # Install dependencies
pytest                           # Run tests
python src/main.py              # Run main script
```
"""
    
    agentrules_path = config.target_dir / ".agentrules"
    with open(agentrules_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  Generated .agentrules")


def generate_technology_rules(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate technology-specific rules in .agent/rules/."""
    workshop = config.workshop_data
    technology = workshop.get("technology", {})
    lang = technology.get("language", "").lower()
    
    # Load relevant knowledge files
    knowledge_content = ""
    for kf in workshop.get("knowledge_files", []):
        knowledge = load_knowledge_file(config.factory_root, kf)
        if knowledge:
            knowledge_content += f"\n## From {kf}\n\n"
            # Extract key patterns
            if "best_practices" in knowledge:
                knowledge_content += "### Best Practices\n"
                for practice in knowledge.get("best_practices", []):
                    knowledge_content += f"- {practice}\n"
            if "anti_patterns" in knowledge:
                knowledge_content += "\n### Anti-Patterns to Avoid\n"
                for name, details in knowledge.get("anti_patterns", {}).items():
                    problem = details.get("problem", "") if isinstance(details, dict) else str(details)
                    knowledge_content += f"- **{name}**: {problem}\n"
    
    # Generate rule file
    content = f"""# {technology.get('language', 'Technology')} Development Rules

## Overview
Rules for developing in {technology.get('language', 'this language')} using {technology.get('stack', 'this stack')}.

## Applies To
"""
    
    for ext in stack_config.get("file_extensions", []):
        content += f"- `**/*{ext}` files\n"
    
    content += f"""
---

{knowledge_content}

---

## Workshop-Specific Notes

This is a learning environment. Prioritize:
1. Understanding over speed
2. Clarity over cleverness
3. Questions over assumptions
4. Testing over guessing
"""
    
    # Determine rule filename
    rule_filename = f"{lang or 'technology'}.md"
    rule_path = config.target_dir / ".agent" / "rules" / rule_filename
    
    with open(rule_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Generated .agent/rules/{rule_filename}")


def generate_readme(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate comprehensive README.md."""
    workshop = config.workshop_data
    technology = workshop.get("technology", {})
    
    content = f"""# {workshop.get('name', 'Workshop')}

> **Stack:** {technology.get('stack', 'Unknown')} | **Level:** {workshop.get('level', 'Unknown')} | **Duration:** {workshop.get('duration', {}).get('total_hours', 2.5)} hours

## Overview

**Workshop ID:** `{workshop.get('workshopId', '')}`

## Prerequisites

### Required Knowledge
"""
    
    for prereq in workshop.get("prerequisites", {}).get("knowledge", []):
        content += f"- {prereq}\n"
    
    content += """
### Required Tools
"""
    
    for tool in workshop.get("prerequisites", {}).get("tools", []):
        content += f"- {tool}\n"
    
    content += """
## Learning Objectives

By the end of this workshop, you will be able to:

"""
    
    for i, obj in enumerate(workshop.get("learning_objectives", []), 1):
        content += f"{i}. **{obj.get('objective', '')}** ({obj.get('bloom_level', 'understand').title()})\n"
    
    content += """
## Workshop Timeline

| Phase | Duration |
|-------|----------|
"""
    
    for phase in workshop.get("phases", []):
        content += f"| {phase.get('name', '')} | {phase.get('duration_minutes', 0)} min |\n"
    
    content += f"""| **Total** | **{workshop.get('duration', {}).get('total_hours', 2.5)} hours** |

## Quick Start

"""
    
    if stack_config.get("package_manager") == "npm":
        content += """```bash
# Install dependencies
npm install

# Run tests
npm test

# Start development
npm run dev
```
"""
    elif stack_config.get("package_manager") == "pip":
        content += """```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```
"""
    
    content += """
## Project Structure

```
"""
    
    for dir_name in stack_config.get("directories", ["src", "tests"]):
        content += f"{dir_name}/\n"
    
    content += """.agent/rules/       # AI assistance rules
.agentrules         # Project-level AI rules
README.md            # This file
```

## Exercises

"""
    
    for exercise in workshop.get("exercises", []):
        content += f"""### {exercise.get('name', '')}

**Difficulty:** {exercise.get('difficulty', 'medium').title()} | **Duration:** {exercise.get('duration_minutes', 30)} minutes

{exercise.get('description', '')}

**Hints:**
"""
        for hint in exercise.get("hints", [])[:3]:
            content += f"- {hint}\n"
        content += "\n"
    
    content += """## Challenges

"""
    
    for challenge in workshop.get("challenges", []):
        content += f"""### {challenge.get('name', '')}

{challenge.get('description', '')}

**Requirements:**
"""
        for req in challenge.get("requirements", []):
            content += f"- {req}\n"
        content += "\n"
    
    content += """## Self-Assessment

Ask yourself:

"""
    
    for question in workshop.get("assessment", {}).get("self_assessment", []):
        content += f"- [ ] {question}\n"
    
    content += """
## Resources

"""
    
    resources = workshop.get("resources", {})
    if resources.get("official_docs"):
        content += "### Official Documentation\n"
        for doc in resources["official_docs"]:
            content += f"- {doc}\n"
        content += "\n"
    
    if resources.get("tutorials"):
        content += "### Tutorials\n"
        for tutorial in resources["tutorials"]:
            content += f"- {tutorial}\n"
        content += "\n"
    
    content += """
## Next Steps

"""
    
    next_steps = workshop.get("next_steps", {})
    if next_steps.get("next_workshop"):
        content += f"**Next Workshop:** `{next_steps['next_workshop']}`\n\n"
    
    if next_steps.get("practice_projects"):
        content += "**Practice Projects:**\n"
        for project in next_steps["practice_projects"]:
            content += f"- {project}\n"
    
    content += """
---

*Generated by Antigravity Agent Factory Workshop Export*
"""
    
    readme_path = config.target_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  Generated README.md")


def copy_knowledge_files(config: WorkshopConfig):
    """Copy relevant knowledge files to the project."""
    workshop = config.workshop_data
    knowledge_files = workshop.get("knowledge_files", [])
    
    if not knowledge_files:
        return
    
    knowledge_dir = config.target_dir / ".agent" / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    
    for kf in knowledge_files:
        src = config.factory_root / "knowledge" / kf
        if src.exists():
            dst = knowledge_dir / kf
            shutil.copy2(src, dst)
            print(f"  Copied knowledge: {kf}")


def generate_exercise_files(config: WorkshopConfig, stack_config: Dict[str, Any]):
    """Generate exercise starter files."""
    workshop = config.workshop_data
    lang = workshop.get("technology", {}).get("language", "").lower()
    
    # Determine file extension
    ext_map = {
        "solidity": ".sol",
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "rust": ".rs"
    }
    ext = ext_map.get(lang, ".txt")
    
    # Determine source directory
    src_dir = "contracts" if lang == "solidity" else "src"
    exercises_dir = config.target_dir / src_dir / "exercises"
    exercises_dir.mkdir(parents=True, exist_ok=True)
    
    for exercise in workshop.get("exercises", []):
        if exercise.get("starter_code"):
            filename = f"{exercise.get('exerciseId', 'exercise')}{ext}"
            filepath = exercises_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(exercise["starter_code"])
            
            print(f"  Created exercise: {filename}")
    
    # Create solutions directory (hidden)
    solutions_dir = config.target_dir / ".solutions"
    solutions_dir.mkdir(parents=True, exist_ok=True)
    
    for exercise in workshop.get("exercises", []):
        if exercise.get("solution_code"):
            filename = f"{exercise.get('exerciseId', 'exercise')}_solution{ext}"
            filepath = solutions_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(exercise["solution_code"])
    
    # Add solutions to gitignore
    gitignore_path = config.target_dir / ".gitignore"
    with open(gitignore_path, 'a', encoding='utf-8') as f:
        f.write("\n# Solutions (hidden until needed)\n.solutions/\n")


def generate_ai_context_file(config: WorkshopConfig):
    """Generate an AI context file for enhanced assistance."""
    workshop = config.workshop_data
    
    content = f"""# AI Learning Assistant Context

## Workshop Information
- **ID:** {workshop.get('workshopId', '')}
- **Name:** {workshop.get('name', '')}
- **Level:** {workshop.get('level', '')}
- **Duration:** {workshop.get('duration', {}).get('total_hours', 2.5)} hours

## Current Phase Guidance

When assisting with this workshop:

### Phase 1: Concept
- Explain concepts clearly with examples
- Use diagrams when helpful
- Answer foundational questions patiently

### Phase 2: Demo
- Walk through code step by step
- Explain the "why" behind each decision
- Point out best practices

### Phase 3: Exercise
- Provide hints when asked
- Help debug without giving solutions
- Encourage experimentation

### Phase 4: Challenge
- Be more hands-off
- Guide toward solutions rather than provide them
- Celebrate progress and learning

### Phase 5: Reflection
- Help consolidate learning
- Connect concepts to real-world applications
- Suggest next steps

## Learning Objectives to Support
"""
    
    for obj in workshop.get("learning_objectives", []):
        content += f"""
### {obj.get('objective', '')}
- Bloom's Level: {obj.get('bloom_level', 'understand')}
- Verification: {obj.get('verification', '')}
"""
    
    content += """
## Common Questions & Answers
"""
    
    for phase in workshop.get("phases", []):
        if phase.get("common_questions"):
            content += f"\n### {phase.get('name', '')}\n"
            for q in phase["common_questions"]:
                content += f"- {q}\n"
    
    content += """
## Axiom Zero Integration

Remember to embody:
- **Love:** Patient explanations, encouraging feedback, celebrating progress
- **Truth:** Accurate information, honest about limitations, verified code
- **Beauty:** Clean code, elegant solutions, well-structured learning
"""
    
    context_path = config.target_dir / ".agent" / "WORKSHOP_CONTEXT.md"
    with open(context_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  Generated WORKSHOP_CONTEXT.md")


def export_workshop(workshop_id: str, target_dir: str, factory_root: str = None):
    """
    Main export function.
    
    Args:
        workshop_id: Workshop identifier (e.g., 'L1_ethereum_fundamentals')
        target_dir: Target directory for the exported project
        factory_root: Path to the Antigravity Agent Factory (auto-detected if None)
    """
    # Determine factory root
    if factory_root is None:
        factory_root = Path(__file__).parent.parent.parent
    else:
        factory_root = Path(factory_root)
    
    target_path = Path(target_dir)
    
    print(f"\n{'='*60}")
    print(f"Exporting Workshop: {workshop_id}")
    print(f"Target: {target_path}")
    print(f"{'='*60}\n")
    
    # Load workshop definition
    print("Loading workshop definition...")
    workshop_data = load_workshop(factory_root, workshop_id)
    
    # Get stack configuration
    technology = workshop_data.get("technology", {})
    stack_config = get_stack_config(technology)
    
    if not stack_config:
        print(f"Warning: No specific stack config found for {technology}")
        stack_config = {
            "package_manager": "pip",
            "main_language": "python",
            "directories": ["src", "tests"],
            "file_extensions": [".py"],
            "gitignore_patterns": ["__pycache__/", "*.pyc", ".env", ".venv/"]
        }
    
    # Create config
    config = WorkshopConfig(
        workshop_id=workshop_id,
        target_dir=target_path,
        factory_root=factory_root,
        workshop_data=workshop_data
    )
    
    # Create target directory
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Generate all artifacts
    print("\nGenerating project structure...")
    create_directory_structure(config, stack_config)
    
    print("\nGenerating configuration files...")
    generate_gitignore(config, stack_config)
    
    if stack_config.get("package_manager") == "npm":
        generate_package_json(config, stack_config)
    elif stack_config.get("package_manager") == "pip":
        generate_requirements_txt(config, stack_config)
    
    print("\nGenerating Antigravity rules...")
    generate_agentrules(config, stack_config)
    generate_technology_rules(config, stack_config)
    
    print("\nCopying knowledge files...")
    copy_knowledge_files(config)
    
    print("\nGenerating exercise files...")
    generate_exercise_files(config, stack_config)
    
    print("\nGenerating documentation...")
    generate_readme(config, stack_config)
    generate_ai_context_file(config)
    
    print(f"\n{'='*60}")
    print(f"Export complete!")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  1. Open {target_path} in your IDE")
    print(f"  2. Install dependencies")
    print(f"  3. Read README.md to begin the workshop")
    print(f"\nHappy learning!")
    
    return str(target_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python export_workshop.py <workshop_id> <target_directory>")
        print("Example: python export_workshop.py L1_ethereum_fundamentals c:/App/learning/ethereum")
        sys.exit(1)
    
    workshop_id = sys.argv[1]
    target_dir = sys.argv[2]
    factory_root = sys.argv[3] if len(sys.argv) > 3 else None
    
    export_workshop(workshop_id, target_dir, factory_root)
