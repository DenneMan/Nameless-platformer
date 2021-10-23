import pygame, sys, pathlib
import engine
import helper
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

player = helper.make_moveable_empty(SCREEN_W / 2, 128,)

camera_sys = engine.CameraSystem()

world = helper.load_level()

engine.entities.append(player)

spritesheet = Spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tileset\\Walls')
test = spritesheet.parse_all()

####################
#  Main game loop  #
####################
while True:
    # Get delta time
    dt = engine.deltaTime()
    
    # Get Input

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (int(((mouse_pos[0] - camera_sys.offset.x) / 128) * 2), int(((mouse_pos[1] - camera_sys.offset.y) / 128) * 2))
                for entity in engine.entities:
                    if entity.name == 'world':
                        if str(mouse_pos) in entity.children:
                            entity.children.pop(str(mouse_pos))
                print(player.camera.zoom)

            if event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (int(((mouse_pos[0] - camera_sys.offset.x) / 128) * 2), int(((mouse_pos[1] - camera_sys.offset.y) / 128) * 2))
                for entity in engine.entities:
                    if entity.name == 'world':
                        entity.children[str(mouse_pos)] = helper.make_tile(mouse_pos[0], mouse_pos[1], 0)
                
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
    if active_keys[pygame.K_w]:
        player.controller.direction.y = -1
    elif active_keys[pygame.K_s]:
        player.controller.direction.y = 1
    else:
        player.controller.direction.y = 0

    if active_keys[pygame.K_a]:
        player.controller.direction.x = -1
    elif active_keys[pygame.K_d]:
        player.controller.direction.x = 1
    else:
        player.controller.direction.x = 0
    
    active_buttons = pygame.mouse.get_pressed()

    # Update entities

    engine.update(dt, player)

    # Draw visuals
    canvas.fill((0, 0, 0))

    camera_sys.update(canvas)

    canvas.blit(pygame.transform.scale(test['top_and_left'], (TILE_SIZE, TILE_SIZE)), (0, 0))
    display.blit(canvas, (0, 0))
    pygame.display.flip()