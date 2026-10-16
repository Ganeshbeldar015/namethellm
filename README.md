# Name That LLM

Authorship attribution pipeline across 18 frontier LLMs using stylometry, NLP, and machine learning for the Kaggle Code Competition.

## Quickstart

### Installation
```bash
pip install -e .
```

### Running Tests
```bash
# Unit tests
python -m pytest tests/unit

# Harness integrity self-test
python scripts/check_harness.py && python -m pytest tests/harness
```

### Data Ingestion & Splitting API
```python
from namethellm import data, split

# Load and validate dataset
train_df = data.load_train_data()
test_df = data.load_test_data()

# 5-fold cross-validation strictly grouped on prompt_id
splits = split.get_group_kfold_splits(train_df, n_splits=5, seed=42)
for fold, (train_idx, val_idx) in enumerate(splits):
    print(f"Fold {fold}: {len(train_idx)} train, {len(val_idx)} val")
```
