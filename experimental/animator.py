from tkinter import *


class Test:
    def __init__(self, level, colour, colour2):
        self.incrementer = 4
        self.delay = 5
        self.deci = .005
        self.deci2 = .999
        self.deci3 = .999
        self.col = colour
        self.col2 = colour2
        self.stopped = False
        self.level = level

    def stopanim(self):
        self.stopped = True

    def animate(self):

        if self.stopped is False:
            if self.deci3 <= .45:
                self.deci3 = .45
            else:
                self.deci3 = self.deci3 - .005
            if self.deci > .999:
                self.deci = .005
            if self.deci2 < .005:
                self.deci2 = .999

            self.delay = self.delay + self.incrementer
            self.deci = self.deci + .01
            self.deci2 = self.deci2 - .01
            win.after(self.delay, lambda: (self.topBar.place(relx=self.deci, rely=.27), self.animate()))
            win.after(self.delay, lambda: (self.BottomBar.place(relx=self.deci2, rely=.52), self.animate()))
            win.after(self.delay, lambda: (self.LevelUp.place(relx=.392, rely=self.deci3), self.animate()))
            win.after(5000, lambda: self.stopanim())
        else:
            win.after(0, lambda: (self.topBar.place_forget(), self.BottomBar.place_forget(), self.LevelUp.place_forget()))

    def draw(self, Window):
        global win
        win = Window

        levStr = str(self.level)
        levStr2 = " ".join(levStr)

        self.topBar = Label(Window, text='_____________________', font=('Arial', 30, 'bold'), bg='#141414', fg=self.col)
        self.BottomBar = Label(Window, text='_____________________', font=('Arial', 30, 'bold'), bg='#141414', fg=self.col)
        self.LevelUp = Label(Window, text='L E V E L  ' + levStr2, font=('Segoe UI', 20, 'bold'), bg='#141414', fg=self.col2)

        self.animate()

