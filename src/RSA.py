from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generatePrivateKey():
    privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publicKey = privateKey.public_key()

    return publicKey, privateKey


a, b = generatePrivateKey()
print(type(a))
print(a)
print(type(b))
print(b)

print(a.public_bytes
      (
          encoding=serialization.Encoding.PEM,
          format=serialization.PublicFormat.SubjectPublicKeyInfo)
      )