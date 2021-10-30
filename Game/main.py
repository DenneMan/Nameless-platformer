import pygame, os
import engine, scene
from config import *

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"
display = pygame.display.set_mode((SCREEN_W, SCREEN_H))

sm = scene.SceneManager()
sm.push(scene.MainMenu())
running = True
while running:
    running = not sm.isEmpty()
    sm.input()
    sm.update(engine.deltaTime())
    sm.draw(display)
    pygame.display.flip()