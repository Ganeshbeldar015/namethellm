---
status: complete
owner: test-author
task: TASK-003
inputs:
  - harness/artifacts/TASK-003/01-spec.md
  - harness/artifacts/TASK-003/03-plan.md
---
# 04-tests.md — Tests for TASK-003

## 1. Traceability Matrix

| Acceptance Criteria | Test Function | Test File |
|---|---|---|
| `AC-007-a` | `test_validate_submission_valid` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_wrong_type` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_column_mismatch` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_row_count_mismatch` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_id_mismatch` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_nulls` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_invalid_model_label` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_generate_submission_happy_path` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_generate_submission_catches_bad_predictions` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_validate_submission_file_roundtrip` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_dynamic_sizing_large_test` | `tests/unit/test_submission.py` |
| `AC-007-a` | `test_empty_test_set_handling` | `tests/unit/test_submission.py` |

## 2. Red Run Evidence
Executed command:
`python -m pytest tests/unit/test_submission.py`

Exit code: `1`

Output capture:
```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\WorkSpace\Project\namethellm
configfile: pyproject.toml
plugins: anyio-4.15.0
collected 0 items / 1 error

=================================== ERRORS ====================================
_______________ ERROR collecting tests/unit/test_submission.py ________________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_submission.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_submission.py:9: in <module>
    from namethellm.submission import (
E   ModuleNotFoundError: No module named 'namethellm.submission'
=========================== short test summary info ===========================
ERROR tests/unit/test_submission.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 1.14s ===============================
```

Tests failed cleanly due to missing target module `namethellm.submission`. Ready for Builder handoff.
