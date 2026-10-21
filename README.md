<h1 align="center">Agent Workflow</h1>

<p align="center">
  <a href="#quickstart"><img src="https://img.shields.io/badge/Quick_Start-1_command-blue?style=for-the-badge" alt="Quick Start"></a>
  <a href="#setup"><img src="https://img.shields.io/badge/Setup-Automatic-7c5cff?style=for-the-badge" alt="Setup Guide"></a>
  <a href="#results"><img src="https://img.shields.io/badge/Test_Results-Measured-blue?style=for-the-badge" alt="Test Results"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-red?style=for-the-badge" alt="中文 README"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-macOS_%7C_Windows-lightgrey" alt="macOS and Windows">
  <img src="https://img.shields.io/badge/Claude_Code-supported-D97757" alt="Claude Code">
  <img src="https://img.shields.io/badge/Codex-supported-412991" alt="Codex">
  <img src="https://img.shields.io/badge/Cursor-supported-000000" alt="Cursor">
  <img src="https://img.shields.io/badge/notes-Obsidian-7C3AED?logo=obsidian&logoColor=white" alt="Obsidian">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/background_hooks-0_AI_tokens-success" alt="Hooks use no AI tokens">
</p>

<h3 align="center">Your AI agent forgets everything when the chat ends.<br>This gives it a notebook, and a code of conduct.</h3>

<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">简体中文</a>
</p>

A ready-made setup for **Claude Code, Codex, and Cursor** on **Mac and Windows**. It keeps the instructions agents load short, steers them toward small changes, makes them report honestly, and saves every chat to Obsidian so the next chat can pick up where the last one left off.

<a id="contents"></a>
## 🧭 Contents

| **Start here** | **Use it** | **Reference** |
|---|---|---|
| [One-command setup](#quickstart) | [Day-to-day use](#daily) | [Setup options](docs/setup-options.md) |
| [What gets installed](#setup) | [Included tools](#extras) | [What’s in this repo](#repo) |
| [Test results](#results) | [ICM](#icm) | [Checks](#checks) |
| [Problems it solves](#problems) | [Troubleshooting](#troubleshooting) | [Credits](#credits) |

---

<a id="problems"></a>
## 🤔 Problems it solves

| Without this workflow | With this workflow |
|---|---|
| ❌ Every new chat starts from zero, so you re-explain the project. | ✅ The agent reads a 5–15 line handoff note and carries on. |
| ❌ Long chats get slower and pricier as the whole history is re-sent. | ✅ Short rules and short replies keep each message light. |
| ❌ The agent claims tests passed when nothing was run. | ✅ The agent must report what it verified and label what it didn't. |
| ❌ The agent adds layers and libraries you didn't ask for. | ✅ The core rules call for the smallest complete change. |
| ❌ Why you made a decision is buried in some old chat. | ✅ Every chat is in Obsidian; ask *"why did we do X?"* |
| ❌ The agent reads whole folders to find one function. | ✅ Optional code map (Graphify) lets it look things up instead. |
| ❌ Each app needs its own setup and its own rules. | ✅ Claude Code, Codex, and Cursor all follow the same rules. |
| ❌ Saving chats by hand is easy to forget. | ✅ Chats save in the background after each message, using no AI tokens. |

<a id="results"></a>
## 📊 Test results

The original 4-step cache pilot measured **characters**, not tokens: replies were about 49% shorter. That does not establish a reduction in total token usage.

A later test used real Claude Code counters: a 364-line Python shop, five successive coding prompts, three Haiku sessions per condition. The previous full workflow used **73.8% more total tokens** (1,604,721 vs. 923,168 per session), with **9/9 final checks in both conditions**. Most of the increase was cached input. Estimated list-price cost rose 24.4%; this is not a subscription bill.

**Revised setup, fresh rerun:** 4.5% fewer total tokens on average, all 9/9 final checks passed; estimated API cost was 2.5% higher. Three runs per condition on one small task, with substantial variation—this is not a general savings claim.

The revised defaults shorten the core rules, load detailed guidance only when needed, keep Ponytail opt-in, and skip Graphify setup for directly readable tasks. Skills and chat sync remain available. See [the benchmark method and revision results](docs/token-benchmark.md). Savings depend on the task; no universal percentage is promised.

<sub>[↑ Back to top](#contents)</sub>

---

<a id="quickstart"></a>
## 🚀 One-command setup

You need **Python 3.10–3.14**, an internet connection, and at least one coding app installed and signed in. No Git checkout, manual pip installs, skill links, or Cursor rule pasting are needed.

**Mac — paste into Terminal:**

```bash
python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

**Windows — paste into PowerShell:**

```powershell
py -3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

If Python is missing, install it from [python.org](https://www.python.org/downloads/) first. On Windows, `python` can replace `py -3` if you installed Python without the launcher.

**Already have this repo?** Run `python3 setup.py --install` (Windows: `py -3 setup.py --install`). Run it without `--install` for a preview that makes no changes or network calls. The downloadable bootstrap also accepts `--preview`.

<a id="setup"></a>
## What the command sets up

| Included | What happens automatically |
|---|---|
| Shared rules | Claude Code and Codex receive a managed block in their global instructions. Cursor loads the same rules through a session-start hook. |
| Chat history | Hooks save local Claude Code, Codex, and Cursor transcripts to your vault. Existing chats get a first sync. |
| Python tools | A private environment installs pinned versions of the chat exporter, Graphify, and MarkItDown. Your system Python packages stay separate. |
| ICM | Verified snapshots of the templates and `icm-architect` are downloaded, and the skills are connected to all three apps. |
| Vault | Creates `~/Obsidian Sync/ObsidianVault`, including its Home note. Obsidian is an optional viewer; saving notes works without it. |

Run the same command again to repair or update the managed setup. Existing custom global instructions, unrelated hooks, notes, and plugin preferences are preserved. Replaced files are backed up under `~/Scripts/agent-workflow-backups/`. Existing ICM folders and architect skills are kept, including local changes.

<a id="app-claude"></a>
<a id="app-codex"></a>
<a id="app-cursor"></a>
### Finish inside your apps

- Start a **new chat** so the app loads the rules. Approve the workflow hooks if prompted; in Codex, review `/hooks`. The installer does not grant trust for you.
- To view the notes, open `~/Obsidian Sync/ObsidianVault` using **Open folder as vault** in Obsidian. The folder name does not require the paid Obsidian Sync service.

Cursor's [documented sessionStart hook](https://cursor.com/docs/hooks#sessionstart) injects the rules automatically. Existing manually pasted workflow rules can be removed from Cursor's User Rules to avoid duplication. This setup targets local coding apps; cloud agents need their own environment.

Ponytail and nightly scheduled sync remain optional. See [setup options](docs/setup-options.md) if you want them. Hooks already sync chats after agent turns.

**Windows:** the generated configuration is covered by tests on macOS; a real Windows installation has not yet been verified.

---

<a id="daily"></a>
## 💬 Day-to-day use

You mostly just talk to the agent:

| When | Say this to the agent |
|---|---|
| Before closing a long chat | *"Write the handoff note for this repo."* |
| Starting a new chat on the same project | *"Read the handoff note and continue."* |
| A separate task comes up that needs none of this chat's context | Start a new chat for that task, even in the same project. |
| You need an old decision | *"Check the notes: why did we do X?"* |
| You picked between real options | *"Write an ADR for this decision."* |
| You learned something worth keeping | *"Save this."* |
| You want a step-by-step structure for a process, or a map of a messy folder | *"/icm-architect map this repo."* (needs [ICM](#extras)) |

The handoff note is a 5–15 line summary of what's done, what's broken, and what's next. The agent searches the vault only for what you ask about; it never loads all of it.

**Ponytail settings** (type in the chat box):

| Command | What it does |
|---|---|
| `/ponytail lite` | Gentler |
| `/ponytail full` | Full guidance for this chat |
| `/ponytail ultra` | Strictest |
| `stop ponytail` | Turn it off |

To remove it completely, see [Ponytail's uninstall steps](https://github.com/DietrichGebert/ponytail#uninstall).

<a id="extras"></a>
## 🧩 Included tools

The full setup installs these tools. They run only when needed; installing Graphify does not create a project map.

- **Graphify:** run `~/Scripts/graphify-bootstrap /path/to/project` when you want a code map. On Windows use `& "$HOME/Scripts/graphify-bootstrap.cmd" C:\path\to\project`. Each repo keeps its own graph and vault namespace.
- **MarkItDown:** use `~/Scripts/markitdown document.pdf` (Windows: `& "$HOME/Scripts/markitdown.cmd" document.pdf`).

<a id="icm"></a>
### ICM

`/icm` supplies the method and reusable workspaces. `/icm-architect` designs new structures or maps an existing folder. Ask *"/icm-architect map this repo"* in a new chat. Maps still require your approval; new workspaces belong in your project.

The installer downloads pinned upstream snapshots into `~/Scripts/icm` and `~/Scripts/icm-architect`, checks their SHA-256 hashes, and copies architect skills into Claude Code, Codex, and Cursor. Existing folders and skills are preserved. Versions and sources are recorded in [bundle.json](bundle.json).

ICM is by RinDig. The `/icm` integration and workflow routing are by [zandy700](https://github.com/zandy700).

---

<a id="troubleshooting"></a>
## 🩺 Troubleshooting

| Problem | What to try |
|---|---|
| No chats in Obsidian | Read the last lines of the log. Mac: `tail -20 "$HOME/Obsidian Sync/claude_obsidian_sync.log"` · Windows: `Get-Content "$HOME/Obsidian Sync/claude_obsidian_sync.log" -Tail 20` |
| Claude Code chats missing | Check `~/Scripts/agent-workflow-setup.log`, then rerun the setup command. |
| Codex chats missing | Did you approve the hook in `/hooks`? See [Codex](#app-codex) |
| Agent ignores the rules | Start a new chat; rules only load when a chat starts |
| Nightly sync not running | Mac: `launchctl print "gui/$(id -u)/local.agent-workflow.obsidian-sync"` · Windows: `Get-ScheduledTask agent-workflow-obsidian-sync` |
| Windows: typing `python` opens the Microsoft Store | Reinstall Python from [python.org](https://www.python.org/downloads/) and tick "Add python.exe to PATH", then run the installer again |
| You moved or upgraded Python on Windows | Rerun the full setup command to check the runtime and regenerate hooks |

<sub>[↑ Back to top](#contents)</sub>

---

<a id="repo"></a>
## 📁 What's in this repo

```
agent-workflow/
├── README.md            this guide (English)
├── README.zh-CN.md      this guide (简体中文)
├── LICENSE              MIT license
├── bootstrap.py         downloads and launches setup
├── setup.py             full setup: tools, ICM, hooks, and sync
├── bundle.json          pinned tool versions and ICM checksums
├── install.py           core file installer
├── payload/             everything the installer copies
│   ├── claude/          rules for Claude Code
│   ├── codex/           rules for Codex
│   ├── cursor/          rules and automatic session-start loader
│   ├── obsidian/        chat-saving and vault scripts
│   ├── skills/          the /icm skill
│   └── scripts/         on-demand reference file, document scan
└── docs/                deeper guides and the images used here
```

<a id="reading"></a>
## 📚 Further reading

- [How it works](docs/how-it-works.md): diagrams of what loads when, and where tokens are saved
- [Using the Obsidian notes](docs/obsidian-notes-guide.md): handoffs, decision records, saved lessons, reference briefs

<a id="checks"></a>
## 🧪 Checks (no AI calls)

These check the scripts for errors and run the installer against a throwaway folder, without calling any AI model:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile bootstrap.py setup.py install.py payload/cursor/*.py payload/obsidian/*.py payload/scripts/*.py
```

The suite covers generated Windows configuration, repeat installs, custom settings, download integrity, and a bootstrap preview. This is separate from testing on a real Windows PC.

<a id="credits"></a>
## 🙏 Credits

This workflow installs tools from their upstream sources. ICM snapshots retain their upstream licenses; package versions and snapshot checksums are recorded in the bundle manifest:

- [Ponytail](https://github.com/DietrichGebert/ponytail) by DietrichGebert (MIT)
- [Obsidian](https://obsidian.md)
- [Interpretable Context Methodology](https://github.com/RinDig/Interpretable-Context-Methodology) and [icm-architect](https://github.com/RinDig/icm-architect) by RinDig (MIT)
- [Graphify](https://pypi.org/project/graphifyy/), [MarkItDown](https://github.com/microsoft/markitdown), [claude-conversation-extractor](https://pypi.org/project/claude-conversation-extractor/)

<a id="license"></a>
## 📄 License

[MIT](LICENSE). Free to use, change and share, including commercially, as long as you keep the copyright notice. Provided as is, with no warranty.

<p align="center"><sub><a href="#contents">↑ Back to top</a></sub></p>
