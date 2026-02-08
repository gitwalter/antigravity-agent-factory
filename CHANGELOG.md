# Changelog

All notable changes to the Antigravity Agent Factory project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.0] - 2026-02-08

### Changed - Upstream Synchronization & Cleanup
- **Synchronized** with upstream reference repository (`gitwalter/antigravity-agent-factory`)
- **Branding Preservation**: Intelligent conflict resolution to maintain "Antigravity" branding vs "Cursor".
- **Documentation Cleanup**: Removed 20+ extraneous upstream documentation files to keep `docs/` focused.
- **Sync Script**: Added `scripts/maintenance/sync_upstream.py` to automate future syncs with doc pruning.
- **CI Fix**: Patched `verify-proofs.yml` to handle existing Lean toolchains idempotently.

## [4.0.0] - 2026-02-08

### Added
- Initial Antigravity Agent Factory fork setup.