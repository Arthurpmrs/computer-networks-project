import json
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, gethostbyname, gethostname
from nfs.config import SERVER_PORT

def udp_client():
    server_name = '192.168.0.36'
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


def tcp_client(server_name: str, server_port: int, data: dict):
    # server_name = '192.168.0.36'
    # server_port = 12000
    data.update({
        "src_host_ip": gethostbyname(gethostname()),
        "src_host_server_port": SERVER_PORT
    })
    
    message = json.dumps(data)
    # n = input("Digite um número para ser elevado ao quadrado: ")

    # message = str(number).encode()

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, data["dst_host_port"]))

    print(f"Requesting to server (ip={server_name}, port={server_port})...")
    client_socket.send(message.encode())
    response = client_socket.recv(1024)

    # print(f"Server Answer: {response.decode()}")
    # print(f"Sending address: {client_socket.getsockname()}")

    print("Response received. Closing conection...\n")
    client_socket.close()

    ans = response.decode()
    print(f"Sua resposta é: {ans}")


if __name__ == "__main__":
    tcp_client()
