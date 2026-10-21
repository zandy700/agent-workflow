#!/usr/bin/env python3
"""Install the complete workflow. Preview by default; --install performs setup."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import zipfile

import bootstrap
import install

ROOT = Path(__file__).resolve().parent
RUNTIME = "Scripts/agent-workflow-runtime"
TOOLS = ("claude-extract", "graphify", "markitdown")


def runtime_python(home):
    return home / RUNTIME / ("Scripts/python.exe" if install.WINDOWS else "bin/python")


def environment(home):
    # Disposable-home installs must never export the real user's chats or vault.
    return {**os.environ, "HOME": str(home), "USERPROFILE": str(home),
            "OBSIDIAN_VAULT": str(home / "Obsidian Sync/ObsidianVault"), "PYTHONUTF8": "1"}


def run(command, home, label):
    log_path = home / "Scripts/agent-workflow-setup.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    print(label, flush=True)
    with log_path.open("a", encoding="utf-8") as log:
        log.write(f"\n{label}\n")
        log.flush()
        result = subprocess.run([str(arg) for arg in command], env=environment(home),
                                stdout=log, stderr=subprocess.STDOUT, timeout=900)
    if result.returncode:
        tail = "\n".join(log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-30:])
        raise RuntimeError(f"{label} failed (exit {result.returncode}).\n{tail}\nFull log: {log_path}")


def check_asset(path, required):
    if path.exists():
        if not path.is_dir() or not all((path / name).exists() for name in required):
            raise ValueError(f"Existing folder is incomplete; preserve or rename it before retrying: {path}")
        return True
    if path.is_symlink():
        raise ValueError(f"Broken symlink must be repaired before installing: {path}")
    return False


def asset(home, spec):
    destination = home / spec["destination"]
    if check_asset(destination, spec["required"]):
        print(f"Keeping existing {destination}")
        return destination
    print(f"Installing {spec['name']} ({spec['revision'][:8]})…", flush=True)
    data = bootstrap.download(spec["url"])
    if hashlib.sha256(data).hexdigest() != spec["sha256"]:
        raise ValueError(f"Checksum mismatch for {spec['name']}; no files installed")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="workflow-asset-", dir=destination.parent) as directory:
        source = bootstrap.extract(data, Path(directory))
        check_asset(source, spec["required"])
        # Move a fully verified tree into place; never edit an existing third-party clone.
        source.rename(destination)
    return destination


def wrappers(home):
    items = {}
    for name in TOOLS:
        executable = runtime_python(home).parent / (name + ".exe" if install.WINDOWS else name)
        if install.WINDOWS:
            items[f"Scripts/{name}.cmd"] = f'@"{executable}" %*\r\n'.encode()
        else:
            items[f"Scripts/{name}"] = f'#!/bin/sh\nexec {shlex.quote(str(executable))} "$@"\n'.encode()
    return items


def setup(home, write=False):
    if sys.version_info < (3, 10) or sys.version_info >= (3, 15):
        raise ValueError("Use Python 3.10–3.14 for the bundled tools")
    manifest = json.loads((ROOT / "bundle.json").read_text(encoding="utf-8"))
    # Parse and validate existing settings before downloads or any writes.
    items = install.plan(home)
    for spec in manifest["assets"]:
        check_asset(home / spec["destination"], spec["required"])
    skills = [home / app / "skills/icm-architect" for app in (".claude", ".agents", ".cursor")]
    for path in skills:
        check_asset(path, ["SKILL.md"])
    if not write:
        install.apply(home, items)
        print("Full setup also installs an isolated Python environment and these pinned packages:")
        print("  " + ", ".join(manifest["packages"]))
        print("Installs ICM + icm-architect, connects all three apps, and runs the first local chat sync.")
        print("Preview only. Run this command with --install to proceed.")
        return

    runtime = home / RUNTIME
    python = runtime_python(home)
    if runtime.exists() and not (runtime / "pyvenv.cfg").is_file():
        raise ValueError(f"Refusing to replace a folder that is not a Python environment: {runtime}")
    if not python.is_file():
        run([sys.executable, "-m", "venv", runtime], home, "Creating isolated Python environment…")
    run([python, "-m", "pip", "install", "--disable-pip-version-check", "--no-input",
         *manifest["packages"]], home, "Installing workflow tools…")
    run([python, "-m", "pip", "check"], home, "Checking installed dependencies…")
    for tool in TOOLS:
        executable = python.parent / (tool + ".exe" if install.WINDOWS else tool)
        run([executable, "--help"], home, f"Checking {tool}…")
    sources = {spec["name"]: asset(home, spec) for spec in manifest["assets"]}
    for path in skills:
        if check_asset(path, ["SKILL.md"]):
            print(f"Keeping existing {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="workflow-skill-", dir=path.parent) as directory:
                staged = Path(directory) / "icm-architect"
                shutil.copytree(sources["icm-architect"], staged, ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"))
                staged.rename(path)

    # Replan now that the runtime exists so hooks use its absolute interpreter path.
    items = install.plan(home)
    items.update(wrappers(home))
    install.apply(home, items, write=True)
    if not install.WINDOWS:
        for name in TOOLS:
            path = home / "Scripts" / name
            path.chmod(path.stat().st_mode | 0o111)
    vault = home / "Obsidian Sync/ObsidianVault"
    vault.mkdir(parents=True, exist_ok=True)
    run([python, home / "Obsidian Sync/sync_claude_obsidian.py", "--all"], home, "Syncing existing local chats…")
    if not (vault / "Home.md").is_file():
        raise RuntimeError("Sync did not create the vault Home.md; see the setup log")
    print("\nWorkflow installed. Rules, hooks, tools, ICM, and the first sync are ready.")
    print(f"Vault: {vault}")
    print("Open that folder as a vault in Obsidian when you want to view your notes.")
    print("Start new chats in your coding apps. Approve workflow hooks if an app prompts you.")
    print("Codex: review /hooks. Cursor: rules load through the sessionStart hook; no paste step.")
    print("Ponytail and the optional nightly schedule remain off unless you enable them.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args(argv)
    home = args.home.expanduser().resolve()
    if not home.is_dir():
        parser.error(f"Home directory does not exist: {home}")
    try:
        setup(home, args.install)
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        print(f"Setup failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
