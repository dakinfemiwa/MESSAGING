import sys
import socket
import threading
import select
import string
	
def broadcast (sock, message, usr):
    try:
        for socket in CLIST:
            if socket != server_socket:
                print('FROM: ', usr)
                print('MESSAGE: ' , message)
                socket.send(message)
    except:
        print('ERROR: Broadcast error - perhaps a client disconnected?')

if __name__ == "__main__":

    CLIST = []
    People = []
    Users = {}
    
    print('INFO: Chat server - BETA')
    # IP = str(input("Enter IP to bind server: "))
    IP = '0.0.0.0'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, 6666))
    server_socket.listen(10)
 
    CLIST.append(server_socket)   # Add socket

    while 1:
        # Get list of ready to be read with select
        read_sockets, write_sockets, error_sockets = select.select(CLIST, [], [])

        for sock in read_sockets:

            if sock == server_socket: 
                sockfd, addr = server_socket.accept()   # New connection recieved 
                CLIST.append(sockfd)                    # Append the new connection
                print("STATUS: Client [%s, %s] connected" % addr)

            else:
                try:
                    data = sock.recv(4096, )            # Data recieved from client
                except:
                    broadcast(sock, str.encode("\n") + str.encode(str(Users[addr]) + " has left the server"),
                            addr)
                    del Users[addr]
                    print("STATUS: Client [%s, %s] is offline" % addr)
                    sock.close()
                    CLIST.remove(sock)
                    continue

                if data:                                # Client send data
                    if data == "q" or data == "Q":      # If client quit
                        print("STATUS: Client [%s, %s] quit" % addr)
                        sock.close()                    # Close socket
                        CLIST.remove(sock)
                        # Remove from our list
                    elif '$$$' in data.decode():
                        username = data.decode().strip('$$$')
                        Users[addr] = username
                    elif '-$$' in data.decode():
                        version = data.decode().strip('-$$')
                        broadcast(sock, str.encode("\nThis user is connected through version " + version), 'ALL')
                    elif '$-$online' in data.decode():
                        broadcast(sock, str.encode("\nCurrent connected users:"), 'ALL')
                        
                        for x in range(0, len(CLIST)-1):
                            client = list(Users.values())[x]
                            client = str(client)
                            broadcast(sock, str.encode("\n") + str.encode(client), 'ALL')
                    else:
                        broadcast(sock, data, addr)                  
                
    server_socket.close()    
