# User Guide

For a comprehensive list of all available resources, see the ****Antigravity Catalog****. This guide explains how to use the **Antigravity Agent Factory** to generate and manage AI-powered development systems.

## Core Concepts

- **Blueprints**: Pre-configured templates for common tech stacks. **View all Blueprints**
- **Agents**: Specialized AI assistants tailored for specific roles. **View all Agents**
- **Skills**: Modular capabilities that agents can use. **View all Skills**
- **Workflows**: Standard operating procedures for development. **View all Workflows**
- **MCP Servers**: Model Context Protocol servers that provide tools for filesystem access, git, etc.

## Usage Patterns

### 1. Generating a New Project (Quick Start)
Run the following command to generate a demo project in 5 minutes:
```bash
python cli/factory_cli.py --quickstart
```

### 2. Using Blueprints
To see all available blueprints:
```bash
python cli/factory_cli.py --list-blueprints
```
To generate a project from a specific blueprint:
```bash
python cli/factory_cli.py --blueprint python-fastapi --output ./my-new-project
```

### 3. Interactive Mode
For a custom setup with specific agents and skills:
```bash
python cli/factory_cli.py --interactive
```

### 4. Analyzing an Existing Project
To check if a project is ready for Antigravity:
```bash
python cli/factory_cli.py --analyze ./my-existing-repo
```

## Agent Configuration

The factory generates a `.agentrules` file in your project root. This file contains the instructions that guide the AI's behavior. Simply open your project in a compatible IDE (like Cursor or VS Code with Antigravity extensions) to start using the agents.
