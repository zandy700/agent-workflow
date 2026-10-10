# Shareable agent workflow (macOS)

This package carries the same core workflow rules used with Claude Code and Codex: focused code reading, acceptance checks, small tool output, per-repository Graphify/Obsidian namespaces, concise handoffs, and sensible context resets. It includes the chat sync and Graphify bootstrap scripts for Claude Code and Codex. No transcripts, vault notes, tokens, credentials, account settings, or personal backups are included.

The installer copies files into **your** home directory. It previews changes by default, backs up each file it replaces, and merges only its hook commands into existing JSON settings. Inspect the preview and included files before installing. It does not sign into apps, download dependencies, start a Graphify scan, or activate the nightly schedule.

## Install on your Mac

1. Install and sign into Claude Code, Codex, and Obsidian. Use a personal machine and a personal vault, because the chat sync copies conversation text into that vault.
2. Extract this package, open Terminal in the extracted folder, and run `python3 install.py`. Read its proposed file list. Then run `python3 install.py --install` to apply it. Existing files are backed up under `~/Scripts/agent-workflow-backups/<timestamp>/`.
3. Install these separately if you want the related steps to work: [Graphify](https://pypi.org/project/graphifyy/) (`graphify` CLI and its skill), [MarkItDown](https://github.com/microsoft/markitdown) (`markitdown` command), and `claude-conversation-extractor` (`claude-extract` command). The core reading/editing rules still apply when these are absent, but graph creation, document conversion, or Claude transcript extraction cannot run. The bundle does not include third-party skill code.
4. Add `~/Scripts` to your shell `PATH` if it is not already there; the installed `graphify-bootstrap` wrapper lives there. Or call `~/Scripts/graphify-bootstrap` with its full path.
5. Start fresh chats in each app to load the new instructions. Ask each one to state its loaded workflow rule and check its hook status. A config file on disk alone does not prove the app loaded it.

The installer writes a **disabled until loaded** launchd definition for the full nightly Obsidian export at 22:00. After dependencies work, enable it with:

```bash
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/local.agent-workflow.obsidian-sync.plist"
```

The Stop hooks already request incremental sync after agent turns. The actual timing and loading of hooks must be checked in each app; the package only verifies the local configuration and scripts.

For a repository that needs a graph, run `~/Scripts/graphify-bootstrap /path/to/repository` once. It refuses `$HOME`. It will use `~/Obsidian Sync/ObsidianVault` by default, and creates that repository's own graph and vault folders. Do this only after Graphify is installed and after reviewing the repo. The `~/Obsidian Sync/ObsidianVault/chats/` folder holds synced transcripts; it is **not** part of this package.

## What is and is not included

- Included: exact Claude/Codex core instruction files as packaged, on-demand workflow reference, MarkItDown scan script, chat-to-Obsidian pipeline, a vault organization guide (installed to `ObsidianVault/knowledge/`, linked from generated project Home notes), guarded Graphify bootstrap and Stop hook, and config merger.
- External dependencies: Graphify, MarkItDown, `claude-extract`, and any skills referenced by the instructions, including ICM. Install them from their own sources only when you need them. Their availability is not proven by this package.
- The conversation note that prompted this export uses the third-party [Should I Build?](https://github.com/Endokelp/Should-I-build) skill. It is a separate, expensive multi-agent research workflow and is not part of the core token-saving rules. To reproduce that session, install it and its `last30days` and `deep-research` companion skills separately, then deliberately invoke it. This package does not run those agents.
- No personal projects or repositories are bundled. Each repo should have a short project `CLAUDE.md` and `AGENTS.md` based on its actual structure; this is a per-project step.

## Local checks without model calls

```bash
python3 -m py_compile install.py payload/obsidian/*.py
bash -n payload/obsidian/*.sh payload/scripts/*.sh
python3 install.py
```

The package does not claim a measured token reduction on your machine. A short pilot on the original setup found lower average input on one task, with quality edge cases in every candidate. Do not turn on a costly benchmark just to install this workflow.
