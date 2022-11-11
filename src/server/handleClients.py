from requests import Request, Session
from requests.exceptions import InvalidSchema, ConnectionError

from src.utils import initiate_connection, encrypt, decrypt, split_and_encrypt, join_and_decrypt


def client_handler(**kwargs):
    """
    Main function of the client handler
    :param kwargs:  arg passed by the thread
    """
    s = Session()

    socket = kwargs["connection"]
    server_private_key = kwargs["server_private_key"]
    server_public_key = kwargs["server_public_key"]

    client_public_key = initiate_connection(server_public_key, socket)

    print(f"Connected with client {kwargs['client']}")
    print("Testing RSA client side")

    data = b''
    while data == b'':
        data = socket.recv(2048)
        print(data)

    if decrypt(server_private_key, data) == b'Rammus best waifu':
        print("RSA is working client side")
    else:
        print("ERROR RSA is not working client side")
        exit(0)

    print("Testing RSA server side")

    socket.send(encrypt(client_public_key, b'Indeed, rammus best waifu'))

    while True:
        encrypted_data_chunks = socket.recv(5000)

        if encrypted_data_chunks == b'':
            continue

        # Joining and decrypting chunks
        data = str(join_and_decrypt(server_private_key, encrypted_data_chunks))

        print(data)
        print(f"Type de data: {type(data)}")

        reqs = data.split("\r\n\r\n")

        try:
            reqs.remove("")
        except ValueError as e:
            print(e)

        for req in reqs:
            first_req = req.replace("\r", "").split("\n")

            first_line = first_req[0].split(" ")

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
            res = s.send(request)

            print("[REQ]", *(k for k in first_line), res.status_code)  # lmao

            # Splitting and encrypting chunks
            encrypted_data_chunks = split_and_encrypt(client_public_key, res.content)

            socket.sendall(encrypted_data_chunks)

            # TODO handle https
