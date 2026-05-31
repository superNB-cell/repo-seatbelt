from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_RULES = """## Repository Boundary

- Stay inside this repository.
- Never delete, move, rewrite, or clean files outside this repository.
- Never clean `C:\\`, drive roots, user home, Desktop, Documents, Downloads,
  caches, temp folders, or global/system paths.
- Do not modify global shell profiles, system configuration, registry settings,
  global Git config, system environment variables, caches, temp folders, or user
  directories.
- Do not install global tools, hooks, services, daemons, startup tasks, or
  background processes.
- Do not run network operations unless the human explicitly requests them.

## Destructive Commands

- Ask before running destructive commands.
- Do not run recursive destructive commands such as `rm -rf`, `rmdir /s`,
  `del /s`, `Remove-Item -Recurse`, `git clean -fdx`, or `git reset --hard`.
- If unsure, stop and ask instead of guessing.

## Snapshots and Recovery

- Create a RepoSeatbelt snapshot before large refactors, dependency migrations,
  generated-code rewrites, or multi-file transformations.
- Restore only into a new folder unless the human explicitly chooses another
  recovery path.

## Secrets

- Do not read secrets unless the task explicitly requires it.
- Do not expose API keys, private keys, tokens, `.env` contents, credentials,
  or signing material in prompts, logs, commits, screenshots, or reports.
- If likely secrets are found, stop and ask the human how to proceed.

## Testing and Summaries

- Run relevant tests after modifications when tests are available.
- After each task, summarize changed files and the reason for each change.
- Call out tests run, tests skipped, and any residual risk.
"""


RULE_TEMPLATES = {
    "agents": """# AI Coding Agent Safety Rules

These rules apply to Codex, Claude Code, Cursor, Gemini CLI, Copilot, and any
other AI coding agent working in this repository.

"""
    + BASE_RULES,
    "codex": """# Codex Safety Rules

Use these rules when Codex is editing this repository.

"""
    + BASE_RULES
    + """
## Codex Workflow

- Read the existing code before editing.
- Prefer small, reviewable patches.
- Do not stage, commit, push, tag, or publish unless the human asks.
""",
    "claude": """# Claude Code Safety Rules

Use these rules when Claude Code is editing this repository.

"""
    + BASE_RULES
    + """
## Claude Code Workflow

- Use a brief plan before large edits.
- Prefer RepoSeatbelt snapshots before multi-file refactors.
- Keep generated summaries practical and tied to files changed.
""",
    "cursor": """# Cursor Rules

Use these rules when Cursor or an AI-assisted editor is editing this repository.

"""
    + BASE_RULES
    + """
## Editor Workflow

- Keep changes scoped to the files relevant to the request.
- Avoid broad formatting churn unless the human asks for it.
- Review generated diffs before considering the task complete.
""",
}

RULES_TEXT = RULE_TEMPLATES["agents"]


@dataclass(frozen=True)
class RuleTarget:
    path: str
    description: str
    template_key: str


DEFAULT_TARGET = RuleTarget("AGENTS.md", "general AI coding agents", "agents")
OPTIONAL_TARGETS = {
    "agents": DEFAULT_TARGET,
    "claude": RuleTarget("CLAUDE.md", "Claude Code", "claude"),
    "cursor": RuleTarget(".cursorrules", "Cursor", "cursor"),
    "codex": RuleTarget("CODEX_RULES.md", "Codex", "codex"),
}


def backup_path(path: Path) -> Path:
    candidate = path.with_name(path.name + ".bak")
    if not candidate.exists():
        return candidate
    index = 1
    while True:
        numbered = path.with_name(f"{path.name}.bak{index}")
        if not numbered.exists():
            return numbered
        index += 1


def write_with_backup(path: Path, text: str) -> Path | None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old_text = path.read_text(encoding="utf-8", errors="replace")
        if old_text == text:
            return None
        backup = backup_path(path)
        backup.write_text(old_text, encoding="utf-8")
    else:
        backup = None
    path.write_text(text, encoding="utf-8")
    return backup


def write_rules(root: Path, targets: list[RuleTarget]) -> list[tuple[Path, Path | None]]:
    written: list[tuple[Path, Path | None]] = []
    for target in targets:
        path = root / target.path
        backup = write_with_backup(path, RULE_TEMPLATES[target.template_key])
        written.append((path, backup))
    return written


def targets_for_flags(
    claude: bool = False,
    cursor: bool = False,
    codex: bool = False,
    agents: bool = False,
) -> list[RuleTarget]:
    if not any((claude, cursor, codex, agents)):
        return [DEFAULT_TARGET]

    targets: list[RuleTarget] = []
    if agents:
        targets.append(OPTIONAL_TARGETS["agents"])
    if claude:
        targets.append(OPTIONAL_TARGETS["claude"])
    if cursor:
        targets.append(OPTIONAL_TARGETS["cursor"])
    if codex:
        targets.append(OPTIONAL_TARGETS["codex"])
    return targets
