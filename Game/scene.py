import pygame, math, random
from datetime import datetime
import engine, helper, universal
from level import Level
from world import World_Inside, World_Outside
from gui import GUI
from config import *

class Scene():
    def __init__(self):
        pass
    def onEnter(self):
        pass
    def onExit(self):
        pass
    def input(self, sm):
        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP, self.ABILITY = False, False, False, False, False, False, False, False, False, False, False, False, False
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
        if active_keys[pygame.K_e]:
            self.ABILITY = True
    def update(self, sm, dt):
        pass
    def draw(self, sm, surface):
        pass

class MainMenu(Scene):
    def onEnter(self):
        universal.sound_manager.playMusic('stray_cat')
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
    def onEnter(self):
        universal.sound_manager.playMusic('rivaling_force')
    def onExit(self):
        universal.reset_multipliers()
    def __init__(self):
        self.state = 'gaming'

        engine.entities = []
        #self.camera_sys = engine.CameraSystem((39, 39, 54))
        self.out_of_bounds = 25 * TILE_SIZE
        self.camera_sys = engine.CameraSystem((135, 206, 235), self.out_of_bounds)
        self.playing, self.running = False, True

        #self.wall_tileset = engine.load_spritesheet('assets\\sprites\\tilesets\\Walls.png', 32, 32)
        #self.bg_tileset = engine.load_spritesheet('assets\\sprites\\tilesets\\background.png', 32, 32)
        #World_Inside(self.wall_tileset, self.bg_tileset, 'assets\\tilesets\\walls\\Map.json')

        self.tileset = engine.load_spritesheet('assets\\sprites\\tilesets\\Outside.png', 32, 32)
        World_Outside(self.tileset, 'assets\\tilesets\\walls\\Outside_1.json')

        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP = False, False, False, False, False, False, False, False, False, False, False, False

        self.player = helper.instantiate('player', SCREEN_W * 2, 400, False)
        engine.entities.append(self.player)
        enemy = helper.spawn_enemy(SCREEN_W * 2, 400)
        engine.entities.append(enemy)

        self.text = pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50)

        self.gui = GUI()

        self.upgrade_images = engine.load_spritesheet('assets\\sprites\\Icons.png', 24, 24)
        temp = []
        for image in self.upgrade_images:
            temp.append(pygame.transform.scale(image, (256, 256)))
        self.upgrade_images = temp
        self.upgrade_choices = None
        self.upgrade_rects = [pygame.Rect(SCREEN_W / 4 * 1 - 128, SCREEN_H / 2 - 128, 256, 256), pygame.Rect(SCREEN_W / 4 * 2 - 128, SCREEN_H / 2 - 128, 256, 256), pygame.Rect(SCREEN_W / 4 * 3 - 128, SCREEN_H / 2 - 128, 256, 256)]
        self.clicked_upgrade = None
        self.active_upgrades = []
    def input(self, sm):
        super().input(sm)
        if self.BACK:
            sm.pop()
            sm.push(Fade(self, None, 0.5))
        if self.M1:
            if self.state == 'gaming':
                self.player.controller.attack()
            elif self.state == 'upgrading':
                for i in range(3):
                    if self.upgrade_rects[i].collidepoint(pygame.mouse.get_pos()):
                        self.clicked_upgrade = i
        #if self.SCR_DOWN:
        #    self.player.camera.zoom -= 0.5
        #    self.player.camera.zoom = max(self.player.camera.zoom, 0.5)
        #if self.SCR_UP:
        #    self.player.camera.zoom += 0.5
        #    self.player.camera.zoom = min(self.player.camera.zoom, 2)
        if self.BACK:
            self.playing = False
        if self.JUMP:
            self.player.controller.is_jumping = True
        self.player.controller.direction = 'stop'
        if self.LEFT and not self.RIGHT:
            self.player.controller.direction = 'left'
        if self.RIGHT and not self.LEFT:
            self.player.controller.direction = 'right'
        if self.DASH:
            self.player.controller.is_dashing = True
        if self.player.controller.health <= 0 or self.player.collider.t > self.out_of_bounds:
            sm.pop()
            sm.push(Fade(self, None, 0.5))
        if universal.soul_blast and self.ABILITY:
            ...
            #soul.Soul(self.player.collider.l + self.player.collider.w / 2, self.player.collider.t + self.player.collider.h / 2)
    def update(self, sm, dt):
        if self.state == 'gaming':
            for entity in engine.entities:
                if entity.animations != None:
                    entity.animations.update(dt)

                if entity.type == 'collectable':
                    p_rect = pygame.Rect(self.player.collider.l, self.player.collider.t, self.player.collider.w, self.player.collider.h)
                    e_rect = pygame.Rect(entity.collider.l, entity.collider.t, entity.collider.w, entity.collider.h)
                    if p_rect.colliderect(e_rect):
                        universal.sound_manager.playSound('coin_pickup_' + str(random.randint(1, 3)))
                        engine.entities.remove(entity)

                if entity.destruct:
                    entity.destruct_timer -= dt
                    if entity.destruct_timer <= 0:
                        if entity.name == "enemy":
                            universal.level_manager.give_exp(entity.controller.max_health)
                            helper.spawn_coins(entity.collider.l + entity.collider.w / 2, entity.collider.t + entity.collider.h / 2, int((entity.controller.max_health / 100) * universal.gold_mult))
                            if universal.lifesteal_mult != 0:
                                self.player.controller.health += entity.controller.max_health * universal.lifesteal_mult
                        engine.entities.remove(entity)
                else:
                    if entity.name == "enemy":
                        if entity.collider.t > self.out_of_bounds:
                            universal.level_manager.give_exp(entity.controller.max_health / 9)
                            engine.entities.remove(entity)


                if entity.controller != None:
                    entity.controller.update(dt)
            self.gui.update(dt)
            a = 0
            for e in engine.entities:
                if e.name == 'enemy':
                    a += 1
            if a == 0:
                enemy = helper.spawn_enemy(SCREEN_W * 2, 400)
                engine.entities.append(enemy)
        elif self.state == 'upgrading':
            if self.clicked_upgrade != None:
                self.state = 'gaming'
                self.active_upgrades.append(self.upgrade_choices[self.clicked_upgrade])

                if self.upgrade_choices[self.clicked_upgrade] == 6:
                    universal.gold_mult += 0.5
                if self.upgrade_choices[self.clicked_upgrade] == 10:
                    universal.lifesteal_mult += 0.05
                if self.upgrade_choices[self.clicked_upgrade] == 20:
                    universal.damage_mult += 0.2
                if self.upgrade_choices[self.clicked_upgrade] == 22:
                    universal.resistance_mult += 0.2

                self.clicked_upgrade = None
    def draw(self, sm, surface):
        self.camera_sys.update(surface)
        self.gui.draw(surface, self.camera_sys.offset)
        if self.state == 'upgrading':
            fill = pygame.Surface((SCREEN_W, SCREEN_H))
            fill.fill((0, 0, 0))
            fill.set_alpha(200)
            surface.blit(fill, (0, 0))

            for i in range(3):
                surface.blit(self.upgrade_images[self.upgrade_choices[i]], self.upgrade_rects[i])

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
        # Adds a scene at the top of the stack
        if not self.isEmpty():
            self.scenes[-1].onExit()
        self.scenes.append(scene)
        self.scenes[-1].onEnter()
    def pop(self):
        # Remove the scene on the top of the stack
        self.scenes[-1].onExit()
        self.scenes.pop()
        if not self.isEmpty():
            self.scenes[-1].onEnter()