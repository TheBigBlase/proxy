import socket as sk
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""


def client_main():
    with open("./id_rsa", "rb") as key_file:
        client_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    with open("./id_rsa.pub", "rb") as key_file:
        client_public_key = key_file.read()

    browser_port = 1700  # listen to browser
    server_port = 5555  # connect to proxy

    '''
    socket_client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket_client.bind(("", browser_port))
    socket_client.listen()
    print("Listening to browser")
    '''

    # CONNECTING TO PROXY SERVER
    socket_proxy = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket_proxy.connect(("51.178.85.45", server_port))
    print("connected to server")

    # WAITING THE PUBLIC KEY FROM THE SERVER
    server_public_key = listen(socket_proxy)
    server_public_key = serialization.load_pem_public_key(server_public_key)
    print(server_public_key)

    # SENDING OUR PUBLIC KEY TO THE SERVER
    socket_proxy.send(b"SENDING CLIENT PUBLIC KEY\n" + client_public_key)

    # LISTENING SAUSAGE KEYWORD
    data = listen(socket_proxy)

    decrypted_data = client_private_key.decrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
                               )

    if decrypted_data == b'SAUCISSE':
        print('Secure connection with the server verified')
    else:
        print('Couldn\'t manage to secure the connection with the server, decryption did not work')

    # SENDING HOTDOG KEYWORD
    socket_proxy.send(server_public_key.encrypt(b'HOT DOG', padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )))

    '''
    while True:
        try:
            (file_descriptor, client_IP) = socket_client.accept()
            """
            print(socketForClient, "\n")
            print(clientIP, "\n")
            print(serverSocket)
            """
            data = file_descriptor.recv(1700)
            socket_proxy.sendall(data)
            print("************************\n", data, "\n************************\n\n")

            file_descriptor.close()
        except KeyboardInterrupt:
            socket_client.close()
            socket_proxy.close()
            #TODO : close socket when interupt / finished
    '''


def listen(connection) -> bytes:
    data = b''
    while data == b'':
        data = connection.recv(2048)
        print(data)
        return data
