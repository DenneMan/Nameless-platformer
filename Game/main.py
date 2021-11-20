# Python imports
import pygame, os
# Personal imports
import engine, scene, soundmanager, level, universal
from config import *

pygame.init()

# Position the screen at (0, 0) and...
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"
# set the width and height as (SCREEN_W, SCREEN_H) from config.py
display = pygame.display.set_mode((SCREEN_W, SCREEN_H))

universal.sound_manager = soundmanager.SoundManager()
universal.level_manager = level.Level()
universal.scene_manager = scene.SceneManager()
universal.scene_manager.push(scene.Fade(None, scene.MainMenu(), 0.5))

running = True
while running:
    # If scenemanager is empty: close application
    running = not universal.scene_manager.isEmpty()
    universal.scene_manager.input()
    universal.scene_manager.update(engine.deltaTime())
    universal.scene_manager.draw(display)
    pygame.display.flip()   