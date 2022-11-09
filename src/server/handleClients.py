import requests as req


def client_handler(**kwargs):
    """
    Main function of the client handler
    :param kwargs:  arg passed by the thread
    """
    connection = kwargs["connection"]
    server_private_key = kwargs["server_private_key"]
    server_public_key = kwargs["server_public_key"]

    connection.send("SENDING SERVER PUBLIC KEY\n" + server_public_key)

    while True:
        data = str(connection.recv(2048))
        print(data)

        #if cmd.startswith(b"exit"):
        #    break
