import socket
import select
from datetime import datetime
from collections import OrderedDict


def Broadcast (sock, message, usr):
    try:
        for socket in CLIST:
            if socket != serverSocket:
                if message.decode() != '\n':
                    print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + message.decode())
                socket.send(message)
    except:
        print('ERROR: Broadcast error - perhaps a client disconnected?')


def Handler():
    # Handles permissions
    pass


if __name__ == "__main__":

    try:

        def startUp():
            global CLIST, People, Users, IP, serverSocket

            CLIST = []
            People = []
            Users = {}

            print('INFO: Chat server - V2')
            IP = '0.0.0.0'

            # IP = str(input("Enter IP to bind server: "))

            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((IP, 6666))
            serverSocket.listen(10)

            CLIST.append(serverSocket)

        startUp()

        while 1:

            read_sockets, write_sockets, error_sockets = select.select(CLIST, [], [])

            for sock in read_sockets:

                if sock == serverSocket:

                    sockfd, addr = serverSocket.accept()
                    CLIST.append(sockfd)
                    print("STATUS: Client [%s, %s] connected" % addr)

                else:
                    try:
                        data = sock.recv(4096, )
                    except:
                        try:
                            Broadcast(sock, str.encode("\n") + str.encode(str(Users[addr]) + " has left the server"), addr)
                        except:
                            print('ERROR: Unable to notify clients of disconnect.')
                        try:
                            del Users[addr]
                            print("STATUS: Client [%s, %s] is offline" % addr)
                        except:
                            pass
                        sock.close()
                        CLIST.remove(sock)
                        continue

                    if data:
                        if '$$$' in data.decode():
                            USERNAME = data.decode().strip('$$$')
                            Users[addr] = USERNAME

                        elif '-$$' in data.decode():
                            VERSION = data.decode().strip('-$$')
                            Broadcast(sock, str.encode("\nThis user is connected through version " + VERSION), Users[addr])

                        elif '$-$online' in data.decode():
                            try:
                                Broadcast(sock, str.encode("\nCurrent connected users:"), Users[addr])

                                for x in range(0, len(CLIST)-1):
                                    client = list(Users.values())[x]
                                    client = str(client)
                                    Broadcast(sock, str.encode("\n") + str.encode(client), Users[addr])
                            except:
                                print('ERROR: Could not print online user list.')
                        elif '$-$shutdown' in data.decode():
                            try:
                                serverSocket.close()
                                Broadcast(sock, str.encode("\nServer is shutting down"), 'game')
                                serverSocket.close()
                            except:
                                Broadcast(sock, str.encode("\nServer shutdown failed"), 'game')
                        elif '$-$restart' in data.decode():
                            try:
                                serverSocket.close()
                                startUp()
                                Broadcast(sock, str.encode("\nServer is restarting"), 'game')
                            except:
                                Broadcast(sock, str.encode("\nServer restart failed"), 'game')
                        elif '$$-' in data.decode():
                            targetUser = data.decode().strip('$$-')
                            try:
                                for key, val in Users.items():
                                    if val == targetUser:
                                        targetIP = key
                                        break
                                for socket in CLIST:
                                    if str(targetIP[0]) in str(socket):
                                        if str(targetIP[1]) in str(socket):
                                            Broadcast(sock, str.encode(targetUser) + str.encode(' was kicked from the server'), 'SVR')
                                            socket.send(str.encode('You have been kicked by an admin, connection lost.'))
                                            CLIST.remove(socket)
                                            del Users[targetIP]
                            except:
                                print('ERROR: Unhandled kick')
                        elif '$-$cpl' in data.decode():
                            Broadcast(sock, str.encode('\nServer is now being being controlled by a control panel'), 'SVR')
                        else:
                            try:
                                Broadcast(sock, data, Users[addr])
                            except:
                                Broadcast(sock, data, 'SOLO')
                                print('ERROR: Broadcast error - perhaps a solo client disconnected?')

    except Exception as error:
        print(error)
        print('Runtime error')

    serverSocket.close()    
