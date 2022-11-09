import socket
import sys
from threading import Thread
from handleClients import client_handler

def serverMain():
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # PORT
    PORT = 5555

    # Bind the socket to server address and PORT
    server_address = ('localhost', PORT)
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

        thread = Thread(target=client_handler, args=(connection, client))
        thread.start()
        thread_pool.append(thread)


    # Closing socket
    tcp_socket.close()

    # Joining threads
    for thread in thread_pool:
        print("closing threads")
        thread.join()
