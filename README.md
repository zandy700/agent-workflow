# Agent workflow (macOS)

Rules, hooks, and scripts that make Claude Code, Codex, and Cursor read less, check more, and spend fewer tokens. Every agent chat is saved to an Obsidian vault, so a new session can pick up from a short note instead of a long transcript.

- **How it works and where it saves tokens:** [docs/how-it-works.md](docs/how-it-works.md)
- **Using the Obsidian notes day to day** (handoffs, decisions, saved lessons): [docs/obsidian-notes-guide.md](docs/obsidian-notes-guide.md)

## Setup overview

Do the parts in order. Only Parts 1 to 3 are needed for the core workflow; the rest add to it.

| Part | What you get | Time |
|---|---|---|
| [1. Install the workflow](#part-1-install-the-workflow) | Rules and hooks for all three apps | 5 min |
| [2. Set up Obsidian](#part-2-set-up-obsidian) | A vault to hold notes and chats | 5 min |
| [3. Connect agent chats to Obsidian](#part-3-connect-agent-chats-to-obsidian) | Every chat saved to the vault automatically | 10 min |
| [4. Add the rules to Cursor](#part-4-add-the-rules-to-cursor) | Cursor follows the same rules | 2 min |
| [5. Install Ponytail](#part-5-install-ponytail) | Agents stick to the smallest working change | 5 min |
| [6. Optional extras](#part-6-optional-extras) | Code graphs, document conversion | 5 min |
| [7. Check that it works](#part-7-check-that-it-works) | Confidence each app loaded everything | 5 min |

**Before you start:** install and sign into the apps you use (Claude Code, Codex, Cursor). You need Python 3 (`python3 --version` in Terminal) and `git`.

---

## Part 1. Install the workflow

The installer copies the rules and scripts into your home folder and adds its hooks to each app's settings. It shows what it will change first, and backs up any file it replaces.

**1. Download the package.** In Terminal:

```bash
git clone https://github.com/zandy700/agent-workflow.git
cd agent-workflow
```

**2. Preview.** Nothing is written yet:

```bash
python3 install.py
```

Read the list of files it would write.

**3. Install:**

```bash
python3 install.py --install
```

Replaced files are backed up to `~/Scripts/agent-workflow-backups/<timestamp>/`. Running it again is safe; it reports "Already installed" when nothing changed.

---

## Part 2. Set up Obsidian

Obsidian is a free notes app that works on a plain folder of Markdown files. The installer already created that folder: `~/Obsidian Sync/ObsidianVault`. ("Obsidian Sync" here is just the folder name; you don't need Obsidian's paid Sync service.)

**1. Install Obsidian** from [obsidian.md](https://obsidian.md) and open it.

**2. Open the vault.** On the start screen choose **Open folder as vault**, then pick `ObsidianVault` inside the `Obsidian Sync` folder in your home folder.

> Tip: in Finder, press `Cmd+Shift+G` and paste `~/Obsidian Sync/ObsidianVault` to jump there.

**3. Hide generated graph notes** (they get numerous once you use Graphify). Open **Graph view**, click the gear icon at its top right, and under **Filters** type `-path:graphify` in the search box.

The vault will hold the text of your agent chats. Use a personal vault on a personal machine.

---

## Part 3. Connect agent chats to Obsidian

After every agent turn, a hook runs the sync script in the background. It copies new chats into `ObsidianVault/chats/<app>/<YYYY-MM>/`. The agent never waits for it, and it uses no model tokens.

| App | How its chats are read | What you do |
|---|---|---|
| Claude Code | the `claude-extract` tool | Install it (step 1) |
| Codex | read directly from `~/.codex/sessions` | Trust the hook (step 3) |
| Cursor | read directly from `~/.cursor/projects` | Nothing; Cursor picks up the hook itself |

**1. Install the Claude Code chat extractor.**

If you installed Python from python.org or via `pyenv`/`nvm`:

```bash
pip3 install claude-conversation-extractor
```

If `pip3` refuses with "externally managed environment" (common with Homebrew Python), use `pipx` instead:

```bash
brew install pipx
pipx install claude-conversation-extractor
```

**2. Run the first full sync by hand.** This exports existing chats and builds the vault's `Home.md`:

```bash
"$HOME/Obsidian Sync/sync_claude_obsidian.sh" --all
```

Open Obsidian: you should see `Home.md` and a `chats/` folder. If it's empty, read the log:

```bash
tail -20 "$HOME/Obsidian Sync/claude_obsidian_sync.log"
```

**3. Trust the Codex hook.** Codex runs a new hook only after you approve it. Start `codex`, type `/hooks`, review the Stop hook that runs `agent_stop_hook.sh`, and trust it.

**4. Turn on the nightly full sync** (optional; it also refreshes the generated index notes each night at 22:00):

```bash
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/local.agent-workflow.obsidian-sync.plist"
```

**5. Test it.** Send one message in any app, wait a few seconds, and look in `chats/` in Obsidian for today's chat.

Now learn how to use the notes: **[docs/obsidian-notes-guide.md](docs/obsidian-notes-guide.md)**.

---

## Part 4. Add the rules to Cursor

Claude Code and Codex read their rules from files the installer wrote. Cursor keeps its global rules inside the app, so paste them in once.

1. Open `payload/cursor/USER_RULES.md` from this package and copy all of it.
2. In Cursor: **Customize → Rules → User Rules**, paste, and save.

([Cursor rules docs](https://cursor.com/docs/rules))

---

## Part 5. Install Ponytail

[Ponytail](https://github.com/DietrichGebert/ponytail) (MIT, by DietrichGebert) keeps agents to the smallest change that works: reuse before writing, standard library before new dependencies, shortest diff. It installs from its own repo so it keeps updating. It needs `node` (`node --version`).

**Claude Code:** send these as two separate prompts:

```text
/plugin marketplace add DietrichGebert/ponytail
```
```text
/plugin install ponytail@ponytail
```

**Codex:** in Terminal:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Then start `codex`, open `/hooks`, trust Ponytail's hooks, and start a new thread.

**Cursor:** in Terminal:

```bash
git clone https://github.com/DietrichGebert/ponytail ~/Scripts/ponytail
node ~/Scripts/ponytail/scripts/cursor-hooks.js install
```

Leave the clone where it is; Cursor's hooks run from it.

**Using it:** switch levels with `/ponytail lite`, `/ponytail full`, or `/ponytail ultra`; turn it off with `stop ponytail`. To remove it, see [Ponytail's uninstall steps](https://github.com/DietrichGebert/ponytail#uninstall).

---

## Part 6. Optional extras

Skip these until you want them. The rules work without them; the related steps are simply skipped.

**Code graphs (Graphify).** Lets agents find code by asking a graph instead of reading whole folders.

```bash
pip3 install graphifyy          # or: pipx install graphifyy
```

Then, once per repository (not your home folder):

```bash
~/Scripts/graphify-bootstrap /path/to/your/repo
```

That builds the graph (no model calls, no cost), keeps it fresh on each commit, and creates the repo's notebook in the vault. To run it as plain `graphify-bootstrap`, add `~/Scripts` to your `PATH`:

```bash
echo 'export PATH="$HOME/Scripts:$PATH"' >> ~/.zshrc
```

**Document conversion (MarkItDown).** Lets agents turn PDFs, Word, and PowerPoint files into Markdown and read only the parts they need.

```bash
pip3 install 'markitdown[all]'  # or: pipx install 'markitdown[all]'
```

---

## Part 7. Check that it works

A file on disk doesn't prove the app loaded it. In each app, **start a fresh chat** and ask:

```text
What workflow rules did you load from your global instructions? Is Ponytail active?
```

You should hear about acceptance checks, small tool output, handoff notes in the Obsidian vault, and Ponytail. Then send one more message and confirm the chat appears in `ObsidianVault/chats/`.

**Something not working?**

| Problem | Check |
|---|---|
| No chats in the vault | `tail -20 "$HOME/Obsidian Sync/claude_obsidian_sync.log"` |
| Codex chats missing | Did you trust the hook in `/hooks`? |
| Claude Code chats missing | `claude-extract --help` works? If not, redo Part 3 step 1 |
| Nightly sync not running | `launchctl print "gui/$(id -u)/local.agent-workflow.obsidian-sync"` |
| Rules not followed | Start a new chat; rules load at session start |

---

## Benchmark

A 4-turn incremental coding task (build a cache class → add TTL → add stats → write tests) was run twice in parallel using Claude Haiku: one agent with no rules (bare), one with the workflow rules injected (Ponytail + editing discipline).

**Output tokens (measured as response chars):**

| Turn | Bare | Workflow | Savings |
|---|---|---|---|
| T1: KV store class | ~450 | ~395 | 12% |
| T2: add TTL expiry | ~760 | ~480 | 37% |
| T3: add hit-rate stats | ~1,030 | ~430 | 58% |
| T4: write 3 tests | ~1,200 | ~450 | 63% |
| **Total output** | **~3,440** | **~1,755** | **~49%** |

The gap widens each turn because the bare agent re-echoes the full growing class inline. Those code blocks re-enter conversation history and are re-sent as input on every subsequent turn. All-in (output + accumulated history re-sent as input) savings over 4 turns: **~24%**, growing with session length.

The workflow rule injection (~1,200 chars) is front-loaded on Turn 1 and pays for itself by Turn 2.

**The bare agent lied about verification.** In Turn 4 it reported:

> *"Files are in the scratchpad: kvstore.py and test_kvstore.py. Running `python3 test_kvstore.py` prints '3 passed'."*

Neither file existed. The agent fabricated the file paths, the run, and the output. The workflow agent said *"I did not execute this"* on Turn 1 when it hadn't run a check, and reported an actual pass only after writing and running the file. This is the editing-discipline rule at work: **report verified outcomes; label anything untested.** Without it, an agent fills in plausible-sounding results that never happened.

---

## For contributors: checks without model calls

```bash
python3 -m py_compile install.py payload/obsidian/*.py
bash -n payload/obsidian/*.sh payload/scripts/*.sh
python3 install.py --home "$(mktemp -d)" --install
```
