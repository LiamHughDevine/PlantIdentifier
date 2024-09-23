import numpy as np
from layer import Layer


class Reshape(Layer):
    def __init__(
        self, input_shape: tuple[int, int, int], output_shape: tuple[int, int]
    ):
        self.input_shape = input_shape
        self.output_shape = output_shape

    def forward(self, input: np.ndarray) -> np.ndarray:
        return np.reshape(input, self.output_shape)

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        # The reshape layer does not need to learn
        _ = learning_rate
        return np.reshape(output_gradient, self.input_shape)
