# FAQ

## Is this a sandbox?

No. RepoSeatbelt is a local safety helper, not a sandbox.

## Is this antivirus?

No. RepoSeatbelt is not antivirus and does not scan for malware.

## Is this a guarantee?

No. RepoSeatbelt can reduce risk, but it cannot guarantee protection.

## Does it stop Codex from deleting files?

No. It creates checks, rules, and snapshots that reduce risk, but it cannot
guarantee another tool will behave safely.

## Does it upload my code?

No. RepoSeatbelt has no network calls or telemetry.

## Does it read my secrets?

It scans small text files for likely secret patterns and reports paths and
finding kinds. It should not print secret values.

## Does it work on Windows?

Yes. Windows and PowerShell are the first-class workflow.

## Does it work without Claude Code?

Yes. Claude Code skills are optional.

## Why does pip install -e . fail on my machine?

Editable install can fail if your Python packaging environment cannot import
`setuptools.build_meta`, install build backend dependencies, or reach package
indexes. That is usually an environment problem rather than a RepoSeatbelt CLI
bug.

You can still try source mode:

```powershell
$env:PYTHONPATH="$PWD\src"
.\.venv\Scripts\python.exe -m repo_seatbelt.cli --help
```

Or use the no-install fallback launcher:

```powershell
py seatbelt.py --help
py seatbelt.py doctor
```

The normal install command is still:

```powershell
python -m pip install -e .
```

## Why not just use Git?

Use Git too. RepoSeatbelt adds pre-agent checks, local snapshots, rule files,
and reports. It is not a replacement for Git or real backups.

## Why restore into a new folder?

Restoring into a new folder avoids overwriting or deleting the current project.

## Can I use it with Cursor?

Yes. Use `seatbelt rules --cursor` to generate `.cursorrules`.

## Can I use it with Claude Code?

Yes. Use `seatbelt rules --claude` and the optional skills.

## Can I use it with Gemini CLI?

Yes. Use the general `AGENTS.md` rules and the CLI workflow.
