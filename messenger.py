from argparse import ArgumentParser
from data.client import Client
from data.server import LocalServer
from data.server import RemoteServer


def initialisation_server() :           # Récupération du server (json) utilisé et conversion en instance de Server
    parser = ArgumentParser()
    parser.add_argument('-s','--server',type=str, help = 'Enter json server path')
    parser.add_argument('--url',type=str, help = 'Enter the url of a remote server')
    args = parser.parse_args()
    # FORCER A AVOIR 1 ET 1 SEUL UNQUE ARGUMENT (NECESSAIRE)
    if args.server != None :            # Local server
        print(f'Server json : {args.server}')
        jason_file_name = args.server
        local_server = LocalServer.load(jason_file_name)    
        return(local_server)
    if args.url != None :            # Remote server
        print(f'Remote Server : {args.url}')
        url = args.url
        remote_server = RemoteServer(url)    
        return(remote_server)

if __name__ == "__main__":
    server = initialisation_server()
    client = Client(server)
    client.main_menu()  