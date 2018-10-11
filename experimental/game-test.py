import game
import menu
import _thread

GHub = game.GameHub()
GHub.draw()

while True:
    if not GHub.logged():
        continue
    myData = GHub.get()
    break

menu.GameMenu.draw()
