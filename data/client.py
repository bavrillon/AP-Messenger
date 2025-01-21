import os
import shutil
from psutil import Process
from time import sleep  

from .server import Server

class Client :          #Messenger app
    start_yellow_writings  = '\033[33m'
    start_red_writings  = '\033[31m'
    start_green_writings  = '\033[32m'
    end_color_writings  = '\033[0m'


    def __init__(self,server: Server):   #En réalité, server est une instance de LocalServer ou RemoteServer, qui sont des classes héritant de la classe Server
        self.server = server    #Local server OR Remote server
        
    def __repr__(self):
        return(f'Client(server={self.server})')
    
    def display_users(self) -> None:
        self.clear_screen()
        print(self.start_yellow_writings + '\nUser list\n-------')
        if self.server.get_users() == False :
            print('Erreur, veuillez réessayer plus tard !')
            sleep(0.8)
            self.main_menu()
        users_list = self.server.get_users()
        for user in users_list :
            print(user.id,' - ',user.name)
        print('\nn. Create user\nb. Ban user\nx. Main menu')
        choice = input('Select an option: ' + self.end_color_writings)
        if choice == 'n':
            new_names_draft = input(self.start_yellow_writings + 'Name of the new users (separators = ,) : ' + self.end_color_writings)
            new_names_list = new_names_draft.split(',')
            res = self.server.create_user(new_names_list)
            if res == False :
                print('Erreur, la création a échoué, veuillez réessayer plus tard !')
            else : 
                print('La création a été effectuée avec succès !')
            sleep(0.8)
            self.main_menu()
            sleep(0.8)
            self.display_users()
        elif choice == 'x':
            self.main_menu()
        elif choice == 'b':
            ID_banned_users_draft = input(self.start_yellow_writings + 'ID of the banned users (separators = ,) : ' + self.end_color_writings)
            ID_banned_users_list = ID_banned_users_draft.split(',')
            for ID in ID_banned_users_list :
                if not(ID.strip().isdigit()) or not(int(ID.strip()) in [user.id for user in self.server.get_users()]):
                    print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, ID)
                    sleep(0.8)
                    self.display_users()
            ID_banned_users = [int(ID.strip()) for ID in ID_banned_users_list]
            res = self.server.ban_user(ID_banned_users)
            if res == False :
                print("Erreur, l'utilisateur n'a pas pu être supprimé, veuillez réessayer plus tard !")
            else : 
                print("L'utilisateur a été supprimé avec succès !")
            sleep(0.8)
            self.display_users()
        else:
            print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, choice)
            sleep(0.8)
            self.display_users()

    def display_messages(self) -> None:
        self.clear_screen()
        channel_ID = input(self.start_yellow_writings + 'ID of the channel : ' + self.end_color_writings)
        if self.server.get_channels() == False :
            print('Erreur, veuillez réessayer plus tard !')
            sleep(0.8)
            self.main_menu()
        channels_list = self.server.get_channels()
        if not(channel_ID.strip().isdigit()) or not(int(channel_ID.strip()) in [channel.id for channel in channels_list]):
                print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, channel_ID)
                sleep(0.8)
                self.display_messages()
        print(self.start_red_writings + '\nMessages of the channel')
        size = shutil.get_terminal_size(fallback=(80, 24))
        window_size = size.columns
        print(''+'-' * window_size + '\n')
        if self.server.get_messages(int(channel_ID)) == False :
            print('Erreur, veuillez réessayer plus tard !')
            sleep(0.8)
            self.main_menu()
        messages_list = self.server.get_messages(int(channel_ID))
        for message in messages_list:
        #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
                print(f"{self.start_red_writings}{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{self.start_green_writings}{message.content}{self.end_color_writings}")
        print(self.start_yellow_writings + 's. Send a message on the channel\no. See another channel\nx. Main menu')
        choice = input('Select an option: ' + self.end_color_writings)
        if choice == 's':
            sender_id = input(self.start_yellow_writings + 'ID of the sender : ' + self.end_color_writings)
            if not(sender_id.strip().isdigit()) or not(int(sender_id.strip()) in [user.id for user in self.server.get_users()]):
                print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, sender_id)
                sleep(0.8)
                self.display_messages()
            content = input(self.start_yellow_writings + 'Content of the message : ' + self.end_color_writings)
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
            print('Unknown option:' + self.end_color_writings, choice)
            sleep(0.8)
            self.main_menu()

    def display_channels(self) -> None:
        self.clear_screen()
        print(self.start_yellow_writings + '\nChannels list\n-------')
        channels_list = self.server.get_channels()
        for channel in channels_list :
            print(f"{channel.id} - {channel.name} : {channel.members_ids}")
        print('\nn. Create channel\nd. Delete channel\nx. Main menu')
        choice = input('Select an option: ' + self.end_color_writings)
        if choice == 'n':
            channel = input(self.start_yellow_writings + 'Name of the new channel : ' + self.end_color_writings)
            first_member_id = input(self.start_yellow_writings + 'ID of the first user belonging to the new channel: ' + self.end_color_writings)
            if not(first_member_id.isdigit()) or not(int(first_member_id) in [user.id for user in self.server.get_users()]):
                print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, first_member_id)
                sleep(0.8)
                self.display_channels()
            member_ids = [int(first_member_id)] 
            while True:
                choice = input(self.start_yellow_writings + 'Add a member (yes/no) ? : ' + self.end_color_writings)
                if choice == 'no':
                    break
                elif choice != 'yes':
                    print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, choice)
                    sleep(0.8)
                    self.display_channels()
                other_member_id = input(self.start_yellow_writings + 'ID of the next user belonging to the new channel: ' + self.end_color_writings)
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
            ID_channel = input(self.start_yellow_writings + 'ID of the channel to delete : ' + self.end_color_writings)
            if not(ID_channel.isdigit()) or not(int(ID_channel) in [channel.id for channel in self.server.get_channels()]):
                print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, ID_channel)
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
            print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, choice)
            sleep(0.8)
            self.display_channels()
    
    def main_menu(self) -> None:
        self.clear_screen()
        size = shutil.get_terminal_size(fallback=(80, 24))
        window_size = size.columns
        print(self.start_yellow_writings + ''+'#' * window_size)
        print('# Messenger #')
        print('#' * window_size)
        print('\n1. See users\n2. See channels\n3. See messages\nx. Leave')
        choice = input('Select an option: ' + self.end_color_writings)
        if choice == 'x':
            print(self.start_yellow_writings + 'Bye!' + self.end_color_writings)
            exit()
        elif choice == '1':
            self.display_users()
        elif choice == '2':
            self.display_channels()
        elif choice == '3': 
            self.display_messages()
        else:
            print(self.start_yellow_writings + 'Unknown option:' + self.end_color_writings, choice)
            sleep(0.8)
            self.main_menu()
    
    def clear_screen(self) -> None:
        if Process(os.getppid()).name() == 'bash.exe':
            os.system('clear')
        else :
            os.system('cls' if os.name == 'nt' else 'clear')