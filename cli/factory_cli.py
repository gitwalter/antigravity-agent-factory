#!/usr/bin/env python3
"""
Antigravity Agent Factory - Command Line Interface
CLI for generating Cursor agent development systems.

Usage:
    python factory_cli.py --config project.yaml --output C:\\Projects\\my-project
    python factory_cli.py --blueprint python-fastapi --output C:\\Projects\\my-project
    python factory_cli.py --interactive --output C:\\Projects\\my-project
    python factory_cli.py --list-blueprints

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.core.generate_project import ProjectConfig, ProjectGenerator, create_quickstart_config


def get_factory_root() -> Path:
    """Get the factory root directory.
    
    Returns:
        Path to factory root.
    """
    return Path(__file__).parent.parent


def display_welcome() -> None:
    """Display warm welcome message."""
    print()
    print("=" * 60)
    print("  Welcome to Antigravity Agent Factory!")
    print("=" * 60)
    print()
    print("We're excited to show you what's possible.")
    print("Let's create something amazing together...")
    print()


def display_tour(output_dir: str, files_created: int) -> None:
    """Display post-generation tour with warm, caring guidance.
    
    Args:
        output_dir: Path to generated project.
        files_created: Number of files created.
    """
    print()
    print("=" * 60)
    print("  Congratulations! Your project is ready!")
    print("=" * 60)
    print()
    print(f"We created {files_created} files for you in: {output_dir}")
    print()
    print("Here's what you got:")
    print("  .agentrules    Your AI guidance system (the brain)")
    print("  PURPOSE.md      Your project's mission (the heart)")
    print("  .agent/agents/ Specialized AI assistants (your team)")
    print("  .agent/skills/ Reusable capabilities")
    print("  workflows/      Development methodology")
    print("  knowledge/      Domain knowledge files")
    print()
    print("Ready to try it out?")
    print(f"  1. Open {output_dir} in Antigravity IDE")
    print('  2. Ask: "Help me understand this project"')
    print('  3. Ask: "Create a new task endpoint"')
    print()
    print("When you're ready to build your own:")
    print("  python cli/factory_cli.py --interactive")
    print()
    print("We can't wait to see what you create!")
    print()


def display_error_with_help(error_msg: str, suggestion: str) -> None:
    """Display error message with caring, helpful guidance.
    
    Args:
        error_msg: The error that occurred.
        suggestion: Helpful suggestion for fixing it.
    """
    print()
    print("Oops! Something went wrong, but don't worry - we can fix this.")
    print()
    print(f"  What happened: {error_msg}")
    print(f"  How to fix it: {suggestion}")
    print()
    print("Still stuck? Check docs/TROUBLESHOOTING.md or open an issue.")
    print("Remember: Every expert was once a beginner. You've got this!")
    print()


def run_quickstart(output_dir: str = None, blueprint_id: str = None) -> None:
    """Run zero-config quick start to generate a demo project.
    
    This creates a complete demo project with sensible defaults,
    allowing users to see the factory's value in under 5 minutes.
    
    Args:
        output_dir: Optional output directory (defaults to ./quickstart-demo).
        blueprint_id: Optional blueprint override (defaults to python-fastapi).
    """
    display_welcome()
    
    # Set defaults
    if output_dir is None:
        output_dir = "./quickstart-demo"
    
    # Create configuration
    config = create_quickstart_config()
    
    # Override blueprint if specified
    if blueprint_id:
        config.blueprint_id = blueprint_id
        print(f"Using blueprint: {blueprint_id}")
    else:
        print(f"Using blueprint: {config.blueprint_id} (Python + FastAPI)")
    
    print(f"Output directory: {output_dir}")
    print()
    
    # Generate with progress
    print("Building your demo project with care...")
    
    try:
        generator = ProjectGenerator(config, output_dir)
        result = generator.generate()
        
        if result['success']:
            display_tour(output_dir, len(result['files_created']))
        else:
            error_msg = result['errors'][0] if result['errors'] else "Unknown error"
            display_error_with_help(
                error_msg,
                "Try running from the factory root directory, or check file permissions."
            )
            sys.exit(1)
            
    except Exception as e:
        display_error_with_help(
            str(e),
            "Make sure you have write permissions to the output directory."
        )
        sys.exit(1)


def list_blueprints() -> None:
    """List all available blueprints."""
    blueprints_dir = get_factory_root() / '.agent' / 'blueprints'
    
    print("\n[*] Available Blueprints\n")
    print("-" * 60)
    
    for blueprint_dir in sorted(blueprints_dir.iterdir()):
        if blueprint_dir.is_dir():
            blueprint_file = blueprint_dir / 'blueprint.json'
            if blueprint_file.exists():
                with open(blueprint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata = data.get('metadata', {})
                    name = metadata.get('blueprintName', blueprint_dir.name)
                    desc = metadata.get('description', 'No description')
                    tags = metadata.get('tags', [])
                    
                    print(f"\n  {blueprint_dir.name}")
                    print(f"    Name: {name}")
                    print(f"    Description: {desc}")
                    print(f"    Tags: {', '.join(tags)}")
            else:
                print(f"\n  {blueprint_dir.name} (no blueprint.json)")
    
    print("\n" + "-" * 60)
    print("\nUsage: python factory_cli.py --blueprint <blueprint-id> --output <path>\n")


def list_patterns() -> None:
    """List all available patterns."""
    patterns_dir = get_factory_root() / '.agent' / 'patterns'
    
    print("\n[*] Available Patterns\n")
    print("-" * 60)
    
    for pattern_type in ['agents', 'skills', 'workflows']:
        type_dir = patterns_dir / pattern_type
        if type_dir.exists():
            print(f"\n  {pattern_type.upper()}:")
            for pattern_file in sorted(type_dir.glob('*.json')):
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata = data.get('metadata', {})
                    desc = metadata.get('description', '')
                    print(f"    - {pattern_file.stem}: {desc}")
    
    print("\n" + "-" * 60 + "\n")


def interactive_mode(output_dir: str) -> None:
    """Run interactive requirements gathering.
    
    Args:
        output_dir: Target output directory.
    """
    print("\n=== Antigravity Agent Factory - Interactive Mode ===\n")
    print("=" * 60)
    print("Let's gather requirements for your new agent system.\n")
    
    # Phase 1: Project Context
    print("[PHASE 1] Project Context\n")
    
    project_name = input("1. Project name: ").strip()
    if not project_name:
        project_name = "new-agent-project"
    
    project_description = input("2. Project description: ").strip()
    
    print("\n   Available domains: web, mobile, data-science, sap, devops, general")
    domain = input("3. Domain/Industry [general]: ").strip() or "general"
    
    team_context = input("4. Team size and experience (optional): ").strip()
    
    # Phase 2: Technology Stack
    print("\n[PHASE 2] Technology Stack\n")
    
    print("   Available languages: python, typescript, java, csharp, go, rust, abap")
    primary_language = input("1. Primary programming language [python]: ").strip() or "python"
    
    frameworks_input = input("2. Frameworks (comma-separated, e.g., fastapi,sqlalchemy): ").strip()
    frameworks = [f.strip() for f in frameworks_input.split(',')] if frameworks_input else []
    
    # Check for matching blueprint
    blueprint_id = None
    if primary_language == 'python' and 'fastapi' in [f.lower() for f in frameworks]:
        blueprint_id = 'python-fastapi'
        print(f"\n   [OK] Matched blueprint: {blueprint_id}")
    elif primary_language == 'typescript' and 'react' in [f.lower() for f in frameworks]:
        blueprint_id = 'typescript-react'
        print(f"\n   [OK] Matched blueprint: {blueprint_id}")
    elif primary_language == 'java' and 'spring' in [f.lower() for f in frameworks]:
        blueprint_id = 'java-spring'
        print(f"\n   [OK] Matched blueprint: {blueprint_id}")
    elif primary_language == 'abap':
        blueprint_id = 'sap-abap'
        print(f"\n   [OK] Matched blueprint: {blueprint_id}")
    
    # Phase 3: Workflow
    print("\n[PHASE 3] Workflow Methodology\n")
    
    print("   Available triggers: jira, confluence, github, gitlab, manual")
    triggers_input = input("1. Workflow triggers (comma-separated) [manual]: ").strip() or "manual"
    triggers = [t.strip() for t in triggers_input.split(',')]
    
    # Phase 4: Agents & Skills
    print("\n[PHASE 4] Agent Capabilities\n")
    
    print("   Available agents: code-reviewer, test-generator, explorer")
    agents_input = input("1. Agents to include (comma-separated) [code-reviewer]: ").strip() or "code-reviewer"
    agents = [a.strip() for a in agents_input.split(',')]
    
    print("   Available skills: bugfix-workflow, feature-workflow, grounding, tdd, code-templates")
    skills_input = input("2. Skills to include (comma-separated) [bugfix-workflow,tdd]: ").strip() or "bugfix-workflow,tdd"
    skills = [s.strip() for s in skills_input.split(',')]
    
    # Phase 5: Project Management (Optional)
    print("\n[PHASE 5] Project Management (Optional)\n")
    
    pm_enabled = False
    pm_backend = None
    pm_doc_backend = None
    pm_methodology = None
    
    enable_pm = input("1. Enable project management system? [y/N]: ").strip().lower()
    if enable_pm == 'y':
        pm_enabled = True
        
        print("\n   Available PM backends: github, jira, azure-devops, linear")
        pm_backend = input("2. PM backend [github]: ").strip() or "github"
        
        print("\n   Available doc backends: github-wiki, confluence, azure-wiki, none")
        pm_doc_backend = input("3. Documentation backend [github-wiki]: ").strip() or "github-wiki"
        
        print("\n   Available methodologies: scrum, kanban, hybrid, waterfall")
        pm_methodology = input("4. Methodology [scrum]: ").strip() or "scrum"
        
        print(f"\n   [OK] PM system enabled: {pm_backend} + {pm_methodology}")
    
    # Phase 6: MCP Servers
    print("\n[PHASE 6] MCP Server Integration\n")
    
    mcp_servers = []
    
    # Define starter packs
    starter_packs = {
        'minimal': {
            'name': 'Minimal Starter',
            'servers': ['filesystem', 'git', 'memory']
        },
        'web-developer': {
            'name': 'Web Developer Starter',
            'servers': ['filesystem', 'git', 'memory', 'github', 'postgresql', 'playwright']
        },
        'data-science': {
            'name': 'Data Science Starter',
            'servers': ['filesystem', 'memory', 'time', 'jupyter', 'bigquery', 'pinecone']
        },
        'ai-agent': {
            'name': 'AI Agent Starter',
            'servers': ['filesystem', 'memory', 'sequentialthinking', 'langgraph', 'knowledge-graph', 'chromadb']
        },
        'enterprise': {
            'name': 'Enterprise Starter',
            'servers': ['filesystem', 'git', 'memory', 'github', 'atlassian', 'slack', 'sentry']
        }
    }
    
    # Server configs for quick access
    server_configs = {
        'filesystem': {'name': 'filesystem', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-filesystem', '.'], 'purpose': 'File operations'},
        'git': {'name': 'git', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-git', '--repository', '.'], 'purpose': 'Git operations'},
        'memory': {'name': 'memory', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-memory'], 'purpose': 'Persistent memory'},
        'time': {'name': 'time', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-time'], 'purpose': 'Date/time utilities'},
        'fetch': {'name': 'fetch', 'purpose': 'Web content (built-in)'},
        'sequentialthinking': {'name': 'sequentialthinking', 'url': 'https://remote.mcpservers.org/sequentialthinking/mcp', 'purpose': 'Problem-solving'},
        'github': {'name': 'github', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-github'], 'env': {'GITHUB_TOKEN': '${GITHUB_TOKEN}'}, 'purpose': 'GitHub integration'},
        'atlassian': {'name': 'atlassian', 'url': 'https://mcp.atlassian.com/v1/sse', 'purpose': 'Jira/Confluence'},
        'linear': {'name': 'linear', 'url': 'https://mcp.linear.app/mcp', 'purpose': 'Linear issues'},
        'slack': {'name': 'slack', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-slack'], 'env': {'SLACK_BOT_TOKEN': '${SLACK_BOT_TOKEN}'}, 'purpose': 'Slack messaging'},
        'sentry': {'name': 'sentry', 'command': 'npx', 'args': ['-y', '@sentry/mcp-server'], 'env': {'SENTRY_AUTH_TOKEN': '${SENTRY_AUTH_TOKEN}'}, 'purpose': 'Error tracking'},
        'playwright': {'name': 'playwright', 'command': 'npx', 'args': ['-y', '@playwright/mcp@latest'], 'purpose': 'Browser automation'},
        'postgresql': {'name': 'postgresql', 'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-postgres'], 'env': {'DATABASE_URL': '${DATABASE_URL}'}, 'purpose': 'PostgreSQL database'},
        'mongodb': {'name': 'mongodb', 'command': 'npx', 'args': ['-y', '@mongodb/mcp-server'], 'env': {'MONGODB_URI': '${MONGODB_URI}'}, 'purpose': 'MongoDB database'},
        'pinecone': {'name': 'pinecone', 'command': 'npx', 'args': ['-y', '@pinecone/mcp-server'], 'env': {'PINECONE_API_KEY': '${PINECONE_API_KEY}'}, 'purpose': 'Vector database'},
        'chromadb': {'name': 'chromadb', 'command': 'npx', 'args': ['-y', 'chroma-mcp-server'], 'purpose': 'Local embeddings'},
        'bigquery': {'name': 'bigquery', 'url': 'https://bigquery.googleapis.com/mcp', 'purpose': 'BigQuery analytics'},
        'docker': {'name': 'docker', 'command': 'npx', 'args': ['-y', '@docker/mcp-server'], 'purpose': 'Container management'},
        'deepwiki': {'name': 'deepwiki', 'url': 'https://mcp.deepwiki.com/mcp', 'purpose': 'GitHub repo docs'},
        'huggingface': {'name': 'huggingface', 'url': 'https://huggingface.co/mcp', 'env': {'HF_TOKEN': '${HF_TOKEN}'}, 'purpose': 'HuggingFace Hub'},
        'mlflow': {'name': 'mlflow', 'command': 'mlflow-mcp-server', 'env': {'MLFLOW_TRACKING_URI': '${MLFLOW_TRACKING_URI}'}, 'purpose': 'ML experiment tracking'},
        'langgraph': {'name': 'langgraph', 'purpose': 'Agent orchestration (requires deployment URL)'},
        'knowledge-graph': {'name': 'knowledge-graph', 'command': 'npx', 'args': ['-y', 'mcp-knowledge-graph'], 'purpose': 'Agent memory'},
        'jupyter': {'name': 'jupyter', 'command': 'npx', 'args': ['-y', 'jupyter-mcp-server'], 'purpose': 'Notebook execution'},
        'ollama': {'name': 'ollama', 'command': 'npx', 'args': ['-y', 'ollama-mcp'], 'purpose': 'Local LLM'},
        'brave-search': {'name': 'brave-search', 'command': 'npx', 'args': ['-y', '@anthropics/mcp-server-brave-search'], 'env': {'BRAVE_API_KEY': '${BRAVE_API_KEY}'}, 'purpose': 'Web search'},
        'notion': {'name': 'notion', 'url': 'https://mcp.notion.so/mcp', 'purpose': 'Notion docs'},
        'figma': {'name': 'figma', 'url': 'https://mcp.figma.com', 'purpose': 'Design extraction'},
        'sap-documentation': {'name': 'sap-documentation', 'url': 'https://mcp-sap-docs.marianzeis.de/mcp', 'purpose': 'SAP Help Portal'},
        'sap-abap-documentation': {'name': 'sap-abap-documentation', 'url': 'https://mcp-abap.marianzeis.de/mcp', 'purpose': 'ABAP keywords, DSAG guidelines, Clean ABAP'}    }
    
    # Step 1: Ask about starter pack
    print("   Choose a starter pack or custom selection:\n")
    print("   1. Minimal (3 servers) - filesystem, git, memory")
    print("   2. Web Developer (6 servers) - + github, postgresql, playwright")
    print("   3. Data Science (6 servers) - + jupyter, bigquery, pinecone")
    print("   4. AI Agent (6 servers) - + langgraph, knowledge-graph, chromadb")
    print("   5. Enterprise (7 servers) - + atlassian, slack, sentry")
    print("   6. Custom - Select individual servers")
    print("   7. Skip - No MCP servers")
    
    pack_choice = input("\n   Select option [1]: ").strip() or "1"
    
    selected_servers = []
    
    if pack_choice == "1":
        selected_servers = starter_packs['minimal']['servers'].copy()
        print(f"\n   [OK] Using Minimal Starter: {', '.join(selected_servers)}")
    elif pack_choice == "2":
        selected_servers = starter_packs['web-developer']['servers'].copy()
        print(f"\n   [OK] Using Web Developer Starter: {', '.join(selected_servers)}")
    elif pack_choice == "3":
        selected_servers = starter_packs['data-science']['servers'].copy()
        print(f"\n   [OK] Using Data Science Starter: {', '.join(selected_servers)}")
    elif pack_choice == "4":
        selected_servers = starter_packs['ai-agent']['servers'].copy()
        print(f"\n   [OK] Using AI Agent Starter: {', '.join(selected_servers)}")
    elif pack_choice == "5":
        selected_servers = starter_packs['enterprise']['servers'].copy()
        print(f"\n   [OK] Using Enterprise Starter: {', '.join(selected_servers)}")
    elif pack_choice == "6":
        # Custom selection - show categories
        print("\n   Available servers by category:\n")
        print("   CORE: filesystem, git, memory, time, fetch, brave-search, sequentialthinking")
        print("   CODE: github, sentry, playwright, deepwiki, sap-documentation")
        print("   DATA: postgresql, mongodb, pinecone, chromadb, bigquery")
        print("   CLOUD: docker")
        print("   COLLAB: atlassian, linear, slack, notion, figma")
        print("   AI/ML: huggingface, mlflow, langgraph, knowledge-graph, ollama, jupyter")
        
        custom_input = input("\n   Enter servers (comma-separated): ").strip()
        if custom_input:
            selected_servers = [s.strip() for s in custom_input.split(',')]
            print(f"\n   [OK] Selected: {', '.join(selected_servers)}")
    elif pack_choice == "7":
        print("\n   [OK] Skipping MCP server configuration")
    
    # Auto-add based on PM backend
    if pm_enabled:
        if pm_backend == 'github' and 'github' not in selected_servers:
            selected_servers.append('github')
            print("   [OK] Auto-added GitHub MCP for PM")
        elif pm_backend == 'jira' and 'atlassian' not in selected_servers:
            selected_servers.append('atlassian')
            print("   [OK] Auto-added Atlassian MCP for Jira")
        elif pm_backend == 'azure-devops':
            mcp_servers.append({
                'name': 'azure-devops',
                'command': 'npx',
                'args': ['-y', '@mcp-apps/azure-devops-mcp-server'],
                'purpose': 'Azure DevOps Work Items'
            })
            print("   [OK] Auto-added Azure DevOps MCP")
        elif pm_backend == 'linear' and 'linear' not in selected_servers:
            selected_servers.append('linear')
            print("   [OK] Auto-added Linear MCP for PM")
    
    # Auto-add based on triggers
    if 'jira' in triggers or 'confluence' in triggers:
        if 'atlassian' not in selected_servers:
            selected_servers.append('atlassian')
            print("   [OK] Auto-added Atlassian MCP for Jira/Confluence triggers")
    
    if 'github' in triggers and 'github' not in selected_servers:
        selected_servers.append('github')
        print("   [OK] Auto-added GitHub MCP for GitHub triggers")
    
    # Convert selected servers to MCP config
    for server_id in selected_servers:
        if server_id in server_configs:
            mcp_servers.append(server_configs[server_id])
    
    # Step 2: Ask about custom/local servers
    add_custom = input("\n   Add custom/local MCP servers? [y/N]: ").strip().lower()
    if add_custom == 'y':
        while True:
            print("\n   Enter custom server details (or 'done' to finish):")
            custom_name = input("   Server name: ").strip()
            if custom_name.lower() == 'done' or not custom_name:
                break
            custom_command = input("   Command (e.g., python, npx): ").strip()
            custom_args = input("   Arguments (comma-separated): ").strip()
            custom_env = input("   Env vars (VAR1=val1,VAR2=val2): ").strip()
            custom_purpose = input("   Purpose: ").strip()
            
            custom_server = {
                'name': custom_name,
                'command': custom_command,
                'purpose': custom_purpose or 'Custom server'
            }
            if custom_args:
                custom_server['args'] = [a.strip() for a in custom_args.split(',')]
            if custom_env:
                env_dict = {}
                for pair in custom_env.split(','):
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        env_dict[k.strip()] = v.strip()
                custom_server['env'] = env_dict
            
            mcp_servers.append(custom_server)
            print(f"   [OK] Added custom server: {custom_name}")
    
    # Summary
    print("\n" + "=" * 60)
    print("[SUMMARY] REQUIREMENTS\n")
    print(f"  Project: {project_name}")
    print(f"  Description: {project_description}")
    print(f"  Domain: {domain}")
    print(f"  Language: {primary_language}")
    print(f"  Frameworks: {', '.join(frameworks) if frameworks else 'None'}")
    print(f"  Blueprint: {blueprint_id or 'None (custom)'}")
    print(f"  Triggers: {', '.join(triggers)}")
    print(f"  Agents: {', '.join(agents)}")
    print(f"  Skills: {', '.join(skills)}")
    print(f"  MCP Servers: {len(mcp_servers)}")
    if pm_enabled:
        print("  PM System: Enabled")
        print(f"    Backend: {pm_backend}")
        print(f"    Doc Backend: {pm_doc_backend}")
        print(f"    Methodology: {pm_methodology}")
    else:
        print("  PM System: Disabled")
    print(f"  Output: {output_dir}")
    print("=" * 60)
    
    confirm = input("\nGenerate project? [Y/n]: ").strip().lower()
    if confirm == 'n':
        print("Cancelled.")
        return
    
    # Add PM agents and skills if enabled
    if pm_enabled:
        agents.extend(['product-owner', 'sprint-master', 'task-manager', 'reporting-agent'])
        skills.extend(['create-epic', 'create-story', 'create-task', 'estimate-task', 
                       'run-standup', 'plan-sprint', 'close-sprint', 'generate-burndown', 'health-check'])
    
    # Generate
    config = ProjectConfig(
        project_name=project_name,
        project_description=project_description,
        domain=domain,
        primary_language=primary_language,
        frameworks=frameworks,
        triggers=triggers,
        agents=agents,
        skills=skills,
        mcp_servers=mcp_servers,
        blueprint_id=blueprint_id,
        team_context=team_context,
        pm_enabled=pm_enabled,
        pm_backend=pm_backend,
        pm_doc_backend=pm_doc_backend,
        pm_methodology=pm_methodology
    )
    
    generator = ProjectGenerator(config, output_dir)
    result = generator.generate()
    
    if result['success']:
        print("\n[SUCCESS] Project generated successfully!")
        print(f"   Location: {result['target_dir']}")
        print(f"   Files created: {len(result['files_created'])}")
        print("\n   Next steps:")
        print("   1. Open the project in Antigravity IDE")
        print("   2. The .agentrules will configure agent behavior")
        print("   3. Start developing with AI assistance!")
    else:
        print("\n[ERROR] Generation failed:")
        for error in result['errors']:
            print(f"   - {error}")


def generate_from_blueprint(
    blueprint_id: str, 
    output_dir: str, 
    project_name: str = None,
    pm_enabled: bool = False,
    pm_backend: str = None,
    pm_doc_backend: str = None,
    pm_methodology: str = None
) -> None:
    """Generate project from a blueprint.
    
    Args:
        blueprint_id: Blueprint identifier.
        output_dir: Target output directory.
        project_name: Optional project name override.
        pm_enabled: If True, include PM system.
        pm_backend: PM backend (github, jira, azure-devops, linear).
        pm_doc_backend: Documentation backend.
        pm_methodology: PM methodology (scrum, kanban, hybrid, waterfall).
    """
    blueprint_path = get_factory_root() / '.agent' / 'blueprints' / blueprint_id / 'blueprint.json'
    
    if not blueprint_path.exists():
        print(f"[ERROR] Blueprint not found: {blueprint_id}")
        print("   Use --list-blueprints to see available blueprints")
        sys.exit(1)
    
    with open(blueprint_path, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)
    
    metadata = blueprint.get('metadata', {})
    stack = blueprint.get('stack', {})
    
    # Extract agents and skills from blueprint
    agents = [a['patternId'] for a in blueprint.get('agents', [])]
    skills = [s['patternId'] for s in blueprint.get('skills', [])]
    mcp_servers = blueprint.get('mcpServers', [])
    
    # Add PM agents, skills, and MCP servers if enabled
    if pm_enabled:
        agents.extend(['product-owner', 'sprint-master', 'task-manager', 'reporting-agent'])
        skills.extend(['create-epic', 'create-story', 'create-task', 'estimate-task', 
                       'run-standup', 'plan-sprint', 'close-sprint', 'generate-burndown', 'health-check'])
        
        # Add PM MCP server
        if pm_backend == 'github':
            mcp_servers.append({
                'name': 'github-pm',
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-github'],
                'purpose': 'GitHub Issues and Projects'
            })
        elif pm_backend == 'jira':
            mcp_servers.append({
                'name': 'atlassian',
                'url': 'https://mcp.atlassian.com/v1/sse',
                'purpose': 'Jira integration'
            })
        elif pm_backend == 'azure-devops':
            mcp_servers.append({
                'name': 'azure-devops',
                'command': 'npx',
                'args': ['-y', '@mcp-apps/azure-devops-mcp-server'],
                'purpose': 'Azure DevOps Work Items'
            })
        elif pm_backend == 'linear':
            mcp_servers.append({
                'name': 'linear',
                'command': 'npx',
                'args': ['-y', 'mcp-remote', 'https://mcp.linear.app/sse'],
                'purpose': 'Linear Issues and Projects'
            })
        
        print(f"   [OK] PM system enabled: {pm_backend} + {pm_methodology}")
    
    # Extract configuration from blueprint
    config = ProjectConfig(
        project_name=project_name or blueprint_id + '-project',
        project_description=metadata.get('description', ''),
        domain=', '.join(metadata.get('tags', [])),
        primary_language=stack.get('primaryLanguage', 'python'),
        frameworks=[f['name'] for f in stack.get('frameworks', [])],
        triggers=['jira', 'confluence'],  # Default triggers
        agents=agents,
        skills=skills,
        mcp_servers=mcp_servers,
        blueprint_id=blueprint_id,
        pm_enabled=pm_enabled,
        pm_backend=pm_backend,
        pm_doc_backend=pm_doc_backend,
        pm_methodology=pm_methodology
    )
    
    print(f"\n[*] Generating from blueprint: {blueprint_id}")
    print(f"   Output: {output_dir}\n")
    
    # Check knowledge coverage before generation
    _check_blueprint_knowledge(blueprint_id)
    
    generator = ProjectGenerator(config, output_dir)
    result = generator.generate()
    
    if result['success']:
        print("\n[SUCCESS] Project generated successfully!")
        print(f"   Location: {result['target_dir']}")
        print(f"   Files created: {len(result['files_created'])}")
    else:
        print("\n[ERROR] Generation failed:")
        for error in result['errors']:
            print(f"   - {error}")
        sys.exit(1)


def generate_from_config_file(config_path: str, output_dir: str) -> None:
    """Generate project from configuration file.
    
    Args:
        config_path: Path to configuration file.
        output_dir: Target output directory.
    """
    if not os.path.exists(config_path):
        print(f"[ERROR] Configuration file not found: {config_path}")
        sys.exit(1)
    
    try:
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        else:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        config = ProjectConfig.from_dict(data)
        
        print(f"\n[*] Generating from config: {config_path}")
        print(f"   Project: {config.project_name}")
        print(f"   Output: {output_dir}\n")
        
        generator = ProjectGenerator(config, output_dir)
        result = generator.generate()
        
        if result['success']:
            print("\n[SUCCESS] Project generated successfully!")
            print(f"   Location: {result['target_dir']}")
            print(f"   Files created: {len(result['files_created'])}")
        else:
            print("\n[ERROR] Generation failed:")
            for error in result['errors']:
                print(f"   - {error}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Error loading configuration: {e}")
        sys.exit(1)


def analyze_repository(repo_path: str) -> None:
    """Analyze an existing repository for Cursor artifacts.
    
    Args:
        repo_path: Path to repository to analyze.
    """
    from scripts.analysis.repo_analyzer import RepoAnalyzer
    
    print(f"\n[*] Analyzing repository: {repo_path}\n")
    print("=" * 60)
    
    try:
        analyzer = RepoAnalyzer(repo_path)
        inventory = analyzer.analyze()
        print(inventory.get_summary())
        print("=" * 60)
    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")
        sys.exit(1)


def onboard_repository(
    repo_path: str,
    blueprint_id: str = None,
    dry_run: bool = False,
    pm_enabled: bool = False,
    pm_backend: str = None,
    pm_doc_backend: str = None,
    pm_methodology: str = None
) -> None:
    """Onboard an existing repository with Antigravity Agent Factory.
    Args:
        repo_path: Path to repository to onboard.
        blueprint_id: Optional blueprint to use.
        dry_run: If True, preview changes without making them.
        pm_enabled: If True, include PM system.
        pm_backend: PM backend (github, jira, azure-devops, linear).
        pm_doc_backend: Documentation backend.
        pm_methodology: PM methodology (scrum, kanban, hybrid, waterfall).
    """
    from scripts.analysis.repo_analyzer import RepoAnalyzer
    
    print(f"\n[*] Onboarding repository: {repo_path}")
    if dry_run:
        print("    Mode: DRY RUN (no changes will be made)")
    print("=" * 60 + "\n")
    
    try:
        # First analyze to get tech stack info
        analyzer = RepoAnalyzer(repo_path)
        inventory = analyzer.analyze()
        
        # Use suggested blueprint if not specified
        if not blueprint_id and inventory.tech_stack.suggested_blueprint:
            blueprint_id = inventory.tech_stack.suggested_blueprint
            print(f"[*] Auto-detected blueprint: {blueprint_id}")
        
        # Load blueprint or use defaults
        if blueprint_id:
            blueprint_path = get_factory_root() / '.agent' / 'blueprints' / blueprint_id / 'blueprint.json'
            if blueprint_path.exists():
                with open(blueprint_path, 'r', encoding='utf-8') as f:
                    blueprint = json.load(f)
                
                stack = blueprint.get('stack', {})
                config = ProjectConfig(
                    project_name=Path(repo_path).name,
                    project_description=blueprint.get('metadata', {}).get('description', ''),
                    domain=', '.join(blueprint.get('metadata', {}).get('tags', [])),
                    primary_language=stack.get('primaryLanguage', 'python'),
                    frameworks=[f['name'] for f in stack.get('frameworks', [])],
                    triggers=['jira', 'confluence'],
                    agents=[a['patternId'] for a in blueprint.get('agents', [])],
                    skills=[s['patternId'] for s in blueprint.get('skills', [])],
                    mcp_servers=blueprint.get('mcpServers', []),
                    blueprint_id=blueprint_id
                )
            else:
                print(f"[WARNING] Blueprint not found: {blueprint_id}")
                config = _create_default_config(repo_path, inventory)
        else:
            config = _create_default_config(repo_path, inventory)
        
        # Create generator in onboarding mode
        generator = ProjectGenerator(
            config,
            repo_path,
            onboarding_mode=True,
            dry_run=dry_run,
            conflict_resolver=_interactive_conflict_resolver if not dry_run else None
        )
        
        result = generator.generate()
        
        print("\n" + "=" * 60)
        if result['success']:
            print("[SUCCESS] Onboarding completed!")
            print(f"   Scenario: {result.get('scenario', 'unknown')}")
            print(f"   Files created/modified: {len(result['files_created'])}")
            print(f"   Skipped: {len(result.get('skipped', []))}")
            print(f"   Merged: {len(result.get('merged', []))}")
            
            if result.get('skipped'):
                print("\n   Skipped artifacts:")
                for item in result['skipped']:
                    print(f"     - {item}")
            
            # Offer knowledge extension analysis
            if not dry_run:
                _offer_knowledge_extension(blueprint_id)
        else:
            print("[ERROR] Onboarding failed:")
            for error in result['errors']:
                print(f"   - {error}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Onboarding failed: {e}")
        sys.exit(1)


def _check_blueprint_knowledge(blueprint_id: str) -> None:
    """Check and warn about missing knowledge for a blueprint.
    
    Args:
        blueprint_id: Blueprint identifier
    """
    try:
        blueprint_path = get_factory_root() / 'blueprints' / blueprint_id / 'blueprint.json'
        knowledge_dir = get_factory_root() / 'knowledge'
        
        if not blueprint_path.exists():
            return
        
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint = json.load(f)
        
        knowledge_files = blueprint.get('knowledge', [])
        missing = [k['filename'] for k in knowledge_files 
                   if not (knowledge_dir / k['filename']).exists()]
        
        if missing:
            print("   [!] Knowledge files missing for this blueprint:")
            for mf in missing[:3]:
                print(f"       - {mf}")
            if len(missing) > 3:
                print(f"       ... and {len(missing) - 3} more")
            print("       Run --coverage-report to see full details")
            print()
    except Exception:
        pass  # Don't block generation for knowledge issues


def _offer_knowledge_extension(blueprint_id: str = None) -> None:
    """Offer knowledge extension after onboarding.
    
    Args:
        blueprint_id: Blueprint used for onboarding (if any)
    """
    print("\n" + "-" * 60)
    print("  Knowledge Extension Available")
    print("-" * 60)
    
    try:
        from scripts.analysis.knowledge_gap_analyzer import KnowledgeGapAnalyzer
        
        factory_root = get_factory_root()
        analyzer = KnowledgeGapAnalyzer(
            factory_root / 'knowledge',
            factory_root / 'scripts' / 'taxonomy'
        )
        result = analyzer.analyze("agent_taxonomy.json")
        
        print("\n  Factory Knowledge Status:")
        print(f"    Coverage: {result.coverage_percentage:.1f}%")
        print(f"    Topics covered: {result.covered_topics}/{result.total_topics}")
        
        # Show top gaps
        top_gaps = result.get_top_gaps(3)
        if top_gaps:
            print("\n  Top knowledge gaps:")
            for gap in top_gaps:
                print(f"    - {gap.topic.name} ({gap.priority.name})")
        
        print("\n  Would you like to extend the knowledge base?")
        print("    1. Analyze all gaps")
        print("    2. Extend a specific topic")
        print("    3. Skip for now")
        
        choice = input("\n  Enter choice [3]: ").strip()
        
        if choice == '1':
            print()
            analyze_knowledge_gaps()
        elif choice == '2':
            topic = input("  Enter topic name: ").strip()
            if topic:
                print()
                extend_knowledge_topic(topic)
        else:
            print("\n  Tip: Run 'factory_cli.py --analyze-gaps' anytime to check knowledge status.")
    
    except Exception as e:
        # Don't fail onboarding if knowledge extension has issues
        print(f"\n  [Note] Knowledge extension unavailable: {e}")
        print("  You can run --analyze-gaps later to check knowledge status.")


def _create_default_config(repo_path: str, inventory) -> ProjectConfig:
    """Create default configuration based on inventory.
    
    Args:
        repo_path: Path to repository.
        inventory: Repository inventory.
        
    Returns:
        ProjectConfig with sensible defaults.
    """
    return ProjectConfig(
        project_name=Path(repo_path).name,
        project_description=f"Cursor agent system for {Path(repo_path).name}",
        domain="general",
        primary_language=inventory.tech_stack.languages[0] if inventory.tech_stack.languages else "python",
        frameworks=inventory.tech_stack.frameworks,
        triggers=['jira', 'confluence'],
        agents=['code-reviewer', 'test-generator', 'explorer'],
        skills=['bugfix-workflow', 'feature-workflow', 'grounding', 'tdd'],
        mcp_servers=[],
        blueprint_id=None
    )


def _interactive_conflict_resolver(prompt):
    """Interactively resolve a conflict with user input.
    
    Args:
        prompt: ConflictPrompt to display.
        
    Returns:
        ConflictResolution: User's chosen resolution.
    """
    from scripts.git.merge_strategy import ConflictResolution  # noqa: F401
    
    print("\n" + prompt.format_prompt())
    
    while True:
        try:
            choice = input("\nEnter choice [1-{}] (or Enter for recommended): ".format(
                len(prompt.options)
            )).strip()
            
            if not choice:
                return prompt.recommendation
            
            idx = int(choice) - 1
            if 0 <= idx < len(prompt.options):
                return prompt.options[idx]
            
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nUsing recommended option.")
            return prompt.recommendation


def rollback_session(repo_path: str, session_id: str = None) -> None:
    """Rollback an onboarding session.
    
    Args:
        repo_path: Path to repository.
        session_id: Optional session ID. If not provided, lists available sessions.
    """
    from scripts.git.backup_manager import BackupManager
    
    manager = BackupManager(repo_path)
    
    if not session_id:
        # List available sessions
        sessions = manager.list_sessions()
        
        if not sessions:
            print("No backup sessions found.")
            return
        
        print(f"\n[*] Available backup sessions for: {repo_path}\n")
        for i, session in enumerate(sessions, 1):
            status = "rolled back" if session.rolled_back else (
                "completed" if session.completed else "incomplete"
            )
            print(f"  [{i}] {session.session_id}")
            print(f"      Created: {session.created_at}")
            print(f"      Status: {status}")
            print(f"      Files: {len(session.entries)}")
            if session.description:
                print(f"      Description: {session.description}")
            print()
        
        try:
            choice = input("Enter session number to rollback (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return
            
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                session_id = sessions[idx].session_id
            else:
                print("Invalid choice.")
                return
        except (ValueError, KeyboardInterrupt):
            return
    
    # Confirm rollback
    confirm = input(f"\nRollback session {session_id}? This will restore original files. [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Perform rollback
    if manager.rollback_session(session_id):
        print(f"\n[SUCCESS] Session {session_id} rolled back successfully.")
    else:
        print(f"\n[ERROR] Failed to rollback session {session_id}.")
        sys.exit(1)


# =============================================================================
# KNOWLEDGE EXTENSION COMMANDS
# =============================================================================

def analyze_knowledge_gaps(
    scope: str = 'all',
    filter_value: str = None
) -> None:
    """Analyze knowledge gaps in the Factory.
    
    Args:
        scope: Analysis scope (all, blueprint, domain, topic)
        filter_value: Filter value for the scope
    """
    from scripts.analysis.knowledge_gap_analyzer import KnowledgeGapAnalyzer, GapPriority
    
    print()
    print("=" * 60)
    print("  Knowledge Gap Analysis")
    print("=" * 60)
    print()
    
    factory_root = get_factory_root()
    analyzer = KnowledgeGapAnalyzer(
        factory_root / 'knowledge',
        factory_root / 'scripts' / 'taxonomy'
    )
    
    try:
        print(f"Analyzing gaps (scope: {scope})")
        result = analyzer.analyze("agent_taxonomy.json")
        
        # Apply scope filtering
        if scope == 'topic' and filter_value:
            result.gaps = [g for g in result.gaps if filter_value.lower() in g.topic.name.lower()]
        elif scope == 'domain' and filter_value:
            result.gaps = [g for g in result.gaps if filter_value.lower() in g.coverage.topic_path.lower()]
        
        print()
        print(f"Total Topics: {result.total_topics}")
        print(f"Covered: {result.covered_topics}")
        print(f"Coverage: {result.coverage_percentage:.1f}%")
        print()
        
        if not result.gaps:
            print("[OK] No gaps found!")
            return
        
        print(f"Found {len(result.gaps)} gaps:")
        print()
        
        # Group by priority
        for priority in GapPriority:
            gaps = result.gaps_by_priority.get(priority, [])
            if gaps:
                print(f"  {priority.name} ({len(gaps)}):")
                for gap in gaps[:5]:  # Show first 5 per priority
                    print(f"    - {gap.topic.name}: {gap.description}")
                if len(gaps) > 5:
                    print(f"    ... and {len(gaps) - 5} more")
                print()
        
        # Show suggestions
        print("To extend a topic:")
        print("  python cli/factory_cli.py --extend-knowledge <topic_name>")
        print("  Or ask: 'Follow extend-knowledge skill for <topic_name>'")
        print()
        
    except Exception as e:
        print(f"[ERROR] Gap analysis failed: {e}")
        sys.exit(1)


def show_coverage_report(blueprint_id: str) -> None:
    """Show knowledge coverage report for a blueprint.
    
    Args:
        blueprint_id: Blueprint identifier
    """
    factory_root = get_factory_root()
    blueprint_path = factory_root / 'blueprints' / blueprint_id / 'blueprint.json'
    knowledge_dir = factory_root / 'knowledge'
    
    print()
    print("=" * 60)
    print(f"  Knowledge Coverage: {blueprint_id}")
    print("=" * 60)
    print()
    
    try:
        if not blueprint_path.exists():
            print(f"[ERROR] Blueprint not found: {blueprint_id}")
            sys.exit(1)
        
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint = json.load(f)
        
        knowledge_refs = blueprint.get('knowledge', [])
        
        print(f"Blueprint: {blueprint_id}")
        print(f"Knowledge Files: {len(knowledge_refs)}")
        
        # Check each file
        existing = 0
        missing_files = []
        
        print()
        print("File Status:")
        for k in knowledge_refs:
            filename = k['filename']
            file_path = knowledge_dir / filename
            
            if file_path.exists():
                existing += 1
                # Try to get version
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    version = data.get('version', '')
                except Exception:
                    version = ''
                print(f"  [OK] {filename} {version}")
            else:
                missing_files.append(filename)
                print(f"  [MISSING] {filename}")
        
        coverage = (existing / len(knowledge_refs) * 100) if knowledge_refs else 100.0
        print()
        print(f"Coverage Score: {coverage:.1f}%")
        
        if missing_files:
            print()
            print("To create missing files:")
            for mf in missing_files:
                topic = mf.replace('-patterns.json', '').replace('.json', '').replace('-', '_')
                print(f"  'Follow extend-knowledge skill for {topic}'")
        
        print()
        
    except Exception as e:
        print(f"[ERROR] Coverage report failed: {e}")
        sys.exit(1)


def suggest_extensions(blueprint_id: str) -> None:
    """Suggest knowledge extensions for a blueprint.
    
    Args:
        blueprint_id: Blueprint identifier
    """
    factory_root = get_factory_root()
    blueprint_path = factory_root / 'blueprints' / blueprint_id / 'blueprint.json'
    knowledge_dir = factory_root / 'knowledge'
    
    print()
    print("=" * 60)
    print(f"  Extension Suggestions: {blueprint_id}")
    print("=" * 60)
    print()
    
    try:
        if not blueprint_path.exists():
            print(f"[ERROR] Blueprint not found: {blueprint_id}")
            sys.exit(1)
        
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint = json.load(f)
        
        # Get current knowledge refs
        current_refs = set(k['filename'] for k in blueprint.get('knowledge', []))
        
        # Get all available knowledge files
        available = set(f.name for f in knowledge_dir.glob('*.json'))
        
        # Get blueprint tags for relevance matching
        tags = set(t.lower() for t in blueprint.get('metadata', {}).get('tags', []))
        
        # Find relevant files not yet in blueprint
        suggestions = []
        for filename in available - current_refs:
            # Skip manifest and schemas
            if filename in ('manifest.json',) or filename.startswith('schema'):
                continue
            # Check if file seems relevant to blueprint tags
            name_parts = set(filename.replace('.json', '').replace('-', ' ').split())
            if name_parts & tags or 'patterns' in filename:
                suggestions.append(filename)
        
        if not suggestions:
            print("[OK] No additional knowledge files suggested.")
            print("     Blueprint knowledge appears comprehensive.")
            return
        
        print(f"Found {len(suggestions)} knowledge files that could enhance this blueprint:")
        print()
        
        for i, filename in enumerate(sorted(suggestions)[:15], 1):
            print(f"  {i}. {filename}")
        
        if len(suggestions) > 15:
            print(f"  ... and {len(suggestions) - 15} more")
        
        print()
        print("To add these to the blueprint, edit:")
        print(f"  blueprints/{blueprint_id}/blueprint.json")
        print()
        
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Suggestion failed: {e}")
        sys.exit(1)


def extend_knowledge_topic(
    topic_name: str,
    auto_apply: bool = False,
    use_mock_llm: bool = False
) -> None:
    """Show extension instructions using Factory artifacts.
    
    Uses artifacts:
    - Template: templates/knowledge/knowledge-file.tmpl
    - Pattern: patterns/knowledge/knowledge-schema.json
    - Skill: .agent/skills/extend-knowledge/SKILL.md    
    Args:
        topic_name: Topic to extend
        auto_apply: Not used
        use_mock_llm: Not used
    """
    from scripts.analysis.knowledge_gap_analyzer import KnowledgeGapAnalyzer
    
    print()
    print("=" * 60)
    print(f"  Knowledge Extension: {topic_name}")
    print("=" * 60)
    print()
    
    factory_root = Path(__file__).parent.parent
    knowledge_dir = factory_root / "knowledge"
    taxonomy_dir = factory_root / "scripts" / "taxonomy"
    
    # Check if topic has a gap
    try:
        analyzer = KnowledgeGapAnalyzer(knowledge_dir, taxonomy_dir)
        result = analyzer.analyze("agent_taxonomy.json")
        
        gap = None
        for g in result.gaps:
            if g.topic.name.lower() == topic_name.lower():
                gap = g
                break
        
        if not gap:
            print(f"[INFO] Topic '{topic_name}' is not in gaps list.")
            print("       It may already be covered or not in taxonomy.")
            print()
            print("  Run: python cli/factory_cli.py --analyze-gaps")
            print()
            return
        
        # Show gap info
        target_file = f"{topic_name.lower().replace('_', '-')}-patterns.json"
        
        print(f"  Gap Type: {gap.gap_type.name}")
        print(f"  Priority: {gap.priority.name}")
        print(f"  Required Depth: {gap.coverage.required_depth}")
        print(f"  Target File: knowledge/{target_file}")
        print()
        
        # Show artifacts to use
        print("-" * 60)
        print("  ARTIFACTS TO USE")
        print("-" * 60)
        print()
        print("  1. TEMPLATE: templates/knowledge/knowledge-file.tmpl")
        print("     Read this for the JSON structure")
        print()
        print("  2. PATTERN: patterns/knowledge/knowledge-schema.json")
        print("     Read this for validation rules (min 3 patterns, etc.)")
        print()
        print("  3. SKILL: .agent/skills/extend-knowledge/SKILL.md")
        print("     Follow this step-by-step process")
        print()
        
        # Show instructions
        print("-" * 60)
        print("  INSTRUCTIONS")
        print("-" * 60)
        print()
        print(f"  1. Research: {topic_name.replace('_', ' ')}")
        print("  2. Read template: templates/knowledge/knowledge-file.tmpl")
        print(f"  3. Create file: knowledge/{target_file}")
        print(f"  4. Include at least {max(3, gap.coverage.required_depth)} patterns")
        print("  5. Add code examples and sources")
        print("  6. Validate JSON structure")
        print()
        print("  Ask: 'Follow extend-knowledge skill for " + topic_name + "'")
        print()
        
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


# =============================================================================
# DEPENDENCY VALIDATION COMMANDS
# =============================================================================

def validate_dependencies() -> int:
    """Validate the Factory dependency graph.
    
    Returns:
        Exit code (0 = valid, 1 = errors found)
    """
    from scripts.validation.dependency_validator import DependencyValidator
    
    print()
    print("=" * 60)
    print("  Factory Dependency Graph Validation")
    print("=" * 60)
    print()
    
    factory_root = Path(__file__).parent.parent
    validator = DependencyValidator(factory_root)
    validator.scan_artifacts()
    
    result = validator.validate()
    
    if result.cycles:
        print("[ERROR] Circular dependencies detected:")
        for cycle in result.cycles:
            print(f"  {' -> '.join(cycle)}")
        print()
    
    if result.broken_refs:
        print("[ERROR] Broken references (hard dependencies):")
        for ref in result.broken_refs:
            print(f"  - {ref}")
        print()
    
    if result.version_errors:
        print("[WARNING] Version constraint violations:")
        for err in result.version_errors:
            print(f"  - {err}")
        print()
    
    if result.is_valid:
        stats = validator.get_statistics()
        print("[OK] Dependency graph is valid")
        print(f"     Nodes: {stats['total_nodes']}")
        print(f"     Edges: {stats['total_edges']}")
        print()
        return 0
    else:
        return 1


def show_dependents(node_id: str) -> None:
    """Show what depends on a given node.
    
    Args:
        node_id: Node identifier (e.g., knowledge:fastapi-patterns.json)
    """
    from scripts.validation.dependency_validator import DependencyValidator
    
    print()
    print("=" * 60)
    print(f"  Dependents of: {node_id}")
    print("=" * 60)
    print()
    
    factory_root = Path(__file__).parent.parent
    validator = DependencyValidator(factory_root)
    validator.scan_artifacts()
    
    dependents = validator.reverse_lookup(node_id)
    
    if dependents:
        print(f"Direct dependents ({len(dependents)}):")
        for dep in sorted(dependents):
            print(f"  - {dep}")
    else:
        print("No nodes directly depend on this artifact.")
    print()


def show_impact_analysis(node_id: str) -> None:
    """Show impact analysis for a node (all transitively affected).
    
    Args:
        node_id: Node identifier (e.g., skill:grounding)
    """
    from scripts.validation.dependency_validator import DependencyValidator
    
    print()
    print("=" * 60)
    print(f"  Impact Analysis: {node_id}")
    print("=" * 60)
    print()
    
    factory_root = Path(__file__).parent.parent
    validator = DependencyValidator(factory_root)
    validator.scan_artifacts()
    
    affected = validator.impact_analysis(node_id)
    
    if affected:
        print(f"Changes to {node_id} would affect {len(affected)} artifacts:")
        print()
        
        # Group by type
        by_type = {}
        for node in affected:
            node_type = node.split(":")[0] if ":" in node else "unknown"
            if node_type not in by_type:
                by_type[node_type] = []
            by_type[node_type].append(node)
        
        for node_type, nodes in sorted(by_type.items()):
            print(f"  {node_type.upper()} ({len(nodes)}):")
            for node in sorted(nodes):
                print(f"    - {node}")
            print()
    else:
        print("No nodes would be affected by changes to this artifact.")
    print()


def show_dependency_order() -> None:
    """Show topological installation order for all artifacts."""
    from scripts.validation.dependency_validator import DependencyValidator
    from graphlib import CycleError
    
    print()
    print("=" * 60)
    print("  Dependency Installation Order")
    print("=" * 60)
    print()
    
    factory_root = Path(__file__).parent.parent
    validator = DependencyValidator(factory_root)
    validator.scan_artifacts()
    
    try:
        order = validator.get_install_order()
        print(f"Install order ({len(order)} artifacts):")
        print()
        for i, node in enumerate(order, 1):
            print(f"  {i:3}. {node}")
        print()
    except CycleError as e:
        print(f"[ERROR] Cannot determine order: {e}")
        print("        Fix circular dependencies first.")
        print()


def show_dependency_stats() -> None:
    """Show dependency graph statistics."""
    from scripts.validation.dependency_validator import DependencyValidator
    
    print()
    print("=" * 60)
    print("  Dependency Graph Statistics")
    print("=" * 60)
    print()
    
    factory_root = Path(__file__).parent.parent
    validator = DependencyValidator(factory_root)
    validator.scan_artifacts()
    
    stats = validator.get_statistics()
    
    print(f"  Total Nodes: {stats['total_nodes']}")
    print(f"  Total Edges: {stats['total_edges']}")
    print()
    
    print("  Nodes by Type:")
    for node_type, count in sorted(stats['nodes_by_type'].items()):
        print(f"    {node_type}: {count}")
    print()
    
    print("  Edges by Type:")
    for edge_type, count in sorted(stats['edges_by_type'].items()):
        print(f"    {edge_type}: {count}")
    print()


def export_dependency_graph(output_file: str) -> None:
    """Export dependency graph to JSON file.
    
    Args:
        output_file: Path to output JSON file
    """
    from scripts.validation.dependency_validator import DependencyValidator
    
    factory_root = Path(__file__).parent.parent
    validator = DependencyValidator(factory_root)
    validator.scan_artifacts()
    
    graph = validator.export_graph()
    
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)
    
    print(f"[OK] Exported dependency graph to {output_path}")
    print(f"     Nodes: {len(graph['nodes'])}")
    print(f"     Edges: {len(graph['edges'])}")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Antigravity Agent Factory - Generate Antigravity agent development systems',        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Quick Start - See it work in 5 minutes!
  %(prog)s --quickstart
  %(prog)s --quickstart --quickstart-output C:\\Projects\\my-demo
  %(prog)s --quickstart --quickstart-blueprint nextjs-fullstack
  
  # List available options
  %(prog)s --list-blueprints
  %(prog)s --list-patterns
  
  # Generate new project from scratch
  %(prog)s --blueprint python-fastapi --output C:\\Projects\\my-api
  %(prog)s --config project.yaml --output C:\\Projects\\my-project
  %(prog)s --interactive --output C:\\Projects\\my-project
  
  # Generate with Project Management System
  %(prog)s --blueprint python-fastapi --output C:\\Projects\\my-api --pm-enabled --pm-backend github --pm-methodology scrum
  %(prog)s --blueprint java-spring --output C:\\Projects\\my-api --pm-enabled --pm-backend jira --pm-doc-backend confluence
  
  # Onboard existing repository
  %(prog)s --analyze C:\\Projects\\existing-repo
  %(prog)s --onboard C:\\Projects\\existing-repo
  %(prog)s --onboard C:\\Projects\\existing-repo --blueprint csharp-dotnet
  %(prog)s --onboard C:\\Projects\\existing-repo --pm-enabled --pm-backend azure-devops
  %(prog)s --onboard C:\\Projects\\existing-repo --dry-run
  %(prog)s --rollback C:\\Projects\\existing-repo
  
  # Dependency Validation
  %(prog)s --validate-deps                                    # Full validation
  %(prog)s --dependents knowledge:fastapi-patterns.json       # Who depends on this?
  %(prog)s --impact skill:grounding                           # Impact analysis
  %(prog)s --dep-order                                        # Installation order
  %(prog)s --dep-stats                                        # Graph statistics
  %(prog)s --export-deps deps.json                            # Export to JSON
  
  # Knowledge Extension (uses Factory artifacts)
  %(prog)s --analyze-gaps                                    # Analyze all gaps
  %(prog)s --analyze-gaps --gap-scope blueprint --gap-filter ai-agent-development
  %(prog)s --coverage-report ai-agent-development            # Blueprint coverage
  %(prog)s --suggest-extensions ai-agent-development         # Suggest additions
  %(prog)s --extend-knowledge constitutional_ai              # Show extension instructions
        '''
    )
    
    parser.add_argument(
        '--list-blueprints',
        action='store_true',
        help='List all available blueprints'
    )
    
    parser.add_argument(
        '--list-patterns',
        action='store_true',
        help='List all available patterns'
    )
    
    parser.add_argument(
        '--blueprint',
        type=str,
        metavar='ID',
        help='Generate from a blueprint (e.g., python-fastapi)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        metavar='FILE',
        help='Generate from a configuration file (YAML or JSON)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run interactive requirements gathering'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        metavar='DIR',
        help='Output directory for generated project'
    )
    
    parser.add_argument(
        '--name',
        type=str,
        metavar='NAME',
        help='Project name (overrides blueprint/config name)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Antigravity Agent Factory 2.0.0'    )
    
    # Onboarding commands
    parser.add_argument(
        '--analyze',
        type=str,
        metavar='REPO',
        help='Analyze existing repository for Cursor artifacts'
    )
    
    parser.add_argument(
        '--onboard',
        type=str,
        metavar='REPO',
        help='Onboard existing repository (non-destructive integration)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview onboarding changes without making them'
    )
    
    parser.add_argument(
        '--rollback',
        type=str,
        metavar='REPO',
        help='Rollback an onboarding session'
    )
    
    parser.add_argument(
        '--session-id',
        type=str,
        metavar='ID',
        help='Specific backup session ID for rollback'
    )
    
    # Quick start commands
    parser.add_argument(
        '--quickstart',
        action='store_true',
        help='Generate a demo project instantly with zero configuration'
    )
    
    parser.add_argument(
        '--quickstart-blueprint',
        type=str,
        metavar='ID',
        help='Blueprint to use for quickstart (default: python-fastapi)'
    )
    
    parser.add_argument(
        '--quickstart-output',
        type=str,
        metavar='DIR',
        help='Output directory for quickstart (default: ./quickstart-demo)'
    )
    
    # Project Management System commands
    parser.add_argument(
        '--pm-enabled',
        action='store_true',
        help='Enable project management system (adds PM agents, skills, and MCP configs)'
    )
    
    parser.add_argument(
        '--pm-backend',
        type=str,
        choices=['github', 'jira', 'azure-devops', 'linear'],
        metavar='BACKEND',
        help='PM backend: github, jira, azure-devops, or linear'
    )
    
    parser.add_argument(
        '--pm-doc-backend',
        type=str,
        choices=['github-wiki', 'confluence', 'azure-wiki', 'none'],
        metavar='DOC_BACKEND',
        help='Documentation backend: github-wiki, confluence, azure-wiki, or none'
    )
    
    parser.add_argument(
        '--pm-methodology',
        type=str,
        choices=['scrum', 'kanban', 'hybrid', 'waterfall'],
        metavar='METHODOLOGY',
        help='PM methodology: scrum, kanban, hybrid, or waterfall'
    )
    
    # Dependency Validation commands
    parser.add_argument(
        '--validate-deps',
        action='store_true',
        help='Validate the Factory dependency graph (cycles, broken refs)'
    )
    
    parser.add_argument(
        '--dependents',
        type=str,
        metavar='NODE',
        help='Show what depends on a node (e.g., knowledge:fastapi-patterns.json)'
    )
    
    parser.add_argument(
        '--impact',
        type=str,
        metavar='NODE',
        help='Show impact analysis for a node (all transitively affected)'
    )
    
    parser.add_argument(
        '--dep-order',
        action='store_true',
        help='Show topological installation order for all artifacts'
    )
    
    parser.add_argument(
        '--dep-stats',
        action='store_true',
        help='Show dependency graph statistics'
    )
    
    parser.add_argument(
        '--export-deps',
        type=str,
        metavar='FILE',
        help='Export dependency graph to JSON file'
    )
    
    # Knowledge Extension commands
    parser.add_argument(
        '--analyze-gaps',
        action='store_true',
        help='Analyze knowledge gaps in the Factory knowledge base'
    )
    
    parser.add_argument(
        '--gap-scope',
        type=str,
        choices=['all', 'blueprint', 'domain', 'topic'],
        default='all',
        metavar='SCOPE',
        help='Scope for gap analysis: all, blueprint, domain, or topic'
    )
    
    parser.add_argument(
        '--gap-filter',
        type=str,
        metavar='VALUE',
        help='Filter value for gap analysis (blueprint ID, domain name, or topic name)'
    )
    
    parser.add_argument(
        '--extend-knowledge',
        type=str,
        metavar='TOPIC',
        help='Show extension instructions for a topic (uses Factory artifacts)'
    )
    
    parser.add_argument(
        '--coverage-report',
        type=str,
        metavar='BLUEPRINT',
        help='Show knowledge coverage report for a blueprint'
    )
    
    parser.add_argument(
        '--suggest-extensions',
        type=str,
        metavar='BLUEPRINT',
        help='Suggest knowledge extensions for a blueprint'
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_blueprints:
        list_blueprints()
        return
    
    if args.list_patterns:
        list_patterns()
        return
    
    # Handle onboarding commands
    if args.analyze:
        analyze_repository(args.analyze)
        return
    
    if args.onboard:
        onboard_repository(
            args.onboard, 
            args.blueprint, 
            args.dry_run,
            pm_enabled=args.pm_enabled,
            pm_backend=args.pm_backend,
            pm_doc_backend=args.pm_doc_backend,
            pm_methodology=args.pm_methodology
        )
        return
    
    if args.rollback:
        rollback_session(args.rollback, args.session_id)
        return
    
    # Handle dependency validation commands
    if args.validate_deps:
        exit_code = validate_dependencies()
        sys.exit(exit_code)
    
    if args.dependents:
        show_dependents(args.dependents)
        return
    
    if args.impact:
        show_impact_analysis(args.impact)
        return
    
    if args.dep_order:
        show_dependency_order()
        return
    
    if args.dep_stats:
        show_dependency_stats()
        return
    
    if args.export_deps:
        export_dependency_graph(args.export_deps)
        return
    
    # Handle knowledge extension commands
    if args.analyze_gaps:
        analyze_knowledge_gaps(
            scope=args.gap_scope,
            filter_value=args.gap_filter
        )
        return
    
    if args.coverage_report:
        show_coverage_report(args.coverage_report)
        return
    
    if args.suggest_extensions:
        suggest_extensions(args.suggest_extensions)
        return
    
    if args.extend_knowledge:
        extend_knowledge_topic(args.extend_knowledge)
        return
    
    # Handle quickstart command
    if args.quickstart:
        run_quickstart(
            output_dir=args.quickstart_output or args.output,
            blueprint_id=args.quickstart_blueprint
        )
        return
    
    # Validate output directory for generation commands
    if args.blueprint or args.config or args.interactive:
        if not args.output:
            print("[ERROR] --output is required for generation")
            parser.print_help()
            sys.exit(1)
    
    # Handle generation commands
    if args.interactive:
        interactive_mode(args.output)
    elif args.blueprint:
        generate_from_blueprint(
            args.blueprint, 
            args.output, 
            args.name,
            pm_enabled=args.pm_enabled,
            pm_backend=args.pm_backend,
            pm_doc_backend=args.pm_doc_backend,
            pm_methodology=args.pm_methodology
        )
    elif args.config:
        generate_from_config_file(args.config, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
