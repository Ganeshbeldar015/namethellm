---
status: complete
owner: po-spec
task: TASK-001
inputs:
  - docs/harness.md
  - harness/tasks/TASK-001.md
---
# 01-spec.md — Specification for TASK-001

## 1. Problem
To train models that reliably attribute ~4,000 text passages across 18 frontier LLMs without benchmark contamination or prompt memorization, we need an airtight data ingestion module and a cross-validation strategy strictly grouped by `prompt_id`.

## 2. Scope
- Ingestion and schema validation of `dataset/train.csv`, `dataset/test.csv`, and `dataset/sample_submission.parquet`.
- Enforcing label integrity: all training labels must match exactly one of the 18 valid model candidate strings.
- Enforcing zero null values across all required fields.
- Cross-validation generator using `GroupKFold` / `StratifiedGroupKFold` partitioned by `prompt_id`.

## 3. Out of Scope
- Model training, feature extraction, or prediction inference.
- Modification of source dataset files in `dataset/`.

## 4. User Stories
- As an ML engineer, I want to load `dataset/train.csv` and get an immediate exception if columns or labels are malformed, so bad data never enters training.
- As an ML engineer, I want cross-validation folds strictly grouped by `prompt_id` so that unseen prompt generalization is truthfully evaluated.
- As an ML engineer, I want to inspect and validate `dataset/test.csv` format matching Kaggle's interactive and rerun environments.

## 5. Requirements to Acceptance Criteria Mapping

### REQ-001: Data Ingestion & Validation
- **`AC-001-a`**: Given `dataset/train.csv`, when loaded by `namethellm.data.load_train_data()`, then:
  1. It returns a DataFrame with 2,699 rows and columns `['id', 'prompt_id', 'text', 'model']`.
  2. All `model` values strictly belong to the 18 approved candidate models.
  3. No null or empty values exist in any column.
- **`AC-001-b`**: Given `dataset/test.csv`, when loaded by `namethellm.data.load_test_data()`, then:
  1. It returns a DataFrame with columns `['id', 'text']`.
  2. No null values exist in `id` or `text`.
- **`AC-001-c`**: Given `dataset/sample_submission.parquet`, when loaded by `namethellm.data.load_sample_submission()`, then:
  1. It returns a DataFrame with columns `['id', 'model']`.

### REQ-002: Grouped Validation Scheme
- **`AC-002-a`**: Given `train_df` with 150 unique `prompt_id`s, when split via `namethellm.split.get_group_kfold_splits(train_df, n_splits=5)`, then:
  1. For every fold $k \in \{0, \dots, 4\}$, $\text{set}(\text{prompt\_id}_{train}) \cap \text{set}(\text{prompt\_id}_{val}) = \emptyset$.
  2. The union of all validation splits covers all 2,699 samples exactly once.
- **`AC-002-b`**: Given the 18 model classes, every validation fold contains samples from all 18 classes where feasible (stratified group splitting).

## 6. Edge Cases & Constraints
- **Asymmetric Class Size**: Model `claude-fable-5` has 149 samples, while all 17 other models have 150 samples. Grouping splitters must gracefully accommodate this without raising balancing exceptions.
- **Missing File Error**: Attempting to load non-existent paths must raise standard `FileNotFoundError`.
- **Invalid Label Error**: Rows containing unexpected model names must raise `ValueError` detailing the invalid label.

## 7. Non-Functional Requirements
- Hermetic execution without network access.
- Ingestion execution time for full dataset < 500ms.
- Deterministic folding behavior when `seed` is provided.

## 8. Open Questions
- None. Requirements fully defined from Kaggle competition specification and `docs/harness.md`.
