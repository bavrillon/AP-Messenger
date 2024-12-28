from datetime import datetime
import time
import json
import argparse
#import psutil
import os

class User :
    def __init__(self,id:int,name:str):
        self.id = id
        self.name = name

    def __repr__(self):
        return(f'User(id={self.id},name={self.name})')
  
    def to_dico(self):
        user_dico = {"id": self.id, "name": self.name}
        return(user_dico)
    
    @staticmethod
    def from_dico(user_dico:dict):
        user_User = User(user_dico['id'],user_dico['name'])
        return(user_User)
    

class Channel :
    def __init__(self,id:int,name:str,members_ids:list):
        self.id = id
        self.name = name
        self.members_ids = members_ids
    
    def __repr__(self):
        return(f'Channel(id={self.id},name={self.name},members_ids={self.members_ids})')
  
    def to_dico(self):
        channel_dico = {"id": self.id, "name": self.name, "member_ids": self.members_ids}
        return(channel_dico)
    
    @staticmethod
    def from_dico(channel_dico:dict):
        channel_Channel = Channel(channel_dico['id'],channel_dico['name'],channel_dico['member_ids'])
        return(channel_Channel)

class Message :
    def __init__(self,id:int,reception_date:str,sender_id:str,channel:str,content:str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
        
    def __repr__(self):
        return(f'Message(id={self.id},reception_date={self.reception_date},sender_id={self.sender_id},channel={self.channel},content={self.content})')
    
    def to_dico(self):
        message_dico = {"id": self.id, "reception_date": self.reception_date, "sender_id": self.sender_id, "channel": self.channel, "content": self.content}
        return(message_dico)
    
    @staticmethod
    def from_dico(message_dico:dict):
        message_Message = Message(message_dico['id'],message_dico['reception_date'],message_dico['sender_id'],message_dico['channel'],message_dico['content'])
        return(message_Message)
    
class Server :
    def __init__(self,users:'list[User]',channels:'list[Channel]',messages:'list[Message]'):
        self.users = users
        self.channels = channels
        self.messages = messages
    
    def __repr__(self):
        return(f'Server(users={self.users},channels={self.channels},messages={self.messages})')

    def to_dico(self) ->dict:
        server_dico = {"users": [user_User.to_dico() for user_User in self.users],"channels": [channel_Channel.to_dico() for channel_Channel in self.channels],"messages": [message_Message.to_dico() for message_Message in self.messages]}
        return(server_dico)
    
    def save(self,file):
        server_dico = {"users": [user_User.to_dico() for user_User in self.users],"channels": [channel_Channel.to_dico() for channel_Channel in self.channels],"messages": [message_Message.to_dico() for message_Message in self.messages]}
        with open(file, "w") as f:
            json.dump(server_dico, f)
    
    def create_user(self,names):
        new_users_names_draft = names.split(',')
        new_users_names = [name.strip() for name in new_users_names_draft]
        for name_user in new_users_names :
            n = max([user.id for user in server.users])+1
            self.users.append(User(n,name_user))
        self.save(JASON_FILE_NAME)

    def ban_user(self,ID_banned_users):
        ID_banned_users_draft = ID_banned_users.split(',')
        ID_banned_users = [int(ID.strip()) for ID in ID_banned_users_draft]
        index_banned_users = []
        for index,user in enumerate(self.users) :
            if user.id in ID_banned_users :
                index_banned_users.append(index)
        index_banned_users.sort(reverse=True)
        for index in index_banned_users:
            self.users.pop(index)
        self.save(JASON_FILE_NAME)
    
    def create_channel(self):
        channel = input('\033[33mName of the new channel\033[0m: ')
        first_member_id = int(input('\033[33mID of the first user belonging to the new channel: \033[0m'))
        member_ids = [first_member_id]
        while True:
            choice = input('\033[33mAdd a member (yes/no) ? : \033[0m')
            if choice == 'no':
                break
            elif choice != 'yes':
                print('\033[33mUnknown option:\033[0m', choice)
                continue
            member_ids.append(int(input('\033[33mID of the next user belonging to the new channel: \033[0m')))
        n = max([channel.id for channel in server.channels])+1
        server.channels.append(Channel(n+1,channel,member_ids))
        print('\033[33mThe new channel have successfully been created !\033[0m')
        self.save(JASON_FILE_NAME)

    @staticmethod
    def load(file):
        with open(file, "r") as f:
            server_dico = json.load(f)
        server_Server = Server([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)
    
    @staticmethod
    def from_dico(server_dico:dict) :
        server_Server = Server([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)

class Client :          #Messenger app
    def __init__(self,server:'Server'):
        self.server = server
        
    def __repr__(self):
        return(f'Client(server={self.server})')
    
    def display_users(self):
#        self.clear_screen()
        print('\033[33m\nUser list\n-------')
        for user in self.server.users :
            print(user.id,' - ',user.name)
        print('\nn. Create user\nb. Ban user\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'n':
            new_names = input('\033[33mName of the new users (separators = ,) : \033[0m')
            self.server.create_user(new_names)
            self.main_menu()
        elif choice == 'x':
            self.main_menu()
        elif choice == 'b':
            banned_id = input('\033[33mID of the banned users (separators = ,) : \033[0m')
            self.server.ban_user(banned_id)
            self.main_menu()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            time.sleep(0.8)
            self.display_users()

    def display_messages(self):
#        self.clear_screen()
        channel = int(input('\033[33mName of the channel: \033[0m'))
        print('\033[31m\nMessages of the channel\n-------')
        for message in self.server.messages :
            if message.channel == channel :
        #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
                print(f"{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{message.content}")
        print('\033[33mx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'x':
            self.main_menu()
        else:
            print('Unknown option:\033[0m', choice)
            time.sleep(0.8)
            self.main_menu()

    def display_channels(self):
#        self.clear_screen()
        print('\033[33m\nChannels list\n-------')
        for channel in self.server.channels :
            print(f"{channel.id} - {channel.name} : {channel.members_ids}")
        print('\nn. Create channel\nx. Main menu')
        choice = input('Select an option: \033[0m')
        if choice == 'n':
            self.server.create_channel()
            self.main_menu()
        elif choice == 'x':
            self.main_menu()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            time.sleep(0.8)
            self.display_channels()
    
    def main_menu(self):
#        self.clear_screen()
        print('\033[33m=== Messenger ===')
        print('\n1. See users\n2. See channels\n3. See messages\nx. Leave')
        choice = input('Select an option: \033[0m')
        if choice == 'x':
            print('\033[33mBye!\033[0m')
        elif choice == '1':
            self.display_users()
        elif choice == '2':
            self.display_channels()
        elif choice == '3': 
            self.display_messages()
        else:
            print('\033[33mUnknown option:\033[0m', choice)
            time.sleep(0.8)
            self.main_menu()
    
#    def clear_screen(self):
#        if psutil.Process(os.getppid()).name() == 'bash.exe':
#            os.system('clear')
#        else :
#            os.system('cls' if os.name == 'nt' else 'clear')
    
parser = argparse.ArgumentParser()
parser.add_argument('-s','--server', help = 'Enter json server path')
args = parser.parse_args()
print(f'Server json : {args.server}')

JASON_FILE_NAME = args.server
server = Server.load(JASON_FILE_NAME)
client = Client(server)

client.main_menu()  