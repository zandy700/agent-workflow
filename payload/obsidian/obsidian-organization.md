---
title: Obsidian organization
tags: [obsidian, organization]
created: 2026-10-09
updated: 2026-10-09
status: active
type: reference
---

# Obsidian organization

Back to [[Home]].

## The PARA Method

A common way to organize a vault into four top-level folders:

- **Projects:** Active efforts with a specific deadline.
- **Areas:** Ongoing spheres of responsibility (e.g., health, finances).
- **Resources:** Reference material and topics of general interest.
- **Archives:** Inactive or completed items kept for the future.

This workflow's vault uses repository-specific notebooks and generated chat and graph folders, not PARA top-level folders.
For future projects, use these categories for handwritten notes within that project's notebook when useful. Keep each repository's notes in its own notebook, and leave generated chat and graph folders in place.

## Bidirectional linking

Using double brackets (`[[Note Name]]`) connects notes to each other, building a visual **Graph View** of how thoughts relate across different projects and time periods.
Link related handwritten notes and each project's Home index so they can be found from either direction.

## On-demand agent retrieval

For coding tasks, use the current repository and its short handoff first. When a past decision or other project context is needed but missing, search that repository's `<repo-id>/` notebook with `rg -n -i -g '*.md'` and read only relevant matches. Search `knowledge/` separately for guidance shared across projects. Do not load chat archives or search the whole vault on every prompt; if no note matches, rely on current code and say the note was not found.

This borrows selective, on-demand retrieval from [obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) without installing its hooks, scheduled agents, vault layout, or semantic index. Token savings and coding quality from this rule have not been measured. The Claude Code and Codex rules are installed to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`; the Cursor copy is `payload/cursor/USER_RULES.md` in this package, pasted into Cursor User Rules.
