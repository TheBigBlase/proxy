from requests import Request, Session
from requests.exceptions import ConnectionError, InvalidSchema

import socket as sk

from src.utils import (
    asym_decrypt,
    asym_encrypt,
    asym_join_and_decrypt,
    asym_split_and_encrypt,
    asym_initiate_connection,
    sym_encrypt,
    sym_decrypt,
    sym_gen_key,
    Fernet
)


def test_rsa(socket, server_private_key, client_public_key)->Fernet:
    fernet = None
    print("Testing RSA client side")
    data = b''
    while data == b'':
        data = socket.recv(2048)

    if asym_decrypt(server_private_key, data) == b'Rammus best waifu':
        print("RSA is working client side")
    else:
        print("ERROR RSA is not working client side")
        exit(0)

    print("Testing RSA server side")

    socket.send(asym_encrypt(client_public_key, b'Indeed, rammus best waifu'))
    #TODO wait for ack then send fernet key
    ack = b""
    ack = socket.recv(2)

    if ack == b"OK":
        (fernet, key) = sym_gen_key()
        socket.send(asym_encrypt(client_public_key, key))
    else:
        print("[ERROR] ack failed, sym key not send")
        exit(0)

    return fernet


def recieve_from_client(socket, server_private_key, fernet):
    encrypted_data = socket.recv(5000)

    if encrypted_data == b'':
        return b""

    # Joining and decrypting chunks
    #data = str(asym_join_and_decrypt(server_private_key, encrypted_data), "utf-8")
    #sym version :
    data = sym_decrypt(encrypted_data, fernet)

    return data

def handle_https(web_socket, client_socket, fernet, address, webserver, port, req):
    web_socket.connect((webserver, port))
    web_socket.send(req)

    web_socket.setblocking(0)
    client_socket.setblocking(0)

    request = web_socket.recv(10000)

    web_socket.close()
    client_socket.sendall(sym_encrypt(request, fernet))

def handle_http(web_socket, client_socket, fernet, address, webserver, port, req):

    web_socket.connect((webserver, port))
    web_socket.send(req)

    # Makefile for socket
    file_object = web_socket.makefile('wb', 0)
    file_object.write(b"GET " + bytes(address, "utf-8") + b" HTTP/1.0\n\n")

    res = web_socket.makefile("rb").readlines()
    file_object.close()
    web_socket.close()

    size = []
    toSend = []

    for i in range(0, len(res)):
        toSend.append(sym_encrypt(res[i], fernet))
        size.append(len(toSend[i]))

    client_socket.send(b"{\"SIZE\": " + bytes(str(size), "utf-8") + b"}")
    #recv ack
    if client_socket.recv(2) != b"OK":
        print("error")
        exit(-1)

    for i in toSend:
        client_socket.send(i)

    print("[REQ]", address,
          "OK" if res[0][12:15] == "OK" else "ERROR") # lmao


def client_handler(**kwargs):
    """
    Main function of the client handler
    :param kwargs:  arg passed by the thread
    """

    client_socket = kwargs["connection"]
    server_private_key = kwargs["server_private_key"]
    server_public_key = kwargs["server_public_key"]
    fernet = kwargs["fernet"]

    client_public_key = asym_initiate_connection(server_public_key, client_socket)

    fernet = test_rsa(client_socket, server_private_key, client_public_key)

    while True:
        webserver = ""
        trueReq = recieve_from_client(client_socket, server_private_key, fernet)
        reqs = str(trueReq)[2:-1]

        first_req = reqs.replace("\r", "").split("\n")

        first_line = first_req[0].split(" ")


        web_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        # reuse socket after crash (don't wait 1 min)
        web_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)


        if first_line[0] == "CONNECT":
            webserver = first_line[1]
            webserver = webserver.split(":")
            webserver, port = webserver[0].replace("https://", "").split("/")[0], int(webserver[1])
            handle_https(web_socket, client_socket, fernet, first_line[1], webserver, port, trueReq)

        else:
            webserver = first_line[1].replace("http://", "").split("/")[0]
            port = 80
            handle_http(web_socket, client_socket, fernet, first_line[1], webserver, port, trueReq)
