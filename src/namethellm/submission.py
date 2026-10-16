"""Verified submission.parquet generator and defensive validator."""

import logging
from pathlib import Path
from typing import Any, Union
import pandas as pd

from namethellm.constants import SUBMISSION_COLUMNS, VALID_MODELS_SET

logger = logging.getLogger(__name__)


def validate_submission(sub_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    """Validate submission DataFrame against strict competition requirements.

    Ensures:
      1. sub_df is a pandas DataFrame.
      2. Columns match SUBMISSION_COLUMNS exactly (['id', 'model']).
      3. Row count matches test_df exactly.
      4. 'id' values match test_df row-for-row with zero duplicates.
      5. Zero null or NaN values in either column.
      6. All values in 'model' are valid labels from VALID_MODELS.

    Raises:
      TypeError: If sub_df is not a DataFrame.
      ValueError: If any validation rule is violated.
    """
    if not isinstance(sub_df, pd.DataFrame):
        raise TypeError(f"sub_df must be a pandas DataFrame, got {type(sub_df).__name__}")

    if list(sub_df.columns) != SUBMISSION_COLUMNS:
        raise ValueError(
            f"Columns must match {SUBMISSION_COLUMNS} exactly, got {list(sub_df.columns)}"
        )

    if len(sub_df) != len(test_df):
        raise ValueError(
            f"Row count mismatch: expected {len(test_df)} rows, got {len(sub_df)} rows"
        )

    if sub_df.isna().sum().sum() > 0:
        null_counts = sub_df.isna().sum().to_dict()
        raise ValueError(f"Submission contains null or NaN values: {null_counts}")

    if len(test_df) > 0:
        if not (sub_df["id"].values == test_df["id"].values).all():
            raise ValueError(
                "IDs do not match test_df row-for-row, or ID order is misaligned."
            )

    if len(sub_df) > 0:
        invalid_labels = set(sub_df["model"]) - VALID_MODELS_SET
        if invalid_labels:
            raise ValueError(
                f"Invalid model labels found: {sorted(invalid_labels)}. "
                f"All predictions must be members of VALID_MODELS."
            )


def generate_submission(
    model: Any,
    test_df: pd.DataFrame,
    output_path: Union[str, Path] = "submission.parquet",
) -> pd.DataFrame:
    """Generate and validate a submission DataFrame and write to Apache Parquet.

    Args:
      model: Fitted estimator exposing a predict(texts) method.
      test_df: Test set DataFrame containing at least ['id', 'text'] columns.
      output_path: Path where submission.parquet will be written.

    Returns:
      Validated submission DataFrame.

    Raises:
      ValueError: If predictions or resulting DataFrame fail validation.
    """
    output_path = Path(output_path)

    if len(test_df) == 0:
        sub_df = pd.DataFrame(columns=SUBMISSION_COLUMNS)
    else:
        predictions = model.predict(test_df["text"])
        sub_df = pd.DataFrame(
            {
                "id": test_df["id"].values,
                "model": predictions,
            }
        )

    # Validate before persisting
    validate_submission(sub_df, test_df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sub_df.to_parquet(output_path, index=False, engine="pyarrow")
    logger.info("Successfully wrote %d rows to %s", len(sub_df), output_path)

    return sub_df


def validate_submission_file(
    file_path: Union[str, Path],
    test_df: pd.DataFrame,
) -> pd.DataFrame:
    """Read a submission parquet file from disk and run complete validation.

    Args:
      file_path: Path to existing submission.parquet.
      test_df: Ground truth test DataFrame to validate against.

    Returns:
      Validated DataFrame loaded from parquet.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Submission file does not exist: {file_path}")

    sub_df = pd.read_parquet(file_path, engine="pyarrow")
    validate_submission(sub_df, test_df)
    return sub_df


def main() -> None:
    """CLI entrypoint: trains baseline model and generates submission.parquet."""
    from namethellm.data import load_test_data, load_train_data
    from namethellm.models.baseline import BaselineTFIDFClassifier

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger.info("Loading training and test data...")
    train_df = load_train_data()
    test_df = load_test_data()

    logger.info(
        "Fitting baseline TF-IDF model on %d training samples...", len(train_df)
    )
    clf = BaselineTFIDFClassifier()
    clf.fit(train_df["text"], train_df["model"])

    submission_file = Path("submission.parquet")
    logger.info("Generating %s for %d test samples...", submission_file, len(test_df))
    generate_submission(clf, test_df, output_path=submission_file)

    logger.info("Verifying generated file...")
    sub_df = validate_submission_file(submission_file, test_df)
    logger.info("Validation PASSED. Generated submission preview:")
    logger.info("\n%s", sub_df.head())


if __name__ == "__main__":
    main()
