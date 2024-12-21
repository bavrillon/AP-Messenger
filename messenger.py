from datetime import datetime
import json
import argparse
import sys
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
    
    @classmethod
    def from_dico(cls,user_dico:dict):
        user_User = cls(user_dico['id'],user_dico['name'])
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
    
    @classmethod
    def from_dico(cls,channel_dico:dict):
        channel_Channel = cls(channel_dico['id'],channel_dico['name'],channel_dico['member_ids'])
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
    
    @classmethod
    def from_dico(cls,message_dico:dict):
        message_Message = cls(message_dico['id'],message_dico['reception_date'],message_dico['sender_id'],message_dico['channel'],message_dico['content'])
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
        channel = input('Name of the new channel: ')
        first_member_id = int(input('ID of the first user belonging to the new channel: '))
        member_ids = [first_member_id]
        while True:
            choice = input('Add a member (yes/no) ? : ')
            if choice == 'no':
                break
            elif choice != 'yes':
                print('Unknown option:', choice)
                continue
            member_ids.append(int(input('ID of the next user belonging to the new channel: ')))
        n = max([channel.id for channel in server.channels])+1
        server.channels.append(Channel(n+1,channel,member_ids))
        print('The new channel have successfully been created !')
        self.save(JASON_FILE_NAME)

    @classmethod
    def load(cls, file):
        with open(file, "r") as f:
            server_dico = json.load(f)
        server_Server = cls([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)
    
    @classmethod
    def from_dico(cls,server_dico:dict) :
        server_Server = cls([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)

class Client :          #Messenger app
    def __init__(self,server:'Server'):
        self.server = server
        
    def __repr__(self):
        return(f'Client(server={self.server})')
    
    def display_users(self):
        self.clear_screen()
        print('\nUser list\n-------')
        for user in self.server.users :
            print(user.id,' - ',user.name)
        print('\nn. Create user\nb. Ban user\nx. Main menu')
        choice = input('Select an option: ')
        if choice == 'n':
            new_names = input('Name of the new users (separators = ,) : ')
            self.server.create_user(new_names)
            self.main_menu()
        elif choice == 'x':
            self.main_menu()
        elif choice == 'b':
            banned_id = input('ID of the banned users (separators = ,) : ')
            self.server.ban_user(banned_id)
            self.main_menu()
        else:
            print('Unknown option:', choice)

    def display_messages(self):
        self.clear_screen()
        channel = int(input('Name of the channel: '))
        print('\nMessages of the channel\n-------')
        for message in self.server.messages :
            if message.channel == channel :
        #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
                print(f"{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{message.content}")
        print('x. Main menu')
        choice = input('Select an option: ')
        if choice == 'x':
            self.main_menu()
        else:
            print('Unknown option:', choice)

    def display_channels(self):
        self.clear_screen()
        print('\nChannels list\n-------')
        for channel in self.server.channels :
            print(f"{channel.id} - {channel.name} : {channel.members_ids}")
        print('\nn. Create channel\nx. Main menu')
        choice = input('Select an option: ')
        if choice == 'n':
            self.server.create_channel()
            self.main_menu()
        elif choice == 'x':
            self.main_menu()
        else:
            print('Unknown option:', choice)
    
    def main_menu(self):
        self.clear_screen()
        print('=== Messenger ===')
        print('\n1. See users\n2. See channels\n3. See messages\nx. Leave')
        choice = input('Select an option: ')
        if choice == 'x':
            print('Bye!')
        elif choice == '1':
            self.display_users()
        elif choice == '2':
            self.display_channels()
        elif choice == '3':
            self.display_messages()
        else:
            print('Unknown option:', choice)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear') # la commande pour effacer est `cls` sous Windows et `clear` sur presque tout le reste
    
parser = argparse.ArgumentParser()
parser.add_argument('-s','--server', help = 'Enter json server path')
args = parser.parse_args()
print(f'Server json : {args.server}')

JASON_FILE_NAME = args.server
server = Server.load(JASON_FILE_NAME)
client = Client(server)

client.main_menu()  