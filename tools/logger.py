from datetime import datetime


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def log(LOG_MESSAGE, LOG_TYPE="INFO"):
        TIME_PREFIX = str(datetime.now().strftime('%H:%M:%S'))
        print('[{0}] {1}: {2}'.format(TIME_PREFIX, LOG_TYPE, LOG_MESSAGE))


if __name__ == '__main__':
    Logger.log('Test event.', 'ERROR')
