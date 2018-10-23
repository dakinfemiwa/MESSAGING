from tkinter import *
import socket


class Game:
    def __init__(self, data):
        self.WINDOW_RESOLUTION = '600x250'
        # self.WINDOW_BACKGROUND = '#353B48'
        self.WINDOW_BACKGROUND = '#141414'
        self.WINDOW_FOREGROUND = '#FFFFFF'
        self.WINDOW_SPECIAL_FOREGROUND = '#2F3640'
        self.WINDOW_SPECIAL_BACKGROUND = '#DCDDE1'
        self.WINDOW_HIGHLIGHT_BACKGROUND = '#535C68'
        self.WINDOW_CHAT_BACKGROUND = '#BDC3C7'
        # self.WINDOW_CHAT_BACKGROUND = '#F39C12'
        self.WINDOW_TITLE = 'Game (alpha)'
        self.WINDOW_TITLE_FONT = ('Segoe UI', 16, 'bold')
        self.WINDOW_SUB_FONT = ('Arial', 11, 'bold')
        self.WINDOW_SUB_FONT2 = ('Segoe UI', 10, 'bold')
        self.WINDOW_BUTTON_FONT = ('Segoe UI', 12, 'bold')
        self.WINDOW_THEME = '#16A085'
        self.WINDOW_THEME2 = '#9B59B6'
        self.WINDOW_ERROR = '#E74C3C'

        self.CONFIG_LOGGER = 'True'
        self.CONFIG_UPDATER = 'False'
        self.CONFIG_ADVANCED = 'False'
        self.CONFIG_VERSION = '1.0'

        self.MESSAGE_HOST_MATCH = 'Host match as lobby leader and configure game settings'
        self.MESSAGE_JOIN_MATCH = 'Join a match using a valid lobby host code'

        self.MESSAGE_HOST_CODE = 'Share this code with new players so they can join the match'
        self.MESSAGE_JOIN_CODE = 'To join the match you must enter a valid host code'

        # self.IP = '127.0.0.1'
        self.IP = 'chat-sv.ddns.net'
        self.PORT = 6666

        def gonext():
            self.pageNumber = self.pageNumber + 1
            self.set(self.pageNumber)

        def goback():
            self.pageNumber = self.pageNumber - 1
            self.set(self.pageNumber)

        self.consoleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandCache = []
        self.windowItems = []
        self.pageNumber = 1

        self.Window = Tk()
        self.Window.geometry(self.WINDOW_RESOLUTION)
        self.Window.configure(bg=self.WINDOW_BACKGROUND)
        self.Window.title(self.WINDOW_TITLE)

        self.titleText = StringVar()
        self.creditsText = StringVar()

        self.titleText.set((data['information']['username']).upper())
        self.creditsText.set(data['game']['credits'] + ' credits')

        self.titleLabel = Label(self.Window, textvariable=self.titleText, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        self.titleLabel.place(relx=.05, rely=.08)

        self.creditsLabel = Label(self.Window, textvariable=self.creditsText, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        # self.creditsLabel.place(relx=.82, rely=.10)

        self.hostButton = Button(self.Window, text='HOST MATCH', font=self.WINDOW_BUTTON_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME, command=lambda: self.host(), bd=0)
        self.hostInfo = Label(self.Window, text=self.MESSAGE_HOST_MATCH, font=self.WINDOW_SUB_FONT2, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.joinButton = Button(self.Window, text='JOIN MATCH', font=self.WINDOW_BUTTON_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME2, command=lambda: self.join(), bd=0)
        self.joinInfo = Label(self.Window, text=self.MESSAGE_JOIN_MATCH, font=self.WINDOW_SUB_FONT2, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.nextButton = Button(self.Window, text='→', font=self.WINDOW_BUTTON_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME, command=lambda: gonext(), bd=0)
        self.nextButton.place(relx=.92, rely=.84)

        self.backButton = Button(self.Window, text='←', font=self.WINDOW_BUTTON_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME, command=lambda: goback(), bd=0)
        self.backButton.place(relx=.05, rely=.84)

        self.codeLabel = Label(self.Window, text='2930192', font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.codeInfo = Label(self.Window, text=self.MESSAGE_HOST_CODE, font=self.WINDOW_SUB_FONT2, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)
        self.entryInfo = Label(self.Window, text=self.MESSAGE_JOIN_CODE, font=self.WINDOW_SUB_FONT2, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.codeEntry = Entry(self.Window, width=10, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND, bd=0)
        self.codeEntry.configure(insertbackground=self.WINDOW_THEME2)

        self.lobbyChat = Text(self.Window, bd=0, bg=self.WINDOW_BACKGROUND, fg='white', height="7", width="40", font=('courier new', 10, 'bold'))
        self.lobbyEntry = Entry(self.Window, width=39, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND, bd=2)
        self.lobbyEntry.configure(insertbackground='white')

        self.lobbyPlayers = Label(self.Window, text='Players currently connected [2/5]', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)

        self.playerOne = Label(self.Window, text='Red', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)
        self.playerTwo = Label(self.Window, text='Green', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)
        self.playerThree = Label(self.Window, text='Yellow', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)
        self.playerFour = Label(self.Window, text='Blue', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)
        self.playerFive = Label(self.Window, text='Purple', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)

        self.readyOne = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c', bg=self.WINDOW_BACKGROUND)
        self.readyTwo = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#2ecc71', bg=self.WINDOW_BACKGROUND)
        self.readyThree = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c', bg=self.WINDOW_BACKGROUND)
        self.readyFour = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c', bg=self.WINDOW_BACKGROUND)
        self.readyFive = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#2ecc71', bg=self.WINDOW_BACKGROUND)

        self.windowItems = [self.hostButton, self.hostInfo, self.joinButton, self.joinInfo, self.codeLabel, self.codeInfo,
                            self.codeEntry, self.entryInfo, self.lobbyEntry, self.lobbyChat, self.lobbyPlayers]

        # self.set(self.pageNumber)
        self.set(4)

        self.Window.mainloop()

    def clear(self):
        for item in self.windowItems:
            item.place_forget()

    def front(self):
        self.clear()
        self.hostButton.place(relx=.05, rely=.3)
        self.hostInfo.place(relx=.054, rely=.41)
        self.joinButton.place(relx=.05, rely=.5)
        self.joinInfo.place(relx=.054, rely=.61)

    def host(self):
        self.clear()
        self.hostButton.place(relx=.05, rely=.3)
        self.codeLabel.place(relx=.054, rely=.44)
        self.codeInfo.place(relx=.054, rely=.61)

    def join(self):
        self.clear()
        self.joinButton.place(relx=.05, rely=.3)
        self.codeEntry.place(relx=.055, rely=.44)
        self.entryInfo.place(relx=.055, rely=.61)
        self.codeEntry.focus_force()

    def lobby(self):
        def enter(text):
            self.lobbyChat.config(state=NORMAL)
            self.lobbyChat.tag_add('DEFAULT', 1.0, 1000.0)
            self.lobbyChat.tag_configure('DEFAULT', foreground=self.WINDOW_CHAT_BACKGROUND, font=('courier new', 10))
            self.lobbyChat.insert(END, text)
            self.lobbyChat.config(state=DISABLED)

        def send(event):
            if self.lobbyEntry.get() != '':
                enter('TEST (HOST): ' + self.lobbyEntry.get() + '\n')
                self.lobbyEntry.delete(0, END)
                self.lobbyChat.see(END)

        enter('HOST: Created new lobby\n')

        self.clear()
        self.lobbyChat.place(relx=.052, rely=.26)
        self.lobbyEntry.bind('<Return>', send)
        self.lobbyEntry.place(relx=.052, rely=.73)
        self.lobbyEntry.focus_force()
        self.lobbyPlayers.place(relx=.61, rely=.25)

        # TEST

        self.playerOne.place(relx=.61, rely=.35)
        self.playerTwo.place(relx=.61, rely=.45)
        self.playerThree.place(relx=.61, rely=.55)
        self.playerFour.place(relx=.61, rely=.65)
        self.playerFive.place(relx=.61, rely=.75)

        self.readyOne.place(relx=.92, rely=.35)
        self.readyTwo.place(relx=.92, rely=.45)
        self.readyThree.place(relx=.92, rely=.55)
        self.readyFour.place(relx=.92, rely=.65)
        self.readyFive.place(relx=.92, rely=.75)

    def game(self):
        self.clear()

    def set(self, page):
        if page == 1:
            self.front()
        elif page == 2:
            self.host()
        elif page == 3:
            self.join()
        elif page == 4:
            self.lobby()
        elif page == 5:
            self.game()
        if page == 1:
            self.backButton.place_forget()
        else:
            self.backButton.place(relx=.05, rely=.84)


testData = {
    'information': {
        'username': 'test'
    },
    'game': {
        'credits': '300'
    }
}

if __name__ == '__main__':
    GameT = Game(testData)
