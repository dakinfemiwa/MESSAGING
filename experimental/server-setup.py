import configparser


# Class used to setup servers - no verification checks.
class ServerSetup:
    def __init__(self):
        self.configFile = 'server-config.ini'
        self.defaultContents = '[Server]\nName: Server\nServer Version: 1.00b\nMinimum Version: 0.00\nDuplicate Names: N\n\n[Connection]\nAddress: 0.0.0.0\nPort: 6666'

    def setup(self):
        file = open(self.configFile, 'w+')
        file.write(self.defaultContents)
        file.close()

        config = configparser.ConfigParser()
        config.read(self.configFile)
        config['Server']['Name'] = input('Server Name: ')
        config['Server']['Minimum Version'] = str(float(input('Minimum Version (default. none): ')))
        config['Server']['Duplicate Names'] = input('Allow duplicate usernames [Y/N]: ')
        config['Connection']['Address'] = input('Server Address (default. 0.0.0.0): ')
        config['Connection']['Port'] = input('Server Port (default. 6666): ')

        with open(self.configFile, 'w') as configfile:
            config.write(configfile)


if __name__ == '__main__':
    Setup = ServerSetup()
    Setup.setup()
