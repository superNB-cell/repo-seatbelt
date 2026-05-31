---
name: buckle-up
description: Use before asking an AI coding agent to modify a repository.
---

# Buckle Up

Use this skill before coding starts.

1. Confirm the current repository path.
2. Run or ask the user to run `seatbelt doctor`.
3. If risk is MEDIUM or HIGH, explain why and recommend fixes before coding.
4. Run or ask the user to run `seatbelt snapshot`.
5. Stay inside the repository.
6. Do not read secrets such as `.env`, private keys, API keys, token files, or credential stores.
7. Do not delete files outside the repository.
8. Do not use recursive destructive commands.
9. After changes, summarize changed files and tests run.

Safety rules:

- No network calls unless the user explicitly requests them.
- No background services.
- No destructive operations without explicit approval.

Example prompts:

- `/buckle-up before refactoring this project`
- `/buckle-up and check if this repo is safe for Codex changes`
