# Shareable agent workflow
Purpose: portable macOS rules and existing Obsidian/Graphify integrations.
Architecture: install.py previews or copies payload/ files and merges supported hooks.
Directories: payload/claude and payload/codex contain rules; scripts and obsidian contain tools.
Use Python standard library; retain dry-run default, backup behavior and hook idempotence.
Never bundle credentials, transcripts, personal vault notes, caches or backups.
Safe edits: README.md, install.py and reviewed payload files. No model calls during checks.
Check: python3 install.py --home <disposable-home>; repeat --install twice to test idempotence.
Test with disposable settings to verify unrelated hooks survive. Never test by replacing live settings.
No dependencies are installed and no schedule is activated by the installer.
