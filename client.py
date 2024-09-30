import socket

BUFFER_SIZE = 4096
SERVER_IP = "192.168.0.50"
SERVER_PORT = 2222
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
FORMAT = "utf-8"
IDENTIFY = "!IDENTIFY"
SEND = "!SEND"

def send_file(client, file):
    data = file.read()
    client.recv(5)
    while True:
        packet = bytes(data[:BUFFER_SIZE])
        if not packet:
            return
        client.send(packet)
        client.recv(5)
        data = data[BUFFER_SIZE:]


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDRESS)
    identify_encode = IDENTIFY.encode("utf-8")
    client.send(identify_encode)

    try:
        with open("PlantTestImage1.jpg", "rb") as file:
            send_file(client, file)
            print("Image sent")
            plant_name = client.recv(BUFFER_SIZE)
            plant_name = plant_name.decode(FORMAT)
            print(f"Plant: {plant_name}")
    except OSError:
        print("Please input a valid image")


if __name__ == "__main__":
    main()
