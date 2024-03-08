import sys
from socket import socket, AF_INET, SOCK_DGRAM


def power_of_2(n: str) -> str:
    n_int = int(n)
    return str(n_int ** 2)


def main():
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


if __name__ == "__main__":
    main()
