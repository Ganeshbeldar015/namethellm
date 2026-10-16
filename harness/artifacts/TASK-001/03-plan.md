---
status: complete
owner: tech-lead
task: TASK-001
inputs:
  - harness/artifacts/TASK-001/01-spec.md
---
# 03-plan.md — Implementation Plan for TASK-001

## 1. Architectural Approach
We establish the foundational data access and cross-validation layer in `src/namethellm/`:
- `constants.py`: Enumerates the 18 candidate models and canonical DataFrame column sets.
- `data.py`: Provides type-annotated loader functions with strict schema verification and custom error handling.
- `split.py`: Provides leak-free cross-validation splitting using Scikit-Learn's `GroupKFold` / `StratifiedGroupKFold` grouped on `prompt_id`.

## 2. File-Level Change List
| File Path | Action | Purpose |
|---|---|---|
| `src/namethellm/__init__.py` | Create | Package initialization and version definition |
| `src/namethellm/constants.py` | Create | 18 valid model names, schema column definitions |
| `src/namethellm/data.py` | Create | Data loading functions, schema and label validation |
| `src/namethellm/split.py` | Create | Grouped cross-validation split generation |
| `tests/unit/__init__.py` | Create | Unit test package |
| `tests/unit/test_data.py` | Create | Unit tests for AC-001-a, AC-001-b, and schema error handling |
| `tests/unit/test_split.py` | Create | Unit tests for AC-002-a, AC-002-b, and zero-overlap verification |

## 3. Lane Decomposition & Exclusive File Ownership
Parallelism for this task is sequential (solo builder lane `main`):
- **Lane `main` owns**:
  - `src/namethellm/__init__.py`
  - `src/namethellm/constants.py`
  - `src/namethellm/data.py`
  - `src/namethellm/split.py`

Test Author owns:
  - `tests/unit/__init__.py`
  - `tests/unit/test_data.py`
  - `tests/unit/test_split.py`

No file ownership overlap exists.

## 4. Test Strategy per Acceptance Criteria
- **`AC-001-a`**: In `test_data.py`:
  - Load `dataset/train.csv` and assert shape `(2699, 4)`, exact column names, non-null status, and all values in `model` are in `VALID_MODELS`.
  - Provide a malformed DataFrame (missing column, null value, invalid model string) and assert that `validate_train_schema()` raises `ValueError`.
- **`AC-001-b`**: In `test_data.py`:
  - Load `dataset/test.csv` and assert columns `['id', 'text']` and non-null status.
- **`AC-002-a`**: In `test_split.py`:
  - Run 5-fold split on `train.csv`. For each fold, extract `train_prompts = set(train_df.iloc[train_idx]['prompt_id'])` and `val_prompts = set(train_df.iloc[val_idx]['prompt_id'])`.
  - Assert `len(train_prompts.intersection(val_prompts)) == 0`.
  - Assert that union of all `val_idx` has length 2,699 with no duplicates.
- **`AC-002-b`**: In `test_split.py`:
  - Assert that all 18 models are represented in each validation fold.

## 5. Risk Assessment & Mitigations
- **Risk**: Asymmetric class count (claude-fable-5 has 149 rows, others 150).
  - *Mitigation*: Use `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)` which balances group assignments while handling slight class count discrepancies smoothly.
- **Risk**: Parquet engine variation.
  - *Mitigation*: Standardize on `pyarrow` (now installed).

## 6. Rollback Plan
If any regressions occur, revert git branch to `5601319`.
