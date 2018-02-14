from tkinter import *
import tkinter.ttk
import json

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)

def sendMessage(thing):
    entryBox.delete(0, END)
    send_data = thing
    CODES = '[' + user + '] - ' + send_data
    print(CODES)
    #full_msg = str.encode
    #client_socket.send(str.encode(user))
    client_socket.send(str.encode('\n'))
    client_socket.send(str.encode(CODES))
    print()

def PressAction(event):
	entryBox.config(state=NORMAL)
	sendMessage(entryBox.get())
def DisableEntry(event):
	entryBox.config(state=DISABLED)

# Config incorporation.
colourTheme = config['window']['theme']
windowResolution = config['window']['resolution']
windowTitle = config['window']['title']
windowForeground = config['window']['foreground']
windowBackground = config['window']['background']

programVersion = config['information']['version']
programStage = config['information']['stage']

Window = Tk()
Window.configure(bg=windowBackground)
Window.geometry(windowResolution)
Window.title(windowTitle)

titleText = StringVar()
titleText.set('C H A T')

lineText = StringVar()
lineText.set('___________________________________________________________________________')

enterMessageText = StringVar()
enterMessageText.set('M E S S A G E: ')

buttonText = StringVar()
buttonText.set('S E N D')

connectingText = StringVar()
connectingText.set('Connecting to the chat server...')

bLabel = Label(Window, bg=windowBackground, fg=windowBackground).pack()

lineLabel = Label(Window, textvariable=lineText, font='Arial 15 bold', fg=colourTheme, bg=windowBackground)
lineLabel.place(relx=.04, rely=.14)

titleLabel = Label(Window, textvariable=titleText, font='Arial 20 bold', bg=windowBackground, fg=windowForeground)
titleLabel.place(relx=.04,rely=.09)

enterMessageLabel = Label(Window, textvariable=enterMessageText, font='Arial 13 bold', bg=windowBackground, fg=windowForeground)
enterMessageLabel.place(relx=.04,rely=.85)

entryBox = Entry(Window, width=100)
entryBox.place(relx=.18,rely=.855)

entryBox.bind("<Return>", DisableEntry)
entryBox.bind("<KeyRelease-Return>", PressAction)

connectingLabel = Label(Window, textvariable=connectingText, font='Arial 8 bold', fg=colourTheme, bg=windowBackground)
connectingLabel.place(relx=.040,rely=.225)

sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1)
sendButton.place(relx=.86,rely=.855)

ChatLog = Text(Window, bd=0, bg="gray", height="13", width="91", font="Arial")
ChatLog.place(relx=.043,rely=.23)

#ChatLog.insert

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
            _thread.interrupt_main()     # Interrupt main wen socket closes
            break
        if not recv_data:               # If recv has no data, close conection (error)
                print("Server closed connection")
                _thread.interrupt_main()
                break
        else:
            ChatLog.insert(recv_data.decode())
            print(recv_data.decode())

#Window.mainloop()
"""COLLECTS IP ADRESS"""
print("||||| TCP Client ||||")
#ip = '127.0.0.1'
ip = "92.238.60.233"
print("Connecting to ",ip,":6666")

user = 'NO'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, 6666))
Window.mainloop()
print("Connected to ", ip,":6666")
#usr = str(raw_input("Enter username: ")

_thread.start_new_thread(recv_data,())
_thread.start_new_thread(Window.mainloop())

try:
    while 1:
        continue
except:
    print("Client program quits....")
    client_socket.close()       
