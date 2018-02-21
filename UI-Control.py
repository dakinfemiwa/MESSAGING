from tkinter import *
import json
import tkinter.ttk

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

Window = Tk()
Window.configure(bg=windowBackground)
Window.geometry('700x300')
Window.title(windowTitle)

titleText = StringVar()
titleText.set('C O N T R O L  P A N E L')

lineText = StringVar()
lineText.set('__________________________________________________________')

enterMessageText = StringVar()
enterMessageText.set('')

buttonText = StringVar()
buttonText.set('C L E A R')

serverOneText = StringVar()
serverOneText.set('S E R V E R  1')

serverOneStatusText = StringVar()
serverOneStatusText.set('O N L I N E')

serverOneStatusColour = '#00FF00'

serverTwoText = StringVar()
serverTwoText.set('S E R V E R  2')

serverTwoStatusText = StringVar()
serverTwoStatusText.set('O F F L I N E')

serverTwoStatusColour = '#FF0000'

versionText = StringVar()
versionText.set('V E R S I O N  ' + programVersion)

bLabel = Label(Window, bg=windowBackground, fg=windowBackground).pack()

lineLabel = Label(Window, textvariable=lineText, font='Arial 15 bold', fg=colourTheme, bg=windowBackground)
lineLabel.place(relx=.04, rely=.14)

titleLabel = Label(Window, textvariable=titleText, font='Arial 15 bold', bg=windowBackground, fg=windowForeground)
titleLabel.place(relx=.04, rely=.09)

serverOneLabel = Label(Window, textvariable=serverOneText, font='Arial 11 bold', fg='#FFFFFF', bg=windowBackground)
serverOneLabel.place(relx=.04, rely=.27)

serverOneStatus = Label(Window, textvariable=serverOneStatusText, font='Arial 10 bold', fg=serverOneStatusColour, bg=windowBackground)
serverOneStatus.place(relx=.2, rely=.272)

serverOneShutDown = tkinter.ttk.Button(Window, text='S H U T D O W N')
serverOneShutDown.place(relx=.045, rely=.37)

serverOneStart = tkinter.ttk.Button(Window, text='S T A R T')
serverOneStart.place(relx=.2, rely=.37)

serverOneRestart = tkinter.ttk.Button(Window, text='R E S T A R T')
serverOneRestart.place(relx=.32, rely=.37)

###

serverTwoLabel = Label(Window, textvariable=serverTwoText, font='Arial 11 bold', fg='#FFFFFF', bg=windowBackground)
serverTwoLabel.place(relx=.04, rely=.47)

serverTwoStatus = Label(Window, textvariable=serverTwoStatusText, font='Arial 10 bold', fg=serverTwoStatusColour, bg=windowBackground)
serverTwoStatus.place(relx=.2, rely=.472)

serverTwoShutDown = tkinter.ttk.Button(Window, text='S H U T D O W N')
serverTwoShutDown.place(relx=.045, rely=.57)

serverTwoStart = tkinter.ttk.Button(Window, text='S T A R T')
serverTwoStart.place(relx=.2, rely=.57)

serverTwoRestart = tkinter.ttk.Button(Window, text='R E S T A R T')
serverTwoRestart.place(relx=.32, rely=.57)

sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1)
sendButton.place(relx=.827, rely=.855)

versionLabel = Label(Window, textvariable=versionText, font='Arial 10 bold', bg=windowBackground, fg=colourTheme)
versionLabel.place(relx=.3, rely=.18)

ChatLog = Text(Window, bd=2, bg="#141414", height="8", width="36", font="Arial")
ChatLog.place(relx=.48, rely=.29)

if __name__ == '__main__':
    Window.mainloop()
