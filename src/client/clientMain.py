import socket as sk
import math
import time

from src.utils import initiate_connection, encrypt, decrypt, chunk_and_encrypt

"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""


def client_main(client_private_key, client_public_key):
    browser_port = 1700  # listen to browser
    server_port = 5555  # connect to proxy

    socket_browser = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    # reuse socket after crash (don't wait 1 min)
    socket_browser.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    socket_browser.bind(("", browser_port))
    socket_browser.listen()
    print("Listening to browser")

    socket_proxy = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    # reuse socket after crash (don't wait 1 min)
    socket_proxy.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    socket_proxy.connect(("51.178.85.45", server_port))

    server_public_key = initiate_connection(client_public_key, socket_proxy)

    print("connected to server.")
    print("Testing RSA client side")

    socket_proxy.send(encrypt(server_public_key, b'Rammus best waifu'))

    data = b''
    while data == b'':
        data = socket_proxy.recv(2048)
        print(data)

    if decrypt(client_private_key, data) == b'Indeed, rammus best waifu':
        print("RSA is working server side")
    else:
        print("ERROR RSA is not working server side")
        exit(0)

    while True:
        try:
            (file_descriptor, _) = socket_browser.accept()

            # receive and send request
            data = file_descriptor.recv(5000)
            print(data)

            # Splitting data into separate chunks cause of RSA asymmetric limitations
            encrypted_data_chunks = chunk_and_encrypt(server_public_key, data)

            socket_proxy.sendall(encrypted_data_chunks)

            encrypted_data_chunks = socket_proxy.recv(5000)

            data_chunks = [decrypt(client_private_key, encrypted_data) for encrypted_data in
                           encrypted_data_chunks.split(b';\n;\n')]

            file_descriptor.send(b''.join(data_chunks) + b"\r\n\r\n")

            file_descriptor.close()

        except (KeyboardInterrupt, OSError):
            socket_browser.close()
            socket_proxy.close()
            # TODO : close socket when interupt / finished
        except UnicodeDecodeError as e:
            print(e)
