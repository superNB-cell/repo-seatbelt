from __future__ import annotations

import fnmatch
from pathlib import Path


DEFAULT_IGNORES = [
    ".venv/",
    "venv/",
    "env/",
    ".git/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "node_modules/",
    "dist/",
    "build/",
    ".repo-seatbelt/snapshots/",
    ".pip-tmp/",
]


def load_patterns(root: Path) -> list[str]:
    patterns: list[str] = []
    for rel in (".gitignore", ".seatbeltignore"):
        path = root / rel
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            patterns.append(line.replace("\\", "/"))
    return DEFAULT_IGNORES + patterns


def _match_file(pattern: str, rel: str) -> bool:
    rel = rel.replace("\\", "/")
    name = rel.rsplit("/", 1)[-1]
    pattern = pattern.lstrip("/")
    if "/" not in pattern:
        return fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel, pattern)
    return fnmatch.fnmatch(rel, pattern)


def is_ignored(rel: str, patterns: list[str], is_dir: bool = False) -> bool:
    rel = rel.replace("\\", "/").strip("/")
    for pattern in patterns:
        pattern = pattern.strip()
        if not pattern:
            continue
        if pattern.endswith("/"):
            directory = pattern.strip("/")
            if rel == directory or rel.startswith(directory + "/"):
                return True
            if fnmatch.fnmatch(rel, directory) or fnmatch.fnmatch(rel + "/", pattern):
                return True
            if "/" not in directory and any(fnmatch.fnmatch(part, directory) for part in rel.split("/")):
                return True
            continue
        if _match_file(pattern, rel):
            return True
        if is_dir and _match_file(pattern.rstrip("/") + "/", rel + "/"):
            return True
    return False
