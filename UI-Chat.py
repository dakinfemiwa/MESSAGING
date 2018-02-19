from tkinter import *
import tkinter.ttk
import json
import socket
import _thread
import sys
import os

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)

def sendMessage(msgInput):
    def Log(MESSAGE, colour=colourTheme):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        LineNumber = float(ChatLog.index(END))-1.0
        ChatLog.insert(END, MESSAGE)
        num = len(MESSAGE)
        ChatLog.tag_add(MESSAGE, LineNumber, LineNumber+num)
        ChatLog.tag_config(MESSAGE, foreground=colour, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)
    
    entryBox.delete(0, END)
    sendData = msgInput
    colours = [
        'blue',
        'green',
        'purple',
        'yellow',
        'red',
        'orange',
        'white'
        ]

    HELP_MSG = '''.help - prints the help menu
.quit - exit the server gracefully
.name - change current username (unavailable)
.clear - clear chat (client-side)
.online - view online users
.colour - change theme colour
.update - update the client (unavailable)
.restart - restart the client
    '''

    ADMIN_MSG = '''.kick - kick a client off (unavailable)
.clearall - clears messages for everyone
.fq - force quits all clients (unstable - causes server shut down)
.message - private message a user (unavailable)
'''
    try:
        if msgInput == '.help':
            Log(HELP_MSG, '#FFFFFF')
            
        elif msgInput == '.clear':
            ChatLog.config(state=NORMAL)
            ChatLog.delete(1.0, END)
            CLEAR_MSG = 'Chat was cleared successfully.'
            Log(CLEAR_MSG, '#FFFFFF')
            
        elif msgInput == '.name':
            UN_MSG = 'This function is unavailable right now.'
            Log(UN_MSG, '#FFFFFF')
            
        elif '.colour' in msgInput:
            if len(msgInput) < 9:
                CL_MSG = 'The correct usage is .colour <colour>'
                Log(CL_MSG, '#FFFFFF')
            else:
                colour = msgInput[8:]
                if colour in colours:
                    if colour == 'white':
                        config['window']['theme'] = '#FFFFFF'
                    elif colour == 'red':
                        config['window']['theme'] = '#FF0000'
                    elif colour == 'blue':
                        config['window']['theme'] = '#00BFFF'
                    elif colour == 'green':
                        config['window']['theme'] = '#7CFC00'
                    elif colour == 'yellow':
                        config['window']['theme'] = '#FFFF00'
                    elif colour == 'purple':
                        config['window']['theme'] = '#8A2BE2'
                    elif colour == 'orange':
                        config['window']['theme'] = '#FF8C00'

                    with open('config.json', 'w') as jsonConfig:
                        jsonConfig.write(json.dumps(config, indent=8))
                    
                    CL_MSG = 'Theme colour was changed; restart client'
<<<<<<< HEAD
                    Log(CL_MSG, '#FFFFFF')
                    
=======
                    Log(CL_MSG, '#FFFFFF')                    
>>>>>>> 8248c72b4e2ac8c1a4e8c25f62fac8c04ab6c4df
                else:
                    CL_MSG = 'You selected an invalid colour'
                    Log(CL_MSG, '#FFFFFF')
            
        elif len(msgInput) > 150:
            SPAM_MSG = 'Your message was not sent due to potential spam.'
            Log(SPAM_MSG, '#FFFFFF')
            
        elif msgInput == '.quit':
            Window.destroy()
            clientSocket.close()
            
        elif msgInput == '.online':
            clientSocket.send(str.encode('$-$online'))
            
        elif msgInput == '.admin':
            Log(ADMIN_MSG)
            
        elif msgInput == '.fq':
            clientSocket.send(str.encode('$-$quit'))

        elif msgInput == '.clearall':
            CLALL_MSG = 'Chat has been cleared for all users by ' + USERNAME
            clientSocket.send(str.encode('$-$clear'))
            
        elif msgInput == '.message':
            MSG_MSG = 'This function is unavailable right now.'
            Log(MSG_MSG)
            
        elif msgInput == '.kick':
            KICK_MSG = 'This function is unavailable right now.'
            Log(KICK_MSG)
            
        elif msgInput == '.update':
            UPDT_MSG = 'No updates are available right now.'
            Log(UPDT_MSG)
            
        else:
            SEND_MESSAGE = USERNAME + ': ' + sendData
            clientSocket.send(str.encode('\n'))
            clientSocket.send(str.encode(SEND_MESSAGE))
    except:
        pass

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

versionText = StringVar()
versionText.set('V E R S I O N  ' + programVersion)

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

entryBox.insert(END, '.help')

connectingLabel = Label(Window, textvariable=connectingText, font='Arial 8 bold', fg=colourTheme, bg=windowBackground)
connectingLabel.place(relx=.040,rely=.225)

sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1, command=lambda:PressAction("<Return>"))
sendButton.place(relx=.86,rely=.855)

verionLabel = Label(Window, textvariable=versionText, font='Arial 11 bold', bg=windowBackground, fg=colourTheme)
verionLabel.place(relx=.08, rely=.17)

ChatLog = Text(Window, bd=1, bg="#141414", height="13", width="91", font="Arial")
ChatLog.place(relx=.043,rely=.23)

# Receiving data from other clients.	
def Receive():
    def Log(MESSAGE, colour=colourTheme):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        LineNumber = float(ChatLog.index(END))-1.0
        ChatLog.insert(END, MESSAGE)
        num = len(MESSAGE)
        ChatLog.tag_add(MESSAGE, LineNumber, LineNumber+num)
        ChatLog.tag_config(MESSAGE, foreground=colour, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)
    while True:
        try:
            receiveData = clientSocket.recv(4096)            
        except:
            # When the server goes down.
            print("INFO: Server closed connection")
            _thread.interrupt_main()
            break	
        if not receiveData:
            print("INFO: Server closed connection")
            _thread.interrupt_main()
            break
        else:
            if receiveData.decode() == '$-$quit':
                Window.destroy()
                clientSocket.close()
                _thread.interrupt_main()
            elif receiveData.decode() == '$-$clear':
                ChatLog.config(state=NORMAL)
                ChatLog.delete(1.0, END)
                CLEAR_MSG = 'Chat was cleared by an admin'
                Log(CLEAR_MSG, '#FFFFFF')
            else:
                ChatLog.config(state=NORMAL)
                LineNumber = float(ChatLog.index(END))-1.0
                ChatLog.insert(END, receiveData)
                num = len(receiveData)
                ChatLog.tag_add("Them", LineNumber, LineNumber+num)
                ChatLog.tag_config("Them", foreground='#ffffff', font=("courier new", 11, "bold"))
                ChatLog.config(state=DISABLED)
                ChatLog.see(END)

IP = '86.153.124.215'
PORT = 6666

print("WELCOME: Ready to connect.")
print("INFO: Connecting to ", str(IP) + ":" + str(PORT))

USERNAME = str(input("INPUT: Enter username: "))

ADMIN_MSG = 'An Admin has joined with elevated permissions'
JOIN_MSG = USERNAME + ' has joined the server'
FINAL_VERSION = '-$$' + programVersion
FINAL_NAME = '$$$' + USERNAME

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((IP, PORT))
    print("INFO: Sending client information...")
    clientSocket.send(str.encode(FINAL_NAME))
    clientSocket.send(str.encode(FINAL_VERSION))
    print("INFO: Connected to ", str(IP) + ':' + str(PORT))
    clientSocket.send(str.encode('\n'))
    clientSocket.send(str.encode(JOIN_MSG))
    # clientSocket.send(str.encode('\n'))
    # clientSocket.send(str.encode(ADMIN_MSG))

    _thread.start_new_thread(Receive, ())
    _thread.start_new_thread(Window.mainloop())
except:
    print('ERROR: Unable to connect to the requested server.')

try:
    while True:
        continue
except:
    print("INFO: Client program quit....")
    clientSocket.close()       
