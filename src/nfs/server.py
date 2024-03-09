import sys
import time
import json
import logging
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from nfs.config import SERVER_PORT, CONFIG_FOLDER

logger = logging.getLogger(__name__)

def power_of_2(n: str) -> str:
    n_int = int(n)
    time.sleep(3)
    return str(n_int ** 2)

def add(a: str, b: str) -> str:
    a_int = int(a)
    b_int = int(b)
    return str(b_int + a_int)

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


def handle_request(message: str) -> str:
    try:
        data = json.loads(message)
        request_type = data["type"]
    except(json.JSONDecodeError, TypeError, KeyError):
        logger.error("Host sent an invalid request.")
        return "Invalid request."

    if request_type == "square":
        logger.info("Host sent a request to square a number.")
        return power_of_2(data["number"])
    elif request_type == "sum":
        logger.info("Host sent a request to sum two numbers.")
        try:
            result =  add(data["a"], data["b"])
        except KeyError:
            logger.error("Host sent invalid data.")
            return "Invalid data sent."
    else:
        logger.error("Host sent an invalid request.")
        return "Invalid request."

def tcp_server():
    welcoming_port = SERVER_PORT
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(("", welcoming_port))
    server_socket.listen(1)

    logger.info("The server is up and running.")
    while True:
        try:
            connection_socket, client_address = server_socket.accept()
            logger.info(f"TCP tunnel stablished with {client_address}.")
        except KeyboardInterrupt:
            logger.info("Terminating server...")
            server_socket.close()
            sys.exit()

        message = connection_socket.recv(1024)
        logger.info("Recieving...")
        logger.info(f"    Client Message: {message.decode()}")
    
        response = handle_request(message.decode())
        connection_socket.send(response.encode())

        logger.info(f"TCP tunnel with {client_address} closed.")
        connection_socket.close()


if __name__ == "__main__":
    tcp_server()
