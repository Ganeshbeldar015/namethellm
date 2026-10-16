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

### Baseline Model Evaluation
```bash
# Run 5-fold GroupKFold baseline evaluation
python -m namethellm.evaluate
```

Current Baseline Performance:
- **OOF Balanced Accuracy**: **0.3004** (vs. random guess 0.0555).

### API Usage
```python
from namethellm import data, split, metrics
from namethellm.models.baseline import BaselineTFIDFClassifier

# Load dataset
train_df = data.load_train_data()

# Evaluate balanced accuracy
y_true = train_df["model"].values
# preds = ...
# score = metrics.compute_balanced_accuracy(y_true, preds)
```
