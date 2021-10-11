import pygame, sys, time
import engine
from player import Player
from settings import *

#######################################
#  Initialize variables and funcions  #
#######################################
pygame.init()

canvas = pygame.Surface((SCREEN_W, SCREEN_H))
display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Platformer')

player_images = engine.load_spritesheet('assets/sprites/character.png', 16)

center_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 256), '', (245, 217, 76), (SCREEN_W / 2, SCREEN_H / 2), 'center')


colliders = []
colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2, SCREEN_H / 2 + 32, 512, 64))
colliders.append(pygame.Rect(SCREEN_W / 2 + 512 / 2, SCREEN_H / 2 - 32, 64, 64))
colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2 - 64, SCREEN_H / 2 - 32, 64, 64))

colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2, SCREEN_H / 5, 512, 64))


direction = STOP

last_frame_time = time.time()

# Cleanup crew:

player = engine.Entity()
player.transform = engine.Transform(SCREEN_W / 2, SCREEN_H / 3, 64, 64)
player.animations.add('idle', engine.Animation(player_images[0:3], 3))
player.animations.add('running', engine.Animation(player_images[8:16], 8))
player.animations.add('jump', engine.Animation(player_images[8:9], 1))
player.animations.add('apex', engine.Animation(player_images[9:10], 1))
player.animations.add('fall', engine.Animation(player_images[10:11], 1))
player.animations.add('land', engine.Animation(player_images[3:8], 16))
player.controller = Player(player.transform)

coin_images = engine.load_spritesheet('assets/sprites/coin.png', 8)

coin = engine.Entity()
coin.transform = engine.Transform(300, 300, 32, 32)
coin.animations.add('idle', engine.Animation(coin_images, 14))
coin.type = 'collectable'

camera_sys = engine.CameraSystem()
player.camera = engine.Transform(20, 20, SCREEN_W - 40, SCREEN_H - 40)

entities = []
entities.append(coin)
entities.append(player)

# Delta time (time between frames) function, used for equations that contain time (ex. Distance = Speed * Time)
# This is used to create frame rate independancy, I.e nomatter how low or how high the fps is, movement is the same
def getDeltaTime():
    global last_frame_time
    this_frame_time = time.time()
    delta_time = this_frame_time - last_frame_time
    last_frame_time = this_frame_time
    return delta_time

####################
#  Main game loop  #
####################
while True:
    # Get delta time
    dt = getDeltaTime()
    
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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

    # Update entities
    for entity in entities:
        entity.animations.animations_list[entity.state].update(dt)

        if entity.type == 'collectable':
            if player.transform.get_rect().colliderect(entity.transform.get_rect()):
                entities.remove(entity)
                # TODO Increment score and display it

        if entity.controller != None:
            entity.controller.update(dt, colliders)

    # Draw visuals
    canvas.fill((0, 0, 0))

    center_text.draw(canvas)

    camera_sys.update(canvas, entities, colliders)

    display.blit(canvas, (0, 0))
    pygame.display.flip()