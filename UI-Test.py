from tkinter import *
import tkinter.ttk
import json
import socket
import _thread
import sys

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)


def sendMessage(msgInput):
    def add(MESSAGE, colour=colourTheme):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        LineNumber = float(ChatLog.index(END)) - 1.0
        ChatLog.insert(END, MESSAGE)
        num = len(MESSAGE)
        ChatLog.tag_add(MESSAGE, LineNumber, LineNumber + num)
        ChatLog.tag_config(MESSAGE, foreground=colour, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)

    entryBox.delete(0, END)
    sendData = msgInput

    if msgInput == '.help':
        HELP_MSG = '''.help - prints the help menu
.quit - exit the server gracefully
.name - change current username (unavailable)
.clear - clear chat (client-side)
.online - view online users
'''

        ADMIN_MSG = '''.kick - kick a client off
.clearall - clears messages for everyone
.fq - force quits all clients
.status - view server status
.message - private message a user
'''
        add(HELP_MSG, '#FFFFFF')
    elif msgInput == '.clear':
        ChatLog.config(state=NORMAL)
        ChatLog.delete(1.0, END)
        CLEAR_MSG = 'Chat was cleared successfully.'
        add(CLEAR_MSG, '#FFFFFF')
    elif msgInput == '.name':
        username = input("Enter username")
        UN_MSG = USERNAME + " has changed username to " + username
        add(UN_MSG, '#FFFFFF')
        USERNAME = username2;
    elif msgInput == '.quit':
        Window.destroy()
        clientSocket.close()
    elif msgInput == '.colour':
        CL_MSG = 'Open UI-Settings to change the theme.'
        add(CL_MSG, '#FFFFFF')
    elif len(msgInput) > 150:
        SPAM_MSG = 'Your message was not sent due to potential spam.'
        add(SPAM_MSG, '#FFFFFF')
    elif msgInput == '.online':
        clientSocket.send(str.encode('$-$online'))
    else:
        CODES = USERNAME + ': ' + sendData
        clientSocket.send(str.encode('\n'))
        clientSocket.send(str.encode(CODES))


def PressAction(event):
    entryBox.config(state=NORMAL)
    sendMessage(entryBox.get())


def DisableEntry(event):
    entryBox.config(state=DISABLED)


# Receiving data from other clients.
def Receive():
    while True:
        try:
            receiveData = clientSocket.recv(4096)
        except:
            # When the server goes down.
            print("INFO: Server closed connection")
            # When the connection closes, interrupt the main thread.
            _thread.interrupt_main()
            break
        # If not data is returned, close the connection.
        if not receiveData:
            print("INFO: Server closed connection")
            _thread.interrupt_main()
            break
        else:
            ChatLog.config(state=NORMAL)
            LineNumber = float(ChatLog.index(END)) - 1.0
            ChatLog.insert(END, receiveData)
            num = len(receiveData)
            ChatLog.tag_add("Them", LineNumber, LineNumber + num)
            ChatLog.tag_config("Them", foreground='#ffffff', font=("courier new", 11, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.see(END)


IP = '86.153.124.215'
PORT = 6666
# USERNAME = 'NO'

print("WELCOME: Ready to connect.")
print("INFO: Connecting to ", str(IP) + ":" + str(PORT))
FINAL_NAME = ''


def enterUsername():
    global userEntry, item, usernameUI
    usernameUI = Tk()
    usernameUI.title("Welcome")
    usernameUI.geometry("300x200")
    usernameUI.config(bg="#AAAAAA")
    gap = Label(usernameUI, bg="#AAAAAA").pack()
    userText = Label(usernameUI, text="Enter username", bg="#AAAAAA").pack()
    gap = Label(usernameUI, bg="#AAAAAA").pack()
    item = StringVar()
    userEntry = Entry(usernameUI, textvariable=item, bg="#AAAAAA").pack()
    gap = Label(usernameUI, bg="#AAAAAA").pack()
    userButton = Button(usernameUI, text="Choose Username", command=convertUser, bg="#FFFFFF").pack()


def convertUser():
    global USERNAME
    USERNAME = item.get()
    print(USERNAME)
    usernameUI.destroy()
    continueGOING()


enterUsername()


def continueGOING():
    GUI()
    global clientSocket
    for char in USERNAME.upper():
        FINAL_NAME = '$$$' + USERNAME

    ADMIN_MSG = 'An Admin has joined with elevated permissions'
    JOIN_MSG = USERNAME + ' has joined the server'

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((IP, PORT))
        clientSocket.send(str.encode(FINAL_NAME))
        print("INFO: Sending client information...")
        print("INFO: Connected to ", str(IP) + ':' + str(PORT))
        clientSocket.send(str.encode('\n'))
        clientSocket.send(str.encode(JOIN_MSG))
        clientSocket.send(str.encode('\n'))
        # clientSocket.send(str.encode('$$$Latest'))
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
        print("INFO: Client program quits....")
        clientSocket.close()


def GUI():
    global ChatLog, entryBox
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
    titleLabel.place(relx=.04, rely=.09)

    enterMessageLabel = Label(Window, textvariable=enterMessageText, font='Arial 13 bold', bg=windowBackground,
                              fg=windowForeground)
    enterMessageLabel.place(relx=.04, rely=.85)

    entryBox = Entry(Window, width=100)
    entryBox.place(relx=.18, rely=.855)

    entryBox.bind("<Return>", DisableEntry)
    entryBox.bind("<KeyRelease-Return>", PressAction)

    entryBox.insert(END, '.help')

    connectingLabel = Label(Window, textvariable=connectingText, font='Arial 8 bold', fg=colourTheme,
                            bg=windowBackground)
    connectingLabel.place(relx=.040, rely=.225)

    sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1,
                        command=lambda: PressAction("<Return>"))
    sendButton.place(relx=.86, rely=.855)

    verionLabel = Label(Window, textvariable=versionText, font='Arial 11 bold', bg=windowBackground, fg=colourTheme)
    verionLabel.place(relx=.08, rely=.17)

    ChatLog = Text(Window, bd=1, bg="#141414", height="13", width="91", font="Arial")
    ChatLog.place(relx=.043, rely=.23)