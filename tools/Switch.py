from tkinter import *


class Switch:
    def __init__(self, window, text='YES', fg='#2F3542', bg='#FFFFFF', font=('MS PGothic', 11, 'bold'), bd=0):
        self.SwitchMode = 1
        self.SwitchButton = Button(window, text=text, fg=fg, bg=bg, font=font, bd=bd, command=lambda: self.switchSetting(), width=4)

    def place(self, x, y):
        self.SwitchButton.place(relx=x, rely=y)

    def get(self):
        return self.SwitchMode

    def set(self, v):
        if v == 1:
            self.SwitchButton.config(text='YES')
            self.SwitchMode = 1
        else:
            self.SwitchButton.config(text='NO')
            self.SwitchMode = 0

    def switchSetting(self):
        if self.SwitchButton.cget('text') == 'YES':
            self.SwitchButton.config(text='NO')
            self.SwitchMode = 0
        else:
            self.SwitchButton.config(text='YES')
            self.SwitchMode = 1


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x200')
    Test = Switch(root)
    Test.place(0.05, 0.2)
    root.mainloop()
