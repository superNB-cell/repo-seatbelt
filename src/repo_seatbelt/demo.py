from __future__ import annotations

from pathlib import Path


def _candidate_roots(search_start: Path | None = None) -> list[Path]:
    roots: list[Path] = []
    if search_start is not None:
        start = search_start.resolve()
        roots.extend([start, *start.parents])

    package_file = Path(__file__).resolve()
    roots.extend(package_file.parents)

    unique_roots: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if root not in seen:
            unique_roots.append(root)
            seen.add(root)
    return unique_roots


def demo_project_path(search_start: Path | None = None) -> Path | None:
    for root in _candidate_roots(search_start):
        candidate = root / "examples" / "demo-project"
        if candidate.is_dir():
            return candidate
    return None


def demo_walkthrough(search_start: Path | None = None) -> str:
    demo = demo_project_path(search_start)
    demo_line = (
        f"[INFO] Demo project: {demo}"
        if demo is not None
        else "[WARN] Bundled demo project was not found."
    )
    cd_line = f"  cd {demo}" if demo is not None else "  cd <repo-root>/examples/demo-project"
    return "\n".join(
        [
            "RepoSeatbelt demo",
            "",
            "[INFO] This command does not modify your files.",
            demo_line,
            "",
            "Try this safe walkthrough:",
            cd_line,
            "  seatbelt doctor",
            "  seatbelt snapshot",
            "  seatbelt rules --agents --codex --claude --cursor",
            "  seatbelt report",
            "",
            "The demo project contains harmless fake secret-looking values so",
            "doctor can show warnings without using real credentials.",
        ]
    )
