---
name: safe-refactor
description: Use for refactoring, cleanup, restructuring, packaging, polish, or large multi-file changes.
---

# Safe Refactor

Use this skill when the user asks for a refactor or broad cleanup.

1. Start with a small refactor plan.
2. Require a RepoSeatbelt snapshot before large changes.
3. Prefer small incremental edits.
4. Do not rewrite the whole project unless explicitly requested.
5. Preserve public behavior unless the task says otherwise.
6. Run tests after changes.
7. Produce a refactor report with changed files, risks, tests run, and next steps.

Safety rules:

- Stay inside the repository.
- Do not read or expose secrets.
- Do not run recursive destructive commands.
- Do not modify global config or install global tools.
- No network calls unless explicitly requested.

Example prompts:

- `/safe-refactor clean up the CLI modules`
- `/safe-refactor improve packaging without changing behavior`
