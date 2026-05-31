from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from .ignore import is_ignored


MAX_TEXT_FILE_BYTES = 1_000_000
MAX_FINDINGS = 200

RISKY_EXACT_FILENAMES = {
    "id_rsa",
    "id_ed25519",
    "private_key",
    "private_key.pem",
    "credentials",
    "credentials.json",
}

SECRET_PATTERNS = [
    ("OPENAI_API_KEY", re.compile(r"\bOPENAI_API_KEY\b\s*[:=]|sk-[A-Za-z0-9_-]{20,}")),
    ("ANTHROPIC_API_KEY", re.compile(r"\bANTHROPIC_API_KEY\b\s*[:=]|sk-ant-[A-Za-z0-9_-]{20,}")),
    ("DEEPSEEK_API_KEY", re.compile(r"\bDEEPSEEK_API_KEY\b\s*[:=]")),
    ("AWS_ACCESS_KEY_ID", re.compile(r"\bAWS_ACCESS_KEY_ID\b\s*[:=]|\bA[KS]IA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bGITHUB_TOKEN\b\s*[:=]|\bgithub_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("access_token", re.compile(r"\baccess_token\b\s*[:=]")),
    ("refresh_token", re.compile(r"\brefresh_token\b\s*[:=]")),
]


@dataclass(frozen=True)
class Finding:
    path: str
    kind: str
    source: str
    severity: str = "HIGH"


def risky_filename(path: Path) -> str | None:
    name = path.name
    lower = name.lower()
    if lower in {".env.example", ".env.sample", ".env.template"}:
        return None
    if lower == ".env" or lower.startswith(".env."):
        return ".env file"
    if lower in RISKY_EXACT_FILENAMES:
        return lower
    if "private_key" in lower:
        return "private_key"
    return None


def should_exclude_from_snapshot(path: Path) -> bool:
    return risky_filename(path) is not None


def scan_text(text: str) -> list[str]:
    matches: list[str] = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            matches.append(label)
    return matches


def _looks_binary(data: bytes) -> bool:
    if not data:
        return False
    return b"\x00" in data[:4096]


def scan_repository(root: Path, patterns: list[str] | None = None) -> list[Finding]:
    root = root.resolve()
    if patterns is None:
        from .ignore import load_patterns

        ignore_patterns = load_patterns(root)
    else:
        ignore_patterns = patterns
    findings: list[Finding] = []

    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root).as_posix() if current_path != root else ""
        kept_dirs = []
        for directory in dirs:
            rel = f"{rel_dir}/{directory}".strip("/")
            if not is_ignored(rel, ignore_patterns, is_dir=True):
                kept_dirs.append(directory)
        dirs[:] = kept_dirs

        for filename in files:
            path = current_path / filename
            rel = path.relative_to(root).as_posix()
            if is_ignored(rel, ignore_patterns):
                continue

            risky = risky_filename(path)
            if risky:
                findings.append(Finding(rel, risky, "filename"))
                if len(findings) >= MAX_FINDINGS:
                    return findings

            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size > MAX_TEXT_FILE_BYTES:
                continue

            try:
                data = path.read_bytes()
            except OSError:
                continue
            if _looks_binary(data):
                continue

            text = data.decode("utf-8", errors="ignore")
            for kind in scan_text(text):
                findings.append(Finding(rel, kind, "content"))
                if len(findings) >= MAX_FINDINGS:
                    return findings

    return findings
