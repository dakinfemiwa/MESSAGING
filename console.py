from tkinter import *


class Console:
    def __init__(self):
        self.WINDOW_RESOLUTION = '600x250'
        self.WINDOW_BACKGROUND = '#353B48'
        self.WINDOW_FOREGROUND = '#FFFFFF'
        self.WINDOW_SPECIAL_FOREGROUND = '#2F3640'
        self.WINDOW_SPECIAL_BACKGROUND = '#DCDDE1'
        self.WINDOW_HIGHLIGHT_BACKGROUND = '#535C68'
        self.WINDOW_CHAT_BACKGROUND = '#BDC3C7'
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

        self.MESSAGE_HELP = '.LOG <on/off> - view server logs\n' \
                            '.GAME <player> <view/edit/delete> - manage players\n' \
                            '.SHUTDOWN - server shutdown\n' \
                            '.CLEAR - clear console log'

        self.MESSAGE_LOG = 'LOG COMMAND:\nPrint server logs in console <on/off>'
        self.MESSAGE_LOG_ON = 'LOG COMMAND:\nTurned server logging on successfully.'
        self.MESSAGE_LOG_OFF = 'LOG COMMAND:\nTurned server logging off successfully.'
        self.MESSAGE_LOG_FAIL = 'LOG COMMAND:\nInvalid arguments <on/off>'

        self.MESSAGE_GAME = 'GAME COMMAND:\nManage registered players <player> <view/edit/delete>'

        self.IP = 'chat-sv.ddns.net'
        self.PORT = 6666

    def draw(self):
        global Window, chatBox, messageBox

        def send(event):
            eventPlay = event
            eventPlay.split()
            self.command(messageBox.get())

        Window = Tk()
        Window.geometry(self.WINDOW_RESOLUTION)
        Window.configure(bg=self.WINDOW_BACKGROUND)
        Window.title(self.WINDOW_TITLE)

        titleText = StringVar()
        settingsText = StringVar()
        exitText = StringVar()
        createText = StringVar()
        userText = StringVar()
        passText = StringVar()
        enterMessageText = StringVar()
        buttonText = StringVar()
        errorText = StringVar()

        titleText.set('SERVER CONSOLE')
        settingsText.set('SIGN IN')
        exitText.set('SIGN IN AS GUEST')
        createText.set('SIGN UP')
        userText.set('USERNAME')
        passText.set('PASSWORD')
        enterMessageText.set('M E S S A G E')
        buttonText.set(' → ')
        errorText.set('')

        titleLabel = Label(Window, textvariable=titleText, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)

        messageLabel = Label(Window, textvariable=enterMessageText, width=16, font=('Segoe UI', 8, 'bold'), fg=self.WINDOW_SPECIAL_FOREGROUND, bg=self.WINDOW_SPECIAL_BACKGROUND)
        messageBox = Entry(Window, width=52, bd=0, font=('Segoe UI', 10, 'bold'), fg=self.WINDOW_FOREGROUND, bg=self.WINDOW_HIGHLIGHT_BACKGROUND)
        sendButton = Button(Window, textvariable=buttonText, font=('Segoe UI', 8, ''), width=7, bd=0, fg=self.WINDOW_SPECIAL_FOREGROUND, bg=self.WINDOW_SPECIAL_BACKGROUND, command=lambda: self.command(messageBox.get()))

        chatBox = Text(Window, bd=2, bg=self.WINDOW_BACKGROUND, height="8", width="67", font=('courier new', 10))

        titleLabel.place(relx=0.05, rely=0.08)

        chatBox.place(relx=.05, rely=.23)

        messageLabel.place(relx=0.05, rely=0.85374)
        messageBox.place(relx=0.265, rely=0.852)
        sendButton.place(relx=0.87, rely=0.852)

        messageBox.focus_force()
        messageBox.bind('<Return>', send)

        chatBox.config(state=DISABLED)

        Window.mainloop()

    def command(self, cmd):
        chatBox.config(state=NORMAL)
        if self.COMMAND_HELP in cmd.upper():
            chatBox.insert(END, '\n' + self.MESSAGE_HELP)
        if self.COMMAND_CLEAR in cmd.upper():
            chatBox.delete(1.0, END)
        elif self.COMMAND_LOG in cmd.upper():
            if len(cmd) <= 6:
                chatBox.insert(END, '\n' + self.MESSAGE_LOG)
            else:
                if cmd.upper().split()[1] == 'ON':
                    chatBox.insert(END, '\n' + self.MESSAGE_LOG_ON)
                elif cmd.upper().split()[1] == 'OFF':
                    chatBox.insert(END, '\n' + self.MESSAGE_LOG_OFF)
                else:
                    chatBox.insert(END, '\n' + self.MESSAGE_LOG_FAIL)
        elif self.COMMAND_GAME in cmd.upper():
            if len(cmd) <= 6:
                chatBox.insert(END, '\n' + self.MESSAGE_GAME)
        chatBox.tag_add('DEFAULT', 1.0, 1000.0)
        chatBox.tag_configure('DEFAULT', foreground=self.WINDOW_CHAT_BACKGROUND, font=('courier new', 10))
        chatBox.config(state=DISABLED)
        chatBox.see(END)
        messageBox.delete(0, END)

    @staticmethod
    def close():
        Window.destroy()


if __name__ == '__main__':
    Main = Console()
    Main.draw()
