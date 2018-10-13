import socket
import select
import time
from datetime import datetime
import json
import ast
import os


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

        permnum = None

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
                            if '$$$' in data.decode():
                                USERNAME = data.decode().strip('$$$')
                                if '%!' in USERNAME:
                                    tempUsername = USERNAME.strip('%!')
                                else:
                                    admins = ['Test']
                                    Users[addr] = USERNAME

                            if '#!-' in data.decode():
                                tempPassword = data.decode().strip('#!-')
                                for line in open("data/accounts.txt", "r").readlines():
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
                                        "%H:%M:%S")) + '] ' + 'GAME: Started hangman game with word: ' + str(word))
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
                                        "%H:%M:%S")) + '] ' + 'GAME: Restarted ongoing hangman game')
                            elif '[]/./LOST' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Ongoing hangman game ended')
                            elif '[]_@' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Ongoing hangman game ended')
                            elif '-=;/;' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                lettersent = data.decode.strip('-=;/;')
                                print('[' + str(datetime.now().strftime(
                                    "%H:%M:%S")) + '] ' + "GAME: Guessed letter '{0}' in hangman".format(lettersent))
                            elif '*@;#-' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                playername = data.decode.strip('*@;#-')
                                print('[' + str(datetime.now().strftime(
                                    "%H:%M:%S")) + '] ' + "GAME: {0} joined hangman game".format(playername))
                            elif 'WORD_GUESSED69' in data.decode():
                                Broadcast(sock, data, Users[addr], True)
                                print('[' + str(datetime.now().strftime(
                                        "%H:%M:%S")) + '] ' + 'GAME: Hangman word was guessed correctly')
                            elif '(' == str(data.decode())[0]:
                                def replace_line(file_name, line_num, text):
                                    lines = open(file_name, 'r').readlines()
                                    lines[line_num] = text
                                    out = open(file_name, 'w')
                                    out.writelines(lines)
                                    out.close()


                                unsavedData = str(data.decode()).strip('(')
                                unsavedData = ast.literal_eval(unsavedData)
                                #dumped = json.dumps(unsavedData)
                                #saveUser = unsavedData["information"]["username"]
                                #unsavedData["information"]["username"]
                                
                                with open('data/data-{0}.json'.format(newName), 'w') as jsonConfig:
                                    json.dump(unsavedData, jsonConfig)

                                with open('data/game-accounts.txt', 'r+') as myFile:
                                    print(myFile.readlines)
                                    print(oldName)
                                    for num, line in enumerate(myFile, 1):
                                        if oldName in line:
                                            permnum = num - 1

                                file5 = open('data/game-accounts.txt', 'r')
                                file5r = file5.readlines()
                                cred2 = str(file5r[permnum])
                                credentials2 = cred2.split(',')
                                credentials2[0] = newName
                                newl = ','.join(credentials2)
                                replace_line('data/game-accounts.txt', permnum, newl)

                            elif '}' == str(data.decode())[0]:

                                allNames = str(data.decode()).strip('}').split(',')
                                oldName = allNames[0]
                                newName = allNames[1]

                                os.rename('data/data-{0}.json'.format(oldName), 'data/data-{0}.json'.format(newName))
                                
                            elif '~' == str(data.decode())[0]:

                                with open('data/game-accounts.txt') as myFile:
                                    for num, line in enumerate(myFile, 1):
                                        if str(data.decode()).strip('~') in line:
                                            permnum = num - 1

                                if permnum is not None:
                                    filef = open('data/game-accounts.txt', 'r')
                                    filer = filef.readlines()
                                    cred = str(filer[permnum])
                                    credentials = cred.split(',')
                                    recUser = data.decode().strip('~')
                                else:
                                    sock.send(str.encode('False'))

                            elif '>' == str(data.decode())[0]:
                                time.sleep(.08)
                                if permnum is not None:
                                    permnum = None
                                    if str(data.decode()).strip('>') == credentials[1].rstrip():
                                        sock.send(str.encode('True'))
                                        time.sleep(.08)
                                        try:
                                            print('[' + str(datetime.now().strftime(
                                                "%H:%M:%S")) + '] ' + 'GAME: User {0} logged in successfully'.format(recUser))
                                        except:
                                            pass
                                        with open('data/data-{0}.json'.format(recUser)) as jsonConfig:
                                            config = json.load(jsonConfig)
                                            sock.send(str.encode(str(config)))
                                    else:
                                        try:
                                            print('[' + str(datetime.now().strftime(
                                                "%H:%M:%S")) + '] ' + 'GAME: User {0} attempted to login (failed)'.format(recUser))
                                        except:
                                            pass
                                        sock.send(str.encode('False'))

                            elif '/' == str(data.decode())[0]:
                                if '_' == str(data.decode())[1]:

                                    newUser = str(data.decode()).strip('/_')

                                    with open('data/game-accounts.txt') as myFile:
                                        for num, line in enumerate(myFile, 1):
                                            if str(data.decode()).strip('/_') in line:
                                                permnum = num - 1

                                    if permnum is not None:
                                        sock.send(str.encode('False'))

                            elif '-' == str(data.decode())[0]:
                                if '/' == str(data.decode())[1]:
                                    if permnum is None:
                                        import shutil
                                        newPass = str(data.decode()).strip('-/')
                                        file2 = open('data/game-accounts.txt', 'a')
                                        newStr = newUser + ',' + newPass + '\n'
                                        file2.write(newStr)
                                        file2.close()
                                        sock.send(str.encode('True'))
                                        time.sleep(.08)
                                        shutil.copy2('data/data-Default.json', 'data/data-{0}.json'.format(newUser))
                                        with open('data/data-{0}.json'.format(newUser)) as jsonConfig:
                                            config = json.load(jsonConfig)
                                            config["information"]["username"] = newUser
                                            config["information"]["name"] = newUser
                                            sock.send(str.encode(str(config)))
                                        with open('data/data-{0}.json'.format(newUser)) as jsonConfig:
                                            json.dump(config, jsonConfig)
                                    
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
            except Exception as e:
                import sys
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    except Exception as e:
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    serverSocket.close()    
