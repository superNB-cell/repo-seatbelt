import json
from pathlib import Path

from repo_seatbelt.config import initialize
from repo_seatbelt.rules import RULES_TEXT, targets_for_flags, write_rules


def test_initialize_creates_config_snapshot_dir_ignore_and_agents(tmp_path: Path) -> None:
    initialize(tmp_path)
    assert (tmp_path / ".repo-seatbelt" / "config.json").exists()
    assert (tmp_path / ".repo-seatbelt" / "snapshots").is_dir()
    assert (tmp_path / ".seatbeltignore").exists()
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == RULES_TEXT

    config = json.loads((tmp_path / ".repo-seatbelt" / "config.json").read_text(encoding="utf-8"))
    assert config["telemetry"] is False
    assert config["network"] is False
    assert config["snapshot_include_secret_files"] is False


def test_initialize_backs_up_existing_files(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("old rules", encoding="utf-8")
    initialize(tmp_path)
    assert agents.read_text(encoding="utf-8") == RULES_TEXT
    assert (tmp_path / "AGENTS.md.bak").read_text(encoding="utf-8") == "old rules"


def test_rule_generation_optional_targets(tmp_path: Path) -> None:
    targets = targets_for_flags(agents=True, claude=True, cursor=True, codex=True)
    write_rules(tmp_path, targets)
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".cursorrules").exists()
    assert (tmp_path / "CODEX_RULES.md").exists()


def test_rule_generation_without_flags_defaults_to_agents() -> None:
    targets = targets_for_flags()
    assert [target.path for target in targets] == ["AGENTS.md"]


def test_rule_generation_with_codex_flag_only_skips_agents() -> None:
    targets = targets_for_flags(codex=True)
    assert [target.path for target in targets] == ["CODEX_RULES.md"]
