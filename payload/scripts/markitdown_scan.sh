#!/bin/bash
# Scan a directory for markitdown-convertible documents that have no .md sibling yet.
# Used by the SessionStart hook in ~/.claude/settings.json; also runnable by hand:
#   ~/Scripts/markitdown_scan.sh [dir]
dir="${1:-$PWD}"
# A session started in $HOME would list Downloads/Desktop noise; scan it only when asked by hand.
[ -z "$1" ] && [ "$dir" = "$HOME" ] && exit 0
cd "$dir" 2>/dev/null || exit 0

found=$(find . -maxdepth 3 \
  \( -name .git -o -name node_modules -o -name Library -o -name .venv -o -name venv \
     -o -name dist -o -name build -o -name .Trash -o -name .cache \) -prune -o \
  -type f \( -iname '*.pdf' -o -iname '*.docx' -o -iname '*.doc' -o -iname '*.pptx' \
     -o -iname '*.xlsx' -o -iname '*.xls' -o -iname '*.epub' -o -iname '*.msg' \) -print 2>/dev/null |
  while IFS= read -r f; do [ -e "${f%.*}.md" ] || printf '%s\n' "$f"; done)

[ -z "$found" ] && exit 0
n=$(printf '%s\n' "$found" | wc -l | tr -d ' ')

echo "markitdown scan of $dir — $n convertible document(s) with no .md sibling:"
lim=10; [ -n "$1" ] && lim=$n   # hook run: first 10; run by hand with a dir: all
printf '%s\n' "$found" | head -"$lim"
[ "$n" -gt "$lim" ] && echo "... and $((n - lim)) more (full list: ~/Scripts/markitdown_scan.sh <dir>)"
echo "Convert one only when the task needs it (global rule: Documents)."
