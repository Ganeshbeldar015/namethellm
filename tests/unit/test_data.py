import pytest
import pandas as pd
from pathlib import Path

from namethellm import data
from namethellm.constants import VALID_MODELS, TRAIN_COLUMNS, TEST_COLUMNS


def test_load_train_data_shape_and_columns():
    """AC-001-a: Loads train.csv with 2,699 rows and correct columns."""
    df = data.load_train_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2699, 4)
    assert list(df.columns) == TRAIN_COLUMNS


def test_load_train_data_valid_labels():
    """AC-001-a: All models belong to the 18 approved candidate models."""
    df = data.load_train_data()
    unique_models = set(df["model"].unique())
    assert len(unique_models) == 18
    assert unique_models == set(VALID_MODELS)


def test_load_train_data_no_nulls():
    """AC-001-a: Zero null values exist in any column."""
    df = data.load_train_data()
    assert df.isnull().sum().sum() == 0


def test_validate_train_schema_missing_column():
    """Raises ValueError if required column is missing."""
    df = pd.DataFrame({"id": ["1"], "prompt_id": ["p1"], "text": ["hello"]})
    with pytest.raises(ValueError, match="Missing required columns"):
        data.validate_train_schema(df)


def test_validate_train_schema_invalid_label():
    """Raises ValueError if model label is outside the 18 candidate models."""
    df = pd.DataFrame({
        "id": ["1"],
        "prompt_id": ["p1"],
        "text": ["hello"],
        "model": ["unapproved-model-v1"]
    })
    with pytest.raises(ValueError, match="Invalid model labels found"):
        data.validate_train_schema(df)


def test_load_test_data():
    """AC-001-b: Loads test.csv with id and text columns."""
    df = data.load_test_data()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == TEST_COLUMNS
    assert df.isnull().sum().sum() == 0


def test_load_sample_submission():
    """Loads sample_submission.parquet with id and model columns."""
    df = data.load_sample_submission()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "model"]
    assert df.shape[0] > 0


def test_missing_file_raises_filenotfound(tmp_path):
    """Attempting to load missing file raises FileNotFoundError."""
    missing_path = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        data.load_train_data(missing_path)
