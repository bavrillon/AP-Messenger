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
            'content': 'Hi 👋'
        }
    ]
}



def create_user(name):
    n = len(server['users'])
    server['users'].append({'id':(n+1), 'name':name})

def create_channel(channel,members):
    n = len(server['channels'])
    server['channels'].append({'id':(n+1), 'name':channel, 'member_ids':members})

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
        print('Unknown option:', choice)

def display_channels():
    print('\nChannels list\n-------')
    for elem in server['channels'] :
        print(elem['id'],' - ',elem['name'],' : ',elem['member_ids'])
    print('\nn. Create channel\nx. Main menu')
    ch = input('Select an option: ')
    if ch == 'n':
        channel = input('Name of the new channel: ')
        members = list(input('ID of the users belonging to the new channel (without separators): '))
        create_channel(channel,members)
        main_menu()
    elif ch == 'x':
        main_menu()
    else:
        print('Unknown option:', choice)

def main_menu():
    print('\n1. See users\n2. See channels\nx. Leave')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
    elif choice == '1':
        display_users()
    elif choice == '2':
        display_channels()
    else:
        print('Unknown option:', choice)



print('=== Messenger ===')
main_menu()
