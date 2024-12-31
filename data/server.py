import json
from .user import User
from .message import Message
from .channel import Channel

class Server :
    def __init__(self,file_path:'str',users:'list[User]',channels:'list[Channel]',messages:'list[Message]'):
        self.file_path = file_path
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
            n = max([user.id for user in self.users])+1
            self.users.append(User(n,name_user))
        self.save(self.file_path)

    def ban_user(self,ID_banned_users):
        ID_banned_users_draft = ID_banned_users.split(',')
        for ID in ID_banned_users_draft :
            if not(ID.strip().isdigit()) or not(int(ID.strip()) in [user.id for user in self.users]):
                print('\033[33mUnknown option:\033[0m', ID)
                return
        ID_banned_users = [int(ID.strip()) for ID in ID_banned_users_draft]
        index_banned_users = []
        for index,user in enumerate(self.users) :
            if user.id in ID_banned_users :
                index_banned_users.append(index)
        index_banned_users.sort(reverse=True)
        for index in index_banned_users:
            self.users.pop(index)
        self.save(self.file_path)
    
    def create_channel(self):
        channel = input('\033[33mName of the new channel : \033[0m')
        first_member_id = input('\033[33mID of the first user belonging to the new channel: \033[0m')
        if not(first_member_id.isdigit()) or not(int(first_member_id) in [user.id for user in self.users]):
            print('\033[33mUnknown option:\033[0m', first_member_id)
            return
        member_ids = [int(first_member_id)]
        while True:
            choice = input('\033[33mAdd a member (yes/no) ? : \033[0m')
            if choice == 'no':
                break
            elif choice != 'yes':
                print('\033[33mUnknown option:\033[0m', choice)
                continue
            other_member_id = input('\033[33mID of the next user belonging to the new channel: \033[0m')
            if not(other_member_id.isdigit()) or not(int(other_member_id) in [user.id for user in self.users]):
                print('\033[33mUnknown option:\033[0m', other_member_id)
                return
            member_ids.append(int(other_member_id))
        n = max([channel.id for channel in self.channels])+1
        self.channels.append(Channel(n+1,channel,member_ids))
        print('\033[33mThe new channel have successfully been created !\033[0m')
        self.save(self.file_path)

    def delete_channel(self):
        ID_channel = input('\033[33mID of the channel to delete : \033[0m')
        if not(ID_channel.isdigit()) or not(int(ID_channel) in [channel.id for channel in self.channels]):
            print('\033[33mUnknown option:\033[0m', ID_channel)
            return
        for channel in self.channels :
            if channel.id == ID_channel :
                self.channels.remove(channel)
        print('\033[33mThe channel have successfully been deleted !\033[0m')
        self.save(self.file_path)

    @staticmethod
    def load(file):
        with open(file, "r") as f:
            server_dico = json.load(f)
        server_Server = Server(file,[User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)
    
    @staticmethod
    def from_dico(server_dico:dict) :
        server_Server = Server([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)