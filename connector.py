from tkinter import *
import json
import chat


def displayWindow(usernameSet=None):
    global config, colourTheme, windowBackground, windowForeground
    global windowTitle, programVersion, programStage, windowResolution

    def basicAuth():
        inputIP = entryBox.get()
        inputUN = entryBox2.get()
        try:
            if "*" == inputUN[0]:
                ConnectWindow.destroy()
                displayWindow(inputUN.strip('*'))
            else:
                ConnectWindow.destroy()
                chat.Client.external(inputIP, inputUN)
        except:
            print('ERROR: Invalid username entered.')
            exit(69)

    def advancedAuth():
        inputIP = entryBox.get()
        inputUN = entryBox2.get()
        inputPW = entryBox3.get()
        inputUN = inputUN + '%!'

        ConnectWindow.destroy()
        chat.Client.external(inputIP, inputUN, inputPW)

    def basicSubmit(event):
        basicAuth()

    def advancedSubmit(event):
        advancedAuth()

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

    titleText = StringVar()
    titleText.set('C O N N E C T')

    serverText = StringVar()
    serverText.set('S E R V E R  I P')

    usernameText = StringVar()
    usernameText.set('U S E R N A M E')

    passwordText = StringVar()
    passwordText.set('P A S S W O R D')

    lineText = StringVar()
    lineText.set('_' * 37)

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

    entryBox.insert(END, 'chat-sv.ddns.net')

    enterUsernameLabel = Label(ConnectWindow, textvariable=usernameText, font='Arial 10 bold', bg=windowBackground,
                               fg=windowForeground)
    enterUsernameLabel.place(relx=.04, rely=.60)

    enterPasswordLabel = Label(ConnectWindow, textvariable=passwordText, font='Arial 10 bold', bg=windowBackground,
                               fg=windowForeground)

    entryBox3 = Entry(ConnectWindow, width=27)
    entryBox3.bind("<Return>", advancedSubmit)

    if usernameSet is not None:
        entryBox2 = Entry(ConnectWindow, width=29)
        entryBox2.place(relx=.047, rely=.735)
        entryBox2.bind("<Return>", advancedSubmit)
        entryBox2.insert(END, usernameSet)
        enterPasswordLabel.place(relx=.444, rely=.60)
        entryBox3.place(relx=.4535, rely=.735)
        sendButton = Button(ConnectWindow, textvariable=buttonText, font='Arial 7 bold', width=7, height=1,
                            command=lambda: advancedSubmit(''))
        sendButton.place(relx=.834, rely=.735)
    else:
        entryBox2 = Entry(ConnectWindow, width=57)
        entryBox2.place(relx=.047, rely=.735)
        entryBox2.bind("<Return>", basicSubmit)
        sendButton = Button(ConnectWindow, textvariable=buttonText, font='Arial 7 bold', width=7, height=1,
                            command=lambda: basicSubmit(''))
        sendButton.place(relx=.834, rely=.735)

    ConnectWindow.mainloop()


displayWindow()
