from convolutional import Convolutional
from dense import Dense
from neural_network import NeuralNetwork
from reshape import Reshape
from sigmoid import Sigmoid


class ConvolutionalNeuralNetwork(NeuralNetwork):
    def __init__(
        self,
        input_depth: int,
        input_size: int,
        kernel_size: int,
        kernels: int,
        dense_nodes: int,
        output_size: int,
    ):
        assert input_size >= kernel_size
        convolution_size = input_size - kernel_size + 1
        convolution_total_entries = kernels * convolution_size * convolution_size

        self.layers = [
            Convolutional((input_depth, input_size, input_size), kernel_size, kernels),
            Sigmoid(),
            Reshape(
                (kernels, convolution_size, convolution_size),
                (convolution_total_entries, 1),
            ),
            Dense(convolution_total_entries, dense_nodes),
            Sigmoid(),
            Dense(dense_nodes, output_size),
            Sigmoid(),
        ]
