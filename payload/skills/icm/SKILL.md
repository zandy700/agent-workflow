---
name: icm
description: Use Interpretable Context Methodology to create or run a reusable, staged Markdown workflow. Trigger for ICM, stage contracts, workspace-builder, or the bundled ICM workspaces; skip ordinary one-step project tasks.
---

# Interpretable Context Methodology

Canonical templates: `~/Scripts/icm` (a clone of RinDig/Interpretable-Context-Methodology in the user's home folder). This repository is a template library, not an executable plugin. If the folder is missing, tell the user to clone it (see the agent-workflow README, Optional extras → ICM) instead of guessing its contents.

1. Identify the current project and the requested workflow. Choose an existing workspace under `workspaces/` or use `workspaces/workspace-builder/` for a new domain. If no project or destination is clear, ask where the workspace should live.
2. Read the chosen workspace's `CLAUDE.md` and `CONTEXT.md`, even in Codex or Cursor; they are the repository's routing files. Read `_core/CONVENTIONS.md` when building or changing a workspace. Load only the stage references named in that stage's Inputs table.
3. Create a project-local copy when the user asks to set up a workflow. Keep setup answers, `_config/`, and stage `output/` files in that project. Do not write them into the canonical clone or another project's workspace. Preserve existing project instructions and files unless the user requests a change.
4. Follow the numbered stage order, input/output contracts, checkpoints, and audits. At a checkpoint, present the current artifact for human review before advancing. Treat edited output files as the next stage's input.
5. Verify setup by checking that referenced files exist, placeholders intended for setup are resolved, and the first stage can be routed from the copied workspace. Report the workspace path and next stage.

Bundled choices: `script-to-animation`, `course-deck-production`, `voice-driven-animation`, and `workspace-builder`. Invoke this skill as `/icm` in tools that support skill commands.

Companion skill: for designing a NEW workspace from a described process, mapping a repo/vault/folder so agents can find things, or restructuring an existing folder into ICM, use `/icm-architect` (`~/Scripts/icm-architect`). It builds or audits the structure; this skill supplies the spec and ready-made workspaces it draws on. Prefer icm-architect over `workspace-builder` for new domains.
