import tkinter.ttk
from tkinter import *


class Error:
    DEFAULT_TITLE = 'Error'
    DEFAULT_TEXT = 'An unknown error occurred'
    DEFAULT_OPTIONS = ['Confirm', 'Ignore']

    def __init__(self, title=DEFAULT_TITLE, text=DEFAULT_TEXT, options=DEFAULT_OPTIONS):
        self.errorTitle = title
        self.errorText = text
        self.errorOptions = options
        self.errorOutcome = None

        self.errorFont = ('Calibri', 12)
        self.errorBackground = '#D4D6D8'
        self.errorResolution = '540x180'

    def show(self):
        errorWindow = Tk()
        errorWindow.geometry(self.errorResolution)
        errorWindow.configure(bg=self.errorBackground)
        errorWindow.title(self.errorTitle)

        errorTextWindow = Text(errorWindow, bd=0, bg=self.errorBackground, font=self.errorFont, width=62, height=5)
        errorTextWindow.place(relx=0.04, rely=0.2)
        errorTextWindow.insert(END, self.errorText)
        errorTextWindow.configure(state=DISABLED)

        errorAction1 = tkinter.ttk.Button(errorWindow, command=lambda: (self.set(errorAction1.cget('text')), errorWindow.destroy()))
        errorAction2 = tkinter.ttk.Button(errorWindow, command=lambda: (self.set(errorAction2.cget('text')), errorWindow.destroy()))
        errorAction3 = tkinter.ttk.Button(errorWindow, command=lambda: (self.set(errorAction3.cget('text')), errorWindow.destroy()))

        errorCounter = 0
        errorPlacement = 0.825
        errorActionButtons = [errorAction1, errorAction2, errorAction3]

        for errorOption in self.errorOptions:
            errorActionButtons[errorCounter].configure(text=errorOption)
            errorActionButtons[errorCounter].place(relx=errorPlacement, rely=0.8)
            errorPlacement -= 0.15
            errorCounter += 1

        errorWindow.mainloop()

    def set(self, outcome):
        self.errorOutcome = outcome

    def outcome(self):
        return self.errorOutcome


if __name__ == '__main__':
    Test = Error('Exceeded thread count - fatal',
                 'The number of running threads has exceeded the maximum - 100 threads -  '
                 'You can carry on running the program while it is in an unsafe state by clicking Ignore.'
                 ' To close the program click Confirm. To attempt a restart, click the Restart button.',
                 ['Confirm', 'Ignore', 'Restart'])
    Test.show()
    print(Test.outcome())
