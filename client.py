import socket


def send_file(client_socket, server_address, buffer_size, file):
    data = file.read()
    client_socket.recv(4)
    while True:
        packet = bytes(data[:buffer_size])
        if not packet:
            return
        client_socket.sendto(packet, server_address)
        client_socket.recv(4)
        data = data[buffer_size:]


def main():
    buffer_size = 1024
    server_ip = "192.168.0.50"
    server_port = 2222
    server_address = (server_ip, server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    identify_encode = "IDENTIFY".encode("utf-8")
    client_socket.sendto(identify_encode, server_address)

    try:
        with open("PlantTestImage1.jpg", "rb") as file:
            send_file(client_socket, server_address, buffer_size, file)
            print("Image sent")
            plant_name = client_socket.recv(buffer_size)
            plant_name = plant_name.decode("utf-8")
            print(f"Plant: {plant_name}")
    except OSError:
        print("Please input a valid image")


if __name__ == "__main__":
    main()
