from tkinter import *
import socket
import ast


class Console:
    def __init__(self):
        self.WINDOW_RESOLUTION = '600x250'
        self.WINDOW_BACKGROUND = '#353B48'
        self.WINDOW_FOREGROUND = '#FFFFFF'
        self.WINDOW_SPECIAL_FOREGROUND = '#2F3640'
        self.WINDOW_SPECIAL_BACKGROUND = '#DCDDE1'
        self.WINDOW_HIGHLIGHT_BACKGROUND = '#535C68'
        # self.WINDOW_CHAT_BACKGROUND = '#BDC3C7'
        self.WINDOW_CHAT_BACKGROUND = '#f39c12'
        self.WINDOW_TITLE = 'Console'
        self.WINDOW_TITLE_FONT = ('Arial', 16, 'bold')
        self.WINDOW_SUB_FONT = ('Arial', 11, 'bold')
        self.WINDOW_BUTTON_FONT = ('Arial', 12, 'bold')
        self.WINDOW_THEME = '#16A085'
        self.WINDOW_ERROR = '#E74C3C'

        self.CONFIG_LOGGER = 'True'
        self.CONFIG_UPDATER = 'False'
        self.CONFIG_ADVANCED = 'False'
        self.CONFIG_VERSION = '1.0'

        self.COMMAND_HELP = '.HELP'
        self.COMMAND_LOG = '.LOG'
        self.COMMAND_GAME = '.GAME'
        self.COMMAND_CLEAR = '.CLEAR'
        self.COMMAND_SHUTDOWN = '.SHUTDOWN'
        self.COMMAND_CONNECT = '.CONNECT'
        self.COMMAND_DISCONNECT = '.DISCONNECT'

        self.MESSAGE_HELP = '.LOG <on/off> - view server logs\n' \
                            '.GAME <player> <view/edit/delete> - manage players\n' \
                            '.CONNECT [address] [port] - connect to server\n' \
                            '.DISCONNECT - disconnect from server\n' \
                            '.SHUTDOWN - server shutdown\n' \
                            '.CLEAR - clear console log' \

        self.MESSAGE_LOG = 'LOG COMMAND:\nPrint server logs in console <on/off>'
        self.MESSAGE_LOG_ON = 'LOG COMMAND:\nTurned server logging on successfully.'
        self.MESSAGE_LOG_OFF = 'LOG COMMAND:\nTurned server logging off successfully.'
        self.MESSAGE_LOG_FAIL = 'LOG COMMAND:\nInvalid arguments <on/off>'

        self.MESSAGE_GAME = 'GAME COMMAND:\nManage registered players <player> <view/edit/delete>'
        self.MESSAGE_GAME_NEW = 'GAME COMMAND:\nEnter a new value for this field:'
        self.MESSAGE_GAME_ENTER_NUM = 'GAME COMMAND:\nEnter number of the value you want to edit:'
        self.MESSAGE_GAME_EDIT_SUCCESS = 'GAME COMMAND:\nSuccessfully updated player records.'
        self.MESSAGE_GAME_EDIT_FAIL = 'GAME COMMAND:\nCould not update player records.'

        self.MESSAGE_SHUTDOWN_WARNING = 'SHUTDOWN COMMAND:\nAre you sure you want to shutdown the server? <Y/N>'
        self.MESSAGE_SHUTDOWN_DONE = 'SHUTDOWN COMMAND:\nSent shutdown command to server successfully.'
        self.MESSAGE_SHUTDOWN_CANCELLED = 'SHUTDOWN COMMAND:\nCancelled server shutdown command successfully.'
        self.MESSAGE_SHUTDOWN_YES = 'Y'
        self.MESSAGE_SHUTDOWN_NO = 'N'

        self.MESSAGE_CONNECT_START = 'CONNECT COMMAND:\nAttempting to connect to: {0}:{1}'
        self.MESSAGE_CONNECT_DONE = 'CONNECT COMMAND:\nConnected to server successfully'

        self.MESSAGE_DISCONNECT = 'DISCONNECT COMMAND:\nDisconnected from server successfully.'

        self.MESSAGE_ERROR_CONNECT = 'CONNECT COMMAND:\nFailed to connect to server (the server is either offline or an invalid address was entered.'
        self.MESSAGE_ERROR_DISCONNECT = 'DISCONNECT COMMAND:\nUnable to disconnect from server (there may have been no connection)'

        self.MESSAGE_ERROR_GAME = 'GAME COMMAND:\nInvalid arguments <player> <view/edit/delete>'

        self.MESSAGE_ERROR_UNAVAILABLE = 'This command is not available.'

        self.GAME_EDIT_NUMBERS = [1, 2, 3, 4, 5]
        self.GAME_EDIT_VAlUES = ['username', 'level', 'xp', 'credits', 'points']

        self.IP = 'chat-sv.ddns.net'
        self.IP = '127.0.0.1'
        self.PORT = 6666

        self.consoleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def draw(self):
        global Window, chatBox, commandBox, hasConfirmed

        hasConfirmed = False

        def send(event):
            eventPlay = str(event)
            eventPlay.split()
            self.command(commandBox.get())

        Window = Tk()
        Window.geometry(self.WINDOW_RESOLUTION + '+200+200')
        Window.configure(bg=self.WINDOW_BACKGROUND)
        Window.title(self.WINDOW_TITLE)

        titleText = StringVar()
        enterCommandText = StringVar()
        buttonText = StringVar()

        titleText.set('SERVER CONSOLE')
        enterCommandText.set('C O M M A N D')
        buttonText.set(' → ')

        titleLabel = Label(Window, textvariable=titleText, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)

        commandLabel = Label(Window, textvariable=enterCommandText, width=16, font=('Segoe UI', 8, 'bold'), fg=self.WINDOW_SPECIAL_FOREGROUND, bg=self.WINDOW_SPECIAL_BACKGROUND)
        commandBox = Entry(Window, width=52, bd=0, font=('Segoe UI', 10, 'bold'), fg=self.WINDOW_FOREGROUND, bg=self.WINDOW_HIGHLIGHT_BACKGROUND)
        sendButton = Button(Window, textvariable=buttonText, font=('Segoe UI', 8, ''), width=7, bd=0, fg=self.WINDOW_SPECIAL_FOREGROUND, bg=self.WINDOW_SPECIAL_BACKGROUND, command=lambda: self.command(commandBox.get()))

        chatBox = Text(Window, bd=2, bg=self.WINDOW_BACKGROUND, height="8", width="67", font=('courier new', 10))
        # chatScrollbar = Scrollbar(Window, orient="vertical")

        titleLabel.place(relx=0.05, rely=0.08)

        chatBox.place(relx=0.05, rely=0.23)
        # chatScrollbar.place(relx=0.925, rely=0.235)

        commandLabel.place(relx=0.05, rely=0.85374)
        commandBox.place(relx=0.265, rely=0.852)
        sendButton.place(relx=0.872, rely=0.852)

        commandBox.focus_force()
        commandBox.bind('<Return>', send)

        chatBox.config(state=DISABLED)
        # chatBox.configure(yscrollcommand=chatScrollbar.set)
        # chatScrollbar.configure(command=chatBox.yview)

        Window.mainloop()

    def command(self, cmd):
        global hasConfirmed, isEditingFinal, valNumber, isEditing

        if self.COMMAND_HELP in cmd.upper():
            self.show(self.MESSAGE_HELP)
        if self.COMMAND_CLEAR in cmd.upper():
            commandBox.delete(1.0, END)
        elif self.COMMAND_LOG in cmd.upper():
            if len(cmd) <= 6:
                self.show(self.MESSAGE_LOG)
            else:
                if cmd.upper().split()[1] == 'ON':
                    self.show(self.MESSAGE_LOG_ON)
                elif cmd.upper().split()[1] == 'OFF':
                    self.show(self.MESSAGE_LOG_OFF)
                else:
                    self.show(self.MESSAGE_LOG_FAIL)
        elif self.COMMAND_GAME in cmd.upper():
            if len(cmd) <= 6:
                self.show(self.MESSAGE_GAME)
            else:
                self.game(cmd)
        elif self.COMMAND_CONNECT in cmd.upper():
            if len(cmd) <= 9:
                self.connect()
            else:
                self.connect(cmd)
        elif self.COMMAND_DISCONNECT in cmd.upper():
            self.disconnect()
        elif self.COMMAND_SHUTDOWN in cmd.upper():
            self.show(self.MESSAGE_SHUTDOWN_WARNING)
            hasConfirmed = True
        elif self.MESSAGE_SHUTDOWN_YES == cmd.upper():
            if hasConfirmed:
                self.show(self.MESSAGE_SHUTDOWN_DONE)
                hasConfirmed = False
        elif self.MESSAGE_SHUTDOWN_NO == cmd.upper():
            if hasConfirmed:
                self.show(self.MESSAGE_SHUTDOWN_CANCELLED)
                hasConfirmed = False
        else:
            try:
                if isEditingFinal:
                    self.change(valNumber, cmd)
            except:
                pass
            try:
                if isEditing:
                    for numbers in self.GAME_EDIT_NUMBERS:
                        if numbers == int(cmd):
                            valNumber = int(cmd)
                            isEditingFinal = True
                            isEditing = False
                            self.show('\n' + self.MESSAGE_GAME_NEW)
                            break
            except:
                pass
        commandBox.delete(0, END)

    def request(self, name):
        self.connect()
        self.consoleSocket.send(str.encode('QU3RY' + name))
        while True:
            serverResponse = self.consoleSocket.recv(4096,).decode()
            if 'information' in serverResponse:
                returnedData = serverResponse
                break
            elif 'GAME COMMAND' in serverResponse:
                self.show(serverResponse)
                returnedData = None
                break
        return returnedData

    def edit(self, name):
        global isEditing, playerData

        playerData = self.request(name)
        playerData = ast.literal_eval(playerData)
        self.show((playerData['information']['username']).upper() + ' - INFORMATION', False)
        self.show('1: USERNAME: ' + playerData['information']['username'], False)
        self.show('2: LEVEL: ' + playerData['information']['level'], False)
        self.show('3: XP: ' + playerData['information']['xp'], False)
        self.show('4: CREDITS: ' + playerData['game']['credits'], False)
        self.show('5: POINTS: ' + playerData['game']['points'], True)
        self.show(self.MESSAGE_GAME_ENTER_NUM, False)
        isEditing = True

    def change(self, val, new):
        global isEditing, isEditingFinal
        isEditing = False
        isEditingFinal = False
        changeVal = self.GAME_EDIT_VAlUES[val - 1]
        if val <= 3:
            playerData['information'][changeVal] = new
        else:
            playerData['game'][changeVal] = new
        if val != 1:
            self.consoleSocket.send(str.encode('€' + str(playerData)))
            self.show(self.MESSAGE_GAME_EDIT_SUCCESS)
        else:
            self.show(self.MESSAGE_GAME_EDIT_FAIL)

    def game(self, cmd):
        try:
            firstArgument = cmd.upper().split()[1]
            secondArgument = cmd.upper().split()[2]
            if secondArgument == 'VIEW' or secondArgument == 'EDIT' or secondArgument == 'DELETE':
                if secondArgument == 'VIEW':
                    import _thread
                    returnedData = self.request(firstArgument)
                    if returnedData:
                        returnedData = ast.literal_eval(returnedData)
                        self.show((returnedData['information']['username']).upper() + ' - INFORMATION')
                        self.show('NAME: ' + returnedData['information']['name'], False)
                        self.show('LEVEL: ' + returnedData['information']['level'], False)
                        self.show('XP: ' + returnedData['information']['xp'], False)
                        self.show('CREDITS: ' + returnedData['game']['credits'], False)
                        self.show('POINTS: ' + returnedData['game']['points'], False)
                        self.show('CREATED: ' + returnedData['information']['date'], False)
                        # self.show('ROLE: ' + returnedData['information']['role'])
                elif secondArgument == 'EDIT':
                    self.edit(firstArgument)
                else:
                    pass
            else:
                self.show(self.MESSAGE_ERROR_GAME)
        except IndexError:
            self.show(self.MESSAGE_ERROR_GAME)

    def show(self, message, newline=True):
        chatBox.config(state=NORMAL)
        if newline:
            chatBox.insert(END, '\n' + message + '\n')
        else:
            chatBox.insert(END, '\n' + message)
        chatBox.tag_add('DEFAULT', 1.0, 1000.0)
        chatBox.tag_configure('DEFAULT', foreground=self.WINDOW_CHAT_BACKGROUND, font=('courier new', 10))
        chatBox.config(state=DISABLED)
        chatBox.see(END)

    def connect(self, args=None):
        try:
            if not args:
                connectionIP = self.IP
                connectionPort = self.PORT
            else:
                connectionIP = args.split()[1]
                connectionPort = int(args.split()[2])
            self.show(self.MESSAGE_CONNECT_START.format(connectionIP, connectionPort))
            self.consoleSocket.settimeout(3)
            self.consoleSocket.connect((connectionIP, connectionPort))
            self.consoleSocket.settimeout(None)
            self.show(self.MESSAGE_CONNECT_DONE)
        except:
            self.show(self.MESSAGE_ERROR_CONNECT)

    def disconnect(self):
        try:
            self.consoleSocket.send(str.encode('D1SC0NN3CT'))
            self.consoleSocket.close()
            self.show(self.MESSAGE_DISCONNECT)
        except:
            self.show(self.MESSAGE_ERROR_DISCONNECT)

    @staticmethod
    def close():
        Window.destroy()


if __name__ == '__main__':
    Main = Console()
    Main.draw()
