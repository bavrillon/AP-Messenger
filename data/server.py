from json import dump,load
import requests
from .user import User
from .message import Message
from .channel import Channel

class Server:

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def get_users(self):
        pass
    
    def create_user(self, names: list[str]):
        pass

    def ban_user(self, ID_banned_users: list[int]):
        pass
    
    def get_channels(self):
        pass
    
    def create_channel(self):
        pass

    def delete_channel(self):
        pass

    def get_messages(self,channel: int):
        pass



class LocalServer(Server) :
    def __init__(self,file_path:'str',users:'list[User]',channels:'list[Channel]',messages:'list[Message]'):
        super().__init__()
        self._file_path = file_path
        self._users = users
        self._channels = channels
        self._messages = messages
    
    def __repr__(self):
        super().__repr__()
        return(f'Local server(users={self._users},channels={self._channels},messages={self._messages})')

    def to_dico(self) ->dict:
        server_dico = {"users": [user_User.to_dico() for user_User in self._users],"channels": [channel_Channel.to_dico() for channel_Channel in self._channels],"messages": [message_Message.to_dico() for message_Message in self._messages]}
        return(server_dico)
    
    def save(self,file):
        server_dico = {"users": [user_User.to_dico() for user_User in self._users],"channels": [channel_Channel.to_dico() for channel_Channel in self._channels],"messages": [message_Message.to_dico() for message_Message in self._messages]}
        with open(file, "w") as f:
            dump(server_dico, f)

    def get_user(self):
        super().get_users()
        return(self._users)
    
    def create_user(self, names: list[str]):
        super().create_user()
        new_users_names_draft = names.split(',')
        new_users_names = [name.strip() for name in new_users_names_draft]
        for name_user in new_users_names :
            n = max([user.id for user in self._users])+1
            self._users.append(User(n,name_user))
        self.save(self._file_path)

    def ban_user(self, ID_banned_users: list[int]):
        super().ban_user()
        ID_banned_users_draft = ID_banned_users.split(',')
        for ID in ID_banned_users_draft :
            if not(ID.strip().isdigit()) or not(int(ID.strip()) in [user.id for user in self._users]):
                print('\033[33mUnknown option:\033[0m', ID)
                return
        ID_banned_users = [int(ID.strip()) for ID in ID_banned_users_draft]
        index_banned_users = []
        for index,user in enumerate(self._users) :
            if user.id in ID_banned_users :
                index_banned_users.append(index)
        index_banned_users.sort(reverse=True)
        for index in index_banned_users:
            self._users.pop(index)
        self.save(self._file_path)
    
    def get_channels(self):
        super().get_channels()
        return(self._channels)

    def create_channel(self):
        super().create_channel()
        channel = input('\033[33mName of the new channel : \033[0m')
        first_member_id = input('\033[33mID of the first user belonging to the new channel: \033[0m')
        if not(first_member_id.isdigit()) or not(int(first_member_id) in [user.id for user in self._users]):
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
            if not(other_member_id.isdigit()) or not(int(other_member_id) in [user.id for user in self._users]):
                print('\033[33mUnknown option:\033[0m', other_member_id)
                return
            member_ids.append(int(other_member_id))
        n = max([channel.id for channel in self._channels])+1
        self._channels.append(Channel(n+1,channel,member_ids))
        print('\033[33mThe new channel have successfully been created !\033[0m')
        self.save(self._file_path)

    def delete_channel(self):
        super().delete_channel()
        ID_channel = input('\033[33mID of the channel to delete : \033[0m')
        if not(ID_channel.isdigit()) or not(int(ID_channel) in [channel.id for channel in self._channels]):
            print('\033[33mUnknown option:\033[0m', ID_channel)
            return
        for channel in self._channels :
            if channel.id == int(ID_channel) :
                self._channels.remove(channel)
        print('\033[33mThe channel have successfully been deleted !\033[0m')
        self.save(self._file_path)

    def get_messages(self, ID_channel: int):
        super().get_messages()
        messages = []
        for message in self._messages :
            if message.channel == ID_channel :
                messages.append(message)
        return(messages)

    @classmethod
    def load(cls, file) :
        with open(file, "r") as f:
            server_dico = load(f)
        server_Server = cls(file,[User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)
    
    @classmethod
    def from_dico(cls, server_dico: dict) :
        server_Server = LocalServer([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)

class RemoteServer :
    def __init__(self,url:'str'):
        super().__init__()
        self._url = url
    
    def __repr__(self):
        super().__repr__()
        return(f'Remote server(url={self._url})')
    
    def get_users(self):
        super().get_users()
        reponse = requests.get(self.url + '/users')
        list_users = reponse.json()       #Retourne la liste des dictionnaires que sont les users
        users = []                        #Liste d'instances de la classe User
        for user_dico in list_users :
            user = User.from_dico(user_dico)
            users.append(user)
        return(users)
    
    def get_channels(self):
        super().get_channels()
        reponse = requests.get(self.url + '/channels')
        list_channels = reponse.json()       #Retourne la liste des dictionnaires que sont les channels
        channels = []                        #Liste d'instances de la classe Channel
        for channel_dico in list_channels :
            channel = Channel.from_dico(channel_dico)
            channels.append(channel)
        return(channels)
    
    def get_messages(self, ID_channel: int): 
        super().get_messages()
        reponse = requests.get(self.url + '/channels/' + str(ID_channel) + '/messages')
        list_messages = reponse.json()       #Retourne la liste des dictionnaires que sont les messages
        messages = []                        #Liste d'instances de la classe Message
        for message_dico in list_messages :
            message = Message.from_dico(message_dico)
            messages.append(message)
        return(messages)
