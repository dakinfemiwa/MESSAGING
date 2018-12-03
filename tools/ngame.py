import configparser
from threading import Thread
from time import sleep
from tkinter import *

from tools.Player import Player
from tools.Switch import Switch
from tools.animator import Animate
from tools.Network import Host, Join

# from tools.error import Error


class Game:
    def __init__(self):
        self.W_BG = '#2F3542'
        self.W_FG = '#FFFFFF'
        self.W_SIZE = '600x300'
        self.W_SIZE = '800x300'
        self.W_TITLE = 'PLACEHOLDER'

        self.W_FONT = ('MS PGothic', 30, 'bold')
        self.W_FONT2 = ('MS PGothic', 12, 'bold')
        self.W_FONT3 = ('MS PGothic', 10, 'bold')
        self.W_FONT4 = ('MS PGothic', 11, 'bold')

        self.G_GAMEMODE = 0
        self.GamePage = 1
        self.GameLives = 3
        self.GameCooldown = 20

        self.S_GAME = 'PLACEHOLDER'
        self.S_SINGLEPLAYER = 'SINGLE-PLAYER'
        self.S_MULTIPLAYER = 'MULTI-PLAYER'
        self.S_CUSTOMIZE = 'CUSTOMIZE'
        self.S_SETTINGS = 'SETTINGS'
        self.S_EXITGAME = 'EXIT GAME'

        self.S_VERSION = 'Version A - 0.1'
        self.S_HELP = 'SHOW HELP'
        self.S_UPDATE = 'AUTO-UPDATE'
        self.S_LOGGING = 'LOG EVENTS'
        self.S_CHEAT = 'ALLOW CHEATS'
        self.S_LIVES = '3 LIVES REMAINING'
        self.S_POSITION = 'SHOW POSITION'
        self.S_PAGE = 'SHOW PAGE'

        self.C_RED = '#E74C3C'
        self.C_GREEN = '#2ECC71'
        self.C_ORANGE = '#F39C12'
        self.C_BLUE = '#3498DB'
        self.C_YELLOW = '#F1C40F'
        self.C_GRAY = '#95A5A6'
        self.C_LIGHTGRAY = '#BDC3C7'

        self.Configuration = configparser.ConfigParser()
        self.Configuration.read('game-config.ini')

        self.whiteFloor = None
        self.whiteFloor2 = None
        self.whiteFloor3 = None
        self.whiteFloor4 = None
        self.whiteFloor5 = None
        self.whiteFloor6 = None
        self.whiteFloor7 = None
        self.whiteFloor8 = None
        self.whiteFloor9 = None

        self.allFloors = [self.whiteFloor, self.whiteFloor2, self.whiteFloor3, self.whiteFloor4, self.whiteFloor5, self.whiteFloor6, self.whiteFloor7, self.whiteFloor8]

        self.GameWindow = Tk()
        self.GameWindow.geometry(self.W_SIZE)
        self.GameWindow.title(self.W_TITLE)
        self.GameWindow.config(bg=self.W_BG)

        self.GameTitle = Label(self.GameWindow, text=self.S_GAME, font=self.W_FONT, bg=self.W_BG, fg=self.W_FG)
        self.GameTitle.place(relx=.05, rely=.1)

        self.GameSingleplayer = Button(self.GameWindow, text=self.S_SINGLEPLAYER, font=self.W_FONT2, bg=self.W_BG, fg=self.W_FG, bd=0, command=lambda: self.startGame(0))
        self.GameSingleplayer.place(relx=.05, rely=.3)
        self.GameMultiplayer = Button(self.GameWindow, text=self.S_MULTIPLAYER, font=self.W_FONT2, bg=self.W_BG, fg=self.W_FG, bd=0, command=lambda: self.startGame(1))
        self.GameMultiplayer.place(relx=.05, rely=.4)
        self.GameCustomize = Button(self.GameWindow, text=self.S_CUSTOMIZE, font=self.W_FONT2, bg=self.W_BG, fg=self.W_FG, bd=0, command=lambda: self.customizeScreen())
        self.GameCustomize.place(relx=.05, rely=.5)
        self.GameSettings = Button(self.GameWindow, text=self.S_SETTINGS, font=self.W_FONT2, bg=self.W_BG, fg=self.W_FG, bd=0, command=lambda: self.changeSettings())
        self.GameSettings.place(relx=.05, rely=.6)
        self.GameExitGame = Button(self.GameWindow, text=self.S_EXITGAME, font=self.W_FONT2, bg=self.W_BG, fg=self.C_RED, bd=0, command=lambda: self.exitGame())
        self.GameExitGame.place(relx=.05, rely=.7)

        self.GameLivesRemaining = Label(self.GameWindow, text=self.S_LIVES, font=self.W_FONT4, bg=self.W_BG, fg=self.C_RED)

        self.SettingsVersion = Label(self.GameWindow, text=self.S_VERSION, font=self.W_FONT2, bg=self.W_BG, fg=self.C_GRAY)
        self.SettingsHelp = Label(self.GameWindow, text=self.S_HELP, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)
        self.SettingsUpdate = Label(self.GameWindow, text=self.S_UPDATE, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)
        self.SettingsLog = Label(self.GameWindow, text=self.S_LOGGING, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)
        self.SettingsCheat = Label(self.GameWindow, text=self.S_CHEAT, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)

        self.SettingsPosition = Label(self.GameWindow, text=self.S_POSITION, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)
        self.SettingsPage = Label(self.GameWindow, text=self.S_PAGE, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)

        self.SettingsPositionSwitch = Switch(self.GameWindow)
        self.SettingsPageSwitch = Switch(self.GameWindow)

        self.SettingsHelpSwitch = Switch(self.GameWindow)
        self.SettingsUpdateSwitch = Switch(self.GameWindow)
        self.SettingsLogSwitch = Switch(self.GameWindow)
        self.SettingsCheatSwitch = Switch(self.GameWindow)

        self.currentLocation = StringVar()
        self.PlayerPosition = Label(self.GameWindow, textvariable=self.currentLocation, font=self.W_FONT3, bg=self.W_BG, fg=self.C_GRAY)

        self.currentPage = StringVar()
        self.PlayerPage = Label(self.GameWindow, textvariable=self.currentPage, font=self.W_FONT3, bg=self.W_BG, fg=self.C_GREEN)

        self.GameAssets = [self.GameTitle, self.GameSingleplayer, self.GameMultiplayer, self.GameCustomize, self.GameSettings, self.GameExitGame]
        self.SettingsAssets = [self.SettingsVersion]

        self.THREAD_CONFIG = Thread(target=self.loadConfiguration, args=())
        self.THREAD_WINDOW = Thread(target=self.GameWindow.mainloop())

    def drawStart(self):
        global keyPressedL, keyPressedR

        keyPressedR = False
        keyPressedL = False

        def handleKeyPress(event):
            global keyPressedL, keyPressedR
            if self.gs == 'host':
                if event.keysym == 'Left':
                    keyPressedL = True
                    P.setVelocityX(-0.0025)
                elif event.keysym == 'Right':
                    keyPressedR = True
                    P.setVelocityX(+0.0025)
                elif event.keysym == 'Up':
                    if not P.isJumping():
                        if keyPressedL:
                            P.jump(0)
                        elif keyPressedR:
                            P.jump(1)
                        else:
                            P.jump(2)
            else:
                if event.keysym == 'Left':
                    keyPressedL = True
                    self.T.setVelocityX(-0.0025)
                elif event.keysym == 'Right':
                    keyPressedR = True
                    self.T.setVelocityX(+0.0025)
                elif event.keysym == 'Up':
                    if not self.T.isJumping():
                        if keyPressedL:
                            self.T.jump(0)
                        elif keyPressedR:
                            self.T.jump(1)
                        else:
                            self.T.jump(2)

        def handleKeyRelease(event):
            global keyPressedL, keyPressedR
            if self.gs == 'host':
                if event.keysym == 'Left':
                    keyPressedL = False
                    if not keyPressedR:
                        P.setVelocityX(0)
                elif event.keysym == 'Right':
                    keyPressedR = False
                    if not keyPressedL:
                        P.setVelocityX(0)
            else:
                pass

        def evStopL(event):
            global keyPressedL, keyPressedR
            keyPressedL = False
            if self.gs == 'host':
                if not keyPressedR:
                    P.setVelocityX(0)
            else:
                self.T.setVelocityX(0)

        def evStopR(event):
            global keyPressedL, keyPressedR
            keyPressedR = False
            if self.gs == 'host':
                if not keyPressedL:
                    P.setVelocityX(0)
            else:
                self.T.setVelocityX(0)

        self.clearScreen()
        self.GameWindow.bind('<Up>', handleKeyPress)
        self.GameWindow.bind('<Right>', handleKeyPress)
        self.GameWindow.bind('<Left>', handleKeyPress)
        self.GameWindow.bind('<KeyRelease-Left>', evStopL)
        self.GameWindow.bind('<KeyRelease-Right>', evStopR)

        self.PlayerPage.place(relx=.825, rely=.05)

        self.drawPage(1)
        self.GameWindow.after(1, lambda: self.GameLivesRemaining.place(relx=.41, rely=.15))
        self.GameWindow.after(3000, lambda: self.GameLivesRemaining.place_forget())

        P = Player(self.GameWindow, 'white')
        P.draw(.05, .5)

        if self.gs == 'host':

            gThread = Thread(target=self.moveDown, args=(P, ))
            uThread = Thread(target=self.updateLocation, args=(P, ))
            cThread = Thread(target=self.changeLocation, args=(P, ))
            pThread = Thread(target=self.showLocation, args=(P, ))
            bThread = Thread(target=self.checkBoundary, args=(P, ))

        else:

            gThread = Thread(target=self.moveDown, args=(self.T, ))
            uThread = Thread(target=self.updateLocation, args=(self.T, ))
            cThread = Thread(target=self.changeLocation, args=(self.T, ))
            pThread = Thread(target=self.showLocation, args=(self.T, ))
            bThread = Thread(target=self.checkBoundary, args=(self.T, ))

        allThreads = [gThread, uThread, cThread, pThread, bThread]

        for thread in allThreads:
            thread.start()

    def clearFloors(self):
        try:
            for floor in self.allFloors:
                floor.place_forget()
        except:
            print('cleanup error')

    def drawPage(self, n):
        self.currentPage.set('GAME PAGE: ' + str(n))
        self.clearFloors()
        if n == 1:
            self.whiteFloor = Label(self.GameWindow, bg=self.W_FG, height=3, width=200)
            self.whiteFloor.place(relx=.0, rely=.85)
        elif n == 2:
            self.whiteFloor2 = Label(self.GameWindow, bg=self.W_FG, height=3, width=43)
            self.whiteFloor2.place(relx=.0, rely=.85)

            self.whiteFloor3 = Label(self.GameWindow, bg=self.W_FG, height=3, width=100)
            self.whiteFloor3.place(relx=.70, rely=.85)
        elif n == 3:
            self.whiteFloor4 = Label(self.GameWindow, bg=self.W_FG, height=3, width=20)
            self.whiteFloor4.place(relx=.0, rely=.85)

            self.whiteFloor5 = Label(self.GameWindow, bg=self.W_FG, height=3, width=100)
            self.whiteFloor5.place(relx=.925, rely=.85)

            self.whiteFloor6 = Label(self.GameWindow, bg=self.W_FG, height=1, width=10)
            self.whiteFloor6.place(relx=.2, rely=.7)

            self.whiteFloor7 = Label(self.GameWindow, bg=self.W_FG, height=1, width=8)
            self.whiteFloor7.place(relx=.4, rely=.6)

            self.whiteFloor8 = Label(self.GameWindow, bg=self.W_FG, height=1, width=14)
            self.whiteFloor8.place(relx=.68, rely=.65)
        self.allFloors = [self.whiteFloor, self.whiteFloor2, self.whiteFloor3, self.whiteFloor4, self.whiteFloor5, self.whiteFloor6, self.whiteFloor7, self.whiteFloor8]

    def loadConfiguration(self):
        configEntries = ['Show-Help', 'Auto-Update', 'Log-Events', 'Allow-Cheats', 'Show-Position', 'Show-Pages']
        configValues = [0, 0, 0, 0, 0, 0]
        configSwitches = [self.SettingsHelpSwitch, self.SettingsUpdateSwitch, self.SettingsLogSwitch, self.SettingsCheatSwitch, self.SettingsPositionSwitch, self.SettingsPageSwitch]

        for value in configEntries:
            configValues[configEntries.index(value)] = int(self.Configuration['Settings'][value])
            configSwitches[configEntries.index(value)].set(int(self.Configuration['Settings'][value]))

    def moveDown(self, p):
        while True:
            if p.gravity():
                if self.GamePage == 1:
                    playerLocation = p.getLocation()
                    if playerLocation[1] < .79:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                elif self.GamePage == 2:
                    playerLocation = p.getLocation()
                    if playerLocation[1] < .79:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    elif playerLocation[1] <= 1.10 and 0.39 < playerLocation[0] < 0.68:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    if .97 > playerLocation[0] > .70 and playerLocation[1] > 0.79:
                        p.setLocation(playerLocation[0], 0.79)
                elif self.GamePage == 3:
                    playerLocation = p.getLocation()
                    if 0.28 >= playerLocation[0] >= 0.20:
                        print('t1')
                        if playerLocation[1] < .64:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                        elif playerLocation[1] > 0.7:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    elif 0.39 >= round(playerLocation[0], 2) >= 0.29:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    elif 0.48 >= round(playerLocation[0], 2) >= 0.39:
                        if playerLocation[1] < .54:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                        elif playerLocation[1] > 0.6:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    elif 0.66 >= playerLocation[0] >= 0.49:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    elif 0.79 >= playerLocation[0] >= 0.67:
                        if playerLocation[1] < .59:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                        elif playerLocation[1] > 0.65:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    elif 0.92 >= playerLocation[0] >= 0.80:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    else:
                        print('t4')
                        print(round(playerLocation[0], 2))
                        if playerLocation[1] < .79:
                            p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                    if .99 > playerLocation[0] > .92 and playerLocation[1] > 0.79:
                        p.setLocation(playerLocation[0], 0.79)
                sleep(0.005)
            else:
                sleep(0.005)

    @staticmethod
    def changeLocation(p):
        while True:
            playerLocation = p.getLocation()
            playerLocation[0] = playerLocation[0] + p.getVelocityX()
            sleep(0.005)

    def loseLives(self, p):
        self.GameLives -= 1
        if self.GameLives == 0:
            self.GamePage = 0
            self.clearScreen()
            t = Label(self.GameWindow, text='GAME OVER', font=self.W_FONT, bg=self.W_BG, fg=self.C_RED)
            t.place(relx=.049, rely=.2)
            self.GamePage = 1
            self.drawPage(1)
            p.setLocation(0.05, .5)
        else:
            self.GameLivesRemaining.config(text=f'{self.GameLives} LIVES REMAINING')
            self.GameWindow.after(1, lambda: self.GameLivesRemaining.place(relx=.41, rely=.15))
            self.GameWindow.after(3000, lambda: self.GameLivesRemaining.place_forget())
            self.GamePage = 1
            self.drawPage(1)
            p.setLocation(0.05, .5)

    def checkBoundary(self, p):
        while True:
            playerLocation = p.getLocation()
            if playerLocation[1] > 0.85:
                self.loseLives(p)
            if playerLocation[0] <= -0.02:
                if self.GamePage > 1:
                    self.drawPage(self.GamePage - 1)
                    self.GamePage -= 1
                    p.setLocation(0.95, playerLocation[1])
            elif playerLocation[0] >= 1.01:
                self.drawPage(self.GamePage + 1)
                self.GamePage += 1
                p.setLocation(0.05, playerLocation[1])

            sleep(0.01)

    def updateLocation(self, p):
        while True:
            p.refresh()
            if self.G_GAMEMODE == 1:
                self.Session.send(';' + str(self.GamePage) + ';' + str(round(p.getLocation()[0], 2)) + ';' + str(round(p.getLocation()[1], 2)))
            sleep(0.001)

    def startGame(self, t):
        self.setGamemode(t)
        if t == 0:
            self.drawStart()
        else:
            self.clearScreen()
            b = Button(self.GameWindow, text='HOST', command=lambda: (b.place_forget(), b2.place_forget(), self.host()))
            b.pack()
            b2 = Button(self.GameWindow, text='JOIN', command=lambda: (b.place_forget(), b2.place_forget(), self.join()))
            b2.pack()

    def host(self):
        self.gs = 'host'
        self.T = Player(self.GameWindow, self.C_BLUE)
        self.T.draw(.1, .5)
        self.Session = Host(self.T, self)
        self.drawStart()
        self.Session.run()

    def join(self):
        self.gs = 'join'
        self.T = Player(self.GameWindow, self.C_BLUE)
        self.T.draw(.1, .5)
        self.Session = Join(self.T, self)
        # Thread(target=Session.startlisten, args=()).start()
        self.drawStart()
        self.Session.connect()
        self.Session.startlisten()

    def getPage(self):
        return self.GamePage

    def exitGame(self):
        self.GameWindow.destroy()

    def runGame(self):
        self.THREAD_WINDOW.start()

    def restartGame(self):
        pass

    def showConsole(self):
        pass

    def clearScreen(self):
        for GameAsset in self.GameAssets:
            GameAsset.place_forget()

    def changeSettings(self):
        for GameAsset in self.GameAssets:
            GameAsset.place_forget()
        self.THREAD_CONFIG.start()
        self.GameTitle.config(text='SETTINGS')
        self.GameTitle.place(relx=.05, rely=.1)
        self.SettingsVersion.place(relx=.75, rely=.85)

        self.SettingsHelp.place(relx=.051, rely=.35)
        self.SettingsHelpSwitch.place(0.275, 0.35)

        self.SettingsUpdate.place(relx=.051, rely=.45)
        self.SettingsUpdateSwitch.place(0.275, 0.45)

        self.SettingsLog.place(relx=.051, rely=.55)
        self.SettingsLogSwitch.place(0.275, 0.55)

        self.SettingsCheat.place(relx=.051, rely=.65)
        self.SettingsCheatSwitch.place(0.275, 0.65)

        self.SettingsPosition.place(relx=.38, rely=.35)
        self.SettingsPositionSwitch.place(0.604, 0.35)

        self.SettingsPage.place(relx=.38, rely=.45)
        self.SettingsPageSwitch.place(0.604, 0.45)

        Animate(self.GameWindow, .05, .1).scroll()

    def customizeScreen(self):
        for GameAsset in self.GameAssets:
            GameAsset.place_forget()
        self.GameTitle.config(text='CUSTOMIZE')
        self.GameTitle.place(relx=.05, rely=.1)
        Animate(self.GameWindow, .05, .1).scroll()

    def setGamemode(self, g):
        self.restartGame()
        self.G_GAMEMODE = g

    def showLocation(self, p):
        self.PlayerPosition.place(relx=.05, rely=.05)
        while True:
            self.currentLocation.set(f'L: {p.getLocation()[0]:.2f}, {p.getLocation()[1]:.2f} | X: {p.getVelocityX()}')
            sleep(0.01)


if __name__ == '__main__':
    Test = Game()
    Test.runGame()
