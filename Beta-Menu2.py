import Game
from tkinter import *
import _thread

if True:
    GHub = Game.GameHub()
    GHub.draw()

    while True:
        if not GHub.logged():
            continue
        myData = GHub.get()
        # GHub.close()
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


GH_USERNAME = 'Shivam'
GH_CREDITS = '85'
GH_POINTS = '4000'


class GameMenu:
    @staticmethod
    def draw():

        global hangmanButton, tttButton, gameButton

        Dashboard = Tk()
        Dashboard.geometry('700x350')
        Dashboard.configure(bg='#141414')
        Dashboard.title('Game MENU')

        titleLabel = Label(Dashboard, text=GH_USERNAME.upper(), font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#141414')
        titleLabel.place(relx=.05, rely=.08)

        emptyBar = Label(Dashboard, text='_____________________________________________________________________________________________________________________________', font=('Segoe UI', 8, 'bold'), fg='#7ed6df', bg='#141414')
        emptyBar.place(relx=.052, rely=.885)

        fillBar = Label(Dashboard, text='__________________________________________________________________________', font=('Segoe UI', 8, 'bold'), fg='#22a6b3', bg='#141414')
        fillBar.place(relx=.052, rely=.885)

        levelLabel = Label(Dashboard, text='L E V E L', font=('Segoe UI', 25, 'bold'), fg='#22a6b3', bg='#141414')
        levelLabel.place(relx=.05, rely=.78)

        levelNum = Label(Dashboard, text='73', font=('Segoe UI', 25, 'bold'), fg='#7ed6df', bg='#141414')
        levelNum.place(relx=.25, rely=.78)

        def drawImg():

            if 1:

                statsPhoto = PhotoImage(Dashboard, file="assets/images/stats-icon.gif")
                statsPhoto = statsPhoto.zoom(10)
                statsPhoto = statsPhoto.subsample(128)

                settingsPhoto = PhotoImage(Dashboard, file="assets/images/settings-icon.gif")
                settingsPhoto = settingsPhoto.subsample(31)

                gamePhoto = PhotoImage(Dashboard, file="assets/images/game-icon.gif")
                gamePhoto = gamePhoto.subsample(12)

                gameButton = Button(Dashboard, image=gamePhoto, bg='#141414', bd=0)
                gameButton.place(relx=.05, rely=.22)

                statsButton = Button(Dashboard, image=statsPhoto, bg='#141414', bd=0)
                statsButton.place(relx=.05, rely=.42)

                settingsButton = Button(Dashboard, image=settingsPhoto, bg='#141414', bd=0)
                settingsButton.place(relx=.05, rely=.62)

            if 0:
                pass

        def hideAll():
            try:
                for item in gameItems:
                    item.place_forget()
            except:
                pass

        def showGames():
            global gameItems, hangmanButton, tttButton, unknownButton

            gamesLabel = Label(Dashboard, text='GAMES', font=('Segoe UI', 13, 'bold'), fg='#2ecc71', bg='#141414')
            gamesLabel.place(relx=.15, rely=.22)

            tttButton = Button(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(1))
            tttButton.place(relx=.15, rely=.34)

            hangmanButton = Button(Dashboard, text='HANGMAN', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(2))
            hangmanButton.place(relx=.15, rely=.44)

            tttPlayed = Label(Dashboard, text='- last played on 01/10/2018', font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            tttPlayed.place(relx=.35, rely=.355)

            hangmanPlayed = Label(Dashboard, text='- last played on 10/10/2018', font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            hangmanPlayed.place(relx=.35, rely=.455)

            unknownButton = Button(Dashboard, text='TEST GAME', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(3))
            unknownButton.place(relx=.15, rely=.54)

            unknownPlayed = Label(Dashboard, text='- last played on 11/10/2018', font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            unknownPlayed.place(relx=.35, rely=.555)

            creditsLabel = Label(Dashboard, text='CREDITS', font=('Segoe UI', 13, 'bold'), fg='#f1c40f', bg='#141414')
            creditsLabel.place(relx=.764, rely=.22)

            creditsAmount = Label(Dashboard, text=GH_CREDITS + ' CREDITS', font=('Segoe UI', 12, 'bold'), fg='#bdc3c7', bg='#141414')
            creditsAmount.place(relx=.764, rely=.345)

            pointsAmount = Label(Dashboard, text=GH_POINTS + ' POINTS', font=('Segoe UI', 12, 'bold'), fg='#bdc3c7', bg='#141414')
            pointsAmount.place(relx=.764, rely=.445)

            LaunchButton = Button(Dashboard, text='LAUNCH GAME', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                                  fg='#2ecc71', command=lambda: Dashboard.destroy())
            LaunchButton.place(relx=.76, rely=.72)

            gameItems = [gamesLabel, tttButton, hangmanButton, LaunchButton, tttPlayed, hangmanPlayed, creditsLabel, creditsAmount, pointsAmount, unknownButton, unknownPlayed]

        """

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

        InfoButton = Button(Dashboard, text='VIEW ACCOUNT DETAILS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                            fg='#9b59b6', command=lambda: Dashboard.destroy())
        InfoButton.place(relx=.17, rely=.84)

        SwitchButton = Button(Dashboard, text='SWITCH ACCOUNTS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                            fg='#9b59b6', command=lambda: Dashboard.destroy())
        SwitchButton.place(relx=.49, rely=.84)

        StoreButton = Button(Dashboard, text='SPEND CREDITS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                              fg='#f1c40f', command=lambda: Dashboard.destroy())
        StoreButton.place(relx=.76, rely=.84)"""

        def selectGame(GameT=1):
            global tttButton, hangmanButton, selected
            if GameT == 1:
                hangmanButton.place_forget()
                tttButton = Button(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 12, 'bold'), bg='white', fg='#141414', bd=0, command=lambda: selectGame(1))
                tttButton.place(relx=.15, rely=.34)
                hangmanButton.place_forget()
                hangmanButton = Button(Dashboard, text='HANGMAN', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(2))
                hangmanButton.place(relx=.15, rely=.44)
                selected = 1
            elif GameT == 2:
                hangmanButton.place_forget()
                tttButton = Button(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 12, 'bold'), fg='white', bg='#141414', bd=0, command=lambda: selectGame(1))
                tttButton.place(relx=.15, rely=.34)
                hangmanButton.place_forget()
                hangmanButton = Button(Dashboard, text='HANGMAN', font=('Segoe UI', 12, 'bold'), fg='#141414', bg='white', bd=0, command=lambda: selectGame(2))
                hangmanButton.place(relx=.15, rely=.44)
                selected = 2
        drawImg()
        Dashboard.mainloop()


GameMenu.draw()
