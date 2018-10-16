import socket
import select
import time
from datetime import datetime


def Broadcast(sock, message, usr, hidden=False):
    try:
        for socket in CLIST:
            if socket != serverSocket:
                if message.decode() != '\n':
                    print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] MESSAGE: ' + message.decode().lstrip().rstrip())
                    socket.send(message)
    except:
        print('[' + str(datetime.now().strftime(
            "%H:%M:%S")) + '] ' + 'ERROR: Unable to broadcast message - hard disconnect')


if __name__ == "__main__":
    try:
        def startUp():
            global CLIST, People, Users, IP, serverSocket

            CLIST = []
            People = []
            Users = {}

            print('[' + str(datetime.now().strftime(
                "%H:%M:%S")) + '] ' + 'STATUS: Chat server initialized with version four support')
            IP = '0.0.0.0'

            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            serverSocket.bind((IP, 6666))
            serverSocket.listen(10)

            print('[' + str(datetime.now().strftime(
                "%H:%M:%S")) + '] ' + 'STATUS: Listening for incoming connections')

            CLIST.append(serverSocket)

        startUp()

        while True:
            read_sockets, write_sockets, error_sockets = select.select(CLIST, [], [])

            try:

                for sock in read_sockets:
                    if sock == serverSocket:
                        sockfd, addr = serverSocket.accept()
                        CLIST.append(sockfd)
                        print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + 'CONNECT: Client [%s, %s] connected' % addr)

                    else:
                        try:
                            data = sock.recv(20, )
                        except:
                            try:
                                tempstore = str(Users[addr])
                            except:
                                pass
                            try:
                                Broadcast(sock, str.encode(tempstore + " has left the server"), 'SEN')
                                time.sleep(.03)
                                Broadcast(sock, str.encode('.;/~' + tempstore), 'SEN')
                            except Exception as details:
                                print('[' + str(datetime.now().strftime(
                                    "%H:%M:%S")) + '] ' + 'WARNING: A disconnect message may have failed to send')
                            try:
                                del Users[addr]
                                print('[' + str(datetime.now().strftime(
                                    "%H:%M:%S")) + '] ' + 'DISCONNECT: Client [%s, %s] disconnected' % addr)
                            except Exception as details:
                                print('ERROR OCCURED')
                            sock.close()
                            CLIST.remove(sock)
                            continue

                        if data:
                                Broadcast(sock, data, 'Test')
            except:
                pass

    except Exception as error:
        print(error)

    serverSocket.close()    
