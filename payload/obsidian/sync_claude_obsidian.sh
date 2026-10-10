#!/bin/bash
# Sync agent chats (Claude Code, Codex, Cursor; terminal + desktop) → Obsidian vault.
# Runs after every agent turn (Stop hooks) and nightly via launchd (pass --all for a full re-export).
# Chats land in $VAULT_DIR/chats/{code,codex,cursor}/.

VAULT_DIR="${OBSIDIAN_VAULT:-$HOME/Obsidian Sync/ObsidianVault}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"   # this folder; survives being moved
EXPORT_DIR="$SCRIPT_DIR/.staging"       # staging area, emptied on every run
LOG="$SCRIPT_DIR/claude_obsidian_sync.log"
LOCK="/tmp/claude_obsidian_sync.lock"

# One run at a time (hooks fire every turn); steal a lock older than 10 min.
find "$LOCK" -maxdepth 0 -mmin +10 -exec rmdir {} \; 2>/dev/null
mkdir "$LOCK" 2>/dev/null || exit 0
trap 'rmdir "$LOCK"' EXIT

mkdir -p "$EXPORT_DIR/code" "$VAULT_DIR"
echo "[$(date)] Starting sync ($*)" >> "$LOG"

# 1. Claude Code (terminal + desktop share ~/.claude/projects)
if command -v claude-extract &> /dev/null; then
    if [ "$1" = "--all" ]; then N=(--all); else N=(--recent 10); fi
    claude-extract "${N[@]}" --output "$EXPORT_DIR/code" >/dev/null 2>> "$LOG"
else
    echo "[$(date)] claude-extract missing: pip install claude-conversation-extractor" >> "$LOG"
fi

# 2. Codex (CLI + desktop) and Cursor
python3 "$SCRIPT_DIR/agent_chats_to_md.py" --export-dir "$EXPORT_DIR" --vault-dir "$VAULT_DIR" 2>> "$LOG"

# 3. Frontmatter + tags + wikilinks, then into the vault
python3 "$SCRIPT_DIR/claude_to_obsidian.py" --export-dir "$EXPORT_DIR" --vault-dir "$VAULT_DIR" --move >> "$LOG" 2>&1

# 4. Nightly: refresh each bootstrapped repo's graph notes in the vault
if [ "$1" = "--all" ]; then
    for O in "$VAULT_DIR"/graphify/*/.origin; do
        R=$(cat "$O" 2>/dev/null); [ -f "$R/graphify-out/graph.json" ] || continue
        [ "$R/graphify-out/graph.json" -nt "$(dirname "$O")/graph.canvas" ] &&
            python3 "$SCRIPT_DIR/vault_organize.py" graph "$R" "$(basename "$(dirname "$O")")" 2>> "$LOG"
    done
    python3 "$SCRIPT_DIR/vault_organize.py" home 2>> "$LOG"
fi

echo "[$(date)] Sync completed" >> "$LOG"
