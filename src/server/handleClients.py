def client_handler(*arg):
    """
    Main function of the client handler
    :param arg:  arg passed by the thread
    """
    connection = arg[0]
    while True:
        data = connection.recv(32)
        print("Received data: {data}")

        cmd = data.split(" ")[0]
        if cmd.startswith(b"exit"):
            break



