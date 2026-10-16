import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import breaker


def test_failure_signature_hashing():
    sig1 = breaker.compute_failure_signature(["test_a", "test_b"], "AssertionError: 1 != 2")
    sig2 = breaker.compute_failure_signature(["test_b", "test_a"], "AssertionError: 1 != 2")
    sig3 = breaker.compute_failure_signature(["test_a"], "AssertionError: 1 != 2")
    assert sig1 == sig2
    assert sig1 != sig3


def test_breaker_condition_1_stage_retries():
    budgets = {"max_stage_retries": 3}
    tripped, reason = breaker.check_trip_conditions(budgets, stage_retries=4)
    assert tripped
    assert "Stage retries (4) exceeded" in reason


def test_breaker_condition_2_identical_failures():
    budgets = {"max_identical_failures": 2}
    tripped, reason = breaker.check_trip_conditions(budgets, identical_failure_count=2)
    assert tripped
    assert "Identical failure" in reason


def test_breaker_condition_3_diff_limits():
    budgets = {"max_diff_lines_per_lane": 400, "max_files_per_lane": 15}
    tripped, _ = breaker.check_trip_conditions(budgets, diff_lines=450)
    assert tripped
    tripped, _ = breaker.check_trip_conditions(budgets, files_changed=16)
    assert tripped


def test_breaker_condition_4_guard_violation():
    tripped, reason = breaker.check_trip_conditions({}, guard_violation=True)
    assert tripped
    assert "Guard violation" in reason


def test_breaker_condition_5_unapproved_tool():
    tripped, reason = breaker.check_trip_conditions({}, unapproved_tool_used=True)
    assert tripped
    assert "unapproved tool" in reason


def test_breaker_condition_6_no_progress():
    budgets = {"no_progress_window": 3}
    # Failing test counts: 5 -> 5 -> 5 (no progress)
    tripped, reason = breaker.check_trip_conditions(budgets, progress_history=[5, 5, 5])
    assert tripped
    assert "No progress" in reason

    # Progress made: 5 -> 4 -> 3
    tripped, _ = breaker.check_trip_conditions(budgets, progress_history=[5, 4, 3])
    assert not tripped


def test_breaker_condition_7_budget_exhaustion():
    budgets = {"max_session_minutes": 90, "max_tool_calls_per_stage": 150}
    tripped, _ = breaker.check_trip_conditions(budgets, session_minutes=95.0)
    assert tripped
    tripped, _ = breaker.check_trip_conditions(budgets, tool_calls=155)
    assert tripped


def test_breaker_condition_8_consecutive_malformed_artifacts():
    tripped, reason = breaker.check_trip_conditions({}, malformed_artifact_count=2)
    assert tripped
    assert "malformed" in reason
