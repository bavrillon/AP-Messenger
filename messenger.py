from argparse import ArgumentParser
from time import sleep

from data.client import Client
from data.server import LocalServer
from data.server import RemoteServer


def initialisation_server() :           # Récupération du server (json) utilisé et conversion en instance de Server
    parser = ArgumentParser()
    parser.add_argument('-s','--server',type=str, help = 'Enter json server path')
    parser.add_argument('--url',type=str, help = 'Enter the url of a remote server')
    args = parser.parse_args()
    # FORCER A AVOIR 1 ET 1 SEUL UNQUE ARGUMENT (NECESSAIRE) !!
    if (args.server == None) and  (args.url == None) :
        return(None)
    elif args.server != None :            # Local server
        print(f'Server json : {args.server}')
        sleep(0.5)
        jason_file_name = args.server
        local_server = LocalServer.load(jason_file_name)    
        return(local_server)
    elif args.url != None :            # Remote server
        print(f'Remote Server : {args.url}')
        sleep(0.5)
        url = args.url
        remote_server = RemoteServer(url)    
        return(remote_server)

if __name__ == "__main__":
    server = initialisation_server()
    if server == None :
        print('Vous devez démarrer le programme avec un serveur. Lancer "--help" pour des informations supplémentaires')
    else :
        client = Client(server)
        client.main_menu()  