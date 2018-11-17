from experimental import game
import socket
import time
import os
from tkinter import *
import experimental.animator
from datetime import datetime

if True:
    GHub = game.GameHub()
    GHub.run()

    while True:
        if not GHub.logged():
            continue
        myData = GHub.get()
        break

    GH_NAME = myData['information']['name']
    GH_USERNAME = myData["information"]["username"]
    GH_LEVEL = myData["information"]["level"]
    GH_XP = myData["information"]["xp"]
    GH_DATE = myData["information"]["date"]
    GH_CREDITS = myData["game"]["credits"]
    GH_POINTS = myData["game"]["points"]
    GH_WINS = myData["game"]["wins"]
    GH_TIES = myData["game"]["ties"]
    GH_LOSSES = myData["game"]["losses"]
    GH_H_TRACKING = myData["hangman"]["tracking"]
    GH_H_TIES = myData["hangman"]["ties"]
    GH_H_WINS = myData["hangman"]["wins"]
    GH_H_LOSSES = myData["hangman"]["losses"]
    #####
    GH_T_TRACKING = myData["tictactoe"]["tracking"]
    GH_T_WINS = myData["tictactoe"]["wins"]
    GH_T_LOSSES = myData["tictactoe"]["losses"]

    GH_H_DATE = myData["hangman"]["date"]
    GH_T_DATE = myData["tictactoe"]["date"]

tempName = GH_USERNAME

if False:

    GH_NAME = 'Test'
    GH_USERNAME = 'Shivam'
    GH_CREDITS = '85'
    GH_DATE = '10/10/2018'
    GH_WINS = '5'
    GH_TIES = '2'
    GH_LOSSES = '3'
    GH_H_WINS = '5'
    GH_H_TIES = '2'
    GH_H_LOSSES = '3'
    GH_TRACKING = 'Yes'
    GH_H_TRACKING = 'Yes'
    GH_H_DATE = '10/10/2018'
    GH_T_DATE = '10/10/2018'

    GH_T_WINS = '5'
    GH_T_LOSSES = '3'

    GH_POINTS = '4000'
    GH_LEVEL = 19
    GH_XP = 510

GH_ROLES = ['ADMIN', 'MEMBER']
GH_ROLE_COLOURS = ['#e74c3c', '#f39c12']
GH_H_PLAYED = int(GH_H_WINS) + int(GH_H_TIES) + int(GH_H_LOSSES)
GH_T_PLAYED = int(GH_T_WINS) + int(GH_T_LOSSES)
GH_XP = int(GH_XP)
GH_LEVEL = int(GH_LEVEL)
GH_TOTAL = 500
# GH_ROLE = 'ADMIN'
GH_ROLE = 'MEMBER'
GH_ROLE_COLOUR = GH_ROLE_COLOURS[GH_ROLES.index(GH_ROLE)]
GH_COL = '#22a6b3'
GH_COL2 = '#7ed6df'

x = GH_XP / 500
y = x * 125
y = round(y)
y2 = '_' * y
z = '_' * 125

if GH_XP >= GH_TOTAL:
    y2 = '_' * 125

if GH_LEVEL < 20:
    GH_COL = '#22a6b3'
    GH_COL2 = '#7ed6df'

elif 20 <= GH_LEVEL < 40:
    GH_COL = '#27ae60'
    GH_COL2 = '#2ecc71'

elif 40 <= GH_LEVEL < 60:
    GH_COL = '#c0392b'
    GH_COL2 = '#e74c3c'

elif 60 <= GH_LEVEL < 80:
    GH_COL = '#f39c12'
    GH_COL2 = '#f1c40f'

elif 80 <= GH_LEVEL < 100:
    GH_COL = '#6D214F'
    GH_COL2 = '#B33771'

elif 100 <= GH_LEVEL < 120:
    GH_COL = '#82589F'
    GH_COL2 = '#D6A2E8'

else:
    GH_COL = '#182C61'
    GH_COL2 = '#3B3B98'
    
playedStr = '{0} played'.format(GH_H_PLAYED)

try:
    winsStr = '{0} wins ({1:.2f}%)'.format(GH_H_WINS, float(int(GH_H_WINS) / int(GH_H_PLAYED) * 100))
except:
    winsStr = '0 wins (0%)'

try:
    tiesStr = '{0} ties ({1:.2f}%)'.format(GH_H_TIES, float(int(GH_H_TIES) / int(GH_H_PLAYED) * 100))
except:
    tiesStr = '0 ties (0%)'
    
try:
    lostStr = '{0} lost ({1:.2f}%)'.format(GH_H_LOSSES, float(int(GH_H_LOSSES) / int(GH_H_PLAYED) * 100))
except:
    lostStr = '0 lost (0%)'

playedStr2 = '{0} played'.format(GH_T_PLAYED)

try:
    winsStr2 = '{0} wins ({1:.2f}%)'.format(GH_T_WINS, float(int(GH_T_WINS) / int(GH_T_PLAYED) * 100))
except:
    winsStr2 = '0 wins (0%)'

try:
    lostStr2 = '{0} lost ({1:.2f}%)'.format(GH_T_LOSSES, float(int(GH_T_LOSSES) / int(GH_T_PLAYED) * 100))
except:
    lostStr2 = '0 lost (0%)'


class GameMenu:
    @staticmethod
    def save(latestData):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.settimeout(3)
        clientSocket.connect(('chat-sv.ddns.net', 6666))
        clientSocket.send(str.encode('}' + GH_USERNAME + ',' + myData["information"]["username"]))
        time.sleep(.08)
        clientSocket.send(str.encode('(' + str(latestData)))
        time.sleep(.08)
        clientSocket.close()

    @staticmethod
    def levelup(latestData):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.settimeout(3)
        clientSocket.connect(('chat-sv.ddns.net', 6666))
        clientSocket.send(str.encode('€' + str(latestData)))
        time.sleep(.08)
        clientSocket.close()

    @staticmethod
    def refresh():
        emptyBar.place(relx=.052, rely=.885)
        fillBar.place(relx=.052, rely=.885)
        roleButton.place(relx=.32, rely=.828)
        levelLabel.place(relx=.05, rely=.78)
        levelNum.place(relx=.25, rely=.78)
        gameButton.place(relx=.05, rely=.22)
        statsButton.place(relx=.05, rely=.42)
        settingsButton.place(relx=.05, rely=.62)
    
    @staticmethod
    def draw():

        global hangmanButton, tttButton, gameButton, myData, Dashboard, titleLabel, MainAssets, statsButton, settingsButton, roleButton, emptyBar, fillBar, levelNum, levelLabel, levelUpButton

        Dashboard = Tk()
        Dashboard.geometry('700x350')
        Dashboard.configure(bg='#141414')
        Dashboard.title('Game MENU')

        titleLabel = Label(Dashboard, text=GH_USERNAME.upper(), font=('Segoe UI', 15, 'bold'), fg='#FFFFFF', bg='#141414')
        titleLabel.place(relx=.05, rely=.08)

        emptyBar = Label(Dashboard, text=z, font=('Segoe UI', 8, 'bold'), fg=GH_COL2, bg='#141414')
        emptyBar.place(relx=.052, rely=.885)

        fillBar = Label(Dashboard, text=y2, font=('Segoe UI', 8, 'bold'), fg=GH_COL, bg='#141414')
        fillBar.place(relx=.052, rely=.885)

        roleButton = Button(Dashboard, text=GH_ROLE.upper(), font=('Segoe UI', 12, 'bold'), fg=GH_ROLE_COLOUR, bg='#141414', bd=0, height=1)
        #roleButton.place(relx=.32, rely=.825)

        if GH_XP >= GH_TOTAL:
            levelUpButton = Button(Dashboard, text='LEVEL UP', font=('Segoe UI', 12, 'bold'), fg='#2ecc71', bg='#141414', bd=0, height=1, command=lambda: levelUp())
            levelUpButton.place(relx=.834, rely=.828)

        levelLabel = Label(Dashboard, text='L E V E L', font=('Segoe UI', 25, 'bold'), fg=GH_COL, bg='#141414')
        levelLabel.place(relx=.05, rely=.78)

        levelNum = Label(Dashboard, text=GH_LEVEL, font=('Segoe UI', 25, 'bold'), fg=GH_COL2, bg='#141414')
        levelNum.place(relx=.25, rely=.78)

        statsPhoto = PhotoImage(file="assets/images/stats-icon.gif", master=Dashboard)
        statsPhoto = statsPhoto.zoom(10)
        statsPhoto = statsPhoto.subsample(128)

        settingsPhoto = PhotoImage(file="assets/images/settings-icon.gif", master=Dashboard)
        settingsPhoto = settingsPhoto.subsample(31)

        gamePhoto = PhotoImage(file="assets/images/game-icon.gif", master=Dashboard)
        gamePhoto = gamePhoto.subsample(12)

        gameButton = Button(Dashboard, image=gamePhoto, bg='#141414', bd=0, command=lambda: (hideAll(), showGames()))
        gameButton.place(relx=.05, rely=.22)

        statsButton = Button(Dashboard, image=statsPhoto, bg='#141414', bd=0, command=lambda: (hideAll(), showStats()))
        statsButton.place(relx=.05, rely=.42)

        settingsButton = Button(Dashboard, image=settingsPhoto, bg='#141414', bd=0, command=lambda: (hideAll(), showSettings()))
        settingsButton.place(relx=.05, rely=.62)

        MainAssets = [emptyBar, fillBar, roleButton, levelLabel, levelNum, statsPhoto, settingsButton, gameButton, gamePhoto, settingsButton]

        def hideAll():
            try:
                for item in gameItems:
                    item.place_forget()
            except:
                pass
            try:
                for item in statsItems:
                    item.place_forget()
            except:
                pass
            try:
                for item in settingsItems:
                    item.place_forget()
            except:
                pass
            try:
                for item in detailsItems:
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

            tttPlayed = Label(Dashboard, text='last played on ' + str(GH_T_DATE), font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            tttPlayed.place(relx=.35, rely=.355)

            hangmanPlayed = Label(Dashboard, text='last played on ' + str(GH_H_DATE), font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            hangmanPlayed.place(relx=.35, rely=.455)

            unknownButton = Button(Dashboard, text='TEST GAME', font=('Segoe UI', 12, 'bold'), bg='#141414', fg='white', bd=0, command=lambda: selectGame(3))
            unknownButton.place(relx=.15, rely=.54)

            unknownPlayed = Label(Dashboard, text='last played on --/--/----', font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            unknownPlayed.place(relx=.35, rely=.555)

            creditsLabel = Label(Dashboard, text='CREDITS', font=('Segoe UI', 13, 'bold'), fg='#f1c40f', bg='#141414')
            creditsLabel.place(relx=.774, rely=.22)

            creditsAmount = Label(Dashboard, text=GH_CREDITS + ' CREDITS', font=('Segoe UI', 12, 'bold'), fg='#bdc3c7', bg='#141414')
            creditsAmount.place(relx=.774, rely=.345)

            pointsAmount = Label(Dashboard, text=GH_POINTS + ' POINTS', font=('Segoe UI', 12, 'bold'), fg='#bdc3c7', bg='#141414')
            pointsAmount.place(relx=.774, rely=.445)

            LaunchButton = Button(Dashboard, text='LAUNCH GAME', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                                  fg='#2ecc71', command=lambda: launchGame())
            LaunchButton.place(relx=.774, rely=.72)

            gameItems = [gamesLabel, tttButton, hangmanButton, LaunchButton, tttPlayed, hangmanPlayed, creditsLabel, creditsAmount, pointsAmount, unknownButton, unknownPlayed]

        def launchGame():
            selectedGame = 1
            if selectedGame == 1:
                myData["tictactoe"]["date"] = datetime.now().strftime("%d/%m/%Y")
            else:
                myData["hangman"]["date"] = datetime.now().strftime("%d/%m/%Y")
            GameMenu.save(myData)

        def resetStats():
            myData["game"]["wins"] = '0'
            myData["game"]["ties"] = '0'
            myData["game"]["losses"] = '0'
            myData["hangman"]["ties"] = '0'
            myData["hangman"]["wins"] = '0'
            myData["hangman"]["losses"] = '0'
            myData["tictactoe"]["wins"] = '0'
            myData["tictactoe"]["losses"] = '0'
            GameMenu.save(myData)

            savedLabel = Label(Dashboard, text='Reset statistics successfully', font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            savedLabel.place(relx=.7, rely=.732)

            Dashboard.after(3000, lambda: savedLabel.place_forget())

        def showStats():
            global statsItems
            
            statsLabel = Label(Dashboard, text='STATISTICS', font=('Segoe UI', 13, 'bold'), fg='#f1c40f', bg='#141414')
            statsLabel.place(relx=.15, rely=.22)

            tStatsLabel = Label(Dashboard, text='TIC TAC TOE', font=('Segoe UI', 13, 'bold'), fg='white', bg='#141414')
            tStatsLabel.place(relx=.55, rely=.30)

            hStatsLabel = Label(Dashboard, text='HANGMAN', font=('Segoe UI', 13, 'bold'), fg='white', bg='#141414')
            hStatsLabel.place(relx=.15, rely=.30)

            winsLabel = Label(Dashboard, text='WINS', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            winsLabel.place(relx=.152, rely=.4)

            tiesLabel = Label(Dashboard, text='TIES', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            tiesLabel.place(relx=.152, rely=.5)

            loseLabel = Label(Dashboard, text='LOSSES', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            loseLabel.place(relx=.152, rely=.60)

            playedLabel = Label(Dashboard, text='GAMES PLAYED', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            playedLabel.place(relx=.152, rely=.70)

            winsStat = Label(Dashboard, text=winsStr, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            winsStat.place(relx=.38, rely=.41)

            tiesStat = Label(Dashboard, text=tiesStr, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            tiesStat.place(relx=.38, rely=.51)

            loseStat = Label(Dashboard, text=lostStr, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            loseStat.place(relx=.38, rely=.61)

            playedStat = Label(Dashboard, text=playedStr, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            playedStat.place(relx=.38, rely=.71)

            ##

            winsLabel2 = Label(Dashboard, text='WINS', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            winsLabel2.place(relx=.552, rely=.4)
            
            loseLabel2 = Label(Dashboard, text='LOSSES', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            loseLabel2.place(relx=.552, rely=.50)

            playedLabel2 = Label(Dashboard, text='GAMES PLAYED', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            playedLabel2.place(relx=.552, rely=.60)

            winsStat2 = Label(Dashboard, text=winsStr2, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            winsStat2.place(relx=.78, rely=.41)

            loseStat2 = Label(Dashboard, text=lostStr2, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            loseStat2.place(relx=.78, rely=.51)

            playedStat2 = Label(Dashboard, text=playedStr2, font=('Segoe UI', 10, 'bold italic'), fg='#bdc3c7', bg='#141414')
            playedStat2.place(relx=.78, rely=.61)

            ResetButton = Button(Dashboard, text='RESET STATS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                                  fg='#f1c40f', command=lambda: resetStats())
            ResetButton.place(relx=.8, rely=.72)

            statsItems = [ResetButton, winsLabel2, loseLabel2, playedLabel2, winsStat2, loseStat2, playedStat2, statsLabel, tStatsLabel, hStatsLabel, winsLabel, tiesLabel, loseLabel, playedLabel, winsStat, tiesStat, loseStat, playedStat]

        def levelUp():
            newLevel = GH_LEVEL + 1

            if newLevel < 20:
                GH_COL = '#22a6b3'
                GH_COL2 = '#7ed6df'

            elif 20 <= newLevel < 40:
                GH_COL = '#27ae60'
                GH_COL2 = '#2ecc71'

            elif 40 <= newLevel < 60:
                GH_COL = '#c0392b'
                GH_COL2 = '#e74c3c'

            elif 60 <= newLevel < 80:
                GH_COL = '#f39c12'
                GH_COL2 = '#f1c40f'

            elif 80 <= newLevel < 100:
                GH_COL = '#6D214F'
                GH_COL2 = '#B33771'

            elif 100 <= newLevel < 120:
                GH_COL = '#82589F'
                GH_COL2 = '#D6A2E8'

            else:
                GH_COL = '#182C61'
                GH_COL2 = '#3B3B98'


            hideAll()
            statsButton.place_forget()
            gameButton.place_forget()
            settingsButton.place_forget()
            levelUpButton.place_forget()
            try:
                for item in MainAssets:
                    item.place_forget()
            except:
                pass
            myData["information"]["level"] = str(newLevel)
            myData["information"]["xp"] = "10"
            x = 10 / 500
            y = x * 125
            y = round(y)
            y2 = '_' * y
            z = '_' * 125
            GameMenu.levelup(myData)
            global fillBar, levelLabel, levelNum, emptyBar, roleButton
            fillBar = Label(Dashboard, text=y2, font=('Segoe UI', 8, 'bold'), fg=GH_COL, bg='#141414')
            emptyBar = Label(Dashboard, text=z, font=('Segoe UI', 8, 'bold'), fg=GH_COL2, bg='#141414')
            levelLabel = Label(Dashboard, text='L E V E L', font=('Segoe UI', 25, 'bold'), fg=GH_COL, bg='#141414')

            levelNum = Label(Dashboard, text=newLevel, font=('Segoe UI', 25, 'bold'), fg=GH_COL2, bg='#141414')
            roleButton = Button(Dashboard, text=GH_ROLE.upper(), font=('Segoe UI', 12, 'bold'), fg=GH_ROLE_COLOUR, bg='#141414', bd=0, height=1)

            inst = experimental.animator.Test(newLevel, GH_COL, GH_COL2)
            inst.draw(Dashboard)
            Dashboard.after(5000, lambda: GameMenu.refresh())
            Dashboard.after(5000, lambda: fillBar.place(relx=.052, rely=.885))
            Dashboard.after(5000, lambda: emptyBar.place(relx=.052, rely=.885))
            Dashboard.after(5000, lambda: levelLabel.place(relx=.05, rely=.78))
            Dashboard.after(5000, lambda: levelNum.place(relx=.25, rely=.78))
            Dashboard.after(5000, lambda: roleButton.place(relx=.32, rely=.825))

        def showSettings():
            global settingsItems, changeButton, pUserLabel, pNameLabel
            
            settingsLabel = Label(Dashboard, text='SETTINGS', font=('Segoe UI', 13, 'bold'), fg='#9b59b6', bg='#141414')
            settingsLabel.place(relx=.15, rely=.22)

            usernameLabel = Label(Dashboard, text='USERNAME', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            usernameLabel.place(relx=.152, rely=.34)

            nameLabel = Label(Dashboard, text='NAME', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            nameLabel.place(relx=.152, rely=.44)

            dateLabel = Label(Dashboard, text='CREATED', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            dateLabel.place(relx=.152, rely=.54)

            trackingLabel = Label(Dashboard, text='TRACKING', font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#141414')
            trackingLabel.place(relx=.152, rely=.64)

            changeButton = Button(Dashboard, text='CHANGE DETAILS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                                  fg='#9b59b6', command=lambda: changeDetails())
            changeButton.place(relx=.6, rely=.72)

            signButton = Button(Dashboard, text='SIGN OUT', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                                  fg='#9b59b6', command=lambda: signOut())
            signButton.place(relx=.83, rely=.72)

            pUserLabel = Label(Dashboard, text=myData["information"]["username"], font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            pUserLabel.place(relx=.352, rely=.35)

            pNameLabel = Label(Dashboard, text=GH_NAME, font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            pNameLabel.place(relx=.352, rely=.45)

            pDateLabel = Label(Dashboard, text=GH_DATE, font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            pDateLabel.place(relx=.352, rely=.55)
            
            pTrackLabel = Label(Dashboard, text=GH_H_TRACKING, font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            pTrackLabel.place(relx=.352, rely=.65)

            settingsItems = [pUserLabel, pNameLabel, pDateLabel, pTrackLabel, settingsLabel, usernameLabel, nameLabel, dateLabel, trackingLabel, changeButton, signButton]

        def changeDetails():
            global detailsItems
            changeButton.place_forget()

            newUsernameEntry = Entry(Dashboard, font=("Segoe UI", 10, "bold italic"), bg='#141414', fg='white')
            newUsernameEntry.place(relx=.652, rely=.34)

            newNameEntry = Entry(Dashboard, font=("Segoe UI", 10, "bold italic"), bg='#141414', fg='white')
            newNameEntry.place(relx=.652, rely=.44)

            saveButton = Button(Dashboard, text='SAVE DETAILS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                                  fg='#9b59b6', command=lambda: saveDetails(newUsernameEntry.get(), newNameEntry.get()))
            saveButton.place(relx=.63, rely=.72)

            detailsItems = [newUsernameEntry, newNameEntry, saveButton]

        def saveDetails(usr,  name):
            global myData
            for item in detailsItems:
                item.place_forget()

            savedLabel = Label(Dashboard, text='New details saved successfully', font=("Segoe UI", 10, "bold italic"), fg='#bdc3c7', bg='#141414')
            savedLabel.place(relx=.53, rely=.732)

            try:
                with open('data/data-stored.txt', 'r') as storedFile:
                    storedData = storedFile.readlines()[0].split(',')
                    storedData[0] = usr
                    fileData = ",".join(storedData)
                with open('data/data-stored.txt', 'w') as updatedFile:
                    updatedFile.write(fileData)
            except:
                pass

            if len(usr) >= 3:
                pUserLabel.config(text=usr)
                titleLabel.config(text=usr.upper())
                myData["information"]["username"] = usr
            if len(name) >= 3:
                pNameLabel.config(text=name)
                myData["information"]["name"] = name
                
            GameMenu.save(myData)

            Dashboard.after(3000, lambda: savedLabel.place_forget())
            Dashboard.after(3000, lambda: changeButton.place(relx=.6, rely=.72))

        def signOut():
            try:
                os.remove("data/data-stored.txt")
            except:
                pass
            Dashboard.destroy()

        """

        SwitchButton = Button(Dashboard, text='SWITCH ACCOUNTS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                            fg='#9b59b6', command=lambda: Dashboard.destroy())
        SwitchButton.place(relx=.49, rely=.84)

        StoreButton = Button(Dashboard, text='SPEND CREDITS', font=('Segoe UI', 12, 'bold'), bg='#141414', borderwidth=0,
                              fg='#f1c40f', command=lambda: Dashboard.destroy())
        StoreButton.place(relx=.76, rely=.84)

        """

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
            gameItems.append(hangmanButton)
            gameItems.append(tttButton)
                
        Dashboard.mainloop()


if __name__ == '__main__':
    GameMenu.draw()
