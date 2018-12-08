from tkinter import *
from threading import Thread
from time import sleep
from tools.animator import Animate


class Slider:
    def __init__(self, w, c='red', g=None):
        self.Velocity = [0.00, 0.00]
        self.Location = [0.00, 0.00]
        self.Colour = c
        self.Window = w
        self.GameInstance = g

        self.SliderItem = Label(self.Window, text='❰ ❱', font=('Arial', 6, 'bold'), fg=self.Colour, bg=self.Colour, width=10, height=1)

        self.THREAD_AI = Thread(target=self.moveAround, args=())
        self.THREAD_MOVEMENT = Thread(target=self.updateLocation, args=())

    def moveAround(self):
        while True:
            self.setVelocityX(-0.0025)
            sleep(1.75)
            self.setVelocityX(+0.0025)
            sleep(1.75)

    def updateLocation(self):
        while True:
            currentLocation = self.getLocation()
            self.setLocation(currentLocation[0] + self.getVelocityX(), currentLocation[1])
            self.refresh()
            sleep(0.01)

    def draw(self, x, y):
        self.Location = [x, y]
        self.SliderItem.place(relx=x, rely=y)
        self.THREAD_AI.start()
        self.THREAD_MOVEMENT.start()

    def place_forget(self):
        self.SliderItem.place_forget()

    def hide(self):
        self.SliderItem.place_forget()

    def refresh(self):
        self.SliderItem.place(relx=self.getLocation()[0], rely=self.getLocation()[1])

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
    root.config(bg='#141414')
    root.geometry('400x200')
    Test = Slider(root, c='#FFFFFF')
    button = Button(command=lambda: Test.draw(.8, .8)).pack()
    root.mainloop()
