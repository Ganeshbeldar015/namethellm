---
status: complete
owner: test-author
task: TASK-004
inputs:
  - harness/artifacts/TASK-004/01-spec.md
  - harness/artifacts/TASK-004/03-plan.md
---
# 04-tests.md — Tests for TASK-004

## 1. Traceability Matrix

| Acceptance Criteria | Test Function | Test File |
|---|---|---|
| `AC-004-a` | `test_stylometric_extractor_shape_and_features` | `tests/unit/test_stylometry.py` |
| `AC-004-a` | `test_stylometric_extractor_no_nans_or_infs` | `tests/unit/test_stylometry.py` |
| `AC-004-a` | `test_stylometric_extractor_edge_cases` | `tests/unit/test_stylometry.py` |
| `AC-004-a` | `test_stylometric_extractor_pipeline_compatibility` | `tests/unit/test_stylometry.py` |
| `AC-004-a` | `test_stylometric_extractor_discriminative_signals` | `tests/unit/test_stylometry.py` |

## 2. Red Run Evidence
Executed command:
`python -m pytest tests/unit/test_stylometry.py`

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
_______________ ERROR collecting tests/unit/test_stylometry.py ________________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_stylometry.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_stylometry.py:8: in <module>
    from namethellm.features.stylometry import StylometricFeatureExtractor
E   ModuleNotFoundError: No module named 'namethellm.features'
=========================== short test summary info ===========================
ERROR tests/unit/test_stylometry.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 2.87s ===============================
```

Tests failed cleanly due to missing target module `namethellm.features`. Ready for Builder handoff.
