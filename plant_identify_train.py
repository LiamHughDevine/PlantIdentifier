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
    target_resolution = 256
    dense_nodes = 200
    transform = transforms.Compose(
        [
            transforms.Resize((target_resolution, target_resolution)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    training_data = PlantNet(args.dataset, "train", transform=transform)

    num_classes = len(training_data.classes)
    network = ConvolutionalNeuralNetwork(2, target_resolution, 3, 5, dense_nodes, num_classes)
    network.load_weights("plant_network.pkl")

    epochs = 40
    learning_rate = 10

    network.train_data_loader(
        training_data,
        epochs,
        learning_rate,
        binary_cross_entropy,
        binary_cross_entropy_prime,
    )

    network.save_weights("plant_network.pkl")


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
