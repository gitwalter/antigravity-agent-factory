import pytest
from pathlib import Path
import shutil
import tempfile
from scripts.maintenance.link_checker import LinkChecker


@pytest.fixture
def temp_repo():
    """Creates a temporary repository structure for testing."""
    temp_dir = tempfile.mkdtemp()
    root = Path(temp_dir)

    # Create some files
    (root / "docs").mkdir()
    (root / "docs" / "target.md").write_text("# Target", encoding="utf-8")
    (root / "README.md").write_text(
        "[Target](docs/target.md) and [Missing](missing.md)", encoding="utf-8"
    )

    yield root
    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_link_validation(temp_repo):
    checker = LinkChecker(temp_repo, fix_mode=False, check_external=False)
    checker.build_index()

    # Check README.md
    readme_path = temp_repo / "README.md"
    await checker.process_file(readme_path)

    assert checker.links_found == 2
    assert len(checker.broken_internal) == 1
    assert "missing.md" in str(checker.broken_internal[0][1])


@pytest.mark.asyncio
async def test_link_repair(temp_repo):
    # Move target.md to a new location
    (temp_repo / "new_dir").mkdir()
    target_old = temp_repo / "docs" / "target.md"
    target_new = temp_repo / "new_dir" / "target.md"
    shutil.move(str(target_old), str(target_new))

    # README still points to ./docs/target.md which is now broken
    checker = LinkChecker(temp_repo, fix_mode=True, check_external=False)
    checker.build_index()  # Must re-index after move!

    readme_path = temp_repo / "README.md"
    await checker.process_file(readme_path)

    # It should have found 2 broken links:
    # 1. target.md (moved)
    # 2. missing.md (doesn't exist)

    assert checker.broken_links_count == 2
    assert checker.fixed_links_count == 1

    # Verify file content was updated
    new_content = readme_path.read_text(encoding="utf-8")
    assert "new_dir/target.md" in new_content
    # Note: os.path.relpath from root to new_dir/target.md from README.md dir:
    # README is at root. parent is root. target is root/new_dir/target.md. relpath: new_dir/target.md
    assert "./docs/target.md" not in new_content
    assert "**Broken**" not in new_content
    assert "[Missing](missing.md)" in new_content  # Remains broken


@pytest.mark.asyncio
async def test_link_normalization(temp_repo):
    """Verifies that valid root-based links are converted to relative paths when --normalize is active."""
    # Create target in docs/
    (temp_repo / "docs").mkdir(exist_ok=True)
    target = temp_repo / "docs" / "target.md"
    target.write_text("# Target", encoding="utf-8")

    # Create a file at root with an absolute-style link
    readme = temp_repo / "README.md"
    readme.write_text("[Absolute](/docs/target.md)", encoding="utf-8")

    # Create a file in a subfolder with an absolute-style link
    (temp_repo / "sub").mkdir()
    sub_file = temp_repo / "sub" / "other.md"
    sub_file.write_text("[Absolute](/docs/target.md)", encoding="utf-8")

    checker = LinkChecker(
        temp_repo, fix_mode=True, check_external=False, normalize=True
    )
    checker.build_index()

    await checker.process_file(readme)
    await checker.process_file(sub_file)

    # Verify README.md normalization (from root to docs/target.md)
    # Target is root/docs/target.md. Source is root/README.md. Relpath: docs/target.md
    assert "docs/target.md" in readme.read_text(encoding="utf-8")
    assert "/docs/target.md" not in readme.read_text(encoding="utf-8")

    # Verify sub/other.md normalization (from sub/ to docs/target.md)
    # Target is root/docs/target.md. Source is root/sub/other.md. Relpath: ../docs/target.md
    content = sub_file.read_text(encoding="utf-8")
    assert "../docs/target.md" in content
    assert (
        "(/docs/target.md)" not in content
    )  # Specific check for the markdown link parenthesized part


def test_find_best_match(temp_repo):
    checker = LinkChecker(temp_repo)

    # Should find target.md anywhere in the repo
    (temp_repo / "deep" / "path").mkdir(parents=True)
    other_file = temp_repo / "deep" / "path" / "other.json"
    other_file.write_text("{}", encoding="utf-8")

    checker.build_index()

    # Passing Path.parent to find_best_match
    readme_path = temp_repo / "README.md"
    found = checker.find_best_match(readme_path, "other.json")
    assert found is not None
    assert found.name == "other.json"

    found = checker.find_best_match(readme_path, "missing.md")
    assert found is None
