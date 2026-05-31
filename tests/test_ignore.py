from repo_seatbelt.ignore import DEFAULT_IGNORES, is_ignored


def test_directory_wildcard_ignore_pattern() -> None:
    assert is_ignored("tmpabc", ["tmp*/"], is_dir=True)
    assert is_ignored("nested/tmpabc/file.txt", ["tmp*/"])


def test_default_generated_and_dependency_dirs_are_ignored() -> None:
    ignored_paths = [
        ".venv/Lib/site-packages/pkg/module.py",
        "venv/lib/site-packages/pkg/module.py",
        "env/lib/site-packages/pkg/module.py",
        ".git/config",
        "__pycache__/mod.pyc",
        ".pytest_cache/v/cache/nodeids",
        ".mypy_cache/meta.json",
        ".ruff_cache/content",
        "node_modules/pkg/index.js",
        "dist/archive.whl",
        "build/lib/module.py",
        ".repo-seatbelt/snapshots/old.zip",
        ".pip-tmp/pip-build-tracker/file",
    ]
    for rel in ignored_paths:
        assert is_ignored(rel, DEFAULT_IGNORES), rel
