from src.server.serverMain import serverMain
from src.client.clientMain import clientMain

import argparse

if __name__ == "__main__":
    ## BEGIN ARGUMENT PARSER
    parser = argparse.ArgumentParser(\
            description="lightweight handler to run server or client")

    parser.add_argument("-s", "--server", help = "run server",\
            action="store_true", default = False)

    parser.add_argument("-c", "--client", help = "make a new cache "\
            + "file (useful for storing data)",
            action="store_true", default = False)

    args = parser.parse_args()
    ## END ARGUMENT PARSER
    if args.server:
        serverMain()
    elif args.client:
        clientMain()
    else:
        print("Error : please specify either --client or --server")
