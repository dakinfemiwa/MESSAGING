from tkinter import *


class Connect:
    def __init__(self):
        self.WINDOW_BACKGROUND = '#141414'
        self.WINDOW_FOREGROUND = '#FFFFFF'

        self.WINDOW_FONT_1 = ('Segoe UI', 22, 'bold')
        self.WINDOW_FONT_2 = ('Segoe UI', 16, 'bold italic')
        self.WINDOW_FONT_3 = ('Segoe UI', 12, 'bold')

        self.delay = 1
        self.deci = .001
        self.incrementer = 1
        self.tempcol = 'blue'

        self.delay2 = 1
        self.deci2 = .05
        self.incrementer2 = 1

        self.COL_GREY = '#95A5A6'

        self.useGameServer = True

        self.root = Tk()
        self.root.geometry('650x300')
        self.root.configure(bg=self.WINDOW_BACKGROUND)

        self.titleText = StringVar()
        self.titleText.set('CONNECT FOUR')

        self.subtitleText = StringVar()
        self.subtitleText.set('Waiting for a game...')

        self.title_label = Label(self.root, textvariable=self.titleText, font=self.WINDOW_FONT_1, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        self.title_label.place(relx=.05, rely=.05)

        self.subtitle_label = Label(self.root, textvariable=self.subtitleText, font=self.WINDOW_FONT_2, bg=self.WINDOW_BACKGROUND, fg=self.COL_GREY)
        # self.subtitle_label.place(relx=.05, rely=.15)

        self.top_bar = Label(self.root, text='                                    ', font=self.WINDOW_FONT_2, bg=self.WINDOW_BACKGROUND, fg='RED', height=1)
        self.small_bar = Label(self.root, text='__', font=self.WINDOW_FONT_2, bg=self.WINDOW_BACKGROUND, fg='RED', height=1)

        self.username_label = Label(self.root, text='USERNAME', font=self.WINDOW_FONT_3, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        self.username_label.place(relx=.05, rely=.35)

        self.animate()
        self.animate2()

        self.root.mainloop()

    def animate(self):

        self.delay = self.delay + self.incrementer
        self.deci = self.deci + .01
        if self.tempcol == '#8e44ad':
            self.tempcol = '#16a085'
        else:
            self.tempcol = '#8e44ad'
        if self.deci <= .42:
            self.root.after(self.delay, lambda: (self.top_bar.place(relx=self.deci, rely=.08), self.animate()))
            self.root.after(self.delay, lambda: (self.title_label.config(fg=self.tempcol)))

    def animate2(self):

        self.delay2 = self.delay2 + self.incrementer2
        self.deci2 = self.deci2 + .004
        if self.deci2 <= .18:
            self.root.after(self.delay2, lambda: (self.small_bar.place(relx=self.deci2, rely=.40), self.animate2()))
        else:
            self.deci2 = 0.05
            self.root.after(self.delay2, lambda: (self.small_bar.place(relx=self.deci2, rely=.40), self.animate2()))



if __name__ == '__main__':
    Test = Connect()