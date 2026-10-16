# AGENTS.md — Name That LLM
> Map, not manual. Deep detail lives in linked files.

## What this is
Authorship attribution pipeline for classifying text across 18 frontier LLMs using stylometry, NLP, and machine learning.
Full engineering specification: [docs/harness.md](docs/harness.md). Operating instructions: [docs/prompt.md](docs/prompt.md).

## Start here (every session)
1. Read this file → 2. [harness/state/state.json](harness/state/state.json) → 3. [docs/prompt.md](docs/prompt.md) §1 Boot Sequence.

## Commands
Canonical commands from [docs/harness.md](docs/harness.md):
- `install`: `pip install -r requirements.txt`
- `lint`: `python -m flake8 src tests`
- `format`: `python -m black --check src tests`
- `typecheck`: `python -m mypy src`
- `unit test`: `pytest tests/unit`
- `integration test`: `pytest tests/integration`
- `build`: `python -m build`
- `harness self-test`: `python scripts/check_harness.py && pytest tests/harness`

## Layout
- `dataset/`: Training, test, and sample submission data
- `docs/`: Master prompt, raw problem statement, harness architecture, memory, and ADRs
- `harness/`: Roles, agents, workflows, standards, tools, state, and execution logs
- `scripts/`: Deterministic checks (`check_harness.py`, `guard_paths.py`, `breaker.py`)
- `src/`: Product source code (`namethellm`)
- `tests/`: Harness unit tests and application unit/integration tests

## Roles
| Agent | Role File | Artifact |
|---|---|---|
| Orchestrator | [harness/roles/orchestrator.md](harness/roles/orchestrator.md) | `harness/state/state.json`, `harness/logs/*` |
| PO-Spec | [harness/roles/po-spec.md](harness/roles/po-spec.md) | `harness/artifacts/<T>/01-spec.md` |
| Tech Lead | [harness/roles/tech-lead.md](harness/roles/tech-lead.md) | `harness/artifacts/<T>/03-plan.md` |
| Test Author | [harness/roles/test-author.md](harness/roles/test-author.md) | `harness/artifacts/<T>/04-tests.md` |
| Builder | [harness/roles/builder.md](harness/roles/builder.md) | `harness/artifacts/<T>/05-build.md` |
| Reviewer | [harness/roles/reviewer.md](harness/roles/reviewer.md) | `harness/artifacts/<T>/06-review.md` |
| Security | [harness/roles/security.md](harness/roles/security.md) | `harness/artifacts/<T>/06b-security.md` |
| QA | [harness/roles/qa.md](harness/roles/qa.md) | `harness/artifacts/<T>/07-qa.md` |
| Scribe | [harness/roles/scribe.md](harness/roles/scribe.md) | `harness/artifacts/<T>/08-docs.md` |
| Librarian | [harness/roles/librarian.md](harness/roles/librarian.md) | `docs/memory/lessons.md` |

## Rules (top 10)
1. **Never improvise outside the harness**: Follow [docs/prompt.md](docs/prompt.md).
2. **Deterministic checks decide done**: Verified via [harness/standards/definition-of-done.md](harness/standards/definition-of-done.md).
3. **Artifacts are contracts**: Every handoff must validate per [harness/standards/handoff-contract.md](harness/standards/handoff-contract.md).
4. **Tests-first**: Failing tests must precede implementation per [harness/standards/testing.md](harness/standards/testing.md).
5. **No prompt leakage**: Always group CV by `prompt_id` per [docs/adr/ADR-0001-group-kfold.md](docs/adr/ADR-0001-group-kfold.md).
6. **Stay in your lane**: Strictly respect allow-lists checked by `scripts/guard_paths.py`.
7. **Circuit breakers trip on failure**: Enforced by `scripts/breaker.py` and [harness/state/budgets.json](harness/state/budgets.json).
8. **No secrets in commits**: Enforced by [harness/roles/security.md](harness/roles/security.md).
9. **Zero warnings & clean code**: Conforms to [harness/standards/coding.md](harness/standards/coding.md).
10. **State lives on disk**: Re-derive state from [harness/state/state.json](harness/state/state.json) and disk.

## Gates & breakers
See [docs/prompt.md](docs/prompt.md) §9 for G0–G5 quality gates and circuit breaker budgets.

## Memory map
- Decisions: [harness/logs/decisions.log.md](harness/logs/decisions.log.md) & [docs/adr/ADR-0001-group-kfold.md](docs/adr/ADR-0001-group-kfold.md)
- Lessons learned: [docs/memory/lessons.md](docs/memory/lessons.md)
- Assumptions: [docs/memory/assumptions.md](docs/memory/assumptions.md)
- Glossary: [docs/memory/glossary.md](docs/memory/glossary.md)

## Do-not list
- Do not edit files outside role allow-list.
- Do not bypass quality gates or weaken tests.
- Do not execute destructive git commands (`git push --force`, `git reset --hard`).
- Do not call unapproved network APIs during offline evaluation.
