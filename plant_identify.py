import argparse
import numpy as np
from neural_network import NeuralNetwork
from PIL import Image
from prediction import Prediction


class NoExistingNeuralNetwork(Exception):
    pass


def classify(image: np.ndarray) -> Prediction:
    network = NeuralNetwork()
    if not network.load_weights("model.mdl"):
        raise NoExistingNeuralNetwork()
    image = image.reshape(3, 256, 256)
    prediction = network.forward(image)
    single_prediction = np.argmax(prediction)
    confidence = round(prediction[single_prediction][0] * 100, 2)
    return Prediction(single_prediction, confidence, prediction)


def main(args):
    image_name = args.image_name
    image = None
    try:
        image = Image.open(image_name)
    except OSError:
        print("Please input a valid image")
        return

    width = 256
    height = 256
    image = image.resize((width, height))
    image = image.convert("RGB")

    image_arr = np.array(image)

    try:
        prediction = classify(image_arr)
        print(f"Prediction: {prediction.single_prediction}")
        print(f"Confidence: {prediction.confidence}")
        print(f"Full prediction: {prediction.full_prediction}")
    except NoExistingNeuralNetwork as _:
        print("Please first train the network")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", action="store", dest="image_name", default="")
    args = parser.parse_args()
    main(args)
