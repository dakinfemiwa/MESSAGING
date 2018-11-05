import socket
import select
import time
from tools.logger import Logger
from requests import get


# Rewriting game server using classes.
class GameServer:
    def __init__(self):
        self.IP = '0.0.0.0'
        self.EXTERNAL_IP = get('https://api.ipify.org').text
        self.PORT = 6666
        self.BUFFER_SIZE = 4096
        self.LISTEN_INT = 10
        self.LIST = []

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
                        sockfd, addr = self.serverSocket.accept()
                        self.LIST.append(sockfd)
                        Logger.log('Client [{0}:{1}] connected to the server.'.format(addr[0], addr[1]), 'CONNECT')
                    else:
                        try:
                            receivedData = sock.recv(self.BUFFER_SIZE, )
                        except:
                            self.broadcast("[undefined] left the server")
                            try:
                                del self.connectedUsers[addr]
                                Logger.log('Client [{0}:{1}] disconnected from the server.'.format(addr[0], addr[1]), 'DISCONNECT')
                            except Exception as error:
                                Logger.error(error)
                            sock.close()
                            self.LIST.remove(sock)
                            continue
                        if receivedData:
                            if 'QUIT' in receivedData.decode():
                                self.LIST.remove(sock)
                                sock.close()
                            else:
                                self.broadcast(receivedData.decode())
            except Exception as error:
                Logger.error(error)

    def broadcast(self, message):
        try:
            for connectedSocket in self.LIST:
                if connectedSocket != self.serverSocket:
                    connectedSocket.send(str.encode(message))
                    Logger.log(message.rstrip().lstrip(), 'MESSAGE')
                    time.sleep(0.05)
        except Exception as error:
            Logger.error(error)


if __name__ == '__main__':
    try:
        Server = GameServer()
        Server.run()
    except Exception as e:
        Logger.error(e)
