---
status: complete
owner: scribe
task: TASK-001
inputs:
  - harness/artifacts/TASK-001/05-build.md
---
# 08-docs.md — Documentation for TASK-001

## 1. Documentation Updates
- Created top-level `README.md` with installation commands, test instructions, and Python usage examples for `data.py` and `split.py`.
- Formatted docstrings for all public methods in `namethellm.data` and `namethellm.split`.

## 2. API Summary
- `namethellm.data.load_train_data(path='dataset/train.csv') -> pd.DataFrame`
- `namethellm.data.load_test_data(path='dataset/test.csv') -> pd.DataFrame`
- `namethellm.data.load_sample_submission(path='dataset/sample_submission.parquet') -> pd.DataFrame`
- `namethellm.split.get_group_kfold_splits(df, group_col='prompt_id', target_col='model', n_splits=5, seed=42) -> list[tuple[np.ndarray, np.ndarray]]`

## 3. Link Integrity
All file paths and links verified to exist.
