import json
import requests
import time
from datetime import datetime

from .user import User
from .message import Message
from .channel import Channel

class Server:

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def get_users(self) -> list[User]:
        pass
    
    def create_user(self, names: list[str]) -> User:
        pass

    def ban_user(self, ID_banned_users: list[int]) -> None:
        pass
    
    def get_channels(self) -> list[Channel]:
        pass
    
    def create_channel(self, name:str, member_ids: list[int]) -> Channel:
        pass

    def delete_channel(self, channel_id: int) -> None:
        pass

    def get_messages(self, channel: int) -> list[Message]:
        pass

    def send_message(self, sender: int, channel: int, content: str) -> None:
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

    def to_dico(self)->dict:
        server_dico = {"users": [user_User.to_dico() for user_User in self._users],"channels": [channel_Channel.to_dico() for channel_Channel in self._channels],"messages": [message_Message.to_dico() for message_Message in self._messages]}
        return(server_dico)
    
    def save(self,file) -> None:
        server_dico = {"users": [user_User.to_dico() for user_User in self._users],"channels": [channel_Channel.to_dico() for channel_Channel in self._channels],"messages": [message_Message.to_dico() for message_Message in self._messages]}
        with open(file, "w", encoding = 'utf8') as f:
            json.dump(server_dico, f)

    def get_users(self) -> list[User]:
        super().get_users()
        return(self._users)
    
    def create_user(self, names: list[str]) -> None:
        super().create_user(names)
        new_users_names = [name.strip() for name in names]
        for name_user in new_users_names :
            n = max([user.id for user in self._users])+1
            self._users.append(User(n,name_user))
        self.save(self._file_path)

    def ban_user(self, ID_banned_users: list[int]) -> None:
        super().ban_user(ID_banned_users)
        index_banned_users = []
        for index,user in enumerate(self._users) :
            if user.id in ID_banned_users :
                index_banned_users.append(index)
        index_banned_users.sort(reverse=True)
        for index in index_banned_users:                # On supprime l'utilisateur banni de toutes les channels
            for channel in self._channels :
                for ID in channel.members_ids :
                    if ID == self._users[index].id :
                        channel.members_ids.remove(ID)
            self._users.pop(index)
        self.save(self._file_path)
    
    def get_channels(self) -> list[Channel]:
        super().get_channels()
        return(self._channels)

    def create_channel(self, name: str, member_ids: list[int]) -> None:
        super().create_channel(name, member_ids)
        n = max([channel.id for channel in self._channels])+1
        self._channels.append(Channel(n+1,name,member_ids))
        self.save(self._file_path)

    def delete_channel(self, channel_id: int) -> None:
        super().delete_channel(channel_id)
        for channel in self._channels :
            if channel.id == channel_id :
                self._channels.remove(channel)
        self.save(self._file_path)

    def get_messages(self, ID_channel: int) -> Message:
        super().get_messages(ID_channel)
        messages = []
        for message in self._messages :
            if message.channel == ID_channel :
                messages.append(message)
        return(messages)
    
    def send_message(self, sender_id: int, channel: int, content: str) -> None:
        super().send_message(sender_id, channel, content)
        id = max([message.id for message in self._messages])+1
        reception_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = Message(id,reception_date,sender_id,channel,content)
        self._messages.append(message)
        self.save(self._file_path)

    @classmethod
    def load(cls, file) -> Server:
        with open(file, "r", encoding = 'utf8') as f:
            server_dico = json.load(f)
        server_Server = cls(file,[User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)
    
    @classmethod
    def from_dico(cls, server_dico: dict) -> Server:
        server_Server = LocalServer([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)

class RemoteServer(Server) :
    def __init__(self,url:'str'):
        super().__init__()
        self._url = url
    
    def __repr__(self):
        super().__repr__()
        return(f'Remote server(url={self._url})')
    
    def get_users(self) -> list[User]:
        super().get_users()
        reponse = requests.get(self._url + '/users')
        if reponse.status_code != 200 :
            return(False)
        list_users = reponse.json()       #Retourne la liste des dictionnaires que sont les users
        users = []                        #Liste d'instances de la classe User
        for user_dico in list_users :
            user = User.from_dico(user_dico)
            users.append(user)
        return(users)
    
    def create_user(self, names: list[str]) -> None:
        super().create_user(names)
        url_creation_user = self._url + '/users/create'
        for user_name in names :
            post = requests.post(url_creation_user, json={'name' : user_name}).status_code
            if post != 200 :
                return(False)

    def ban_user(self, ID_banned_users: list[int]) -> None:
        return(False) 

    def get_channels(self) -> list[Channel]:
        super().get_channels()
        reponse = requests.get(self._url + '/channels')
        if reponse.status_code != 200 :
            return(False)
        list_channels = reponse.json()       #Retourne la liste des dictionnaires que sont les channels
        channels = []                        #Liste d'instances de la classe Channel
        for channel_dico_draft in list_channels :
            channel_dico = channel_dico_draft
            members_ids = []
            reponse = requests.get(self._url + '/channels/'+ str(channel_dico_draft['id']) + '/members').json() # Retourne la liste des dictionnaires que sont les membres
            for member in reponse :
                members_ids.append(member['id'])            
            channel_dico['member_ids'] = members_ids
            channel = Channel.from_dico(channel_dico)
            channels.append(channel)
        return(channels)
    
    def create_channel(self, channel_name: str, member_ids: list[int]) -> None:
        super().create_channel(channel_name, member_ids)
        url_creation_channel = self._url + '/channels/create'
        response = requests.post(url_creation_channel, json={'name': channel_name}).json() # Retourne un dictionnaire
        id_channel = response['id']
        url_join_channel = self._url + '/channels/' + str(id_channel) + '/join'
        for user_id in member_ids :
            post = requests.post(url_join_channel, json={'user_id': user_id}).status_code
            if post != 200 :
                return(False)

    def delete_channel(self, channel_id: int) -> None:
        super().delete_channel(channel_id)
        return(False)

    def get_messages(self, ID_channel: int) -> list[Message]: 
        super().get_messages(ID_channel)
        reponse = requests.get(self._url + '/channels/' + str(ID_channel) + '/messages')
        if reponse.status_code == 404 :
            return(False)
        list_messages = reponse.json()       #Retourne la liste des dictionnaires que sont les messages
        messages = []                        #Liste d'instances de la classe Message
        for message_dico in list_messages :
            message_dico['channel'] = message_dico['channel_id']
            del message_dico['channel_id']
            message = Message.from_dico(message_dico)
            messages.append(message)
        return(messages)
    
    def send_message(self, sender_id: int, channel: int, content: str) -> None:
        super().send_message(sender_id, channel, content)
        url_send_message = self._url + '/channels/' + str(channel) + '/messages/post'
        post = requests.post(url_send_message, json={'sender_id': sender_id, 'content':content}).status_code
        if post != 200 :
            return(False)
