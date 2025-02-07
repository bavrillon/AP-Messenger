import json
import requests
import time
from datetime import datetime

from .user import User
from .message import Message
from .channel import Channel

class Server:
    # Pas besoin de déclarer __init__ et __repr__. Vous n'avez besoin
    # de déclarer que les fonctions qui sont appelées explicitement
    # sur des Server

    def get_users(self) -> list[User] | None:
        # Nous n'avons pas vu les exceptions en cours,
        # mais elles permettent de remonter des erreurs d'exécutions.
        # Ici ce code n'est pas censé être atteint, car la fonction
        # sera toujours appelée sur une sous-classe qui la redéfinira.
        # Si on oublie de la redéfinir, l'erreur sera assez explicite
        # (Not implemented)
        raise NotImplementedError()

    # Attention, votre type de retour doit être cohérent avec
    # les autres implémentations (dans LocalServer et RemoteServer)
    # et avec l'usage que vous en faites (dans Client)
    def create_user(self, names: list[str]) -> bool:
        raise NotImplementedError()

    def ban_user(self, ID_banned_users: list[int]) -> None:
        raise NotImplementedError()
    
    def get_channels(self) -> list[Channel] | None:
        raise NotImplementedError()
    
    def create_channel(self, name:str, member_ids: list[int]) -> bool:
        raise NotImplementedError()

    def delete_channel(self, channel_id: int) -> None:
        raise NotImplementedError()

    def get_messages(self, channel: int) -> list[Message] | None:
        raise NotImplementedError()

    def send_message(self, sender: int, channel: int, content: str) -> bool:
        raise NotImplementedError()



class LocalServer(Server) :
    def __init__(self,file_path:'str',users:'list[User]',channels:'list[Channel]',messages:'list[Message]'):
        # Puisque Server.__init__ ne fait rien, pas la peine de l'appeler
        self._file_path = file_path
        self._users = users
        self._channels = channels
        self._messages = messages
    
    def __repr__(self):
        return(f'Local server(users={self._users},channels={self._channels},messages={self._messages})')

    def to_dico(self) -> dict[str, list]: # On peut préciser les types des clefs et valeurs
        # L'indentation améliore la lisibilité
        server_dico = {
            "users": [user_User.to_dico() for user_User in self._users],
            "channels": [channel_Channel.to_dico() for channel_Channel in self._channels],
            "messages": [message_Message.to_dico() for message_Message in self._messages]
        }
        return(server_dico)

    # La fonction save n'ayant pas vocation à être utilisée
    # hors de la classe, vous pouvez la préfixer par "_"
    def _save(self,file) -> None:
        # Il vaut mieux éviter la duplication de code :
        # vous pouvez utiliser la fonction déjà définie
        server_dico = self.to_dico()
        with open(file, "w", encoding = 'utf8') as f:
            json.dump(server_dico, f)

    def get_users(self) -> list[User] | None:
        return(self._users)
    
    def create_user(self, names: list[str]) -> bool:
        new_users_names = [name.strip() for name in names]
        for name_user in new_users_names :
            n = max([user.id for user in self._users])+1
            self._users.append(User(n,name_user))
        self._save(self._file_path)

        return True

    def ban_user(self, ID_banned_users: list[int]) -> None:
        index_banned_users = []
        for index,user in enumerate(self._users) :
            if user.id in ID_banned_users :
                index_banned_users.append(index)
        index_banned_users.sort(reverse=True)
        # Le nom "index" est trop générique pour
        # cet enchaînement de boucles et conditions
        for index_to_ban in index_banned_users:                # On supprime l'utilisateur banni de toutes les channels
            for channel in self._channels :
                # Par convention, on réserve les noms en majuscules
                # aux constantes
                for member_id in channel.members_ids :
                    if member_id == self._users[index_to_ban].id :
                        # Il vaut mieux éviter de modifier la liste sur
                        # laquelle on itère avec remove ou append.
                        # Ici, lorsque vous faites un remove,
                        # vous raccourcissez la liste, et la boucle
                        # for va sauter un élément. Vous pouvez le tester
                        # avec le code suivant :
                        # >>> l = ['a', 'b', 'c', 'd']
                        # >>> for x in l:
                        # ...     print(x)
                        # ...     if x == 'b':
                        # ...         l.remove(x)
                        # ...
                        # a
                        # b
                        # d
                        channel.members_ids.remove(member_id)
            self._users.pop(index_to_ban)
        self._save(self._file_path)

    # Vous pouvez faire une version plus simple de ban_user :
    def ban_user_2(self, ids_to_ban: list[int]) -> None:
        for id_to_ban in ids_to_ban:
            for channel in self._channels:
                channel.members_ids = [member_id for member_id in channel.members_ids if member_id != id_to_ban]
            self._users = [user for user in self._users if user.id != id_to_ban]
        self._save(self._file_path)

    def get_channels(self) -> list[Channel] | None:
        return(self._channels)

    def create_channel(self, name: str, member_ids: list[int]) -> bool:
        n = max([channel.id for channel in self._channels])+1
        self._channels.append(Channel(n,name,member_ids)) # Vous avez déjà fait +1 à la ligne précédente
        self._save(self._file_path)

        return True

    def delete_channel(self, channel_id: int) -> None:
        for channel in self._channels :
            if channel.id == channel_id :
                self._channels.remove(channel)
        self._save(self._file_path)

    def get_messages(self, ID_channel: int) -> list[Message] | None:
        messages = []
        for message in self._messages :
            if message.channel == ID_channel :
                messages.append(message)
        return(messages)
    
    def send_message(self, sender_id: int, channel: int, content: str) -> bool:
        id = max([message.id for message in self._messages])+1
        reception_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = Message(id,reception_date,sender_id,channel,content)
        self._messages.append(message)
        self._save(self._file_path)

        return True

    @classmethod
    def load(cls, file: str) -> Server:
        with open(file, "r", encoding = 'utf8') as f:
            server_dico = json.load(f)
        server_Server = cls(file,[User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)
    
    @classmethod
    def from_dico(cls, server_dico: dict) -> Server:
        # Cette fonction ne fonctionnera pas : LocalServer.__init__ attend
        # un premier paramètre "file"
        server_Server = LocalServer([User.from_dico(user_dico) for user_dico in server_dico['users']],[Channel.from_dico(channel_dico) for channel_dico in server_dico['channels']],[Message.from_dico(message_dico) for message_dico in server_dico['messages']])
        return(server_Server)

class RemoteServer(Server) :
    def __init__(self,url:'str'):
        self._url = url
    
    def __repr__(self):
        return(f'Remote server(url={self._url})')
    
    # Si vous renvoyez autre chose qu'une liste,
    # il faut le mettre dans le type de retour
    def get_users(self) -> list[User] | None:
        reponse = requests.get(self._url + '/users')
        if reponse.status_code != 200 :
            return None

        list_users = reponse.json()       #Retourne la liste des dictionnaires que sont les users
        users = []                        #Liste d'instances de la classe User
        for user_dico in list_users :
            user = User.from_dico(user_dico)
            users.append(user)
        return(users)
    
    def create_user(self, names: list[str]) -> bool:
        url_creation_user = self._url + '/users/create'
        for user_name in names :
            post = requests.post(url_creation_user, json={'name' : user_name}).status_code
            if post != 200 :
                return(False)

        return True

    def ban_user(self, ID_banned_users: list[int]) -> None:
        return

    def get_channels(self) -> list[Channel] | None:
        reponse = requests.get(self._url + '/channels')
        if reponse.status_code != 200 :
            return None
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
    
    def create_channel(self, channel_name: str, member_ids: list[int]) -> bool:
        url_creation_channel = self._url + '/channels/create'
        response = requests.post(url_creation_channel, json={'name': channel_name}).json() # Retourne un dictionnaire
        id_channel = response['id']
        url_join_channel = self._url + '/channels/' + str(id_channel) + '/join'
        for user_id in member_ids :
            post = requests.post(url_join_channel, json={'user_id': user_id}).status_code
            if post != 200 :
                return(False)

        return True

    def delete_channel(self, channel_id: int) -> None:
        return

    def get_messages(self, ID_channel: int) -> list[Message] | None:
        reponse = requests.get(self._url + '/channels/' + str(ID_channel) + '/messages')
        # Il y a d'autres codes d'erreur que 404, il vaut
        # donc mieux vérifier s'il vaut 200
        if reponse.status_code != 200:
            return None
        list_messages = reponse.json()       #Retourne la liste des dictionnaires que sont les messages
        messages = []                        #Liste d'instances de la classe Message
        for message_dico in list_messages :
            message_dico['channel'] = message_dico['channel_id']
            del message_dico['channel_id']
            message = Message.from_dico(message_dico)
            messages.append(message)
        return(messages)
    
    def send_message(self, sender_id: int, channel: int, content: str) -> bool:
        url_send_message = self._url + '/channels/' + str(channel) + '/messages/post'
        post = requests.post(url_send_message, json={'sender_id': sender_id, 'content':content}).status_code
        if post != 200 :
            return(False)

        return True
