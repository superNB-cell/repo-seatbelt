# Codex Safety Rules

Use these rules when Codex is editing this repository.

## Repository Boundary

- Stay inside this repository.
- Never delete, move, rewrite, or clean files outside this repository.
- Never clean `C:\`, drive roots, user home, Desktop, Documents, Downloads,
  caches, temp folders, or global/system paths.
- Do not modify global shell profiles, system configuration, registry settings,
  global Git config, system environment variables, caches, temp folders, or user
  directories.
- Do not install global tools, hooks, services, daemons, startup tasks, or
  background processes.
- Do not run network operations unless the human explicitly requests them.

## Destructive Commands

- Ask before running destructive commands.
- Do not run recursive destructive commands such as `rm -rf`, `rmdir /s`,
  `del /s`, `Remove-Item -Recurse`, `git clean -fdx`, or `git reset --hard`.
- If unsure, stop and ask instead of guessing.

## Snapshots and Recovery

- Create a RepoSeatbelt snapshot before large refactors, dependency migrations,
  generated-code rewrites, or multi-file transformations.
- Restore only into a new folder unless the human explicitly chooses another
  recovery path.

## Secrets

- Do not read secrets unless the task explicitly requires it.
- Do not expose API keys, private keys, tokens, `.env` contents, credentials,
  or signing material in prompts, logs, commits, screenshots, or reports.
- If likely secrets are found, stop and ask the human how to proceed.

## Testing and Summaries

- Run relevant tests after modifications when tests are available.
- After each task, summarize changed files and the reason for each change.
- Call out tests run, tests skipped, and any residual risk.

## Codex Workflow

- Read the existing code before editing.
- Prefer small, reviewable patches.
- Do not stage, commit, push, tag, or publish unless the human asks.
