from tkinter import *
import _thread
import time
from tools.logger import Logger
import socket
import ast
import random


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
            self.setVelocityY(Username, 0.00)
            self.strVolX = '+0.01'

        def handleMovementL(event):
            self.setVelocityX(Username, -0.01)
            self.setVelocityY(Username, 0.00)
            self.strVolX = '-0.01'

        def handleMovementU(event):
            self.setVelocityY(Username, -0.01)
            self.setVelocityX(Username, 0.00)
            self.strVolY = '-0.01'

        def handleMovementD(event):
            self.setVelocityY(Username, 0.01)
            self.setVelocityX(Username, 0.00)
            self.strVolY = '+0.01'

        def handleMovementS(event):
            self.setVelocityY(Username, 0.00)
            self.setVelocityX(Username, 0.00)

        def handlePosW(event):
            if self.facing != 1:
                if self.facing == 4:
                    self.locations[self.locIndex][0] = self.locations[self.locIndex][0] + 0.028
                self.facing = 1
                self.locations[self.locIndex][1] = self.locations[self.locIndex][1] - 0.0625
                self.GAME_PIECE_PLAYER_2.config(text="""↑
●""")

        def handlePosS(event):
            pass
#            """
#            if self.facing != 3:
#                self.facing = 1
#                self.locations[self.locIndex][1] = self.locations[self.locIndex][1] + 0.0625
#                self.GAME_PIECE_PLAYER_2.config(text="""●
#↓""")

        def handlePosA(event):
            if self.facing != 4:
                if self.facing == 1:
                    self.locations[self.locIndex][1] = self.locations[self.locIndex][1] + 0.0625
                self.locations[self.locIndex][0] = self.locations[self.locIndex][0] - 0.028
                self.facing = 4
                self.GAME_PIECE_PLAYER_2.config(text="← ●")

        def handlePosD(event):
            if self.facing != 2:
                if self.facing == 1:
                    self.locations[self.locIndex][1] = self.locations[self.locIndex][1] + 0.0625
                elif self.facing == 4:
                    self.locations[self.locIndex][0] = self.locations[self.locIndex][0] + 0.028
                self.facing = 2
                self.GAME_PIECE_PLAYER_2.config(text="● →")
        

        self.gamePlayers = ['Shivam', 'TEST', 'TEST2', 'TEST3']
        self.velocityX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.velocityY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.hasConnected = False
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.locations = [[0.05, 0.25], [0.05, 0.45], [0.05, 0.65], [0.05, 0.85]]

        self.Window = Tk()
        self.Window.geometry(self.WINDOW_RESOLUTION)
        self.Window.configure(bg=self.WINDOW_BACKGROUND)
        self.Window.title(self.WINDOW_TITLE)

        self.locIndex = self.gamePlayers.index(uName)
        
        self.facing = 3

        self.tickrate = 40
        self.strVolX = '+0.00'
        self.strVolY = '-0.00'

        self.currentPosition = StringVar()
        self.currentPosition.set(f'X: {self.getVelocityX(Username)} ● Y: {self.getVelocityY(Username)} | {self.locations[self.locIndex][0]:.2f}, {self.locations[self.locIndex][1]:.2f}  [TR: {self.tickrate}] [User: {Username}]')

        self.notificationText = StringVar()
        self.notificationText.set(f'{uName} joined the game.')

        self.Window.bind('<Right>', handleMovementR)
        self.Window.bind('<Left>', handleMovementL)
        self.Window.bind('<Up>', handleMovementU)
        self.Window.bind('<Down>', handleMovementD)
        self.Window.bind('<space>', handleMovementS)

        self.Window.bind('w', handlePosW)
        self.Window.bind('W', handlePosW)
        self.Window.bind('s', handlePosS)
        self.Window.bind('S', handlePosS)
        self.Window.bind('a', handlePosA)
        self.Window.bind('A', handlePosA)
        self.Window.bind('d', handlePosD)
        self.Window.bind('D', handlePosD)

        self.GAME_PIECE_PLAYER_1 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#e74c3c', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_1.place(relx=.05, rely=.25)

        self.GAME_PIECE_PLAYER_2 = Label(self.Window, text="""●
↓""", bg=self.WINDOW_BACKGROUND, fg='#16a085', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_2.place(relx=.05, rely=.45)

        self.GAME_PIECE_PLAYER_3 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#3498db', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_3.place(relx=.05, rely=.65)

        self.GAME_PIECE_PLAYER_4 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#f39c12', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_4.place(relx=.05, rely=.85)

        self.currentVelocityX = Label(self.Window, textvariable=self.currentPosition, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND, font=('Courier New', 12, 'bold'))
        self.currentVelocityX.place(relx=.025, rely=.02)

        self.notification = Label(self.Window, textvariable=self.notificationText, bg=self.WINDOW_BACKGROUND, fg='#e74c3c', font=('Courier New', 12, 'bold'))
        self.notification.place(relx=.025, rely=.90)

        self.gamePieces = [self.GAME_PIECE_PLAYER_1, self.GAME_PIECE_PLAYER_2, self.GAME_PIECE_PLAYER_3, self.GAME_PIECE_PLAYER_4]

        self.Window.after(3000, lambda: self.notificationText.set(''))

        self.currentItemCoords = [0, 0]

        Logger.log(f"Launched game window -  running on {self.tickrate} tickrate.")

        # _thread.start_new_thread(self.updatePieces, ())
        _thread.start_new_thread(self.startListening, ())
        _thread.start_new_thread(self.updatePieces, ())
        # _thread.start_new_thread(self.makeItems, ())
        _thread.start_new_thread(self.Window.mainloop(), )

    def makeItems(self):
        while True:
            time.sleep(random.randint(2, 5))
            locX2 = random.uniform(0.20, 0.90)
            locY2 = random.uniform(0.20, 0.85)
            self.clientSocket.send(str.encode(f'ITEM<>{locX2:.2f},{locY2:.2f}'))

    def setVelocityX(self, playerName, velocityX):
        self.velocityX[self.gamePlayers.index(playerName)] = velocityX

    def getVelocityX(self, playerName):
        return self.velocityX[self.gamePlayers.index(playerName)]

    def setVelocityY(self, playerName, velocityY):
        self.velocityY[self.gamePlayers.index(playerName)] = velocityY

    def getVelocityY(self, playerName):
        return self.velocityY[self.gamePlayers.index(playerName)]

    def setOLoc(self, x, y, u):
        self.locations[self.gamePlayers.index(u)][0] = float(x)
        self.locations[self.gamePlayers.index(u)][1] = float(y)
        self.gamePieces[self.gamePlayers.index(u)].place_forget()
        self.Window.after(1, (self.gamePieces[self.gamePlayers.index(u)].place(relx=self.locations[self.gamePlayers.index(u)][0], rely=self.locations[self.gamePlayers.index(u)][1])))

    def updatePieces(self):
        while True:

            time.sleep(1 / self.tickrate)

            if self.getVelocityX(Username) < 0:
                if self.locations[self.locIndex][0] > 0.02:
                    self.locations[self.locIndex][0] = self.locations[self.locIndex][0] + self.getVelocityX(Username)
            else:
                if self.locations[self.locIndex][0] < 0.96:
                    self.locations[self.locIndex][0] = self.locations[self.locIndex][0] + self.getVelocityX(Username)

            if self.getVelocityY(Username) < 0:
                if self.locations[self.locIndex][1] > 0.02:
                    self.locations[self.locIndex][1] = self.locations[self.locIndex][1] + self.getVelocityY(Username)
            else:
                if self.locations[self.locIndex][1] < 0.88:
                    self.locations[self.locIndex][1] = self.locations[self.locIndex][1] + self.getVelocityY(Username)

            diffX = self.locations[self.locIndex][0] - 1.00
            diffY = self.locations[self.locIndex][1] - 1.00

            if diffX < 0:
                diffX = diffX * -1

            if diffY < 0:
                diffY = diffY * -1

            diffXItem = self.currentItemCoords[0] - 1
            diffYItem = self.currentItemCoords[1] - 1

            if diffXItem < 0:
                diffXItem = diffXItem * -1

            if diffYItem < 0:
                diffYItem = diffYItem * -1

            if diffXItem - 0.03 < diffX < diffXItem + 0.03:
                if diffYItem - 0.03 < diffY < diffYItem + 0.03:
                    self.tempItem.place_forget()
                    self.currentItemCoords = [0, 0]
                    self.notificationText.set('Received power-up!')
                    self.Window.after(3000, lambda: self.notificationText.set(''))

                    print('IN BOX, ', diffY, diffX)


            xloc = self.locations[self.locIndex][0]
            yloc = self.locations[self.locIndex][1]

            self.clientSocket.send(str.encode(f'POSITION<>{Username}<>{float(xloc):.2f},{float(yloc):.2f}'))

            self.currentPosition.set(f'X: {self.getVelocityX(Username)} ● Y: {self.getVelocityY(Username)} | {self.locations[self.locIndex][0]:.2f}, {self.locations[self.locIndex][1]:.2f}  [TR: {self.tickrate}] [User: {Username}]')
            self.gamePieces[self.gamePlayers.index(Username)].place_forget()
            self.Window.after(1, (self.gamePieces[self.gamePlayers.index(Username)].place(relx=self.locations[self.locIndex][0], rely=self.locations[self.locIndex][1])))

    def createItem(self, x, y):
        self.tempItem = Label(self.Window, text='▲', fg=self.WINDOW_FOREGROUND, bg=self.WINDOW_BACKGROUND)
        self.tempItem.place(relx=x, rely=y)

        self.currentItemCoords = [x, y]

        self.Window.after(5000, lambda: self.tempItem.place_forget())

    def startListening(self):
        # _thread.start_new_thread(self.makeItems, ())
        try:
            self.clientSocket.connect((self.IP, self.PORT))
            self.hasConnected = True
            self.clientSocket.send(str.encode(f'USERNAME<>{Username}'))
            Logger.log('Connected to server correctly.')
            # self.clientSocket.send(str.encode('CLIENT_INFORMATION<>' + str(clientInformation)))
        except Exception as e:
            self.notificationText.set('Could not connect to the local server.')
            self.Window.after(3000, lambda: self.notificationText.set(''))
            Logger.error(e)
            Logger.log('Failed to connect to the local game server.', 'ERROR')
        if self.hasConnected:
            while True:
                try:
                    receive_data = self.clientSocket.recv(27)
                    # print(receive_data.decode())
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
                    elif arguments[0] == 'ITEM':
                        # print(receive_data.decode())
                        posArgs2 = receive_data.decode().strip('ITEM<>')
                        posArgs2 = posArgs2.split(',')
                        self.createItem(float(posArgs2[0]), float(posArgs2[1]))
                    elif arguments[0] == 'USER_LIST':
                        all_users = arguments[1].split(';')
                        for user in all_users:
                            if user is not '':
                                Logger.log(user, 'USER LIST')
                    elif arguments[0] == 'POSITION':
                        # print(receive_data.decode())
                        userName = arguments[1]
                        if userName != Username:
                            Logger.log('handling', userName)
                            posArgs = receive_data.decode().strip('POSITION<>' + userName)
                            posArgs = posArgs.split(',')
                            self.setOLoc(posArgs[0], posArgs[1], userName)

                except Exception as e:
                    self.notificationText.set('Lost connection to the game server.')
                    self.Window.after(3000, lambda: self.notificationText.set(''))
                    Logger.error(e)
                    Logger.log('Lost connection to the game server or received invalid data.', 'ERROR')
                    break


# Username = input('U: ')
Username = 'TEST'

clientInformation = {'Client Information': {'Username': Username, 'Version': '5.00', 'Rank': 'User'}}

if __name__ == '__main__':
    T = Connect(Username)
