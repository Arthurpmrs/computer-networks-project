import sys
import time
import json
import logging
import threading
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from nfs.config import SERVER_PORT, CONFIG_FOLDER
from nfs.database import DatabaseConnector, DBhandler

logger = logging.getLogger(__name__)

pendingConnectionRequests: list[dict] = []

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


def handle_request(message: str, client_address: tuple[str, str]) -> str:
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
            return add(data["a"], data["b"])
        except KeyError:
            logger.error("Host sent invalid data.")
            return "Invalid data sent."
    elif request_type == "connect_host_request":
        logger.info("Another host has sent a connection request.")
        print(data)
        print(client_address)
        if data.get("is_wsl_host"):
            data.update({"src_host_ip": client_address[0]})
        # data.update({"requesting_host_ip": client_address[0]})
        # data.update({"requesting_host_port": client_address[1]})

        pendingConnectionRequests.append(data)
        logger.info("Request saved. Waiting confirmation.")
        return "Request saved. Waiting confirmation."
    else:
        logger.error("Host sent an invalid request.")
        return "Invalid request."

def handle_client(connection_socket: socket, client_address: tuple[str, str]):
    while True:
        data = connection_socket.recv(1024)
        if not data:
            break

        message = data.decode()
        logger.info(f"Recieving from {client_address}...")
        logger.info(f"    Client Message: {message}")

        response = handle_request(message, client_address)
        connection_socket.send(response.encode())

    logger.info(f"TCP tunnel with {client_address} closed.")
    connection_socket.close()

def tcp_server():
    welcoming_port = SERVER_PORT
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(("", welcoming_port))
    server_socket.listen(10)

    logger.info("The server is up and running.")
    while True:
        try:
            connection_socket, client_address = server_socket.accept()
            logger.info(f"TCP tunnel stablished with {client_address}.")
            
            client_thread = threading.Thread(
                target=handle_client, 
                args=(connection_socket, client_address)
            )
            client_thread.start()
        except KeyboardInterrupt:
            logger.info("Terminating server...")
            server_socket.close()
            sys.exit()


if __name__ == "__main__":
    tcp_server()
