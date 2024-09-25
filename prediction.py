import numpy as np


class Prediction:
    def __init__(
        self, single_prediction: np.intp, confidence: float, full_prediction: np.ndarray
    ):
        self.single_prediction = single_prediction
        self.confidence = confidence
        self.full_prediction = full_prediction
