from datetime import datetime
import json

JASON_FILE_NAME = 'server.json'

with open(JASON_FILE_NAME, "r") as f:
    server = json.load(f)

def sauvegarde_json() :
    with open(JASON_FILE_NAME, "w") as f:
        json.dump(server, f)

def creation_liste_user():
    member_1 = input('ID of the first user belonging to the new channel: ')
    members = [member_1]
    choice = input('Add a member (yes/no) ? : ')
    if (choice != 'yes' and choice != 'no'):
            print('Unknown option:', choice)
            choice = input('Add a member (yes/no) ? : ')
    while choice != 'no':
        members.append(input('ID of the next user belonging to the new channel: '))
        choice = input('Add a member (yes/no) ? : ')
        if (choice != 'yes' and choice != 'no'):
            print('Unknown option:', choice)
            choice = input('Add a member (yes/no) ? : ')
    return(members)

def create_user(names):
    new_users_names_draft = names.split(',')
    new_users_names = [name.strip() for name in new_users_names_draft]
    for name_user in new_users_names :
        n = max([user['id'] for user in server['users']])+1
        server['users'].append({'id':(n), 'name':name_user})
    sauvegarde_json()

def create_channel():
    channel = input('Name of the new channel: ')
    members = creation_liste_user()
    n = max([channel['id'] for channel in server['channels']])+1
    server['channels'].append({'id':(n+1), 'name':channel, 'member_ids':members})
    print('The new channel have successfully been created !')
    sauvegarde_json()
    main_menu()

def display_users():
    print('\nUser list\n-------')
    for user in server['users'] :
        print(user['id'],' - ',user['name'])
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
    for message in server['messages'] :
        if message['channel'] == channel :
    #       print(message['id'],' -\nReception date : ',message['reception_date'],' -\nsender id : ',message['sender_id'],'\n',message['content'])
            print(f"{message['id']} -\nReception date : {message['reception_date']}\nsender id : {message['sender_id']}\n{message['content']}")
    print('x. Main menu')
    choice = input('Select an option: ')
    if choice == 'x':
        main_menu()
    else:
        print('Unknown option:', choice)

def display_channels():
    print('\nChannels list\n-------')
    for channel in server['channels'] :
        print(f"{channel['id']} - {channel['name']} : {channel['member_ids']}")
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
