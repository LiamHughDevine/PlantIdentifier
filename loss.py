import numpy as np


def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    # Prevents divide by zero error
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


def binary_cross_entropy_prime(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    # Prevents divide by zero error
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return ((1 - y_true) / (1 - y_pred) - y_true / y_pred) / np.size(y_true)
