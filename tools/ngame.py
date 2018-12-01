from tkinter import *
from threading import Thread
from tools.animator import Animate
from tools.Player import Player
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

        self.G_GAMEMODE = 0
        self.G_PAGE = 0

        self.S_GAME = 'PLACEHOLDER'
        self.S_SINGLEPLAYER = 'SINGLE-PLAYER'
        self.S_MULTIPLAYER = 'MULTI-PLAYER'
        self.S_CUSTOMIZE = 'CUSTOMIZE'
        self.S_SETTINGS = 'SETTINGS'
        self.S_EXITGAME = 'EXIT GAME'
        self.S_HELP = 'SHOW HELP'

        self.S_VERSION = 'Version A - 0.1'

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

        self.SettingsVersion = Label(self.GameWindow, text=self.S_VERSION, font=self.W_FONT2, bg=self.W_BG, fg=self.C_GRAY)
        self.SettingsHelp = Label(self.GameWindow, text=self.S_HELP, font=self.W_FONT2, bg=self.W_BG, fg=self.C_LIGHTGRAY)

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
        whiteFloor = Label(self.GameWindow, bg=self.W_FG, height=3, width=100)
        whiteFloor.place(relx=.0, rely=.85)
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

    def moveDown(self, p):
        while True:
            if p.gravity():
                playerLocation = p.getLocation()
                if playerLocation[1] < .79:
                    p.setLocation(playerLocation[0], playerLocation[1] + 0.005)
                sleep(0.005)
            else:
                sleep(0.005)

    def changeLocation(self, p):
        while True:
            playerLocation = p.getLocation()
            playerLocation[0] = playerLocation[0] + p.getVelocityX()
            sleep(0.005)

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


if __name__ == '__main__':
    Test = Game()
    Test.runGame()
