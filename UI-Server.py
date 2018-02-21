import socket
import select
from datetime import datetime


def Broadcast (sock, message, usr):
    try:
        for socket in CLIST:
            if socket != serverSocket:
                if message.decode() != '\n':
                    print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + message.decode())
                socket.send(message)
    except:
        print('ERROR: Broadcast error - perhaps a client disconnected?')


if __name__ == "__main__":

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
                    try:
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
                    except:
                        print('ERROR: Data handling failed.')
                    else:
                        try:
                            Broadcast(sock, data, Users[addr])
                        except:
                            Broadcast(sock, data, 'SOLO')
                            print('ERROR: Broadcast error - perhaps a solo client disconnected?')
                
    serverSocket.close()    
