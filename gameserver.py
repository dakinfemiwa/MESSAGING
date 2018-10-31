import socket
import select
import time
from datetime import datetime
import json
import ast
import os
import sys


def Broadcast(message):
    for iSocket in CLIST:
        if iSocket != serverSocket:
            iSocket.send(str.encode(message))
        print(message)


if __name__ == "__main__":
    if 1:
        def startUp():
            global CLIST, People, Users, IP, serverSocket

            CLIST = []
            People = []
            Users = {}

            print('[' + str(datetime.now().strftime(
                "%H:%M:%S")) + '] ' + 'STATUS: Chat server initialized with version four support')
            IP = '0.0.0.0'

            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((IP, 6666))
            serverSocket.listen(10)

            print('[' + str(datetime.now().strftime(
                "%H:%M:%S")) + '] ' + 'STATUS: Listening for incoming connections')

            CLIST.append(serverSocket)

        startUp()

        while True:
            read_sockets, write_sockets, error_sockets = select.select(CLIST, [], [])

            if 1:

                for sock in read_sockets:
                    if sock == serverSocket:
                        sockfd, addr = serverSocket.accept()
                        CLIST.append(sockfd)
                        print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + 'CONNECT: Client [%s, %s] connected' % addr)
                        sockfd.send(str.encode('TT'))

                    else:
                        try:
                            data = sock.recv(4096, )
                        except:
                            try:
                                tempstore = str(Users[addr])
                            except:
                                pass
                            try:
                                Broadcast("DISCONNECT:{0}".format(tempstore))
                                time.sleep(.02)
                                Broadcast("USER has left the server")
                            except Exception as details:
                                print('[' + str(datetime.now().strftime(
                                    "%H:%M:%S")) + '] ' + 'WARNING: A disconnect message may have failed to send')
                            try:
                                del Users[addr]
                                print('[' + str(datetime.now().strftime(
                                    "%H:%M:%S")) + '] ' + 'DISCONNECT: Client [%s, %s] disconnected' % addr)
                            except Exception as details:
                                print(details)
                            sock.close()
                            CLIST.remove(sock)
                            continue

                        if data:
                            if '$$$' in data.decode():
                                USERNAME = data.decode().strip('$$$')
                                if '%!' in USERNAME:
                                    tempUsername = USERNAME.strip('%!')
                                else:
                                    Users[addr] = USERNAME

                            else:
                                if 1:
                                    Broadcast(data.decode())
                                if 0:
                                    print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'ERROR: Unable to broadcast message - hard disconnect')
            if 0:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    if 0:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    serverSocket.close()    
