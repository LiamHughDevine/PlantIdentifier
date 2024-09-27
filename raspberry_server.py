import socket
import time


def main():
    buffer_size = 1024
    server_port = 2222
    server_ip = "192.168.0.50"
    message_from_server = "Hello"
    bytes_to_send = message_from_server.encode("utf-8")
    raspberry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    raspberry_socket.bind((server_ip, server_port))
    print("Server is running")
    message, address = raspberry_socket.recvfrom(buffer_size)
    message = message.decode("utf-8")
    print(message)
    print(f"Client address: {address[0]}")
    raspberry_socket.sendto(bytes_to_send, address)


if __name__ == "__main__":
    main()
