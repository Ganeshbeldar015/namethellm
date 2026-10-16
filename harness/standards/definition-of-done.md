# Definition of Done (DoD)

A task in this repository is strictly **Done** when all of the following conditions are met:

1. **Artifact Trail**: All expected stage artifacts (`01-spec.md` through `08-docs.md`) exist under `harness/artifacts/<TASK-ID>/`, and each handoff JSON is validated by `scripts/validate_handoff.py`.
2. **Quality Gates G0–G4 Green**:
   - **G0**: Harness integrity (`check_harness.py` exits 0).
   - **G1**: Lane gate (code formatting, linting, typecheck, lane unit tests pass).
   - **G2**: Merge gate (full unit suite passes, test coverage >= 80% on changed lines).
   - **G3**: Review gate (0 BLOCKER, 0 MAJOR findings, 0 high/critical security vulnerabilities, 0 exposed secrets).
   - **G4**: QA gate (all acceptance criteria have passing test evidence; no skipped or xfail tests added).
3. **Guard Compliance**: `scripts/guard_paths.py` reports zero allow-list violations.
4. **Circuit Breakers**: `scripts/breaker.py` reports breaker is not tripped; all actions within budgets.
5. **No Open Questions**: All requirement ambiguities resolved or formally logged as assumptions.
6. **Documentation & Memory**: Scribe updated project documentation and README/CHANGELOG; Librarian captured lessons in `docs/memory/lessons.md`.
7. **State & Logs**: `harness/state/state.json` reflects task completion; events appended to `harness/logs/events.jsonl`.
