import pygame, sys, pathlib, time
import engine
import helper
from datetime import datetime
from world import World
from config import *
import game

class Menu():
    def __init__(self, game):
        self.game = game
        self.run_display = True
    
    def draw(self):
        self.game.window.blit(self.game.canvas, (0, 0))
        pygame.display.update()
        self.reset_keys

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.small_canvas = pygame.Surface((240, 135))
        self.state = "Start"

        self.back_x = 0
        self.mid_x = 0
        self.front_x = 0
    
    def display_menu(self):

        current_hour = int(str(datetime.now().time())[:2])
        if current_hour >= 20 or current_hour <= 5:
            cycle = 'Night\\'
        else:
            cycle = 'Day\\'
        self.background = self.import_background(cycle)
        self.title = pygame.transform.scale(pygame.image.load('assets\\sprites\\KingsQuest.png').convert_alpha(), (129 * 8, 39 * 8))

        self.displaying = True
        while self.displaying:
            self.dt = engine.deltaTime()
            self.game.get_keys()
            self.handle_parallax()
            self.game.canvas.blit(self.title, (SCREEN_W / 2 - self.title.get_width() / 2, 5 * 8))
            self.game.reset_keys()
            self.game.display.blit(self.game.canvas, (0, 0))
            pygame.display.flip()

    def import_background(self, cycle):
        directory = 'assets\\sprites\\Parallax Pixel Skies\\'
        images = [
            [pygame.transform.scale(pygame.image.load(directory + cycle + 'back.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)],
            [pygame.transform.scale(pygame.image.load(directory + cycle + 'mid.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)],
            [pygame.transform.scale(pygame.image.load(directory + cycle + 'front.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)]]
        return images

    def handle_parallax(self):
        for i, image in enumerate(self.background):
            image[1].x -= self.dt * i * 20 + self.dt * 10
            if image[1].x < -SCREEN_W:
                image[1].x = 0
            self.game.canvas.blit(image[0], (image[1].x, 0))
            self.game.canvas.blit(image[0], (image[1].x + SCREEN_W, 0))




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
