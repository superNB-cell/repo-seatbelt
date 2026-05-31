from __future__ import annotations

import os
import tempfile
from pathlib import Path


def _same_path(left: Path, right: Path) -> bool:
    return str(left.resolve()).casefold() == str(right.resolve()).casefold()


def _candidate_roots(values: list[str | Path | None]) -> list[Path]:
    roots: list[Path] = []
    for value in values:
        if not value:
            continue
        try:
            roots.append(Path(value).expanduser().resolve())
        except OSError:
            continue
    return roots


def default_temp_roots() -> list[Path]:
    return _candidate_roots([tempfile.gettempdir(), os.environ.get("TEMP"), os.environ.get("TMP")])


def default_cache_roots(home: Path) -> list[Path]:
    return _candidate_roots(
        [
            os.environ.get("XDG_CACHE_HOME"),
            os.environ.get("LOCALAPPDATA"),
            home / ".cache",
            home / "AppData" / "Local",
        ]
    )


def dangerous_path_reason(
    path: Path,
    home: Path | None = None,
    temp_roots: list[Path] | None = None,
    cache_roots: list[Path] | None = None,
) -> str | None:
    target = path.expanduser().resolve()

    if target.anchor and str(target).casefold() == target.anchor.casefold():
        if target.drive:
            return f"current path is the drive root ({target.anchor})"
        return "current path is the filesystem root"

    if target.parent == target:
        return "current path is the filesystem root"

    home_path = (home or Path.home()).expanduser().resolve()
    if _same_path(target, home_path):
        return "current path is the user home root"

    for name in ("Desktop", "Documents", "Downloads"):
        special = home_path / name
        if special.exists() and _same_path(target, special):
            return f"current path is the {name} root"

    for temp_root in temp_roots if temp_roots is not None else default_temp_roots():
        if _same_path(target, temp_root):
            return "current path is a temp root"

    for cache_root in cache_roots if cache_roots is not None else default_cache_roots(home_path):
        if cache_root.exists() and _same_path(target, cache_root):
            return "current path is a cache root"

    return None
