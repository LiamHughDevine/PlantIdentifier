import numpy as np
from convolutional_neural_network import ConvolutionalNeuralNetwork
from keras.api.datasets import mnist
from keras.api.utils import to_categorical
from loss import binary_cross_entropy, binary_cross_entropy_prime


def preprocess_data(x, y, limit):
    zero_index = np.where(y == 0)[0][:limit]
    one_index = np.where(y == 1)[0][:limit]
    all_indices = np.hstack((zero_index, one_index))
    all_indices = np.random.permutation(all_indices)
    x = x[all_indices]
    x = x.reshape(len(x), 1, 28, 28)
    y = y[all_indices]
    y = to_categorical(y)
    y = y.reshape(len(y), 2, 1)
    return x, y


def main():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, y_train = preprocess_data(x_train, y_train, 100)
    x_test, y_test = preprocess_data(x_test, y_test, 100)

    network = ConvolutionalNeuralNetwork(1, 28, 3, 5, 100, 2)
    network.load_weights("model.mdl")

    epochs = 20
    learning_rate = 0.1

    network.train_ndarray(
        x_train,
        y_train,
        epochs,
        learning_rate,
        binary_cross_entropy,
        binary_cross_entropy_prime,
    )

    for x, y in zip(x_test, y_test):
        output = network.forward(x)
        print(f"pred: {np.argmax(output)}, true: {np.argmax(y)}")

    network.save_weights("model.mdl")


if __name__ == "__main__":
    main()
