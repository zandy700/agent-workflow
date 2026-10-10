#!/bin/bash
# Stop hook for Codex and Cursor (Claude Code has the same two commands inline in settings.json).
# Runs detached so the agent never waits on it.
D="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${CURSOR_PROJECT_DIR:-$PWD}"
cat > /dev/null   # drain the hook's stdin payload
( "$D/sync_claude_obsidian.sh" >> "$D/claude_obsidian_sync.log" 2>&1
  [ "$PROJECT_DIR" != "$HOME" ] && [ -f "$PROJECT_DIR/graphify-out/graph.json" ] &&
    (cd "$PROJECT_DIR" && graphify update .) >> "$HOME/.cache/graphify-stop-hook.log" 2>&1 ) &
exit 0
