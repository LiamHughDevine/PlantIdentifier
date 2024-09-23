import numpy as np
from activation import Activation


class Sigmoid(Activation):
    def __init__(self):
        def sigmoid(x: np.ndarray) -> np.ndarray:
            return 1 / (1 + np.exp(-x))

        def sigmoid_prime(x: np.ndarray) -> np.ndarray:
            s = sigmoid(x)
            return s * (1 - s)

        super().__init__(sigmoid, sigmoid_prime)
