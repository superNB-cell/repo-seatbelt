from __future__ import annotations

from pathlib import Path


def resolve_path(path: Path) -> Path:
    return path.expanduser().resolve()


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()
