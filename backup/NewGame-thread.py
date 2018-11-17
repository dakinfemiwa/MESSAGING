from tkinter import *
import _thread
import threading
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

        def createBullet(event):
            bulletVelocity = [self.getVelocityX(Username) * 2, self.getVelocityY(Username) * 2]
            self.clientSocket.send(str.encode(f'BALL<>{self.locations[self.locIndex][0]:.2f},{self.locations[self.locIndex][1]:.2f},{bulletVelocity[0]},{bulletVelocity[1]},{self.playerColours[self.locIndex]}'))

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

        self.gamePlayers = ['Shivam', 'TEST', 'TEST2', 'TEST3']
        self.velocityX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.velocityY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.hasConnected = False
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.locations = [[0.05, 0.15], [0.05, 0.35], [0.05, 0.55], [0.05, 0.75]]
        self.playerColours = ['#e74c3c', '#16a085', '#3498db', '#f39c12']

        self.Window = Tk()
        self.Window.geometry(self.WINDOW_RESOLUTION)
        self.Window.configure(bg=self.WINDOW_BACKGROUND)
        self.Window.title(self.WINDOW_TITLE)

        self.locIndex = self.gamePlayers.index(uName)

        self.speed = 40
        self.strVolX = '+0.00'
        self.strVolY = '-0.00'

        self.currentPosition = StringVar()
        self.currentPosition.set(f'X: {self.getVelocityX(Username)} ● Y: {self.getVelocityY(Username)} | {self.locations[self.locIndex][0]:.2f}, {self.locations[self.locIndex][1]:.2f}  [SP: {self.speed}] [User: {Username}]')

        self.notificationText = StringVar()
        self.notificationText.set(f'{uName} joined the game.')

        self.mainNotification = StringVar()
        self.mainNotification.set('TEST')

        self.Window.bind('<Right>', handleMovementR)
        self.Window.bind('<Left>', handleMovementL)
        self.Window.bind('<Up>', handleMovementU)
        self.Window.bind('<Down>', handleMovementD)
        self.Window.bind('<space>', handleMovementS)
        self.Window.bind('z', createBullet)
        self.Window.bind('Z', createBullet)

        self.bullet = None
        self.tempItem = None

        self.GAME_PIECE_PLAYER_1 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#e74c3c', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_1.place(relx=.05, rely=.15)

        self.GAME_PIECE_PLAYER_2 = Label(self.Window, text="●", bg=self.WINDOW_BACKGROUND, fg='#16a085', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_2.place(relx=.05, rely=.435)

        self.GAME_PIECE_PLAYER_3 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#3498db', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_3.place(relx=.05, rely=.55)

        self.GAME_PIECE_PLAYER_4 = Label(self.Window, text='●', bg=self.WINDOW_BACKGROUND, fg='#f39c12', font=('Segoe UI', 12, 'bold'))
        self.GAME_PIECE_PLAYER_4.place(relx=.05, rely=.75)

        self.currentVelocityX = Label(self.Window, textvariable=self.currentPosition, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND, font=('Courier New', 12, 'bold'))
        self.currentVelocityX.place(relx=.025, rely=.02)

        self.notification = Label(self.Window, textvariable=self.notificationText, bg=self.WINDOW_BACKGROUND, fg='#e74c3c', font=('Courier New', 12, 'bold'))
        self.notification.place(relx=.025, rely=.90)

        self.gamePieces = [self.GAME_PIECE_PLAYER_1, self.GAME_PIECE_PLAYER_2, self.GAME_PIECE_PLAYER_3, self.GAME_PIECE_PLAYER_4]

        self.Window.after(3000, lambda: self.notificationText.set(''))

        self.currentItemCoords = [0, 0]

        Logger.log(f"Launched game window -  running on {self.speed} speed.")

        threading.Thread(target=self.startListening, args=()).start()
        threading.Thread(target=self.updatePieces, args=()).start()
        threading.Thread(target=self.Window.mainloop()).start()

    def drawBullet(self, lx, ly, velx, vely, col):
        self.bullet = Label(self.Window, text='-', font=('Segoe UI', 14, 'bold'), fg=col, bg=self.WINDOW_BACKGROUND)
        threading.Thread(target=self.updateItem, args=(self.bullet, lx, ly, velx, vely)).start()

    def updateItem(self, item, lx, ly, vx, vy):
        localNewLX = lx
        localNewLY = ly
        while True:
            time.sleep(1 / self.speed)
            localNewLX = float(localNewLX) + float(vx)
            localNewLY = float(localNewLY) + float(vy)

            item.place(relx=localNewLX, rely=localNewLY)

            try:
                diffXItem = float(localNewLX) - 1
                diffYItem = float(localNewLY) - 1

                if diffXItem < 0:
                    diffXItem = diffXItem * -1

                if diffYItem < 0:
                    diffYItem = diffYItem * -1

                if 1 < float(localNewLX) or float(localNewLX) < 0:
                    item.place_forget()
                    item = None
                    break

                if 1 < float(localNewLY) or float(localNewLY) < 0:
                    item.place_forget()
                    item = None
                    break

                cached = self.locations

                playerDifferenceX = cached[self.locIndex][0] - 1.00
                playerDifferenceY = cached[self.locIndex][1] - 1.00

                differenceX1 = cached[0][0] - 1.00
                differenceY1 = cached[0][1] - 1.00

                differenceX2 = cached[1][0] - 1.00
                differenceY2 = cached[1][1] - 1.00

                differenceX3 = cached[2][0] - 1.00
                differenceY3 = cached[2][1] - 1.00

                differenceX4 = cached[3][0] - 1.00
                differenceY4 = cached[3][1] - 1.00

                preDifferences = [[differenceX1, differenceY1], [differenceX2, differenceY2], [differenceX3, differenceY3], [differenceX4, differenceY4]]

                for uncheckedDifference in preDifferences:
                    diffIndex = preDifferences.index(uncheckedDifference)
                    if uncheckedDifference[0] < 0:
                        uncheckedDifference[0] = uncheckedDifference[0] * -1
                    if uncheckedDifference[1] < 0:
                        uncheckedDifference[1] = uncheckedDifference[1] * -1
                    preDifferences[diffIndex] = uncheckedDifference

                allDifferences = preDifferences

                if playerDifferenceX < 0:
                    playerDifferenceX = playerDifferenceX * -1

                if playerDifferenceY < 0:
                    playerDifferenceY = playerDifferenceY * -1

                differenceIndex = allDifferences.index([playerDifferenceX, playerDifferenceY])

                differenceHit = None

                for difference in allDifferences:
                    if diffXItem - 0.04 < difference[0] < diffXItem + 0.04:
                        if diffYItem - 0.04 < difference[1] < diffYItem + 0.04:
                            differenceHitT = allDifferences.index(difference)
                            if item.cget("foreground") != self.playerColours[differenceHitT]:
                                item.place_forget()
                                item = None
                                differenceHit = allDifferences.index(difference)
                                break

                if differenceHit is not None:
                    if differenceHit == differenceIndex:
                        self.notificationText.set('You were hit!')
                        self.Window.after(3000, lambda: self.notificationText.set(''))
                    else:
                        self.notificationText.set(f'{[self.gamePlayers[differenceHitT]][0]} was hit by {self.gamePlayers[differenceIndex]}')
                        self.Window.after(3000, lambda: self.notificationText.set(''))
                    break

            except Exception as e:
                Logger.error(e)

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
            time.sleep(1 / self.speed)

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

            xloc = self.locations[self.locIndex][0]
            yloc = self.locations[self.locIndex][1]

            self.clientSocket.send(str.encode(f'POSITION<>{Username}<>{float(xloc):.2f},{float(yloc):.2f}'))

            self.currentPosition.set(f'X: {self.getVelocityX(Username)} ● Y: {self.getVelocityY(Username)} | {self.locations[self.locIndex][0]:.2f}, {self.locations[self.locIndex][1]:.2f}  [SP: {self.speed}] [User: {Username}]')
            self.gamePieces[self.gamePlayers.index(Username)].place_forget()
            self.Window.after(1, (self.gamePieces[self.gamePlayers.index(Username)].place(relx=self.locations[self.locIndex][0], rely=self.locations[self.locIndex][1])))

    def createItem(self, x, y):
        self.tempItem = Label(self.Window, text='▲', fg=self.WINDOW_FOREGROUND, bg=self.WINDOW_BACKGROUND)
        self.tempItem.place(relx=x, rely=y)
        self.currentItemCoords = [x, y]
        self.Window.after(5000, lambda: self.tempItem.place_forget())

    def startListening(self):
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
                    receive_data = self.clientSocket.recv(35)
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
                    elif arguments[0] == 'BALL':
                        posArgs3 = receive_data.decode().strip('BALL<>')
                        posArgs3 = posArgs3.split(',')
                        self.drawBullet(posArgs3[0], posArgs3[1], posArgs3[2], posArgs3[3], posArgs3[4])
                    elif arguments[0] == 'POSITION':
                        # print(receive_data.decode())
                        userName = arguments[1]
                        if userName != Username:
                            posArgs = receive_data.decode().strip('POSITION<>' + userName)
                            posArgs = posArgs.split(',')
                            self.setOLoc(posArgs[0], posArgs[1], userName)

                except Exception as e:
                    self.notificationText.set('Lost connection to the game server.')
                    self.Window.after(3000, lambda: self.notificationText.set(''))
                    Logger.error(e)
                    Logger.log('Lost connection to the game server or received invalid data.', 'ERROR')
                    break


Username = input('U: ').upper()
# Username = 'TEST2'

clientInformation = {'Client Information': {'Username': Username, 'Version': '5.00', 'Rank': 'User'}}

if __name__ == '__main__':
    T = Connect(Username)
