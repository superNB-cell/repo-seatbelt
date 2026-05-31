# Windows-First Design

RepoSeatbelt prioritizes Windows users because many AI-assisted projects start
in PowerShell and live in folders like Desktop or Documents.

## Why Paths Matter

Risky locations include:

- `C:\` and other drive roots
- User home
- Desktop
- Documents
- Downloads
- Temp roots
- Cache roots

These folders often contain unrelated personal files. RepoSeatbelt warns before
an AI coding agent starts editing from one of those locations.

## Local Keys

Developers often keep local API keys or tokens in project files while
experimenting. RepoSeatbelt looks for likely secret filenames and small text
files with common key names. It reports the path and kind of issue without
printing secret values.

## What It Checks

- Path safety
- Git availability and repository status
- Uncommitted Git changes when Git is available
- Likely secrets and risky filenames
- Snapshot availability in reports

RepoSeatbelt helps reduce risk, but it is not a sandbox or guarantee.
