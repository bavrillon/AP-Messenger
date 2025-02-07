import os
import shutil
from psutil import Process
from time import sleep  

from .server import Server

class Client :          #Messenger app
    # Par convention, on écrit les noms
    # de constantes en majuscules
    START_YELLOW_WRITINGS  = '\033[33m'
    START_RED_WRITINGS  = '\033[31m'
    START_GREEN_WRITINGS  = '\033[32m'
    END_COLOR_WRITINGS  = '\033[0m'


    def __init__(self,server: Server):   #En réalité, server est une instance de LocalServer ou RemoteServer, qui sont des classes héritant de la classe Server
        # self.server n'ayant pas vocation à être
        # exposé à l'extérieur, vous pouvez le renommer en
        # self._server
        self.server = server    #Local server OR Remote server
        
    def __repr__(self) -> str:
        return(f'Client(server={self.server})')
    
    def display_users(self) -> None:
        self.clear_screen()
        print(self.START_YELLOW_WRITINGS + '\nUser list\n-------')
        # Il vaut mieux créer la variable users_list directement
        # pour éviter 2 appels à la fonction self.server.get_users,
        # qui peuvent être coûteux lorsqu'ils font appel au réseau
        users_list = self.server.get_users()
        if users_list is None:
            print('Erreur, veuillez réessayer plus tard !')
            sleep(0.8)
            return self.main_menu()
        for user in users_list :
            print(user.id,' - ',user.name)
        print('\nn. Create user\nb. Ban user\nx. Main menu')
        choice = input('Select an option: ' + self.END_COLOR_WRITINGS)
        if choice == 'n':
            new_names_draft = input(self.START_YELLOW_WRITINGS + 'Name of the new users (separators = ,) : ' + self.END_COLOR_WRITINGS)
            # Il vaut mieux appeler .strip() directement, pour éviter
            # de dupliquer (ou oublier) l'appel dans les fonctions
            # Server.create_user
            new_names_list = [name.strip() for name in new_names_draft.split(',')]
            res = self.server.create_user(new_names_list)
            if res == False :
                print('Erreur, la création a échoué, veuillez réessayer plus tard !')
            else : 
                print('La création a été effectuée avec succès !')
            sleep(0.8)
            self.main_menu()
            sleep(0.8)
            # Cette fonction ne sera jamais appelée
            # car on ne sort jamais de self.main_menu
            self.display_users()
        elif choice == 'x':
            self.main_menu()
        elif choice == 'b':
            ID_banned_users_draft = input(self.START_YELLOW_WRITINGS + 'ID of the banned users (separators = ,) : ' + self.END_COLOR_WRITINGS)
            ID_banned_users_list = ID_banned_users_draft.split(',')
            for id_to_ban in ID_banned_users_list :
                if not(id_to_ban.strip().isdigit()) or not(int(id_to_ban.strip()) in [user.id for user in users_list]):
                    print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, id_to_ban)
                    sleep(0.8)
                    self.display_users()
            ID_banned_users = [int(id_to_ban.strip()) for id_to_ban in ID_banned_users_list]
            # La fonction ban_user renvoie toujours None
            res = self.server.ban_user(ID_banned_users)
            if res == False :
                print("Erreur, l'utilisateur n'a pas pu être supprimé, veuillez réessayer plus tard !")
            else : 
                print("L'utilisateur a été supprimé avec succès !")
            sleep(0.8)
            self.display_users()
        else:
            print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, choice)
            sleep(0.8)
            self.display_users()

    def display_messages(self) -> None:
        self.clear_screen()
        channel_ID = input(self.START_YELLOW_WRITINGS + 'ID of the channel : ' + self.END_COLOR_WRITINGS)
        channels_list = self.server.get_channels()
        if channels_list is None:
            print('Erreur, veuillez réessayer plus tard !')
            sleep(0.8)
            return self.main_menu()
        if not(channel_ID.strip().isdigit()) or not(int(channel_ID.strip()) in [channel.id for channel in channels_list]):
                print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, channel_ID)
                sleep(0.8)
                self.display_messages()
        print(self.START_RED_WRITINGS + '\nMessages of the channel')
        size = shutil.get_terminal_size(fallback=(80, 24))
        window_size = size.columns
        print(''+'-' * window_size + '\n')
        if self.server.get_messages(int(channel_ID)) is None:
            print('Erreur, veuillez réessayer plus tard !')
            sleep(0.8)
            self.main_menu()
        messages_list = self.server.get_messages(int(channel_ID))
        for message in messages_list:
        #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
                print(f"{self.START_RED_WRITINGS}{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{self.START_GREEN_WRITINGS}{message.content}{self.END_COLOR_WRITINGS}")
        print(self.START_YELLOW_WRITINGS + 's. Send a message on the channel\no. See another channel\nx. Main menu')
        choice = input('Select an option: ' + self.END_COLOR_WRITINGS)
        if choice == 's':
            sender_id = input(self.START_YELLOW_WRITINGS + 'ID of the sender : ' + self.END_COLOR_WRITINGS)
            if not(sender_id.strip().isdigit()) or not(int(sender_id.strip()) in [user.id for user in self.server.get_users()]):
                print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, sender_id)
                sleep(0.8)
                self.display_messages()
            content = input(self.START_YELLOW_WRITINGS + 'Content of the message : ' + self.END_COLOR_WRITINGS)
            res = self.server.send_message(int(sender_id),int(channel_ID),content)
            if res == False :
                print("Erreur, le message n'a pas pu être envoyé, veuillez réessayer plus tard !")
            else : 
                print("Le message a été envoyé avec succès !")
            sleep(0.8)
            self.display_messages()
        elif choice == 'o':
            self.display_messages()
        elif choice == 'x':
            self.main_menu()
        else:
            print('Unknown option:' + self.END_COLOR_WRITINGS, choice)
            sleep(0.8)
            self.main_menu()

    def display_channels(self) -> None:
        self.clear_screen()
        print(self.START_YELLOW_WRITINGS + '\nChannels list\n-------')
        channels_list = self.server.get_channels()
        for channel in channels_list :
            print(f"{channel.id} - {channel.name} : {channel.members_ids}")
        print('\nn. Create channel\nd. Delete channel\nx. Main menu')
        choice = input('Select an option: ' + self.END_COLOR_WRITINGS)
        if choice == 'n':
            channel = input(self.START_YELLOW_WRITINGS + 'Name of the new channel : ' + self.END_COLOR_WRITINGS)
            first_member_id = input(self.START_YELLOW_WRITINGS + 'ID of the first user belonging to the new channel: ' + self.END_COLOR_WRITINGS)
            if not(first_member_id.isdigit()) or not(int(first_member_id) in [user.id for user in self.server.get_users()]):
                print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, first_member_id)
                sleep(0.8)
                self.display_channels()
            member_ids = [int(first_member_id)] 
            while True:
                choice = input(self.START_YELLOW_WRITINGS + 'Add a member (yes/no) ? : ' + self.END_COLOR_WRITINGS)
                if choice == 'no':
                    break
                elif choice != 'yes':
                    print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, choice)
                    sleep(0.8)
                    self.display_channels()
                other_member_id = input(self.START_YELLOW_WRITINGS + 'ID of the next user belonging to the new channel: ' + self.END_COLOR_WRITINGS)
                if not(other_member_id.isdigit()) or not(int(other_member_id) in [user.id for user in self.server.get_users()]):
                    sleep(0.8)
                    self.display_channels()
                member_ids.append(int(other_member_id))
            member_ids_set = set(member_ids) # Création d'un objet de type set pour supprimer les éventuelles répétitions
            member_ids = list(member_ids_set)
            res = self.server.create_channel(channel,member_ids)
            if res == False :
                print("Erreur, le nouveau groupe n'a pas pu être créé, veuillez réessayer plus tard !")
            else : 
                print("Le nouveau groupe a été créé avec succès !")
            sleep(0.8)
            self.display_channels()
        if choice == 'd':
            ID_channel = input(self.START_YELLOW_WRITINGS + 'ID of the channel to delete : ' + self.END_COLOR_WRITINGS)
            if not(ID_channel.isdigit()) or not(int(ID_channel) in [channel.id for channel in self.server.get_channels()]):
                print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, ID_channel)
                sleep(0.8)
                self.display_channels()          
            res = self.server.delete_channel(int(ID_channel))
            if res == False :
                print("Erreur, le groupe n'a pas pu être supprimé, veuillez réessayer plus tard !")
            else : 
                print("Le groupe a été supprimé avec succès !")
            sleep(0.8)
            self.display_channels()
        elif choice == 'x':
            self.main_menu()
        else:
            print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, choice)
            sleep(0.8)
            self.display_channels()
    
    def main_menu(self) -> None:
        self.clear_screen()
        size = shutil.get_terminal_size(fallback=(80, 24))
        window_size = size.columns
        print(self.START_YELLOW_WRITINGS + ''+'#' * window_size)
        print('# Messenger #')
        print('#' * window_size)
        print('\n1. See users\n2. See channels\n3. See messages\nx. Leave')
        choice = input('Select an option: ' + self.END_COLOR_WRITINGS)
        if choice == 'x':
            print(self.START_YELLOW_WRITINGS + 'Bye!' + self.END_COLOR_WRITINGS)
            exit()
        elif choice == '1':
            self.display_users()
        elif choice == '2':
            self.display_channels()
        elif choice == '3': 
            self.display_messages()
        else:
            print(self.START_YELLOW_WRITINGS + 'Unknown option:' + self.END_COLOR_WRITINGS, choice)
            sleep(0.8)
            self.main_menu()
    
    def clear_screen(self) -> None:
        if Process(os.getppid()).name() == 'bash.exe':
            os.system('clear')
        else :
            os.system('cls' if os.name == 'nt' else 'clear')