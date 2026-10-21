# Agent Workflow

**English** · [简体中文](README.zh-CN.md)

Shared coding rules, project handoffs, and local chat history for **Claude Code, Codex, and Cursor**.

<a id="quickstart"></a>
## Install

Requires **Python 3.10–3.14**, internet access, and a coding app installed and signed in. [Get Python](https://www.python.org/downloads/) if needed.

**Mac — Terminal:**

```bash
python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

**Windows — PowerShell:**

```powershell
py -3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

On Windows, use `python` instead of `py -3` if the launcher is unavailable. Already cloned the repo? Run `python3 setup.py --install`; omit `--install` to preview.

**After installation:**

1. Start a new chat. Approve workflow hooks if prompted; in Codex, review `/hooks`. Cursor loads the rules automatically through its session-start hook.
2. To view your notes, open `~/Obsidian Sync/ObsidianVault` as a vault in Obsidian. Obsidian is optional, and paid Sync is not required.

Rerun the command to update. Custom instructions, unrelated hooks, notes, and existing ICM folders are preserved; replaced files are backed up. [Setup and recovery details](docs/setup-options.md)

**Windows:** configuration is tested on macOS; a full installation on Windows remains unverified. This setup is for local coding apps.

<a id="setup"></a>
<a id="extras"></a>
<a id="icm"></a>
## Included

| Part | What it does |
|---|---|
| Shared rules | Keep changes focused, require honest verification, and put independent tasks in new sessions. |
| Chat sync and handoffs | Save local transcripts to a Markdown vault and carry project state between chats. |
| ICM + icm-architect | Provide reusable workflows, design project structures, and map folders. |
| Graphify + MarkItDown | Map code and convert documents, using tools installed in an isolated Python environment. |

Tools run on demand. Project maps require approval. Ponytail and nightly sync are optional; see [setup options](docs/setup-options.md).

<a id="daily"></a>
## Everyday use

| When | Ask the agent |
|---|---|
| Before closing a chat | “Write the handoff note for this repo.” |
| Continuing in a new chat | “Read the handoff note and continue.” |
| Looking up a decision | “Check the notes: why did we do X?” |
| Organizing a project | “/icm-architect map this repo.” |

A task that needs none of the current chat's context gets its own session, even in the same repo.

<a id="results"></a>
<a id="checks"></a>
## Details

- [Setup options, troubleshooting, and checks](docs/setup-options.md)
- [How it works](docs/how-it-works.md) · [Using the notes](docs/obsidian-notes-guide.md)
- [Benchmark results and limits](docs/token-benchmark.md) — no guaranteed token or cost savings.
- [Pinned versions and download checksums](bundle.json)

## Credits and license

Built with [ICM](https://github.com/RinDig/Interpretable-Context-Methodology) and [icm-architect](https://github.com/RinDig/icm-architect) by RinDig, [Graphify](https://pypi.org/project/graphifyy/), [MarkItDown](https://github.com/microsoft/markitdown), and [claude-conversation-extractor](https://pypi.org/project/claude-conversation-extractor/). Optional: [Obsidian](https://obsidian.md) and [Ponytail](https://github.com/DietrichGebert/ponytail).

[MIT license](LICENSE). Upstream tools retain their own licenses.
