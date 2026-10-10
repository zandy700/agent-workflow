#!/usr/bin/env python3
"""Sync agent chats (Claude Code, Codex, Cursor) into the Obsidian vault.

Runs in the background after every agent turn (agent_stop_hook.py) and nightly
with --all (launchd on macOS, Task Scheduler on Windows). Chats land in
<vault>/chats/{code,codex,cursor}/.
"""
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = Path(os.environ.get("OBSIDIAN_VAULT", Path.home() / "Obsidian Sync/ObsidianVault"))
EXPORT = HERE / ".staging"
LOG = HERE / "claude_obsidian_sync.log"
LOCK = Path(tempfile.gettempdir()) / "claude_obsidian_sync.lock"
# Windows Python writes redirected output in the legacy code page; the helpers print ✓ and ═.
os.environ.setdefault("PYTHONUTF8", "1")


def find_tool(name):
    # Scheduled runs get a bare PATH, and pip often puts tools in a Scripts folder that isn't on it.
    extra = [sysconfig.get_path("scripts"), str(Path.home() / ".local/bin"), "/opt/homebrew/bin", "/usr/local/bin"]
    if hasattr(sysconfig, "get_preferred_scheme"):
        extra.append(sysconfig.get_path("scripts", sysconfig.get_preferred_scheme("user")))
    return shutil.which(name, path=os.pathsep.join([os.environ.get("PATH", ""), *extra]))


def run(full, log):
    def note(msg):
        log.write(f"[{datetime.now():%c}] {msg}\n")
        log.flush()

    note(f"Starting sync ({'--all' if full else 'recent'})")
    (EXPORT / "code").mkdir(parents=True, exist_ok=True)
    VAULT.mkdir(parents=True, exist_ok=True)
    py, common = sys.executable, ["--export-dir", str(EXPORT), "--vault-dir", str(VAULT)]

    # 1. Claude Code (terminal + desktop share ~/.claude/projects)
    extract = find_tool("claude-extract")
    if extract:
        scope = ["--all"] if full else ["--recent", "10"]
        subprocess.run([extract, *scope, "--output", str(EXPORT / "code")], stdout=subprocess.DEVNULL, stderr=log)
    else:
        note("claude-extract missing: pip install claude-conversation-extractor")

    # 2. Codex and Cursor
    subprocess.run([py, str(HERE / "agent_chats_to_md.py"), *common], stderr=log)

    # 3. Frontmatter + tags + wikilinks, then into the vault
    subprocess.run([py, str(HERE / "claude_to_obsidian.py"), *common, "--move"], stdout=log, stderr=subprocess.STDOUT)

    # 4. Nightly: refresh each bootstrapped repo's graph notes, then the vault Home
    if full:
        for origin in (VAULT / "graphify").glob("*/.origin"):
            repo = Path(origin.read_text(encoding="utf-8").strip())
            graph, canvas = repo / "graphify-out/graph.json", origin.parent / "graph.canvas"
            if graph.is_file() and (not canvas.exists() or graph.stat().st_mtime > canvas.stat().st_mtime):
                subprocess.run([py, str(HERE / "vault_organize.py"), "graph", str(repo), origin.parent.name], stderr=log)
        subprocess.run([py, str(HERE / "vault_organize.py"), "home"], stderr=log)
    note("Sync completed")


def main(full=False):
    # One run at a time (hooks fire every turn); take over a lock older than 10 minutes.
    try:
        if time.time() - LOCK.stat().st_mtime > 600:
            LOCK.rmdir()
    except OSError:
        pass
    try:
        LOCK.mkdir()
    except FileExistsError:
        return
    try:
        with LOG.open("a", encoding="utf-8") as log:
            run(full, log)
    finally:
        LOCK.rmdir()


if __name__ == "__main__":
    main("--all" in sys.argv[1:])
