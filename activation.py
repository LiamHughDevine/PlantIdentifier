import numpy as np
from typing import Callable
from layer import Layer


class Activation(Layer):
    def __init__(self, activation: Callable, activation_prime: Callable):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input: np.ndarray) -> np.ndarray:
        self.input = input
        return self.activation(self.input)

    def backward(self, output_gradient: np.ndarray, learning_rate: float):
        # The activation layer will not change so does not need the learning
        # rate
        _ = learning_rate
        return np.multiply(output_gradient, self.activation_prime(self.input))
