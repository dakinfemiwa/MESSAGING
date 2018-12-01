from tkinter import *
from threading import Thread
from tools.animator import Animate
from tools.Player import Player
from tools.Switch import Switch
from time import sleep
# from tools.error import Error


class Game:
    def __init__(self):
        self.W_BG = '#2F3542'
        self.W_FG = '#FFFFFF'
        self.W_SIZE = '600x300'
        self.W_TITLE = 'PLACEHOLDER'

        self.W_FONT = ('MS PGothic', 30, 'bold')
        self.W_FONT2 = ('MS PGothic', 12, 'bold')
        self.W_FONT3 = ('MS PGothic', 10, 'bold')
        self.W_FONT4 = ('MS PGothic', 11, 'bold')

        self.G_GAMEMODE = 0
        self.GamePage = 1
        self.GameLives = 3

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

        self.C_RED = '#E74C3C'
        self.C_GREEN = '#2ECC71'
        self.C_ORANGE = '#F39C12'
        self.C_BLUE = '#3498DB'
        self.C_YELLOW = '#F1C40F'
        self.C_GRAY = '#95A5A6'
        self.C_LIGHTGRAY = '#BDC3C7'

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

        self.SettingsHelpSwitch = Switch(self.GameWindow)
        self.SettingsUpdateSwitch = Switch(self.GameWindow)
        self.SettingsLogSwitch = Switch(self.GameWindow)
        self.SettingsCheatSwitch = Switch(self.GameWindow)

        self.currentLocation = StringVar()
        self.PlayerPosition = Label(self.GameWindow, textvariable=self.currentLocation, font=self.W_FONT3, bg=self.W_BG, fg=self.C_GRAY)

        self.GameAssets = [self.GameTitle, self.GameSingleplayer, self.GameMultiplayer, self.GameCustomize, self.GameSettings, self.GameExitGame]
        self.SettingsAssets = [self.SettingsVersion]

        self.THREAD_MOVEMENT = Thread(target=self.handleMovement, args=())
        self.THREAD_WINDOW = Thread(target=self.GameWindow.mainloop())

    def drawStart(self):

        global lPressed, rPressed

        lPressed = False
        rPressed = False

        def evJump(event):
            global lPressed, rPressed
            if lPressed:
                P.jump(0)
            elif rPressed:
                P.jump(1)
            else:
                P.jump(2)

        def evLeft(event):
            global lPressed, rPressed
            lPressed = True
            P.setVelocityX(-0.0025)

        def evRight(event):
            global lPressed, rPressed
            rPressed = True
            P.setVelocityX(0.0025)

        def evStopL(event):
            global lPressed, rPressed
            lPressed = False
            if not rPressed:
                P.setVelocityX(0)

        def evStopR(event):
            global lPressed, rPressed
            rPressed = False
            if not lPressed:
                P.setVelocityX(0)

        self.clearScreen()
        #self.whiteFloor = Label(self.GameWindow, bg=self.W_FG, height=3, width=100)
        #self.whiteFloor.place(relx=.0, rely=.85)
        P = Player(self.GameWindow, 'white')
        P.draw(.05, .5)
        self.GameWindow.bind('<Up>', evJump)
        self.GameWindow.bind('<Right>', evRight)
        self.GameWindow.bind('<Left>', evLeft)
        self.GameWindow.bind('<KeyRelease-Left>', evStopL)
        self.GameWindow.bind('<KeyRelease-Right>', evStopR)
        gThread = Thread(target=self.moveDown, args=(P, )).start()
        uThread = Thread(target=self.updateLocation, args=(P, )).start()
        cThread = Thread(target=self.changeLocation, args=(P, )).start()
        pThread = Thread(target=self.showLocation, args=(P, )).start()
        bThread = Thread(target=self.checkBoundary, args=(P, )).start()
        self.drawPage(1)
        self.GameWindow.after(1, lambda: self.GameLivesRemaining.place(relx=.37, rely=.15))
        self.GameWindow.after(3000, lambda: self.GameLivesRemaining.place_forget())

    def drawPage(self, n):
        if n == 1:
            self.whiteFloor = Label(self.GameWindow, bg=self.W_FG, height=3, width=100)
            self.whiteFloor.place(relx=.0, rely=.85)
        elif n == 2:
            self.whiteFloor.place_forget()
            self.whiteFloor2 = Label(self.GameWindow, bg=self.W_FG, height=3, width=43)
            self.whiteFloor2.place(relx=.0, rely=.85)

            self.whiteFloor3 = Label(self.GameWindow, bg=self.W_FG, height=3, width=100)
            self.whiteFloor3.place(relx=.72, rely=.85)

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
                    elif playerLocation[1] <= 1.10 and 0.5 < playerLocation[0] < 0.7:
                        p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                sleep(0.005)
            else:
                sleep(0.005)

    def changeLocation(self, p):
        while True:
            playerLocation = p.getLocation()
            playerLocation[0] = playerLocation[0] + p.getVelocityX()
            sleep(0.005)

    def loseLives(self, p):
        playerLocation = p.getLocation()
        self.GameLives -= 1
        if self.GameLives == 0:
            print('Game over!')
        else:
            self.GameLivesRemaining.config(text=f'{self.GameLives} LIVES REMAINING')
            self.GameWindow.after(1, lambda: self.GameLivesRemaining.place(relx=.37, rely=.15))
            self.GameWindow.after(3000, lambda: self.GameLivesRemaining.place_forget())
            self.GamePage = 1
            self.drawPage(1 )
            p.setLocation(0.05, .5)

    def checkBoundary(self, p):
        while True:
            playerLocation = p.getLocation()
            if playerLocation[1] > 0.9:
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
            sleep(0.001)

    def startGame(self, t):
        self.setGamemode(t)
        self.drawStart()
        self.THREAD_MOVEMENT.start()

    def exitGame(self):
        self.GameWindow.destroy()

    def runGame(self):
        self.THREAD_WINDOW.start()

    def restartGame(self):
        pass

    def showConsole(self):
        pass

    def handleMovement(self):
        pass

    def clearScreen(self):
        for GameAsset in self.GameAssets:
            GameAsset.place_forget()

    def changeSettings(self):
        for GameAsset in self.GameAssets:
            GameAsset.place_forget()
        self.GameTitle.config(text='SETTINGS')
        self.GameTitle.place(relx=.05, rely=.1)
        self.SettingsVersion.place(relx=.75, rely=.85)

        self.SettingsHelp.place(relx=.051, rely=.35)
        self.SettingsHelpSwitch.place(0.3, 0.35)

        self.SettingsUpdate.place(relx=.051, rely=.45)
        self.SettingsUpdateSwitch.place(0.3, 0.45)

        self.SettingsLog.place(relx=.051, rely=.55)
        self.SettingsLogSwitch.place(0.3, 0.55)

        self.SettingsCheat.place(relx=.051, rely=.65)
        self.SettingsCheatSwitch.place(0.3, 0.65)

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
