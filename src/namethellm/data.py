"""Data loading and schema validation module."""

from pathlib import Path
from typing import Union
import pandas as pd

from namethellm.constants import (
    TRAIN_COLUMNS,
    TEST_COLUMNS,
    VALID_MODELS_SET,
)


def validate_train_schema(df: pd.DataFrame) -> None:
    """Validates that train DataFrame conforms to expected schema and label constraints.

    Raises:
        ValueError: If columns are missing, nulls are present, or invalid labels exist.
    """
    missing_cols = [col for col in TRAIN_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in train data: {missing_cols}")

    null_counts = df[TRAIN_COLUMNS].isnull().sum()
    if null_counts.any():
        null_cols = null_counts[null_counts > 0].to_dict()
        raise ValueError(f"Null values detected in train columns: {null_cols}")

    labels = set(df["model"].unique())
    invalid_labels = labels - VALID_MODELS_SET
    if invalid_labels:
        raise ValueError(f"Invalid model labels found in train data: {sorted(invalid_labels)}")


def validate_test_schema(df: pd.DataFrame) -> None:
    """Validates that test DataFrame conforms to expected schema.

    Raises:
        ValueError: If required columns are missing or nulls are present.
    """
    missing_cols = [col for col in TEST_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in test data: {missing_cols}")

    null_counts = df[TEST_COLUMNS].isnull().sum()
    if null_counts.any():
        null_cols = null_counts[null_counts > 0].to_dict()
        raise ValueError(f"Null values detected in test columns: {null_cols}")


def load_train_data(path: Union[str, Path] = "dataset/train.csv") -> pd.DataFrame:
    """Loads and validates the training dataset.

    Args:
        path: Filepath to train.csv.

    Returns:
        Validated pandas DataFrame.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        ValueError: If validation fails.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Training dataset not found: {file_path.resolve()}")

    df = pd.read_csv(file_path)
    validate_train_schema(df)
    return df


def load_test_data(path: Union[str, Path] = "dataset/test.csv") -> pd.DataFrame:
    """Loads and validates the test dataset.

    Args:
        path: Filepath to test.csv.

    Returns:
        Validated pandas DataFrame.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        ValueError: If validation fails.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Test dataset not found: {file_path.resolve()}")

    df = pd.read_csv(file_path)
    validate_test_schema(df)
    return df


def load_sample_submission(
    path: Union[str, Path] = "dataset/sample_submission.parquet"
) -> pd.DataFrame:
    """Loads the sample submission parquet file.

    Args:
        path: Filepath to sample_submission.parquet.

    Returns:
        Loaded pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Sample submission file not found: {file_path.resolve()}")

    return pd.read_parquet(file_path)
