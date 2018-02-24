from tkinter import *
import json
import socket
import _thread

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)

def sendMessage(msgInput):
    global username

    def Log(message):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        LineNumber = float(ChatLog.index(END)) - 1.0
        ChatLog.insert(END, message)
        num = len(message)
        ChatLog.tag_add(message, LineNumber, LineNumber + num)
        ChatLog.tag_config(message, foreground=colourTheme, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)

    COLOUR_COMMAND = 'The correct usage is .colour <colour>'
    entryBox.delete(0, END)
    sendData = msgInput
    colours = [
        'blue', 'green', 'purple', 'yellow', 'red', 'orange', 'white', 'gray'
    ]
    if True:
        if msgInput == '.help':
            Log(HELP_MESSAGE)

        elif msgInput == '.clear':
            ChatLog.config(state=NORMAL)
            ChatLog.delete(1.0, END)
            Log(CLEAR_COMMAND)

        elif '.name' in msgInput:
            if len(msgInput) < 7:
                Log(NAME_COMMAND)
            else:
                new_name = msgInput[6:]
                SEND_MESSAGE = username_old + ' has changed their name to ' + new_name
                clientSocket.send(str.encode('\n'))
                clientSocket.send(str.encode(SEND_MESSAGE))
                Window.after(500)
                clientSocket.send(str.encode('\n'))
                final2 = '$$$' + new_name
                username = new_name
                clientSocket.send(str.encode(final2))

        elif msgInput == '.about':
            Log(VERSION_MESSAGE)

        elif '.colour' in msgInput:
            if len(msgInput) < 9:
                Log(COLOUR_COMMAND)
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
                    elif colour == 'gray':
                        config['window']['theme'] = '#CCCCCC'

                    with open('config.json', 'w') as jsonConfig:
                        jsonConfig.write(json.dumps(config, indent=8))

                    COLOUR_COMMAND = 'Theme colour was changed; restart client'
                    Log(COLOUR_COMMAND)
                else:
                    COLOUR_COMMAND = 'You selected an invalid colour'
                    Log(COLOUR_COMMAND)

        elif len(msgInput) > 150:
            Log(SPAM_MESSAGE)

        elif msgInput == '.quit':
            Window.destroy()
            clientSocket.close()

        elif msgInput == '.online':
            clientSocket.send(str.encode('$-$online'))

        elif msgInput == '.fq':
            clientSocket.send(str.encode('$-$quit'))

        elif msgInput == '.ca':
            clientSocket.send(str.encode('$-$clear'))

        elif msgInput == '.admin':
            Log(ADMIN_MESSAGE)

        elif msgInput == '.message':
            if len(msgInput) < 10:
                Log(MESSAGE_COMMAND)
            else:
                targetUser = msgInput[9:]

        elif msgInput == '.kick':
            if len(msgInput) < 7:
                Log(KICK_COMMAND)
            else:
                targetUser = msgInput[6:]

        elif msgInput == '.update':
            Log(UPDATE_COMMAND)

        else:
            sendmsg = username + ': ' + sendData
            clientSocket.send(str.encode('\n'))
            clientSocket.send(str.encode(sendmsg))
    # except:
    # pass


def PressAction(event):
    entryBox.config(state=NORMAL)
    sendMessage(entryBox.get())


def DisableEntry(event):
    entryBox.config(state=DISABLED)

def permCheck(permission):
    QUERY = '---' + permission
    clientSocket.send(QUERY)


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
buttonText.set(' ➤ ')

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

sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1,
                    command=lambda: PressAction("<Return>"))
sendButton.place(relx=.86, rely=.855)

versionLabel = Label(Window, textvariable=versionText, font='Arial 11 bold', bg=windowBackground, fg=colourTheme)
versionLabel.place(relx=.08, rely=.17)

ChatLog = Text(Window, bd=1, bg="#141414", height="13", width="91", font="Arial")
ChatLog.place(relx=.043, rely=.23)


# Receiving data from other clients.
def Receive():
    def Log(MESSAGE, colour=colourTheme):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        LineNumber = float(ChatLog.index(END)) - 1.0
        ChatLog.insert(END, MESSAGE)
        num = len(MESSAGE)
        ChatLog.tag_add(MESSAGE, LineNumber, LineNumber + num)
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
                Log(CLEAR_MESSAGE_ADMIN, '#FFFFFF')
            else:
                ChatLog.config(state=NORMAL)
                LineNumber = float(ChatLog.index(END)) - 1.0
                ChatLog.insert(END, receiveData)
                num = len(receiveData)
                ChatLog.tag_add("Them", LineNumber, LineNumber + num)
                ChatLog.tag_config("Them", foreground='#ffffff', font=("courier new", 11, "bold"))
                ChatLog.config(state=DISABLED)
                ChatLog.see(END)


HELP_MESSAGE = '''.help - prints the help menu
.quit - exit the server gracefully
.name - change current username (unavailable)
.clear - clear chat (client-side)
.online - view online users
.colour - change theme colour
.update - update the client (unavailable)
.restart - restart the client
.about - view information about client
    '''

ADMIN_MESSAGE = '''.kick - kick a client off (unavailable)
.ca - clears messages for everyone
.fq - force quits all clients
.message - private message a user (unavailable)
'''

CLEAR_MESSAGE_ADMIN = 'Chat was cleared by an admin'
CLEAR_COMMAND = 'Chat was cleared successfully.'
NAME_COMMAND = 'This function is unavailable right now.'
SPAM_MESSAGE = 'Your message was not sent due to potential spam.'
MESSAGE_COMMAND = 'This function is unavailable right now.'
KICK_COMMAND = 'The correct usage for this command is .kick <user>'
UPDATE_COMMAND = 'No updates are available right now.'
VERSION_MESSAGE = 'Running GUI version of chat client [' + programVersion + ']'


# Admin permissions - to be handled in configuration file.
ADMIN_COMMAND_SYNTAX = 'admin.commands.show'
ADMIN_COMMAND_KICK = 'admin.commands.kick'
ADMIN_COMMAND_MESSAGE = 'admin.commands.message'
ADMIN_COMMAND_CLEARALL = 'admin.commands.clearall'
ADMIN_COMMAND_FORCEQUIT = 'admin.commands.forcequit'
ADMIN_COMMAND_RESTART = 'admin.commands.restart'
ADMIN_COMMAND_NICKNAME = 'admin.commands.nickname'
ADMIN_MESSAGE_JOIN = 'admin.messages.join'
ADMIN_MESSAGE_LEAVE = 'admin.messages.leave'

IP = '86.172.96.18'
PORT = 6666

print("WELCOME: Ready to connect.")
print("INFO: Connecting to ", str(IP) + ":" + str(PORT))

username = str(input("INPUT: Enter username: "))
username_old = username

# Admin permissions not sorted yet
ADMIN_MSG = 'An Admin has joined with elevated permissions'
JOIN_MSG = username + ' has joined the server'
FINAL_VERSION = '-$$' + programVersion
FINAL_NAME = '$$$' + username

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
    print("INFO: The client was forced to close.")
    clientSocket.close()

