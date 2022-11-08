import socket as sk

"""
J'ai paramétré mon navigateur (Firefox) pour qu'il redirige toutes les données 
HTTP et HTTPS au localhost port 1700
"""

numeroPort = 1700

socketServeur = sk.socket()
socketServeur.bind(("", numeroPort))
socketServeur.listen()
print("\nA l'écoute\n")

while (True) :
    (socketPourClient, clientIP) = socketServeur.accept()
    """
    print(socketForClient, "\n")
    print(clientIP, "\n")
    print(serverSocket)
    """
    data = socketPourClient.recv(1700)
    print("************************\n", data, "\n************************\n\n")

    socketPourClient.close()