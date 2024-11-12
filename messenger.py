from datetime import datetime
import json

JASON_FILE_NAME = 'server.json'

def ouverture_json(file) :
    with open(file, "r") as f:
        server = json.load(f)
    return(server)


def sauvegarde_json(file,new_content) :
    with open(file, "w") as f:
        json.dump(new_content, f)


server = ouverture_json(JASON_FILE_NAME)

def creation_liste_user():
    first_member_id = int(input('ID of the first user belonging to the new channel: '))
    member_ids = [first_member_id]
    while True:
        choice = input('Add a member (yes/no) ? : ')
        if choice == 'no':
            break
        # Les 4 lignes ci-dessus peuvent être remplacées par :
        # while (choice := input('Add a member (yes/no) ? : ')) != 'no':
        elif choice != 'yes':
            print('Unknown option:', choice)
            continue
        member_ids.append(int(input('ID of the next user belonging to the new channel: ')))

    return member_ids

def create_user(names):
    new_users_names_draft = names.split(',')
    new_users_names = [name.strip() for name in new_users_names_draft]
    for name_user in new_users_names :
        n = max([user['id'] for user in server['users']])+1
        server['users'].append({'id':(n), 'name':name_user})
    sauvegarde_json(JASON_FILE_NAME,server)

def create_channel():
    channel = input('Name of the new channel: ')
    members = creation_liste_user()
    n = max([channel['id'] for channel in server['channels']])+1
    server['channels'].append({'id':(n+1), 'name':channel, 'member_ids':members})
    print('The new channel have successfully been created !')
    sauvegarde_json(JASON_FILE_NAME,server)
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
