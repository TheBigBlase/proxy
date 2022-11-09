import requests as req
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def client_handler(**kwargs):
    """
    Main function of the client handler
    :param kwargs:  arg passed by the thread
    """
    connection = kwargs["connection"]
    server_private_key = kwargs["server_private_key"]
    server_public_key = kwargs["server_public_key"]

    connection.settimeout(5)

    # SENDING OUR PUBLIC KEY TO THE CLIENT
    connection.send(b"SENDING SERVER PUBLIC KEY\n" + server_public_key)

    # RECEIVING CLIENTS' PUBLIC KEY
    client_public_key = listen(connection)
    client_public_key = serialization.load_pem_public_key(client_public_key)
    print(client_public_key)

    connection.send(client_public_key.encrypt(b'SAUCISSE', padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
                                              ))

    # LISTENING HOT DOG KEYWORD
    data = listen(connection)

    decrypted_data = server_private_key.decrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
                                                )

    if decrypted_data == b'HOT DOG':
        print('Secure connection with the client verified')
    else:
        print('Couldn\'t manage to secure the connection with the client, decryption did not work')


def listen(connection):
    data = b''
    while data == b'':
        data = connection.recv(2048)
        print(data)
        return data

        # if cmd.startswith(b"exit"):
        #    break
