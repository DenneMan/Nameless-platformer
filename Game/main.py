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

player_images = engine.load_spritesheet('assets/character/spritesheet.png', 16)
player_animation = engine.Animation(player_images, 3, 0, 2) # IDLE

center_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 256), '', (245, 217, 76), (SCREEN_W / 2, SCREEN_H / 2), 'center')

pygame.display.set_caption('Platformer')

colliders = []
colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2, SCREEN_H / 2 + 32, 512, 64))
colliders.append(pygame.Rect(SCREEN_W / 2 + 512 / 2, SCREEN_H / 2 - 32, 64, 64))
colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2 - 64, SCREEN_H / 2 - 32, 64, 64))

colliders.append(pygame.Rect(SCREEN_W / 2 - 512 / 2, SCREEN_H / 5, 512, 64))

player = Player(player_animation)
direction = STOP

last_frame_time = time.time()

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
    player.update(dt, direction, colliders, center_text)

    # Draw visuals
    canvas.fill((28, 28, 28))

    for collider in colliders:
        pygame.draw.rect(canvas, (255, 255, 255), collider)
    player.draw(canvas, dt)

    center_text.draw(canvas)

    display.blit(canvas, (0, 0))
    pygame.display.flip()