import argparse
from src.server.serverMain import server_main
from src.client.clientMain import client_main


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
        server_main()
    elif args.client:
        client_main()
    else:
        print("Error : please specify either --client or --server")
