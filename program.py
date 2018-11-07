import socket
import time
import ast
import _thread
from tools.logger import Logger
from datetime import datetime

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

clientInformation['Client Information']['Username'] = input(f'[{datetime.now().strftime("%H:%M:%S")}] INPUT: Enter username: ')

IP = '127.0.0.1'
PORT = 6666

Logger.log(f'Attempting to connect to [{IP}:{PORT}]')

gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gameSocket.connect((IP, PORT))
gameSocket.send(str.encode(f'CLIENT_INFORMATION<>{str(clientInformation)}'))
time.sleep(0.01)
# gameSocket.send(b'ONLINE')
gameSocket.send(b'CONNECT4<>START<>SM')


def listen():
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
            elif arguments[0] == 'SERVER_INFORMATION':
                serverInfo = ast.literal_eval(str(arguments[1]))
                serverData = []
                for field in ['Server Name', 'Uptime', 'Minimum Version', 'Server Version']:
                    serverData.append(serverInfo['Server Information'][field])
                    Logger.log(f'{field}: {str(serverInfo["Server Information"][field])}', 'SERVER')
            elif arguments[0] == 'USER_LIST':
                all_users = arguments[1].split(';')
                for user in all_users:
                    if user is not '':
                        Logger.log(user, 'USER LIST')
            elif arguments[0] == 'CONNECT4':
                handle_game_cmd(arguments)


def handle_game_cmd(cmd):
    if cmd[1] == 'CHALLENGED':
        print('Challenged by', cmd[2])
        gameSocket.send(str.encode('CONNECT4<>ACCEPTED<>' + cmd[2]))
    elif cmd[1] == 'ACCEPTED':
        print('Accepted by', cmd[2])


Testing = False

if Testing:

    from tkinter import *
    root = Tk()
    ent = Entry(root)
    ent.pack()
    but = Button(root, command=lambda:(gameSocket.send(str.encode(f'{ent.get()}')))).pack()
    _thread.start_new_thread(root.mainloop(),)


_thread.start_new_thread(listen(), )
