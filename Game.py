from tkinter import *
import socket
import _thread
import ast
import time


class GameHub:
    def __init__(self):
        self.WINDOW_RESOLUTION = '600x250'
        self.WINDOW_BACKGROUND = '#141414'
        self.WINDOW_FOREGROUND = '#FFFFFF'
        self.WINDOW_TITLE = 'TITLE'
        self.WINDOW_TITLE_FONT = ('Arial', 16, 'bold')
        self.WINDOW_SUB_FONT = ('Arial', 11, 'bold')
        self.WINDOW_BUTTON_FONT = ('Arial', 12, 'bold')
        self.WINDOW_THEME = '#16A085'
        self.WINDOW_ERROR = '#E74C3C'

        self.CONFIG_LOGGER = 'True'
        self.CONFIG_UPDATER = 'False'
        self.CONFIG_ADVANCED = 'False'
        self.CONFIG_VERSION = '1.0'

        self.AUTH_MESSAGE_1 = 'Could not connect to the auth server'.upper()
        self.AUTH_MESSAGE_2 = 'Invalid login details entered'.upper()
        self.AUTH_MESSAGE_3 = 'An unknown error occurred'.upper()

        self.IP = '127.0.0.1'
        self.PORT = 6666

    def draw(self):
        global Window, errorText, userLabel, passLabel, checked

        Window = Tk()
        Window.geometry(self.WINDOW_RESOLUTION)
        Window.configure(bg=self.WINDOW_BACKGROUND)
        Window.title(self.WINDOW_TITLE)

        titleText = StringVar()
        settingsText = StringVar()
        exitText = StringVar()
        userText = StringVar()
        passText = StringVar()
        errorText = StringVar()

        titleText.set('ENTER LOGIN DETAILS')
        settingsText.set('SIGN IN')
        exitText.set('SIGN IN AS GUEST')
        userText.set('USERNAME')
        passText.set('PASSWORD')
        errorText.set('')

        titleLabel = Label(Window, textvariable=titleText, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)

        userLabel = Label(Window, textvariable=userText, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        passLabel = Label(Window, textvariable=passText, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)

        userEntry = Entry(Window, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND, highlightthickness=2, width=40)
        passEntry = Entry(Window, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND, highlightthickness=2, width=40, show="*")

        loginButton = Button(Window, textvariable=settingsText, font=self.WINDOW_BUTTON_FONT, fg=self.WINDOW_THEME, bg=self.WINDOW_BACKGROUND, bd=0, command=lambda: self.auth(True, userEntry.get(), passEntry.get()))
        guestButton = Button(Window, textvariable=exitText, font=self.WINDOW_BUTTON_FONT, fg='#3498db', bg=self.WINDOW_BACKGROUND, bd=0, command=lambda: self.auth(False))

        errorLabel = Label(Window, textvariable=errorText, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_ERROR)
        errorLabel.place(relx=0.05, rely=0.735)

        titleLabel.place(relx=0.05, rely=0.08)

        userLabel.place(relx=0.05, rely=0.25)
        passLabel.place(relx=0.05, rely=0.5)

        userEntry.place(relx=0.055, rely=0.35)
        passEntry.place(relx=0.055, rely=0.6)

        loginButton.place(relx=0.85, rely=0.85)
        guestButton.place(relx=0.043, rely=0.85)

        userEntry.bind('<Return>', (lambda event: self.auth(True, userEntry.get(), passEntry.get())))
        passEntry.bind('<Return>', (lambda event: self.auth(True, userEntry.get(), passEntry.get())))

        checked = False

        Window.mainloop()

    def auth(self, authorize=False, username=None, password=None):
        global playerData, checked

        def connect():
            global playerData, checked
            try:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.settimeout(3)
                clientSocket.connect((self.IP, self.PORT))
                clientSocket.send(str.encode('~' + str(username)))
                time.sleep(.08)
                clientSocket.send(str.encode('>' + str(password)))
                while True:
                    serverResponse = clientSocket.recv(4096, ).decode()
                    if serverResponse == 'True':
                        checked = True
                    elif serverResponse == 'False':
                        errorText.set(self.AUTH_MESSAGE_2)
                        userLabel.config(fg=self.WINDOW_ERROR)
                        passLabel.config(fg=self.WINDOW_ERROR)
                    elif 'information' in serverResponse:
                        if checked is True:
                            playerData = ast.literal_eval(serverResponse)
                            clientSocket.close()
                            Window.destroy()
                            _thread.interrupt_main()
                            break
            except:
                errorText.set(self.AUTH_MESSAGE_1)

        if authorize:
            _thread.start_new_thread(connect, ())
        else:
            playerData = None

    @staticmethod
    def logged():
        return checked

    @staticmethod
    def get():
        return playerData

    @staticmethod
    def close():
        # _thread.interrupt_main()
        Window.destroy()


if __name__ == '__main__':
    Main = GameHub()
    Main.draw()
