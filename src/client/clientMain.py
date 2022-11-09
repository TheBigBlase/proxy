import socket as sk
"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""

def client_main():
    browser_port = 1700 # listen to browser
    server_port = 5555 # connect to proxy

    socket_client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket_client.bind(("", browser_port))
    socket_client.listen()
    print("Listening to browser")

    socket_proxy = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket_proxy.connect(("localhost", server_port))

    print("connected to server")

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
