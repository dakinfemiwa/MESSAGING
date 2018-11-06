import socket
import select
import time
import ast
from tools.logger import Logger
from requests import get


class GameServer:
    def __init__(self):
        self.IP = '0.0.0.0'
        self.EXTERNAL_IP = get('https://api.ipify.org').text
        self.PORT = 6666
        self.BUFFER_SIZE = 4096
        self.LISTEN_INT = 10
        self.LIST = []
        self.MIN_VERSION = 3.00

        self.connectedUsers = {}
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverStatus = True

        Logger.log('Initialized chat server with version four support.')

    def run(self):
        self.serverSocket.bind((self.IP, self.PORT))
        self.serverSocket.listen(self.LISTEN_INT)
        self.LIST.append(self.serverSocket)
        self.receive()

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
                            elif arguments[0] == 'CLIENT_INFORMATION':
                                Logger.log(f'Received client information from [{address[0]}:{address[1]}]')
                                clientInformation = ast.literal_eval(arguments[1])
                                clientData = []
                                for field in ['Username', 'Version', 'Rank']:
                                    clientData.append(str([clientInformation['Client Information'][field]][0]))
                                if clientData[0] == '' or clientData[0] == ' ':
                                    sock.send(b'CONN_ERROR<>Invalid username (username not allowed)')
                                    Logger.log(f'Rejected connection from [{address[0]}:{address[1]}] due to invalid username.')
                                else:
                                    if float(clientData[1]) < self.MIN_VERSION:
                                        sock.send(str.encode(f'CONN_ERROR<>Client is out of date (latest version is {str(self.MIN_VERSION)})'))
                                        Logger.log(f'Rejected connection from [{address[0]}:{address[1]}] ({clientData[0]}) due to outdated client [{clientData[1]}]', 'DISCONNECT')
                                        sock.close()
                                        self.LIST.remove(sock)
                                    else:
                                        self.connectedUsers[address] = clientData[0]
                                        sock.send(b'CONN_SUCCESS<>Successfully connected to the server.')
                            else:
                                self.broadcast(receivedData.decode())
            except Exception as error:
                Logger.error(error)

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
