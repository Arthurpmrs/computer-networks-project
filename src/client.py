from socket import socket, AF_INET, SOCK_DGRAM


def main():
    server_name = '192.168.0.42'
    port = 12000

    n = 36

    message = str(n).encode()

    client_socket = socket(AF_INET, SOCK_DGRAM)

    client_socket.sendto(message, (server_name, port))

    response, server_address = client_socket.recvfrom(2048)

    print(f"Seding address: {client_socket.getsockname()}")
    print(f"Server Answer: {response.decode()}")
    print(f"Server Address: {server_address}")

    client_socket.close()


if __name__ == "__main__":
    main()
