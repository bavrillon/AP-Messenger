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
    if (args.server is None) and  (args.url is None) :
        return None # Pas besoin de mettre des parenthèses sur un return
    elif args.server is not None :            # Local server
        print(f'Server json : {args.server}')
        sleep(0.5)
        jason_file_name = args.server
        local_server = LocalServer.load(jason_file_name)
        return local_server
    elif args.url is not None :            # Remote server
        print(f'Remote Server : {args.url}')
        sleep(0.5)
        url = args.url
        remote_server = RemoteServer(url)
        return remote_server

if __name__ == "__main__":
    server = initialisation_server()
    # En Python, on préfère en général écrire "is None" que "== None".
    # C'est plus une convention qu'autre chose, mais si vous voulez en savoir
    # plus sur les raisons historiques, vous pouvez lire cet article :
    # http://jaredgrubb.blogspot.com/2009/04/python-is-none-vs-none.html
    if server is None:
        print('Vous devez démarrer le programme avec un serveur. Lancer "--help" pour des informations supplémentaires')
        exit()

    # Fonctionnellement il n'y a pas de différence entre if + else ou if + exit sans else.
    # Mais le sens que vous transmettez n'est pas le même :
    # if / else signifie que vous mettez les 2 conditions sur un pied d'égalité
    # if + exit signifie "on évactue rapidement un cas d'erreur, puis on continue le flot normal d'exécution"
    client = Client(server)
    client.main_menu()
