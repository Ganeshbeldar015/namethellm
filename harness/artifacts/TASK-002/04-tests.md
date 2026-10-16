---
status: complete
owner: test-author
task: TASK-002
inputs:
  - harness/artifacts/TASK-002/01-spec.md
  - harness/artifacts/TASK-002/03-plan.md
---
# 04-tests.md — Tests for TASK-002

## 1. Traceability Matrix

| Acceptance Criteria | Test Function | Test File |
|---|---|---|
| `AC-003-a` | `test_balanced_accuracy_matches_sklearn` | `tests/unit/test_metrics.py` |
| `AC-003-a` | `test_per_class_recall_matches_mean_balanced_accuracy` | `tests/unit/test_metrics.py` |
| `AC-003-a` | `test_perfect_accuracy` | `tests/unit/test_metrics.py` |
| `AC-003-a` | `test_zero_recall_no_division_error` | `tests/unit/test_metrics.py` |
| `AC-005-a` | `test_baseline_classifier_fit_predict` | `tests/unit/test_baseline.py` |
| `AC-005-a` | `test_group_kfold_evaluation_exceeds_random_guess` | `tests/unit/test_baseline.py` |

## 2. Red Run Evidence
Executed command:
`python -m pytest tests/unit/test_metrics.py tests/unit/test_baseline.py`

Exit code: `1`

Output capture:
```
collected 0 items / 2 errors

=================================== ERRORS ====================================
_________________ ERROR collecting tests/unit/test_metrics.py _________________
tests\unit\test_metrics.py:5: in <module>
    from namethellm.metrics import compute_balanced_accuracy, compute_per_class_recall
E   ModuleNotFoundError: No module named 'namethellm.metrics'
________________ ERROR collecting tests/unit/test_baseline.py _________________
tests\unit\test_baseline.py:6: in <module>
    from namethellm.models.baseline import BaselineTFIDFClassifier
E   ModuleNotFoundError: No module named 'namethellm.models'
=========================== short test summary info ===========================
ERROR tests/unit/test_metrics.py
ERROR tests/unit/test_baseline.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!
============================== 2 errors in 8.41s ==============================
```

Tests failed cleanly due to missing target modules. Ready for Builder handoff.
