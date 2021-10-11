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

player_images = engine.load_spritesheet('assets/sprites/character.png', 16)
player_animations = engine.Animations()
player_animations.add('idle', engine.Animation(player_images[0:3], 3))
player_animations.add('running', engine.Animation(player_images[8:16], 8))
player_animations.add('jump', engine.Animation(player_images[8:9], 1))
player_animations.add('apex', engine.Animation(player_images[9:10], 1))
player_animations.add('fall', engine.Animation(player_images[10:11], 1))
player_animations.add('land', engine.Animation(player_images[3:8], 16))

#player_animation = engine.Animation(player_images, 3, 0, 2) # IDLE

center_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 256), '', (245, 217, 76), (SCREEN_W / 2, SCREEN_H / 2), 'center')

pygame.display.set_caption('Platformer')

colliders = []
colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2, SCREEN_H / 2 + 32, 512, 64))
colliders.append(pygame.Rect(SCREEN_W / 2 + 512 / 2, SCREEN_H / 2 - 32, 64, 64))
colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2 - 64, SCREEN_H / 2 - 32, 64, 64))

colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2, SCREEN_H / 5, 512, 64))

player = Player(player_animations)
direction = STOP

last_frame_time = time.time()

# Cleanup crew:

entities = []

coin_images = engine.load_spritesheet('assets/sprites/coin.png', 8)

coin = engine.Entity()
coin.transform = engine.Transform(300, 300, 32, 32)
coin.animations.add('idle', engine.Animation(coin_images, 14))
coin.type = 'collectable'

entities.append(coin)

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
        player.is_jumping = True
    if active_keys[pygame.K_a] and not active_keys[pygame.K_d]:
        direction = LEFT
    elif active_keys[pygame.K_d] and not active_keys[pygame.K_a]:
        direction = RIGHT
    else:
        direction = STOP
    if active_keys[pygame.K_LSHIFT]:
        player.is_dashing = True

    # Update entities
    for entity in entities:
        entity.animations.animations_list[entity.state].update(dt)

        if entity.type == 'collectable':
            if player.rect.colliderect(entity.transform.rect):
                entities.remove(entity)
                # TODO Increment score and display it


    player.update(dt, direction, colliders, center_text)

    # Draw visuals
    canvas.fill((28, 28, 28))

    for collider in colliders:
        pygame.draw.rect(canvas, (255, 255, 255), collider)
    player.draw(canvas, dt)

    # Draw entities
    for entity in entities:
        entity.animations.animations_list[entity.state].draw(canvas, (entity.transform.x, entity.transform.y), (entity.transform.width, entity.transform.height), False, False)

    center_text.draw(canvas)

    display.blit(canvas, (0, 0))
    pygame.display.flip()