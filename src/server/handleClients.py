def client_handler(**kwargs):
    """
    Main function of the client handler
    :param arg:  arg passed by the thread
    """
    connection = kwargs["connection"]
    server_private_key = kwargs["server_private_key"]
    server_public_key = kwargs["server_public_key"]

    connection.send("SENDING SERVER PUBLIC KEY\n" + server_public_key)

    while True:
        data = connection.recv(32)
        print("Received data: {data}")

        cmd = data.split(" ")[0]
        if cmd.startswith(b"exit"):
            break



