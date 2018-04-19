from tkinter import *
import json
import UI_Chat


def draw():
    global config, colourTheme, windowBackground, windowForeground
    global windowTitle, programVersion, programStage, windowResolution

    def auth():
        first_ip = entryBox.get()
        first_user = entryBox2.get()
        ConnectWindow.destroy()
        UI_Chat.Client.external(first_ip, first_user)

    def press(event):
        entryBox.config(state=NORMAL)
        auth()

    def disable(event):
        entryBox.config(state=DISABLED)

    with open('config.json') as jsonConfig:
        config = json.load(jsonConfig)

    # Config incorporation.
    colourTheme = config['window']['theme']
    windowResolution = config['window']['resolution']
    windowTitle = config['window']['title']
    windowForeground = config['window']['foreground']
    windowBackground = config['window']['background']

    programVersion = config['information']['version']
    programStage = config['information']['stage']

    ConnectWindow = Tk()
    ConnectWindow.configure(bg=windowBackground)
    ConnectWindow.geometry('450x200')
    ConnectWindow.title(windowTitle)
    # MainWindow.attributes('-topmost', True)

    titleText = StringVar()
    titleText.set('C O N N E C T')

    lineText = StringVar()
    lineText.set('_____________________________________')

    serverText = StringVar()
    serverText.set('S E R V E R  I P')

    usernameText = StringVar()
    usernameText.set('U S E R N A M E')

    buttonText = StringVar()
    buttonText.set(' ➤ ')

    lineLabel = Label(ConnectWindow, textvariable=lineText, font='Arial 15 bold', fg=colourTheme, bg=windowBackground)
    lineLabel.place(relx=.04, rely=.15)

    titleLabel = Label(ConnectWindow, textvariable=titleText, font='Arial 15 bold', bg=windowBackground,
                       fg=windowForeground)
    titleLabel.place(relx=.04, rely=.09)

    enterServerLabel = Label(ConnectWindow, textvariable=serverText, font='Arial 10 bold', bg=windowBackground,
                              fg=windowForeground)
    enterServerLabel.place(relx=.04, rely=.34)

    entryBox = Entry(ConnectWindow, width=67)
    entryBox.place(relx=.047, rely=.47)

    entryBox.bind("<Return>", disable)
    entryBox.bind("<KeyRelease-Return>", press)

    entryBox.insert(END, 'chatserver.hopto.org')

    enterUsernameLabel = Label(ConnectWindow, textvariable=usernameText, font='Arial 10 bold', bg=windowBackground,
                             fg=windowForeground)
    enterUsernameLabel.place(relx=.04, rely=.60)

    entryBox2 = Entry(ConnectWindow, width=56)
    entryBox2.place(relx=.047, rely=.735)

    entryBox2.bind("<Return>", disable)
    entryBox2.bind("<KeyRelease-Return>", press)

    sendButton = Button(ConnectWindow, textvariable=buttonText, font='Arial 7 bold', width=7, height=1,
                        command=lambda:press('done'))
    sendButton.place(relx=.834, rely=.735)

    ConnectWindow.mainloop()


draw()
