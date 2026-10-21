#!/usr/bin/env python3
"""Download this workflow and run its full installer; no Git checkout required."""
import argparse
import io
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

MAX_DOWNLOAD = 64 * 1024 * 1024


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "agent-workflow-setup"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("Download exceeds the 64 MB bundle limit")
    return data


def extract(data, destination):
    """Validate the entire ZIP before extracting a single-root GitHub archive."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if not entries or len(entries) > 10000 or sum(i.file_size for i in entries) > 128 * 1024 * 1024:
            raise ValueError("Empty or oversized bundle")
        roots = set()
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if (path.is_absolute() or not path.parts or ".." in path.parts
                    or "\\" in entry.filename or ":" in entry.filename
                    or stat.S_ISLNK(entry.external_attr >> 16)):
                raise ValueError(f"Unsafe archive member: {entry.filename}")
            roots.add(path.parts[0])
        if len(roots) != 1:
            raise ValueError("Bundle must contain one top-level directory")
        archive.extractall(destination)
    root = destination / roots.pop()
    if not root.is_dir():
        raise ValueError("Bundle root is not a directory")
    return root


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="main", help="workflow Git commit, branch or tag")
    parser.add_argument("--preview", action="store_true", help="download and preview without installing")
    parser.add_argument("--home", type=Path, help="target home for a disposable or custom install")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10) or sys.version_info >= (3, 15):
        parser.error("Use Python 3.10–3.14 for the bundled tools")
    url = "https://codeload.github.com/zandy700/agent-workflow/zip/" + urllib.parse.quote(args.ref, safe="")
    print("Downloading Agent Workflow…", flush=True)
    with tempfile.TemporaryDirectory(prefix="agent-workflow-") as directory:
        root = extract(download(url), Path(directory))
        script = root / "setup.py"
        if not script.is_file():
            raise ValueError("This revision does not contain setup.py")
        command = [sys.executable, str(script), *([] if args.preview else ["--install"])]
        if args.home is not None:
            command.extend(["--home", str(args.home.expanduser().resolve())])
        return subprocess.run(command, cwd=root).returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        sys.exit(f"Setup failed: {error}")
