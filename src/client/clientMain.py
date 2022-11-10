import socket as sk

from src.utils import initiate_connection
"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""

def client_main(private_key, public_key):
    browser_port = 1700 # listen to browser
    server_port = 5555 # connect to proxy

    socket_browser = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    #reuse socket after crash (dont wait 1 min)
    socket_browser.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    socket_browser.bind(("", browser_port))
    socket_browser.listen()
    print("Listening to browser")

    socket_proxy = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    #reuse socket after crash (dont wait 1 min)
    socket_proxy.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    socket_proxy.connect(("localhost", server_port))


    server_public_key = initiate_connection(public_key, socket_proxy)

    print("connected to server")

    while True:
        try:
            (file_descriptor, _) = socket_browser.accept()

            #recieve and send request
            data = file_descriptor.recv(5000)
            socket_proxy.sendall(data)

            #recieve and send res
            res = socket_proxy.recv(20000)
            file_descriptor.send(res + b"\r\n\r\n")

            file_descriptor.close()

        except (KeyboardInterrupt, OSError):
            socket_browser.close()
            socket_proxy.close()
            #TODO : close socket when interupt / finished
        except UnicodeDecodeError:
            pass

