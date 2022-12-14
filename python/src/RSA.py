from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_key = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
    public_key = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

    
    with open("id_rsa", "wb") as file:
        file.write(
            private_key
        )

    # Write the public key in the id_ras.pub file
    with open("id_rsa.pub", "wb") as file:
        file.write(
            public_key
        )

    os.chmod("id_rsa", 0o700)#private key is read only form user only

    return public_key, private_key


#public_key, private_key = generatePrivateKey()

