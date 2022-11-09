import socket
import sys
from threading import Thread
from src.server.handleClients import client_handler
from cryptography.hazmat.primitives import serialization


def server_main():
    with open("./id_rsa", "rb") as key_file:
        server_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    with open("./id_rsa.pub", "rb") as key_file:
        server_public_key = key_file.read()

    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

        kwargs = {"connection": connection,
                  "client": client,
                  "server_private_key": server_private_key,
                  "server_public_key": server_public_key}

        thread = Thread(target=client_handler, kwargs=kwargs)
        thread.start()
        thread_pool.append(thread)

    # Closing socket
    tcp_socket.close()

    # Joining threads
    for thread in thread_pool:
        print("closing threads")
        thread.join(2)
