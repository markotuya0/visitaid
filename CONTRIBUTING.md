# Contributing to VisitAid

## Git Workflow

### Branches

- **`main`** — Production-ready code only. Never commit directly here.
- **Feature branches** — All work happens here first.

### Branch Naming

Use this format: `type/short-description`

| Type | When to use | Example |
|------|-------------|---------|
| `feature/` | New functionality | `feature/add-text-reading` |
| `fix/` | Bug fixes | `fix/audio-delay` |
| `chore/` | Maintenance, config, deps | `chore/update-dependencies` |
| `docs/` | Documentation only | `docs/add-readme` |
| `refactor/` | Code restructuring | `refactor/simplify-agent` |

### Commit Messages

Format: `type(scope): description`

```
feat(agent): add YOLO obstacle detection
fix(tts): resolve audio cutoff issue
chore(deps): update vision-agents to 0.4.0
docs(readme): add setup instructions
refactor(processors): extract common logic
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `chore` — Maintenance (deps, config, build)
- `docs` — Documentation changes
- `refactor` — Code change that doesn't add features or fix bugs

**Scope:** The part of the codebase affected (agent, tts, stt, processors, etc.)

### Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout main
   git checkout -b feature/your-feature-name
   ```

2. Make commits with clear messages:
   ```bash
   git add <files>
   git commit -m "feat(agent): add obstacle warning system"
   ```

3. When done, merge into `main`:
   ```bash
   git checkout main
   git merge feature/your-feature-name
   git branch -d feature/your-feature-name  # delete the branch
   ```

### Rules

- Never commit `.env` — it contains API keys
- Never push directly to `main` — always use feature branches
- Keep commits small and focused
- Write commit messages in present tense ("add" not "added")
