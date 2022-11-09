import socket as sk
"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""

def client_main():
    browser_port = 1700 # listen to browser
    server_port = 5555 # connect to proxy

    socket_browser = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket_browser.bind(("", browser_port))
    socket_browser.listen()
    print("Listening to browser")

    socket_proxy = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket_proxy.connect(("localhost", server_port))

    print("connected to server")

    while True:
        try:
            (file_descriptor, client_IP) = socket_browser.accept()
            """
            print(socketForClient, "\n")
            print(clientIP, "\n")
            print(serverSocket)
            """
            data = file_descriptor.recv(5000)
            socket_proxy.sendall(data)
            res = socket_proxy.recv(20000)

            file_descriptor.send(res + b"\r\n\r\n")
            res.decode("utf-8")

            print(res + b"\r\n\r\n")

            file_descriptor.close()

        except (KeyboardInterrupt, OSError):
            socket_browser.close()
            socket_proxy.close()
            #TODO : close socket when interupt / finished
        except UnicodeDecodeError:
            pass

