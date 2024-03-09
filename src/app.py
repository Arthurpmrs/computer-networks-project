import sys
import json
import threading
from nfs.server import tcp_server
from nfs.client import tcp_client

def add_host(saved_hosts: list[str]) -> None:
    host = input("Enter the host ip: ")
    saved_hosts.append(host)
    print(f"Host {host} added to the list.")

def select_a_host(saved_hosts: list[str]) -> str:
    print("Select a host:")
    for i, host in enumerate(saved_hosts):
        print(f"    {i + 1}. {host}")
    try:
        option = int(input("Select an option: "))
        if option < 1 or option > len(saved_hosts):
            print("Invalid option.")
            return ""
        else:
            return saved_hosts[option - 1]
    except ValueError:
        print("Invalid option.")
        return ""

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

    saved_hosts:list[str] = []
    selected_host: str = ""
    # outside_server_name = input("Enter the outside server ip: ")

    while True:
        print()
        print(f"selected_host: {selected_host}")
        print("Options:")
        print("    1. Add new host")
        print("    2. Select a host")
        print("    3. Get the square of a number from the selected host")
        print("    4. Sum two numbers")
        print("    0. Exit")

        try:
            option = int(input("Select an option: "))
            if option == 1:
                add_host(saved_hosts)
            elif option == 2:
                selected_host = select_a_host(saved_hosts)
            elif option == 3:
                if selected_host == "":
                    print("You must select a host first.")
                    continue
                handle_square(selected_host)
            elif option == 4:
                if selected_host == "":
                    print("You must select a host first.")
                    continue
                handle_sum(selected_host)
            else:
                print("Exiting app...")
                sys.exit()
        except KeyboardInterrupt:
            print("Exiting app...")
            sys.exit()


if __name__ == "__main__":
    main()