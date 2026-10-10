# Coding principles
- Think first: state assumptions; if ambiguous, name the readings and ask; say so when a simpler approach exists.
- Simplicity: minimum code that solves it; no speculative features, single-use abstractions, or handling for impossible cases.
- Surgical: touch only what the request needs; match existing style; mention unrelated dead code, remove only orphans you created.
- Goal-driven: before editing, name the observable acceptance checks and boundary cases; after, verify them and ask whether they could pass while missing a requirement. Report verified outcomes; label anything untested.

# graphify
- Skill: `~/.agents/skills/graphify/SKILL.md` (`/graphify`). If `graphify-out/graph.json` exists and the question is structural ("where is X", "what calls Y"), try `graphify query|path|explain` before broad grep.
- No graph and the task needs real exploration: run `graphify-bootstrap` once (free, idempotent, refuses `$HOME`). Skip it for trivial edits, a known single file, or docs questions. If it fails, say so once and continue with grep/reads.
- The Stop hook (`~/Obsidian Sync/agent_stop_hook.sh`) already runs `graphify update .` each turn; run it by hand only to query right after edits in the same turn.
- One repo = one graph = one vault namespace: `<repo>/graphify-out/`, `<vault>/<repo-id>/`, `<vault>/graphify/<repo-id>/`. `<vault>` = `~/Obsidian Sync/ObsidianVault`; `<repo-id>` = repo name (`<owner>--<repo>` on a clash). Never merge repos or graphs unless asked for that exact merge.
- Chats sync automatically to `<vault>/chats/` (log: `~/Obsidian Sync/claude_obsidian_sync.log`). Don't hand-copy chats.

# Project AGENTS.md
- Each project root (not `$HOME` or third-party clones like `~/Scripts/{ponytail,markitdown,icm,icm-architect}`) needs an `AGENTS.md` (Codex/Cursor) consistent with its `CLAUDE.md` (Claude Code), under ~60 lines, that routes: purpose + architecture, top-level dirs, conventions, safe vs off-limits files (generated, vendored, secrets, lockfiles, `graphify-out/`), preferred libraries, run/build/test.
- Missing or graphify-only: write it from what the repo actually contains (unknowns = `TODO`), above the graphify section. Never overwrite existing content; no task progress.

# Reading and tool output
- On-demand vault recall: when a task needs past project context missing here, search `<vault>/<repo-id>/` for relevant terms with `rg -n -i -g '*.md'`, then read only matching notes. Search `<vault>/knowledge/` separately for reusable cross-project guidance. Do not scan on every prompt or load chat archives; if nothing relevant matches, use current code and say the note was not found.
- Locate with summaries (graph, signatures, headings, schemas), then read the implementation, callers, and tests the change depends on. Correctness needs the real code.
- Don't re-read content already in context unless it may have changed (edits, file-writing tools, git checkout/pull); then re-read only the relevant range.
- Never read raw data or real secrets (`.env`, credential `config.json`); use schemas and example configs.
- Keep output small: targeted `grep -n`, ranges, quiet flags. For long test/build/log output, save the full log to a file, report the summary (counts, failures, first error), and grep the file for details. Never cut off the failing lines.
- Prefer a short deterministic script over many manual steps for mechanical processing.
- Use local exact search for names/paths. If a remote search fails from quota, auth, or connectivity, report once and fall back locally; retry only after conditions change. Never upload private files for search without authorization.

# Documents and pasted material
- Files (.pdf/.docx/.doc/.pptx/.xlsx/.xls/.epub/.msg) the task needs: convert with markitdown to a sibling `.md` without asking, then tell the user what was converted and where. The gain is selective reading, not automatic savings. Skip, and say so, for 1-2 page docs, scanned PDFs, or layout-heavy files.
- Pasted text is already in context; saving it shrinks nothing. Only reusable reference material (~800+ words) that later sessions need gets a brief in `<vault>/<repo-id>/briefs/`, keeping every requirement, number, name, path, and error text exact, at whatever length that takes.

# Context and sessions
- Unrelated next task: suggest a new chat (`/new`). Same work with heavy or stale context: suggest `/compact` at a natural break. No fixed turn or percentage triggers; check `/status`.
- Write the handoff note before suggesting a reset. A note doesn't remove history; only `/compact` or a new chat changes what is in context.
- Caching: cached input is cheaper but still fills the context window and is re-sent each turn. Compaction replaces history with a summary; the unchanged instruction prefix can stay cached.
- Handoff note: `<vault>/<repo-id>/status.md`, overwritten, 5-15 lines: branch/worktree, done, verification + result, unresolved, next action. Concurrent tasks/worktrees: one each in `<vault>/<repo-id>/handoffs/<branch-or-worktree>.md`. New chats read the note, not old transcripts.
- At each finished logical unit, propose a checkpoint commit. Commit only on the user's yes; never push unless asked.

# Delegation and models
- Delegate only when it keeps large output out of the main context or runs independent work in parallel; sub-agents start cold. Keep judgment calls and final decisions here.
- A cheaper model saves only if it succeeds without retries: smaller models for well-specified bulk mechanical work with an easy check; debugging, design, and review on a capable model. If the model is clearly mismatched for what's coming, suggest `/model`.

# On-demand workflows (steps/templates: `~/Scripts/agent-workflow-reference.md`; read only when doing one)
- **ICM:** `icm-architect` skill for new project structure or "map this folder/repo"; `icm` (`~/Scripts/icm`) holds the spec. Create workspaces in the user's project, never in the `~/Scripts/icm*` clones.
- **System map:** suggest (never auto-create) when I keep hunting for where things live or changes ripple widely; repo size is a hint, not proof. Ask first.
- **ADR:** when the user picks between real alternatives (architecture, library, data model, deliberate unusual pattern), write `<vault>/<repo-id>/decisions/ADR-NNNN-<slug>.md` and say so. Before changing an area, list `decisions/` and open only a match. Supersede; never delete or silently refactor away.
- **Harvest:** only on "save this"/"harvest": one atomic note in `<vault>/knowledge/`, updating a match instead of duplicating. No secrets or personal data.
