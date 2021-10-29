import pygame, sys, pathlib, time
import engine
import helper
from menu import Loading
from world import World
from config import *

class timer():
    def __init__(self):
        self.times = []
        self.average = 0
        self.time_between = 0
        self.stop_time = 0
        self.start_time = 0
    def start(self):
        self.start_time = time.time()
    def stop(self):
        self.stop_time = time.time()
        self.time_between = self.stop_time - self.start_time
        self.times.append(self.time_between)
        self.average = sum(self.times) / len(self.times)
full_timer = timer()
update_timer = timer()
draw_timer = timer()

class Game():
    def __init__(self):
        pygame.init()

        self.canvas = pygame.Surface((SCREEN_W, SCREEN_H))
        self.display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('Platformer')

        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP = False, False, False, False, False, False, False, False, False, False, False, False
        self.playing, self.running = False, True

        self.player = helper.instantiate('player', SCREEN_W / 2, 400, False)
        self.player.gui = engine.GUI(self.player.camera)
        coins_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '0', (245, 217, 76), (50, 2), 'topleft')
        self.player.gui.add_text(coins_text)
        self.player.gui.add_text(helper.combo_text)

        dummy = helper.make_dummy(SCREEN_W / 2, SCREEN_H / 2, False)

        self.camera_sys = engine.CameraSystem()

        wall_tileset = engine.load_spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\Walls.png', 32, 32)
        bg_tileset = engine.load_spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\background\\background.png', 32, 32)
        World(wall_tileset, bg_tileset, str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\walls\\Map.json')

        engine.entities.append(dummy)
        engine.entities.append(self.player)

        self.text = pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50)
        self.current_menu = Loading(self)

    def game_loop(self):
        while self.playing:
            if DEBUG: full_timer.start()
            self.dt = engine.deltaTime()
            self.get_keys()
            if self.M1:
                self.player.controller.attack()
            if self.SCR_DOWN:
                self.player.camera.zoom -= self.dt * 6
                self.player.camera.zoom = max(self.player.camera.zoom, 0.5)
            if self.SCR_UP:
                self.player.camera.zoom += self.dt * 6
                self.player.camera.zoom = min(self.player.camera.zoom, 2)
            if self.BACK:
                self.playing = False
            if self.JUMP:
                self.player.controller.is_jumping = True
            self.player.controller.direction = STOP
            if self.LEFT and not self.RIGHT:
                self.player.controller.direction = LEFT
            if self.RIGHT and not self.LEFT:
                self.player.controller.direction = RIGHT
            if self.DASH:
                self.player.controller.is_dashing = True

            if DEBUG: update_timer.start()
            engine.update(self.dt, self.player)
            if DEBUG: update_timer.stop()
            
            self.canvas.fill((0, 0, 0))

            self.camera_sys.update(self.canvas)
            
            if DEBUG: draw_timer.start()
            self.display.blit(self.canvas, (0, 0))
            if DEBUG: draw_timer.stop()
            pygame.display.flip()
            self.reset_keys()
            if DEBUG: full_timer.stop()
            if DEBUG: print(f"Draw is {round((draw_timer.average / full_timer.average) * 100, 2)}%, Update is {round((update_timer.average / full_timer.average) * 100, 2)}%")

    def get_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.current_menu.displaying = False
            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.M1 = True
                if event.button == 4:
                    self.SCR_DOWN = True
                if event.button == 5:
                    self.SCR_UP = True
        # Keyboard input
        active_keys = pygame.key.get_pressed()
        if active_keys[pygame.K_ESCAPE]:
            self.BACK = True
        if active_keys[pygame.K_SPACE]:
            self.JUMP = True
        if active_keys[pygame.K_a]:
            self.LEFT = True
        if active_keys[pygame.K_d]:
            self.RIGHT = True
        if active_keys[pygame.K_LSHIFT]:
            self.DASH = True

    def reset_keys(self):
        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP = False, False, False, False, False, False, False, False, False, False, False, False