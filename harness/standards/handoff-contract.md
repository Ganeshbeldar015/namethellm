# Handoff Contract Standard

Every stage handoff in the harness must produce a valid JSON artifact named:
`harness/artifacts/<TASK-ID>/handoff-<from>-to-<to>.json`

## Schema

```json
{
  "task_id": "T-0001",
  "from": "tech-lead",
  "to": "test-author",
  "artifact": "harness/artifacts/T-0001/03-plan.md",
  "status": "complete | blocked | needs-info",
  "summary": "Summary of stage output (<= 120 words)",
  "inputs_consumed": ["01-spec.md", "02-design.md"],
  "acceptance_refs": ["AC-001-a", "AC-001-b"],
  "open_questions": [],
  "assumptions": [],
  "files_touched": ["src/..."],
  "checks_run": [{"cmd": "pytest tests/...", "exit": 0}],
  "next_expected_artifact": "04-tests.md"
}
```

## Rejection Rules

The Orchestrator automatically rejects a handoff if:
1. The referenced artifact does not exist on disk.
2. `status` is not `"complete"`.
3. Any ID in `acceptance_refs` does not exist in `docs/harness.md`.
4. Any path in `files_touched` is outside the role's write allow-list.
5. `checks_run` is empty for roles required to run checks (`builder`, `qa`, `security`).
