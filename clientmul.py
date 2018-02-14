import socket
import _thread
import sys

pin ='ABC'
	
def recv_data():            #Receive data from other clients connected to server
    while 1:
        try:
            recv_data = client_socket.recv(4096)            
        except:
            #Process terminates
            print("Server closed connection")
            _thread.interrupt_main()     # Interrupt main when socket closes
            break
        if not recv_data:               # If recv has no data, close conection (error)
                print("Server closed connection")
                _thread.interrupt_main()
                break
        else:
            print(recv_data.decode())

def send_data():                # Send data from client to server"
    while 1:
        send_data = str(input("Message [Q for QUIT]: "))
        if send_data == "q" or send_data == "Q":
            client_socket.send(str.encode(send_data))
            _thread.interrupt_main()
            break
        else:
            CODES = '[' + user + '] - ' + send_data
            print(CODES)
            #full_msg = str.encode
            #client_socket.send(str.encode(user))
            client_socket.send(str.encode('\n'))
            client_socket.send(str.encode(CODES))
        
if __name__ == "__main__":

    print("||||| TCP Client ||||")
    ip = str(input("Enter server IP to connect: "))
    print("Connecting to ",ip,":6666")
    
    user = str(input("Enter username:"))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, 6666))

    print("Connected to ", ip,":6666")
    #usr = str(raw_input("Enter username: ")

    _thread.start_new_thread(recv_data,())
    _thread.start_new_thread(send_data,())

    try:
        while 1:
            continue
    except:
        print("Client program quits....")
        client_socket.close()       
