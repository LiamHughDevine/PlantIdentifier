import numpy as np
import socket
import threading
from io import BytesIO
from neural_network import NeuralNetwork
from PIL import Image
from prediction import Prediction


IMAGE_SIZE = 128
BUFFER_SIZE = 1024
SERVER_IP = "192.168.0.50"
SERVER_PORT = 2222
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
FORMAT = "utf-8"
IDENTIFY = "!IDENTIFY"
SEND = "!SEND"


class NoExistingNeuralNetwork(Exception):
    pass


def classify(network: NeuralNetwork, image: np.ndarray) -> Prediction:
    image = image.reshape(3, IMAGE_SIZE, IMAGE_SIZE)
    prediction = network.forward(image)
    single_prediction = np.argmax(prediction)
    confidence = round(prediction[single_prediction][0] * 100, 2)
    return Prediction(single_prediction, confidence, prediction)


def receive_file(connection: socket.socket) -> bytes:
    send_encode = SEND.encode(FORMAT)
    data = bytes()
    receiving = True
    while receiving:
        try:
            connection.send(send_encode)
            packet = connection.recv(BUFFER_SIZE)
        except Exception as error:
            receiving = False
            packet = bytes()
            print(error)
        data += bytes(packet)
        if len(packet) < BUFFER_SIZE:
            receiving = False
    return data


def handle_client(connection: socket.socket, network: NeuralNetwork):
    identify_sent = False
    counter = 0
    while not identify_sent:
        message = connection.recv(BUFFER_SIZE)
        message = message.decode(FORMAT)
        if message == "!IDENTIFY":
            identify_sent = True
        counter += 1
        if counter > 10:
            connection.close()
            return

    data = receive_file(connection)
    print("Image received")

    image = Image.open(BytesIO(data))
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = image.convert("RGB")

    image_arr = np.array(image)

    try:
        prediction = classify(network, image_arr)
        print(f"Prediction: {prediction.single_prediction}")
        print(f"Confidence: {prediction.confidence}")
        print(f"Full prediction: {prediction.full_prediction}")
        print(f"Plant: {prediction.plant_name}")
        plant_name_encode = prediction.plant_name.encode("utf-8")
        connection.send(plant_name_encode)
    except NoExistingNeuralNetwork as _:
        print("Please first train the network")

    connection.close()


def main():
    network = NeuralNetwork()
    if not network.load_weights("plant_network.pkl"):
        raise NoExistingNeuralNetwork()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    print("Server is running")

    server.listen()

    while True:
        connection, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, network))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
