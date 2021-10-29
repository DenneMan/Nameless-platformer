from game import Game
import menu

g = Game()

while g.running:
    #g.current_menu.display()
    g.playing = True
    g.game_loop()