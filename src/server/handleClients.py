from requests import Request, Session
from requests.exceptions import InvalidSchema, ConnectionError

def client_handler(*arg):
    """
    Main function of the client handler
    :param arg:  arg passed by the thread
    """
    s = Session()



    connection = arg[0]
    while True:
        data = connection.recv(5000).decode()
        reqs = data.split("\r\n\r\n")
        reqs.remove("")

        for req in reqs:
            print(req)
            first_req = req.replace("\r","").split("\n")

            first_line = first_req[0].split(" ")

            fields = first_req[1:] #ignore the GET / HTTP/1.1
            if "" in fields:
                fields.remove("")
            output = {}

            for field in fields:
                if not field:
                    continue
                try:
                    key,value = field.split(': ')
                    output[key] = value
                except (InvalidSchema, ConnectionError):
                    continue
                except ValueError:
                    pass

            print(first_line[0], first_line[1], output)

            request = Request(first_line[0], first_line[1], headers = output).prepare()
            res = s.send(request)
            connection.send(res.content)
            #TODO handle https

        #if cmd.startswith(b"exit"):
        #    break
