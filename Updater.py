import os
import urllib.request


class Update():
    def Download(self):
        try:
            os.remove('temp')
            os.mkdir('temp')
        except:
            pass
        os.chdir('temp')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/dakinfemiwa/MESSAGING/master/version.txt',
                                   'version.txt')
        updateInfo = open('version.txt', 'r+')
        latestVersion = updateInfo.readlines()[0]
        updateInfo.close()
        urllib.request.urlretrieve('https://raw.githubusercontent.com/dakinfemiwa/MESSAGING/master/UI-Chat.py',
                                   'UI-Chat.py')

        os.chdir('..')
        return latestVersion

    def Switch(self):
        os.remove('version.txt')
        os.rename('UI-Chat.py', 'temp/UI-Chat-old.py')
        os.chdir('temp')
        os.rename('UI-Chat.py', '../UI-Chat.py')
        os.rename('version.txt', '../version.txt')
        os.chdir('..')
