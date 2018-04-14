from tkinter import *
import tkinter.ttk
import json
import socket
import _thread
import Updater
import urllib.request


class Client:
    @staticmethod
    def configure():
        global config, colourTheme, windowBackground, windowForeground
        global windowTitle, programVersion, programStage, windowResolution

        with open('config.json') as jsonConfig:
            config = json.load(jsonConfig)

        # Config incorporation.
        colourTheme = config['window']['theme']
        windowResolution = config['window']['resolution']
        windowTitle = config['window']['title']
        windowForeground = config['window']['foreground']
        windowBackground = config['window']['background']

        programVersion = config['information']['version']
        programStage = config['information']['stage']

    @staticmethod
    def connect():

        global clientSocket, username

        print("WELCOME: Ready to connect.")
        print("INFO: Connecting to ", str(IP) + ":" + str(PORT))

        username = str(input("INPUT: Enter username: "))

        if ADMIN_LEVEL > 0:
            USER_PERMISSIONS.extend((ADMIN_COMMAND_SYNTAX, ADMIN_MESSAGE_JOIN, ADMIN_MESSAGE_LEAVE))

        join_message = username + ' has joined the server'
        final_name = '$$$' + username

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            clientSocket.connect((IP, PORT))
            print("INFO: Sending client information...")
            clientSocket.send(str.encode(final_name))
            print("INFO: Connected to ", str(IP) + ':' + str(PORT))
            clientSocket.send(str.encode(join_message))

            _thread.start_new_thread(Manager.search, ())

            _thread.start_new_thread(Client.receive, ())
            _thread.start_new_thread(MainWindow.mainloop(), ())

        except:
            print('ERROR: Unable to connect to the requested server.')
            print('INFO: Server is most likely offline, check with control panel.')
            exit(1)

        try:
            while True:
                continue
        except:
            print("INFO: The client was forced to close.")
            clientSocket.close()

    @staticmethod
    def close(self):
        pass

    @staticmethod
    def send(message):
        try:
            if message[0] == '.':
                Client.command(message)
            else:
                entryBox.delete(0, END)
                send_msg = username + ': ' + message
                clientSocket.send(str.encode(send_msg))
        except TypeError:
            pass
        except IndexError:
            pass

    @staticmethod
    def receive():

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
                    MainWindow.destroy()
                    clientSocket.close()
                    _thread.interrupt_main()
                elif receive_data.decode() == '$-$clear':
                    ChatLog.config(state=NORMAL)
                    ChatLog.delete(1.0, END)
                    Window.show(CLEAR_MESSAGE_ADMIN)
                elif '$-$play' in receive_data.decode():
                    #data_original = receive_data.decode()
                    #data_original = data_original[8:]
                    urllib.request.urlretrieve(
                        'https://raw.githubusercontent.com/dakinfemiwa/MESSAGING/unstable/song.mp3',
                        'song.mp3')
                    import os
                    os.startfile('song.mp3')

                else:
                    Window.show(receive_data.decode())

    @staticmethod
    def command(command):
        global username, clientSocket

        entryBox.delete(0, END)

        colours = [
            'blue', 'green', 'purple', 'yellow', 'red', 'orange', 'white', 'gray'
        ]

        try:
            if command == '.help':
                Window.show(HELP_MESSAGE)

            elif command == '.clear':
                ChatLog.config(state=NORMAL)
                ChatLog.delete(1.0, END)
                Window.show(CLEAR_COMMAND)

            elif '.name' in command:
                if len(command) < 7:
                    Window.show(NAME_COMMAND)
                else:
                    new_name = command[6:]
                    updated_name = username + ' has changed their name to ' + new_name
                    clientSocket.send(str.encode('\n'))
                    clientSocket.send(str.encode(updated_name))
                    MainWindow.after(500)
                    clientSocket.send(str.encode('\n'))
                    second_name = '$$$' + new_name
                    username = new_name
                    clientSocket.send(str.encode(second_name))

            elif command == '.about':
                Window.show(VERSION_MESSAGE)

            elif '.colour' in command:
                if len(command) < 9:
                    Window.show('The correct usage is .colour <colour>')
                else:
                    colour = command[8:]
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

                        Window.show('Theme colour was changed; restart client')
                    else:
                        Window.show('You selected an invalid colour')

            elif len(command) > 150:
                Window.show(SPAM_MESSAGE)

            elif command == '.quit':
                MainWindow.destroy()
                clientSocket.close()

            elif command == '.online':
                clientSocket.send(str.encode('$-$online'))

            elif command == '.fq':
                if has('admin.commands.forcequit'):
                    clientSocket.send(str.encode('$-$quit'))
                else:
                    Window.show(INSUFFICIENT_PERMISSIONS)

            elif command == '.ca':
                if has('admin.commands.clearall'):
                    clientSocket.send(str.encode('$-$clear'))
                else:
                    Window.show(INSUFFICIENT_PERMISSIONS)

            elif command == '.admin':
                if has('admin.commands.show'):
                    Window.show(ADMIN_MESSAGE)
                else:
                    Window.show(INSUFFICIENT_PERMISSIONS)

            elif '.ghost' in command:
                if has('admin.commands.ghost'):
                    if len(command) < 8:
                        Window.show(GHOST_COMMAND)
                    else:
                        target_user = command[7:]
                        final_string = '_-$' + target_user
                        clientSocket.send(str.encode(final_string))
                else:
                    Window.show(INSUFFICIENT_PERMISSIONS)

            elif command == '.restart':
                clientSocket.send(str.encode('$-$restart'))

            elif command == '.shutdown':
                clientSocket.send(str.encode('$-$shutdown'))

            elif command == '.message':
                if len(command) < 10:
                    Window.show(MESSAGE_COMMAND)
                else:
                    target_user = command[9:]

            elif '.kick' in command:
                if len(command) < 7:
                    Window.show(KICK_COMMAND)
                else:
                    target_user = command[6:]
                    final_string = '$$-' + target_user
                    clientSocket.send(str.encode(final_string))

            elif command == '.update':
                MainWindow.destroy()
                # clientSocket.close()
                Manager.search('FORCED')

            else:
                Window.show('That is an invalid command')

        except:
            pass

    def disconnect(self):
        pass


class Window:
    @staticmethod
    def draw():
        global ChatLog, MainWindow, entryBox

        def press(event):
            entryBox.config(state=NORMAL)
            Client.send(entryBox.get())

        def disable(event):
            entryBox.config(state=DISABLED)

        MainWindow = Tk()
        MainWindow.configure(bg=windowBackground)
        MainWindow.geometry(windowResolution)
        MainWindow.title(windowTitle)
        MainWindow.attributes('-topmost', True)

        titleText = StringVar()
        titleText.set('C H A T')

        lineText = StringVar()
        lineText.set('___________________________________________________________________________')

        enterMessageText = StringVar()
        enterMessageText.set('M E S S A G E: ')

        buttonText = StringVar()
        buttonText.set(' ➤ ')

        settingsText = StringVar()
        settingsText.set('⚙️')

        versionText = StringVar()
        versionText.set('V E R S I O N  ' + programVersion)

        lineLabel = Label(MainWindow, textvariable=lineText, font='Arial 15 bold', fg=colourTheme, bg=windowBackground)
        lineLabel.place(relx=.04, rely=.14)

        titleLabel = Label(MainWindow, textvariable=titleText, font='Arial 20 bold', bg=windowBackground,
                           fg=windowForeground)
        titleLabel.place(relx=.04, rely=.09)

        enterMessageLabel = Label(MainWindow, textvariable=enterMessageText, font='Arial 13 bold', bg=windowBackground,
                                  fg=windowForeground)
        enterMessageLabel.place(relx=.04, rely=.85)

        entryBox = Entry(MainWindow, width=100)
        entryBox.place(relx=.18, rely=.855)

        entryBox.bind("<Return>", disable)
        entryBox.bind("<KeyRelease-Return>", press)

        entryBox.insert(END, '.help')

        sendButton = Button(MainWindow, textvariable=buttonText, font='Arial 7 bold', width=7, height=1,
                            command=lambda: press("<Return>"))
        sendButton.place(relx=.86, rely=.855)

        settingsButton = Button(MainWindow, textvariable=settingsText, font='Arial 7 bold', width=3, height=1,
                                command=lambda: Window.settings())
        settingsButton.place(relx=.927, rely=.855)

        versionLabel = Label(MainWindow, textvariable=versionText, font='Arial 11 bold', bg=windowBackground,
                             fg=colourTheme)
        versionLabel.place(relx=.08, rely=.17)

        ChatLog = Text(MainWindow, bd=1, bg="#141414", height="13", width="91", font="Arial")
        ChatLog.place(relx=.043, rely=.23)

    @staticmethod
    def settings():
        global Settings

        MainWindow.destroy()

        Settings = Tk()
        Settings.configure(bg='#141414')
        Settings.geometry(windowResolution)
        Settings.title('Settings')

        Settings.attributes('-topmost', True)

        title_type = StringVar()
        info_message = StringVar()
        lines = StringVar()

        info_message.set('CHANGE HOW THE GUI LOOKS [FONT / COLOUR / THEME]')
        lines.set('_' * 75)

        title_colour = '#00FF00'
        title_type.set('S E T T I N G S')

        title_line = Label(Settings, textvariable=lines, font='Arial 15 bold', fg=title_colour, bg='#141414')
        title_line.place(relx=.04, rely=.14)

        deep_line = Label(Settings, textvariable=lines, font='Arial 15 bold', fg=title_colour, bg='#141414')
        deep_line.place(relx=.04, rely=.8)

        main_label = Label(Settings, textvariable=title_type, font='Arial 16 bold', fg='#141414', bg=title_colour)
        main_label.place(relx=.046, rely=.09)

        info_label = Label(Settings, textvariable=info_message, font='verdana 10 bold italic', fg='#00FF00', bg='#141414',
                        justify=LEFT)
        # info_label.place(relx=.045, rely=.9)
        info_label.place(relx=.1, rely=.165)

    def close(self):
        pass

    @staticmethod
    def alert(mode, message, frame=None):
        global Notification

        def execute():
            if frame is None:
                Notification.destroy()
            elif frame is 'UPDATE':
                Notification.destroy()
                Manager.search('FORCED')
            elif frame is 'UPDATE2':
                Notification.destroy()

        Notification = Tk()
        Notification.configure(bg='#141414')
        Notification.geometry('520x180+30+30')
        Notification.title('Notification')

        Notification.overrideredirect(1)
        Notification.attributes('-topmost', True)

        title_type = StringVar()
        error_message = StringVar()
        title_colour = StringVar()
        lines = StringVar()

        error_message.set(message)
        lines.set('_' * 43)

        if mode == 'ERROR':
            title_colour = '#F2473F'
            title_type.set('E R R O R')
        elif mode == 'WARNING':
            title_colour = '#FF8C00'
            title_type.set('W A R N I N G')
        elif mode == 'NORMAL':
            title_colour = '#CCCCCC'
            title_type.set('N O T I F I C A T I O N')

        title_line = Label(Notification, textvariable=lines, font='Arial 15 bold', fg=title_colour, bg='#141414')
        title_line.place(relx=.04, rely=.14)

        deep_line = Label(Notification, textvariable=lines, font='Arial 19 bold', fg=title_colour, bg='#141414')
        deep_line.place(relx=.0, rely=.8)

        main_label = Label(Notification, textvariable=title_type, font='Arial 16 bold', fg='#141414', bg=title_colour)
        main_label.place(relx=.046, rely=.09)

        error_label = Label(Notification, textvariable=error_message, font='system 11 bold', fg='#FFFFFF', bg='#141414',
                            justify=LEFT)
        error_label.place(relx=.045, rely=.4)

        button = tkinter.ttk.Button(Notification, text='OK', command=lambda: (execute()))
        button.place(relx=.81, rely=.79)

        if frame is 'UPDATE2':
            button.place_forget()
            execute()

        Notification.mainloop()

    @staticmethod
    def show(message):
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, '\n' + message)
        ChatLog.tag_add(message, float(ChatLog.index(END)) - 1.0, (float(ChatLog.index(END)) - 1.0) + len(message))
        ChatLog.tag_config(message, foreground=colourTheme, font=("courier new", 11, "bold"))
        ChatLog.config(state=DISABLED)
        ChatLog.see(END)


class Manager:
    @staticmethod
    def warn():
        Window.alert('WARNING', 'UPDATING IS CURRENTLY UNSTABLE DOING SO MAY PREVENT\n'
                                'THE PROGRAM FROM RUNNING OR CRASHING DURING RUNTIME', 'UPDATE')

    @staticmethod
    def search(frame='AUTO'):
        global Notification

        info_file = open('version.txt', 'r+')
        current_version = info_file.readlines()[0]
        info_file.close()
        try:
            if config['settings']['auth'] == 'true':
                print('INFO: Permissions support ON')
                if ADMIN_LEVEL > 1:
                    USER_PERMISSIONS.extend((ADMIN_COMMAND_KICK, ADMIN_COMMAND_CLEARALL, ADMIN_COMMAND_MESSAGE))
                if ADMIN_LEVEL > 2:
                    USER_PERMISSIONS.extend((ADMIN_COMMAND_RESTART, ADMIN_COMMAND_SHUTDOWN, ADMIN_COMMAND_FORCEQUIT, ADMIN_COMMAND_GHOST))
        except:
            pass

        latest_version = External.Download()
        # Update is available
        if float(latest_version) > float(current_version):
            if frame is 'FORCED':
                Window.alert('NORMAL', 'AN UPDATE WAS FOUND - THE LATEST VERSION IS V ' + latest_version, 'UPDATE2')
                External.Switch()
            else:
                Window.show('An update was found, type .update to update the client.')

        # Update is not available
        else:
            if frame is 'FORCED':
                Window.alert('NORMAL', 'NO UPDATES WERE FOUND - CURRENT VERSION V ' + current_version)


Manager = Manager()
External = Updater.Update()
Client.configure()
Window.draw()


def has(permission):
    if permission in USER_PERMISSIONS:
        return True
    else:
        return False


HELP_MESSAGE = '''.help - prints the help menu
.quit - exit the server gracefully
.name - change current username
.clear - clear chat
.online - view online users
.colour - change theme colour
.update - update the client
.about - view information about client
'''

ADMIN_MESSAGE = '''.kick - kick a client off
.ca - clears messages for everyone
.fq - force quits all clients
.message - private message a user (unavailable)
.restart - restarts the server
.shutdown - shuts down the server
'''

CLEAR_MESSAGE_ADMIN = 'Chat was cleared by an admin'
CLEAR_COMMAND = 'Chat was cleared successfully.'
NAME_COMMAND = 'The correct usage for this command is .name <username>'
GHOST_COMMAND = 'The correct usage for this command is .ghost <user>'
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
ADMIN_COMMAND_GHOST = '.admin.commands.ghost'
ADMIN_MESSAGE_JOIN = 'admin.messages.join'
ADMIN_MESSAGE_LEAVE = 'admin.messages.leave'

INSUFFICIENT_PERMISSIONS = 'You do not have the permission to execute this command'
USER_PERMISSIONS = []

IP = '86.153.124.99'
PORT = 6666
ADMIN_LEVEL = 3

Client.connect()
