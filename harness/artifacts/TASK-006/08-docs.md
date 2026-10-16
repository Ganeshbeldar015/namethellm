---
status: complete
owner: scribe
task: TASK-006
inputs:
  - harness/artifacts/TASK-006/05-build.md
---
# 08-docs.md — Documentation for TASK-006

## 1. Documentation Updates
- Updated `README.md` with:
  - Benchmark performance table: Sprint 3 Stylegram achieves OOF Balanced Accuracy of **0.3430** (+0.0426 gain over baseline).
  - Python API usage example showing `StylegramClassifier` model fitting and submission generation.
- Authored docstrings for all classes and functions in:
  - `src/namethellm/features/text_transforms.py`: `shape_text()`, `function_text()`.
  - `src/namethellm/models/stylegram.py`: `StylegramClassifier`.
  - `src/namethellm/models/__init__.py`.

## 2. API Summary
- `namethellm.features.text_transforms.shape_text(texts: Sequence[str]) -> list[str]`
- `namethellm.features.text_transforms.function_text(texts: Sequence[str]) -> list[str]`
- `namethellm.models.stylegram.StylegramClassifier`: Multi-view classifier fusing word n-grams, char n-grams, casing shape n-grams, function syntax n-grams, and 46 stylometric features.
