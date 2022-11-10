from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os


def generateKeys():
    privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publicKey = privateKey.public_key()

    privateKey = privateKey.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
    publicKey = publicKey.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

    
    with open("id_rsa", "wb") as file:
        file.write(
            privateKey
        )

    # Write the public key in the id_ras.pub file
    with open("id_rsa.pub", "wb") as file:
        file.write(
            publicKey
        )

    os.chmod("id_rsa", 0o700)#private key is read only form user only

    return publicKey, privateKey


#publicKey, privateKey = generatePrivateKey()

