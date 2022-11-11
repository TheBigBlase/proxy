import math
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def initiate_connection(public_key, socket):
    socket.send(public_key)
    return serialization.load_pem_public_key(socket.recv(5000))


def encrypt(public_key, data):
    return public_key.encrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))


def decrypt(private_key, data):
    return private_key.decrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))


def chunk_and_encrypt(public_key, data, chunk_size=190):
    data_chunks = []

    for i in range(math.ceil(len(data) / chunk_size)):
        data_chunks.append(data[i * chunk_size:i * chunk_size + chunk_size])

    return b';\n;\n'.join([encrypt(public_key, data) for data in data_chunks])
