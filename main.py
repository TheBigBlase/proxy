import argparse

from cryptography.hazmat.primitives import serialization

from src.client.clientMain import client_main
from src.utils import generateKeys
from src.server.serverMain import server_main

if __name__ == "__main__":
    ## BEGIN ARGUMENT PARSER
    parser = argparse.ArgumentParser(\
            description="lightweight handler to run server or client")

    parser.add_argument("-s", "--server", help = "run server",
            action="store_true", default = False)

    parser.add_argument("-c", "--client", help = "run client",
            action="store_true", default = False)

    parser.add_argument("-r", "--regenRsa", help = "regen rsa keys",
            action="store_true", default = False)

    args = parser.parse_args()

    private_key, public_key = 0, 0

    if not args.regenRsa:
        try:
            with open("./id_rsa", "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                )

            with open("./id_rsa.pub", "rb") as key_file:
                public_key = key_file.read()
                
        except FileNotFoundError:
            print("No keys found ! please regen then with --regenRsa")
    else:
        generateKeys()

    ## END ARGUMENT PARSER
    if args.server:
        server_main(private_key, public_key)
    elif args.client:
        client_main(private_key, public_key)
    else:
        print("Error : please specify either --client or --server")
