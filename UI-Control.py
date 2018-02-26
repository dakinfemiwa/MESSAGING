from tkinter import *
import json
import socket
import tkinter.ttk

with open('config.json') as jsonConfig:
    config = json.load(jsonConfig)

# Control panel used to monitor servers.
# This will simulate a client but will only
# send messages to the server as codes which
# then execute a set of commands on the
# server end.

def check_status():
    global server1
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('0.0.0.0', 6666))
        test_socket.listen(10)
        test_socket.close()
        server1 = False
    except OSError:
        server1 = True


def add(message):
    ChatLog.config(state=NORMAL)
    line = float(ChatLog.index(END)) - 1.0
    ChatLog.insert(END, message)
    ChatLog.insert(END, '\n')
    ChatLog.tag_add(message, line, line + 100)
    ChatLog.tag_config(message, foreground=colourTheme, font=("courier new", 9, "bold"))
    ChatLog.config(state=DISABLED)
    ChatLog.see(END)


def restart(server):
    message = 'Attempting to restart server ' + str(server)
    add(message)

    shutdown(server)

    start(server)


def shutdown(server):
    control_socket = ''

    message = 'Attempting to shutdown server ' + str(server)
    add(message)
    message = 'Attempting to connect to server ' + str(server)
    add(message)

    try:

        IP = '86.172.96.18'
        PORT = 6666

        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.connect((IP, PORT))

        control_socket.send(str.encode('\n'))
        control_socket.send(str.encode('$-$cpl'))

    except:
        add('Connection to the server failed.')

    try:

        if server1 is True:
            # Server is online, shutdown process can continue successfully.
            control_socket.send(str.encode('\n'))
            control_socket.send(str.encode('$-$shutdown'))

            add('Server was shutdown successfully')

        else:
            pass

    except:
        add('There was an unhandled error')



def start(server):
    message = 'Attempting to start server ' + str(server)
    add(message)


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

check_status()


if server1 is False:
    serverOneStatusText = StringVar()
    serverOneStatusText.set('O F F L I N E')
    serverOneStatusColour = '#FF0000'

elif server1 is True:
    serverOneStatusText = StringVar()
    serverOneStatusText.set('O N L I N E')
    serverOneStatusColour = '#00FF00'

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

###################################

serverTwoText = StringVar()
serverTwoText.set('S E R V E R  2')

serverTwoStatusText = StringVar()
serverTwoStatusText.set('O F F L I N E')

serverTwoStatusColour = '#FF0000'

####################################

serverThreeText = StringVar()
serverThreeText.set('S E R V E R  3')

serverThreeStatusText = StringVar()
serverThreeStatusText.set('O F F L I N E')

serverThreeStatusColour = '#FF0000'

versionText = StringVar()
versionText.set('V E R S I O N  ' + programVersion)

bLabel = Label(Window, bg=windowBackground, fg=windowBackground).pack()

lineLabel = Label(Window, textvariable=lineText, font='Arial 15 bold', fg=colourTheme, bg=windowBackground)
lineLabel.place(relx=.04, rely=.14)

titleLabel = Label(Window, textvariable=titleText, font='Arial 15 bold', bg=windowBackground, fg=windowForeground)
titleLabel.place(relx=.04, rely=.09)

serverOneLabel = Label(Window, textvariable=serverOneText, font='Arial 11 bold', fg='#FFFFFF', bg=windowBackground)
serverOneLabel.place(relx=.04, rely=.27)

serverOneStatus = Label(Window, textvariable=serverOneStatusText, font='Arial 10 bold', fg=serverOneStatusColour,
                        bg=windowBackground)
serverOneStatus.place(relx=.2, rely=.272)

serverOneShutDown = tkinter.ttk.Button(Window, text='S H U T D O W N', command=lambda: shutdown(1))
serverOneShutDown.place(relx=.045, rely=.37)

serverOneStart = tkinter.ttk.Button(Window, text='S T A R T', command=lambda: start(1))
serverOneStart.place(relx=.2, rely=.37)

serverOneRestart = tkinter.ttk.Button(Window, text='R E S T A R T', command=lambda: restart(1))
serverOneRestart.place(relx=.32, rely=.37)

###

serverTwoLabel = Label(Window, textvariable=serverTwoText, font='Arial 11 bold', fg='#FFFFFF', bg=windowBackground)
serverTwoLabel.place(relx=.04, rely=.47)

serverTwoStatus = Label(Window, textvariable=serverTwoStatusText, font='Arial 10 bold', fg=serverTwoStatusColour,
                        bg=windowBackground)
serverTwoStatus.place(relx=.2, rely=.472)

serverTwoShutDown = tkinter.ttk.Button(Window, text='S H U T D O W N', command=lambda: shutdown(1))
serverTwoShutDown.place(relx=.045, rely=.57)

serverTwoStart = tkinter.ttk.Button(Window, text='S T A R T', command=lambda: start(2))
serverTwoStart.place(relx=.2, rely=.57)

serverTwoRestart = tkinter.ttk.Button(Window, text='R E S T A R T', command=lambda: restart(2))
serverTwoRestart.place(relx=.32, rely=.57)

###

serverTwoLabel = Label(Window, textvariable=serverThreeText, font='Arial 11 bold', fg='#FFFFFF', bg=windowBackground)
serverTwoLabel.place(relx=.04, rely=.67)

serverThreeStatus = Label(Window, textvariable=serverThreeStatusText, font='Arial 10 bold', fg=serverThreeStatusColour,
                          bg=windowBackground)
serverThreeStatus.place(relx=.2, rely=.672)

serverThreeShutDown = tkinter.ttk.Button(Window, text='S H U T D O W N', command=lambda: shutdown(3))
serverThreeShutDown.place(relx=.045, rely=.77)

serverThreeStart = tkinter.ttk.Button(Window, text='S T A R T', command=lambda: start(3))
serverThreeStart.place(relx=.2, rely=.77)

serverThreeRestart = tkinter.ttk.Button(Window, text='R E S T A R T', command=lambda: restart(3))
serverThreeRestart.place(relx=.32, rely=.77)

###

sendButton = Button(Window, textvariable=buttonText, font='Arial 7 bold', width=13, height=1)
sendButton.place(relx=.827, rely=.855)

versionLabel = Label(Window, textvariable=versionText, font='Arial 10 bold', bg=windowBackground, fg=colourTheme)
versionLabel.place(relx=.3, rely=.18)

ChatLog = Text(Window, bd=2, bg="#141414", height="7.5", width="36", font="Arial")
ChatLog.place(relx=.48, rely=.35)

if __name__ == '__main__':
    Window.mainloop()
