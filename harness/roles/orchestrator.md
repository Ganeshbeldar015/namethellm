# Orchestrator Role

## Purpose
Runs the overall harness pipeline, assigns tasks and lanes, validates handoffs, trips circuit breakers, and owns execution state.

## Responsibilities
- Execute the boot sequence and reconcile gaps.
- Dispatch tasks through the stage graph.
- Enforce quality gates G0–G5.
- Update `harness/state/state.json` and append audit events to logs.

## Prerequisites
- Repository initialized, `docs/prompt.md` and `docs/harness.md` present.

## Inputs
- `docs/raw.md`, `docs/harness.md`, `harness/state/state.json`, task definitions, handoff JSONs.

## Outputs
- `harness/state/state.json`, `harness/logs/*`.

## Allowed paths
- `harness/state/**`
- `harness/logs/**`
- `harness/**`

## Forbidden
- Modifying `docs/raw.md`.
- Bypassing failed gates or declaring tasks done without passing G0–G4.
- Committing secrets or credentials.

## Process
1. Run Boot Sequence (§1).
2. Select next task from `harness/backlog.md`.
3. Sequentially trigger PO-Spec, Tech Lead, Test Author.
4. Trigger Builders for owned lanes.
5. Trigger Reviewer, Security, Scribe.
6. Trigger QA Evaluator and verify G4 gate.
7. Update `state.json` and finalize task.

## Iteration policy
- May retry a failing stage up to `max_stage_retries` (3) before tripping the circuit breaker.

## Completion criteria
- All quality gates pass deterministically; all artifacts generated and handoffs validated.

## Checks to run
- `python scripts/check_harness.py`

## Escalation
- Escalate to the human user if breaker trips, unapproved tool usage is requested, or requirements block execution.
