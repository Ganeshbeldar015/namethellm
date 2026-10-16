---
status: complete
owner: tech-lead
task: TASK-003
inputs:
  - harness/artifacts/TASK-003/01-spec.md
---
# 03-plan.md — Implementation Plan for TASK-003

## 1. Architectural Approach
We design the Kaggle-compliant submission generation and defensive validation module:
- `src/namethellm/submission.py`:
  - `validate_submission(sub_df: pd.DataFrame, test_df: pd.DataFrame) -> None`:
    Rigorous pre-write and post-read validation checking all 6 acceptance constraints:
    1. Input is a pandas DataFrame.
    2. Column list matches `SUBMISSION_COLUMNS = ['id', 'model']` exactly (order, count, names).
    3. Row count matches `len(test_df)` exactly.
    4. `id` column matches `test_df['id']` row-for-row with zero index misalignment or duplicates.
    5. No null or NaN values in any column.
    6. All predicted model labels are members of `VALID_MODELS`.
    Raises descriptive `ValueError` upon any constraint violation.
  - `generate_submission(model: Any, test_df: pd.DataFrame, output_path: Union[str, Path] = "submission.parquet") -> pd.DataFrame`:
    Runs inference using `model.predict(test_df['text'])`, constructs the submission DataFrame, runs `validate_submission()`, writes to `output_path` using Apache Parquet (`to_parquet(index=False)`), and verifies the persisted file.
  - `validate_submission_file(file_path: Union[str, Path], test_df: pd.DataFrame) -> pd.DataFrame`:
    Reads parquet from disk and validates against `test_df`, returning the validated DataFrame.
  - CLI runner: `python -m namethellm.submission`
    Loads training data, trains baseline model, predicts on `dataset/test.csv`, and writes `submission.parquet`.

## 2. File-Level Change List
| File Path | Action | Purpose |
|---|---|---|
| `src/namethellm/submission.py` | Create | Submission generator, defensive validator, and CLI entrypoint |
| `tests/unit/test_submission.py` | Create | Unit tests validating AC-007-a and validation failure modes |

## 3. Lane Decomposition & Exclusive File Ownership
Sequential execution (solo builder lane `main`):
- **Lane `main` owns**:
  - `src/namethellm/submission.py`

- **Test Author owns**:
  - `tests/unit/test_submission.py`

No overlapping ownership exists.

## 4. Test Strategy per Acceptance Criteria
- **`AC-007-a`**: In `tests/unit/test_submission.py`:
  - **Happy Path Generation**: Call `generate_submission` with mock model and synthetic test data; assert file is created, valid parquet, correct schema `['id', 'model']`, matching rows and IDs.
  - **Column Validation Failure**: Call `validate_submission` with missing columns (e.g. `['id']`), extra columns (e.g. `['id', 'model', 'prob']`), or incorrect column names; assert `ValueError`.
  - **Row Count Mismatch Failure**: Call `validate_submission` with row count differing from `test_df`; assert `ValueError`.
  - **ID Misalignment Failure**: Call `validate_submission` with shuffled IDs or mismatched IDs; assert `ValueError`.
  - **Null / NaN Failure**: Call `validate_submission` with NaN in `id` or `model`; assert `ValueError`.
  - **Illegal Model Name Failure**: Call `validate_submission` with model name outside `VALID_MODELS` (e.g., `'unseen-gpt-9'`); assert `ValueError`.
  - **Dynamic Sizing**: Validate behavior on interactive dummy test set (3 rows) and scaled sets (100+ rows).
  - **Empty Test Set**: Safely returns empty submission DataFrame without crashing.

## 5. Risk Assessment & Mitigations
- **Parquet Engine Dependency**: Parquet writing requires an engine (`pyarrow` or `fastparquet`).
  - *Mitigation*: `pyarrow` is locked in `requirements.txt` and verified in virtual environment.
- **Hidden Test Set Size**: Local `dataset/test.csv` has 3 rows, but Kaggle private rerun has ~4,000 rows.
  - *Mitigation*: Hardcoding row numbers is strictly avoided; all operations derive sizes dynamically from `len(test_df)`.

## 6. Rollback Plan
Revert git branch to `fb3b5ce` if unresolvable regressions occur.
