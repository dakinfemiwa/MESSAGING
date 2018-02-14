from tkinter import *
import tkinter.ttk
import json
import socket
import _thread
import sys

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)

def sendMessage(msgInput):
    entryBox.delete(0, END)
    sendData = msgInput
    CODES = USERNAME + ': ' + sendData
    clientSocket.send(str.encode('\n'))
    clientSocket.send(str.encode(CODES))
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END, '\n')
    LineNumber = float(ChatLog.index(END))-1.0
    ChatLog.insert(END, CODES)
    num = len(CODES)
    ChatLog.tag_add("You", LineNumber, LineNumber+num)
    ChatLog.tag_config("You", foreground=colourTheme, font=("Arial", 11, "bold"))
    ChatLog.config(state=DISABLED)
    ChatLog.see(END)

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

sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1, command=lambda:PressAction("<Return>"))
sendButton.place(relx=.86,rely=.855)

ChatLog = Text(Window, bd=0, bg="gray", height="13", width="91", font="Arial")
ChatLog.place(relx=.043,rely=.23)

# Receiving data from other clients.	
def Receive():
    while True:
        try:
            receiveData = clientSocket.recv(4096)            
        except:
            # When the server goes down.
            print("Server closed connection")
			# When the connection closes, interrupt the main thread.
            _thread.interrupt_main()
            break
		# If not data is returned, close the connection.	
        if not receiveData:
                print("Server closed connection")
                _thread.interrupt_main()
                break
        else:
            ChatLog.config(state=NORMAL)
            LineNumber = float(ChatLog.index(END))-1.0
            ChatLog.insert(END, receiveData)
            num = len(receiveData)
            ChatLog.tag_add("Them", LineNumber, LineNumber+num)
            ChatLog.tag_config("Them", foreground='#ffffff', font=("Arial", 11, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.see(END)

IP = '86.153.124.215'
PORT = 6666
# USERNAME = 'NO'

print("WELCOME: Ready to connect.")
print("INFO: Connecting to ", str(IP) + ":" + str(PORT))
final = ''
USERNAME = str(input("INPUT: Enter username: "))
for char in USERNAME.upper():
    final = final + char + ' '
JOIN_MSG = '[ ! ]  ' + final + '  J O I N E D  T H E  C H A T'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((IP, PORT))
    print("INFO: Connected to ", str(IP) + str(PORT))
    clientSocket.send(str.encode('\n'))
    clientSocket.send(str.encode(JOIN_MSG))

    _thread.start_new_thread(Receive, ())
    _thread.start_new_thread(Window.mainloop())
except:
    print('ERROR: Unable to connect to the requested server.')

try:
    while True:
        continue
except:
    print("INFO: Client program quits....")
    clientSocket.close()       
