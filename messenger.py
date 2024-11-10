from datetime import datetime
import json

with open("server.json", "r") as f:
    server = json.load(f)

def sauvegarde_json() :
    with open("server.json", "w") as f:
        json.dump(server, f)

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
    for elem in new_users_names :
        n = max([user['id'] for user in server['users']])+1
        server['users'].append({'id':(n), 'name':elem})
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
    for elem in server['users'] :
        print(elem['id'],' - ',elem['name'])
    print('\nn. Create user\nx. Main menu')
    ch = input('Select an option: ')
    if ch == 'n':
        names = input('Name of the new users (separators = ,) : ')
        create_user(names)
        main_menu()
    elif ch == 'x':
        main_menu()
    else:
        print('Unknown option:', ch)

def display_messages():
    channel = int(input('Name of the channel: '))
    print('\nMessages of the channel\n-------')
    for elem in server['messages'] :
        if elem['channel'] == channel :
    #       print(elem['id'],' -\nReception date : ',elem['reception_date'],' -\nsender id : ',elem['sender_id'],'\n',elem['content'])
            print(f"{elem['id']} -\nReception date : {elem['reception_date']}\nsender id : {elem['sender_id']}\n{elem['content']}")
    print('x. Main menu')
    ch = input('Select an option: ')
    if ch == 'x':
        main_menu()
    else:
        print('Unknown option:', ch)

def display_channels():
    print('\nChannels list\n-------')
    for elem in server['channels'] :
        print(f"{elem['id']} - {elem['name']} : {elem['member_ids']}")
    print('\nn. Create channel\nx. Main menu')
    ch = input('Select an option: ')
    if ch == 'n':
        create_channel()
    elif ch == 'x':
        main_menu()
    else:
        print('Unknown option:', ch)

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
