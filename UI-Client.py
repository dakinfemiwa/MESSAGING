import socket
import _thread
import sys
	
def Receive():
    while 1:
        try:
            recv_data = client_socket.recv(4096)            
        except:
            print("INFO: Server closed connection")
            _thread.interrupt_main()
            break
        if not recv_data:
                print("INFO: Server closed connection")
                _thread.interrupt_main()
                break
        else:
            print(recv_data.decode())

def Send():
    while 1:
        SEND_DATA = str(input("INPUT: Enter your message: "))
        SEND_MESSAGE = user + ': ' + SEND_DATA
        clientSocket.send(str.encode('\n'))
        clientSocket.send(str.encode(SEND_MESSAGE))
        
if __name__ == "__main__":

    IP = '86.153.124.215'
    PORT = 6666

    print("INFO: Ready to connect")
    print("INFO: Connecting to ", str(IP) + ":" + str(PORT))
    
    USERNAME = str(input("INPUT: Enter username: "))

    ADMIN_MSG = 'An Admin has joined with elevated permissions'
    JOIN_MSG = USERNAME + ' has joined the server (through basic UI)'
    FINAL_VERSION = '-$$' + 'BASIC UI'

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((IP, PORT))

    print("INFO: Sending client information...")

    print("INFO: Connected to ", str(IP) + ':' + str(PORT))

    clientSocket.send(str.encode('\n'))
    clientSocket.send(str.encode(JOIN_MSG))
    clientSocket.send(str.encode('\n'))

    _thread.start_new_thread(Receive,())
    _thread.start_new_thread(Send,())

    try:
        while 1:
            continue
    except:
        print("INFO: Client program quit....")
        clientSocket.close()       
