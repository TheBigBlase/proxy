from src.RSA import generateKeys

def initiate_connection(public_key, socket):
    socket.send(public_key)
    return socket.recv(5000)
