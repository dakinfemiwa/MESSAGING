from tkinter import *
from threading import Thread
from time import sleep


class Enemy:
    def __init__(self, w, p, c='red', g=None):
        self.Velocity = [0.00, 0.00]
        self.Location = [0.00, 0.00]
        self.Colour = c
        self.Window = w
        self.GamePlayers = []
        self.GamePlayers.append(p)
        self.GameInstance = g

        self.BulletCooldown = False

        self.ShootingLeft = False
        self.ShootingRight = False

        self.EnemyItem = Label(self.Window, text='❰ ❱', font=('Arial', 14, 'bold'), fg=self.Colour, bg='#2F3542', width=2, height=1)

        self.THREAD_AI = Thread(target=self.moveAround, args=())
        self.THREAD_MOVEMENT = Thread(target=self.updateLocation, args=())
        self.THREAD_AROUND = Thread(target=self.checkSurroundings, args=())
        self.THREAD_SHOOT = Thread(target=self.startShooting, args=())

    def setCooldown(self):
        self.BulletCooldown = True
        sleep(0.9)
        self.BulletCooldown = False

    def moveAround(self):
        while True:
            self.setVelocityX(-0.0025)
            sleep(1)
            self.setVelocityX(+0.0025)
            sleep(1)

    def updateLocation(self):
        while True:
            currentLocation = self.getLocation()
            self.setLocation(currentLocation[0] + self.getVelocityX(), currentLocation[1])
            self.refresh()
            sleep(0.01)

    def checkSurroundings(self):
        while True:
            for p in self.GamePlayers:
                playerLocation = p.getLocation()
                enemyLocation = self.getLocation()
                if abs(playerLocation[0]-enemyLocation[0]) < 0.35:
                    if playerLocation[0] < enemyLocation[0]:
                        self.ShootingLeft = True
                    else:
                        self.ShootingRight = True
                else:
                    self.ShootingLeft = False
                    self.ShootingRight = False
            sleep(0.02)

    def startShooting(self):
        from tools.Bullet import Bullet
        while True:
            if not self.BulletCooldown:
                if self.ShootingLeft:
                    B = Bullet(self.Window, c='#f1c40f', p=self.GamePlayers[0], g=self.GameInstance)
                    B.draw(self.getLocation()[0], self.getLocation()[1])
                    B.setMovement(0)
                if self.ShootingRight:
                    B2 = Bullet(self.Window, c='#f1c40f', p=self.GamePlayers[0], g=self.GameInstance)
                    B2.draw(self.getLocation()[0], self.getLocation()[1])
                    B2.setMovement(1)
                Thread(target=self.setCooldown(), args=()).start()
            sleep(0.01)

    def draw(self, x, y):
        self.Location = [x, y]
        self.EnemyItem.place(relx=x, rely=y)
        self.THREAD_AI.start()
        self.THREAD_MOVEMENT.start()
        self.THREAD_AROUND.start()
        self.THREAD_SHOOT.start()

    def hide(self):
        self.EnemyItem.place_forget()

    def refresh(self):
        self.EnemyItem.place(relx=self.getLocation()[0], rely=self.getLocation()[1])

    def setVelocityX(self, v):
        self.Velocity[0] = v

    def setVelocityY(self, v):
        self.Velocity[1] = v

    def getVelocityX(self):
        return self.Velocity[0]

    def getVelocityY(self):
        return self.Velocity[1]

    def getLocation(self):
        return self.Location

    def setLocation(self, x, y):
        self.Location = [x, y]


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x200')
    Test = Enemy(root, 't', c='green')
    button = Button(command=lambda: Test.draw(.45, .8)).pack()
    root.mainloop()
