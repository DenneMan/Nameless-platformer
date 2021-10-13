import pygame, sys, random
import engine
import helper
from settings import *

#######################################
#  Initialize variables and funcions  #
#######################################
pygame.init()

canvas = pygame.Surface((SCREEN_W, SCREEN_H))
display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Platformer')


#center_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 256), '', (245, 217, 76), (SCREEN_W / 2, SCREEN_H / 2), 'center')


_colliders = []
_colliders.append(pygame.Rect(2, 7, 12, 1))
#_colliders.append(pygame.Rect())
#_colliders.append(pygame.Rect())
#_colliders.append(pygame.Rect())

direction = STOP

colliders = []
for collider in _colliders:
    colliders.append(pygame.Rect(collider[0] * TILE_SIZE, collider[1] * TILE_SIZE, collider[2] * TILE_SIZE, collider[3] * TILE_SIZE))


#coin = helper.instantiate('coin', 300, 300, False)

player = helper.instantiate('player', SCREEN_W / 2, 0, False)
for i in range(10):
    engine.entities.append(helper.instantiate('coin', SCREEN_W / 2, SCREEN_H / 2 - 60, False))

#dash = helper.instantiate('dash', SCREEN_W / 2, SCREEN_H / 3, False)

camera_sys = engine.CameraSystem()
player.camera = engine.Camera(0, 0, SCREEN_W, SCREEN_H)
player.camera.set_world_pos(player.transform.pos.x, player.transform.pos.y)
player.camera.track_entity(player)
player.gui = engine.GUI(player.camera)
player.gui.add_sprite(helper.coin_images[0], (10, 10), (32, 32))
coins_text = engine.GUIText(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '1', (245, 217, 76), (50, 2), 'topleft')
player.gui.add_text(coins_text)


#engine.entities.append(coin)
engine.entities.append(player)

score = 0

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
    if active_keys[pygame.K_a] and not active_keys[pygame.K_d]:
        player.controller.direction = LEFT
    elif active_keys[pygame.K_d] and not active_keys[pygame.K_a]:
        player.controller.direction = RIGHT
    else:
        player.controller.direction = STOP
    if active_keys[pygame.K_LSHIFT]:
        player.controller.is_dashing = True
    
    active_buttons = pygame.mouse.get_pressed()
    if active_buttons[1]:
        ...

    # Update entities

    for entity in engine.entities:
        entity.animations.animations_list[entity.state].update(dt)

        if entity.type == 'collectable':
            if player.transform.get_rect().colliderect(entity.transform.get_rect()):
                engine.entities.remove(entity)
                score += 1
                # TODO Increment score and display it

        if entity.controller != None:
            entity.controller.update(dt, colliders)
    coins_text.set_text(str(score))

    # Draw visuals
    canvas.fill((0, 0, 0))

    camera_sys.update(canvas, colliders)

    display.blit(canvas, (0, 0))
    pygame.display.flip()