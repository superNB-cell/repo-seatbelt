import zipfile
from pathlib import Path

from repo_seatbelt.errors import SeatbeltError
from repo_seatbelt.restore import confirmation_phrase, restore_snapshot
from repo_seatbelt.snapshot import create_snapshot, iter_snapshot_files


def test_snapshot_respects_ignores_and_excludes_snapshots(tmp_path: Path) -> None:
    (tmp_path / "keep.txt").write_text("keep", encoding="utf-8")
    (tmp_path / "skip.log").write_text("skip", encoding="utf-8")
    (tmp_path / ".env").write_text("fake", encoding="utf-8")
    (tmp_path / ".venv" / "Lib" / "site-packages").mkdir(parents=True)
    (tmp_path / ".venv" / "Lib" / "site-packages" / "dependency.py").write_text("dependency", encoding="utf-8")
    (tmp_path / ".seatbeltignore").write_text("*.log\n", encoding="utf-8")
    (tmp_path / ".repo-seatbelt" / "snapshots").mkdir(parents=True)
    (tmp_path / ".repo-seatbelt" / "snapshots" / "old.zip").write_text("old", encoding="utf-8")

    files = {path.relative_to(tmp_path).as_posix() for path in iter_snapshot_files(tmp_path)}
    assert "keep.txt" in files
    assert "skip.log" not in files
    assert ".env" not in files
    assert ".venv/Lib/site-packages/dependency.py" not in files
    assert ".repo-seatbelt/snapshots/old.zip" not in files

    included = {path.relative_to(tmp_path).as_posix() for path in iter_snapshot_files(tmp_path, include_secret_files=True)}
    assert ".env" in included

    result = create_snapshot(tmp_path)
    with zipfile.ZipFile(result.path) as archive:
        names = set(archive.namelist())
    assert "keep.txt" in names
    assert "skip.log" not in names
    assert ".env" not in names
    assert ".venv/Lib/site-packages/dependency.py" not in names
    assert ".repo-seatbelt/snapshots/old.zip" not in names


def test_restore_requires_confirmation_and_extracts_to_new_folder(tmp_path: Path) -> None:
    (tmp_path / "keep.txt").write_text("keep", encoding="utf-8")
    result = create_snapshot(tmp_path)

    try:
        restore_snapshot(tmp_path, result.path, "yes")
    except SeatbeltError:
        pass
    else:
        raise AssertionError("restore should require exact typed confirmation")

    restored = restore_snapshot(tmp_path, result.path, confirmation_phrase(result.path))
    assert restored.destination.name.startswith("restored_")
    assert (restored.destination / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert (tmp_path / "keep.txt").read_text(encoding="utf-8") == "keep"
