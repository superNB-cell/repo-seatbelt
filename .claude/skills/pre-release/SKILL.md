---
name: pre-release
description: Use before publishing repo-seatbelt or another project to GitHub.
---

# Pre Release

Use this skill before a manual release.

1. Check `README.md`.
2. Check `LICENSE`.
3. Check `pyproject.toml`.
4. Check tests.
5. Check GitHub Actions.
6. Check `CHANGELOG.md`.
7. Check `SECURITY.md`.
8. Check `CONTRIBUTING.md`.
9. Run tests.
10. Run `seatbelt doctor`.
11. Check for secrets and local-only files.
12. Verify example commands in the README.
13. Produce a release checklist.

Safety rules:

- Do not publish, push, tag, upload, or create releases automatically.
- Do not expose real secrets.
- No network calls unless explicitly requested.
- No background services.

Example prompts:

- `/pre-release check if this repo is ready for GitHub`
- `/pre-release prepare a release checklist`
