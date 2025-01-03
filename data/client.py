from psutil import Process
import os
from time import sleep

class Client :          #Messenger app
    def __init__(self,server):
        self.server = server
        
    def __repr__(self):
        return(f'Client(server={self.server})')
    
    def display_users(self):
        self.clear_screen()
        print('\033[33m\nUser list\n-------')
        for user in self.server.users :
            print(user.id,' - ',user.name)
        print('\nn. Create user\nb. Ban user\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'n':
            new_names = input('\033[33mName of the new users (separators = ,) : \033[0m')
            self.server.create_user(new_names)
            self.display_users()
        elif choice == 'x':
            self.main_menu()
        elif choice == 'b':
            banned_id = input('\033[33mID of the banned users (separators = ,) : \033[0m')
            self.server.ban_user(banned_id)
            sleep(0.8)
            self.display_users()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            sleep(0.8)
            self.display_users()

    def display_messages(self):
        self.clear_screen()
        channel_ID = input('\033[33mID of the channel: \033[0m')
        if not(channel_ID.strip().isdigit()) or not(int(channel_ID.strip()) in [channel.id for channel in self.server.channels]):
                print('\033[33mUnknown option:\033[0m', channel_ID)
                sleep(0.8)
                self.display_messages()
        print('\033[31m\nMessages of the channel\n-------')
        for message in self.server.messages :
            if message.channel == int(channel_ID) :
        #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
                print(f"{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{message.content}")
        print('\033[33mo. See another channel\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'o':
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
        for channel in self.server.channels :
            print(f"{channel.id} - {channel.name} : {channel.members_ids}")
        print('\nn. Create channel\nd. Delete channel\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'n':
            self.server.create_channel()
            sleep(0.8)
            self.display_channels()
        if choice == 'd':
            self.server.delete_channel()
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
        print('\033[33m=== Messenger ===')
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