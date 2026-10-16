# Parallel Lanes Workflow

1. **Isolation**: When multiple builder lanes run concurrently, each lane operates in its own git worktree or branch `lane/<TASK-ID>-<lane>`.
2. **File Ownership Locks**: Tech Lead maps files exclusively to lanes in `03-plan.md`. Locks are recorded in `harness/state/locks/<lane>.json`.
3. **No Overlapping Paths**: Two parallel lanes must never own the same file path.
4. **Merge Discipline**: Lanes are merged sequentially into the task branch, triggering Gate G2 full unit suite check.
