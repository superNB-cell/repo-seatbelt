from pathlib import Path

from repo_seatbelt.ignore import load_patterns
from repo_seatbelt.secrets import risky_filename, scan_repository, scan_text


def test_scan_text_detects_named_api_keys() -> None:
    assert "OPENAI_API_KEY" in scan_text("OPENAI_" "API_KEY=sk-test")
    assert "ANTHROPIC_API_KEY" in scan_text("ANTHROPIC_" "API_KEY=secret")
    assert "DEEPSEEK_API_KEY" in scan_text("DEEPSEEK_" "API_KEY=secret")
    assert "AWS_ACCESS_KEY_ID" in scan_text("AWS_ACCESS_" "KEY_ID=AKIA" "1234567890123456")
    assert "access_token" in scan_text("access_" "token=abc123")
    assert "refresh_token" in scan_text("refresh_" "token=abc123")


def test_scan_text_detects_github_token_shape() -> None:
    labels = scan_text("token=ghp_" "1234567890abcdefghijklmnopqrstuvwxyz")
    assert "GitHub token" in labels


def test_risky_filename_detects_env_and_ssh_keys() -> None:
    assert risky_filename(Path(".env")) == ".env file"
    assert risky_filename(Path(".env.local")) == ".env file"
    assert risky_filename(Path(".env.example")) is None
    assert risky_filename(Path("id_rsa")) == "id_rsa"
    assert risky_filename(Path("id_ed25519")) == "id_ed25519"
    assert risky_filename(Path("private_key.pem")) == "private_key.pem"


def test_scan_repository_finds_filename_and_content(tmp_path: Path) -> None:
    env_name = "OPENAI_" + "API_KEY"
    github_token = "github_pat_" + "1234567890abcdefghijklmnop"
    (tmp_path / ".env").write_text(f"{env_name}=sk-example", encoding="utf-8")
    (tmp_path / "app.py").write_text(f"token='{github_token}'", encoding="utf-8")
    findings = scan_repository(tmp_path, [])
    kinds = {finding.kind for finding in findings}
    assert ".env file" in kinds
    assert "OPENAI_API_KEY" in kinds
    assert "GitHub token" in kinds


def test_scan_repository_ignores_virtualenv_but_detects_project_root(tmp_path: Path) -> None:
    env_key = "OPENAI_" + "API_KEY"
    site_packages = tmp_path / ".venv" / "Lib" / "site-packages" / "vendor"
    site_packages.mkdir(parents=True)
    (site_packages / "config.py").write_text(f"{env_key}=ignored", encoding="utf-8")
    (tmp_path / "settings.py").write_text(f"{env_key}=detected", encoding="utf-8")

    findings = scan_repository(tmp_path, load_patterns(tmp_path))
    paths = {finding.path for finding in findings}
    assert "settings.py" in paths
    assert ".venv/Lib/site-packages/vendor/config.py" not in paths


def test_scan_repository_ignores_snapshots_by_default(tmp_path: Path) -> None:
    env_key = "OPENAI_" + "API_KEY"
    snapshot_dir = tmp_path / ".repo-seatbelt" / "snapshots"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "old.txt").write_text(f"{env_key}=ignored", encoding="utf-8")

    findings = scan_repository(tmp_path)
    assert findings == []
