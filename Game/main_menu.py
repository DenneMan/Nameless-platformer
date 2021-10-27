import pygame, sys, pathlib, time
import engine
import helper
from world import World
from config import *
import game

def Main():
    #######################################
    #  Initialize variables and funcions  #
    #######################################
    pygame.init()

    canvas = pygame.Surface((SCREEN_W, SCREEN_H))
    display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Platformer')

    button = pygame.Rect((50, 50, 100, 40))
    button.center = (SCREEN_W / 2, SCREEN_H / 2)

    play_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), 'Play', (245, 217, 76), button.center, 'center')
    ####################
    #  Main game loop  #
    ####################
    while True:
        mouse_pos = pygame.mouse.get_pos()
        released_pos = (-100000, -100000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = mouse_pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    released_pos = mouse_pos
        
        if button.collidepoint(released_pos):
            print('clicked')
            game.Main()

        canvas.fill((39, 39, 54))

        pygame.draw.rect(canvas, (100, 100, 100), button)
        play_text.draw(canvas)

        display.blit(canvas, (0, 0))
        pygame.display.update()

if __name__ == "__main__":
    Main()