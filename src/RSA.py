from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generatePrivateKey():
    privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publicKey = privateKey.public_key()

    return publicKey, privateKey


publicKey, privateKey = generatePrivateKey()

with open("../id_rsa", "wb") as file:
    file.write(privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Write the public key in the id_ras.pub file
with open("../id_rsa.pub", "wb") as file:
    file.write(publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    )
