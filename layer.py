import numpy as np
from abc import ABC, abstractmethod


class Layer(ABC):
    @abstractmethod
    def __init__(self):
        self.input = None
        self.output = None

    @abstractmethod
    def forward(self, input: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        pass
