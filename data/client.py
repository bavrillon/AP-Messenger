import os
import shutil
from psutil import Process
from time import sleep

from .server import Server

class Client :          #Messenger app
    def __init__(self,server: Server):   #En réalité, server est une instance de LocalServer ou RemoteServer, qui sont des classes héritant de la classe Server
        self.server = server    #Local server OR Remote server
        
    def __repr__(self):
        return(f'Client(server={self.server})')
    
    def display_users(self):
        self.clear_screen()
        print('\033[33m\nUser list\n-------')
        users_list = self.server.get_users()
        for user in users_list :
            print(user.id,' - ',user.name)
        print('\nn. Create user\nb. Ban user\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'n':
            new_names_draft = input('\033[33mName of the new users (separators = ,) : \033[0m')
            new_names_list = new_names_draft.split(',')
            self.server.create_user(new_names_list)
            sleep(0.8)
            self.display_users()
        elif choice == 'x':
            self.main_menu()
        elif choice == 'b':
            ID_banned_users_draft = input('\033[33mID of the banned users (separators = ,) : \033[0m')
            ID_banned_users_list = ID_banned_users_draft.split(',')
            for ID in ID_banned_users_list :
                if not(ID.strip().isdigit()) or not(int(ID.strip()) in [user.id for user in self.server.get_users()]):
                    print('\033[33mUnknown option:\033[0m', ID)
                    sleep(0.8)
                    self.display_users()
            ID_banned_users = [int(ID.strip()) for ID in ID_banned_users_list]
            self.server.ban_user(ID_banned_users)
            sleep(0.8)
            self.display_users()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            sleep(0.8)
            self.display_users()

    def display_messages(self):
        self.clear_screen()
        channel_ID = input('\033[33mID of the channel : \033[0m')
        channels_list = self.server.get_channels()
        if not(channel_ID.strip().isdigit()) or not(int(channel_ID.strip()) in [channel.id for channel in channels_list]):
                print('\033[33mUnknown option:\033[0m', channel_ID)
                sleep(0.8)
                self.display_messages()
        print('\033[31m\nMessages of the channel\n-------')
        messages_list = self.server.get_messages(int(channel_ID))
        for message in messages_list:
        #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
                print(f"{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{message.content}")
        print('\033[33ms. Send a message on the channel\no. See another channel\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 's':
            sender_id = input('\033[33mID of the sender : \033[0m')
            if not(sender_id.strip().isdigit()) or not(int(sender_id.strip()) in [user.id for user in self.server.get_users()]):
                print('\033[33mUnknown option:\033[0m', sender_id)
                sleep(0.8)
                self.display_messages()
            content = input('\033[33mContent of the message : \033[0m')
            self.server.send_message(int(sender_id),int(channel_ID),content)
            self.display_messages()
        elif choice == 'o':
            self.display_messages()
        elif choice == 'x':
            self.main_menu()
        else:
            print('Unknown option:\033[0m', choice)
            sleep(0.8)
            self.main_menu()

    def display_channels(self):
        self.clear_screen()
        print('\033[33m\nChannels list\n-------')
        channels_list = self.server.get_channels()
        for channel in channels_list :
            print(f"{channel.id} - {channel.name} : {channel.members_ids}")
        print('\nn. Create channel\nd. Delete channel\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'n':
            channel = input('\033[33mName of the new channel : \033[0m')
            first_member_id = input('\033[33mID of the first user belonging to the new channel: \033[0m')
            if not(first_member_id.isdigit()) or not(int(first_member_id) in [user.id for user in self.server.get_users()]):
                print('\033[33mUnknown option:\033[0m', first_member_id)
                sleep(0.8)
                self.display_channels()
            member_ids = [int(first_member_id)] 
            while True:
                choice = input('\033[33mAdd a member (yes/no) ? : \033[0m')
                if choice == 'no':
                    break
                elif choice != 'yes':
                    print('\033[33mUnknown option:\033[0m', choice)
                    sleep(0.8)
                    self.display_channels()
                other_member_id = input('\033[33mID of the next user belonging to the new channel: \033[0m')
                if not(other_member_id.isdigit()) or not(int(other_member_id) in [user.id for user in self.server.get_users()]):
                    sleep(0.8)
                    self.display_channels()
                member_ids.append(int(other_member_id))
            member_ids_set = set(member_ids) # Création d'un objet de type set pour supprimer les éventuelles répétitions
            member_ids = list(member_ids_set)
            self.server.create_channel(channel,member_ids)
            print('\033[33mThe new channel have successfully been created !\033[0m')
            sleep(0.8)
            self.display_channels()
        if choice == 'd':
            ID_channel = input('\033[33mID of the channel to delete : \033[0m')
            if not(ID_channel.isdigit()) or not(int(ID_channel) in [channel.id for channel in self.server.get_channels()]):
                print('\033[33mUnknown option:\033[0m', ID_channel)
                sleep(0.8)
                self.display_channels()          
            self.server.delete_channel(int(ID_channel))
            print('\033[33mThe channel have successfully been deleted !\033[0m')
            sleep(0.8)
            self.display_channels()
        elif choice == 'x':
            self.main_menu()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            sleep(0.8)
            self.display_channels()
    
    def main_menu(self):
        self.clear_screen()
        size = shutil.get_terminal_size(fallback=(80, 24))
        window_size = size.columns
        print('\033[33m'+'#' * window_size)
        print('# Messenger #')
        print('#' * window_size)
        print('\n1. See users\n2. See channels\n3. See messages\nx. Leave')
        choice = input('Select an option: \033[0m')
        if choice == 'x':
            print('\033[33mBye!\033[0m')
            exit()
        elif choice == '1':
            self.display_users()
        elif choice == '2':
            self.display_channels()
        elif choice == '3': 
            self.display_messages()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            sleep(0.8)
            self.main_menu()
    
    def clear_screen(self):
        if Process(os.getppid()).name() == 'bash.exe':
            os.system('clear')
        else :
            os.system('cls' if os.name == 'nt' else 'clear')