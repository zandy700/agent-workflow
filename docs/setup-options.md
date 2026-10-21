# Setup options

The [one-command setup](../README.md#quickstart) is the default. These options are for custom installations.

## Preview or install from a checkout

```bash
python3 setup.py                 # preview; no changes or downloads
python3 setup.py --install       # full setup
python3 setup.py --install --home /path/to/disposable-home
```

Use `py -3` instead of `python3` on Windows. The target home must already exist. A different `--home` also isolates the first sync from your real chats and vault.

For only the original core files, run `python3 install.py --install`. This skips dependency installation, ICM downloads, and the first sync. The core installer still supports a preview when `--install` is omitted.

The downloaded bootstrap accepts `--ref <commit-or-tag>` and `--preview`. Dependency versions and ICM checksums are recorded in [bundle.json](../bundle.json). Python packages are installed into `~/Scripts/agent-workflow-runtime`; command wrappers are in `~/Scripts`. Setup logs are in `~/Scripts/agent-workflow-setup.log`.

## Updates and recovery

Rerun the one-command setup to update managed files and pinned Python tools. Custom instructions outside the `agent-workflow` markers and unrelated hooks are retained. Files replaced by the core installer are backed up under `~/Scripts/agent-workflow-backups/<timestamp>/`.

Existing ICM directories and `icm-architect` skill directories are deliberately retained. To replace one with a newer pinned snapshot, first move the old directory to a backup location, then rerun setup. Broken or incomplete existing directories produce an error instead of being overwritten. Never put project outputs inside these template directories.

A failed setup exits nonzero and reports the failed stage and log path. Dependencies downloaded before a failure may remain; rerunning is supported. Setup does not claim that an app loaded its hooks. Confirm that in a new chat after reviewing the app's trust prompts.

## Ponytail (optional)

Ponytail remains off unless explicitly activated. The installer preserves an existing explicit mode and existing plugin preferences.

Claude Code, in the chat box:

```text
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

Codex, in Terminal:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

For Cursor, follow [Ponytail's installation guide](https://github.com/DietrichGebert/ponytail). In supported chats, activate with `/ponytail lite` or `/ponytail full`. See [workflow defaults](../payload/scripts/agent-workflow-reference.md#ponytail) for configuration paths.

## Optional nightly sync

Stop hooks already sync after agent turns. A nightly run can refresh the complete vault and existing project graph notes. Setup writes the macOS LaunchAgent but does not activate it.

Mac, in Terminal:

```bash
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/local.agent-workflow.obsidian-sync.plist"
```

Windows, in PowerShell:

```powershell
$workflowPython = "$HOME\Scripts\agent-workflow-runtime\Scripts\pythonw.exe"
$workflowScript = "$HOME\Obsidian Sync\sync_claude_obsidian.py"
Register-ScheduledTask -TaskName 'AgentWorkflowObsidianSync' -Trigger (New-ScheduledTaskTrigger -Daily -At 10pm) -Action (New-ScheduledTaskAction -Execute $workflowPython -Argument ('"' + $workflowScript + '" --all'))
```

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile bootstrap.py setup.py install.py payload/cursor/*.py payload/obsidian/*.py payload/scripts/*.py
```

The unit suite uses temporary homes and mocked public downloads; it makes no model calls and does not modify live settings. Real dependency installation and Windows execution should be reported separately from mocked or simulated checks.
