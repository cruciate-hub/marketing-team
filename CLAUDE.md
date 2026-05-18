# Project conventions

## Commit attribution

When committing on behalf of this user, use the generic co-author line:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

Do **not** include the specific model version (e.g. `Claude Opus 4.7 (1M context)`) — the Claude Code auto-mode classifier rejects model-specific co-author attribution as impersonation, so any commit using a model-version line fails to land. The generic form is the only attribution that consistently lands across model versions.
