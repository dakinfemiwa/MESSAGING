from tkinter import *


class Animate:
    def __init__(self, w, x, y, t=0):
        self.animIncrementer = 1
        self.animDelay = 1
        self.animPositionX = x
        self.animPositionY = y
        self.animPosIncrementer = .01
        self.animWindow = w
        self.animLabel = Label(self.animWindow, bg='#2F3542', height=3, width=60)

    def scroll(self):
        if self.animPositionX < .9:
            self.animPositionX += self.animPosIncrementer
            self.animDelay += self.animIncrementer
            self.animWindow.after(self.animDelay, lambda: self.animLabel.place(relx=self.animPositionX, rely=self.animPositionY))
            self.animWindow.after(self.animDelay, lambda: self.scroll())


if __name__ == '__main__':
    def test():
        T = Animate(root, .05, .2)
        T.scroll()

    root = Tk()
    root.geometry('200x100')
    label = Label(root, text='Hello!').place(relx=.05, rely=.2)
    button = Button(root, command=lambda: test()).pack()
    root.mainloop()
