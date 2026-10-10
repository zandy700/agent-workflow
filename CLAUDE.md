# Shareable agent workflow
Purpose: portable rules and Obsidian/Graphify integrations for macOS and Windows.
Architecture: install.py previews or copies payload/ files and merges supported hooks.
Directories: payload/claude, codex, cursor contain rules; scripts and obsidian contain tools; skills holds the /icm skill.
Use Python standard library; retain dry-run default, backup behavior and hook idempotence.
Scripts are Python, not bash, so one copy runs on macOS and Windows; hook commands are only `<python> "<absolute path>"` (no shell syntax).
Never bundle credentials, transcripts, personal vault notes, caches or backups.
Safe edits: README.md, install.py and reviewed payload files. No model calls during checks.
Check: python3 install.py --home <disposable-home>; repeat --install twice to test idempotence.
Test with disposable settings to verify unrelated hooks survive. Never test by replacing live settings.
No dependencies are installed and no schedule is activated by the installer.
