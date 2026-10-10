# How the workflow works

The idea behind every piece: **keep what loads into every turn small, and fetch everything else only when a task needs it.** Each turn re-sends the whole conversation, so a line that is always loaded costs on every turn, and a file that is read only on demand costs once.

These diagrams show where tokens are avoided. They are not measurements; the package makes no claim of a measured saving on your machine.

## 1. Always loaded vs on demand

```mermaid
flowchart LR
    subgraph always["Loaded every session — kept short"]
        R["Global rules<br/>~/.claude/CLAUDE.md<br/>~/.codex/AGENTS.md<br/>Cursor User Rules"]
        P["Project CLAUDE.md / AGENTS.md<br/>under ~60 lines, routes only"]
        PT["Ponytail ruleset<br/>smallest working change"]
        S["Session-start doc scan<br/>at most 10 file names"]
    end
    subgraph demand["Read only when a task needs it"]
        REF["agent-workflow-reference.md<br/>handoff, ADR, harvest templates"]
        G["graphify query / path / explain"]
        V["Vault notes: repo notebook<br/>and knowledge/"]
        D["Documents converted<br/>by MarkItDown"]
        C["Implementation, callers, tests"]
    end
    always -->|"points to"| demand
```

The rule files hold routing, not procedures. Templates and step-by-step workflows live in `agent-workflow-reference.md`, which the agent opens only when it is doing one of them.

## 2. One task, start to finish

```mermaid
flowchart TD
    T([Task]) --> H{"Handoff note<br/>for this repo?"}
    H -->|yes| HN["Read status.md<br/>not old transcripts"]
    H -->|no| L
    HN --> L{"graphify-out/graph.json<br/>exists?"}
    L -->|yes| GQ["graphify query / path<br/>to locate code"]
    L -->|no| GR["Targeted grep -n<br/>signatures, headings"]
    GQ --> RD["Read only the code the change<br/>depends on: implementation,<br/>callers, tests"]
    GR --> RD
    RD --> AC["Name the acceptance checks<br/>before editing"]
    AC --> E["Edit: Ponytail ladder<br/>reuse, stdlib, shortest diff"]
    E --> RUN["Run checks<br/>long output saved to a log file,<br/>only summary + failing lines shown"]
    RUN -->|fail| RD
    RUN -->|pass| REP(["Report verified results<br/>label anything untested"])
```

Locating with a graph or a targeted search replaces reading whole directories. Long test and build output goes to a file, and only the summary and the failing lines enter the conversation.

## 3. After every turn: chats and graph stay current

```mermaid
flowchart TD
    TURN([Agent turn ends]) --> STOP["Stop hook<br/>runs detached, agent never waits"]
    STOP --> SYNC["sync_claude_obsidian.sh"]
    SYNC --> X1["claude-extract<br/>Claude Code chats"]
    SYNC --> X2["agent_chats_to_md.py<br/>Codex and Cursor chats"]
    X1 --> CO["claude_to_obsidian.py<br/>frontmatter, tags, wikilinks"]
    X2 --> CO
    CO --> VC[("Vault<br/>chats/tool/YYYY-MM/")]
    STOP --> GU{"Project has<br/>a graph?"}
    GU -->|yes| GUP["graphify update .<br/>AST only, no model calls"]
    GU -->|no| SKIP([skip])
    NIGHT(["launchd, nightly 22:00"]) -->|"--all"| SYNC
    SYNC -->|"--all only"| VO["vault_organize.py<br/>refresh each repo's graph notes"]
```

None of this runs inside the agent's context. The hooks spend no model tokens; they keep the graph and the vault ready so later sessions can look things up instead of re-reading code or transcripts.

## 4. Recalling past context

```mermaid
flowchart TD
    Q([Task needs a past decision<br/>or context missing from the repo]) --> S1["rg -n -i in vault/repo-id/<br/>this repo's notebook only"]
    Q --> S2["rg -n -i in vault/knowledge/<br/>cross-project guidance"]
    S1 --> M{"Matches?"}
    S2 --> M
    M -->|yes| READ["Read only the matching notes"]
    M -->|no| CODE["Use current code<br/>say the note was not found"]
    NO["Chat archives and the whole vault<br/>are never loaded by default"]
```

One repo maps to one graph and one vault namespace, so a search never pulls in another project's notes.

## 5. Keeping context small over a long session

```mermaid
flowchart LR
    W([Work]) --> U{"Unit of work<br/>finished?"}
    U -->|yes| CP["Propose a checkpoint commit"]
    U -->|no| W
    CP --> K{"Context heavy<br/>or next task unrelated?"}
    K -->|no| W
    K -->|yes| HO["Write handoff note<br/>vault/repo-id/status.md<br/>5-15 lines"]
    HO --> RS["/compact or /clear<br/>or a new chat"]
    RS --> NEW(["New session reads the note,<br/>not the transcript"])

    DEL{"Delegate to a subagent?"} -->|"independent work, or<br/>large output to keep out"| SA["Subagent<br/>cheaper model only for<br/>well-specified mechanical work"]
    DEL -->|"small or dependent steps"| SELF["Do it inline"]
```

A handoff note of 5 to 15 lines replaces carrying a whole transcript forward. Subagents start cold, so they are used only when they keep large output out of the main context or run independent work in parallel.
