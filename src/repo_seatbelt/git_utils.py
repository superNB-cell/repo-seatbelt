from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitStatus:
    git_available: bool
    is_repo: bool
    has_changes: bool
    detail: str


def _run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )


def check_git(root: Path) -> GitStatus:
    if shutil.which("git") is None:
        return GitStatus(False, False, False, "git was not found on PATH")

    repo = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if repo.returncode != 0 or repo.stdout.strip().lower() != "true":
        return GitStatus(True, False, False, "current directory is not a git repository")

    status = _run_git(root, ["status", "--porcelain"])
    has_changes = bool(status.stdout.strip())
    detail = "uncommitted changes found" if has_changes else "working tree is clean"
    return GitStatus(True, True, has_changes, detail)
