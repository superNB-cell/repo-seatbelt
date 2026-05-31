# Contributing

Thanks for helping make RepoSeatbelt useful and boringly safe.

## Local Setup

```powershell
python -m pip install -e .[dev]
pytest
```

## Filing Bugs

Please include:

- Operating system and shell
- Python version
- Command run
- Expected behavior
- Actual behavior

Do not paste real API keys, private keys, tokens, `.env` contents, or customer
data.

## Suggesting Features

Good feature requests explain the workflow, the risk being reduced, and how the
feature can stay local-first.

## Coding Style

- Prefer Python standard library for core v0.1 behavior.
- Keep functions small and focused.
- Keep terminal output friendly and plain.
- Avoid network calls, telemetry, and background services.
- Add tests for safety-sensitive behavior.

## Safety Expectations

- Do not add automatic destructive operations.
- Do not modify global shell profiles, registry, global Git config, or system
  environment variables.
- Do not install global hooks automatically.
- Keep generated files inside the repository.

## Good First Issue Ideas

- Improve `.gitignore` pattern compatibility.
- Add more tests for Windows-like paths.
- Improve report wording.
- Add more demo screenshots or GIFs.
- Expand rule templates without making them bloated.
