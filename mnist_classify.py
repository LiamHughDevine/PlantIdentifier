import argparse
import numpy as np
from neural_network import NeuralNetwork
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--image", action="store", dest="image_name", default="")
args = parser.parse_args()


def main():
    network = NeuralNetwork()
    if not network.load_weights("model.mdl"):
        print("Please first train the network")
        return
    image_name = args.image_name
    image = None
    try:
        image = Image.open(image_name)
    except OSError:
        print("Please input a valid image")
        return

    print(type(image))
    width = 28
    height = 28
    image = image.resize((width, height))
    # Converts to 256 grayscale
    image = image.convert("L")
    image.save("Test.jpg")

    image_arr = np.array(image)
    image_arr = image_arr.reshape(1, 28, 28)
    prediction = network.forward(image_arr)
    single_prediction = np.argmax(prediction)
    confidence = round(prediction[single_prediction][0] * 100, 2)
    print(f"Prediction: {single_prediction}")
    print(f"Confidence: {confidence}")
    print(f"Full prediction: {prediction}")


if __name__ == "__main__":
    main()
