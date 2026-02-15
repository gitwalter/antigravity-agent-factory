#!/usr/bin/env python3
"""
Blueprint Version Updater

Automates blueprint version updates by comparing blueprint.json files
against the version registry and updating outdated versions.

This script:
1. Reads knowledge/version-registry.json
2. Scans all blueprints in blueprints/ directory
3. Compares blueprint framework versions to registry
4. Generates a report of outdated versions
5. Updates blueprint.json files when run with --apply
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class UpdateStatus(Enum):
    """Status of version comparison."""

    UP_TO_DATE = "up_to_date"
    OUTDATED = "outdated"
    NOT_IN_REGISTRY = "not_in_registry"
    INVALID_VERSION = "invalid_version"


@dataclass
class VersionComparison:
    """Result of comparing a blueprint version to registry."""

    blueprint_name: str
    framework_name: str
    current_version: str
    registry_version: Optional[str]
    status: UpdateStatus
    suggested_version: Optional[str] = None
    language: Optional[str] = None


@dataclass
class BlueprintUpdate:
    """Represents an update to be made to a blueprint."""

    blueprint_path: Path
    framework_name: str
    current_version: str
    new_version: str
    language: str


class VersionComparator:
    """Handles version comparison logic."""

    @staticmethod
    def normalize_package_name(name: str) -> str:
        """
        Normalize package name for comparison.

        Args:
            name: Package name from blueprint

        Returns:
            Normalized package name (lowercase, no special chars)
        """
        # Convert to lowercase and remove common separators
        normalized = name.lower().replace("-", "").replace("_", "")
        # Handle common variations
        name_mapping = {
            "langchain": "langchain",
            "langgraph": "langgraph",
            "crewai": "crewai",
            "fastapi": "fastapi",
            "pydantic": "pydantic",
            "pytorch": "pytorch",
            "transformers": "transformers",
            "react": "react",
            "next": "next",
            "nextjs": "next",
            "typescript": "typescript",
            "vite": "vite",
            "springboot": "spring-boot",
            "spring-boot": "spring-boot",
            "aspnetcore": "aspnetcore",
            "asp.netcore": "aspnetcore",
            "anchor": "anchor",
            "solanasdk": "solana-sdk",
            "solana-sdk": "solana-sdk",
        }
        return name_mapping.get(normalized, normalized)

    @staticmethod
    def parse_version(version_str: str) -> Tuple[Optional[List[int]], Optional[str]]:
        """
        Parse version string into components.

        Args:
            version_str: Version string (e.g., "1.2.9", "1.2+", "2.x", "5+")

        Returns:
            Tuple of (version_numbers, suffix) or (None, None) if invalid
        """
        if not version_str:
            return None, None

        # Handle ranges like "2.x", "1.x"
        if version_str.endswith(".x"):
            base = version_str[:-2]
            parts = base.split(".")
            try:
                version_nums = [int(p) for p in parts]
                return version_nums, "x"
            except ValueError:
                return None, None

        # Handle versions with + suffix (e.g., "1.2+", "5+")
        if version_str.endswith("+"):
            base = version_str[:-1]
            parts = base.split(".")
            try:
                version_nums = [int(p) for p in parts]
                return version_nums, "+"
            except ValueError:
                return None, None

        # Handle plain version numbers (e.g., "1.2.9")
        parts = version_str.split(".")
        try:
            version_nums = [int(p) for p in parts]
            return version_nums, None
        except ValueError:
            return None, None

    @staticmethod
    def compare_versions(
        blueprint_version: str, registry_version: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Compare blueprint version to registry version.

        Args:
            blueprint_version: Version from blueprint (e.g., "1.2+", "2.10+")
            registry_version: Version from registry (e.g., "1.2.9", "2.10.0")

        Returns:
            Tuple of (is_outdated, suggested_version)
            is_outdated: True if blueprint version is outdated
            suggested_version: Suggested version string to use
        """
        bp_nums, bp_suffix = VersionComparator.parse_version(blueprint_version)
        reg_nums, reg_suffix = VersionComparator.parse_version(registry_version)

        if bp_nums is None or reg_nums is None:
            return False, None

        # Normalize lengths for comparison
        max_len = max(len(bp_nums), len(reg_nums))
        bp_nums = bp_nums + [0] * (max_len - len(bp_nums))
        reg_nums = reg_nums + [0] * (max_len - len(reg_nums))

        # Compare version numbers
        for i in range(max_len):
            if reg_nums[i] > bp_nums[i]:
                # Registry has newer version
                if bp_suffix == "+":
                    # Blueprint uses + range, suggest registry version with + suffix
                    suggested = ".".join(str(n) for n in reg_nums[: len(bp_nums)]) + "+"
                    return True, suggested
                elif bp_suffix == "x":
                    # Blueprint uses .x range (e.g., "2.x"), suggest major.minor.x pattern
                    # Always use major.minor.x format for .x ranges
                    if len(reg_nums) >= 2:
                        suggested = f"{reg_nums[0]}.{reg_nums[1]}.x"
                    else:
                        suggested = f"{reg_nums[0]}.x"
                    return True, suggested
                else:
                    # Blueprint has exact version, suggest registry version
                    return True, registry_version
            elif reg_nums[i] < bp_nums[i]:
                # Blueprint version is newer (shouldn't happen, but handle gracefully)
                return False, None

        # Versions are equal, check suffixes
        if bp_suffix == "+" and reg_suffix is None:
            # Blueprint allows newer, registry has exact - check if registry is newer
            if len(reg_nums) > len(bp_nums):
                return True, registry_version
            return False, None

        # Versions match
        return False, None


class BlueprintVersionUpdater:
    """Main class for updating blueprint versions."""

    def __init__(self, registry_path: Path, blueprints_dir: Path):
        """
        Initialize the updater.

        Args:
            registry_path: Path to version-registry.json
            blueprints_dir: Path to blueprints directory
        """
        self.registry_path = registry_path
        self.blueprints_dir = blueprints_dir
        self.registry: Dict[str, Any] = {}
        self.comparisons: List[VersionComparison] = []
        self.updates: List[BlueprintUpdate] = []

    def load_registry(self) -> None:
        """Load version registry from JSON file."""
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self.registry = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Version registry not found at {self.registry_path}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in registry file: {e}")

    def find_package_in_registry(
        self, package_name: str, language: str
    ) -> Optional[str]:
        """
        Find package version in registry.

        Args:
            package_name: Name of the package
            language: Programming language (python, javascript, etc.)

        Returns:
            Version string if found, None otherwise
        """
        normalized = VersionComparator.normalize_package_name(package_name)
        packages = self.registry.get("packages", {})

        if language not in packages:
            return None

        lang_packages = packages[language]

        # Try exact match first
        if normalized in lang_packages:
            return lang_packages[normalized]

        # Try case-insensitive match
        for key, value in lang_packages.items():
            if key.lower() == normalized:
                return value

        return None

    def scan_blueprint(self, blueprint_path: Path) -> List[VersionComparison]:
        """
        Scan a single blueprint file for version comparisons.

        Args:
            blueprint_path: Path to blueprint.json file

        Returns:
            List of version comparisons
        """
        comparisons = []

        try:
            with open(blueprint_path, "r", encoding="utf-8") as f:
                blueprint = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not read {blueprint_path}: {e}")
            return comparisons

        stack = blueprint.get("stack", {})
        language = stack.get("primaryLanguage", "").lower()

        # Check frameworks
        frameworks = stack.get("frameworks", [])
        for framework in frameworks:
            name = framework.get("name", "")
            version = framework.get("version", "")

            if not name or not version:
                continue

            registry_version = self.find_package_in_registry(name, language)
            if registry_version:
                is_outdated, suggested = VersionComparator.compare_versions(
                    version, registry_version
                )
                if is_outdated:
                    comparisons.append(
                        VersionComparison(
                            blueprint_name=blueprint_path.parent.name,
                            framework_name=name,
                            current_version=version,
                            registry_version=registry_version,
                            status=UpdateStatus.OUTDATED,
                            suggested_version=suggested,
                            language=language,
                        )
                    )
                else:
                    comparisons.append(
                        VersionComparison(
                            blueprint_name=blueprint_path.parent.name,
                            framework_name=name,
                            current_version=version,
                            registry_version=registry_version,
                            status=UpdateStatus.UP_TO_DATE,
                            language=language,
                        )
                    )
            else:
                comparisons.append(
                    VersionComparison(
                        blueprint_name=blueprint_path.parent.name,
                        framework_name=name,
                        current_version=version,
                        registry_version=None,
                        status=UpdateStatus.NOT_IN_REGISTRY,
                        language=language,
                    )
                )

        # Check tools with versions
        tools = stack.get("tools", [])
        for tool in tools:
            name = tool.get("name", "")
            version = tool.get("version")

            if not name or not version:
                continue

            registry_version = self.find_package_in_registry(name, language)
            if registry_version:
                is_outdated, suggested = VersionComparator.compare_versions(
                    version, registry_version
                )
                if is_outdated:
                    comparisons.append(
                        VersionComparison(
                            blueprint_name=blueprint_path.parent.name,
                            framework_name=name,
                            current_version=version,
                            registry_version=registry_version,
                            status=UpdateStatus.OUTDATED,
                            suggested_version=suggested,
                            language=language,
                        )
                    )

        return comparisons

    def scan_all_blueprints(self) -> None:
        """Scan all blueprint files in the blueprints directory."""
        if not self.blueprints_dir.exists():
            raise FileNotFoundError(
                f"Blueprints directory not found: {self.blueprints_dir}"
            )

        blueprint_files = list(self.blueprints_dir.glob("*/blueprint.json"))
        if not blueprint_files:
            print(f"Warning: No blueprint.json files found in {self.blueprints_dir}")

        for blueprint_path in sorted(blueprint_files):
            comparisons = self.scan_blueprint(blueprint_path)
            self.comparisons.extend(comparisons)

    def generate_report(self) -> str:
        """
        Generate a report of version comparisons.

        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("BLUEPRINT VERSION UPDATE REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Group by blueprint
        by_blueprint: Dict[str, List[VersionComparison]] = {}
        for comp in self.comparisons:
            if comp.blueprint_name not in by_blueprint:
                by_blueprint[comp.blueprint_name] = []
            by_blueprint[comp.blueprint_name].append(comp)

        outdated_count = sum(
            1 for c in self.comparisons if c.status == UpdateStatus.OUTDATED
        )
        up_to_date_count = sum(
            1 for c in self.comparisons if c.status == UpdateStatus.UP_TO_DATE
        )
        not_in_registry_count = sum(
            1 for c in self.comparisons if c.status == UpdateStatus.NOT_IN_REGISTRY
        )

        report_lines.append("Summary:")
        report_lines.append(f"  Outdated versions: {outdated_count}")
        report_lines.append(f"  Up-to-date versions: {up_to_date_count}")
        report_lines.append(f"  Not in registry: {not_in_registry_count}")
        report_lines.append("")

        # Detailed report by blueprint
        for blueprint_name in sorted(by_blueprint.keys()):
            comparisons = by_blueprint[blueprint_name]
            outdated = [c for c in comparisons if c.status == UpdateStatus.OUTDATED]

            if outdated:
                report_lines.append(f"Blueprint: {blueprint_name}")
                report_lines.append("-" * 80)
                for comp in outdated:
                    report_lines.append(f"  {comp.framework_name}:")
                    report_lines.append(f"    Current: {comp.current_version}")
                    report_lines.append(f"    Registry: {comp.registry_version}")
                    report_lines.append(f"    Suggested: {comp.suggested_version}")
                    report_lines.append("")
                report_lines.append("")

        if outdated_count == 0:
            report_lines.append("All versions are up-to-date!")

        return "\n".join(report_lines)

    def prepare_updates(self) -> None:
        """Prepare list of updates to be applied."""
        self.updates = []

        # Group comparisons by blueprint path
        by_blueprint: Dict[str, List[VersionComparison]] = {}
        for comp in self.comparisons:
            if comp.status == UpdateStatus.OUTDATED:
                if comp.blueprint_name not in by_blueprint:
                    by_blueprint[comp.blueprint_name] = []
                by_blueprint[comp.blueprint_name].append(comp)

        for blueprint_name, comparisons in by_blueprint.items():
            blueprint_path = self.blueprints_dir / blueprint_name / "blueprint.json"
            if not blueprint_path.exists():
                continue

            for comp in comparisons:
                if comp.suggested_version:
                    self.updates.append(
                        BlueprintUpdate(
                            blueprint_path=blueprint_path,
                            framework_name=comp.framework_name,
                            current_version=comp.current_version,
                            new_version=comp.suggested_version,
                            language=comp.language or "",
                        )
                    )

    def apply_updates(self) -> None:
        """Apply updates to blueprint files."""
        if not self.updates:
            print("No updates to apply.")
            return

        # Group updates by blueprint file
        by_file: Dict[Path, List[BlueprintUpdate]] = {}
        for update in self.updates:
            if update.blueprint_path not in by_file:
                by_file[update.blueprint_path] = []
            by_file[update.blueprint_path].append(update)

        for blueprint_path, updates in by_file.items():
            try:
                with open(blueprint_path, "r", encoding="utf-8") as f:
                    blueprint = json.load(f)

                updated_count = 0

                # Update frameworks
                frameworks = blueprint.get("stack", {}).get("frameworks", [])
                for framework in frameworks:
                    for update in updates:
                        if framework.get("name") == update.framework_name:
                            framework["version"] = update.new_version
                            updated_count += 1
                            print(
                                f"Updated {blueprint_path.name}: "
                                f"{update.framework_name} "
                                f"{update.current_version} -> {update.new_version}"
                            )

                # Update tools
                tools = blueprint.get("stack", {}).get("tools", [])
                for tool in tools:
                    for update in updates:
                        if tool.get("name") == update.framework_name:
                            tool["version"] = update.new_version
                            updated_count += 1
                            print(
                                f"Updated {blueprint_path.name}: "
                                f"{update.framework_name} "
                                f"{update.current_version} -> {update.new_version}"
                            )

                if updated_count > 0:
                    # Write updated blueprint
                    with open(blueprint_path, "w", encoding="utf-8") as f:
                        json.dump(blueprint, f, indent=2, ensure_ascii=False)
                        f.write("\n")  # Add trailing newline

            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error updating {blueprint_path}: {e}")


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Update blueprint versions based on version registry"
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("knowledge/version-registry.json"),
        help="Path to version registry JSON file",
    )
    parser.add_argument(
        "--blueprints-dir",
        type=Path,
        default=Path("blueprints"),
        help="Path to blueprints directory",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply updates to blueprint files (default is dry-run)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write report to file instead of stdout",
    )

    args = parser.parse_args()

    try:
        updater = BlueprintVersionUpdater(args.registry, args.blueprints_dir)
        updater.load_registry()
        updater.scan_all_blueprints()
        updater.prepare_updates()

        report = updater.generate_report()

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report written to {args.output}")
        else:
            print(report)

        if args.apply:
            print("\n" + "=" * 80)
            print("APPLYING UPDATES")
            print("=" * 80)
            updater.apply_updates()
            print(f"\nApplied {len(updater.updates)} updates.")
        else:
            print("\n" + "=" * 80)
            print("DRY-RUN MODE: No files were modified")
            print("Use --apply to update blueprint files")
            print("=" * 80)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
