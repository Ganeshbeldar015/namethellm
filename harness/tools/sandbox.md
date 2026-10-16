# Bash and Code Execution Sandbox Rules

1. **Working Directory Isolation**: Commands must execute exclusively inside the repository root (`D:\WorkSpace\Project\namethellm`) or `./tmp`. Never access home directories, root system directories, or other repositories.
2. **Authorized Commands Only**: Run only canonical commands explicitly enumerated in `docs/harness.md` Section 8, plus standard read-only inspection utilities (`git status`, `git diff`, `git log`, `python`).
3. **Hermetic Execution**: No outbound network requests during evaluation or test prediction runs.
4. **Safety & Destructive Operations**:
   - `rm -rf` is forbidden outside `./tmp` or `__pycache__` / `.pytest_cache`.
   - `sudo` is strictly forbidden.
   - Force push (`git push --force`) or destructive hard resets are forbidden.
5. **Secret Protection**: Never echo, log, or commit secret keys, credentials, or API tokens.
6. **Execution Limits**: Per-command execution timeout is 120 seconds.
7. **Audit Logging**: Every command execution and exit code must be recorded in `harness/logs/events.jsonl`.
