# Agent workflow reference (on demand)

Read only the section you need. Global rules that point here: `~/.claude/CLAUDE.md` (Claude Code) and `~/.codex/AGENTS.md` (Codex). `<vault>` = `~/Obsidian Sync/ObsidianVault`.

## New-project graphify check
Run before substantive work in a repo that has no graph (skip for trivial edits):
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
