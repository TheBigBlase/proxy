from requests import Request, Session
from requests.exceptions import ConnectionError, InvalidSchema

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
        print(data)

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


def recieve_from_client(socket, server_private_key, fernet)->list[str]:
    encrypted_data = socket.recv(5000)

    if encrypted_data == b'':
        return [""]

    # Joining and decrypting chunks
    #data = str(asym_join_and_decrypt(server_private_key, encrypted_data), "utf-8")
    #sym version : 
    try:
        data = str(sym_decrypt(encrypted_data, fernet), "utf-8")
    except UnicodeDecodeError:
        #remove B'...' manually
        data = str(sym_decrypt(encrypted_data, fernet))[2:-2]

    reqs = data.split("\r\n\r\n")

    try:
        reqs.remove("")
    except ValueError as error:
        print(error)

    return reqs


def client_handler(**kwargs):
    """
    Main function of the client handler
    :param kwargs:  arg passed by the thread
    """
    session = Session()

    socket = kwargs["connection"]
    server_private_key = kwargs["server_private_key"]
    server_public_key = kwargs["server_public_key"]
    fernet = kwargs["fernet"]

    client_public_key = asym_initiate_connection(server_public_key, socket)

    print(f"Connected with client {kwargs['client']}")

    fernet = test_rsa(socket, server_private_key, client_public_key)

    while True:
        reqs = recieve_from_client(socket, server_private_key, fernet)

        for req in reqs:
            first_req = req.replace("\r", "").split("\n")

            first_line = first_req[0].split(" ")

            if first_line[0].startswith("CONNECT"):
                print("[CONNECT] unhandled connect request (https)")
                socket.close()#it crashes anyway, faster this way
                continue


            fields = first_req[1:]  # ignore the GET / HTTP/1.1
            if "" in fields:
                fields.remove("")
            output = {}

            for field in fields:
                if not field:
                    continue
                try:
                    key, value = field.split(': ')
                    output[key] = value
                except (InvalidSchema, ConnectionError):
                    continue
                except ValueError:
                    pass

            # build and send request
            request = Request(first_line[0], first_line[1], headers=output).prepare()
            res = session.send(request)

            print("[REQ]", *(k for k in first_line), res.status_code)  # lmao

            #sym encrypt and send data
            encrypted_data = sym_encrypt(res.content, fernet)

            socket.sendall(encrypted_data)
            #TODO handle https
