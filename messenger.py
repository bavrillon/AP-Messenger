from datetime import datetime
import json

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

JASON_FILE_NAME = 'server.json'

server = Server.load(JASON_FILE_NAME)

def creation_liste_user():
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
    return member_ids

def create_user(names):
    new_users_names_draft = names.split(',')
    new_users_names = [name.strip() for name in new_users_names_draft]
    for name_user in new_users_names :
        n = max([user.id for user in server.users])+1
        server.users.append(User(n,name_user))
    server.save(JASON_FILE_NAME)

def create_channel():
    channel = input('Name of the new channel: ')
    members = creation_liste_user()
    n = max([channel.id for channel in server.channels])+1
    server.channels.append(Channel(n+1,channel,members))
    print('The new channel have successfully been created !')
    server.save(JASON_FILE_NAME)
    main_menu()

def display_users():
    print('\nUser list\n-------')
    for user in server.users :
        print(user.id,' - ',user.name)
    print('\nn. Create user\nx. Main menu')
    choice = input('Select an option: ')
    if choice == 'n':
        names = input('Name of the new users (separators = ,) : ')
        create_user(names)
        main_menu()
    elif choice == 'x':
        main_menu()
    else:
        print('Unknown option:', choice)

def display_messages():
    channel = int(input('Name of the channel: '))
    print('\nMessages of the channel\n-------')
    for message in server.messages :
        if message.channel == channel :
    #       print(message.id',' -\nReception date : ',message.reception_date,' -\nsender id : ',message.sender_id,'\n',message.content)
            print(f"{message.id} -\nReception date : {message.reception_date}\nsender id : {message.sender_id}\n{message.content}")
    print('x. Main menu')
    choice = input('Select an option: ')
    if choice == 'x':
        main_menu()
    else:
        print('Unknown option:', choice)

def display_channels():
    print('\nChannels list\n-------')
    for channel in server.channels :
        print(f"{channel.id} - {channel.name} : {channel.members_ids}")
    print('\nn. Create channel\nx. Main menu')
    choice = input('Select an option: ')
    if choice == 'n':
        create_channel()
    elif choice == 'x':
        main_menu()
    else:
        print('Unknown option:', choice)

def main_menu():
    print('\n1. See users\n2. See channels\n3. See messages\nx. Leave')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
    elif choice == '1':
        display_users()
    elif choice == '2':
        display_channels()
    elif choice == '3':
        display_messages()
    else:
        print('Unknown option:', choice)





print('=== Messenger ===')
main_menu()



