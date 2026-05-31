from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from . import __version__
from .rules import DEFAULT_TARGET, RULES_TEXT, write_with_backup


DEFAULT_SEATBELTIGNORE = """# RepoSeatbelt local ignores
.venv/
venv/
env/
.git/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
node_modules/
dist/
build/
.repo-seatbelt/snapshots/
.pip-tmp/
*.pyc
tmp*/
"""


def default_config(root: Path) -> dict[str, object]:
    return {
        "version": __version__,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(root.resolve()),
        "snapshot_dir": ".repo-seatbelt/snapshots",
        "snapshot_include_secret_files": False,
        "telemetry": False,
        "network": False,
    }


def load_config(root: Path) -> dict[str, object]:
    path = root / ".repo-seatbelt" / "config.json"
    if not path.exists():
        return default_config(root)
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default_config(root)
    config = default_config(root)
    config.update(loaded)
    return config


def initialize(root: Path) -> list[tuple[Path, Path | None]]:
    seatbelt_dir = root / ".repo-seatbelt"
    snapshots_dir = seatbelt_dir / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    written: list[tuple[Path, Path | None]] = []
    config_text = json.dumps(default_config(root), indent=2) + "\n"
    config_path = seatbelt_dir / "config.json"
    written.append((config_path, write_with_backup(config_path, config_text)))

    ignore_path = root / ".seatbeltignore"
    written.append((ignore_path, write_with_backup(ignore_path, DEFAULT_SEATBELTIGNORE)))

    agents_path = root / DEFAULT_TARGET.path
    written.append((agents_path, write_with_backup(agents_path, RULES_TEXT)))
    return written
