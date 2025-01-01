import json
from argparse import ArgumentParser
from data.client import Client
from data.server import Server

def start() :           # Récupération du server (json) utilisé
    parser = ArgumentParser()
    parser.add_argument('-s','--server', help = 'Enter json server path')
    args = parser.parse_args()
    print(f'Server json : {args.server}')
    jason_file_name = args.server
    return (jason_file_name)

if __name__ == "__main__":
    JASON_FILE_NAME = start()
    SERVER = Server.load(JASON_FILE_NAME)
    CLIENT = Client(SERVER)
    CLIENT.main_menu()  