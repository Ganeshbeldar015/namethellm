---
status: complete
owner: po-spec
task: TASK-003
inputs:
  - docs/harness.md
  - harness/tasks/TASK-003.md
---
# 01-spec.md — Specification for TASK-003

## 1. Problem
Kaggle's scoring system rejects any submission that contains missing values, duplicates, unexpected columns, extra/missing rows, or model names outside the 18 valid frontier LLMs. We require an autonomous, defensive submission generator and validator that guarantees strict compliance.

## 2. Scope
- Inference runner on `dataset/test.csv` generating `submission.parquet`.
- Validation function `validate_submission(sub_df, test_df)` verifying:
  1. File is valid Apache Parquet.
  2. Columns are exactly `id` and `model`.
  3. Row count matches `test.csv` exactly.
  4. Every `id` matches `test.csv` with zero duplicates.
  5. Zero null values exist.
  6. Every value in `model` is strictly one of the 18 valid candidate models.
- CLI entrypoint: `python -m namethellm.submission`.

## 3. Out of Scope
- Automatic uploading or remote Kaggle API submission (requires user confirmation per Autonomy Matrix).

## 4. User Stories
- As a competitor, when I run `python -m namethellm.submission`, I want a valid `submission.parquet` generated in the current working directory without manual formatting steps.
- As a competitor, if a model predicts an illegal string or produces NaN predictions, I want an immediate descriptive `ValueError` before anything is written to disk.

## 5. Requirements to Acceptance Criteria Mapping

### REQ-007: Validated Submission File Generation
- **`AC-007-a`**: Given test data and a fitted model, when `generate_submission()` is called:
  1. The output file `submission.parquet` is created in valid Apache Parquet format.
  2. `pd.read_parquet(output_path)` yields exactly columns `['id', 'model']`.
  3. The row count matches `len(test_df)`.
  4. The `id` column matches `test_df['id']` row-for-row with zero duplicates.
  5. No null or NaN values exist.
  6. Every predicted label in `model` is strictly a member of `VALID_MODELS`.

## 6. Edge Cases & Constraints
- Empty test set: Handled safely without index errors.
- Test set size variability: Dynamic sizing accommodating both the 3-row interactive dummy test set and the ~4,000 row hidden test rerun.

## 7. Non-Functional Requirements
- Submission generation runtime < 5 seconds for interactive test set.
- Hermetic offline execution.

## 8. Open Questions
- None.
