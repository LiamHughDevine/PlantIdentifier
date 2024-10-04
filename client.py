import socket

BUFFER_SIZE = 1024
SERVER_IP = "192.168.0.50"
SERVER_PORT = 2222
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
FORMAT = "utf-8"
IDENTIFY = "!IDENTIFY"
SEND = "!SEND"


def send_data(client: socket.socket, data: bytes):
    while True:
        client.recv(5)
        packet = bytes(data[:BUFFER_SIZE])
        if not packet:
            client.send(bytes())
            return
        client.send(packet)
        data = data[BUFFER_SIZE:]
        if len(packet) < BUFFER_SIZE:
            return


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDRESS)
    identify_encode = IDENTIFY.encode("utf-8")
    client.send(identify_encode)
    print("Image Sending")

    data = bytes()
    try:
        with open("PlantTestImage1.jpg", "rb") as file:
            data = file.read()
    except OSError:
        print("Please input a valid image")

    send_data(client, data)
    print("Image sent")
    plant_name = client.recv(BUFFER_SIZE)
    plant_name = plant_name.decode(FORMAT)
    print(f"Plant: {plant_name}")


if __name__ == "__main__":
    main()
