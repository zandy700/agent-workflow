#!/usr/bin/env python3
"""Preview or install the Mac workflow into one user's home directory."""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import plistlib
import shutil


ROOT = Path(__file__).resolve().parent
FILES = {
    "payload/claude/CLAUDE.md": ".claude/CLAUDE.md",
    "payload/codex/AGENTS.md": ".codex/AGENTS.md",
    "payload/scripts/agent-workflow-reference.md": "Scripts/agent-workflow-reference.md",
    "payload/scripts/markitdown_scan.sh": "Scripts/markitdown_scan.sh",
    "payload/obsidian/agent_stop_hook.sh": "Obsidian Sync/agent_stop_hook.sh",
    "payload/obsidian/agent_chats_to_md.py": "Obsidian Sync/agent_chats_to_md.py",
    "payload/obsidian/claude_to_obsidian.py": "Obsidian Sync/claude_to_obsidian.py",
    "payload/obsidian/graphify_bootstrap.sh": "Obsidian Sync/graphify_bootstrap.sh",
    "payload/obsidian/sync_claude_obsidian.sh": "Obsidian Sync/sync_claude_obsidian.sh",
    "payload/obsidian/vault_organize.py": "Obsidian Sync/vault_organize.py",
    "payload/obsidian/obsidian-organization.md": "Obsidian Sync/ObsidianVault/knowledge/obsidian-organization.md",
}


def add_hook(groups, event, command, *, codex=False):
    if codex:
        groups.setdefault(event, [])
        for group in groups[event]:
            if any(h.get("command") == command for h in group.get("hooks", [])):
                return
        groups[event].append({"hooks": [{"type": "command", "command": command, "timeout": 10}]})
    else:
        groups.setdefault(event, [])
        if not any(h.get("command") == command for group in groups[event] for h in group.get("hooks", [])):
            groups[event].append({"hooks": [{"type": "command", "command": command}]})


def json_file(path):
    return json.loads(path.read_text()) if path.exists() else {}


def settings(home):
    claude = json_file(home / ".claude/settings.json")
    hooks = claude.setdefault("hooks", {})
    add_hook(hooks, "SessionStart", '"$HOME/Scripts/markitdown_scan.sh" 2>/dev/null || true')
    add_hook(hooks, "Stop", '"$HOME/Obsidian Sync/sync_claude_obsidian.sh" >> "$HOME/Obsidian Sync/claude_obsidian_sync.log" 2>&1 || true')
    add_hook(hooks, "Stop", 'if [ "$PWD" != "$HOME" ] && [ -f "graphify-out/graph.json" ]; then graphify update . >> "$HOME/.cache/graphify-stop-hook.log" 2>&1 || true; fi')

    codex = json_file(home / ".codex/hooks.json")
    add_hook(codex.setdefault("hooks", {}), "Stop", '"$HOME/Obsidian Sync/agent_stop_hook.sh"', codex=True)
    return {
        ".claude/settings.json": claude,
        ".codex/hooks.json": codex,
    }


def launch_agent(home):
    command = str(home / "Obsidian Sync/sync_claude_obsidian.sh")
    path = ":".join(dict.fromkeys((str(home / ".local/bin"), str(home / "Scripts"), "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin")))
    return plistlib.dumps({
        "Label": "local.agent-workflow.obsidian-sync",
        "ProgramArguments": [command, "--all"],
        "StartCalendarInterval": {"Hour": 22, "Minute": 0},
        "EnvironmentVariables": {"PATH": path},
        "StandardOutPath": str(home / "Obsidian Sync/launchd_sync.log"),
        "StandardErrorPath": str(home / "Obsidian Sync/launchd_sync.error.log"),
        "RunAtLoad": False,
    })


def plan(home):
    items = {dest: (ROOT / source).read_bytes() for source, dest in FILES.items()}
    items["Scripts/graphify-bootstrap"] = b'#!/bin/bash\nexec "$HOME/Obsidian Sync/graphify_bootstrap.sh" "$@"\n'
    for dest, obj in settings(home).items():
        items[dest] = (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
    items["Library/LaunchAgents/local.agent-workflow.obsidian-sync.plist"] = launch_agent(home)
    return items


def main():
    parser = argparse.ArgumentParser(description="Preview by default; --install writes with backups.")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home(), help="target home (also useful for a disposable test)")
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    if not home.is_dir():
        parser.error(f"home directory does not exist: {home}")
    items = plan(home)
    changed = [(rel, data) for rel, data in items.items() if not (home / rel).exists() or (home / rel).read_bytes() != data]
    for rel, _ in changed:
        print(("WRITE " if args.install else "WOULD WRITE ") + str(home / rel))
    if not changed:
        print("Already installed; no changes.")
        return
    if not args.install:
        print(f"{len(changed)} files would change. Review this list, then run with --install.")
        return
    backup = home / "Scripts/agent-workflow-backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
    for rel, data in changed:
        dest = home / rel
        if dest.exists():
            prior = backup / rel
            prior.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, prior)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        if dest.suffix == ".sh" or rel == "Scripts/graphify-bootstrap":
            dest.chmod(dest.stat().st_mode | 0o111)
    (home / "Obsidian Sync/ObsidianVault").mkdir(parents=True, exist_ok=True)
    print(f"Installed {len(changed)} files. Backups of replaced files: {backup if backup.exists() else 'none needed'}")
    print("Next: read README.md for dependencies and nightly schedule activation.")


if __name__ == "__main__":
    main()
