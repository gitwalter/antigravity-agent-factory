#!/usr/bin/env python3
"""
Blueprint Version Updater

This script automatically updates software and LLM versions in blueprint.json files
to their latest stable versions by querying package registries and official sources.

Usage:
    python scripts/update_blueprint_versions.py [--dry-run] [--blueprint BLUEPRINT_ID]
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VersionUpdater:
    """Handles version checking and updates for blueprints."""
    
    def __init__(self, dry_run: bool = False):
        """Initialize the version updater.
        
        Args:
            dry_run: If True, only show what would be updated without making changes
        """
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Antigravity-Blueprint-Updater/1.0'})
        
    def get_pypi_latest_version(self, package_name: str) -> Optional[str]:
        """Get the latest version of a Python package from PyPI.
        
        Args:
            package_name: Name of the package on PyPI
            
        Returns:
            Latest version string or None if not found
        """
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data['info']['version']
        except Exception as e:
            logger.warning(f"Could not fetch version for {package_name}: {e}")
            return None
    
    def get_npm_latest_version(self, package_name: str) -> Optional[str]:
        """Get the latest version of an npm package.
        
        Args:
            package_name: Name of the package on npm
            
        Returns:
            Latest version string or None if not found
        """
        try:
            url = f"https://registry.npmjs.org/{package_name}/latest"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data['version']
        except Exception as e:
            logger.warning(f"Could not fetch version for {package_name}: {e}")
            return None
    
    def get_latest_versions(self) -> Dict[str, str]:
        """Get latest versions for all tracked frameworks and tools.
        
        Returns:
            Dictionary mapping package names to their latest versions
        """
        versions = {}
        
        # Python packages
        python_packages = {
            'langchain': 'langchain',
            'langgraph': 'langgraph',
            'crewai': 'crewai',
            'pyautogen': 'autogen',
            'streamlit': 'streamlit',
            'fastapi': 'fastapi',
            'pydantic': 'pydantic',
            'chromadb': 'chromadb',
            'faiss-cpu': 'faiss',
            'pytest': 'pytest',
            'ruff': 'ruff',
            'mypy': 'mypy',
            'poetry': 'poetry',
            'torch': 'pytorch',
            'tensorflow': 'tensorflow',
            'transformers': 'transformers',
            'openai': 'openai',
            'anthropic': 'anthropic',
            'google-generativeai': 'google-ai',
            'langsmith': 'langsmith',
            'pinecone-client': 'pinecone',
            'qdrant-client': 'qdrant',
            'weaviate-client': 'weaviate',
        }
        
        for package_key, package_name in python_packages.items():
            logger.info(f"Fetching version for {package_name}...")
            version = self.get_pypi_latest_version(package_name)
            if version:
                versions[package_key] = version
                logger.info(f"  ✓ {package_name}: {version}")
        
        # npm packages (for n8n, MCP servers, etc.)
        npm_packages = {
            'n8n': 'n8n',
            '@modelcontextprotocol/sdk': 'mcp-sdk',
            'typescript': 'typescript',
            'next': 'nextjs',
            'react': 'react',
            'vite': 'vite',
        }
        
        for package_key, package_name in npm_packages.items():
            logger.info(f"Fetching version for {package_name}...")
            version = self.get_npm_latest_version(package_key)
            if version:
                versions[package_name] = version
                logger.info(f"  ✓ {package_name}: {version}")
        
        # Database versions (manually curated - check official sources)
        versions['databases'] = {
            'postgresql': '17.2',  # Latest stable as of Feb 2026
            'mongodb': '8.0',
            'redis': '7.4',
            'sqlite': '3.47.0',
            'mysql': '9.1',
            'chromadb': versions.get('chromadb', '1.4.1'),
            'pinecone': 'cloud-managed',
            'qdrant': versions.get('qdrant-client', '1.12.0'),
            'weaviate': versions.get('weaviate-client', '4.9.0'),
        }
        
        # Development tools (manually curated)
        versions['dev_tools'] = {
            'docker': '27.4.0',
            'docker-compose': '2.32.0',
            'git': '2.48.0',
            'node': '22.12.0',  # LTS
            'python': '3.13.1',
            'go': '1.24.0',
            'rust': '1.84.0',
            'java': '23',
            'dotnet': '9.0',
        }
        
        # Cloud platforms & services
        versions['cloud_services'] = {
            'aws-cli': '2.22.0',
            'azure-cli': '2.67.0',
            'gcloud': '507.0.0',
            'terraform': '1.10.0',
            'kubernetes': '1.32.0',
        }
        
        # LLM models (manually curated as of Feb 2026)
        versions['llm_models'] = {
            'openai': {
                'gpt-5.2': 'Latest GPT-5 series (Dec 2025)',
                'gpt-5.3-codex': 'Latest coding model (Feb 2026)',
                'gpt-4o': 'GPT-4 Optimized',
                'gpt-4o-mini': 'GPT-4 Optimized Mini',
                'o1': 'OpenAI o1 reasoning',
                'o1-mini': 'OpenAI o1 mini'
            },
            'anthropic': {
                'claude-opus-4.6': 'Latest Opus (Feb 2026)',
                'claude-3-5-sonnet-20241022': 'Claude 3.5 Sonnet',
                'claude-3-5-haiku-20241022': 'Claude 3.5 Haiku'
            },
            'google': {
                'gemini-3-pro': 'Gemini 3 Pro (Feb 2026)',
                'gemini-3-flash': 'Gemini 3 Flash (Feb 2026)',
                'gemini-2.5-flash': 'Gemini 2.5 Flash',
                'gemini-2.0-flash-exp': 'Gemini 2.0 Flash Experimental'
            },
            'ollama': {
                'llama3.3': 'Llama 3.3',
                'llama3.2': 'Llama 3.2',
                'qwen2.5': 'Qwen 2.5',
                'mistral': 'Mistral',
                'codellama': 'Code Llama'
            }
        }
        
        return versions
    
    def update_framework_versions(self, blueprint: Dict, versions: Dict[str, str]) -> Tuple[Dict, List[str]]:
        """Update framework versions in a blueprint.
        
        Args:
            blueprint: Blueprint dictionary
            versions: Dictionary of latest versions
            
        Returns:
            Tuple of (updated blueprint, list of changes made)
        """
        changes = []
        
        if 'stack' not in blueprint or 'frameworks' not in blueprint['stack']:
            return blueprint, changes
        
        framework_mapping = {
            'LangChain': 'langchain',
            'LangGraph': 'langgraph',
            'CrewAI': 'crewai',
            'AutoGen': 'pyautogen',
            'Streamlit': 'streamlit',
            'FastAPI': 'fastapi',
            'Pydantic': 'pydantic',
        }
        
        for framework in blueprint['stack']['frameworks']:
            framework_name = framework.get('name')
            if framework_name in framework_mapping:
                package_key = framework_mapping[framework_name]
                if package_key in versions:
                    old_version = framework.get('version', 'unknown')
                    new_version = versions[package_key]
                    
                    # Extract major.minor for comparison
                    new_major_minor = '.'.join(new_version.split('.')[:2])
                    framework['version'] = f"{new_major_minor}+"
                    
                    if old_version != framework['version']:
                        changes.append(
                            f"  {framework_name}: {old_version} → {framework['version']} (latest: {new_version})"
                        )
        
        return blueprint, changes
    
    def update_llm_models(self, blueprint: Dict, versions: Dict) -> Tuple[Dict, List[str]]:
        """Update LLM model lists in a blueprint.
        
        Args:
            blueprint: Blueprint dictionary
            versions: Dictionary of latest versions including LLM models
            
        Returns:
            Tuple of (updated blueprint, list of changes made)
        """
        changes = []
        
        if 'stack' not in blueprint or 'llmProviders' not in blueprint['stack']:
            return blueprint, changes
        
        llm_models = versions.get('llm_models', {})
        
        for provider in blueprint['stack']['llmProviders']:
            provider_name_lower = provider.get('name', '').lower()
            
            if provider_name_lower in llm_models:
                old_models = set(provider.get('models', []))
                new_models = list(llm_models[provider_name_lower].keys())
                
                # Keep existing models that are still valid, add new ones
                updated_models = []
                for model in new_models:
                    if model not in old_models:
                        changes.append(f"  {provider['name']}: Added model {model}")
                    updated_models.append(model)
                
                # Note removed models
                for model in old_models:
                    if model not in new_models:
                        changes.append(f"  {provider['name']}: Removed outdated model {model}")
                
                provider['models'] = updated_models
        
        return blueprint, changes
    
    def update_knowledge_files(self, knowledge_dir: Path, versions: Dict[str, str]) -> int:
        """Update library versions in knowledge files.
        
        Args:
            knowledge_dir: Path to knowledge directory
            versions: Dictionary of latest versions
            
        Returns:
            Number of knowledge files updated
        """
        if not knowledge_dir.exists():
            logger.warning(f"Knowledge directory not found: {knowledge_dir}")
            return 0
        
        updated_count = 0
        knowledge_files = list(knowledge_dir.glob('*.json'))
        
        for knowledge_file in knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                
                # Check if file has a versions or dependencies section
                updated = False
                
                # Update version references in the content
                if 'versions' in content:
                    for key, value in content['versions'].items():
                        if key in versions:
                            old_version = value
                            new_version = versions[key]
                            if old_version != new_version:
                                content['versions'][key] = new_version
                                logger.info(f"  {knowledge_file.name}: {key} {old_version} → {new_version}")
                                updated = True
                
                # Add metadata about last version check
                if updated:
                    if 'metadata' not in content:
                        content['metadata'] = {}
                    content['metadata']['last_version_update'] = datetime.now().isoformat()
                    
                    if not self.dry_run:
                        with open(knowledge_file, 'w', encoding='utf-8') as f:
                            json.dump(content, f, indent=2, ensure_ascii=False)
                            f.write('\n')
                        updated_count += 1
                        
            except Exception as e:
                logger.warning(f"Could not process {knowledge_file.name}: {e}")
        
        return updated_count
    
    def update_blueprint_file(self, blueprint_path: Path, versions: Dict[str, str]) -> bool:
        """Update a single blueprint file.
        
        Args:
            blueprint_path: Path to blueprint.json file
            versions: Dictionary of latest versions
            
        Returns:
            True if updates were made, False otherwise
        """
        logger.info(f"\nProcessing: {blueprint_path}")
        
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                blueprint = json.load(f)
            
            all_changes = []
            
            # Update frameworks
            blueprint, framework_changes = self.update_framework_versions(blueprint, versions)
            all_changes.extend(framework_changes)
            
            # Update LLM models
            blueprint, llm_changes = self.update_llm_models(blueprint, versions)
            all_changes.extend(llm_changes)
            
            if not all_changes:
                logger.info("  ✓ No updates needed - already up to date")
                return False
            
            logger.info("  Changes to be made:")
            for change in all_changes:
                logger.info(change)
            
            if not self.dry_run:
                # Write updated blueprint
                with open(blueprint_path, 'w', encoding='utf-8') as f:
                    json.dump(blueprint, f, indent=2, ensure_ascii=False)
                    f.write('\n')  # Add trailing newline
                logger.info(f"  ✓ Updated {blueprint_path}")
            else:
                logger.info("  [DRY RUN] Would update file")
            
            return True
            
        except Exception as e:
            logger.error(f"  ✗ Error processing {blueprint_path}: {e}")
            return False
    
    def update_all_blueprints(self, blueprints_dir: Path, blueprint_id: Optional[str] = None) -> None:
        """Update all blueprint files in the blueprints directory.
        
        Args:
            blueprints_dir: Path to blueprints directory
            blueprint_id: Optional specific blueprint ID to update
        """
        logger.info("=" * 80)
        logger.info("Blueprint Version Updater")
        logger.info("=" * 80)
        
        if self.dry_run:
            logger.info("DRY RUN MODE - No files will be modified")
        
        # Get latest versions
        logger.info("\nFetching latest versions...")
        versions = self.get_latest_versions()
        
        # Update knowledge files first
        knowledge_dir = blueprints_dir.parent / 'knowledge'
        if knowledge_dir.exists():
            logger.info(f"\nUpdating knowledge files in {knowledge_dir}...")
            knowledge_updated = self.update_knowledge_files(knowledge_dir, versions)
            if knowledge_updated > 0:
                logger.info(f"✓ Updated {knowledge_updated} knowledge file(s)")
        
        # Find blueprint files
        if blueprint_id:
            blueprint_files = [blueprints_dir / blueprint_id / 'blueprint.json']
            if not blueprint_files[0].exists():
                logger.error(f"Blueprint not found: {blueprint_id}")
                return
        else:
            blueprint_files = list(blueprints_dir.glob('*/blueprint.json'))
        
        if not blueprint_files:
            logger.warning("No blueprint files found")
            return
        
        logger.info(f"\nFound {len(blueprint_files)} blueprint(s) to process")
        
        # Update each blueprint
        updated_count = 0
        for blueprint_path in sorted(blueprint_files):
            if self.update_blueprint_file(blueprint_path, versions):
                updated_count += 1
        
        # Summary
        logger.info("\n" + "=" * 80)
        logger.info(f"Summary: {updated_count}/{len(blueprint_files)} blueprint(s) updated")
        if self.dry_run:
            logger.info("Run without --dry-run to apply changes")
        logger.info("=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Update blueprint versions to latest stable releases'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )
    parser.add_argument(
        '--blueprint',
        type=str,
        help='Specific blueprint ID to update (e.g., ai-agent-development)'
    )
    parser.add_argument(
        '--blueprints-dir',
        type=Path,
        default=Path(__file__).parents[2] / '.agent' / 'blueprints',
        help='Path to blueprints directory'
    )
    
    args = parser.parse_args()
    
    if not args.blueprints_dir.exists():
        logger.error(f"Blueprints directory not found: {args.blueprints_dir}")
        sys.exit(1)
    
    updater = VersionUpdater(dry_run=args.dry_run)
    updater.update_all_blueprints(args.blueprints_dir, args.blueprint)


if __name__ == '__main__':
    main()
