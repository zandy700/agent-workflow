#!/usr/bin/env python3
"""Preview or install the workflow into one user's home directory (macOS or Windows)."""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import plistlib
import shlex
import shutil
import sys


ROOT = Path(__file__).resolve().parent
WINDOWS = sys.platform == "win32"
FILES = {
    "payload/claude/CLAUDE.md": ".claude/CLAUDE.md",
    "payload/codex/AGENTS.md": ".codex/AGENTS.md",
    "payload/cursor/USER_RULES.md": ".cursor/USER_RULES.md",
    "payload/cursor/workflow_context.py": ".cursor/workflow_context.py",
    "payload/scripts/agent-workflow-reference.md": "Scripts/agent-workflow-reference.md",
    "payload/scripts/markitdown_scan.py": "Scripts/markitdown_scan.py",
    "payload/obsidian/agent_stop_hook.py": "Obsidian Sync/agent_stop_hook.py",
    "payload/obsidian/agent_chats_to_md.py": "Obsidian Sync/agent_chats_to_md.py",
    "payload/obsidian/claude_to_obsidian.py": "Obsidian Sync/claude_to_obsidian.py",
    "payload/obsidian/graphify_bootstrap.py": "Obsidian Sync/graphify_bootstrap.py",
    "payload/obsidian/sync_claude_obsidian.py": "Obsidian Sync/sync_claude_obsidian.py",
    "payload/obsidian/vault_organize.py": "Obsidian Sync/vault_organize.py",
    "payload/obsidian/obsidian-organization.md": "Obsidian Sync/ObsidianVault/knowledge/obsidian-organization.md",
}
# The /icm skill, one copy per app: Claude Code, Codex (~/.agents), Cursor. Copies, not links: Windows restricts symlinks.
ICM_SKILL = [f"{app}/skills/icm/SKILL.md" for app in (".claude", ".agents", ".cursor")]
# Substrings that identify hook commands this installer owns, including the older bash versions.
OURS = ("agent_stop_hook.", "markitdown_scan.", "workflow_context.py", "sync_claude_obsidian.sh", 'graphify update . >> "$HOME/.cache/graphify-stop-hook.log"')
TASK = "agent-workflow-obsidian-sync"
RULE_FILES = {".claude/CLAUDE.md", ".codex/AGENTS.md", ".cursor/USER_RULES.md"}
START, END = "<!-- agent-workflow:start -->", "<!-- agent-workflow:end -->"
# Exact unmarked rules shipped at d3f634f; customized files are never replaced wholesale.
LEGACY_RULE_HASH = "826ddb94647b96ddc5ee88ab73a58ba8e1804b2e95ae489803c208e0e958cddf"


def command(home, rel):
    runtime = home / "Scripts/agent-workflow-runtime" / ("Scripts/python.exe" if WINDOWS else "bin/python")
    executable = str(runtime) if runtime.is_file() else sys.executable
    args = [executable, str(home / rel)]
    return ' '.join(f'"{arg}"' for arg in args) if WINDOWS else shlex.join(args)


def ours(cmd):
    return any(marker in cmd for marker in OURS)


def set_hook(groups, event, cmd, *, codex=False):
    """Make cmd the only hook of ours for this event; leave everyone else's hooks alone."""
    kept = []
    for group in groups.get(event, []):
        hooks = [h for h in group.get("hooks", []) if not ours(h.get("command", ""))]
        if hooks:
            kept.append({**group, "hooks": hooks})
    hook = {"type": "command", "command": cmd, **({"timeout": 10} if codex else {})}
    groups[event] = kept + [{"hooks": [hook]}]


def json_file(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def settings(home):
    stop = command(home, "Obsidian Sync/agent_stop_hook.py")

    claude = json_file(home / ".claude/settings.json")
    hooks = claude.setdefault("hooks", {})
    set_hook(hooks, "SessionStart", command(home, "Scripts/markitdown_scan.py"))
    set_hook(hooks, "Stop", stop)

    codex = json_file(home / ".codex/hooks.json")
    set_hook(codex.setdefault("hooks", {}), "Stop", stop, codex=True)

    cursor = json_file(home / ".cursor/hooks.json")
    cursor.setdefault("version", 1)
    cursor_hooks = cursor.setdefault("hooks", {})
    cursor_hooks["stop"] = [h for h in cursor_hooks.get("stop", []) if not ours(h.get("command", ""))]
    cursor_hooks["stop"].append({"command": stop, "timeout": 10})
    cursor_hooks["sessionStart"] = [h for h in cursor_hooks.get("sessionStart", []) if not ours(h.get("command", ""))]
    cursor_hooks["sessionStart"].append({"command": command(home, ".cursor/workflow_context.py"), "timeout": 10})
    return {
        ".claude/settings.json": claude,
        ".codex/hooks.json": codex,
        ".cursor/hooks.json": cursor,
    }


def launch_agent(home):
    path = ":".join(dict.fromkeys((str(home / ".local/bin"), str(home / "Scripts"), "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin")))
    return plistlib.dumps({
        "Label": "local.agent-workflow.obsidian-sync",
        "ProgramArguments": ["/usr/bin/env", "python3", str(home / "Obsidian Sync/sync_claude_obsidian.py"), "--all"],
        "StartCalendarInterval": {"Hour": 22, "Minute": 0},
        "EnvironmentVariables": {"PATH": path},
        "StandardOutPath": str(home / "Obsidian Sync/launchd_sync.log"),
        "StandardErrorPath": str(home / "Obsidian Sync/launchd_sync.error.log"),
        "RunAtLoad": False,
    })


def schedule_command(home):
    """PowerShell command that turns on the nightly sync in Windows Task Scheduler."""
    exe = Path(sys.executable)
    quiet = exe.with_name("pythonw.exe")  # no console window popping up at 22:00
    script = home / "Obsidian Sync/sync_claude_obsidian.py"
    return (f"Register-ScheduledTask -TaskName '{TASK}' -Trigger (New-ScheduledTaskTrigger -Daily -At 10pm) "
            f"-Action (New-ScheduledTaskAction -Execute '{quiet if quiet.exists() else exe}' -Argument '\"{script}\" --all')")


def merge_rules(existing, body):
    """Replace only our marked block; keep custom global instructions."""
    block = f"{START}\n{body.rstrip()}\n{END}"
    if START in existing or END in existing:
        if existing.count(START) != 1 or existing.count(END) != 1 or existing.index(START) > existing.index(END):
            raise ValueError("Invalid agent-workflow markers; fix the global rules file before installing")
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block + after
    if (not existing.strip() or existing.strip() == body.strip()
            or hashlib.sha256(existing.strip().encode()).hexdigest() == LEGACY_RULE_HASH):
        return block + "\n"
    return existing.rstrip() + "\n\n" + block + "\n"


def plan(home):
    items = {dest: (ROOT / source).read_bytes() for source, dest in FILES.items()}
    for rel in RULE_FILES:
        path = home / rel
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        items[rel] = merge_rules(existing, items[rel].decode()).encode()
    skill = (ROOT / "payload/skills/icm/SKILL.md").read_bytes()
    for dest in ICM_SKILL:
        path = home / dest
        if path.exists() and path.read_bytes() != skill:
            print(f"Keeping existing custom skill: {path}")
        elif (path.is_symlink() or path.parent.is_symlink()) and not path.exists():
            raise ValueError(f"Repair the existing skill symlink before installing: {path.parent}")
        else:
            items[dest] = skill
    # Opt-in activation; preserve an existing explicit Ponytail preference.
    config_dir = home / ("AppData/Roaming" if WINDOWS else ".config")
    if home == Path.home().resolve():
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME") or
                          (os.environ.get("APPDATA") if WINDOWS else "") or config_dir)
    ponytail = config_dir / "ponytail/config.json"
    try:
        rel = str(ponytail.relative_to(home))
    except ValueError:
        print("Ponytail config is outside the target home; set defaultMode to off there if desired.")
    else:
        config = json_file(ponytail)
        if "defaultMode" not in config:
            config["defaultMode"] = "off"
            items[rel] = (json.dumps(config, indent=2) + "\n").encode()
    if WINDOWS:
        items["Scripts/graphify-bootstrap.cmd"] = f'@{command(home, "Obsidian Sync/graphify_bootstrap.py")} %*\r\n'.encode()
    else:
        items["Scripts/graphify-bootstrap"] = f'#!/bin/sh\nexec {command(home, "Obsidian Sync/graphify_bootstrap.py")} "$@"\n'.encode()
        items["Library/LaunchAgents/local.agent-workflow.obsidian-sync.plist"] = launch_agent(home)
    for dest, obj in settings(home).items():
        items[dest] = (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
    return items


def apply(home, items, write=False):
    """Apply a prepared plan, retaining the standalone installer's backup behavior."""
    changed = [(rel, data) for rel, data in items.items() if not (home / rel).exists() or (home / rel).read_bytes() != data]
    for rel, _ in changed:
        print(("WRITE " if write else "WOULD WRITE ") + str(home / rel))
    if not changed:
        print("Already installed; no changes.")
    elif not write:
        print(f"{len(changed)} files would change. Review this list, then run with --install.")
    else:
        backup = home / "Scripts/agent-workflow-backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        for rel, data in changed:
            dest = home / rel
            if dest.exists():
                prior = backup / rel
                prior.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest, prior)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            if rel == "Scripts/graphify-bootstrap":
                dest.chmod(dest.stat().st_mode | 0o111)
        (home / "Obsidian Sync/ObsidianVault").mkdir(parents=True, exist_ok=True)
        print(f"Installed {len(changed)} files. Backups of replaced files: {backup if backup.exists() else 'none needed'}")
    return len(changed)


def main():
    parser = argparse.ArgumentParser(description="Preview core files by default; use setup.py --install for the full bundle.")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home(), help="target home (also useful for a disposable test)")
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    if not home.is_dir():
        parser.error(f"home directory does not exist: {home}")
    apply(home, plan(home), args.install)
    if args.install:
        print("Core files installed. Use setup.py --install for dependencies, ICM, and the first sync.")
    if WINDOWS:
        print("\nOptional nightly sync: paste this into PowerShell once:\n" + schedule_command(home))


if __name__ == "__main__":
    main()
