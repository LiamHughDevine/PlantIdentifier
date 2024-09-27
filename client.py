import socket

def main():
    buffer_size = 1024
    server_address = ("192.168.0.50", 2222)
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message_from_client = "Hello from client"
    bytes_to_send = message_from_client.encode("utf-8")
    udp_client.sendto(bytes_to_send, server_address)
    data, address = udp_client.recvfrom(buffer_size)
    data = data.decode("utf-8")
    print(f"Data from server: {data}")
    print(f"Server IP address: {address[0]}")
    print(f"Server port: {address[1]}")


if __name__ == "__main__":
    main()
