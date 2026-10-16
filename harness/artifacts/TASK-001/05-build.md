---
status: complete
owner: builder
task: TASK-001
inputs:
  - harness/artifacts/TASK-001/03-plan.md
  - harness/artifacts/TASK-001/04-tests.md
---
# 05-build.md — Build Log for TASK-001

## 1. Summary of Changes
Implemented data ingestion, strict schema and model label verification, and leak-free prompt-grouped cross-validation splitting.

### Files Created
- `src/namethellm/__init__.py`: Package initialization.
- `src/namethellm/constants.py`: List of 18 valid candidate models and schema column definitions.
- `src/namethellm/data.py`: `load_train_data()`, `load_test_data()`, `load_sample_submission()`, `validate_train_schema()`, `validate_test_schema()`.
- `src/namethellm/split.py`: `get_group_kfold_splits()` supporting `StratifiedGroupKFold` on `prompt_id`.
- `pyproject.toml`: Package build configuration.

## 2. Key Technical Decisions
- `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)` is utilized to ensure all 18 models are evenly represented across validation folds while strictly ensuring no prompt overlap between training and validation sets.
- Strict input validation raises informative `ValueError` if required columns are missing, nulls are present, or unexpected model labels are encountered.

## 3. Verification Commands & Outputs
- Command: `python -m pytest tests/unit`
  - Result: 12 passed in 22.07s
  - Exit code: 0

- Command: `python scripts/guard_paths.py --role builder --files src/namethellm/__init__.py src/namethellm/constants.py src/namethellm/data.py src/namethellm/split.py`
  - Exit code: 0 (all paths within allow-list).
