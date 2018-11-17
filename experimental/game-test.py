from experimental import game, menu

GHub = game.GameHub()
GHub.draw()

while True:
    if not GHub.logged():
        continue
    myData = GHub.get()
    break

menu.GameMenu.draw()
