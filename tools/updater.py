import configparser
import os
import shutil
import urllib.request
from tkinter import *


class Updater:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('tools/config.ini')
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        self.WINDOW_RESOLUTION = config['Window']['Resolution']
        self.WINDOW_BACKGROUND = config['Window']['Background']
        self.WINDOW_FOREGROUND = config['Window']['Foreground']
        self.WINDOW_TITLE = config['Window']['Title']
        self.WINDOW_TEXT_SMALL = config['Colours']['Small Text']
        self.WINDOW_THEME = config['Colours']['Theme']
        self.WINDOW_NEUTRAL = config['Colours']['Neutral']
        self.WINDOW_WARNING = config['Colours']['Warning']
        self.WINDOW_OK = config['Colours']['Good']
        self.WINDOW_ERROR = config['Colours']['Error']

        self.WINDOW_TITLE_FONT = ('Arial', 30, 'bold')
        self.WINDOW_SUB_FONT = ('Arial', 12, 'bold')
        self.WINDOW_BUTTON_FONT = ('Hurme Geometric Sans 4', 15, 'bold')
        self.WINDOW_TEXT_FONT = ('Hurme Geometric Sans 4', 12, 'bold')
        self.WINDOW_TEXT_SMALL_FONT = ('Hurme Geometric Sans 4', 10, 'bold')

        self.CONFIG_LOGGER = 'True'
        self.CONFIG_UPDATER = 'False'
        self.CONFIG_ADVANCED = 'False'

        self.CONFIG_ADVANCED = config['Settings']['Advanced']
        self.CONFIG_VERSION = config['Settings']['Version']
        self.CONFIG_PROGRAM_NAME = config['Program']['Name']
        self.CONFIG_PROGRAM_GITHUB = config['Program']['Host']
        self.CONFIG_PROGRAM_FILES = config['Program']['Files']
        self.CONFIG_PROGRAM_FILE_VERSION = config['Program']['Version File']

    def draw(self):
        global Window, searchButton, updateButton, notesButton, programNewText, programVersionText, programStatusText
        
        Window = Tk()
        Window.geometry(self.WINDOW_RESOLUTION)
        Window.configure(bg=self.WINDOW_BACKGROUND)
        Window.title(self.WINDOW_TITLE)

        titleText = StringVar()
        subText = StringVar()
        nameText = StringVar()
        versionText = StringVar()
        newText = StringVar()
        statusText = StringVar()
        searchText = StringVar()
        updateText = StringVar()
        notesText = StringVar()
        exitText = StringVar()

        programNameText = StringVar()
        programVersionText  = StringVar()
        programNewText = StringVar()
        programStatusText = StringVar()
        
        titleText.set('UPDATE PROGRAM')
        subText.set('UPDATER CONFIGURED CORRECTLY')
        nameText.set('PROGRAM NAME')
        versionText.set('LOCAL VERSION')
        newText.set('LATEST VERSION')
        statusText.set('UPDATE STATUS')
        searchText.set('SEARCH FOR UPDATE')
        updateText.set('UPDATE PROGRAM')
        notesText.set('VIEW UPDATE NOTES')
        exitText.set('EXIT PROGRAM')

        programNameText.set(self.CONFIG_PROGRAM_NAME.upper())
        programVersionText.set('VERSION N/A')
        programNewText.set('VERSION N/A')
        programStatusText.set('SEARCH FOR UPDATE')

        titleLabel = Label(Window, textvariable=titleText, font=self.WINDOW_TITLE_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        subLabel = Label(Window, textvariable=subText, font=self.WINDOW_SUB_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)

        nameLabel =  Label(Window, textvariable=nameText, font=self.WINDOW_TEXT_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        versionLabel =  Label(Window, textvariable=versionText, font=self.WINDOW_TEXT_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        newLabel = Label(Window, textvariable=newText, font=self.WINDOW_TEXT_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)
        statusLabel =  Label(Window, textvariable=statusText, font=self.WINDOW_TEXT_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_FOREGROUND)

        programNameLabel =  Label(Window, textvariable=programNameText, font=self.WINDOW_TEXT_SMALL_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_TEXT_SMALL)
        programVersionLabel =  Label(Window, textvariable=programVersionText, font=self.WINDOW_TEXT_SMALL_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_TEXT_SMALL)
        programNewLabel = Label(Window, textvariable=programNewText, font=self.WINDOW_TEXT_SMALL_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_TEXT_SMALL)
        programStatusLabel =  Label(Window, textvariable=programStatusText , font=self.WINDOW_TEXT_SMALL_FONT, bg=self.WINDOW_BACKGROUND, fg=self.WINDOW_TEXT_SMALL)

        searchButton = Button(Window, textvariable=searchText, font=self.WINDOW_BUTTON_FONT, fg=self.WINDOW_WARNING, bg=self.WINDOW_BACKGROUND, bd=0, command=lambda:self.search())
        updateButton = Button(Window, textvariable=updateText, font=self.WINDOW_BUTTON_FONT, fg=self.WINDOW_OK, bg=self.WINDOW_BACKGROUND, bd=0, command=lambda:self.update())
        notesButton = Button(Window, textvariable=notesText, font=self.WINDOW_BUTTON_FONT, fg=self.WINDOW_NEUTRAL, bg=self.WINDOW_BACKGROUND, bd=0, command=lambda:self.notes())
        exitButton = Button(Window, textvariable=exitText, font=self.WINDOW_BUTTON_FONT, fg=self.WINDOW_ERROR, bg=self.WINDOW_BACKGROUND, bd=0, command=lambda:self.close())

        titleLabel.place(relx=0.05, rely=0.08)
        subLabel.place(relx=0.05, rely=0.2)

        nameLabel.place(relx=0.05, rely=0.35)
        versionLabel.place(relx=0.05, rely=0.45)
        newLabel.place(relx=0.05, rely=0.55)
        statusLabel.place(relx=0.05, rely=0.65)

        programNameLabel.place(relx=0.25, rely=0.357)
        programVersionLabel.place(relx=0.25, rely=0.457)
        programNewLabel.place(relx=0.25, rely=0.557)
        programStatusLabel.place(relx=0.25, rely=0.657)

        searchButton.place(relx=0.66, rely=0.85)
        exitButton.place(relx=0.05, rely=0.85)

        Window.mainloop()

    def close(self):
        Window.destroy()
        shutil.rmtree('temp')

    def search(self):
        searchButton.place_forget()
        old_version = str(open('version.txt', 'r').readlines()[0])
        programVersionText.set('VERSION ' + str(open('version.txt', 'r').readlines()[0]))
        os.chdir('tools/temp')
        main_url = self.CONFIG_PROGRAM_GITHUB.replace('github.com', 'raw.githubusercontent.com') + '/master/' + self.CONFIG_PROGRAM_FILES
        version_url = self.CONFIG_PROGRAM_GITHUB.replace('github.com', 'raw.githubusercontent.com') + '/master/' + self.CONFIG_PROGRAM_FILE_VERSION
        urllib.request.urlretrieve(main_url, 'main.py')
        urllib.request.urlretrieve(version_url, 'version_new.txt')
        new_version = str(open('version_new.txt', 'r').readlines()[0])
        programNewText.set('VERSION ' + str(open('version_new.txt', 'r').readlines()[0]))
        os.chdir('../')
        os.chdir('../')
        if float(new_version) > float(old_version):
            programStatusText.set('UPDATE AVAILABLE')
            updateButton.place(relx=0.69, rely=0.85)
        else:
            programStatusText.set('NO UPDATE AVAILABLE')

    def check(self):
        old_version = str(open('version.txt', 'r').readlines()[0])
        os.chdir('tools/temp')
        main_url = self.CONFIG_PROGRAM_GITHUB.replace('github.com', 'raw.githubusercontent.com') + '/master/' + self.CONFIG_PROGRAM_FILES
        version_url = self.CONFIG_PROGRAM_GITHUB.replace('github.com', 'raw.githubusercontent.com') + '/master/' + self.CONFIG_PROGRAM_FILE_VERSION
        urllib.request.urlretrieve(main_url, 'main.py')
        urllib.request.urlretrieve(version_url, 'version_new.txt')
        new_version = str(open('version_new.txt', 'r').readlines()[0])
        os.chdir('../')
        os.chdir('../')
        if float(new_version) > float(old_version):
            return True
        else:
            return False

    def update(self):
        """os.chdir('tools/temp')
        main_url = self.CONFIG_PROGRAM_GITHUB.replace('github.com', 'raw.githubusercontent.com') + '/master/' + self.CONFIG_PROGRAM_FILES
        os.rename('../../' + self.CONFIG_PROGRAM_FILES, self.CONFIG_PROGRAM_FILES + '.old')
        urllib.request.urlretrieve(main_url, 'main.py')
        os.rename('main.py', '../../' + self.CONFIG_PROGRAM_FILES)
        updateButton.place_forget()
        programStatusText.set('UPDATE DOWNLOADED')
        os.remove('../../version.txt')
        os.rename('version_new.txt', '../../version.txt')
        notesButton.place(relx=0.66, rely=0.85)
        os.chdir('../')
        os.chdir('../')"""

        """
        cwd = str(os.getcwd())
        cwd = cwd.replace(os.sep, '/')
        counter = 0
        folder = []
        x = len(cwd) - 1
        while True:
            if cwd[x] != '/':
                counter += 1
                x = len(cwd) - counter
                folder.insert(0, cwd[x])
                continue
            else:
                break
        folder.remove('/')
        folder = "".join(folder)
        os.chdir('../')
        shutil.make_archive(folder + '-BACKUP', 'zip', folder)
        urllib.request.urlretrieve('https://github.com/dakinfemiwa/MESSAGING/archive/master.zip', folder + '-NEW.zip')
        zip = zipfile.ZipFile(folder + '-NEW.zip')
        try:
            shutil.rmtree(folder, ignore_errors=True)
        except PermissionError:
            pass
        zip.extractall(folder)
        # os.rename('MESSAGING-master', folder)"""



    def notes(self):
        pass

        
if __name__ == '__main__':
    Main = Updater()
    Main.draw()
    
