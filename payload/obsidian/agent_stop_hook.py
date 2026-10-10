#!/usr/bin/env python3
"""Stop hook for Claude Code, Codex and Cursor.

Starts the chat sync and graph refresh in a background process and returns at
once, so the agent never waits. Always exits 0.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

from sync_claude_obsidian import find_tool, main as sync


def project_dir(payload):
    for key in ("CURSOR_PROJECT_DIR", "CLAUDE_PROJECT_DIR"):
        if os.environ.get(key):
            return os.environ[key]
    try:
        return json.loads(payload).get("cwd") or os.getcwd()
    except (ValueError, AttributeError):
        return os.getcwd()


def worker(project):
    sync()
    project = Path(project)
    graphify = find_tool("graphify")
    if graphify and project.resolve() != Path.home().resolve() and (project / "graphify-out/graph.json").is_file():
        log_dir = Path.home() / ".cache"
        log_dir.mkdir(parents=True, exist_ok=True)
        with (log_dir / "graphify-stop-hook.log").open("a", encoding="utf-8") as log:
            subprocess.run([graphify, "update", "."], cwd=project, stdout=log, stderr=subprocess.STDOUT)


def detach(args):
    quiet = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
    if os.name != "nt":
        subprocess.Popen(args, start_new_session=True, **quiet)
        return
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
    try:  # outlive the app if it closes right after the turn
        subprocess.Popen(args, creationflags=flags | subprocess.CREATE_BREAKAWAY_FROM_JOB, **quiet)
    except OSError:
        subprocess.Popen(args, creationflags=flags, **quiet)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--worker"]:
        worker(sys.argv[2])
    else:
        payload = sys.stdin.read() if not sys.stdin.isatty() else ""
        try:
            detach([sys.executable, str(Path(__file__).resolve()), "--worker", project_dir(payload)])
        except OSError:
            pass
    sys.exit(0)
