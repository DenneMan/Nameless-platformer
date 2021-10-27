import pygame
import time
import random
from pygame.constants import K_SPACE, KEYDOWN

pygame.init()

Y = 200
X = 330

black = (0, 0, 0)

movement = ""
gravi = 0.15
gravity = 0

p_x = 100
p_y = 500
display = pygame.display.set_mode((1360, 660))

bg = pygame.Surface((0, 0))

fps = pygame.time.Clock()

flappy = pygame.Surface((1, 1))
flappy.fill((255, 0, 0))
pygame.transform.scale(flappy, (100,100))

pipe1 = pygame.Surface((1, 1))
pipe1.fill((0, 255, 0))
pipe = pygame.transform.scale(pipe1, (50,400))
pipe_rect = pipe.get_rect()
#pipe2 =  pygame. transform. rotate(pipe1, 180)
#pipe2 = pygame.transform.scale(pipe2, (500,400))

pipe_start_x = 50
pipe_start_y = 50

pipe_list = []

pipe_list.append(pipe_rect)

pipe_time = pygame.time.get_ticks() / 1000
time = pygame.time.get_ticks() / 1000

running = True
while running == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                movement = "up"
            if event.key == pygame.K_w:
                pipe_rect = pipe_rect.copy()
                pipe_rect.x = pipe_start_x
                pipe_rect.y = pipe_start_y
                pipe_list.append(pipe_rect)

        if movement == "up":
            movement = "i"
            Y = Y - 50
            gravi = 0.05
            gravity = 0

    if movement != "":
        Y = Y + gravity
        grav = gravi + gravi
        gravity += grav

    if Y >= 506:
        movement = ""
        Y = 200
        gravi = 0.05
        gravity = 0

    
    display.blit(bg, (0, 0))

  
        
    
    display.blit(flappy, (X, Y))
    
    print(pipe_list)
    for rect in pipe_list:
        #display.blit(pipe2, (p_x+ 38, 600))
        rect.x += 1
        display.blit(pipe, rect)

    #display.blit(pipe2, (300 +38, p_y - 600))
    #display.blit(pipe, (300, p_y))

    fps.tick(70)
    pygame.display.update()
    display.fill(black)