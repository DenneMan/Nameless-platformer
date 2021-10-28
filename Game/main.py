from game import Game
import menu

g = Game()

while g.running:
    g.current_menu.display_menu()
    g.game_loop()