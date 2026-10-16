#!/usr/bin/env python3
"""Circuit breaker monitor for harness tasks."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_BUDGETS = {
    "max_stage_retries": 3,
    "max_identical_failures": 2,
    "max_diff_lines_per_lane": 400,
    "max_files_per_lane": 15,
    "max_parallel_agents": 3,
    "max_session_minutes": 90,
    "max_tool_calls_per_stage": 150,
    "no_progress_window": 3,
}


def compute_failure_signature(test_names: list, error_text: str) -> str:
    content = "|".join(sorted(test_names)) + ":" + error_text.strip()
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def check_trip_conditions(
    budgets: dict,
    stage_retries: int = 0,
    identical_failure_count: int = 0,
    diff_lines: int = 0,
    files_changed: int = 0,
    guard_violation: bool = False,
    unapproved_tool_used: bool = False,
    progress_history: list = None,
    session_minutes: float = 0.0,
    tool_calls: int = 0,
    malformed_artifact_count: int = 0,
) -> tuple[bool, str]:
    """Evaluates the 8 circuit breaker conditions. Returns (tripped, reason)."""
    # 1. Same stage failed > max_stage_retries
    if stage_retries > budgets.get("max_stage_retries", DEFAULT_BUDGETS["max_stage_retries"]):
        return True, f"Stage retries ({stage_retries}) exceeded max_stage_retries ({budgets['max_stage_retries']})"

    # 2. Same failure signature repeated >= max_identical_failures times
    if identical_failure_count >= budgets.get("max_identical_failures", DEFAULT_BUDGETS["max_identical_failures"]):
        return True, f"Identical failure occurred {identical_failure_count} times, reaching threshold"

    # 3. Diff exceeds limits
    if diff_lines > budgets.get("max_diff_lines_per_lane", DEFAULT_BUDGETS["max_diff_lines_per_lane"]):
        return True, f"Diff size ({diff_lines} lines) exceeded max_diff_lines_per_lane"
    if files_changed > budgets.get("max_files_per_lane", DEFAULT_BUDGETS["max_files_per_lane"]):
        return True, f"Files changed ({files_changed}) exceeded max_files_per_lane"

    # 4. Guard violation
    if guard_violation:
        return True, "Guard violation detected: attempted write outside role allow-list"

    # 5. Forbidden / unapproved tool
    if unapproved_tool_used:
        return True, "Forbidden or unapproved tool call attempted"

    # 6. No progress
    window = budgets.get("no_progress_window", DEFAULT_BUDGETS["no_progress_window"])
    if progress_history and len(progress_history) >= window:
        recent = progress_history[-window:]
        # If failure count did not decrease over the window
        if all(recent[i] <= recent[i + 1] for i in range(len(recent) - 1)):
            return True, f"No progress observed over the last {window} iterations"

    # 7. Budget exhaustion
    if session_minutes > budgets.get("max_session_minutes", DEFAULT_BUDGETS["max_session_minutes"]):
        return True, f"Session duration ({session_minutes}m) exceeded budget ({budgets['max_session_minutes']}m)"
    if tool_calls > budgets.get("max_tool_calls_per_stage", DEFAULT_BUDGETS["max_tool_calls_per_stage"]):
        return True, f"Tool calls ({tool_calls}) exceeded stage budget ({budgets['max_tool_calls_per_stage']})"

    # 8. Malformed artifact twice in a row
    if malformed_artifact_count >= 2:
        return True, f"Required artifact or handoff malformed {malformed_artifact_count} times consecutively"

    return False, ""


def trip(reason: str, root: Path = ROOT):
    state_file = root / "harness/state/state.json"
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
            state["breaker"] = {"tripped": True, "reason": reason}
            state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except Exception:
            pass

    failures_log = root / "harness/logs/failures.log.md"
    failures_log.parent.mkdir(parents=True, exist_ok=True)
    with failures_log.open("a", encoding="utf-8") as f:
        f.write(f"\n### BREAKER TRIPPED | {reason}\n")


def main(argv=None):
    budgets_file = ROOT / "harness/state/budgets.json"
    budgets = json.loads(budgets_file.read_text(encoding="utf-8")) if budgets_file.exists() else DEFAULT_BUDGETS
    tripped, reason = check_trip_conditions(budgets)
    if tripped:
        print(f"BREAKER TRIPPED: {reason}", file=sys.stderr)
        return 1
    print("Breaker status: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
