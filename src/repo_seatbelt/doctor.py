from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .git_utils import GitStatus, check_git
from .ignore import load_patterns
from .safety import dangerous_path_reason
from .secrets import Finding, scan_repository


@dataclass(frozen=True)
class DoctorResult:
    root: Path
    dangerous_reason: str | None
    git: GitStatus
    findings: list[Finding]
    risk: str
    advice: list[str]


def score_risk(dangerous_reason: str | None, git: GitStatus, findings: list[Finding]) -> str:
    if dangerous_reason or any(f.severity == "HIGH" for f in findings):
        return "HIGH"
    if not git.is_repo or git.has_changes:
        return "MEDIUM"
    return "LOW"


def build_advice(result: DoctorResult) -> list[str]:
    advice: list[str] = []
    if result.dangerous_reason:
        advice.append("Move into a dedicated project folder before using an AI coding agent.")
    if not result.git.git_available:
        advice.append("Install git or use snapshots as your main rollback mechanism.")
    elif not result.git.is_repo:
        advice.append("Initialize git if this is a project you want to protect with version history.")
    elif result.git.has_changes:
        advice.append("Commit or stash current work if you want an easy rollback point.")
    if result.findings:
        advice.append("Review likely secrets and risky files before sharing prompts, logs, or reports.")
    advice.append("Create a snapshot before large AI-assisted edits or refactors.")
    return advice


def run_doctor(root: Path) -> DoctorResult:
    root = root.resolve()
    dangerous_reason = dangerous_path_reason(root)
    git = check_git(root)
    findings = scan_repository(root, load_patterns(root))
    risk = score_risk(dangerous_reason, git, findings)
    partial = DoctorResult(root, dangerous_reason, git, findings, risk, [])
    return DoctorResult(root, dangerous_reason, git, findings, risk, build_advice(partial))


def format_doctor(result: DoctorResult) -> str:
    risky_count = len(result.findings)
    path_label = f"[HIGH] {result.dangerous_reason}" if result.dangerous_reason else "[OK] OK"
    git_repo_label = "[OK] YES" if result.git.is_repo else "[WARN] NO"
    risky_label = "[OK]" if risky_count == 0 else "[HIGH]"
    lines = [
        "RepoSeatbelt doctor",
        "",
        f"Path safety: {path_label}",
        f"Git repository: {git_repo_label}",
        f"Git status: {result.git.detail}",
        f"Risky files: {risky_label} {risky_count} finding{'s' if risky_count != 1 else ''}",
        "",
        f"Risk score: [{result.risk}]",
        "",
        "Advice:",
    ]
    lines.extend(f"- {item}" for item in result.advice)
    if result.findings:
        lines.extend(["", "Risky files summary:"])
        for finding in result.findings[:20]:
            lines.append(f"- {finding.path}: {finding.kind} ({finding.source})")
        if len(result.findings) > 20:
            lines.append(f"- ...and {len(result.findings) - 20} more")
    return "\n".join(lines)
