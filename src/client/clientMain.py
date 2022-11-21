import math
import socket as sk
import time

from src.utils import (
    asym_decrypt,
    asym_encrypt,
    asym_join_and_decrypt,
    asym_split_and_encrypt,
    asym_initiate_connection,
    sym_decrypt,
    sym_encrypt,
    Fernet,
)

"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""

def test_rsa(socket_proxy, server_public_key, client_private_key):
    print("Testing RSA client side")

    socket_proxy.send(asym_encrypt(server_public_key, b'Rammus best waifu'))

    data = b''
    fernet = None

    while data == b'':
        data = socket_proxy.recv(2048)

    if asym_decrypt(client_private_key, data) == b'Indeed, rammus best waifu':
        print("RSA is working server side, sending ack")
        socket_proxy.send(b"OK")
        #recieve key for frenet
        key = socket_proxy.recv(2048)
        key = asym_decrypt(client_private_key, key)
        fernet = Fernet(key)
    else:
        print("ERROR RSA is not working server side")
        exit(0)

    return fernet



def client_main(client_private_key, client_public_key, server_ip):
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
    socket_proxy.connect((server_ip, server_port))

    server_public_key = asym_initiate_connection(client_public_key, socket_proxy)

    fernet = test_rsa(socket_proxy, server_public_key, client_private_key)

    print("connected to server.")

    while True:
        try:
            (file_descriptor, _) = socket_browser.accept()

            # receive and send request
            data = file_descriptor.recv(5000)

            #sym encription of data
            data = sym_encrypt(data, fernet)

            # Sending the request
            socket_proxy.sendall(data)

            # Receiving the response (100kB max)
            data = socket_proxy.recv(100000)
            data = sym_decrypt(data, fernet)
            file_descriptor.send(data)

            file_descriptor.close()

        except (KeyboardInterrupt, OSError):
            socket_browser.close()
            socket_proxy.close()
            # TODO : close socket when interupt / finished
        except UnicodeDecodeError as e:
            print(e)
