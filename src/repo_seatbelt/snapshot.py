from __future__ import annotations

import os
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import load_config
from .ignore import is_ignored, load_patterns
from .paths import is_within
from .secrets import should_exclude_from_snapshot


@dataclass(frozen=True)
class SnapshotResult:
    path: Path
    size_bytes: int
    file_count: int


def snapshot_dir(root: Path) -> Path:
    return root / ".repo-seatbelt" / "snapshots"


def list_snapshots(root: Path) -> list[Path]:
    directory = snapshot_dir(root)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)


def iter_snapshot_files(root: Path, include_secret_files: bool | None = None) -> list[Path]:
    root = root.resolve()
    patterns = load_patterns(root)
    if include_secret_files is None:
        include_secret_files = bool(load_config(root).get("snapshot_include_secret_files", False))
    files: list[Path] = []
    for current, dirs, filenames in os.walk(root):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root).as_posix() if current_path != root else ""
        kept_dirs = []
        for directory in dirs:
            path = current_path / directory
            rel = f"{rel_dir}/{directory}".strip("/")
            if path.is_symlink() and not is_within(path, root):
                continue
            if not is_ignored(rel, patterns, is_dir=True):
                kept_dirs.append(directory)
        dirs[:] = kept_dirs

        for filename in filenames:
            path = current_path / filename
            rel = path.relative_to(root).as_posix()
            if is_ignored(rel, patterns):
                continue
            if not include_secret_files and should_exclude_from_snapshot(path):
                continue
            if path.is_symlink() and not is_within(path, root):
                continue
            files.append(path)
    return files


def create_snapshot(root: Path) -> SnapshotResult:
    root = root.resolve()
    directory = snapshot_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = directory / f"repo-seatbelt_{timestamp}.zip"

    counter = 1
    while target.exists():
        target = directory / f"repo-seatbelt_{timestamp}_{counter}.zip"
        counter += 1

    files = iter_snapshot_files(root)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())

    return SnapshotResult(target, target.stat().st_size, len(files))


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"
