from tkinter import *
import socket
import random
import _thread
import time
import ast


class Game:
    def __init__(self, data):
        # 192a56 dark blue
        # 2f3640 dark gray
        # 40739e ok blue
        # 6F1E51 magenta
        # 0652DD marine blue
        # 5758BB weird purple
        # 0a3d62 good blue
        # 1e272e almost black
        # 000000 pure black

        self.WINDOW_RESOLUTION = '600x250'
        self.WINDOW_BACKGROUND = '#141414'
        # self.WINDOW_BACKGROUND = '#000000'
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
        self.WINDOW_SUB_FONT3 = ('Segoe UI', 10, 'bold italic')
        self.WINDOW_BUTTON_FONT = ('Segoe UI', 12, 'bold')
        self.WINDOW_LOBBY_FONT = ('courier new', 10, 'bold')
        self.WINDOW_THEME = '#16A085'
        self.WINDOW_THEME2 = '#9B59B6'
        self.WINDOW_THEME3 = '#f39c12'
        self.WINDOW_ERROR = '#E74C3C'

        self.CONFIG_LOGGER = 'True'
        self.CONFIG_UPDATER = 'False'
        self.CONFIG_ADVANCED = 'False'
        self.CONFIG_VERSION = '1.0'

        self.MESSAGE_HOST_MATCH = 'Host match as lobby leader and configure game settings'
        self.MESSAGE_JOIN_MATCH = 'Join a match using a valid lobby host code'
        self.MESSAGE_BROWSE_LOBBY = 'Browse a list of public lobbies that you can join'

        self.MESSAGE_HOST_CODE = 'Share this code with new players so they can join the match'
        self.MESSAGE_JOIN_CODE = 'To join the match you must enter a valid host code'

        self.STR_HOST_MATCH = 'HOST MATCH'
        self.STR_JOIN_MATCH = 'JOIN MATCH'
        self.STR_BROWSE_LOBBY = 'FIND LOBBY'

        self.STR_LOBBY_EXIT = 'LEAVE LOBBY'
        self.STR_LOBBY_READY = 'READY'
        self.STR_LOBBY_UNREADY = 'UNREADY'

        self.IP = '127.0.0.1'
        # self.IP = 'chat-sv.ddns.net'
        self.PORT = 6666

        def nextPage():
            self.pageNumber = self.pageNumber + 1
            self.set(self.pageNumber)

        def lastPage():
            self.pageNumber = self.pageNumber - 1
            self.set(self.pageNumber)

        self.gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandCache = []
        self.windowItems = []
        self.pageNumber = 1
        self.hostCode = 'N/A'
        self.gameState = 'N/A'
        self.gamePlayers = []
        self.readyPlayers = []

        self.Window = Tk()
        self.Window.geometry(self.WINDOW_RESOLUTION)
        self.Window.configure(bg=self.WINDOW_BACKGROUND)
        self.Window.title(self.WINDOW_TITLE)

        self.titleText = StringVar()
        self.creditsText = StringVar()

        self.titleText.set((data['information']['username']).upper())
        self.creditsText.set(data['game']['credits'] + ' credits')

        self.titleLabel = Label(self.Window, textvariable=self.titleText, font=self.WINDOW_TITLE_FONT,
                                bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        self.titleLabel.place(relx=.05, rely=.08)

        self.hostButton = Button(self.Window, text=self.STR_HOST_MATCH, font=self.WINDOW_BUTTON_FONT,
                                 bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME, command=lambda: self.set(2), bd=0)
        self.hostInfo = Label(self.Window, text=self.MESSAGE_HOST_MATCH, font=self.WINDOW_SUB_FONT2,
                              bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.joinButton = Button(self.Window, text=self.STR_JOIN_MATCH, font=self.WINDOW_BUTTON_FONT,
                                 bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME2, command=lambda: self.set(3), bd=0)
        self.joinInfo = Label(self.Window, text=self.MESSAGE_JOIN_MATCH, font=self.WINDOW_SUB_FONT2,
                              bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.browseButton = Button(self.Window, text=self.STR_BROWSE_LOBBY, font=self.WINDOW_BUTTON_FONT,
                                   bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_THEME3, command=lambda: self.list(), bd=0)
        self.browseInfo = Label(self.Window, text=self.MESSAGE_BROWSE_LOBBY, font=self.WINDOW_SUB_FONT2,
                                bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.nextButton = Button(self.Window, text='→', font=self.WINDOW_BUTTON_FONT, bg=self.WINDOW_BACKGROUND,
                                 fg=self.WINDOW_THEME, command=lambda: nextPage(), bd=0)
        self.nextButton.place(relx=.92, rely=.84)

        self.backButton = Button(self.Window, text='←', font=self.WINDOW_BUTTON_FONT, bg=self.WINDOW_BACKGROUND,
                                 fg=self.WINDOW_THEME, command=lambda: lastPage(), bd=0)
        self.backButton.place(relx=.05, rely=.84)

        self.codeLabel = Label(self.Window, text=self.hostCode, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND,
                               fg=self.WINDOW_CHAT_BACKGROUND)

        self.codeInfo = Label(self.Window, text=self.MESSAGE_HOST_CODE, font=self.WINDOW_SUB_FONT2,
                              bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)
        self.entryInfo = Label(self.Window, text=self.MESSAGE_JOIN_CODE, font=self.WINDOW_SUB_FONT2,
                               bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_CHAT_BACKGROUND)

        self.codeEntry = Entry(self.Window, width=10, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND,
                               fg=self.WINDOW_CHAT_BACKGROUND, bd=0)
        self.codeEntry.configure(insertbackground=self.WINDOW_THEME2)

        self.lobbyChat = Text(self.Window, bd=0, bg=self.WINDOW_BACKGROUND, fg='white', height="7", width="40",
                              font=self.WINDOW_LOBBY_FONT)
        self.lobbyEntry = Entry(self.Window, width=39, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND,
                                fg=self.WINDOW_CHAT_BACKGROUND, bd=2)
        self.lobbyEntry.configure(insertbackground='white')

        self.lobbyPlayers = Label(self.Window, text='Players currently connected [1/4]',
                                  font=('Segoe UI', 10, 'bold italic'), fg=self.WINDOW_CHAT_BACKGROUND,
                                  bg=self.WINDOW_BACKGROUND)

        self.playerOne = Label(self.Window, text=testData['information']['username'], font=self.WINDOW_SUB_FONT2,
                               fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND)
        self.playerTwo = Label(self.Window, text='--', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND,
                               bg=self.WINDOW_BACKGROUND)
        self.playerThree = Label(self.Window, text='--', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND,
                                 bg=self.WINDOW_BACKGROUND)
        self.playerFour = Label(self.Window, text='--', font=self.WINDOW_SUB_FONT2, fg=self.WINDOW_CHAT_BACKGROUND,
                                bg=self.WINDOW_BACKGROUND)

        self.readyOne = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c',
                              bg=self.WINDOW_BACKGROUND)
        self.readyTwo = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c',
                              bg=self.WINDOW_BACKGROUND)
        self.readyThree = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c',
                                bg=self.WINDOW_BACKGROUND)
        self.readyFour = Label(self.Window, text='▇', font=self.WINDOW_SUB_FONT2, fg='#e74c3c',
                               bg=self.WINDOW_BACKGROUND)

        self.lobbyLeave = Button(self.Window, text=self.STR_LOBBY_EXIT, font=('segoe ui', 10, 'bold'),
                                 bg=self.WINDOW_BACKGROUND, fg='#e74c3c', bd=0, command=lambda: self.exitlobby())
        self.lobbyReady = Button(self.Window, text=self.STR_LOBBY_READY, font=('segoe ui', 10, 'bold'),
                                 bg=self.WINDOW_BACKGROUND, fg='#2ecc71', bd=0, command=lambda: self.readyplayer())
        self.lobbyUnready = Button(self.Window, text=self.STR_LOBBY_UNREADY, font=('segoe ui', 10, 'bold'),
                                   bg=self.WINDOW_BACKGROUND, fg='#e74c3c', bd=0,
                                   command=lambda: self.readyplayer(False))
        self.lobbyTest = Button(self.Window, text='TEST', font=('segoe ui', 10, 'bold'),
                                bg=self.WINDOW_BACKGROUND, fg='#e74c3c', bd=0,
                                command=lambda: (self.send('JOIN REQUEST:{0}'.format(testData['information']['username'])), self.lobby(False)))
        self.lobbyTest.place(relx=.8, rely=.85)

        self.lobbyStatName = 'None'
        self.lobbyStatPlayers = 'None'
        self.lobbyStatReady = 'None'
        self.lobbyStatGame = 'None'
        self.gotLobbyData = False

        self.playerLabels = [self.playerOne, self.playerTwo, self.playerThree, self.playerFour]
        self.readyLabels = [self.readyOne, self.readyTwo, self.readyThree, self.readyFour]

        self.windowItems = [self.hostButton, self.hostInfo, self.joinButton, self.joinInfo, self.codeLabel,
                            self.codeInfo, self.codeEntry, self.entryInfo, self.lobbyEntry, self.lobbyChat,
                            self.lobbyPlayers, self.playerOne, self.playerTwo, self.playerThree, self.playerFour,
                            self.readyOne, self.readyTwo, self.readyThree, self.readyFour, self.lobbyLeave,
                            self.lobbyReady, self.lobbyUnready, self.browseInfo, self.browseButton]

        self.set(1)
        self.notify()

        self.connect()
        _thread.start_new_thread(self.listen, ())

        self.Window.mainloop()

    def connect(self):
        try:
            self.gameSocket.connect((self.IP, self.PORT))
        except:
            self.chat('ERROR: Failed to connect to relay server\n')

    def send(self, message):
        self.gameSocket.send(str.encode(message))
        # Delay required due to high buffer.
        time.sleep(.01)

    def refresh(self):
        for label in self.playerLabels:
            label.config(text='--')
        for player in self.gamePlayers:
            pIndex = self.gamePlayers.index(player)
            self.playerLabels[pIndex].config(text=player)
        for player in self.readyPlayers:
            rIndex = self.gamePlayers.index(player)
            self.readyLabels[rIndex].config(fg='#2ecc71')
        for player in self.gamePlayers:
            rIndex = self.gamePlayers.index(player)
            if player not in self.readyPlayers:
                self.readyLabels[rIndex].config(fg='#e74c3c')
        self.lobbyPlayers.config(text='Players currently connected [{0}/4]'.format(len(self.gamePlayers)))

    def joinmatch(self):
        self.connect()
        self.send('JOIN REQUEST:Player')

    def listen(self):
        while True:
            try:
                receivedData = self.gameSocket.recv(4096)
                receivedData = receivedData.decode()
            except:
                try:
                    self.chat('ERROR: Lost connection to game server\n')
                except:
                    pass
                break
            if not receivedData:
                try:
                    self.chat('ERROR: Lost connection to game server\n')
                except:
                    pass
                break
            else:
                print(receivedData)
                if self.gameState == 'HOST-LOBBY':
                    allArguments = receivedData.split(':')
                    if allArguments[0] == 'JOIN REQUEST':
                        requesterName = allArguments[1]
                        self.send('HOST NAME:{0}'.format(testData['information']['username']))
                        self.gamePlayers.append(requesterName)
                        self.refresh()
                        self.chat('GAME: {0} joined the lobby \n'.format(requesterName.upper()))
                        playersSplit = ";".join(self.gamePlayers)
                        self.send('PLAYER LIST:{0}'.format(playersSplit))
                    elif allArguments[0] == 'QUERY':
                        lobbyData = {
                            'lobbies': {
                                'number': '1'
                            },
                            'lobby':  {
                                'name': testData['information']['username'],
                                'users': str(len(self.gamePlayers)),
                                'ready': str(len(self.readyPlayers)),
                                'game': 'hangman'
                            }
                        }
                        self.send('LOBBY DATA' + str(lobbyData))
                    elif allArguments[0] == 'READY':
                        readyPlayer = allArguments[1]
                        if readyPlayer not in self.readyPlayers:
                            self.readyPlayers.append(readyPlayer)
                            self.refresh()
                    elif allArguments[0] == 'UNREADY':
                        unreadyPlayer = allArguments[1]
                        self.readyPlayers.remove(unreadyPlayer)
                        self.refresh()
                    elif allArguments[0] == 'LEAVE':
                        leftPlayer = allArguments[1]
                        try:
                            self.gamePlayers.remove(leftPlayer)
                            self.readyPlayers.remove(leftPlayer)
                        except:
                            pass  # Player was not ready before leaving
                        self.send('CHAT:GAME: {0} left the lobby\n'.format(leftPlayer.upper()))
                        self.refresh()
                    elif allArguments[0] == 'CHAT':
                        allArguments.remove('CHAT')
                        allArguments.remove('GAME')
                        chatMessage = ' '.join(allArguments)
                        self.chat('CHAT:' + chatMessage)
                elif self.gameState == 'MAIN':
                    if 'LOBBY DATA' in receivedData:
                        lobbyData = receivedData.strip('LOBBY DATA')
                        lobbyData = ast.literal_eval(lobbyData)
                        if int(lobbyData['lobbies']['number']) != 0:
                            self.lobbyStatName = lobbyData['lobby']['name']
                            self.lobbyStatPlayers = lobbyData['lobby']['users']
                            self.lobbyStatReady = lobbyData['lobby']['ready']
                            self.lobbyStatGame = lobbyData['lobby']['game']
                            self.gotLobbyData = True
                            self.refreshlist()

                else:
                    allArguments = receivedData.split(':')
                    if allArguments[0] == 'HOST NAME':
                        hostName = allArguments[1]
                        self.gamePlayers.append(hostName)
                        self.gamePlayers.append(testData['information']['username'])
                        self.refresh()
                        self.chat('GAME: {0} is the lobby leader \n'.format(hostName.upper()))
                    elif allArguments[0] == 'PLAYER LIST':
                        playersGame = allArguments[1]
                        self.gamePlayers = playersGame.split(';')
                        self.refresh()
                    elif allArguments[0] == 'READY':
                        readyPlayer = allArguments[1]
                        if readyPlayer not in self.readyPlayers:
                            self.readyPlayers.append(readyPlayer)
                            self.refresh()
                    elif allArguments[0] == 'UNREADY':
                        unreadyPlayer = allArguments[1]
                        self.readyPlayers.remove(unreadyPlayer)
                        self.refresh()
                    elif allArguments[0] == 'CHAT':
                        allArguments.remove('CHAT')
                        allArguments.remove('GAME')
                        chatMessage = ' '.join(allArguments)
                        self.chat('CHAT:' + chatMessage)

    @staticmethod
    def generate():
        return str(random.randint(1000000, 9999999))

    def clear(self):
        for item in self.windowItems:
            item.place_forget()

    def front(self):
        self.gameState = 'MAIN'
        self.clear()
        self.hostButton.place(relx=.05, rely=.27)
        self.hostInfo.place(relx=.054, rely=.38)
        self.joinButton.place(relx=.05, rely=.47)
        self.joinInfo.place(relx=.054, rely=.58)
        self.browseButton.place(relx=.05, rely=.67)
        self.browseInfo.place(relx=.054, rely=.78)

    def host(self):
        self.clear()
        self.gameState = 'HOST'
        self.hostCode = self.generate()
        self.hostButton.place(relx=.05, rely=.27)
        self.codeLabel.place(relx=.054, rely=.41)
        self.codeInfo.place(relx=.054, rely=.58)
        self.codeLabel.config(text=self.hostCode)

    def join(self):
        def sendcode(event):
            self.joinmatch()
        self.clear()
        self.gameState = 'JOIN'
        self.joinButton.place(relx=.05, rely=.27)
        self.codeEntry.place(relx=.055, rely=.41)
        self.entryInfo.place(relx=.055, rely=.58)
        self.codeEntry.focus_force()
        self.codeEntry.bind('<Return>', sendcode)

    def notify(self):
        notifText = 'CONNECTION ERROR'
        widthText = len(notifText) + 2
        self.notificationTitle = Label(self.Window, text=notifText, bg='#e74c3c', fg='#141414', font=('Calibri', 14, 'bold'), height=1, width=31, anchor='w')
        self.notificationTitle.place(relx=.15, rely=.25)
        self.notificationBox = Text(self.Window, bg='#140000', fg='white', font=('Segoe UI', 10, ''), bd=0, width=58,
                                    height=5)
        self.notificationBox.place(relx=.15, rely=.35)
        self.notificationBox.insert(END, 'The client failed to connect to the game server, so some features such as lobbies and game statistics will be unavailable. You could try reconnecting or changing the server address below.')
        self.notificationBox.tag_add("!", 1.0, 99999999999999.0)
        self.notificationBox.tag_config("!", foreground='WHITE', font=('Calibri', 11, ""), justify='left',
                                        spacing1='5', spacing2='5')
        self.notificationBox.config(state=DISABLED)
        self.notificationBar = Label(self.Window, bg='#140000', height=1, width=57)
        self.notificationBar.place(relx=.15, rely=.7)
        self.notificationConfirm = Button(self.Window, text='CONFIRM', font=('Segoe UI', 11, "bold"), bg='#140000', fg='#e74c3c', bd=0, height=1, command=lambda: (self.notificationBox.place_forget(),
                                                                                                                                                                   self.notificationTitle.place_forget(),
                                                                                                                                                                   self.notificationBar.place_forget(),
                                                                                                                                                                   self.notificationConfirm.place_forget()))
        self.notificationConfirm.place(relx=.698, rely=.655)

    def lobby(self, host=True):

        def send(event):
            if self.lobbyEntry.get() != '':
                self.chat('{0} ({1}): '.format((testData['information']['username']).upper(), self.gameState) + self.lobbyEntry.get() + '\n')
                self.lobbyEntry.delete(0, END)

        if host:
            self.chat('HOST: Created new lobby\n')
            self.gameState = 'HOST-LOBBY'
            self.gamePlayers.append(testData['information']['username'])
            self.refresh()
        else:
            self.gameState = 'JOIN-LOBBY'

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

        self.readyOne.place(relx=.92, rely=.35)
        self.readyTwo.place(relx=.92, rely=.45)
        self.readyThree.place(relx=.92, rely=.55)
        self.readyFour.place(relx=.92, rely=.65)

        self.lobbyReady.place(relx=.6075, rely=.75)
        self.lobbyLeave.place(relx=.8, rely=.75)

    def refreshlist(self):

        if self.gotLobbyData:

            lobbyNameLabel = Label(self.Window, text=str(self.lobbyStatName).upper(), fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_SUB_FONT3)
            lobbyGameLabel = Label(self.Window, text=str(self.lobbyStatGame).upper(), fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_SUB_FONT3)
            lobbyPlayersLabel = Label(self.Window, text=str(self.lobbyStatPlayers + ' PLAYERS').upper(), fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_SUB_FONT3)
            lobbyReadyLabel = Label(self.Window, text=str(self.lobbyStatReady + ' READY').upper(), fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_SUB_FONT3)

            lobbyNameLabel.place(relx=.45, rely=.3)
            lobbyGameLabel.place(relx=.45, rely=.4)
            lobbyPlayersLabel.place(relx=.45, rely=.5)
            lobbyReadyLabel.place(relx=.45, rely=.6)

            lName = Label(self.Window, text='LOBBY NAME', fg=self.WINDOW_THEME3, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_BUTTON_FONT)
            lName.place(relx=.05, rely=.3)
            lGame = Label(self.Window, text='LOBBY GAME', fg=self.WINDOW_THEME3, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_BUTTON_FONT)
            lGame.place(relx=.05, rely=.4)
            lPlayers = Label(self.Window, text='PLAYERS', fg=self.WINDOW_THEME3, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_BUTTON_FONT)
            lPlayers.place(relx=.05, rely=.5)
            lReady = Label(self.Window, text='READY', fg=self.WINDOW_THEME3, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_BUTTON_FONT)
            lReady.place(relx=.05, rely=.6)

        else:
            lUnavailable = Label(self.Window, text='There are no lobbies available this time.', fg=self.WINDOW_CHAT_BACKGROUND, bg=self.WINDOW_BACKGROUND, font=self.WINDOW_SUB_FONT2)
            lUnavailable.place(relx=.05, rely=.3)

    def list(self):
        self.clear()
        self.send('QUERY')
        self.refreshlist()

    def chat(self, text):
        self.lobbyChat.config(state=NORMAL)
        self.lobbyChat.tag_add('DEFAULT', 1.0, 1000.0)
        self.lobbyChat.tag_configure('DEFAULT', foreground=self.WINDOW_CHAT_BACKGROUND, font=('courier new', 10))
        self.lobbyChat.insert(END, text)
        self.lobbyChat.config(state=DISABLED)
        self.lobbyChat.see(END)

    def readyplayer(self, x=True):
        if x:
            self.send('READY:{0}'.format(testData['information']['username']))
            self.send('CHAT:GAME: {0} is ready to play\n'.format((testData['information']['username']).upper()))
            self.lobbyReady.place_forget()
            self.lobbyUnready.place(relx=.6075, rely=.75)
            self.refresh()
            for player in self.readyPlayers:
                if player == testData['information']['username']:
                    rIndex = self.gamePlayers.index(player)
                    self.readyLabels[rIndex].config(fg='#2ecc71')
        else:
            self.send('UNREADY:{0}'.format(testData['information']['username']))
            self.send('CHAT:GAME: {0} is not ready to play\n'.format((testData['information']['username']).upper()))
            self.lobbyUnready.place_forget()
            self.lobbyReady.place(relx=.6075, rely=.75)
            self.refresh()
            for player in self.readyPlayers:
                if player == testData['information']['username']:
                    rIndex = self.gamePlayers.index(player)
                    self.readyLabels[rIndex].config(fg='#e74c3c')

    def exitlobby(self):
        self.send('LEAVE:{0}'.format(testData['information']['username']))
        self.set(1)

    def game(self):
        self.clear()

    def set(self, page):
        self.pageNumber = page
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
        if page == 1 or page == 4:
            self.backButton.place_forget()
        else:
            self.backButton.place(relx=.05, rely=.84)


testData = {
    'information': {
        'username': 'Shivam'
    },
    'game': {
        'credits': '300'
    }
}

# testData['information']['username'] = input('Test user: ')

if __name__ == '__main__':
    GameT = Game(testData)
