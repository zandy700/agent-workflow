#!/usr/bin/env python3
"""List documents MarkItDown can convert that have no .md sibling yet.

SessionStart hook (no argument): scans the current folder, shows the first 10,
and skips the home folder. By hand: markitdown_scan.py <dir> lists them all.
"""
import os
import sys
from pathlib import Path

EXTS = {".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".xls", ".epub", ".msg"}
SKIP = {".git", "node_modules", "Library", ".venv", "venv", "dist", "build", ".Trash", ".cache"}


def main():
    by_hand = len(sys.argv) > 1
    top = Path(sys.argv[1] if by_hand else os.getcwd())
    if not top.is_dir() or (not by_hand and top.resolve() == Path.home().resolve()):
        return
    found = []
    for root, dirs, files in os.walk(top):
        depth = len(Path(root).relative_to(top).parts)
        dirs[:] = [d for d in dirs if d not in SKIP and depth < 2]  # files at most 3 levels deep
        for name in files:
            p = Path(root, name)
            if p.suffix.lower() in EXTS and not p.with_suffix(".md").exists():
                found.append("./" + p.relative_to(top).as_posix())
    if not found:
        return
    sys.stdout.reconfigure(encoding="utf-8")
    limit = len(found) if by_hand else 10
    print(f"markitdown scan of {top} - {len(found)} convertible document(s) with no .md sibling:")
    print("\n".join(sorted(found)[:limit]))
    if len(found) > limit:
        print(f"... and {len(found) - limit} more (full list: python ~/Scripts/markitdown_scan.py <dir>)")
    print("Convert one only when the task needs it (global rule: Documents).")


if __name__ == "__main__":
    main()
