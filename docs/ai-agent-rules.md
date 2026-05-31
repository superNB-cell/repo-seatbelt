# AI-Agent Rules

RepoSeatbelt can generate rule files for AI coding agents.

## Files

- `AGENTS.md`: General rules for Codex and other AI coding agents.
- `CODEX_RULES.md`: Codex-focused rules.
- `CLAUDE.md`: Claude Code style rules.
- `.cursorrules`: Cursor rules.

## Commands

```powershell
seatbelt rules
seatbelt rules --agents --codex --claude --cursor
```

If no flag is provided, RepoSeatbelt writes `AGENTS.md`.

## Customizing

Edit generated files to match your project. Keep the safety basics:

- Stay inside the repository.
- Ask before destructive commands.
- Create snapshots before large refactors.
- Do not read or expose secrets.
- Run tests after modifications.
- Summarize changed files after each task.

## Limitations

Rules guide agents, but they do not enforce a sandbox. Use Git, backups, and
careful review for important work.
