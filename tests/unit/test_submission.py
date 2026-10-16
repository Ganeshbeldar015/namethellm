"""Unit tests for submission generator and validator (AC-007-a)."""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from namethellm.constants import SUBMISSION_COLUMNS, VALID_MODELS
from namethellm.submission import (
    generate_submission,
    validate_submission,
    validate_submission_file,
)


class MockPredictor:
    """Mock model predicting constant or cyclic valid model names."""

    def __init__(self, target_label: str = "gpt-5.5"):
        self.target_label = target_label

    def predict(self, texts):
        return [self.target_label] * len(texts)


class BadPredictor:
    """Mock model predicting an invalid model name."""

    def predict(self, texts):
        return ["invalid-frontier-llm-99"] * len(texts)


@pytest.fixture
def sample_test_df() -> pd.DataFrame:
    """Returns a synthetic test set mimicking dataset/test.csv."""
    return pd.DataFrame(
        {
            "id": ["test_001", "test_002", "test_003"],
            "text": [
                "Sample prompt text one.",
                "Sample prompt text two.",
                "Sample prompt text three.",
            ],
        }
    )


def test_validate_submission_valid(sample_test_df: pd.DataFrame):
    """AC-007-a: Valid submission DataFrame passes validation with zero errors."""
    valid_sub = pd.DataFrame(
        {
            "id": ["test_001", "test_002", "test_003"],
            "model": ["gpt-5.5", "claude-opus-5", "gemini-3.8-flash"],
        }
    )
    # Should complete without error
    validate_submission(valid_sub, sample_test_df)


def test_validate_submission_wrong_type(sample_test_df: pd.DataFrame):
    """AC-007-a: Non-DataFrame input raises TypeError."""
    with pytest.raises(TypeError, match="must be a pandas DataFrame"):
        validate_submission("not_a_df", sample_test_df)  # type: ignore


def test_validate_submission_column_mismatch(sample_test_df: pd.DataFrame):
    """AC-007-a: Missing or unexpected columns raises ValueError."""
    # Missing 'model'
    missing_col = pd.DataFrame({"id": ["test_001", "test_002", "test_003"]})
    with pytest.raises(ValueError, match="Columns must match"):
        validate_submission(missing_col, sample_test_df)

    # Extra column
    extra_col = pd.DataFrame(
        {
            "id": ["test_001", "test_002", "test_003"],
            "model": ["gpt-5.5", "gpt-5.5", "gpt-5.5"],
            "prob": [0.9, 0.8, 0.7],
        }
    )
    with pytest.raises(ValueError, match="Columns must match"):
        validate_submission(extra_col, sample_test_df)

    # Wrong column names
    wrong_names = pd.DataFrame(
        {
            "row_id": ["test_001", "test_002", "test_003"],
            "prediction": ["gpt-5.5", "gpt-5.5", "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="Columns must match"):
        validate_submission(wrong_names, sample_test_df)


def test_validate_submission_row_count_mismatch(sample_test_df: pd.DataFrame):
    """AC-007-a: Row count differing from test_df raises ValueError."""
    short_sub = pd.DataFrame(
        {
            "id": ["test_001", "test_002"],
            "model": ["gpt-5.5", "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="Row count mismatch"):
        validate_submission(short_sub, sample_test_df)

    long_sub = pd.DataFrame(
        {
            "id": ["test_001", "test_002", "test_003", "test_004"],
            "model": ["gpt-5.5", "gpt-5.5", "gpt-5.5", "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="Row count mismatch"):
        validate_submission(long_sub, sample_test_df)


def test_validate_submission_id_mismatch(sample_test_df: pd.DataFrame):
    """AC-007-a: ID mismatch or permutation raises ValueError."""
    # Shuffled IDs
    shuffled_sub = pd.DataFrame(
        {
            "id": ["test_003", "test_002", "test_001"],
            "model": ["gpt-5.5", "gpt-5.5", "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="IDs do not match"):
        validate_submission(shuffled_sub, sample_test_df)

    # Different IDs
    different_ids = pd.DataFrame(
        {
            "id": ["wrong_1", "wrong_2", "wrong_3"],
            "model": ["gpt-5.5", "gpt-5.5", "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="IDs do not match"):
        validate_submission(different_ids, sample_test_df)


def test_validate_submission_nulls(sample_test_df: pd.DataFrame):
    """AC-007-a: Presence of NaN or None raises ValueError."""
    # Null model prediction
    null_model = pd.DataFrame(
        {
            "id": ["test_001", "test_002", "test_003"],
            "model": ["gpt-5.5", None, "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="null or NaN"):
        validate_submission(null_model, sample_test_df)

    # Null ID
    null_id = pd.DataFrame(
        {
            "id": ["test_001", np.nan, "test_003"],
            "model": ["gpt-5.5", "gpt-5.5", "gpt-5.5"],
        }
    )
    with pytest.raises(ValueError, match="null or NaN"):
        validate_submission(null_id, sample_test_df)


def test_validate_submission_invalid_model_label(sample_test_df: pd.DataFrame):
    """AC-007-a: Model predictions outside VALID_MODELS raises ValueError."""
    invalid_sub = pd.DataFrame(
        {
            "id": ["test_001", "test_002", "test_003"],
            "model": ["gpt-5.5", "claude-fable-99", "gemini-3.8-flash"],
        }
    )
    with pytest.raises(ValueError, match="Invalid model labels found"):
        validate_submission(invalid_sub, sample_test_df)


def test_generate_submission_happy_path(sample_test_df: pd.DataFrame, tmp_path: Path):
    """AC-007-a: generate_submission writes valid parquet file matching all constraints."""
    out_file = tmp_path / "submission.parquet"
    predictor = MockPredictor(target_label="gemini-3.7-flash")

    result_df = generate_submission(predictor, sample_test_df, output_path=out_file)

    # Verify return dataframe
    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == SUBMISSION_COLUMNS
    assert len(result_df) == len(sample_test_df)
    assert (result_df["model"] == "gemini-3.7-flash").all()

    # Verify output parquet file on disk
    assert out_file.exists()
    disk_df = pd.read_parquet(out_file)
    assert list(disk_df.columns) == SUBMISSION_COLUMNS
    assert len(disk_df) == len(sample_test_df)
    assert (disk_df["id"].values == sample_test_df["id"].values).all()
    assert (disk_df["model"].values == "gemini-3.7-flash").all()


def test_generate_submission_catches_bad_predictions(sample_test_df: pd.DataFrame, tmp_path: Path):
    """AC-007-a: generate_submission aborts and does not write parquet if model emits invalid label."""
    out_file = tmp_path / "submission.parquet"
    bad_predictor = BadPredictor()

    with pytest.raises(ValueError, match="Invalid model labels found"):
        generate_submission(bad_predictor, sample_test_df, output_path=out_file)

    assert not out_file.exists()


def test_validate_submission_file_roundtrip(sample_test_df: pd.DataFrame, tmp_path: Path):
    """AC-007-a: validate_submission_file reads and validates a saved parquet file."""
    out_file = tmp_path / "submission.parquet"
    predictor = MockPredictor(target_label="qwen3.8-max")
    generate_submission(predictor, sample_test_df, output_path=out_file)

    loaded_df = validate_submission_file(out_file, sample_test_df)
    assert isinstance(loaded_df, pd.DataFrame)
    assert len(loaded_df) == 3


def test_dynamic_sizing_large_test(tmp_path: Path):
    """AC-007-a: Verification on large test set (e.g. 100 rows)."""
    n_rows = 100
    large_test = pd.DataFrame(
        {
            "id": [f"test_{i:04d}" for i in range(n_rows)],
            "text": [f"Synthetic passage {i}" for i in range(n_rows)],
        }
    )
    out_file = tmp_path / "submission_large.parquet"
    predictor = MockPredictor(target_label=VALID_MODELS[0])

    res = generate_submission(predictor, large_test, output_path=out_file)
    assert len(res) == n_rows
    assert out_file.exists()
    disk_df = pd.read_parquet(out_file)
    assert len(disk_df) == n_rows


def test_empty_test_set_handling(tmp_path: Path):
    """AC-007-a: Edge case: empty test set generates empty parquet schema safely."""
    empty_test = pd.DataFrame(columns=["id", "text"])
    out_file = tmp_path / "submission_empty.parquet"
    predictor = MockPredictor()

    res = generate_submission(predictor, empty_test, output_path=out_file)
    assert len(res) == 0
    assert list(res.columns) == SUBMISSION_COLUMNS
    disk_df = pd.read_parquet(out_file)
    assert len(disk_df) == 0
    assert list(disk_df.columns) == SUBMISSION_COLUMNS
