import Game
from tkinter import *

'''
GHub = Game.GameHub()
GHub.draw()

while True:
    if not GHub.logged():
        continue
    myData = GHub.get()
    break
    


GH_NAME = myData['information']['name']
GH_USERNAME = myData["information"]["username"]
GH_CREDITS = myData["game"]["credits"]
GH_WINS = myData["game"]["wins"]
GH_TIES = myData["game"]["ties"]
GH_LOSSES = myData["game"]["losses"]
GH_H_TRACKING = myData["hangman"]["tracking"]
GH_H_WINS = myData["hangman"]["wins"]
GH_H_LOSSES = myData["hangman"]["losses"]

'''

GH_USERNAME = 'Shivam'
GH_CREDITS = '85'


class GameMenu:
    @staticmethod
    def draw():

        global hangmanButton, tttButton

        Dashboard = Tk()
        Dashboard.geometry('700x350')
        Dashboard.configure(bg='#141414')
        Dashboard.title('Game MENU')

        titleLabel = Label(Dashboard, text=GH_USERNAME.upper(), font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#141414')
        titleLabel.place(relx=.05, rely=.08)

        statsBorder = Text(Dashboard, bd=2, width=34, height=9, bg='#141414')
        statsBorder.place(relx=.353, rely=.39)
        statsBorder.config(state=DISABLED)

        statsLabel = Label(Dashboard, text='STATISTICS', font=('Segoe UI', 13, 'bold'), fg='#f1c40f', bg='#141414')
        statsLabel.place(relx=.363, rely=.41)

        winsLabel = Label(Dashboard, text='WINS', font=('Segoe UI', 12, 'bold'), fg='#2ecc71', bg='#141414')
        winsLabel.place(relx=.363, rely=.51)

        tiesLabel = Label(Dashboard, text='TIES', font=('Segoe UI', 12, 'bold'), fg='#16a085', bg='#141414')
        tiesLabel.place(relx=.363, rely=.61)

        loseLabel = Label(Dashboard, text='LOSSES', font=('Segoe UI', 12, 'bold'), fg='#e74c3c', bg='#141414')
        loseLabel.place(relx=.363, rely=.71)

        winsStat = Label(Dashboard, text='5 - 50%', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
        winsStat.place(relx=.473, rely=.51)

        tiesStat = Label(Dashboard, text='1 - 10%', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
        tiesStat.place(relx=.473, rely=.61)

        loseStat = Label(Dashboard, text='4 - 40%', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
        loseStat.place(relx=.473, rely=.71)

        #creditsAmount = Label(Dashboard, text=GH_CREDITS, font=('Segoe UI', 13, 'bold'), fg='#95a5a6', bg='#141414')
        #creditsAmount.place(relx=.76, rely=.29)

        creditsBorder = Text(Dashboard, bd=2, width=17, height=4, bg='#141414')
        creditsBorder.place(relx=.75, rely=.19)
        creditsBorder.config(state=DISABLED)

        creditsLabel = Label(Dashboard, text='CREDITS', font=('Segoe UI', 13, 'bold'), fg='#f1c40f', bg='#141414')
        creditsLabel.place(relx=.76, rely=.21)

        creditsAmount = Label(Dashboard, text=GH_CREDITS, font=('Segoe UI', 13, 'bold'), fg='#95a5a6', bg='#141414')
        creditsAmount.place(relx=.76, rely=.29)

        gamesBorder = Text(Dashboard, bd=2, width=17, height=9, bg='#141414')
        gamesBorder.place(relx=.75, rely=.39)
        gamesBorder.config(state=DISABLED)

        gamesLabel = Label(Dashboard, text='GAMES', font=('Segoe UI', 13, 'bold'), fg='#2ecc71', bg='#141414')
        gamesLabel.place(relx=.76, rely=.41)

        tttButton = Button(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(1))
        tttButton.place(relx=.76, rely=.51)

        hangmanButton = Button(Dashboard, text='HANGMAN', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(2))
        hangmanButton.place(relx=.76, rely=.61)

        LaunchButton = Button(Dashboard, text='LAUNCH GAME', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                              fg='#2ecc71', command=lambda: Dashboard.destroy())
        LaunchButton.place(relx=.76, rely=.72)

        BackButton = Button(Dashboard, text='CLOSE', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                            fg='#e74c3c', command=lambda: Dashboard.destroy())
        BackButton.place(relx=.05, rely=.84)

        InfoButton = Button(Dashboard, text='VIEW ACCOUNT DETAILS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                            fg='#9b59b6', command=lambda: Dashboard.destroy())
        InfoButton.place(relx=.17, rely=.84)

        SwitchButton = Button(Dashboard, text='SWITCH ACCOUNTS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                            fg='#9b59b6', command=lambda: Dashboard.destroy())
        SwitchButton.place(relx=.49, rely=.84)

        StoreButton = Button(Dashboard, text='SPEND CREDITS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                              fg='#f1c40f', command=lambda: Dashboard.destroy())
        StoreButton.place(relx=.76, rely=.84)

        def selectGame(GameT=1):
            global tttButton, hangmanButton, selected
            if GameT == 1:
                hangmanButton.place_forget()
                tttButton = Button(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 12, 'bold'), bg='white', fg='#141414', bd=0, command=lambda: selectGame(1))
                tttButton.place(relx=.76, rely=.51)
                hangmanButton.place_forget()
                hangmanButton = Button(Dashboard, text='HANGMAN', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(2))
                hangmanButton.place(relx=.76, rely=.61)
                selected = 1
            elif GameT == 2:
                hangmanButton.place_forget()
                tttButton = Button(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 12, 'bold'), fg='white', bg='#141414', bd=0, command=lambda: selectGame(1))
                tttButton.place(relx=.76, rely=.51)
                hangmanButton.place_forget()
                hangmanButton = Button(Dashboard, text='HANGMAN', font=('Segoe UI', 12, 'bold'), fg='#141414', bg='white', bd=0, command=lambda: selectGame(2))
                hangmanButton.place(relx=.76, rely=.61)
                selected = 2

        Dashboard.mainloop()


GameMenu.draw()
