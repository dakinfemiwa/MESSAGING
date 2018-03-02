from tkinter import *
import tkinter.ttk
import json
import socket
import _thread

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)

SUBVERSION = '2.99'


def Notify(type_n, msg, mode=None):
    global Notification

    def command():
        if mode is None:
            Notification.destroy()
        elif mode is 'UPDATE':
            Notification.destroy()
            UpdaterCore.Two()
        elif mode is 'UPDATE2':
            UpdaterCore.Three('OK')
        elif mode is 'UPDATE3':
            Notification.destroy()

    Notification = Tk()
    Notification.configure(bg='#141414')
    Notification.geometry('520x180+30+30')
    Notification.title('Notification')

    Notification.overrideredirect(1)
    Notification.attributes('-topmost', True)

    title_colour = ''
    title_type = StringVar()
    error_message = StringVar()
    error_message.set(msg)

    if type_n == 'ERROR':
        title_colour = '#F2473F'
        title_type.set('E R R O R')
    elif type_n == 'WARNING':
        title_colour = '#FF8C00'
        title_type.set('W A R N I N G')
    elif type_n == 'NORMAL':
        title_colour = '#CCCCCC'
        title_type.set('N O T I F I C A T I O N')

    line_text2 = StringVar()
    line_text2.set('___________________________________________')

    line_text3 = StringVar()
    line_text3.set('______________________________________')

    line_label2 = Label(Notification, textvariable=line_text2, font='Arial 15 bold', fg=title_colour, bg='#141414')
    line_label2.place(relx=.04, rely=.14)

    line_label3 = Label(Notification, textvariable=line_text3, font='Arial 19 bold', fg=title_colour, bg='#141414')
    line_label3.place(relx=.0, rely=.8)

    title_label2 = Label(Notification, textvariable=title_type, font='Arial 16 bold', bg=title_colour, fg='#141414')
    title_label2.place(relx=.046, rely=.09)

    error_label = Label(Notification, textvariable=error_message, font='system 11 bold', fg='#FFFFFF', bg='#141414',
                        justify=LEFT)
    error_label.place(relx=.045, rely=.4)

    ok_button = tkinter.ttk.Button(Notification, text='OK', command=lambda: (command()))
    ok_button.place(relx=.81, rely=.79)

    if mode is 'UPDATE2':
        ok_button.place_forget()
        command()

    Notification.mainloop()


class Updater:
    def Start(self):
        Notify('WARNING', 'UPDATING IS CURRENTLY UNSTABLE DOING SO MAY PREVENT\n'
                          'THE PROGRAM FROM RUNNING OR CRASHING DURING RUNTIME', 'UPDATE')

    def Two(self):
        Notify('NORMAL', 'SEARCHING FOR UPDATES THROUGH GITHUB\n'
                         'YOU ARE CURRENTLY RUNNING ON VERSION ' + SUBVERSION, 'UPDATE2')

    def Three(self, type='SOCK'):
        global Notification
        currentInfo = open('version.txt', 'r+')
        currentVersion = currentInfo.readlines()[0]
        currentInfo.close()

        try:

            import Updater
            Main = Updater.Update()
            latestVersion = Main.Download()
            Notification.destroy()

        except:
            pass

        Main = Updater.Update()
        latestVersion = Main.Download()

        def Log(chat):
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, '\n')
            line_number = float(ChatLog.index(END)) - 1.0
            ChatLog.insert(END, chat)
            num = len(chat)
            ChatLog.tag_add(chat, line_number, line_number + num)
            ChatLog.tag_config(chat, foreground=colourTheme, font=("courier new", 11, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.see(END)

        if float(latestVersion) > float(currentVersion):
            # Update is available
            if type is 'OK':
                Notify('NORMAL', 'AN UPDATE WAS FOUND - THE LATEST VERSION IS V ' + latestVersion, 'UPDATE3')
                Main.Switch()
            else:
                Log('An update was found, type .update to update the client.')

        else:
            # Update is not available
            if type is 'OK':
                Notify('NORMAL', 'NO UPDATES WERE FOUND - CURRENT VERSION V ' + currentVersion)
            else:
                pass


UpdaterCore = Updater()
# UpdaterCore.Update()


def sendMessage(message):
    global username, clientSocket

    def Log(chat):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        line_number = float(ChatLog.index(END)) - 1.0
        ChatLog.insert(END, chat)
        num = len(chat)
        ChatLog.tag_add(chat, line_number, line_number + num)
        ChatLog.tag_config(chat, foreground=colourTheme, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)

    entryBox.delete(0, END)
    send_data = message

    colours = [
        'blue', 'green', 'purple', 'yellow', 'red', 'orange', 'white', 'gray'
    ]

    try:
        if message == '.help':
            Log(HELP_MESSAGE)

        elif message == '.clear':
            ChatLog.config(state=NORMAL)
            ChatLog.delete(1.0, END)
            Log(CLEAR_COMMAND)

        elif '.name' in message:
            if len(message) < 7:
                Log(NAME_COMMAND)
            else:
                new_name = message[6:]
                updated_name = username_old + ' has changed their name to ' + new_name
                clientSocket.send(str.encode('\n'))
                clientSocket.send(str.encode(updated_name))
                Window.after(500)
                clientSocket.send(str.encode('\n'))
                second_name = '$$$' + new_name
                username = new_name
                clientSocket.send(str.encode(second_name))

        elif message == '.about':
            Log(VERSION_MESSAGE)

        elif '.colour' in message:
            if len(message) < 9:
                Log('The correct usage is .colour <colour>')
            else:
                colour = message[8:]
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

                    with open('config.json', 'w') as config_file:
                        config_file.write(json.dumps(config, indent=8))

                    Log('Theme colour was changed; restart client')
                else:
                    Log('You selected an invalid colour')

        elif len(message) > 150:
            Log(SPAM_MESSAGE)

        elif message == '.quit':
            Window.destroy()
            clientSocket.close()

        elif message == '.online':
            clientSocket.send(str.encode('$-$online'))

        elif message == '.fq':
            clientSocket.send(str.encode('$-$quit'))

        elif message == '.ca':
            clientSocket.send(str.encode('$-$clear'))

        elif message == '.admin':
            Log(ADMIN_MESSAGE)

        elif message == '.restart':
            clientSocket.send(str.encode('$-$restart'))
            clientSocket.close()
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Window.after(2000)
            clientSocket.connect((IP, PORT))
            print("INFO: Sending client information...")
            clientSocket.send(str.encode(FINAL_NAME))
            clientSocket.send(str.encode(FINAL_VERSION))
            print("INFO: Connected to ", str(IP) + ':' + str(PORT))
            clientSocket.send(str.encode('\n'))
            clientSocket.send(str.encode(JOIN_MSG))
            _thread.start_new_thread(Receive, ())
            _thread.start_new_thread(Window.mainloop())

        elif message == '.shutdown':
            clientSocket.send(str.encode('$-$shutdown'))
            try:
                Window.quit()
            except:
                pass
            try:
                Window.destroy()
            except:
                pass
            try:
                _thread.interrupt_main()
            except:
                pass
            try:
                clientSocket.close()
            except:
                pass
            exit(0)

        elif message == '.message':
            if len(message) < 10:
                Log(MESSAGE_COMMAND)
            else:
                target_user = message[9:]
                print(target_user)

        elif message == '.kick':
            if len(message) < 7:
                Log(KICK_COMMAND)
            else:
                target_user = message[6:]
                print(target_user)

        elif message == '.update':
            Window.destroy()
            # clientSocket.close()
            UpdaterCore.Start()
            Log(UPDATE_COMMAND)

        else:
            send_msg = username + ': ' + send_data
            clientSocket.send(str.encode('\n'))
            clientSocket.send(str.encode(send_msg))
    except:
        pass


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
Window.attributes('-topmost', True)

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
    def Log(message, colour=colourTheme):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n')
        line_number2 = float(ChatLog.index(END)) - 1.0
        ChatLog.insert(END, message)
        number = len(message)
        ChatLog.tag_add(message, line_number2, line_number2 + number)
        ChatLog.tag_config(message, foreground=colour, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)

    while True:
        try:
            receive_data = clientSocket.recv(4096)
        except:
            # When the server goes down.
            print("INFO: Server closed connection")
            _thread.interrupt_main()
            break
        if not receive_data:
            print("INFO: Server closed connection")
            _thread.interrupt_main()
            break
        else:
            if receive_data.decode() == '$-$quit':
                Window.destroy()
                clientSocket.close()
                _thread.interrupt_main()
            elif receive_data.decode() == '$-$clear':
                ChatLog.config(state=NORMAL)
                ChatLog.delete(1.0, END)
                Log(CLEAR_MESSAGE_ADMIN, '#FFFFFF')
            else:
                ChatLog.config(state=NORMAL)
                line_number = float(ChatLog.index(END)) - 1.0
                ChatLog.insert(END, receive_data)
                num = len(receive_data)
                ChatLog.tag_add("Them", line_number, line_number + num)
                ChatLog.tag_config("Them", foreground='#ffffff', font=("courier new", 11, "bold"))
                ChatLog.config(state=DISABLED)
                ChatLog.see(END)


HELP_MESSAGE = '''.help - prints the help menu
.quit - exit the server gracefully
.name - change current username
.clear - clear chat
.online - view online users
.colour - change theme colour
.update - update the client
.about - view information about client
    '''

ADMIN_MESSAGE = '''.kick - kick a client off (unavailable)
.ca - clears messages for everyone
.fq - force quits all clients
.message - private message a user (unavailable)
.restart - restarts the server
.shutdown - shuts down the server
'''

CLEAR_MESSAGE_ADMIN = 'Chat was cleared by an admin'
CLEAR_COMMAND = 'Chat was cleared successfully.'
NAME_COMMAND = 'The correct usage for this command is .name <username>'
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
ADMIN_COMMAND_NICKNAME = 'admin.commands.nickname'
ADMIN_COMMAND_RESTART = 'admin.commands.restart'
ADMIN_COMMAND_SHUTDOWN = 'admin.commands.shutdown'
ADMIN_MESSAGE_JOIN = 'admin.messages.join'
ADMIN_MESSAGE_LEAVE = 'admin.messages.leave'

USER_PERMISSIONS = []

IP = '86.153.124.149'
PORT = 6666

print("WELCOME: Ready to connect.")
print("INFO: Connecting to ", str(IP) + ":" + str(PORT))

username = str(input("INPUT: Enter username: "))
username_old = username

ADMIN_LEVEL = 1

if ADMIN_LEVEL == 1:
    USER_PERMISSIONS.extend((ADMIN_COMMAND_SYNTAX, ADMIN_COMMAND_CLEARALL, ADMIN_MESSAGE_JOIN, ADMIN_MESSAGE_LEAVE))
elif ADMIN_LEVEL == 2:
    USER_PERMISSIONS.extend((ADMIN_COMMAND_SYNTAX, ADMIN_COMMAND_CLEARALL, ADMIN_MESSAGE_JOIN, ADMIN_MESSAGE_LEAVE))
    USER_PERMISSIONS.extend((ADMIN_COMMAND_KICK, ADMIN_COMMAND_FORCEQUIT, ADMIN_COMMAND_MESSAGE))
elif ADMIN_LEVEL == 3:
    USER_PERMISSIONS.extend((ADMIN_COMMAND_SYNTAX, ADMIN_COMMAND_CLEARALL, ADMIN_MESSAGE_JOIN, ADMIN_MESSAGE_LEAVE))
    USER_PERMISSIONS.extend((ADMIN_COMMAND_KICK, ADMIN_COMMAND_FORCEQUIT, ADMIN_COMMAND_MESSAGE))
    USER_PERMISSIONS.extend((ADMIN_COMMAND_RESTART, ADMIN_COMMAND_SHUTDOWN))

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
    # clientSocket.send(str.encode(FINAL_VERSION))
    print("INFO: Connected to ", str(IP) + ':' + str(PORT))
    clientSocket.send(str.encode('\n'))
    clientSocket.send(str.encode(JOIN_MSG))
    # clientSocket.send(str.encode('\n'))
    # clientSocket.send(str.encode(ADMIN_MSG))
    Main = Updater()
    _thread.start_new_thread(Main.Three, ())

    _thread.start_new_thread(Receive, ())
    _thread.start_new_thread(Window.mainloop(), ())

except:
    print('ERROR: Unable to connect to the requested server.')
    exit(1)

try:
    while True:
        continue
except:
    print("INFO: The client was forced to close.")
    clientSocket.close()
