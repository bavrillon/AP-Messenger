from argparse import ArgumentParser
from data.client import Client
from data.server import Server

def initialisation_server() :           # Récupération du server (json) utilisé et conversion en instance de Server
    parser = ArgumentParser()
    parser.add_argument('-s','--server', help = 'Enter json server path')
    args = parser.parse_args()
    print(f'Server json : {args.server}')
    jason_file_name = args.server
    server = Server.load(jason_file_name)    
    return(server)

if __name__ == "__main__":
    server = initialisation_server()
    client = Client(server)
    client.main_menu()  