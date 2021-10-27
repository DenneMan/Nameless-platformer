from game import Game
import menu

g = Game()

while g.running:
    g.playing = True
    g.game_loop()