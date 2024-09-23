import numpy as np
import pickle
from abc import ABC, abstractmethod
from collections.abc import MutableSequence
from layer import Layer
from typing import Callable


class NeuralNetwork(ABC):
    @abstractmethod
    def __init__(self):
        self.layers: MutableSequence[Layer] = []

    def load_weights(self, file_name: str) -> bool:
        try:
            with open(file_name, "rb") as file:
                self.layers = pickle.load(file)
                return True
        except OSError:
            return False

    def save_weights(self, file_name: str) -> None:
        with open(file_name, "wb") as file:
            pickle.dump(self.layers, file)

    def forward(self, input: np.ndarray) -> np.ndarray:
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def __backward(self, grad: np.ndarray, learning_rate: float) -> None:
        for layer in reversed(self.layers):
            grad = layer.backward(grad, learning_rate)

    def train(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        epochs: int,
        learning_rate: float,
        loss_function: Callable,
        loss_function_prime: Callable,
    ) -> None:
        for e in range(epochs):
            error = 0
            for x, y in zip(x_train, y_train):
                output = self.forward(x)

                error += loss_function(y, output)
                grad = loss_function_prime(y, output)

                self.__backward(grad, learning_rate)

            error /= len(x_train)
            print(f"{e + 1}/{epochs}, error={error}")
