import numpy as np
import socket
from neural_network import NeuralNetwork
from PIL import Image
from prediction import Prediction


class NoExistingNeuralNetwork(Exception):
    pass


def classify(network: NeuralNetwork, image: np.ndarray) -> Prediction:
    image = image.reshape(3, 256, 256)
    prediction = network.forward(image)
    single_prediction = np.argmax(prediction)
    confidence = round(prediction[single_prediction][0] * 100, 2)
    return Prediction(single_prediction, confidence, prediction)


def main():
    network = NeuralNetwork()
    if not network.load_weights("plant_network.pkl"):
        raise NoExistingNeuralNetwork()

    buffer_size = 1024
    server_ip = "192.168.0.50"
    server_port = 2222
    server_address = (server_ip, server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    print("Server is running")

    send_encode = "SEND".encode("utf-8")
    while True:
        data = bytes()
        receiving = True
        while receiving:
            try:
                packet, client_address = server_socket.recvfrom(buffer_size)
                print("Packet received")
                server_socket.sendto(send_encode, client_address)
            except Exception as error:
                receiving = False
                packet = bytes()
                print(error)
            data += bytes(packet)
            if len(packet) < buffer_size:
                receiving = False
        print(data)

        image_name = "received_image.jpg"
        with open(image_name, "wb") as file:
            file.write(data)

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
            prediction = classify(network, image_arr)
            print(f"Prediction: {prediction.single_prediction}")
            print(f"Confidence: {prediction.confidence}")
            print(f"Full prediction: {prediction.full_prediction}")
            print(f"Plant: {prediction.plant_name}")
        except NoExistingNeuralNetwork as _:
            print("Please first train the network")


if __name__ == "__main__":
    main()
