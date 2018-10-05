from tkinter import *


def gameSettings(T='TEMP'):
    Sting = Tk()
    Sting.geometry('700x350')
    Sting.configure(bg='#141414')
    Sting.title('Game settings')

    title = Label(Sting, text='HANGMAN GAME SETTINGS', font=('Segoe UI', 14, 'bold'), bg='#141414', fg='#FFFFFF')
    title.place(relx=.075, rely=.125)

    enterLivesLabel = Label(Sting, text='GAME LIVES', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='#9b59b6')
    enterLivesLabel.place(relx=.075, rely=.24)

    enterLivesBox = Entry(Sting, font=('Segoe UI', 6, ''), fg='white', bg='#141414', bd=2, highlightthickness=2, width=5, disabledforeground='#ffffff', disabledbackground="#141414")
    enterLivesBox.place(relx=.4025, rely=.25)

    enterLivesBox.config(highlightbackground='#FFFFFF')

    upBox = Button(Sting, text='▲', font='Arial 4 bold', width=5, height=1, command=lambda: gameSettings('+'))
    upBox.place(relx=.3625, rely=.25)

    downBox = Button(Sting, text='▼', font='Arial 4 bold', width=5, height=1, command=lambda: gameSettings('-'))
    downBox.place(relx=.3625, rely=.28)

    allowGuessLabel = Label(Sting, text='ALLOW GUESSES', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='#9b59b6')
    allowGuessLabel.place(relx=.075, rely=.34)

    allowedGuess = Entry(Sting, font=('Segoe UI', 6, 'bold'), text='YES', fg='#2ecc71', bg='#141414', bd=2, highlightthickness=2, width=6, disabledforeground='#2ecc71', disabledbackground="#141414")
    allowedGuess.place(relx=.39, rely=.35)

    allowedGuess.delete(0, END)
    allowedGuess.insert(0, 'YES')
    allowedGuess.config(state=DISABLED, justify=CENTER)

    Sting.mainloop()


gameSettings()
