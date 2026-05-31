from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .doctor import format_doctor, run_doctor
from .snapshot import list_snapshots


def latest_snapshot_line(root: Path) -> str:
    snapshots = list_snapshots(root)
    if not snapshots:
        return "Latest snapshot: none"
    latest = snapshots[0]
    return f"Latest snapshot: {latest.name} ({latest.stat().st_size} bytes)"


def write_report(root: Path) -> Path:
    root = root.resolve()
    result = run_doctor(root)
    report_dir = root / ".repo-seatbelt"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "report.md"
    lines = [
        "# RepoSeatbelt Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Risk score: **{result.risk}**",
        "",
        "## Risky Path Checks",
        "",
        f"- Path: `{result.root}`",
        f"- Status: {'DANGER - ' + result.dangerous_reason if result.dangerous_reason else 'OK'}",
        "",
        "## Git Status Summary",
        "",
        f"- Git available: {'yes' if result.git.git_available else 'no'}",
        f"- Git repository: {'yes' if result.git.is_repo else 'no'}",
        f"- Working tree: {result.git.detail}",
        "",
        "## Risky Files Summary",
        "",
    ]
    if result.findings:
        lines.extend(f"- `{finding.path}`: {finding.kind} ({finding.source})" for finding in result.findings)
    else:
        lines.append("- No likely secrets or risky files found.")
    lines.extend(
        [
            "",
            "## Snapshot Summary",
            "",
            f"- {latest_snapshot_line(root)}",
            "",
            "## Suggested Next Actions",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in result.advice)
    lines.extend(["", "## Doctor Output", "", "```text", format_doctor(result), "```"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
