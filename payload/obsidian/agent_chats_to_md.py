#!/usr/bin/env python3
"""Export Codex (CLI+desktop) and Cursor agent chats to markdown for claude_to_obsidian.py.

Usage: agent_chats_to_md.py --export-dir DIR --vault-dir DIR
Writes DIR/codex/*.md and DIR/cursor/*.md. Incremental: skips a session whose vault note
is newer than its source file, so it is cheap enough to run after every agent turn.
"""
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

from claude_to_obsidian import chat_dir

HOME = Path.home()
WRAPPED = re.compile(r"^\s*<([A-Za-z_-]+)[^>]*>[\s\S]*</\1>\s*$")  # injected context blocks


def write(dest: Path, vault_dest: Path, src: Path, title: str, project: str, turns):
    if not turns or (vault_dest.exists() and vault_dest.stat().st_mtime >= src.stat().st_mtime):
        return
    body = "\n\n".join(f"## {'User' if r == 'user' else 'Assistant'}\n\n{t}" for r, t in turns)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f'---\nproject: "{project}"\n---\n# {title}\n\n{body}\n', encoding="utf-8")
    os.utime(dest, (src.stat().st_mtime,) * 2)  # so `created` = when the chat happened


def codex(export: Path, vault: Path):
    files = list((HOME / ".codex/sessions").rglob("rollout-*.jsonl"))
    files += list((HOME / ".codex/archived_sessions").rglob("rollout-*.jsonl"))
    for f in files:
        turns, meta = [], {}
        for line in f.open(encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            p = d.get("payload") or {}
            if d.get("type") == "session_meta":
                meta = p
            elif d.get("type") == "response_item" and p.get("type") == "message" and p.get("role") in ("user", "assistant"):
                text = "\n".join(c.get("text", "") for c in p.get("content", []) if isinstance(c, dict)).strip()
                if not text or WRAPPED.match(text) or text.startswith("# AGENTS.md"):
                    continue
                turns.append((p["role"], text))
        if meta.get("thread_source", "user") != "user" or isinstance(meta.get("source"), dict):
            continue  # guardian/sub-agent threads, not real chats
        day = (meta.get("timestamp") or datetime.fromtimestamp(f.stat().st_mtime).isoformat())[:10]
        sid = (meta.get("id") or f.stem)[-8:]
        name = f"codex-conversation-{day}-{sid}.md"
        cwd = meta.get("cwd", "")
        write(export / "codex" / name, chat_dir(vault, "codex", name) / name, f, name[:-3], Path(cwd).name or cwd, turns)


def cursor(export: Path, vault: Path):
    for f in (HOME / ".cursor/projects").glob("*/agent-transcripts/**/*.jsonl"):
        turns = []
        for line in f.open(encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            text = "\n".join(c.get("text", "") for c in d.get("message", {}).get("content", []) if c.get("type") == "text")
            text = re.sub(r"<timestamp>.*?</timestamp>|</?user_query>", "", text, flags=re.S).strip()
            if text and d.get("role") in ("user", "assistant"):
                turns.append((d["role"], text))
        day = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
        name = f"cursor-conversation-{day}-{f.stem[:8]}.md"
        project = f.parts[f.parts.index("projects") + 1]
        write(export / "cursor" / name, chat_dir(vault, "cursor", name) / name, f, name[:-3], project, turns)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--export-dir", type=Path, required=True)
    ap.add_argument("--vault-dir", type=Path, required=True)
    a = ap.parse_args()
    codex(a.export_dir, a.vault_dir)
    cursor(a.export_dir, a.vault_dir)
