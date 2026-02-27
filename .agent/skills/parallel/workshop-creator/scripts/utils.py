"""Shared utilities for workshop-creator scripts."""

from pathlib import Path


def parse_workshop_md(path: Path) -> tuple[str, str, str]:
    content = path.read_text(encoding="utf-8")
    title = path.stem
    return title, "Workshop training material", content
