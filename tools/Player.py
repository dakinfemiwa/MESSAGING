from tkinter import *
from threading import Thread
from time import sleep
from tools.animator import Animate
# from tools.error import Error


class Player:
    def __init__(self, w, c='red'):
        self.Gravity = True
        self.Velocity = [0.00, 0.00]
        self.Location = [0.00, 0.00]
        self.Colour = c
        self.Window = w

        self.PlayerItem = Label(self.Window, text='lol', fg=self.Colour, bg=self.Colour, width=2, height=1)
        self.PlayerJumping = False

    def draw(self, x, y):
        self.Location = [x, y]
        self.PlayerItem.place(relx=x, rely=y)

    def hide(self):
        self.PlayerItem.place_forget()

    def refresh(self):
        self.PlayerItem.place(relx=self.getLocation()[0], rely=self.getLocation()[1])

    def jump(self, ty):
        self.PlayerJumping = True
        if ty == 1:
            self.setVelocityX(0.005)
        elif ty == 0:
            self.setVelocityX(-0.005)
        jThread = Thread(target=self.jumpEvent, args=()).start()

    def jumpEvent(self):
        originalLocation = self.getLocation()
        threshHold = originalLocation[1] - 0.2
        self.Gravity = False
        while True:
            playerLocation = self.getLocation()
            self.setLocation(playerLocation[0], playerLocation[1] - 0.003)
            if round(playerLocation[1], 2) <= round(threshHold, 2):
                self.Gravity = True
                break
            sleep(0.001)
        sleep(0.20)
        self.setVelocityX(self.getVelocityX() / 2)
        sleep(0.03)
        self.PlayerJumping = False

    def gravity(self):
        return self.Gravity

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

    def isJumping(self):
        return self.PlayerJumping

    def updateLocation(self):
        while True:
            self.refresh()
            sleep(0.0005)


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x200')
    Test = Player(root, 'green')
    button = Button(command=lambda: Test.draw(.05, .8)).pack()
    root.mainloop()
