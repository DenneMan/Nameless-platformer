import pygame, math
from config import *
from datetime import datetime
import engine
import helper
from world import World

class Scene():
    def __init__(self):
        pass
    def onEnter(self):
        pass
    def onExit(self):
        pass
    def input(self, sm):
        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP = False, False, False, False, False, False, False, False, False, False, False, False
        self.mouse_pos = pygame.mouse.get_pos()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.BACK = True
        # Keyboard input
        active_keys = pygame.key.get_pressed()
        if active_keys[pygame.K_SPACE]:
            self.JUMP = True
        if active_keys[pygame.K_a]:
            self.LEFT = True
        if active_keys[pygame.K_d]:
            self.RIGHT = True
        if active_keys[pygame.K_LSHIFT]:
            self.DASH = True
    def update(self, sm, dt):
        pass
    def draw(self, sm, surface):
        pass

class MainMenu(Scene):
    def __init__(self):
        current_hour = int(str(datetime.now().time())[:2])
        if current_hour >= 20 or current_hour <= 5:
            cycle = 'Night'
        else:
            cycle = 'Day'
        directory = 'assets\\sprites\\Parallax Pixel Skies\\'
        self.background = [
            [pygame.transform.scale(pygame.image.load(directory + cycle + '\\back.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)],
            [pygame.transform.scale(pygame.image.load(directory + cycle + '\\mid.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)],
            [pygame.transform.scale(pygame.image.load(directory + cycle + '\\front.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)]]
        self.start_button = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 80), "Play", (255, 255, 255), (SCREEN_W/2, SCREEN_H/2), "center"), (100, 100, 100), (200, 200, 200))
    def input(self, sm):
        super().input(sm)
        if self.BACK:
            sm.pop()
            sm.push(Fade(self, None, 0.5))
        if self.start_button.collide(pygame.mouse.get_pos()):
            if self.M1:
                sm.push(Fade(self, Game(), 0.5))
        self.start_button.highlight(pygame.mouse.get_pos())
    def update(self, sm, dt):
        for i, image in enumerate(self.background):
            image[1].x -= dt * i * 20 + dt * 10
            if image[1].x < -SCREEN_W:
                image[1].x = 0
    def draw(self, sm, surface):
        for image in self.background:
            surface.blit(image[0], (image[1].x, 0))
            surface.blit(image[0], (image[1].x + SCREEN_W, 0))
        self.start_button.draw(surface)


class Game(Scene):
    def __init__(self):
        engine.entities = []
        self.camera_sys = engine.CameraSystem()
        self.playing, self.running = False, True

        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP = False, False, False, False, False, False, False, False, False, False, False, False

        self.player = helper.instantiate('player', SCREEN_W / 2, 400, False)

        dummy = helper.make_dummy(SCREEN_W / 2, SCREEN_H / 2, False)

        self.camera_sys = engine.CameraSystem()

        self.wall_tileset = engine.load_spritesheet('assets\\tilesets\\Walls.png', 32, 32)
        self.bg_tileset = engine.load_spritesheet('assets\\tilesets\\background\\background.png', 32, 32)
        World(self.wall_tileset, self.bg_tileset, 'assets\\tilesets\\walls\\Map.json')

        engine.entities.append(dummy)
        engine.entities.append(self.player)

        self.text = pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50)
    def input(self, sm):
        super().input(sm)
        if self.BACK:
            sm.pop()
            sm.push(Fade(self, None, 0.5))
        if self.M1:
            self.player.controller.attack()
        if self.SCR_DOWN:
            self.player.camera.zoom -= 0.05
            self.player.camera.zoom = max(self.player.camera.zoom, 0.5)
        if self.SCR_UP:
            self.player.camera.zoom += 0.05
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
    def update(self, sm, dt):
        engine.update(dt, self.player)
    def draw(self, sm, surface):
        self.camera_sys.update(surface)

class Transition(Scene):
    def __init__(self, fromScene, toScene, length):
        self.percentage = 0
        self.fromScene = fromScene
        self.toScene = toScene
        self.length = length
    def update(self, sm, dt):
        if self.fromScene is not None:
            self.fromScene.update(sm, dt)
        if len(sm.scenes) > 1:
            if self.toScene is None:
                sm.scenes[-2].update(sm, dt)
            else:
                self.toScene.update(sm, dt)
        self.percentage += (dt / self.length) * 100
        if self.percentage >= 100:
            sm.pop()
            if self.toScene != None:
                sm.push(self.toScene)

class Fade(Transition):
    def draw(self, sm, surface):
        if self.percentage < 50:
            if self.fromScene is not None:
                self.fromScene.draw(sm, surface)
        else:
            if len(sm.scenes) > 1:
                if self.toScene is None:
                    sm.scenes[-2].draw(sm, surface)
                else:
                    self.toScene.draw(sm, surface)
        overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        # Less cpu intensive parabola that looks worse: "alpha = -0.1 * pow(self.percentage, 2) + 10 * self.percentage"
        # Use parabola function to get a smother fade \/
        alpha = math.sqrt(-26.01 * (self.percentage - 100) * (self.percentage))
        overlay.set_alpha(alpha)
        surface.blit(overlay, (0, 0))

class SceneManager:
    def __init__(self):
        self.scenes = []
    def isEmpty(self):
        return len(self.scenes) == 0
    def input(self):
        if not self.isEmpty():
            self.scenes[-1].input(self)
    def update(self, dt):
        if not self.isEmpty():
            self.scenes[-1].update(self, dt)
    def draw(self, surface):
        if not self.isEmpty():
            self.scenes[-1].draw(self, surface)
    def push(self, scene):
        if not self.isEmpty():
            self.scenes[-1].onExit()
        self.scenes.append(scene)
        self.scenes[-1].onEnter()
    def pop(self):
        self.scenes[-1].onExit()
        self.scenes.pop()
        if not self.isEmpty():
            self.scenes[-1].onEnter()