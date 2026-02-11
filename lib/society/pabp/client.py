"""
PABP Client Implementation.

This module provides the client logic for the PABP Bootstrap Protocol,
enabling the installation and update of agent capabilities from
external bundles or repositories.

SDG - Love - Truth - Beauty
"""

import json
import logging
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from lib.society.pabp.adapters import (
    PlatformAdapter,
    AntigravityAdapter,
    detect_platform,
    get_adapter
)
from lib.society.pabp.bundle import AgentBundle, BundleComponent, ComponentType
from lib.society.pabp.renderers import (
    render_agent_markdown,
    render_skill_markdown,
    render_workflow_markdown,
)

logger = logging.getLogger(__name__)

@dataclass
class UpdateResult:
    """Result of an update operation."""
    added: List[str]
    modified: List[str]
    errors: List[str]
    audit_log: Path

class PABPClient:
    """
    Client for PABP operations.
    
    Handles the "pull" process:
    1. Connect to source (repo or bundle)
    2. Discover components
    3. Transform content via adapters
    4. Install to local project
    """
    
    def __init__(self, project_root: Path, target_adapter: Optional[PlatformAdapter] = None):
        self.project_root = project_root
        self.target_adapter = target_adapter or detect_platform(project_root)
        
    def pull_updates(
        self,
        source: Union[str, Path],
        dry_run: bool = False
    ) -> UpdateResult:
        """
        Pull updates from a source.
        
        Args:
            source: URL or local path to source.
            dry_run: If True, do not write changes.
            
        Returns:
            UpdateResult with statistics.
        """
        source_path = Path(source)
        temp_dir = None
        
        # Handle remote URL (simple git clone for now)
        if str(source).startswith(("http", "git@")):
            temp_dir = tempfile.mkdtemp(prefix="pabp_source_")
            
            if str(source).endswith(".zip"):
                self._download_and_extract_zip(str(source), Path(temp_dir))
            else:
                self._clone_repo(str(source), Path(temp_dir))
            source_path = Path(temp_dir)
            
        try:
            return self._install_from_path(source_path, dry_run)
        finally:
            if temp_dir:
                def on_rm_error(func, path, exc_info):
                    import os
                    import stat
                    # Handle read-only files (common in .git)
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                    
                shutil.rmtree(temp_dir, onerror=on_rm_error)

    def _clone_repo(self, url: str, target: Path) -> None:
        """Clone a git repository."""
        import subprocess
        subprocess.check_call(
            ["git", "clone", "--depth", "1", url, str(target)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def _download_and_extract_zip(self, url: str, target: Path) -> None:
        """Download and extract a ZIP bundle."""
        import urllib.request
        import zipfile
        
        # Determine if it's a raw file or GitHub blob
        download_url = url
        if "github.com" in url and "/blob/" in url:
            # Convert blob URL to raw URL
            download_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            
        zip_path = target / "bundle.zip"
        
        logger.info(f"Downloading ZIP from: {download_url}")
        try:
            urllib.request.urlretrieve(download_url, zip_path)
        except Exception as e:
            raise RuntimeError(f"Failed to download ZIP: {e}")
            
        logger.info("Extracting ZIP...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target)
            
        # If the zip contains a single top-level directory, move contents up
        items = list(target.iterdir())
        items = [i for i in items if i.name != "bundle.zip"]
        
        if len(items) == 1 and items[0].is_dir():
            root_dir = items[0]
            for item in root_dir.iterdir():
                shutil.move(str(item), str(target))
            root_dir.rmdir()

    def _install_from_path(self, source_path: Path, dry_run: bool) -> UpdateResult:
        """Install components from a local source path."""
        # Check if this is a PABP Bundle (manifest.json + components/)
        if (source_path / "manifest.json").exists() and (source_path / "components").exists():
            return self._install_from_bundle(source_path, dry_run)
            
        # Standard platform-to-platform transfer
        source_adapter = detect_platform(source_path)
        logger.info(f"Detected source platform: {source_adapter.platform_name}")
        
        added = []
        modified = []
        errors = []
        
        # Discover components
        components = self._discover_components(source_path, source_adapter)
        
        for comp_type, name, content_path in components:
            try:
                # Read content
                content = content_path.read_text(encoding="utf-8")
                
                # Transform content
                transformed = self.target_adapter.transform_content(content, source_adapter)
                
                # Determine target path
                # Standard transfer doesn't usually have suggested path in metadata separately unless in content header?
                # PABP JSON has it in 'target_path' field for scripts.
                # But here we are installing from file/dir structure.
                # We don't have metadata dict here easily accessible unless we parse it specially.
                # Standard components rely on name/type mapping.
                
                target_path = self._get_target_path(comp_type, name)
                full_target_path = self.project_root / target_path
                
                # Check interaction
                if not full_target_path.exists():
                    action = "added"
                elif full_target_path.read_text(encoding="utf-8") != transformed:
                    action = "modified"
                else:
                    action = "skipped"
                    
                if action != "skipped":
                    if not dry_run:
                        full_target_path.parent.mkdir(parents=True, exist_ok=True)
                        full_target_path.write_text(transformed, encoding="utf-8")
                    
                    if action == "added":
                        added.append(f"{comp_type}:{name}")
                    else:
                        modified.append(f"{comp_type}:{name}")
                        
            except Exception as e:
                errors.append(f"{comp_type}:{name} - {str(e)}")
                
        # Handle Rules
        self._install_rules(source_path, source_adapter, dry_run, modified)
        
        # Create audit log
        audit_log = self._create_audit_log(source_path, added, modified, errors, dry_run)
        
        return UpdateResult(added, modified, errors, audit_log)
        
    def _install_from_bundle(self, source_path: Path, dry_run: bool) -> UpdateResult:
        """Install components from a PABP Bundle."""
        logger.info("Detected PABP Bundle format")
        
        added = []
        modified = []
        errors = []
        
        components_dir = source_path / "components"
        
        # Scan all relevant subdirectories
        patterns = [
            "skills/*.pabp.json",
            "agents/*.pabp.json", 
            "knowledge/*.pabp.json",
            "workflows/*.pabp.json",
            "mcp_configs/*.pabp.json",
            "scripts/*.pabp.json"
        ]
        
        found_files = []
        for pattern in patterns:
            found_files.extend(components_dir.rglob(pattern)) # rglob acts on dir, but pattern should be simpler if doing recursive
            # Actually rglob("*.pabp.json") covers everything recursively in components/
            # The original code was: for pabp_file in components_dir.rglob("*.pabp.json"):
            # This already covers all subdirectories including scripts/!
            
        # Reverting to original loop but ensuring we handle the types
        for pabp_file in components_dir.rglob("*.pabp.json"):
            try:
                data = json.loads(pabp_file.read_text(encoding="utf-8"))
                comp_type = data.get("$type")
                name = data.get("name")
                
                if not comp_type or not name:
                    continue
                    
                # Sanitize name for filesystem
                safe_name = self._sanitize_filename(name)
                
                # Special handling for MCP Config (Directory based)
                if comp_type == "mcp_config":
                    target_dir = self.project_root / ".agent" / "mcp" / safe_name
                    if not dry_run:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        
                    files = data.get("files", {})
                    # Add README if missing
                    if "README.md" not in files and "setup-guide.md" not in files:
                        files["README.md"] = f"# {name}\nMCP Configuration"
                        
                    for fname, fcontent in files.items():
                        fpath = target_dir / fname
                        if not dry_run:
                            fpath.write_text(fcontent, encoding="utf-8")
                    
                    added.append(f"mcp:{safe_name}")
                    continue

                # Convert PABP JSON to Target Format
                content = self._convert_pabp_component(data, comp_type)
                
                if not content:
                    continue
                    
                # Determine target path (use safe_name)
                suggested_path = data.get("target_path", "")
                target_path = self._get_target_path(comp_type, safe_name, suggested_path)
                full_target_path = self.project_root / target_path
                
                # Check interaction
                if not full_target_path.exists():
                    action = "added"
                elif full_target_path.read_text(encoding="utf-8") != content:
                    action = "modified"
                else:
                    action = "skipped"
                    
                if action != "skipped":
                    if not dry_run:
                        full_target_path.parent.mkdir(parents=True, exist_ok=True)
                        full_target_path.write_text(content, encoding="utf-8")
                    
                    if action == "added":
                        added.append(f"{comp_type}:{safe_name}")
                    else:
                        modified.append(f"{comp_type}:{safe_name}")
                        
            except Exception as e:
                logger.error(f"Failed to process {pabp_file}: {e}")
                errors.append(f"{pabp_file.name} - {str(e)}")
                
        # Create audit log
        audit_log = self._create_audit_log(source_path, added, modified, errors, dry_run)
        
        return UpdateResult(added, modified, errors, audit_log)
        
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name for use as a filename."""
        import re
        # Replace invalid characters with -
        # Windows: < > : " / \ | ? *
        safe_name = re.sub(r'[<>:"/\\|?*]', '-', name)
        # Strip leading/trailing spaces and dots
        safe_name = safe_name.strip(" .")
        return safe_name

    def _convert_pabp_component(self, data: Dict[str, Any], comp_type: str) -> Optional[str]:
        """Convert PABP JSON structure to target file format (Markdown/JSON/YAML).

        Delegates skill, agent, and workflow rendering to the shared
        ``lib.society.pabp.renderers`` module which produces
        Antigravity-native Markdown.
        """
        if comp_type == "skill":
            return render_skill_markdown(data)
        elif comp_type == "agent":
            return render_agent_markdown(data)
        elif comp_type == "knowledge":
            return json.dumps(data.get("content", {}), indent=2)
        elif comp_type == "workflow":
            return render_workflow_markdown(data)
        elif comp_type == "mcp_config":
            return self._convert_mcp_config(data)
        elif comp_type == "script":
            return data.get("content", "")
        return None
        
    def _convert_skill(self, data: Dict[str, Any]) -> str:
        """Convert Skill JSON to Antigravity Markdown with Frontmatter.

        Delegates to ``renderers.render_skill_markdown`` for proper
        deduplication and format compliance.
        """
        return render_skill_markdown(data)
        
    def _convert_agent(self, data: Dict[str, Any]) -> str:
        """Convert Agent JSON to Antigravity Markdown.

        Delegates to ``renderers.render_agent_markdown`` for proper
        wiki-link skills, relative knowledge paths, and section ordering.
        """
        return render_agent_markdown(data)

    def _convert_mcp_config(self, data: Dict[str, Any]) -> str:
        """
        Convert MCP Config.
        Returns the main SETUP guide or a summary.
        Actuall extraction of files happens during installation.
        """
        # We will handle file writing in _install_from_bundle directly for MCP
        # This just returns a README for the main path
        return data.get("files", {}).get("setup-guide.md", "# MCP Config\nSee files in this directory.")

    def _discover_components(
        self,
        source_path: Path,
        adapter: PlatformAdapter
    ) -> List[Tuple[str, str, Path]]:
        """
        Discover components in source using adapter paths.
        Returns list of (type, name, path).
        """
        components = []
        
        # Skills
        skills_dir = source_path / adapter.skills_dir
        if skills_dir.exists():
            for skill_file in skills_dir.glob("**/SKILL.md"):
                # name is parent dir name usually
                name = skill_file.parent.name
                components.append(("skill", name, skill_file))
                
        # Agents
        agents_dir = source_path / adapter.agents_dir
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                name = agent_file.stem
                components.append(("agent", name, agent_file))
                
        # Knowledge
        knowledge_dir = source_path / adapter.knowledge_dir
        if knowledge_dir.exists():
            for k_file in knowledge_dir.glob("*.json"):
                name = k_file.stem
                components.append(("knowledge", name, k_file))
                
        # Workflows
        workflows_dir = source_path / adapter.workflows_dir
        if workflows_dir.exists():
            for w_file in workflows_dir.glob("*"):
                if w_file.suffix in [".yaml", ".json"]:
                    name = w_file.stem
                    components.append(("workflow", name, w_file))
                    
        return components

    def _get_target_path(self, comp_type: str, name: str, suggested_path: str = "") -> Path:
        """Get target path for component."""
        if comp_type == "skill":
            return self.target_adapter.skill_path(name)
        elif comp_type == "agent":
            return self.target_adapter.agent_path(name)
        elif comp_type == "knowledge":
            return self.target_adapter.knowledge_path(name)
        elif comp_type == "workflow":
            return self.target_adapter.workflow_path(name)
        elif comp_type == "script":
            # Some scripts come with a suggested target_path in JSON
            # We can use that if name is not sufficient
            # But we might need to sanitize it or check for directory traversal?
            # For now, trust the adapter to handle suggested_path or ignore it
            # But wait, adapter.script_path implementation I wrote takes suggested path?
            # Let's check adapter signature. I added: def script_path(self, name: str) -> Path:
            # I need to update adapter signature too potentially if I want adapter to decide
            # Or just handle it here if suggested_path is present and safe.
            
            if suggested_path and ".." not in suggested_path:
                 return Path(suggested_path)
            
            return self.target_adapter.script_path(name)
        else:
            raise ValueError(f"Unknown component type: {comp_type}")

    def _install_rules(
        self,
        source_path: Path,
        source_adapter: PlatformAdapter,
        dry_run: bool,
        modified: List[str]
    ) -> None:
        """Translate and install rules file."""
        source_rules = source_path / source_adapter.rules_path()
        if source_rules.exists():
            content = source_rules.read_text(encoding="utf-8")
            translated = self.target_adapter.translate_rules(content, source_adapter)
            
            target_rules = self.project_root / self.target_adapter.rules_path()
            
            if not target_rules.exists() or target_rules.read_text(encoding="utf-8") != translated:
                if not dry_run:
                    target_rules.parent.mkdir(parents=True, exist_ok=True)
                    target_rules.write_text(translated, encoding="utf-8")
                modified.append("rules")

    def _create_audit_log(
        self,
        source: Path,
        added: List[str],
        modified: List[str],
        errors: List[str],
        dry_run: bool
    ) -> Path:
        """Create an audit log of the operation."""
        log_dir = self.project_root / "docs" / "transfers"
        if not dry_run:
            log_dir.mkdir(parents=True, exist_ok=True)
            
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = log_dir / f"transfer-{timestamp}.json"
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "source": str(source),
            "platform": self.target_adapter.platform_name,
            "dry_run": dry_run,
            "added": added,
            "modified": modified,
            "errors": errors
        }
        
        if not dry_run:
            log_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            
        return log_file
