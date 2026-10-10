#!/usr/bin/env python3
"""graphify-bootstrap [dir]: one-time, idempotent setup of a project for graphify + Obsidian.

1. AST-only graph (no model calls, no cost)  2. wiring for Claude Code, Codex, Cursor
3. git hooks that keep the graph fresh       4. the repo's two vault folders + graph notes
Repo isolation: graph in <repo>/graphify-out, notes in <vault>/<id>/ and <vault>/graphify/<id>/.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from sync_claude_obsidian import HERE, VAULT, find_tool


def git(*args, cwd):
    if not shutil.which("git"):
        return ""
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def repo_id(root):
    saved = root / "graphify-out/.repo-id"
    if saved.exists():
        return saved.read_text(encoding="utf-8").strip()
    rid = root.name
    origin = VAULT / "graphify" / rid / ".origin"
    if origin.exists() and origin.read_text(encoding="utf-8").strip() != str(root):
        # name clash with a different repo: <owner>--<repo> from the remote, else name + hash
        url = re.sub(r"\.git$", "", git("remote", "get-url", "origin", cwd=root))
        m = re.search(r"[:/]([^/]+)/([^/]+)$", url)
        rid = f"{m[1]}--{m[2]}" if m else url or f"{rid}-{hashlib.sha1(str(root).encode()).hexdigest()[:6]}"
    return rid


def main():
    os.environ.setdefault("OBSIDIAN_VAULT", str(VAULT))
    start = Path(sys.argv[1] if len(sys.argv) > 1 else os.getcwd()).resolve()
    root = Path(git("rev-parse", "--show-toplevel", cwd=start) or start).resolve()
    if root in (Path.home().resolve(), Path(root.anchor)):
        sys.exit(f"not a project: {root}")
    graphify = find_tool("graphify")
    if not graphify:
        sys.exit("graphify not found: pip install graphifyy")

    rid = repo_id(root)
    run = lambda *a, **kw: subprocess.run([graphify, *a], cwd=root, **kw)
    run("update", ".", check=True)  # AST-only; creates graphify-out/ on first run
    (root / "graphify-out/.repo-id").write_text(rid + "\n", encoding="utf-8")
    for app in ("claude", "codex", "cursor"):  # project rule files for each app
        run(app, "install", check=True, stdout=subprocess.DEVNULL)

    if git("rev-parse", "--git-dir", cwd=root):
        exclude = Path(git("rev-parse", "--path-format=absolute", "--git-path", "info/exclude", cwd=root))
        exclude.parent.mkdir(parents=True, exist_ok=True)
        lines = exclude.read_text(encoding="utf-8").splitlines() if exclude.exists() else []
        if "graphify-out/" not in lines:
            with exclude.open("a", encoding="utf-8") as f:
                f.write("graphify-out/\n")
        status = run("hook", "status", capture_output=True, text=True)
        if "not installed" in (status.stdout + status.stderr).lower():
            run("hook", "install", stdout=subprocess.DEVNULL)

    (VAULT / rid).mkdir(parents=True, exist_ok=True)
    (VAULT / "graphify" / rid).mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(HERE / "vault_organize.py"), "graph", str(root), rid], check=True)
    print(f"graphify ready: {root} (id: {rid}) -> {VAULT / 'graphify' / rid}")


if __name__ == "__main__":
    main()
