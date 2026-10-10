#!/bin/bash
# Stop hook for Codex and Cursor (Claude Code has the same two commands inline in settings.json).
# Runs detached so the agent never waits on it.
D="$(cd "$(dirname "$0")" && pwd)"
cat > /dev/null   # drain the hook's stdin payload
( "$D/sync_claude_obsidian.sh" >> "$D/claude_obsidian_sync.log" 2>&1
  [ "$PWD" != "$HOME" ] && [ -f graphify-out/graph.json ] &&
    graphify update . >> "$HOME/.cache/graphify-stop-hook.log" 2>&1 ) &
exit 0
