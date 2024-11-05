from datetime import datetime

server = {
    'users': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 1, 'name': 'Town square', 'member_ids': [1, 2]}
    ],
    'messages': [
        {
            'id': 1,
            'reception_date': datetime.now(),
            'sender_id': 1,
            'channel': 1,
            'content': 'Hi '
        }
    ]
}


def creation_liste_user():
    mb1 = input('ID of the first user belonging to the new channel: ')
    members = [mb1]
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

def create_user(name):
    n = max([user['id'] for user in server['users']])+1
    server['users'].append({'id':(n+1), 'name':name})

def create_channel():
    channel = input('Name of the new channel: ')
    members = creation_liste_user()
    n = max([channel['id'] for channel in server['channels']])+1
    server['channels'].append({'id':(n+1), 'name':channel, 'member_ids':members})
    print('The new channel have successfully been created !')
    main_menu()

def display_users():
    print('\nUser list\n-------')
    for elem in server['users'] :
        print(elem['id'],' - ',elem['name'])
    print('\nn. Create user\nx. Main menu')
    ch = input('Select an option: ')
    if ch == 'n':
        name = input('Name of the new user: ')
        create_user(name)
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
            print(elem['id'],' -\nReception date : ',elem['reception_date'],' -\nsender id : ',elem['sender_id'],'\n',elem['content'])
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
