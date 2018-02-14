import sys
import socket
import threading
import select
import string
	
def broadcast (sock, message, usr):
    print(message)
    print(message.decode())
    for socket in CLIST:
        if socket != server_socket and socket != sock:
            print('From: ', usr)
            print('Message recived : ' , message)
            print('Broadcasting...\n')
            socket.send(message)

if __name__ == "__main__":

    CLIST = []
    
    print('Chat server - BETA')
    port = str(input("Enter IP to bind server: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((port, 6666))
    server_socket.listen(10)
 
    CLIST.append(server_socket)   # Add socket

    while 1:
        # Get list of ready to be read with select
        read_sockets,write_sockets,error_sockets = select.select(CLIST,[],[])

        for sock in read_sockets:

            if sock == server_socket: 
                sockfd, addr = server_socket.accept()   # New connection recieved 
                CLIST.append(sockfd)                    # Append the new connection
                print("Client [%s, %s] connected" % addr)
                #broadcast(sockfd, "New client connected ",addr)

            else:
                try:
                    data = sock.recv(4096, )            # Data recieved from client
                except:
                    broadcast(sock, "Client (%s, %s) is offline" % addr,
                            addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CLIST.remove(sock)
                    continue

                if data:                                # Client send data
                    if data == "q" or data == "Q":      # If client quit
                        #broadcast(sock, "Client (%s, %s) quit" % addr, addr)
                        print("Client (%s, %s) quit" % addr)
                        sock.close()                    # Close socket
                        CLIST.remove(sock)              # Remove from our list
                    else:
                        broadcast(sock, data, addr)                       
                
    server_socket.close()    
