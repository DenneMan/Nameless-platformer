# Python imports
import pygame, os
# Personal imports
import engine, scene
from config import *

# Position the screen at (0, 0) and...
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"
# set the width and height as (SCREEN_W, SCREEN_H) from config.py
display = pygame.display.set_mode((SCREEN_W, SCREEN_H))

sm = scene.SceneManager()
sm.push(scene.Fade(None, scene.MainMenu(), 0.5))
running = True
while running:
    # If scenemanager is empty: close application
    running = not sm.isEmpty()
    sm.input()
    sm.update(engine.deltaTime())
    sm.draw(display)
    pygame.display.flip()   