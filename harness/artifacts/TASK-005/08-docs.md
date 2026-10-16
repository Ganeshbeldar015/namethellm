---
status: complete
owner: scribe
task: TASK-005
inputs:
  - harness/artifacts/TASK-005/05-build.md
---
# 08-docs.md — Documentation for TASK-005

## 1. Documentation Updates
- Updated `README.md` with:
  - Benchmark performance table: Baseline 0.3004 -> Sprint 2 Hybrid 0.3304.
  - Python API usage example showing `HybridStyloClassifier` model fitting and submission generation.
- Authored docstrings for all classes and methods in:
  - `src/namethellm/models/hybrid.py`: `HybridStyloClassifier`
  - `src/namethellm/postprocess.py`: `BalancedAccuracyCalibrator`
  - `src/namethellm/models/__init__.py`

## 2. API Summary
- `namethellm.models.hybrid.HybridStyloClassifier`: Hybrid classifier combining word and character TF-IDF representations with 46 scaled stylometric features.
- `namethellm.postprocess.BalancedAccuracyCalibrator`: Postprocessing probability calibrator maximizing macro-averaged recall.
