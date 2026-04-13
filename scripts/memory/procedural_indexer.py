"""
Procedural Indexer
Phase 4 of the Automated Cognitive Memory System.
Scans the `.agent/workflows/` and `.agent/skills/` directories.
Indexes them into the Vector DB using a structure that allows parent-child RAG
(small chunk retrieval -> full document context).
"""

import logging
import os
from pathlib import Path
import yaml
from typing import Dict, List, Any

from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_PROCEDURAL, COLLECTION_TOOLBOX

logger = logging.getLogger(__name__)


class ProceduralIndexer:
    def __init__(self, workspace_root: str = "."):
        self.root = Path(workspace_root)
        self.workflows_dir = self.root / ".agent" / "workflows"
        self.skills_dir = self.root / ".agent" / "skills"
        self.blueprints_dir = self.root / ".agent" / "blueprints"
        self.templates_dir = self.root / ".agent" / "templates"
        self.mcp_dir = self.root / ".agent" / "mcp"
        self.vector_store = get_memory_store()

    def index_all(self):
        """Indexes all procedural factory assets."""
        w = self.index_workflows()
        s = self.index_skills()
        b = self.index_blueprints()
        t = self.index_templates()
        m = self.index_mcp()
        return w, s, b, t, m

    def index_workflows(self) -> int:
        """
        Indexes .md files in the workflows directory.
        Yields chunks for each workflow step (child) mapped to the full workflow (parent).
        """
        count = 0
        if not self.workflows_dir.exists():
            return count

        for filepath in self.workflows_dir.glob("*.md"):
            self._process_markdown_file(filepath, COLLECTION_PROCEDURAL, "workflow")
            count += 1

        return count

    def index_skills(self) -> int:
        """
        Indexes SKILL.md files in the skills directory hierarchy.
        """
        count = 0
        if not self.skills_dir.exists():
            return count

        for filepath in self.skills_dir.rglob("SKILL.md"):
            self._process_markdown_file(filepath, COLLECTION_TOOLBOX, "skill")
            count += 1

        return count
        return count

    def index_blueprints(self) -> int:
        count = 0
        if not self.blueprints_dir.exists():
            return count
        for filepath in self.blueprints_dir.rglob("*.json"):  # mostly manifests
            self._process_markdown_file(filepath, COLLECTION_TOOLBOX, "blueprint")
            count += 1
        return count

    def index_templates(self) -> int:
        count = 0
        if not self.templates_dir.exists():
            return count
        for filepath in self.templates_dir.rglob("*.j2"):  # Jinja templates
            self._process_markdown_file(filepath, COLLECTION_TOOLBOX, "template")
            count += 1
        return count

    def index_mcp(self) -> int:
        count = 0
        if not self.mcp_dir.exists():
            return count
        for filepath in self.mcp_dir.rglob("*.json"):
            self._process_markdown_file(filepath, COLLECTION_TOOLBOX, "mcp_config")
            count += 1
        return count

    def _process_markdown_file(self, filepath: Path, collection: str, doc_type: str):
        """
        Extracts YAML frontmatter (if present) and markdown body.
        Creates a parent document and indexes small, searchable chunk summaries mapping to it.
        """
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read {filepath}: {e}")
            return

        # Parse YAML frontmatter if it exists
        frontmatter = {}
        body = content

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except yaml.YAMLError:
                    logger.warning(f"Failed to parse YAML frontmatter in {filepath}")

        doc_id = filepath.stem if doc_type == "workflow" else filepath.parent.name

        # We index the "Parent"
        # In a real parent-child RAG, we would store chunks that point to this parent ID.
        # Since our MemoryStore directly embeds `content`, we will store the "description"
        # (or first paragraph) as the indexed content, but supply the full body in the metadata payload.
        # This way semantic search matches the intent, but the agent receives the full text.

        searchable_content = frontmatter.get("description", "")
        if not searchable_content:
            # Fallback to first few lines
            searchable_content = "\n".join(body.split("\n")[:3])

        metadata = {
            "id": doc_id,
            "type": doc_type,
            "filepath": str(filepath.relative_to(self.root)),
            "full_body": body,
            "frontmatter": frontmatter,
        }

        vector_id = self.vector_store.add_memory(
            content=f"[{doc_type.upper()}] {doc_id}: {searchable_content}",
            metadata=metadata,
            memory_type=collection,
        )
        logger.debug(
            f"Indexed {doc_type} {doc_id} to {collection} with vector ID {vector_id}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    indexer = ProceduralIndexer()
    w, s, b, t, m = indexer.index_all()
    print(
        f"Indexing Complete: {w} workflows, {s} skills, {b} blueprints, {t} templates, {m} MCPs."
    )
