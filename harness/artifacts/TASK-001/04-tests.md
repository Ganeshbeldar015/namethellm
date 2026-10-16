---
status: complete
owner: test-author
task: TASK-001
inputs:
  - harness/artifacts/TASK-001/01-spec.md
  - harness/artifacts/TASK-001/03-plan.md
---
# 04-tests.md — Tests for TASK-001

## 1. Traceability Matrix

| Acceptance Criteria | Test Function | Test File |
|---|---|---|
| `AC-001-a` | `test_load_train_data_shape_and_columns` | `tests/unit/test_data.py` |
| `AC-001-a` | `test_load_train_data_valid_labels` | `tests/unit/test_data.py` |
| `AC-001-a` | `test_load_train_data_no_nulls` | `tests/unit/test_data.py` |
| `AC-001-a` | `test_validate_train_schema_missing_column` | `tests/unit/test_data.py` |
| `AC-001-a` | `test_validate_train_schema_invalid_label` | `tests/unit/test_data.py` |
| `AC-001-b` | `test_load_test_data` | `tests/unit/test_data.py` |
| `AC-001-c` | `test_load_sample_submission` | `tests/unit/test_data.py` |
| `AC-002-a` | `test_group_kfold_no_prompt_leakage` | `tests/unit/test_split.py` |
| `AC-002-a` | `test_group_kfold_covers_all_samples` | `tests/unit/test_split.py` |
| `AC-002-b` | `test_group_kfold_all_classes_present` | `tests/unit/test_split.py` |
| Determinism | `test_split_deterministic_with_seed` | `tests/unit/test_split.py` |
| Error handling | `test_missing_file_raises_filenotfound` | `tests/unit/test_data.py` |

## 2. Red Run Evidence
Executed command:
`python -m pytest tests/unit`

Exit code: `1`

Output capture:
```
collected 0 items / 2 errors

=================================== ERRORS ====================================
__________________ ERROR collecting tests/unit/test_data.py ___________________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_data.py'.
Traceback:
tests\unit\test_data.py:5: in <module>
    from namethellm import data
E   ModuleNotFoundError: No module named 'namethellm'
__________________ ERROR collecting tests/unit/test_split.py __________________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_split.py'.
Traceback:
tests\unit\test_split.py:5: in <module>
    from namethellm import data
E   ModuleNotFoundError: No module named 'namethellm'
=========================== short test summary info ===========================
ERROR tests/unit/test_data.py
ERROR tests/unit/test_split.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!
============================== 2 errors in 7.23s ==============================
```

Tests failed as expected because implementation in `src/namethellm/` does not yet exist.
Ready for Builder handoff.
