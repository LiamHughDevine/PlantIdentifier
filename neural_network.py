from keras.api.utils import to_categorical
import numpy as np
import pickle
import torch
from abc import ABC
from collections.abc import MutableSequence
from layer import Layer
from torch.utils.data import DataLoader
from typing import Callable, Tuple
from torchvision.datasets import ImageFolder


class NeuralNetwork(ABC):
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

    def train_ndarray(
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

    Batch = Tuple[torch.Tensor, torch.Tensor]
    def train_data_loader(
        self,
        image_folder: ImageFolder,
        epochs: int,
        learning_rate: float,
        loss_function: Callable,
        loss_function_prime: Callable,
    ) -> None:
        """
        all_labels = []
        for _, labels in data_loader:
            print("TEST")
            all_labels.append(labels)
        print("TEST2")
        all_labels = torch.cat(all_labels)
        unique_labels = torch.unique(all_labels)
        num_labels = len(unique_labels)
        """

        limit = 100
        data_loader = DataLoader(image_folder, batch_size=limit, shuffle=True)
        unique_labels = image_folder.classes
        num_labels = len(unique_labels)
        label_mapping = {}
        for i in range(num_labels):
            label_mapping[unique_labels[i]] = i

        print(label_mapping)

        for e in range(epochs):
            error = 0
            for batch_idx, (images, labels) in enumerate(data_loader):
                _ = batch_idx
                for i in range(images.size(0)):
                    image = images[i]
                    label = labels[i].item()

                    print(image)
                    print(label)
                    label = to_categorical(label, num_labels)
                    label.reshape(len(label), 1)
                    print(label)

                    output = self.forward(image)
                    print(output)

                    error += loss_function(label, output)
                    grad = loss_function_prime(label, output)

                    self.__backward(grad, learning_rate)

            error /= len(data_loader)
            print(f"{e + 1}/{epochs}, error={error}")
