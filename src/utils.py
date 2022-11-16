import math
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


##ASYM FUNCTIONS
def asym_initiate_connection(public_key, socket):
    socket.send(public_key)
    return serialization.load_pem_public_key(socket.recv(5000))


def asym_encrypt(public_key, data):
    return public_key.encrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))


def asym_decrypt(private_key, data):
    return private_key.decrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))


def asym_split_and_encrypt(public_key, data, chunk_size=190):
    """
    Split data into chunks with a len of chunk_size
    Each chunk is then encrypted
    :param public_key:
    :param data:
    :param chunk_size:
    :return: byte
    """
    data_chunks = []

    # Loops the exact number of chunks needed
    for i in range(math.ceil(len(data) / chunk_size)):
        data_chunks.append(data[i * chunk_size:i * chunk_size + chunk_size])

    encrypted_data_chunks = []

    # Encrypt each chunk
    for data in data_chunks:
        encrypted_data_chunks.append(asym_encrypt(public_key, data))

    # Joins each chunks with a separator
    res = b';\n;\n'.join(encrypted_data_chunks)

    return res


def asym_join_and_decrypt(private_key, data):
    """
    Decrypts each chunk and join
    :param private_key:
    :param data:
    :return: original data
    """
    data_chunks = []

    # Splitting and decrypting each chunk
    for encrypted_data in data.split(b';\n;\n'):
        data_chunks.append(asym_decrypt(private_key, encrypted_data))

    # Joins each chunk to retrieve the original string
    res = b''.join(data_chunks)

    return res


##SYM FUNCTIONS
def sym_gen_key():
    """
    create a sym key and the object permiting to encrypt data
    :return fernet, object used to encrypt / decrypt
    """
    key = Fernet.generate_key()
    fernet = Fernet(key)
    return fernet, key

def sym_encrypt(message, f):
    return f.encrypt(message)

def sym_decrypt(crypted, f):
    return f.decrypt(crypted)
