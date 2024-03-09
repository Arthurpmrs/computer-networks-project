import sys
import threading
from server import tcp_server
from client import tcp_client

def main():
    print("App started")
    server_thread = threading.Thread(target=tcp_server)
    server_thread.daemon = True
    server_thread.start()

    outside_server_name = input("Enter the outside server ip: ")

    while True:
        print("Options:")
        print("    1. Get the power of 2 of a number")
        print("    2. Exit")

        try:
            option = int(input("Select an option: "))
            if option == 1:
                number = input("Enter a number: ")
                tcp_client(outside_server_name, int(number))
            else:
                print("Exiting app...")
                sys.exit()
        except KeyboardInterrupt:
            print("Exiting app...")
            sys.exit()


if __name__ == "__main__":
    main()