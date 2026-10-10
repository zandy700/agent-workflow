#!/bin/bash
# graphify-bootstrap [dir]  — one-time, idempotent setup of a project for graphify + Obsidian.
#   1. AST-only graph (no LLM, no cost)   2. wiring for Claude Code, Codex, Cursor (project files)
#   3. git hooks that keep the graph fresh   4. the repo's two vault folders + graph notes
# Repo isolation: graph in <repo>/graphify-out, notes in <vault>/<id>/ and <vault>/graphify/<id>/.
# Nightly sync (--all) re-exports every bootstrapped repo, see sync_claude_obsidian.sh.
set -e
export OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-$HOME/Obsidian Sync/ObsidianVault}"
V="${OBSIDIAN_VAULT:-$HOME/Obsidian Sync/ObsidianVault}"
DIR="${1:-$PWD}"
ROOT=$(cd "$(git -C "$DIR" rev-parse --show-toplevel 2>/dev/null || echo "$DIR")" && pwd -P)
[ "$ROOT" = "$HOME" ] || [ "$ROOT" = / ] && { echo "not a project: $ROOT" >&2; exit 1; }
cd "$ROOT"

# <repo-id>: repo name; on a name clash with a different repo, <owner>--<repo> from the remote.
ID=$(cat graphify-out/.repo-id 2>/dev/null || true)
if [ -z "$ID" ]; then
    ID=$(basename "$ROOT")
    O="$V/graphify/$ID/.origin"
    if [ -f "$O" ] && [ "$(cat "$O")" != "$ROOT" ]; then
        R=$(git remote get-url origin 2>/dev/null | sed -E 's#(\.git)?$##; s#.*[:/]([^/]+)/([^/]+)$#\1--\2#')
        ID=${R:-$ID-$(printf %s "$ROOT" | shasum | cut -c1-6)}
    fi
fi

graphify update .                                   # AST-only; creates graphify-out/ on first run
echo "$ID" > graphify-out/.repo-id
graphify claude install >/dev/null                  # CLAUDE.md + hook  (Claude Code terminal + desktop)
graphify codex install >/dev/null                   # AGENTS.md         (Codex terminal + desktop, Cursor)
graphify cursor install >/dev/null                  # .cursor/rules/graphify.mdc (Cursor)

if git rev-parse --git-dir >/dev/null 2>&1; then
    X=$(git rev-parse --path-format=absolute --git-path info/exclude)
    mkdir -p "$(dirname "$X")"
    grep -qx 'graphify-out/' "$X" 2>/dev/null || echo 'graphify-out/' >> "$X"
    graphify hook status 2>&1 | grep -qi "not installed" && graphify hook install >/dev/null || true
fi

mkdir -p "$V/$ID" "$V/graphify/$ID"
python3 "$(dirname "$(readlink -f "$0")")/vault_organize.py" graph "$ROOT" "$ID"
echo "graphify ready: $ROOT (id: $ID) → $V/graphify/$ID/"
