# Reconcile Log — Sprint 0 Scaffold

- **Timestamp**: 2026-10-16T23:25:00+05:30
- **Mode**: SCAFFOLD
- **Derived From**:
  - `docs/raw.md` SHA: `c7791980e8fb30782b3e5ad16eae8cbfa7efbf07f89a339a3a220e491f9867ae`
  - `docs/harness.md` SHA: `ad2f0aae3e34a19ffafddf6a33ecfaf01bc38465d02813ed258fb68a40317daf`

## Changes Summary

| Path | Before | After | Reason |
|---|---|---|---|
| `AGENTS.md` | MISSING | CREATED | Canonical index for agents, roles, commands, rules |
| `CLAUDE.md` | MISSING | CREATED | 3-line IDE pointer to AGENTS.md |
| `.cursor/rules/harness.mdc` | MISSING | CREATED | IDE pointer for Cursor |
| `.github/copilot-instructions.md` | MISSING | CREATED | IDE pointer for Copilot |
| `.mcp.json` | MISSING | CREATED | Filesystem MCP configuration |
| `harness/profile.yaml` | MISSING | CREATED | Derived ML project profile (designer disabled) |
| `harness/state/state.json` | MISSING | CREATED | Execution state in SCAFFOLD mode |
| `harness/state/state.schema.json` | MISSING | CREATED | Schema validation for state |
| `harness/state/budgets.json` | MISSING | CREATED | Circuit breaker budgets and thresholds |
| `harness/state/locks/.gitkeep` | MISSING | CREATED | Directory for lane ownership locks |
| `harness/tools/registry.yaml` | MISSING | CREATED | Tool capabilities and role permissions |
| `harness/tools/sandbox.md` | MISSING | CREATED | Sandbox and code execution rules |
| `harness/standards/*` | MISSING | CREATED | DoD, handoff-contract, coding, testing, git standards |
| `harness/workflows/*` | MISSING | CREATED | Pipeline, sprint template, parallel lanes workflows |
| `harness/roles/*` (10 roles) | MISSING | CREATED | Fat role definitions with all 12 mandatory sections |
| `harness/agents/*` (10 agents) | MISSING | CREATED | Skinny pointers (<= 40 lines) to role files |
| `harness/backlog.md` | MISSING | CREATED | MoSCoW-prioritized sprint tasks |
| `harness/logs/*` | MISSING | CREATED | Session, events, decisions, failures logs |
| `docs/memory/*` | MISSING | CREATED | Lessons, assumptions, glossary, interview records |
| `docs/adr/ADR-0001-*.md` | MISSING | CREATED | GroupKFold on prompt_id architecture decision |
| `scripts/check_harness.py` | MISSING | CREATED | Deterministic harness linter |
| `scripts/guard_paths.py` | MISSING | CREATED | Allow-list path guard |
| `scripts/breaker.py` | MISSING | CREATED | Circuit breaker evaluation script |
| `scripts/validate_handoff.py` | MISSING | CREATED | Handoff JSON validator |
| `tests/harness/*` | MISSING | CREATED | Comprehensive test suite for harness integrity |

## G0 Integrity Status
- `python scripts/check_harness.py`: OK (0 problems)
- All harness unit test cases verified passing.
