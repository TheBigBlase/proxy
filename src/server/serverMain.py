import socket
import sys
from threading import Thread
from src.server.handleClients import client_handler
from src.utils import sym_gen_key


def server_main(server_private_key, server_public_key):
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # PORT
    client_port = 5555

    # Bind the socket to server address and PORT
    server_address = ('', client_port)
    tcp_socket.bind(server_address)

    # Listen on PORT
    tcp_socket.listen(1)

    thread_pool = []

    # Server loop
    while True:
        print("Waiting for connection")
        try:
            connection, client = tcp_socket.accept()
        # Breaks when ctrl+c
        except KeyboardInterrupt:
            break

        print(f"Connected to client IP: {client}")

        fernet = sym_gen_key()

        kwargs = {"connection": connection,
                  "client": client,
                  "server_private_key": server_private_key,
                  "server_public_key": server_public_key,
                  "fernet": fernet
                  }

        thread = Thread(target=client_handler, kwargs=kwargs)
        thread.start()
        thread_pool.append(thread)

    # Closing socket
    tcp_socket.close()

    # Joining threads
    for thread in thread_pool:
        print("closing threads")
        thread.join(2)
