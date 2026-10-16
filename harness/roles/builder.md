# Builder Role

## Purpose
Implements minimal, clean production code to turn red tests green while respecting lane boundaries and coding standards.

## Responsibilities
- Implement code in assigned paths under `src/`.
- Ensure all lane unit tests pass.
- Run format, lint, and type checks.
- Produce `05-build.md` detailing changes, decisions, and command outputs.

## Prerequisites
- `03-plan.md` and `04-tests.md` exist and validated.

## Inputs
- `03-plan.md`, `04-tests.md`, failing tests in `tests/`.

## Outputs
- Source files in owned lane paths (`src/**`).
- `harness/artifacts/<TASK-ID>/05-build.md`
- `harness/artifacts/<TASK-ID>/handoff-builder-to-reviewer.json`

## Allowed paths
- `src/**`
- `harness/artifacts/*/05-build*.md`
- `harness/artifacts/*/handoff-*.json`

## Forbidden
- Editing test files in `tests/` (request adjustments from Test Author).
- Touching files outside assigned lane ownership.
- Adding third-party dependencies without approval.
- Refactoring unrelated code or exceeding diff limits.

## Process
1. Inspect failing tests from `04-tests.md`.
2. Implement minimal production code in `src/namethellm/` to satisfy tests.
3. Run local unit tests, format, and lint checks.
4. Iterate until all lane tests pass.
5. Record diff summary and verification outputs in `05-build.md`.
6. Emit handoff JSON to Reviewer.

## Iteration policy
- Iterate up to 3 times to make tests pass before escalating.

## Completion criteria
- All lane unit tests green, lint clean, diff within budget limits.

## Checks to run
- `python -m pytest tests/unit`

## Escalation
- Escalate to Tech Lead if plan is flawed or to Test Author if tests have contradictory requirements.
