import sys
import json
import threading
from nfs.server import tcp_server
from nfs.client import tcp_client
from nfs.database import DatabaseConnector, DBhandler

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

def select_a_host() -> dict | None:
    print("Select a host:")

    with DatabaseConnector() as con:
        db = DBhandler(con)
        hosts = db.get_hosts()

    if len(hosts) == 0:
        print("No hosts added found.")
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
        

def handle_square(selected_host: str) -> None:
    number = input("\nEnter a number: ")
    if selected_host == "":
        print("You must select a host first.")
        return
    
    data: dict[str, str] = {
        "type": "square",
        "number": number
    }

    tcp_client(selected_host, json.dumps(data))

def handle_sum(selected_host: str) -> None:
    a = input("\nEnter the first number: ")
    b = input("Enter the second number: ")
    
    
    data: dict[str, str] = {
        "type": "sum",
        "a": a,
        "b": b
    }

    tcp_client(selected_host, json.dumps(data))

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
        print("    0. Exit")

        try:
            option = int(input("Select an option: "))
            
            if option == 1:
                add_host()
            elif option == 2:
                selected_host = select_a_host()
            elif option == 3:
                if selected_host is None:
                    print("You must select a host first.")
                    continue
                handle_square(selected_host["ip"])
            elif option == 4:
                if selected_host is None:
                    print("You must select a host first.")
                    continue
                handle_sum(selected_host["ip"])
            else:
                print("Exiting app...")
                sys.exit()
        except KeyboardInterrupt:
            print("Exiting app...")
            sys.exit()


if __name__ == "__main__":
    main()