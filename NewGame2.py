from tkinter import *
import _thread
import time
from tools.logger import Logger
import socket
import ast
import random


class Connect:
    def __init__(self, uName):
        self.WINDOW_BACKGROUND = '#141414'
        self.WINDOW_FOREGROUND = '#FFFFFF'
        self.WINDOW_RESOLUTION = '600x350'
        self.WINDOW_TITLE = 'Placeholder'

        self.IP = '127.0.0.1'
        self.PORT = 6666

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.clientSocket.connect((self.IP, self.PORT))

        self.makeItems()

    def makeItems(self):
        while True:
            time.sleep(random.randint(6, 8))
            locX2 = random.uniform(0.20, 0.90)
            locY2 = random.uniform(0.20, 0.85)
            self.clientSocket.send(str.encode(f'ITEM<>{locX2:.2f},{locY2:.2f}'))
            print('done')
            # time.sleep(20)


if __name__ == '__main__':
    T = Connect('T')
