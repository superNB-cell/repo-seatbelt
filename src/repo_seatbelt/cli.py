from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import initialize
from .demo import demo_walkthrough
from .doctor import format_doctor, run_doctor
from .errors import SeatbeltError
from .report import latest_snapshot_line, write_report
from .restore import confirmation_phrase, find_snapshot, restore_snapshot
from .rules import targets_for_flags, write_rules
from .snapshot import create_snapshot, human_size, list_snapshots


def _print_written(written: list[tuple[Path, Path | None]]) -> None:
    for path, backup in written:
        print(f"[OK] wrote {path}")
        if backup:
            print(f"     backup: {backup}")


def cmd_init(args: argparse.Namespace) -> int:
    root = Path.cwd()
    written = initialize(root)
    print("[OK] RepoSeatbelt initialized.")
    _print_written(written)
    print("")
    print("Next steps:")
    print("  seatbelt doctor")
    print("  seatbelt snapshot")
    print("  seatbelt rules --codex --claude --cursor")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    result = run_doctor(Path.cwd())
    print(format_doctor(result))
    return 2 if result.risk == "HIGH" else 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    result = create_snapshot(Path.cwd())
    print(f"[OK] Snapshot created: {result.path}")
    print(f"[INFO] Files included: {result.file_count}")
    print(f"[INFO] Size: {human_size(result.size_bytes)}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    root = Path.cwd()
    if not args.snapshot:
        snapshots = list_snapshots(root)
        if not snapshots:
            print("[INFO] No snapshots found.")
            return 0
        print("Available snapshots:")
        for snapshot in snapshots:
            print(f"- {snapshot.name} ({human_size(snapshot.stat().st_size)})")
        print("")
        print("Run: seatbelt restore <snapshot-name>")
        return 0

    snapshot = find_snapshot(root, args.snapshot)
    phrase = confirmation_phrase(snapshot)
    print(f"Restore snapshot: {snapshot.name}")
    print(f"This will create a new folder and will not overwrite the current project.")
    typed = input(f"Type '{phrase}' to continue: ")
    result = restore_snapshot(root, snapshot, typed)
    print(f"[OK] Restored {result.file_count} files into: {result.destination}")
    print("[INFO] Compare the restored folder manually before copying files back.")
    return 0


def cmd_rules(args: argparse.Namespace) -> int:
    root = Path.cwd()
    targets = targets_for_flags(claude=args.claude, cursor=args.cursor, codex=args.codex, agents=args.agents)
    written = write_rules(root, targets)
    print("[OK] Safety rules generated.")
    _print_written(written)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    root = Path.cwd()
    result = run_doctor(root)
    print(format_doctor(result))
    print(latest_snapshot_line(root))
    path = write_report(root)
    print(f"[OK] Report written: {path}")
    return 2 if result.risk == "HIGH" else 0


def cmd_demo(args: argparse.Namespace) -> int:
    print(demo_walkthrough())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seatbelt",
        description="RepoSeatbelt: buckle up before you vibe-code.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create local safety config and rules")
    init_parser.set_defaults(func=cmd_init)

    doctor_parser = subparsers.add_parser("doctor", help="check path, git status, and likely secrets")
    doctor_parser.set_defaults(func=cmd_doctor)

    snapshot_parser = subparsers.add_parser("snapshot", help="create a timestamped zip snapshot")
    snapshot_parser.set_defaults(func=cmd_snapshot)

    restore_parser = subparsers.add_parser("restore", help="list or restore snapshots")
    restore_parser.add_argument("snapshot", nargs="?", help="snapshot zip filename to restore")
    restore_parser.set_defaults(func=cmd_restore)

    rules_parser = subparsers.add_parser("rules", help="generate AI-agent safety rules")
    rules_parser.add_argument("--claude", action="store_true", help="also create CLAUDE.md")
    rules_parser.add_argument("--cursor", action="store_true", help="also create .cursorrules")
    rules_parser.add_argument("--codex", action="store_true", help="also create CODEX_RULES.md")
    rules_parser.add_argument("--agents", action="store_true", help="create AGENTS.md")
    rules_parser.set_defaults(func=cmd_rules)

    report_parser = subparsers.add_parser("report", help="write .repo-seatbelt/report.md")
    report_parser.set_defaults(func=cmd_report)

    demo_parser = subparsers.add_parser("demo", help="print a safe guided demo walkthrough")
    demo_parser.set_defaults(func=cmd_demo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except SeatbeltError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCanceled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
