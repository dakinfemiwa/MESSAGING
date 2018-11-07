import socket
import select
import time
import ast
from tools.logger import Logger
from datetime import datetime
from requests import get


class GameServer:
    def __init__(self):
        self.IP = '0.0.0.0'
        # self.EXTERNAL_IP = get('https://api.ipify.org').text
        self.EXTERNAL_IP = '12.345.67.890'
        self.PORT = 6666
        self.BUFFER_SIZE = 4096
        self.LISTEN_INT = 10
        self.LIST = []
        self.MIN_VERSION = 3.00
        self.LAUNCH_TIME = datetime.now().strftime('%H:%M:%S')
        self.SERVER_NAME = 'Game Server [TEST]'

        self.connectedUsers = {}
        self.reversedUsers = {}
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverStatus = True

        self.serverInformation = {
            'Server Information': {
                'Server Name': self.SERVER_NAME,
                'Uptime': self.LAUNCH_TIME,
                'Minimum Version': self.MIN_VERSION
            }
        }

        Logger.log(f'Initialized chat server with version {str(self.MIN_VERSION)} support.')

    def run(self):
        self.serverSocket.bind((self.IP, self.PORT))
        self.serverSocket.listen(self.LISTEN_INT)
        self.LIST.append(self.serverSocket)
        self.receive()

    def users(self):
        userList = []
        for user in self.connectedUsers:
            userList.append(self.connectedUsers[user])
        return userList

    def receive(self):
        Logger.log(f'Started listening for connections at [{self.EXTERNAL_IP}:{self.PORT}]')
        Logger.log(f'Accepting local connections at [127.0.0.1:{self.PORT}]')
        while self.serverStatus:
            try:
                read_sockets, write_sockets, error_sockets = select.select(self.LIST, [], [])
                for sock in read_sockets:
                    if sock == self.serverSocket:
                        sockfd, address = self.serverSocket.accept()
                        self.LIST.append(sockfd)
                        Logger.log(f'Client [{address[0]}:{address[1]}] connected to the server.', 'CONNECT')
                    else:
                        try:
                            receivedData = sock.recv(self.BUFFER_SIZE, )
                        except:
                            self.broadcast('[{user_leaving}] left the server'.format(user_leaving='undefined'))
                            try:
                                try:
                                    disconnected_user = self.connectedUsers[address]
                                    del self.connectedUsers[address]
                                except:
                                    disconnected_user = '[undefined]'
                                Logger.log(f'Client [{address[0]}:{address[1]}] ({disconnected_user}) disconnected from the server.', 'DISCONNECT')
                            except Exception as error:
                                Logger.error(error)
                            sock.close()
                            self.LIST.remove(sock)
                            continue
                        if receivedData:
                            arguments = receivedData.decode().split('<>')
                            if 'DISCONNECT' in receivedData.decode():
                                try:
                                    disconnected_user = self.connectedUsers[address]
                                    del self.connectedUsers[address]
                                except:
                                    disconnected_user = '[undefined]'
                                Logger.log(f'Client [{address[0]}:{address[1]}] ({disconnected_user}) disconnected from the server.', 'DISCONNECT')
                                Logger.log(f'Received quit command from client [{address[0]}:{address[1]}]')
                            elif arguments[0] == 'CONNECT4':
                                self.handle_game_commands(arguments, sock)
                            elif arguments[0] == 'ONLINE':
                                userList = ''
                                for user in self.connectedUsers:
                                    userList = userList + self.connectedUsers[user] + ';'
                                sock.send(str.encode('USER_LIST<>' + userList))
                                Logger.log(f'[{address[0]}:{address[1]}] ({self.connectedUsers[address]}) requested user list.')
                                Logger.log(f'Current connected users: {userList.replace(";", " ")}')
                            elif arguments[0] == 'CLIENT_INFORMATION':
                                Logger.log(f'Received client information from [{address[0]}:{address[1]}]')
                                clientInformation = ast.literal_eval(arguments[1])
                                clientData = []
                                for field in ['Username', 'Version', 'Rank']:
                                    clientData.append(str([clientInformation['Client Information'][field]][0]))
                                if clientData[0] == '' or clientData[0] == ' ':
                                    sock.send(b'CONN_ERROR<>Invalid username (username not allowed)')
                                    Logger.log(f'Rejected connection from [{address[0]}:{address[1]}] due to invalid username.')
                                    sock.close()
                                    self.LIST.remove(sock)
                                else:
                                    userListByName = []
                                    for user in self.connectedUsers:
                                        userListByName.append(self.connectedUsers[user])
                                    if clientData[0] in userListByName:
                                        sock.send(b'CONN_ERROR<>A user with that name is already connected (use a different username)')
                                        Logger.log(f'Rejected connection from [{address[0]}:{address[1]}] ({clientData[0]}) due to duplicate username.', 'DISCONNECT')
                                        sock.close()
                                        self.LIST.remove(sock)
                                    else:
                                        if float(clientData[1]) < self.MIN_VERSION:
                                            sock.send(str.encode(f'CONN_ERROR<>Client is out of date (latest version is {str(self.MIN_VERSION)})'))
                                            Logger.log(f'Rejected connection from [{address[0]}:{address[1]}] ({clientData[0]}) due to outdated client [{clientData[1]}]', 'DISCONNECT')
                                            sock.close()
                                            self.LIST.remove(sock)
                                        else:
                                            self.connectedUsers[address] = clientData[0]
                                            sock.send(b'CONN_SUCCESS<>Successfully connected to the server.')
                                            Logger.log(f'Allowed connection from [{address[0]}:{address[1]}] ({clientData[0]}) [{clientData[1]}]', 'CONNECT')
                                            time.sleep(0.05)
                                            start_dt = datetime.strptime(self.serverInformation['Server Information']['Uptime'], '%H:%M:%S')
                                            end_dt = datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S')
                                            diff = (end_dt - start_dt)
                                            serverInformationTemp = self.serverInformation
                                            serverInformationTemp['Server Information']['Uptime'] = str(diff)
                                            time.sleep(0.05)
                                            sock.send(str.encode(f'SERVER_INFORMATION<>{str(serverInformationTemp)}'))
                                            Logger.log(f'Sent server information to client [{address[0]}:{address[1]}] ({clientData[0]})')
                                            self.serverInformation['Server Information']['Uptime'] = self.LAUNCH_TIME
                            else:
                                self.broadcast(receivedData.decode())
            except Exception as error:
                Logger.error(error)

    def handle_game_commands(self, args, sender):
        if args[0] == 'CONNECT4':
            if args[1] == 'START':
                if args[2] in self.users():
                    ind = self.users().index(args[2])
                    print(self.LIST)
                    print(self.LIST[ind - 1])

                else:
                    sender.send(b'GAME_ERROR<>MEMBER_NOT_FOUND')

    def broadcast(self, message):
        try:
            for connectedSocket in self.LIST:
                if connectedSocket != self.serverSocket:
                    connectedSocket.send(str.encode(message))
                    time.sleep(0.05)
            Logger.log(message.rstrip().lstrip(), 'BROADCAST')
        except Exception as error:
            Logger.error(error)


if __name__ == '__main__':
    try:
        Server = GameServer()
        Server.run()
    except Exception as e:
        Logger.error(e)
