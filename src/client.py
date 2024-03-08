from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


def udp_client():
    server_name = '192.168.0.42'
    port = 12000

    n = 36

    message = str(n).encode()

    client_socket = socket(AF_INET, SOCK_DGRAM)

    client_socket.sendto(message, (server_name, port))

    response, server_address = client_socket.recvfrom(2048)

    print(f"Sending address: {client_socket.getsockname()}")
    print(f"Server Answer: {response.decode()}")
    print(f"Server Address: {server_address}")

    client_socket.close()


def tcp_client():
    server_name = '192.168.0.42'
    port = 12000

    n = 12

    message = str(n).encode()

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, port))

    client_socket.send(message)
    response = client_socket.recv(1024)

    print(f"Sending address: {client_socket.getsockname()}")
    print(f"Server Answer: {response.decode()}")

    client_socket.close()


if __name__ == "__main__":
    tcp_client()
