from pathlib import Path

from repo_seatbelt.cli import build_parser
from repo_seatbelt.demo import demo_project_path, demo_walkthrough
from repo_seatbelt.doctor import format_doctor, run_doctor
from repo_seatbelt.report import write_report


def test_demo_walkthrough_points_to_demo_project(tmp_path: Path) -> None:
    output = demo_walkthrough(tmp_path)
    assert "examples" in output
    assert "demo-project" in output
    assert "does not modify your files" in output


def test_demo_path_resolves_from_nested_directory(tmp_path: Path) -> None:
    demo = tmp_path / "examples" / "demo-project"
    nested = demo / "subdir"
    nested.mkdir(parents=True)
    assert demo_project_path(nested) == demo


def test_cli_help_includes_demo_command() -> None:
    help_text = build_parser().format_help()
    assert "demo" in help_text
    assert "doctor" in help_text


def test_report_writes_summary_without_secret_values(tmp_path: Path) -> None:
    secret_value = "sk-" + "a" * 24
    (tmp_path / "settings.txt").write_text("OPENAI_" f"API_KEY={secret_value}", encoding="utf-8")
    path = write_report(tmp_path)
    text = path.read_text(encoding="utf-8")
    assert "Risk score" in text
    assert "settings.txt" in text
    assert secret_value not in text


def test_doctor_output_does_not_print_secret_values(tmp_path: Path) -> None:
    secret_value = "ghp_" + "a" * 24
    token_name = "GITHUB_" + "TOKEN"
    (tmp_path / "notes.txt").write_text(f"{token_name}={secret_value}", encoding="utf-8")
    output = format_doctor(run_doctor(tmp_path))
    assert "notes.txt" in output
    assert secret_value not in output
