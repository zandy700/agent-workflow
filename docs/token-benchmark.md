# Token benchmark: full vs. lean workflow

## Original run (2026-10-10)

Claude Code 2.1.296, reported model `claude-haiku-5-5`, three sessions per condition. Each session started from the same 364-line Python order library, then received five identical prompts: fix a coupon bug, migrate money to Decimal, add refunds, add CSV reporting, add tests. Both conditions used the same tool permissions. Nine independent checks ran after each prompt.

| Mean per complete session | Vanilla | Previous full workflow |
|---|---:|---:|
| Total tokens, including cache reads | 923,168 | 1,604,721 |
| Output tokens | 42,723 | 44,362 |
| Final checks | 9/9 | 9/9 |

The full configuration used 73.8% more tokens. It included global rules, project documentation, Ponytail 4.9.0 in full mode, Graphify project hooks and a prebuilt graph, and the Graphify/ICM skill descriptions. No skill calls or Graphify queries were recorded. Prompts 2-5 resumed the same session in new CLI processes; Ponytail injected its instructions again on each resume. This is a limitation relative to a continuously open interactive process.

## Revision

- Reduce global rules to a shared short core for Claude, Codex and Cursor; detailed procedures stay in the reference, read only when needed.
- Default new Ponytail configurations to off; preserve existing explicit preferences. Skills remain available for intentional use.
- Do not bootstrap a graph for small, directly readable tasks. Existing graphs and optional bootstrap remain available.
- Group independent reads and related edits, inspect focused output, and avoid unnecessary repeat checks. Keep validation and truthful test reporting.

The new smoke test measured 10,919 processed input tokens for vanilla and 13,797 for the revised setup. Startup overhead is 2,878 tokens. The earlier component smoke test measured 6,715 tokens of overhead. This is a startup comparison, not proof of an end-to-end saving.

## Rerun method

Fresh isolated config and fixture per session, same five prompts and grader, model pinned to `claude-haiku-5-5`, same CLI version, tools and permissions. Three runs each, order baseline/workflow/workflow/baseline/baseline/workflow. Optional skills and Ponytail 4.9.0 remain installed in the workflow condition, with `PONYTAIL_DEFAULT_MODE=off`. The workflow retains its short project documentation. Graph setup is skipped because the fixture is directly readable. Chat sync is excluded in both measured workflow versions to avoid writing personal transcripts into the real vault. This does not test every plugin enabled on a user's machine.

Use the final `modelUsage` cumulative counters once per session. Per-prompt totals are differences between successive cumulative counters; never sum the cumulative totals. Preserve input, cache write, cache read and output separately. Provider cost estimates are not subscription charges. Stop on an error rather than silently retrying failed tasks. Include all completed runs in the report, even if the result is unfavorable.

## Completed rerun (three sessions per condition)

| Mean per complete session | Fresh vanilla | Revised workflow |
|---|---:|---:|
| Total tokens, including cache reads | 1,069,724 | 1,021,720 |
| Output tokens | 41,430 | 42,224 |
| Estimated API list-price cost | $0.043 | $0.044 |
| Final independent checks | 9/9 | 9/9 |

The revised workflow used **4.5% fewer total tokens**, while estimated cost was **2.5% higher**. Cache reads fell, but cache writes and output increased. This does not establish cost savings. All six chats passed all nine final checks. No full Ponytail rules were re-injected in any of the 15 workflow prompts; the 30 prompt results were audited against their raw cumulative counters.

The ranges overlap substantially: vanilla 814,177–1,290,517 tokens; revised workflow 809,989–1,296,145. Three repetitions of one task are too few to establish a reliable general advantage. The new workflow mean is 36.3% below the old full-workflow mean, but that is a historical comparison, not a simultaneous full-vs-lean randomized experiment.

[Per-run counters](token-benchmark-results.json) are included without prompts, transcripts or credentials. Raw logs, runner, fixture and independent grader remain in `~/Scripts/agent-workflow-benchmarks/2026-10-10-lean-workflow/`; the original results remain in `2026-10-10-multiprompt/`. The first sandbox-restricted smoke attempt returned no usage result and was terminated; successful smoke calls are separate from the coding totals.


## Limits

One small fixture and one model cannot establish savings for large projects, memory across fresh chats, or other clients. Correctness here means the nine checked behaviors, not a comprehensive code-quality or safety evaluation. The earlier 49% result counted reply characters; it is not a measured reduction in total tokens.
