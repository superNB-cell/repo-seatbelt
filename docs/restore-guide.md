# Restore Guide

RepoSeatbelt snapshots are timestamped zip files stored in:

```text
.repo-seatbelt/snapshots/
```

## What Is Excluded

RepoSeatbelt respects `.seatbeltignore` and `.gitignore` where possible. It
always excludes `.repo-seatbelt/snapshots/` and skips obvious secret filenames
such as `.env` and private key files by default.

## Restoring

List snapshots:

```powershell
seatbelt restore
```

Restore one snapshot:

```powershell
seatbelt restore repo-seatbelt_20260531_120000.zip
```

RepoSeatbelt asks for typed confirmation and restores into a new
`restored_<timestamp>` folder. It does not overwrite or delete the current
project.

## Comparing Files

After restore, manually compare the restored folder against your current
project with your editor, Git, or a diff tool.

## Limitations

Snapshots are a lightweight local helper. They are not a replacement for Git,
real backups, or a full sandbox.
