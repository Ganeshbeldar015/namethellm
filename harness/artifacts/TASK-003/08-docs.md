---
status: complete
owner: scribe
task: TASK-003
inputs:
  - harness/artifacts/TASK-003/05-build.md
---
# 08-docs.md — Documentation for TASK-003

## 1. Documentation Updates
- Updated `README.md` with:
  - Submission CLI command: `python -m namethellm.submission`.
  - Python API usage example showing model fitting and submission generation via `submission.generate_submission()`.
- Added comprehensive docstrings to all functions in `src/namethellm/submission.py`:
  - `validate_submission(sub_df, test_df)`
  - `generate_submission(model, test_df, output_path)`
  - `validate_submission_file(file_path, test_df)`
  - `main()`

## 2. API Summary
- `namethellm.submission.validate_submission(sub_df: pd.DataFrame, test_df: pd.DataFrame) -> None`
- `namethellm.submission.generate_submission(model: Any, test_df: pd.DataFrame, output_path: Union[str, Path] = "submission.parquet") -> pd.DataFrame`
- `namethellm.submission.validate_submission_file(file_path: Union[str, Path], test_df: pd.DataFrame) -> pd.DataFrame`
