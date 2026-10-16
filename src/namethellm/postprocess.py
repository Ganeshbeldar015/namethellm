"""Postprocessing, probability calibration, and decision thresholding."""

from typing import Any, Optional
import numpy as np
from sklearn.base import BaseEstimator


class BalancedAccuracyCalibrator(BaseEstimator):
    """Calibrate multi-class probability distributions to maximize Balanced Accuracy.

    Uses marginal frequency power scaling:
      w_c = 1.0 / (V_c ** gamma)
      P_calibrated = P * w_c / sum(P * w_c)

    Where V_c is the expected marginal prediction volume for class c.
    This prevents common/easy classes from overshadowing difficult classes,
    increasing macro-averaged recall without degrading calibrated probabilities.
    """

    def __init__(self, gamma: float = 0.05) -> None:
        self.gamma = gamma
        self.weights_: Optional[np.ndarray] = None

    def fit(
        self,
        probs: np.ndarray,
        y: Optional[Any] = None,
    ) -> "BalancedAccuracyCalibrator":
        """Compute class weights based on marginal prediction volume."""
        probs = np.asarray(probs, dtype=np.float64)
        marginal_volume = probs.sum(axis=0) + 1e-6
        if self.gamma == 0.0:
            self.weights_ = np.ones(probs.shape[1], dtype=np.float64)
        else:
            w = 1.0 / (marginal_volume**self.gamma)
            self.weights_ = w / w.mean()
        return self

    def calibrate(self, probs: np.ndarray) -> np.ndarray:
        """Apply learned class calibration weights to probability matrix."""
        probs = np.asarray(probs, dtype=np.float64)
        if self.weights_ is None:
            self.fit(probs)

        calibrated = probs * self.weights_
        # Normalize rows to sum to 1.0
        row_sums = calibrated.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1.0, row_sums)
        return calibrated / row_sums

    def predict(self, probs: np.ndarray) -> np.ndarray:
        """Predict class indices maximizing calibrated probabilities."""
        calibrated = self.calibrate(probs)
        return np.argmax(calibrated, axis=1)
