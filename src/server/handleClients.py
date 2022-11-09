import requests as req

def client_handler(*arg):
    """
    Main function of the client handler
    :param arg:  arg passed by the thread
    """
    connection = arg[0]
    while True:
        data = str(connection.recv(2048))
        print(data)

        #if cmd.startswith(b"exit"):
        #    break
