---
status: complete
owner: test-author
task: TASK-005
inputs:
  - harness/artifacts/TASK-005/01-spec.md
  - harness/artifacts/TASK-005/03-plan.md
---
# 04-tests.md — Tests for TASK-005

## 1. Traceability Matrix

| Acceptance Criteria | Test Function | Test File |
|---|---|---|
| `AC-005-a` | `test_hybrid_stylo_classifier_fit_predict` | `tests/unit/test_hybrid.py` |
| `AC-006-a` | `test_calibrator_properties` | `tests/unit/test_hybrid.py` |
| `AC-006-a` | `test_calibrator_neutral_on_balanced` | `tests/unit/test_hybrid.py` |

## 2. Red Run Evidence
Executed command:
`python -m pytest tests/unit/test_hybrid.py`

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
_________________ ERROR collecting tests/unit/test_hybrid.py __________________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_hybrid.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_hybrid.py:8: in <module>
    from namethellm.models.hybrid import HybridStyloClassifier
E   ModuleNotFoundError: No module named 'namethellm.models.hybrid'
=========================== short test summary info ===========================
ERROR tests/unit/test_hybrid.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 11.44s ==============================
```

Tests failed cleanly due to missing target module `namethellm.models.hybrid`. Ready for Builder handoff.
