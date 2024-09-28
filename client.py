import socket

def main():
    buffer_size = 1024
    server_ip = "192.168.0.50"
    server_port = 2222
    server_address = (server_ip, server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        with open("TestImage1.jpg", "rb") as file:
            print("Image loaded")
            data = file.read()
            while True:
                packet = bytes(data[:buffer_size])
                if not packet:
                    break
                client_socket.sendto(packet, server_address)
                print("Packet sent")
                client_socket.recv(4)
                data = data[:buffer_size]

    except OSError:
        print("Please input a valid image")
    return
            


if __name__ == "__main__":
    main()
