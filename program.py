import socket
import time
from tools.logger import Logger


"""

example = {
    'Release Notes': {
        'Added': [
            'New debugging logger',
            'More logging entries',
            'Recovery commands'
        ],
        'Changed': [
            'Improved updater reliability',
            'Game server structure'
        ],
        'Removed': [
            'Legacy notification support',
            'Support for version three or below',
            'Outdated/unused code'
        ]
    }
}

print('Release notes for Version 4.85:')
print('Added:')
for line in example['Release Notes']['Added']:
    print(f'- {line}')
print('Changed:')
for line in example['Release Notes']['Changed']:
    print(f'- {line}')
print('Removed:')
for line in example['Release Notes']['Removed']:
    print(f'- {line}')
    
"""


clientInformation = {
    'Client Information': {
        'Username': 'Shivam',
        'Version': '4.84',
        'Rank': 'User'
    }
}

clientInformation['Client Information']['Username'] = input(Logger.log('Enter username: '))

IP = '127.0.0.1'
PORT = 6666

gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gameSocket.connect((IP, PORT))
gameSocket.send(str.encode(f'CLIENT_INFORMATION<>{str(clientInformation)}'))
time.sleep(0.01)
# gameSocket.send(b'ONLINE')


while True:
    try:
        receive_data = gameSocket.recv(4096)
    except:
        Logger.log('The server closed the connection (failed to receive any data)', 'ERROR')
        break
    if not receive_data:
        Logger.log('Lost connection to the server (received invalid data)', 'ERROR')
        break
    else:
        arguments = receive_data.decode().split('<>')
        if arguments[0] == 'CONN_ERROR':
            Logger.log('Server rejected connection based on client information.', 'DISCONNECT')
            Logger.log(arguments[1])
            break
        elif arguments[0] == 'CONN_SUCCESS':
            Logger.log(arguments[1])
        elif arguments[0] == 'USER_LIST':
            all_users = arguments[1].split(';')
            for user in all_users:
                print(user)
