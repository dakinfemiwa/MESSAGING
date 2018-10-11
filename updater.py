import os
import urllib.request

# Replace by SM_UPDATER


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
        urllib.request.urlretrieve('https://raw.githubusercontent.com/dakinfemiwa/MESSAGING/master/chat.py',
                                   'chat.py')

        os.chdir('..')
        return latestVersion

    def Switch(self):
        try:
            os.remove('temp/UI-Chat-old.py')
            print('INFO: Removed previous backup.')
        except:
            pass
        os.remove('version.txt')
        os.rename('chat.py', 'temp/UI-Chat-old.py')
        os.chdir('temp')
        os.rename('chat.py', '../chat.py')
        os.rename('version.txt', '../version.txt')
        os.chdir('..')
