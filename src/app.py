import sys
import json
import threading
from nfs.server import tcp_server, pendingConnectionRequests
from nfs.client import tcp_client
from nfs.database import DatabaseConnector, DBhandler
from nfs.config import WSL_HOST

def validate_ip(ip: str) -> bool:
    ip_parts = ip.split(".")
    if len(ip_parts) != 4:
        return False

    for part in ip_parts:
        try:
            part_int = int(part)
            if part_int < 0 or part_int > 255:
                return False
        except ValueError:
            return False

    return True

def add_host() -> None:
    name = input("Enter the host name: ")
    host = input("Enter the host ip: ")
    port = input("Enter the host port (hit enter for default port 12000): ")
    
    if not validate_ip(host):
        print("Invalid ip address.")
        return

    with DatabaseConnector() as con:
        db = DBhandler(con)
        if port == "":
            db.add_host(name, host)
        else:
            db.add_host(name, host, int(port))

    print(f"Host {name} ({host}, {port}) added to the list.")

def send_connect_host_request() -> None:
    print("To connect a new host, enter the following information:")
    name = input("Enter the host name: ")
    host = input("Enter the host ip: ")
    port_str = input("Enter the host port (hit enter for default port 12000): ")
    
    if not validate_ip(host):
        print("Invalid ip address.")
        return
    
    try:
        port = int(port_str) if port_str != "" else 12000
    except ValueError:
        print("Invalid port.")
        return

    data: dict[str, str] = {
        "type": "connect_host_request",
        "dst_host_name": name,
        "dst_host_ip": host,
        "dst_host_port": port,
        "is_wsl_host": WSL_HOST
    }

    ans: str = tcp_client(data["dst_host_ip"], data["dst_host_port"], data)

    if ans == "request-saved":
        print("Connection request saved by the dst host. Adding to database.")
        with DatabaseConnector() as con:
            db = DBhandler(con)
            db.add_host(name, host, port)
    else:
        print("Request not saved by the dst host.")

def send_accept_connect_request(data: dict) -> bool:
    data["type"] = "accept_connect_request"
    ans: str = tcp_client(data["src_host_ip"], data["src_host_server_port"], data)

    if ans == "confirmation-received":
        with DatabaseConnector() as con:
            db = DBhandler(con)
            db.add_host("fix-naming", data["src_host_ip"], data["src_host_server_port"], status="connected")
        return True
    else:
        print("Confirmation message not received by the requesting host.")
        return False
    
def list_connected_hosts() -> None:
    print("Connected hosts:")
    with DatabaseConnector() as con:
        db = DBhandler(con)
        hosts = db.get_hosts()

    if len(hosts) == 0:
        print("No hosts added found.")
        return

    for host in hosts:
        print(f"    [ID={host["host_id"]}] (ip={host["ip"]}, name={host["name"]}, added_at={host["added_date"]}, status={host["status"]})")


def review_pending_connection_requests() -> None:
    if len(pendingConnectionRequests) == 0:
        print("No pending connection requests found.")
        return
    
    print("Pending connection requests:")
    for i, request in enumerate(pendingConnectionRequests):
        print(request)
        print(f"    {i + 1}. (IP={request['src_host_ip']}, ServerPort={request["src_host_server_port"]}")

    while True:
        try:
            option = int(input("Select a request to accept or reject (0 to exit): "))
            if option > len(pendingConnectionRequests):
                print("Invalid option.")
            elif option == 0:
                return
            else:
                break
        except ValueError:
            print("Invalid option.")
    
    selected_host_data = pendingConnectionRequests[option - 1]
    

    action = input("Do you want to accept? (y/n): ").lower()
    while True:
        if action == "y":
            print("Request accepted.")
            if send_accept_connect_request(selected_host_data):
                pendingConnectionRequests.pop(option - 1)
                print("Request removed from pending list.")
            break
        elif action == "n":
            print("Request rejected is not implemented yet. Just stop the program to remove the request.")
            break
        else:
            print("Invalid action.")

def select_a_host() -> dict | None:
    print("Select a host:")

    with DatabaseConnector() as con:
        db = DBhandler(con)
        hosts = db.get_hosts(filter_by="connected")

    if len(hosts) == 0:
        print("No hosts connected.")
        return None

    for i, host in enumerate(hosts):
        print(f"    {i + 1}. [ID={host["host_id"]}] {host["ip"]} ({host["name"]})")

    try:
        option = int(input("Select an option: "))
        if option < 1 or option > len(hosts):
            print("Invalid option.")
            return None
        else:
            return hosts[option - 1]
    except ValueError:
        print("Invalid option.")
        return None
        
# def handle_square(selected_host: str) -> None:
#     number = input("\nEnter a number: ")
#     if selected_host == "":
#         print("You must select a host first.")
#         return
    
#     data: dict[str, str] = {
#         "type": "square",
#         "number": number
#     }

#     tcp_client(selected_host, json.dumps(data))

# def handle_sum(selected_host: str) -> None:
#     a = input("\nEnter the first number: ")
#     b = input("Enter the second number: ")
    
    
#     data: dict[str, str] = {
#         "type": "sum",
#         "a": a,
#         "b": b
#     }

#     tcp_client(selected_host, json.dumps(data))

def main():
    print("App started")
    server_thread = threading.Thread(target=tcp_server)
    server_thread.daemon = True
    server_thread.start()

    selected_host: dict = None

    while True:
        print()

        if selected_host:
            print(f"Selected Host: {selected_host['ip']} ({selected_host['name']})")
        
        print("Options:")
        print("    1. Add new host")
        print("    2. Select a host")
        print("    3. Get the square of a number from the selected host")
        print("    4. Sum two numbers")
        print("    5. Send connection request to another host")
        print("    6. Review pending connection requests")
        print("    7. list connected hosts")
        print("    0. Exit")

        try:
            option = int(input("Select an option: "))
            
            if option == 1:
                add_host()
            elif option == 2:
                selected_host = select_a_host()
            # elif option == 3:
            #     if selected_host is None:
            #         print("You must select a host first.")
            #         continue
            #     handle_square(selected_host["ip"])
            # elif option == 4:
            #     if selected_host is None:
            #         print("You must select a host first.")
            #         continue
            #     handle_sum(selected_host["ip"])
            elif option == 5:
                send_connect_host_request()
            elif option == 6:
                review_pending_connection_requests()
            elif option == 7:
                list_connected_hosts()
            else:
                print("Exiting app...")
                sys.exit()
        except KeyboardInterrupt:
            print("Exiting app...")
            sys.exit()

if __name__ == "__main__":
    main()
    
