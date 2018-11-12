from tkinter import *
import _thread
import time
from tools.logger import Logger
import socket
import ast


class Connect:
    def __init__(self, uName):
        self.WINDOW_BACKGROUND = '#141414'
        self.WINDOW_FOREGROUND = '#FFFFFF'
        self.WINDOW_RESOLUTION = '600x350'
        self.WINDOW_TITLE = 'Placeholder'

        self.IP = '127.0.0.1'
        self.PORT = 6666

        def handleMovementR(event):
            self.setVelocityX(Username, 0.01)
            self.setVelocityY(Username, 0)

        def handleMovementL(event):
            self.setVelocityX(Username, -0.01)
            self.setVelocityY(Username, 0)

        def handleMovementU(event):
            self.setVelocityY(Username, -0.01)
            self.setVelocityX(Username, 0)

        def handleMovementD(event):
            self.setVelocityY(Username, 0.01)
            self.setVelocityX(Username, 0)

        def handleMovementS(event):
            self.setVelocityY(Username, 0)
            self.setVelocityX(Username, 0)

        self.gamePlayers = [Username]
        self.velocityX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.velocityY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.hasConnected = False
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.Window = Tk()
        self.Window.geometry(self.WINDOW_RESOLUTION)
        self.Window.configure(bg=self.WINDOW_BACKGROUND)
        self.Window.title(self.WINDOW_TITLE)

        self.locationX = 0.05
        self.locationY = 0.35
        self.tickrate = 40

        self.currentPosition = StringVar()
        self.currentPosition.set(f'X: {self.getVelocityX(Username)} ● Y: {self.getVelocityY(Username)} | {self.locationX}, {self.locationY}  [Tickrate: {self.tickrate}')

        self.notificationText = StringVar()
        self.notificationText.set(f'{uName} joined the game.')

        self.Window.bind('<Right>', handleMovementR)
        self.Window.bind('<Left>', handleMovementL)
        self.Window.bind('<Up>', handleMovementU)
        self.Window.bind('<Down>', handleMovementD)
        self.Window.bind('<space>', handleMovementS)

        self.GAME_PIECE_PLAYER_1 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#e74c3c', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_1.place(relx=.05, rely=.35)

        self.currentVelocityX = Label(self.Window, textvariable=self.currentPosition, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND, font=('Courier New', 12, 'bold'))
        self.currentVelocityX.place(relx=.025, rely=.02)

        self.notification = Label(self.Window, textvariable=self.notificationText, bg=self.WINDOW_BACKGROUND, fg='#e74c3c', font=('Courier New', 12, 'bold'))
        self.notification.place(relx=.025, rely=.90)

        self.gamePieces = [self.GAME_PIECE_PLAYER_1]

        self.Window.after(3000, lambda: self.notificationText.set(''))

        Logger.log(f"Launched game window -  running on {self.tickrate} tickrate.")

        _thread.start_new_thread(self.updatePieces, ())
        _thread.start_new_thread(self.startListening, ())
        _thread.start_new_thread(self.Window.mainloop(), ())

    def setVelocityX(self, playerName, velocityX):
        self.velocityX[self.gamePlayers.index(playerName)] = velocityX

    def getVelocityX(self, playerName):
        return self.velocityX[self.gamePlayers.index(playerName)]

    def setVelocityY(self, playerName, velocityY):
        self.velocityY[self.gamePlayers.index(playerName)] = velocityY

    def getVelocityY(self, playerName):
        return self.velocityY[self.gamePlayers.index(playerName)]

    def updatePieces(self):
        while True:

            if self.getVelocityX(Username) < 0:
                if self.locationX > 0.02:
                    self.locationX = self.locationX + self.getVelocityX(Username)
            else:
                if self.locationX < 0.96:
                    self.locationX = self.locationX + self.getVelocityX(Username)

            if self.getVelocityY(Username) < 0:
                if self.locationY > 0.02:
                    self.locationY = self.locationY + self.getVelocityY(Username)
            else:
                if self.locationY < 0.88:
                    self.locationY = self.locationY + self.getVelocityY(Username)

            self.currentPosition.set(f'X: {self.getVelocityX(Username):.2f} ● Y: {self.getVelocityY(Username):.2f} | {self.locationX:.2f}, {self.locationY:.2f} -- Tickrate: {self.tickrate}')
            self.GAME_PIECE_PLAYER_1.place_forget()
            self.Window.after(1, (self.GAME_PIECE_PLAYER_1.place(relx=self.locationX, rely=self.locationY)))

            time.sleep(1 / self.tickrate)

    def startListening(self):
        try:
            self.clientSocket.connect((self.IP, self.PORT))
            self.hasConnected = True
            self.clientSocket.send(str.encode('CLIENT_INFORMATION<>' + str(clientInformation)))
        except Exception as e:
            self.notificationText.set('Could not connect to the local server.')
            self.Window.after(3000, lambda: self.notificationText.set(''))
            Logger.error(e)
            Logger.log('Failed to connect to the local game server.', 'ERROR')
        if self.hasConnected:
            while True:
                try:
                    receive_data = self.clientSocket.recv(4096)
                    arguments = receive_data.decode().split('<>')
                    if arguments[0] == 'CONN_ERROR':
                        Logger.log('Server rejected connection based on client information.', 'DISCONNECT')
                        Logger.log(arguments[1])
                        break
                    elif arguments[0] == 'CONN_SUCCESS':
                        Logger.log(arguments[1])
                    elif arguments[0] == 'SERVER_INFORMATION':
                        serverInfo = ast.literal_eval(str(arguments[1]))
                        serverData = []
                        for field in ['Server Name', 'Uptime', 'Minimum Version', 'Server Version']:
                            serverData.append(serverInfo['Server Information'][field])
                            Logger.log(f'{field}: {str(serverInfo["Server Information"][field])}', 'SERVER')
                    elif arguments[0] == 'USER_LIST':
                        all_users = arguments[1].split(';')
                        for user in all_users:
                            if user is not '':
                                Logger.log(user, 'USER LIST')
                except Exception as e:
                    self.notificationText.set('Lost connection to the game server.')
                    self.Window.after(3000, lambda: self.notificationText.set(''))
                    Logger.error(e)
                    Logger.log('Lost connection to the game server or received invalid data.', 'ERROR')
                    break


Username = "Shivam"

clientInformation = {'Client Information': {'Username': Username, 'Version': '5.00', 'Rank': 'User'}}

if __name__ == '__main__':
    T = Connect(Username)
