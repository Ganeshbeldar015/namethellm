# Sprint Template Workflow

Every sprint follows this structure:

1. **Sprint Planning**:
   - Review `harness/backlog.md`.
   - Select tasks for the sprint.
   - Elaborate task definitions into `harness/tasks/<ID>.md`.
   - Pre-create skeleton directories `harness/artifacts/<ID>/`.
2. **Sprint Execution**:
   - Execute the pipeline for each selected task.
   - Run gates G0 through G4 per task.
3. **Sprint Review**:
   - Evaluate demo artifacts, Kaggle test benchmark scores, and OOF balanced accuracy.
   - Human sign-off logged in `harness/logs/decisions.log.md`.
4. **Sprint Retrospective**:
   - Analyze retries, breaker trips, and metrics.
   - Librarian proposes harness adjustments.
   - Commit retro findings to `docs/memory/lessons.md`.
