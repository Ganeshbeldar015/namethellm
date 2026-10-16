# Git Commit Standards

1. **Commit Message Format**: Conventional Commits specification:
   `<type>(<scope>): <short description>`
   Types: `feat`, `fix`, `test`, `chore`, `docs`, `refactor`.
   Example: `feat(features): add punctuation stylometry extractor`
2. **Atomic Commits**: Stage transitions and task completions are committed atomically.
3. **No Destructive Operations**: `git push --force` and `git reset --hard origin` are strictly forbidden.
4. **Lane Branches**: When running parallel builder lanes, each lane works in `lane/<TASK-ID>-<lane>`.
