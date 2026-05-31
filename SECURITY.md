# Security

RepoSeatbelt is local-first. It has no telemetry, no network calls, no secret
collection, and no background service.

## Reporting Vulnerabilities

Please open a private security advisory if the repository host supports it, or
contact the maintainers through the project issue tracker with a minimal
description. Do not include real secrets in reports.

## Design Limits

RepoSeatbelt is a safety helper, not a sandbox or guarantee. It cannot fully
prevent another tool from deleting files, reading secrets, or running unsafe
commands. It helps users check risky conditions, create snapshots, and write
agent rules before work begins.

## Local-Only Expectations

- No telemetry.
- No network calls.
- No secret collection.
- No background services.
- No global shell profile changes.
- No registry changes.
- No global Git config changes.
