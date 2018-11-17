from tkinter import *



"""

example = {
    'Release Notes': {
        'Added': [
            'New debugging logger',
            'More logging entries',
            'Recovery commands'
        ],
        'Changed': [
            'Improved updater reliability',
            'Game server structure'
        ],
        'Removed': [
            'Legacy notification support',
            'Support for version three or below',
            'Outdated/unused code'
        ]
    }
}

print('Release notes for Version 4.85:')
print('Added:')
for line in example['Release Notes']['Added']:
    print(f'- {line}')
print('Changed:')
for line in example['Release Notes']['Changed']:
    print(f'- {line}')
print('Removed:')
for line in example['Release Notes']['Removed']:
    print(f'- {line}')
    
"""



class Connect:
    def __init__(self):

        self.WINDOW_BACKGROUND = '#141414'
        self.WINDOW_FOREGROUND = '#FFFFFF'

        self.WINDOW_FONT_1 = ('Segoe UI', 22, 'bold')
        self.WINDOW_FONT_2 = ('Segoe UI', 16, 'bold italic')
        self.WINDOW_FONT_3 = ('Segoe UI', 12, 'bold')
        self.WINDOW_FONT_4 = ('Segoe UI', 8, 'bold italic')

        self.COL_GREY = '#95A5A6'

        self.useGameServer = True
        self.selected = 0

        def select():
            if self.selected == 0:
                self.username_background.configure(bg=self.WINDOW_FOREGROUND)
                self.username_label.configure(bg=self.WINDOW_FOREGROUND, fg=self.WINDOW_BACKGROUND)
                self.username_info.configure(bg=self.WINDOW_FOREGROUND, fg=self.WINDOW_BACKGROUND)
                self.selected = 1
            else:
                self.username_background.configure(bg=self.WINDOW_BACKGROUND)
                self.username_label.configure(bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
                self.username_info.configure(bg=self.WINDOW_BACKGROUND, fg=self.COL_GREY)
                self.selected = 0

            # self.username_info = Button(self.root, bd=0, text='Join & host games using the game server - requires the server to be online.', font=self.WINDOW_FONT_4, bg=self.WINDOW_FOREGROUND, fg=self.WINDOW_BACKGROUND, command=lambda:select())
            # self.username_info.place(relx=.055, rely=.46)

        self.root = Tk()
        self.root.geometry('650x300')
        self.root.configure(bg=self.WINDOW_BACKGROUND)

        self.titleText = StringVar()
        self.titleText.set('CONNECTION METHOD')

        self.subtitleText = StringVar()
        self.subtitleText.set('Waiting for a game...')

        self.title_label = Label(self.root, textvariable=self.titleText, font=self.WINDOW_FONT_1, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        self.title_label.place(relx=.05, rely=.1)

        self.subtitle_label = Label(self.root, textvariable=self.subtitleText, font=self.WINDOW_FONT_2, bg=self.WINDOW_BACKGROUND, fg=self.COL_GREY)
        # self.subtitle_label.place(relx=.05, rely=.15)

        self.top_bar = Label(self.root, text='                                    ', font=self.WINDOW_FONT_2, bg=self.WINDOW_BACKGROUND, fg='RED', height=1)
        self.small_bar = Label(self.root, text='__', font=self.WINDOW_FONT_2, bg=self.WINDOW_BACKGROUND, fg='RED', height=1)

        self.username_background = Button(self.root, bd=0, text=' ', font=self.WINDOW_FONT_4, bg=self.WINDOW_BACKGROUND, fg=self.COL_GREY, width=60, height=5, command=lambda:select())
        self.username_background.place(relx=.05, rely=.35)

        self.username_label = Button(self.root, bd=0, text='GAME SERVER', font=self.WINDOW_FONT_3, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND, command=lambda:select())
        self.username_label.place(relx=.05, rely=.35)

        self.username_info = Button(self.root, bd=0, text='Join & host games using the game server - requires the server to be online.', font=self.WINDOW_FONT_4, bg=self.WINDOW_BACKGROUND, fg=self.COL_GREY, command=lambda:select())
        self.username_info.place(relx=.055, rely=.46)

        # self.username_background = Label(self.root, text=' ', font=self.WINDOW_FONT_4, bg='yellow', fg=self.COL_GREY, width=60, height=5)
        # self.username_background.place(relx=.05, rely=.35)

        self.root.mainloop()


if __name__ == '__main__':
    Test = Connect()
