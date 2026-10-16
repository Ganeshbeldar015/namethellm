# TASK-001 — Data Ingestion, Schema Validation, and GroupKFold Split

Backlog ref: TASK-001 · Sprint: 1 · Priority: Must

## Intent
Provide robust, leak-free data ingestion and prompt-grouped cross-validation splitting for the Name That LLM pipeline.

## Scope / Out of scope
**In Scope**:
- Ingest and validate `dataset/train.csv`, `dataset/test.csv`, and `dataset/sample_submission.parquet`.
- Enforce schema constraints, null checks, and the 18 valid candidate model names.
- Implement cross-validation splitters (`GroupKFold` / `StratifiedGroupKFold`) strictly grouping by `prompt_id`.

**Out of Scope**:
- Feature extraction, model training, and submission generation (handled in subsequent tasks).

## Guidance
- Adhere strictly to `docs/adr/ADR-0001-group-kfold.md`.
- No `prompt_id` present in training folds may appear in the validation fold.
- Provide clean, typed interfaces with deterministic random seeds.

## Requirements
- `REQ-001`: Ingest and validate `train.csv`, `test.csv`, and `sample_submission.parquet` schema and constraints.
- `REQ-002`: Implement GroupKFold cross-validation grouped on `prompt_id` to prevent prompt leakage.

## Acceptance
- `AC-001-a`: Given `dataset/train.csv`, when loaded by the data ingestion module, then it yields 2,699 rows, 4 columns (`id`, `prompt_id`, `text`, `model`), with 0 nulls and all labels in the 18 valid model names.
- `AC-001-b`: Given `dataset/test.csv`, when loaded, then it yields `id` and `text` columns without error.
- `AC-002-a`: Given a K-fold split (e.g. K=5), when dataset is split on `prompt_id`, then no `prompt_id` in any training fold appears in the corresponding validation fold.

## Risks / Notes
- `claude-fable-5` has 149 examples, while other models have 150. Stratification must tolerate slight class imbalance.
