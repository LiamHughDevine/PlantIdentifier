import argparse
import os
from convolutional_neural_network import ConvolutionalNeuralNetwork
from loss import binary_cross_entropy, binary_cross_entropy_prime
from torchvision import transforms
from torchvision.datasets import ImageFolder


class PlantNet(ImageFolder):
    def __init__(self, root, split, **kwargs):
        self.root = root
        self.split = split
        super().__init__(self.split_folder, **kwargs)

    @property
    def split_folder(self):
        return os.path.join(self.root, self.split)


def main(args):
    transform = transforms.Compose(
        [
            transforms.Resize((600, 600)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    training_data = PlantNet(args.dataset, "train", transform=transform)

    num_classes = len(training_data.classes)
    network = ConvolutionalNeuralNetwork(2, 600, 3, 5, 200, num_classes)

    epochs = 20
    learning_rate = 0.1

    network.train_data_loader(
        training_data,
        epochs,
        learning_rate,
        binary_cross_entropy,
        binary_cross_entropy_prime,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        action="store",
        dest="dataset",
        default=os.path.dirname(os.path.realpath(__file__)) + "/plantnet_300K/images",
    )
    args = parser.parse_args()
    print(args.dataset)
    main(args)
