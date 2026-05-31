# Claude Code Skills

RepoSeatbelt includes optional Claude Code skills in:

```text
.claude/skills/
```

## Skills

- `/buckle-up`
- `/safe-refactor`
- `/pre-release`

The CLI works without Claude Code. Skills are optional prompts/workflows that
encourage safer AI-assisted development.

## Limitations

Skills do not replace sandboxing, Git, or real backups. They should not run
network calls, background services, or destructive operations automatically.
