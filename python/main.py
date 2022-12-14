import argparse
import subprocess

from cryptography.hazmat.primitives import serialization

from src.RSA import generate_keys
from src.client.clientMain import client_main
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

    parser.add_argument("-i", "--ipServer", help = "specify ip address of server" \
            + " (default = localhost)", default = "localhost")

    parser.add_argument("--cBackend", help="use backend written in c",
            action="store_true", default = False)

    args = parser.parse_args()

    private_key, public_key = 0, 0

    if not args.regenRsa and not args.cBackend:
        try:
            with open("./id_rsa", "rb") as key_file:
                #NOTE reading only gives python object, not bytes
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                )

            with open("./id_rsa.pub", "rb") as key_file:
                public_key = key_file.read()

        except FileNotFoundError:
            print("No keys found ! please regen then with --regenRsa")
    else:
        public_key, private_key = generate_keys()


    ## END ARGUMENT PARSER
    if args.server:
        if args.cBackend:
            #becase of NOTE we need to regen files
            #(or figure out another way)
            #remove b'...'
            subprocess.run(["./src/server/c/main.o", str(private_key)[2:-1],
                            str(public_key)[2:-1]], check=False)
        else:
            server_main(private_key, public_key)
    elif args.client:
        client_main(private_key, public_key, args.ipServer)
    else:
        print("Error : please specify either --client or --server")
