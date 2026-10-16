---
status: complete
owner: test-author
task: TASK-006
inputs:
  - harness/artifacts/TASK-006/01-spec.md
  - harness/artifacts/TASK-006/03-plan.md
---
# 04-tests.md — Tests for TASK-006

## 1. Traceability Matrix

| Acceptance Criteria | Test Function | Test File |
|---|---|---|
| `AC-004-a` | `test_shape_text_casing_abstraction` | `tests/unit/test_text_transforms.py` |
| `AC-004-a` | `test_shape_text_edge_cases` | `tests/unit/test_text_transforms.py` |
| `AC-004-a` | `test_function_text_syntax_isolation` | `tests/unit/test_text_transforms.py` |
| `AC-004-a` | `test_function_text_edge_cases` | `tests/unit/test_text_transforms.py` |
| `AC-005-a` | `test_stylegram_classifier_fit_predict` | `tests/unit/test_stylegram.py` |

## 2. Red Run Evidence
Executed command:
`python -m pytest tests/unit/test_text_transforms.py tests/unit/test_stylegram.py`

Exit code: `1`

Output capture:
```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\WorkSpace\Project\namethellm
configfile: pyproject.toml
plugins: anyio-4.15.0
collected 0 items / 2 errors

=================================== ERRORS ====================================
_____________ ERROR collecting tests/unit/test_text_transforms.py _____________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_text_transforms.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_text_transforms.py:3: in <module>
    from namethellm.features.text_transforms import function_text, shape_text
E   ModuleNotFoundError: No module named 'namethellm.features.text_transforms'
________________ ERROR collecting tests/unit/test_stylegram.py ________________
ImportError while importing test module 'D:\WorkSpace\Project\namethellm\tests\unit\test_stylegram.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_stylegram.py:7: in <module>
    from namethellm.models.stylegram import StylegramClassifier
E   ModuleNotFoundError: No module named 'namethellm.models.stylegram'
=========================== short test summary info ===========================
ERROR tests/unit/test_text_transforms.py
ERROR tests/unit/test_stylegram.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!
============================== 2 errors in 3.19s ==============================
```

Tests failed cleanly due to missing target modules. Ready for Builder handoff.
