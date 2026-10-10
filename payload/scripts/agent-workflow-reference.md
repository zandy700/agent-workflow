# Agent workflow reference (on demand)

Read only the section you need. Global rules that point here: `~/.claude/CLAUDE.md` (Claude Code) and `~/.codex/AGENTS.md` (Codex). `<vault>` = `~/Obsidian Sync/ObsidianVault`.

## Graphify
Use an existing graph for unfamiliar structural questions. Bootstrap only when repeated exploration warrants it or the user requests it; skip small tasks whose relevant files can be read directly. No arbitrary repository-size cutoff. For setup:
1. `graphify-bootstrap` (refuses `$HOME`).
2. `graphify-out/graph.json` exists and `graphify query "<one question about the repo>"` returns nodes.
3. `graphify-out/.repo-id` exists, and so does `<vault>/graphify/<repo-id>/`.
If a check fails, report it and continue with grep/reads unless the task needs the graph. A near-empty graph on a docs-only repo is expected.

## Handoff note
`<vault>/<repo-id>/status.md` (sequential work) or `<vault>/<repo-id>/handoffs/<branch-or-worktree>.md` (concurrent). Overwrite in place.
```
# <repo-id> status (YYYY-MM-DD)
Branch/worktree: <name> @ <short sha>, clean|dirty
Done: <1-3 lines>
Verified: <command> -> <result>  (or "not run")
Unresolved: <bugs, open questions, exact error text>
Next: <one concrete action>
```

## ADR
`<vault>/<repo-id>/decisions/ADR-NNNN-<slug>.md`, next free number, 10-20 lines:
```
# ADR-NNNN: <title>
Date: YYYY-MM-DD | Status: accepted (or: superseded by ADR-NNNN)
Decision: ...
Alternatives considered: ...
Rationale: ...
#adr #<repo-id>
```
Not for trivial or reversible choices. To change one, write a new ADR and mark the old one superseded.

## Knowledge harvest
`<vault>/knowledge/<slug>.md`: one concept, ~10-40 lines, tags, `[[links]]` to related notes. Search `knowledge/` first and update a matching note.

## Reference brief
`<vault>/<repo-id>/briefs/<date>-<slug>.md`. Keep requirements, numbers, names, paths, and error text verbatim; drop repetition and examples. Note the source (file path or "pasted <date>").

## System map
Follow `icm-architect` -> `references/system-map.md`: inventory + proposed tree, wait for a yes, catalog, then cards verified against source with `path:line`, verified date + commit. Re-check after big structural changes.

## Measuring a workflow change
Run usage-consuming model benchmarks only with an explicit user budget. Use a small pilot before changing defaults. Compare the same tasks from the same starting state in fresh isolated sessions; hold model, effort, tools, and permissions fixed for workflow comparisons. Compare models separately. Run both conditions at least twice; expand to 3-5 representative tasks if the pilot is promising.
- Record provider/client-reported input, output, cache-read, and cache-write usage when exposed. Record the source of each metric. Missing counters are unavailable, never zero; character counts are estimates only.
- Startup/end context occupancy is not cumulative usage. `/context` or `/status` availability varies by client; `/usage` may report account limits rather than per-task token totals. Use session usage records when available, without dumping prompts or secrets.
- Include conversion requests (Promptbox), failed attempts, subagents, retries, elapsed time, tool calls, and user corrections. Compare correctness with the same independent checks.
- Report cost separately from tokens: cache discounts, model prices, and subscription quotas differ. Do not equate list-price estimates with money saved on a subscription.
- Do not overwrite live global config for a benchmark. Use supported isolated config, preserve work, and report setup limits rather than inventing measurements.
- A shorter instruction file proves only less source text; verify fresh-session loading and end-to-end results before claiming token savings.

## Promptbox and prompt preparation
Use the original prompt directly when it is already clear. Structure is for reorganizing messy requirements; Build intentionally expands a vague idea. Review negations, uncertainty, permissions, exact values, code, and proposed assumptions before sending. A literal-detail pass cannot prove semantic fidelity. Never automatically convert every message or attach old transcripts.

## Search failures and handoffs
Prefer local exact searches for names/paths and available local graphs for relationships. Use semantic/remote retrieval only when it helps and the data is allowed there. On an unavailable service, quota/auth error, or network failure, report once and use local search/reads; retry only if conditions change.
Keep `status.md` to 5-15 lines of current state. If it has become a session log, preserve that existing material in a referenced project note and replace status with a concise handoff. Do not copy or automatically load chat archives.

## Project instructions
At an actual project root, keep factual CLAUDE.md and AGENTS.md consistent, under about 60 lines: purpose/architecture, directories, conventions, safe/off-limits files (generated, vendored, secrets, lockfiles, graphify-out), preferred libraries, run/build/test commands. If missing or graphify-only, add verified facts above the graphify section; unknowns are TODO. Preserve existing content, omit task progress. Never do this in $HOME or third-party tool clones.

## Documents and briefs
Convert task-relevant PDF/Office/EPUB/MSG documents with ~/Scripts/markitdown to sibling .md files and report the path; skip 1-2 page, scanned, or layout-heavy files with a reason. No confirmation needed. Pasted material is already in context: save only reusable references (about 800+ words) needed in later sessions as a brief, preserving every requirement, number, name, path and error exactly.

## Context, caching and recall
Search only the current repo's vault namespace for missing prior context; search knowledge/ separately for reusable guidance. Read matching notes, not chat archives. If no note matches, use current code and say so.
Before reset, overwrite status.md (or a per-worktree handoff for concurrent work), then suggest a new chat for unrelated work or compaction for heavy/stale related context. Check the client's context indicator, not fixed turn counts. Claude uses /context and /compact; Codex uses /status and /compact. Preserve goal/constraints, decisions and why, changed files, verification results, exact unresolved errors and next action. Cached tokens still occupy context; cache discounts, context occupancy and cumulative usage are different metrics. Do not claim a note, conversion, or shorter rules automatically saves total tokens.
Repo ID is graphify-out/.repo-id when present, otherwise repo name; use owner--repo on a clash. Project notes live in <vault>/<repo-id>/ and graph notes in <vault>/graphify/<repo-id>/. Never merge namespaces without explicit authorization.

## ICM
Use icm-architect for new project structure or mapping a folder; icm in ~/Scripts/icm is the spec and examples. Create workspaces in the user's project, never in ~/Scripts/icm or ~/Scripts/icm-architect. System maps require the user's approval before creation. Read only the skill needed for the current request.

## Decisions
Before changing an area, list decisions/ and read matching ADRs only. When the user chooses between real architecture, library or data-model alternatives, write the ADR above and report its path. Supersede old decisions; never silently remove them. Harvest only when asked, one atomic note in knowledge/, updating an existing match; no secrets or personal data.

## Delegation and models
Delegate when independent work can run in parallel or keep large output out of the main context; subagents start cold. Keep judgment and final decisions with the main agent. Smaller models suit mechanical tasks with clear checks; use capable models for debugging/design/review. Suggest /model if mismatched. Include retries and all subagent usage in measurements.

## Ponytail
Optional; the core already covers minimal changes and verification. New installs default Ponytail to off using its supported config. Activate explicitly with /ponytail lite|full when useful. Existing explicit preferences are preserved. Full mode injects rules at session start/resume in the tested version; include that cost in measurements. To opt out of automatic activation, set defaultMode to off in Ponytail's config (XDG_CONFIG_HOME/ponytail/config.json if set, otherwise ~/.config/ponytail/config.json on macOS/Linux or APPDATA/ponytail/config.json on Windows). Preserve other keys. This does not remove skill descriptions or other plugins. Restart the chat to measure the new default.

## Optional plugin startup guidance

Other installed plugins can add instructions independently of this workflow. In the inspected versions, mgrep 0.0.0 and Superpowers 6.4.1 inject startup guidance without a separate switch to suppress only that guidance. For a lean default, disable their plugin loading and enable them explicitly when needed. The workflow installer preserves these third-party plugin preferences.

For Claude Code, run these commands only for plugins you have installed:

```sh
claude plugin disable mgrep@Mixedbread-Grep --scope user
claude plugin disable superpowers@claude-plugins-official --scope user
```

For Codex, change `enabled` to `false` in the matching existing sections of `~/.codex/config.toml` (under your user profile on Windows), preserving other settings:

```toml
[plugins."mgrep@Mixedbread-Grep"]
enabled = false

[plugins."superpowers@claude-plugins-official"]
enabled = false
```

Start a new chat after changing these settings. Both plugins remain installed, but their plugin skills and hooks are disabled. A separately installed `mgrep` CLI remains available. To restore plugin loading, use `claude plugin enable <plugin-id> --scope user` or set the matching Codex `enabled` value to `true`; startup guidance will return too. Existing chats keep previously loaded instructions.

These settings were checked locally. A fresh client session and the additional token impact were not measured. The benchmark excluded these plugins, so its results do not quantify this change.
