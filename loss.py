import numpy as np


def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


def binary_cross_entropy_prime(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return ((1 - y_true) / (1 - y_pred) - y_true / y_pred) / np.size(y_true)
