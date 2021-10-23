import pygame, sys, pathlib

from pygame import sprite
import engine
import helper
from world import World
from spritesheet import Spritesheet
from config import *

#######################################
#  Initialize variables and funcions  #
#######################################
pygame.init()

canvas = pygame.Surface((SCREEN_W, SCREEN_H))
display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Platformer')

direction = STOP
player = helper.instantiate('player', SCREEN_W / 2, 400, False)
player.gui = engine.GUI(player.camera)
player.gui.add_sprite(helper.coin_images[0], (10, 10), (32, 32))
coins_text = engine.GUIText(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '0', (245, 217, 76), (50, 2), 'topleft')
player.gui.add_text(coins_text)
player.gui.add_text(helper.combo_text)

dummy = helper.make_dummy(SCREEN_W / 2, SCREEN_H / 2, False)

camera_sys = engine.CameraSystem()

wall_tileset = engine.load_spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\Walls.png', 32, 32)
bg_tileset = engine.load_spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\background\\background.png', 32, 32)
world = World(wall_tileset, bg_tileset, str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\walls\\Map.json')

engine.entities.append(dummy)
engine.entities.append(player)

####################
#  Main game loop  #
####################
while True:
    # Get delta time
    dt = engine.deltaTime()
    
    # Get Input
    hit = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.controller.attack()
                hit = True
            if event.button == 4: 
                player.camera.zoom -= dt * 6
                player.camera.zoom = max(player.camera.zoom, 0.1)
            if event.button == 5: 
                player.camera.zoom += dt * 6
                player.camera.zoom = min(player.camera.zoom, 2)
    active_keys = pygame.key.get_pressed()
    if active_keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if active_keys[pygame.K_SPACE]:
        player.controller.is_jumping = True
    player.controller.direction = STOP
    if hit == False:
        if active_keys[pygame.K_a] and not active_keys[pygame.K_d]:
            player.controller.direction = LEFT
        elif active_keys[pygame.K_d] and not active_keys[pygame.K_a]:
            player.controller.direction = RIGHT
    if active_keys[pygame.K_LSHIFT]:
        player.controller.is_dashing = True
    
    active_buttons = pygame.mouse.get_pressed()

    # Update entities

    engine.update(dt, player)

    coins_text.set_text(str(player.score))

    # Draw visuals
    canvas.fill((0, 0, 0))

    camera_sys.update(canvas)
    
    display.blit(canvas, (0, 0))
    pygame.display.flip()