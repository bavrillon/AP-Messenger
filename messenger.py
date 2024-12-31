import json
import argparse
from data.client import Client
from data.server import Server

def start() :           # Récupération du server (json) utilisé
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--server', help = 'Enter json server path')
    args = parser.parse_args()
    print(f'Server json : {args.server}')
    JASON_FILE_NAME = args.server
    return (JASON_FILE_NAME)

if __name__ == "__main__":
    JASON_FILE_NAME = start()
    server = Server.load(JASON_FILE_NAME)
    client = Client(server)
    client.main_menu()  