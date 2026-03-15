import os
import re
import asyncio
import argparse
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict


class LinkChecker:
    def __init__(self, root_dir, fix_mode=False, check_external=True, normalize=False):
        self.root_dir = Path(root_dir).resolve()
        self.fix_mode = fix_mode
        self.check_external = check_external
        self.normalize = normalize
        self.broken_internal = []
        self.broken_external = []
        self.scanned_files = 0
        self.links_found = 0

        self.md_link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        self.wiki_link_re = re.compile(r"\[\[([a-zA-Z0-9\-\s._#|]+)\]\]")

        self.index = defaultdict(list)
        self.broken_links_count = 0
        self.fixed_links_count = 0
        self.semaphore = asyncio.Semaphore(50)

    def build_index(self):
        extensions = {
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".py",
            ".js",
            ".ts",
            ".txt",
            ".png",
            ".jpg",
            ".svg",
        }
        ignore_dirs = {
            ".git",
            ".venv",
            "node_modules",
            ".pytest_cache",
            ".ruff_cache",
            "__pycache__",
            "tmp",
        }

        print(f"Indexing repository at {self.root_dir}...")
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext in extensions:
                    file_path = Path(root) / f
                    self.index[f].append(file_path.resolve())
        print(f"Indexed {sum(len(v) for v in self.index.values())} files.")

    async def check_url(self, session, url):
        async with self.semaphore:
            try:
                async with session.head(
                    url, timeout=10, allow_redirects=True
                ) as response:
                    return url, None if response.status < 400 else response.status
            except Exception as e:
                return url, str(e)

    def is_internal(self, link):
        return ":" not in link or link.startswith("file:")

    def find_best_match(self, source_file, link_text):
        target_name = Path(link_text.split("#")[0]).name
        if not target_name:
            return None

        candidates = self.index.get(target_name, [])
        if not candidates and not os.path.splitext(target_name)[1]:
            candidates = self.index.get(f"{target_name}.md", [])

        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]

        source_parts = source_file.resolve().parts
        best_candidate, max_common = candidates[0], -1

        for cand in candidates:
            cand = cand.resolve()
            common = sum(1 for p1, p2 in zip(source_parts, cand.parts) if p1 == p2)
            if common > max_common:
                max_common, best_candidate = common, cand
            elif common == max_common:
                if abs(len(cand.parts) - len(source_parts)) < abs(
                    len(best_candidate.parts) - len(source_parts)
                ):
                    best_candidate = cand
        return best_candidate

    def resolve_to_relative(self, source_file, target_file):
        try:
            rel = os.path.relpath(target_file, source_file.parent).replace("\\", "/")
            if "/" not in rel and not rel.startswith("."):
                rel = f"./{rel}"
            return rel
        except Exception:
            return None

    async def process_file(self, file_path):
        file_path = Path(file_path).resolve()
        async with self.semaphore:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                modified = False

                matches = list(self.md_link_re.finditer(content))
                for match in reversed(matches):
                    text, link = match.groups()
                    self.links_found += 1

                    if self.is_internal(link):
                        if link.startswith("file:"):
                            path_str = unquote(
                                link.replace("file:///", "").replace("file://", "")
                            )
                            # Handle windows paths potentially with drive letters
                            if ":" in path_str and path_str.startswith("/"):
                                path_str = path_str[1:]
                            rel_path = Path(path_str).resolve()
                            is_valid = rel_path.exists()
                        else:
                            clean_link = unquote(link.split("#")[0]).replace("\\", "/")
                            rel_path = (file_path.parent / clean_link).resolve()
                            root_path = (
                                self.root_dir / clean_link.lstrip("/")
                            ).resolve()
                            is_valid = rel_path.exists() or root_path.exists()

                        # Special handling for directory links
                        if (
                            not is_valid
                            and not link.startswith("file:")
                            and clean_link.endswith("/")
                        ):
                            is_valid = rel_path.is_dir() or root_path.is_dir()

                        needs_fix = not is_valid

                        if not is_valid:
                            self.broken_internal.append((file_path, link))
                            self.broken_links_count += 1

                        if needs_fix and self.fix_mode:
                            target = self.find_best_match(file_path, link)
                            if target:
                                anchor = link.split("#")[1] if "#" in link else None
                                fixed = self.resolve_to_relative(file_path, target)
                                if fixed and fixed != link:
                                    if anchor:
                                        fixed += f"#{anchor}"
                                    print(
                                        f"  [FIX] {file_path.relative_to(self.root_dir)}: {link} -> {fixed}"
                                    )
                                    start, end = match.span(2)
                                    content = content[:start] + fixed + content[end:]
                                    modified = True
                                    self.fixed_links_count += 1

                        elif self.normalize and is_valid and link.startswith("/"):
                            # Normalize valid root-based links to relative
                            clean_link = link.split("#")[0].lstrip("/")
                            root_path = (self.root_dir / clean_link).resolve()
                            if root_path.exists():
                                anchor = link.split("#")[1] if "#" in link else None
                                fixed = self.resolve_to_relative(file_path, root_path)
                                if fixed and fixed != link:
                                    if anchor:
                                        fixed += f"#{anchor}"
                                    print(
                                        f"  [NORM] {file_path.relative_to(self.root_dir)}: {link} -> {fixed}"
                                    )
                                    start, end = match.span(2)
                                    content = content[:start] + fixed + content[end:]
                                    modified = True
                                    self.fixed_links_count += 1

                if modified and self.fix_mode:
                    file_path.write_text(content, encoding="utf-8")
                self.scanned_files += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    async def run(self, specific_files=None):
        self.build_index()
        self.external_links_to_check = set()

        files_to_scan = []
        if specific_files:
            files_to_scan = [Path(f).resolve() for f in specific_files]
        else:
            extensions = {".md", ".json", ".yaml", ".yml"}
            ignore_pattern = re.compile(
                r"\.(git|venv|pytest_cache|ruff_cache)|node_modules|tmp|__pycache__"
            )
            for root, _, files in os.walk(self.root_dir):
                if ignore_pattern.search(root):
                    continue
                for f in files:
                    if os.path.splitext(f)[1] in extensions:
                        files_to_scan.append(Path(root) / f)

        print(f"Scanning {len(files_to_scan)} files...")
        await asyncio.gather(*(self.process_file(f) for f in files_to_scan))

    def print_report(self):
        print("\n--- Link Verification Report ---")
        print(f"Scanned Files: {self.scanned_files}")
        print(f"Links Found: {self.links_found}")
        if self.broken_internal:
            print(f"\nBroken Internal Links ({len(self.broken_internal)}):")
            by_file = defaultdict(list)
            for f, l in self.broken_internal:
                by_file[f].append(l)
            for f in sorted(by_file.keys()):
                rel_f = f.relative_to(self.root_dir) if f.is_absolute() else f
                print(f"  {rel_f}:")
                for l in by_file[f]:
                    print(f"    [FAIL] {l}")
        else:
            print("\n[OK] No broken internal links found.")
        if self.fix_mode:
            print(
                f"\nFixed {self.fixed_links_count} out of {self.broken_links_count} broken internal links."
            )


async def main():
    parser = argparse.ArgumentParser(description="Link auditor and repair tool.")
    parser.add_argument("--path", default=".", help="Root path for indexing")
    parser.add_argument("--file", help="Specific file to scan")
    parser.add_argument("--fix", action="store_true", help="Fix broken links")
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize valid root-based links to relative",
    )
    args = parser.parse_args()

    checker = LinkChecker(args.path, fix_mode=args.fix, normalize=args.normalize)
    files = [args.file] if args.file else None
    await checker.run(specific_files=files)
    checker.print_report()


if __name__ == "__main__":
    asyncio.run(main())
