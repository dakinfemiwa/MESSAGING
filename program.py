import socket
import time
import ast
import _thread

try:
    from tools.logger import Logger
except:
    print('ERROR: Failed to import logger.')


class Client:
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 6666
        self.gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientInformation = {'Client Information': {'Username': 'Default', 'Version': '5.00', 'Rank': 'User'}}

        self.clientInformation['Client Information']['Username'] = input('INPUT: Enter username: ')

        self.connect()
        self.listen()

    def connect(self):
        try:
            self.log(f'Attempting to connect to [{self.IP}:{self.PORT}]')
            self.gameSocket.connect((self.IP, self.PORT))
            _thread.start_new(self.listen, ())
            self.log('Sending client information to the server')
            self.send(f'CLIENT_INFORMATION<>{self.clientInformation}')
            self.send('ONLINE')
        except ConnectionRefusedError:
            self.log('Failed to connect to the server (offline)', 'ERROR')

    def listen(self):
        while True:
            try:
                receive_data = self.gameSocket.recv(4096)
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
                    self.command(arguments)

    def send(self, data):
        self.gameSocket.send(str.encode(data))
        self.delay(0.05)

    def command(self, cmd):
        if cmd[1] == 'CHALLENGED':
            print('Challenged by', cmd[2])
            self.send('CONNECT4<>ACCEPTED<>' + cmd[2])
        elif cmd[1] == 'ACCEPTED':
            print('Accepted by', cmd[2])

    @staticmethod
    def log(log, level='INFO'):
        try:
            Logger.log(log, level)
        except:
            pass

    @staticmethod
    def delay(length=0.01):
        time.sleep(length)
        # Removed


# gameSocket.send(b'CONNECT4<>START<>SM')


if __name__ == '__main__':
    User = Client()
