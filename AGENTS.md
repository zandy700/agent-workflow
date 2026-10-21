# Shareable agent workflow
Purpose: portable rules and Obsidian/Graphify integrations for macOS and Windows.
Architecture: bootstrap.py downloads the repo; setup.py installs the full bundle; install.py previews or copies core files and merges hooks.
Directories: payload/claude, codex, cursor contain rules; scripts and obsidian contain tools; skills holds the /icm skill.
Use Python standard library; retain dry-run default, backup behavior and hook idempotence.
Scripts are Python, not bash, so one copy runs on macOS and Windows; hook commands are only `<python> "<absolute path>"` (no shell syntax).
Never bundle credentials, transcripts, personal vault notes, caches or backups.
Safe edits: setup/installer scripts, bundle.json, docs, tests, and reviewed payload files. No model calls during checks.
Check: python3 install.py --home <disposable-home>; repeat --install twice to test idempotence.
Regression checks: python3 -m unittest discover -s tests -v (disposable homes only).
Test with disposable settings to verify unrelated hooks survive. Never test by replacing live settings.
setup.py --install installs pinned dependencies in an isolated environment and runs local chat sync. install.py only copies core files. Neither activates a schedule. Test full setup only in disposable homes.
