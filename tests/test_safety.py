from pathlib import Path

from repo_seatbelt.safety import dangerous_path_reason


def test_home_root_is_dangerous(tmp_path: Path) -> None:
    assert dangerous_path_reason(tmp_path, home=tmp_path) == "current path is the user home root"


def test_filesystem_or_drive_root_is_dangerous(tmp_path: Path) -> None:
    assert dangerous_path_reason(Path(tmp_path.anchor), home=tmp_path) is not None


def test_nested_project_is_not_dangerous(tmp_path: Path) -> None:
    project = tmp_path / "repo"
    project.mkdir()
    assert dangerous_path_reason(project, home=tmp_path) is None


def test_documents_root_is_dangerous_when_present(tmp_path: Path) -> None:
    documents = tmp_path / "Documents"
    documents.mkdir()
    assert dangerous_path_reason(documents, home=tmp_path) == "current path is the Documents root"


def test_temp_root_is_dangerous(tmp_path: Path) -> None:
    temp_root = tmp_path / "Temp"
    temp_root.mkdir()
    assert dangerous_path_reason(temp_root, home=tmp_path, temp_roots=[temp_root]) == "current path is a temp root"


def test_cache_root_is_dangerous(tmp_path: Path) -> None:
    cache_root = tmp_path / ".cache"
    cache_root.mkdir()
    assert dangerous_path_reason(cache_root, home=tmp_path, cache_roots=[cache_root]) == "current path is a cache root"
