import sys
import time
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


def power_of_2(n: str) -> str:
    n_int = int(n)
    time.sleep(3)
    return str(n_int ** 2)


def udp_server():
    server_port = 12000
    server_socket = socket(AF_INET, SOCK_DGRAM)

    server_socket.bind(("", server_port))

    print("The server is up and running.")
    while True:
        try:
            message, client_address = server_socket.recvfrom(2048)
        except KeyboardInterrupt:
            print("\nTerminating server...")
            sys.exit()

        print("Recieving...")
        print(f"    Client Message: {message.decode()}")
        print(f"    Client Address: {client_address}")

        response = power_of_2(message.decode())
        server_socket.sendto(response.encode(), client_address)


def tcp_server():
    welcoming_port = 12000
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(("", welcoming_port))
    server_socket.listen(1)

    print("The server is up and running.")
    while True:
        try:
            connection_socket, client_address = server_socket.accept()
            print(f"\n\nTCP tunnel stablished with {client_address}.")
        except KeyboardInterrupt:
            print("\nTerminating server...")
            server_socket.close()
            sys.exit()

        message = connection_socket.recv(1024)
        print("Recieving...")
        print(f"    Client Message: {message.decode()}")

        response = power_of_2(message.decode())
        connection_socket.send(response.encode())

        print(f"TCP tunnel with {client_address} closed.")
        connection_socket.close()


if __name__ == "__main__":
    tcp_server()
