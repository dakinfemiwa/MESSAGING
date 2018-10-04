import socket
import select
import time
from datetime import datetime


def Broadcast(sock, message, usr, hidden=False):
    global oldMessage
    if 1:
        for socket in CLIST:
            if socket != serverSocket:
                if message.decode() != '\n':
                    if message.decode() != oldMessage:
                        if hidden==False:
                            print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] MESSAGE: ' + message.decode().lstrip().rstrip())
                    oldMessage = message.decode()
                    socket.send(message)
    if 0:
        print('[' + str(datetime.now().strftime(
            "%H:%M:%S")) + '] ' + 'ERROR: Unable to broadcast message - hard disconnect')


if __name__ == "__main__":
    global oldMessage
    oldMessage = ''
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
                            data = sock.recv(4096, )
                        except:
                            try:
                                tempstore = str(Users[addr])
                            except:
                                pass
                            try:
                                Broadcast(sock, str.encode((tempstore) + " has left the server"), 'SEN')
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
                            if '$$$' in data.decode():
                                USERNAME = data.decode().strip('$$$')
                                if '%!' in USERNAME:
                                    tempUsername = USERNAME.strip('%!')
                                else:
                                    admins = ['Test']
                                    Users[addr] = USERNAME

                            if '#!-' in data.decode():
                                tempPassword = data.decode().strip('#!-')
                                for line in open("accounts.txt", "r").readlines():
                                    login_info = line.split()
                                    if tempUsername == login_info[0] and tempPassword == login_info[1]:
                                        print('[' + str(datetime.now().strftime(
                                            "%H:%M:%S")) + '] ' + 'STATUS: An administrator connected to the server')
                                        joinStr = tempUsername + ' has joined the server [admin]'
                                        Broadcast(sock, str.encode(joinStr),
                                                  'ANC')
                                        Users[addr] = tempUsername
                                        time.sleep(.1)
                                        try:
                                            for key, val in Users.items():
                                                if val == tempUsername:
                                                    targetIP = key
                                                    break
                                            for socket in CLIST:
                                                if str(targetIP[0]) in str(socket):
                                                    if str(targetIP[1]) in str(socket):
                                                        time.sleep(.1)
                                                        socket.send(str.encode('-##-3'))
                                        except:
                                            print('[' + str(datetime.now().strftime(
                                                "%H:%M:%S")) + '] ' + 'ERROR: Unable to authenticate user')
                                    else:
                                        Users[addr] = tempUsername
                                        try:
                                            for key, val in Users.items():
                                                if val == tempUsername:
                                                    targetIP = key
                                                    break
                                            for socket in CLIST:
                                                if str(targetIP[0]) in str(socket):
                                                    if str(targetIP[1]) in str(socket):
                                                        time.sleep(.1)
                                                        socket.send(str.encode('Incorrect details!'))
                                                        socket.send(str.encode('\n'))
                                                        socket.send(str.encode('You have been disconnected from the server.'))
                                                        CLIST.remove(socket)
                                                        del Users[targetIP]
                                        except:
                                            print('[' + str(datetime.now().strftime(
                                                "%H:%M:%S")) + '] ' + 'ERROR: Unable to authenticate user')

                            elif '-$$' in data.decode():
                                VERSION = data.decode().strip('-$$')
                                Broadcast(sock, str.encode("\nThis user is connected through version " + VERSION), Users[addr])

                            elif '$-$online' in data.decode():
                                try:
                                    Broadcast(sock, str.encode("\nCurrent connected users:"), Users[addr])

                                    for x in range(0, len(CLIST)-1):
                                        client = list(Users.values())[x]
                                        client = str(client)
                                        Broadcast(sock, str.encode(client) + str.encode("\n"), Users[addr])
                                except:
                                    print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'ERROR: Could not display online users list')
                            elif '$-$shutdown' in data.decode():
                                try:
                                    serverSocket.close()
                                    print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'STATUS: Received shutdown command')
                                    Broadcast(sock, str.encode("\nServer is shutting down"), 'game')
                                    print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'STATUS: Closing all connections')
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
                                    print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'ERROR: Unable to handle a kick')
                            elif '£££' in data.decode():
                                targetUser = data.decode().split()[1]
                                num = len(targetUser) + 2
                                targetMessage = data.decode().strip('£££')[num:]
                                try:
                                    for key, val in Users.items():
                                        if val == targetUser:
                                            targetIP = key
                                            break
                                    for socket in CLIST:
                                        if str(targetIP[0]) in str(socket):
                                            if str(targetIP[1]) in str(socket):
                                                final_msg = '* PRIVATE MESSAGE *: ' + targetMessage
                                                socket.send(str.encode(final_msg))
                                except:
                                    print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'ERROR: Unable to send a private message')
                            elif '_-$' in data.decode():
                                targetUser = data.decode().strip('_-$')
                                try:
                                    for key, val in Users.items():
                                        if val == targetUser:
                                            targetIP = key
                                            break
                                    for socket in CLIST:
                                        if str(targetIP[0]) in str(socket):
                                            if str(targetIP[1]) in str(socket):
                                                socket.send(str.encode('-_$one'))
                                except:
                                    print('ERROR: Unhandled ghost')
                            elif '$-$cpl' in data.decode():
                                Broadcast(sock, str.encode('\nServer is now being being controlled by a control panel'), 'SVR')

                            elif ':-!=!' in data.decode():
                                word = data.decode().strip(':-!=!')
                                word = word[:-12]
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Started Hangman game with word: ' + str(word))
                                Broadcast(sock, data, Users[addr], True)

                            elif '{-=*=-}' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Hangman word was refreshed')
                            elif '[]-=!=-[]' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Hangman lives were refreshed')
                            elif '%^%-' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Restarted ongoing Hangman game')
                            elif '[]/./LOST' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Ongoing hangman game ended')
                            elif '[]_@' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Ongoing hangman game ended')
                            elif 'WORD_GUESSED69' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Hangman word was guessed correctly')

                            else:
                                if "$" in data.decode():
                                    if "%!" in data.decode():
                                        pass
                                else:
                                    try:
                                        Broadcast(sock, data, Users[addr])
                                    except:
                                        Broadcast(sock, data, 'SOLO')
                                        print('[' + str(datetime.now().strftime(
                                            "%H:%M:%S")) + '] ' + 'ERROR: Unable to broadcast message - hard disconnect')
            except:
                pass

    except Exception as error:
        print(error)

    serverSocket.close()    
