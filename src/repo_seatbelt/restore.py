from __future__ import annotations

import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .errors import SeatbeltError
from .paths import is_within
from .snapshot import list_snapshots


@dataclass(frozen=True)
class RestoreResult:
    source: Path
    destination: Path
    file_count: int


def find_snapshot(root: Path, name: str) -> Path:
    candidates = {path.name: path for path in list_snapshots(root)}
    if name not in candidates:
        raise SeatbeltError(f"Snapshot not found: {name}")
    return candidates[name]


def confirmation_phrase(snapshot: Path) -> str:
    return f"RESTORE {snapshot.name}"


def restore_snapshot(root: Path, snapshot: Path, confirmation: str) -> RestoreResult:
    root = root.resolve()
    snapshot = snapshot.resolve()
    expected = confirmation_phrase(snapshot)
    if confirmation != expected:
        raise SeatbeltError(f"Confirmation did not match. Type exactly: {expected}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = root / f"restored_{timestamp}"
    counter = 1
    while destination.exists():
        destination = root / f"restored_{timestamp}_{counter}"
        counter += 1
    destination.mkdir(parents=True)

    file_count = 0
    with zipfile.ZipFile(snapshot) as archive:
        for member in archive.infolist():
            target = destination / member.filename
            if not is_within(target, destination):
                raise SeatbeltError(f"Unsafe path inside snapshot: {member.filename}")
            archive.extract(member, destination)
            if not member.is_dir():
                file_count += 1

    return RestoreResult(snapshot, destination, file_count)
