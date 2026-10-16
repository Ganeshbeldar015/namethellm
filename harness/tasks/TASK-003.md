# TASK-003 — Verified submission.parquet Generator and Validator

Backlog ref: TASK-003 · Sprint: 1 · Priority: Must · Status: Complete

## Intent
Build the test prediction inference pipeline and verification system that generates Kaggle-compliant `submission.parquet` files with strict format checks.

## Scope / Out of scope
**In Scope**:
- `src/namethellm/submission.py`:
  - `generate_submission()`: Runs inference on `dataset/test.csv` using a fitted classifier and outputs `submission.parquet`.
  - `validate_submission()`: Validates that any submission DataFrame conforms strictly to Kaggle submission rules.
  - CLI entrypoint: `python -m namethellm.submission`.
- `tests/unit/test_submission.py`: Comprehensive test suite verifying all 6 criteria of `AC-007-a`.

**Out of Scope**:
- Complex ensembling or deep transformer tuning (deferred to Sprint 2 & 3).

## Guidance
- A submission is rejected by Kaggle if it is missing the `id` or `model` column, contains null values, repeats an ID, predicts a label outside the 18 listed, or does not match test row count.
- Validation must be strict and descriptive.
- File format must be valid Apache Parquet readable by `pd.read_parquet()`.

## Requirements
- `REQ-007`: Generate validated `submission.parquet` meeting all format, ID uniqueness, and valid-label rules.

## Acceptance
- `AC-007-a`: Given test input, when `submission.parquet` is generated, then:
  1. File is valid Apache Parquet format.
  2. Columns are exactly `id` and `model`.
  3. Row count matches `test.csv` exactly.
  4. Every `id` matches `test.csv` with zero duplicates.
  5. Zero null values exist.
  6. Every value in `model` is strictly one of the 18 valid candidate models.

## Risks / Notes
- During interactive development, `test.csv` has 3 rows. When submitted on Kaggle, `test.csv` is swapped for the hidden ~4,000 row test set. The submission generator must dynamically infer on whatever `test.csv` is provided without hardcoding lengths.
