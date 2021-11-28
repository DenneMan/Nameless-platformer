import pygame, math, random, json, datetime
import engine, helper, level, temporary, universal, gui
from world import World_Inside, World_Outside
from config import *

left, right, jump, dash = None, None, None, None
def import_keys():
    global left, right, jump, dash
    with open('settings.json', 'r') as f:
        data = json.load(f)
        left = data["keybinds"]['left']
        right = data["keybinds"]['right']
        jump = data["keybinds"]['jump']
        dash = data["keybinds"]['dash']
import_keys()


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
        self.events = pygame.event.get()
        for event in self.events:
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
        # Keyboard
        active_keys = pygame.key.get_pressed()
        if active_keys[jump]:
            self.JUMP = True
        if active_keys[left]:
            self.LEFT = True
        if active_keys[right]:
            self.RIGHT = True
        if active_keys[dash]:
            self.DASH = True
        if active_keys[pygame.K_e]:
            self.ABILITY = True
    def update(self, sm, dt):
        pass
    def draw(self, sm, surface):
        pass

class MainMenu(Scene):
    def onEnter(self):
        temporary.reset_multipliers()
        universal.sound_manager.playMusic('stray_cat')
    def __init__(self):
        current_hour = int(str(datetime.datetime.now().time())[:2])
        if current_hour >= 20 or current_hour <= 5:
            cycle = 'Night'
        else:
            cycle = 'Day'
        directory = 'assets\\sprites\\Parallax Pixel Skies\\'
        self.background = [
            [pygame.transform.scale(pygame.image.load(directory + cycle + '\\back.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)],
            [pygame.transform.scale(pygame.image.load(directory + cycle + '\\mid.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)],
            [pygame.transform.scale(pygame.image.load(directory + cycle + '\\front.png').convert_alpha(), (SCREEN_W, SCREEN_H)), pygame.math.Vector2(0, 0)]]
        self.start_button = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 80), "Play", (255, 255, 255), (SCREEN_W/2, SCREEN_H/2), "center"), (100, 100, 100), (150, 150, 150))
        self.settings_button = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 80), "Settings", (255, 255, 255), (SCREEN_W/2, SCREEN_H/2 + 80), "center"), (100, 100, 100), (150, 150, 150))
    def input(self, sm):
        super().input(sm)
        if self.BACK:
            sm.pop()
            sm.push(Fade(self, None, 0.5))
        if self.M1:
            if self.start_button.collide(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                sm.push(Fade(self, Game(), 0.5))
            if self.settings_button.collide(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                sm.push(Fade(self, Settings(), 0.5))
        self.start_button.highlight(self.mouse_pos)
        self.settings_button.highlight(self.mouse_pos)
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
        self.settings_button.draw(surface)

class Settings(Scene):
    def __init__(self):
        self.images = engine.load_spritesheet('assets\\sprites\\Settings.png', 240, 135)
        temp = []
        for image in self.images:
            temp.append(pygame.transform.scale(image, (SCREEN_W, SCREEN_H)))
        self.images = temp
        self.state = 'controls'
        self.ps = int(SCREEN_W/240)
        self.back_button = pygame.Rect(2 * self.ps, 2 * self.ps, 14 * self.ps, 10 * self.ps)
        self.c_button = pygame.Rect(18 *self.ps, 2 *self.ps, 53 *self.ps, 10 * self.ps)
        self.gr_button = pygame.Rect(73 *self.ps, 2 *self.ps, 53 *self.ps, 10 * self.ps)
        self.a_button = pygame.Rect(128 *self.ps, 2 *self.ps, 53 *self.ps, 10 * self.ps)
        self.ga_button = pygame.Rect(183 *self.ps, 2 *self.ps, 54 *self.ps, 10 * self.ps)

        self.current_edit = None
        font_size = 8 * self.ps
        self.button_names = ['left', 'right', 'jump', 'dash']
        self.buttons = {}
        self.keys = {}
        for i, name in enumerate(self.button_names):
            self.buttons[name] = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), str.title(name), (255, 255, 255), (20*self.ps, (i + 5) * font_size), "topleft"), (100, 100, 100), (150, 150, 150))
            self.keys[name] = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), str(eval(name)), (150, 150, 150), (40*self.ps, (i + 5) * font_size), "topleft")

        self.highlight_image = pygame.image.load('assets\\sprites\\highlight.png').convert_alpha()
        self.highlight_image = pygame.transform.scale(self.highlight_image, (self.ps,self.ps))
        self.highlight_rects = [
            self.highlight_image.get_rect(),
            self.highlight_image.get_rect(),
            self.highlight_image.get_rect(),
            self.highlight_image.get_rect()
            ]
    
        self.master_volume_button = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), 'Master Volume', (255, 255, 255), (20*self.ps, 5 * font_size), "topleft"), (100, 100, 100), (150, 150, 150))
        self.master_volume_text = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), str(int(universal.sound_manager.master_volume * 100)), (150, 150, 150), (64*self.ps, 5 * font_size), "topleft")
        self.music_volume_button = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), 'Music Volume', (255, 255, 255), (20*self.ps, 6 * font_size), "topleft"), (100, 100, 100), (150, 150, 150))
        self.music_volume_text = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), str(int(universal.sound_manager.music_volume * 100)), (150, 150, 150), (64*self.ps, 6 * font_size), "topleft")
        self.sound_volume_button = engine.Button(engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), 'Sound Volume', (255, 255, 255), (20*self.ps, 7 * font_size), "topleft"), (100, 100, 100), (150, 150, 150))
        self.sound_volume_text = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", font_size), str(int(universal.sound_manager.sound_volume * 100)), (150, 150, 150), (64*self.ps, 7 * font_size), "topleft")
        self.text_buffer = ''
    def input(self, sm):
        super().input(sm)
        if self.BACK:
            sm.set(Fade(self, MainMenu(), 0.5))
        if self.M1:
            if self.back_button.collidepoint(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                sm.set(Fade(self, MainMenu(), 0.5))
            elif self.c_button.collidepoint(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                self.state = 'controls'
                self.place_highlight(pygame.Rect(-100, -100, 1, 1))
                self.current_edit = None
            elif self.gr_button.collidepoint(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                self.state = 'graphics'
                self.place_highlight(pygame.Rect(-100, -100, 1, 1))
                self.current_edit = None
            elif self.a_button.collidepoint(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                self.state = 'audio'
                self.place_highlight(pygame.Rect(-100, -100, 1, 1))
                self.current_edit = None
            elif self.ga_button.collidepoint(self.mouse_pos):
                universal.sound_manager.playSound('click_' + str(random.randint(1, 2)))
                self.state = 'gameplay'
                self.place_highlight(pygame.Rect(-100, -100, 1, 1))
                self.current_edit = None
            
            if self.state == 'controls':
                for name in self.button_names:
                    if self.buttons[name].collide(self.mouse_pos):
                        self.current_edit = name
            elif self.state == 'audio':
                if self.master_volume_button.collide(self.mouse_pos):
                    self.current_edit = 'master'
                    self.text_buffer = ''
                if self.music_volume_button.collide(self.mouse_pos):
                    self.current_edit = 'music'
                    self.text_buffer = ''
                if self.sound_volume_button.collide(self.mouse_pos):
                    self.current_edit = 'sound'
                    self.text_buffer = ''

        for name in self.button_names:
            self.buttons[name].highlight(self.mouse_pos)
        self.master_volume_button.highlight(self.mouse_pos)
        self.music_volume_button.highlight(self.mouse_pos)
        self.sound_volume_button.highlight(self.mouse_pos)
    def update(self, sm, dt):
        if self.state == 'controls':
            for name in self.button_names:
                if self.current_edit == None:
                    self.place_highlight(pygame.Rect(-100, -100, 1, 1))
                elif self.current_edit == name:
                    self.change_key(name)
                    self.place_highlight(self.keys[name].rect)
                self.keys[name].set_text(str.capitalize(pygame.key.name(eval(name))))
        elif self.state == 'graphics':
            ...
        elif self.state == 'audio':
            self.confirm = False
            if self.current_edit == None:
                self.place_highlight(pygame.Rect(-100, -100, 1, 1))
            elif self.current_edit == 'master':
                self.change_str(self.master_volume_text)
                self.place_highlight(self.master_volume_text.rect)
                if self.confirm:
                    self.confirm_str()
            elif self.current_edit == 'music':
                self.change_str(self.music_volume_text)
                self.place_highlight(self.music_volume_text.rect)
                if self.confirm:
                    self.confirm_str()
            elif self.current_edit == 'sound':
                self.change_str(self.sound_volume_text)
                self.place_highlight(self.sound_volume_text.rect)
                if self.confirm:
                    self.confirm_str()
        elif self.state == 'gameplay':
            ...
    def draw(self, sm, surface):
        if self.state == 'controls':
            surface.blit(self.images[0], (0, 0))
            for name in self.button_names:
                self.buttons[name].draw(surface)
                self.keys[name].draw(surface)
            for i, rect in enumerate(self.highlight_rects):
                surface.blit(pygame.transform.rotate(self.highlight_image, i*(-90)), rect)
        elif self.state == 'graphics':
            surface.blit(self.images[1], (0, 0))
        elif self.state == 'audio':
            surface.blit(self.images[2], (0, 0))
            self.master_volume_button.draw(surface)
            self.master_volume_text.draw(surface)
            self.music_volume_button.draw(surface)
            self.music_volume_text.draw(surface)
            self.sound_volume_button.draw(surface)
            self.sound_volume_text.draw(surface)
            for i, rect in enumerate(self.highlight_rects):
                surface.blit(pygame.transform.rotate(self.highlight_image, i*(-90)), rect)
        elif self.state == 'gameplay':
            surface.blit(self.images[3], (0, 0))


    def change_key(self, key):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key != 27:
                    settings = json.load(open('settings.json'))
                    settings['keybinds'][key] = event.key
                    json_settings = json.dumps(settings, indent=4)
                    with open('settings.json', 'w') as f:
                        f.write(json_settings)
                    import_keys()
                self.current_edit = None


    def change_str(self, text):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.confirm = True
                if event.key == pygame.K_BACKSPACE:
                    self.text_buffer = self.text_buffer[:-1]
                    text.set_text(str(self.text_buffer))
                if str.isdecimal(pygame.key.name(event.key)):
                    self.text_buffer += pygame.key.name(event.key)
                    text.set_text(str(self.text_buffer))


    def confirm_str(self):
        volume = int(self.text_buffer)
        self.volume = min(volume, 100)
        if self.current_edit == 'master':
            universal.sound_manager.setMasterVolume(volume / 100)
            self.master_volume_text.set_text(str(int(universal.sound_manager.master_volume * 100)))
        if self.current_edit == 'music':
            universal.sound_manager.setMusicVolume(volume / 100)
            self.music_volume_text.set_text(str(int(universal.sound_manager.music_volume * 100)))
        if self.current_edit == 'sound':
            universal.sound_manager.setSoundVolume(volume / 100)
            self.sound_volume_text.set_text(str(int(universal.sound_manager.sound_volume * 100)))

        settings = json.load(open('settings.json'))
        settings['volumes'][self.current_edit] = volume / 100
        json_settings = json.dumps(settings, indent=4)
        with open('settings.json', 'w') as f:
            f.write(json_settings)
        self.text_buffer = ''
        self.current_edit = None
        self.confirm = False


    def place_highlight(self, target):
        self.highlight_rects[0].topleft = (target.left - self.ps * 1.5, target.top)
        self.highlight_rects[1].topright = (target.right + self.ps, target.top)
        self.highlight_rects[2].bottomright = (target.right + self.ps, target.bottom - self.ps * 0.5)
        self.highlight_rects[3].bottomleft = (target.left - self.ps * 1.5, target.bottom - self.ps * 0.5)

class Game(Scene):
    def onEnter(self):
        universal.sound_manager.playMusic('rivaling_force')
    def __init__(self):
        temporary.enemy_health_mult *= 1.2

        self.spawn_locations = None
        self.level_manager = level.TempLevel()

        self.state = 'gaming'

        engine.entities = []
        #self.camera_sys = engine.CameraSystem((39, 39, 54))
        self.out_of_bounds = 25 * TILE_SIZE
        out_of_bounds_right = 45 * TILE_SIZE
        self.camera_sys = engine.CameraSystem((135, 206, 235), self.out_of_bounds, 0, out_of_bounds_right)
        self.playing, self.running = False, True

        #self.wall_tileset = engine.load_spritesheet('assets\\sprites\\tilesets\\Walls.png', 32, 32)
        #self.bg_tileset = engine.load_spritesheet('assets\\sprites\\tilesets\\background.png', 32, 32)
        #World_Inside(self.wall_tileset, self.bg_tileset, 'assets\\tilesets\\walls\\Map.json')

        i = str(random.randint(1, 3))
        self.tileset = engine.load_spritesheet('assets\\sprites\\tilesets\\Outside.png', 32, 32)
        World_Outside(self.tileset, 'assets\\tilesets\\walls\\Outside_' + i + '.json')

        self.JUMP, self.DASH, self.UP, self.DOWN, self.LEFT, self.RIGHT, self.BACK, self.M1, self.M2, self.M3, self.SCR_DOWN, self.SCR_UP = False, False, False, False, False, False, False, False, False, False, False, False

        #self.player = helper.instantiate('player', SCREEN_W * 2, 400, False)
        #engine.entities.append(self.player)
        #enemy = helper.spawn_enemy(SCREEN_W * 2, 400)
        #engine.entities.append(enemy)

        for pos in universal.spawn_locations:
            if universal.spawn_locations[pos] == 3:
                position = eval(pos)
                position = (position[0] + 1/2, position[1] + 1)
                self.player = helper.spawn_player(position[0] * TILE_SIZE, position[1] * TILE_SIZE, False)
                self.player.collider.set_bottom(position[1] * TILE_SIZE - 1)
                engine.entities.append(self.player)
        for pos in universal.spawn_locations:
            if universal.spawn_locations[pos] == 1:
                if random.randint(0,1):
                    position = eval(pos)
                    enemy = helper.spawn_enemy(position[0] * TILE_SIZE, position[1] * TILE_SIZE)
                    engine.entities.append(enemy)

        self.text = pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50)

        self.gui = gui.GUI()

        self.upgrade_images = engine.load_spritesheet('assets\\sprites\\Icons.png', 24, 24)
        temp = []
        for image in self.upgrade_images:
            temp.append(pygame.transform.scale(image, (256, 256)))
        self.upgrade_images = temp
        self.upgrade_choices = None
        self.upgrade_rects = [pygame.Rect(SCREEN_W / 4 * 1 - 128, SCREEN_H / 2 - 128, 256, 256), pygame.Rect(SCREEN_W / 4 * 2 - 128, SCREEN_H / 2 - 128, 256, 256), pygame.Rect(SCREEN_W / 4 * 3 - 128, SCREEN_H / 2 - 128, 256, 256)]
        self.clicked_upgrade = None
        self.active_upgrades = []

        self.death_text = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 200), 'YOU DIED', (102, 0, 0), (SCREEN_W/2,SCREEN_H/2), "center")
        self.death_opacity = 0

        self.text1 = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 50), '1', (200, 200, 200), (SCREEN_W / 4 * 1, (SCREEN_H / 3)*2), "center")
        self.text2 = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 50), '1', (200, 200, 200), (SCREEN_W / 4 * 2, (SCREEN_H / 3)*2), "center")
        self.text3 = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 50), '1', (200, 200, 200), (SCREEN_W / 4 * 3, (SCREEN_H / 3)*2), "center")
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
                        universal.sound_manager.playSound('click_' + str(random.randint(1,2)))
                        self.clicked_upgrade = i
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
            if self.death_opacity == 0:
                old_sound_volume = universal.sound_manager.sound_volume
                old_master_volume = universal.sound_manager.master_volume
                universal.sound_manager.sound_volume = 1
                universal.sound_manager.master_volume = 1
                universal.sound_manager.playSound('deathsound')
                universal.sound_manager.sound_volume = old_sound_volume
                universal.sound_manager.master_volume = old_master_volume
            self.state = 'death_screen'
        if temporary.soul_blast and self.ABILITY:
            helper.spawn_soul()
            #soul.Soul(self.player.collider.l + self.player.collider.w / 2, self.player.collider.t + self.player.collider.h / 2)
    def update(self, sm, dt):
        if self.state == 'gaming':
            a = 0
            for e in engine.entities:
                if e.name == 'enemy':
                    a += 1
            if a == 0:
                sm.pop()
                sm.push(Fade(self, Game(), 0.5))
            for entity in engine.entities:
                if entity.animations != None:
                    entity.animations.update(dt)

                if entity.type == 'collectable':
                    p_rect = pygame.Rect(self.player.collider.l, self.player.collider.t, self.player.collider.w, self.player.collider.h)
                    e_rect = pygame.Rect(entity.collider.l, entity.collider.t, entity.collider.w, entity.collider.h)
                    if p_rect.colliderect(e_rect):
                        universal.sound_manager.playSound('coin_pickup_' + str(random.randint(1, 3)))
                        temporary.coins += int(random.randint(40,60) * temporary.gold_mult)
                        engine.entities.remove(entity)

                if entity.destruct:
                    entity.destruct_timer -= dt
                    if entity.destruct_timer <= 0:
                        if entity.name == "enemy":
                            self.level_manager.give_exp(entity.controller.max_health)
                            helper.spawn_coins(entity.collider.l + entity.collider.w / 2, entity.collider.t + entity.collider.h / 2, int((entity.controller.max_health / 100)))
                            if temporary.lifesteal_mult != 0:
                                self.player.controller.health += entity.controller.max_health * temporary.lifesteal_mult
                        engine.entities.remove(entity)
                else:
                    if entity.name == "enemy":
                        if entity.collider.t > self.out_of_bounds:
                            self.level_manager.give_exp(entity.controller.max_health / 9)
                            engine.entities.remove(entity)


                if entity.controller != None:
                    entity.controller.update(dt)
            self.gui.update(dt)
        elif self.state == 'upgrading':
            if self.clicked_upgrade != None:
                self.state = 'gaming'
                self.active_upgrades.append(self.upgrade_choices[self.clicked_upgrade])

                allowed_upgrades = [6, 7, 10, 11, 20, 21, 22]


                if self.upgrade_choices[self.clicked_upgrade] == 6:
                    temporary.gold_mult += 0.5
                if self.upgrade_choices[self.clicked_upgrade] == 7:
                    temporary.legday_mult += 0.1
                if self.upgrade_choices[self.clicked_upgrade] == 10:
                    temporary.lifesteal_mult += 0.05
                if self.upgrade_choices[self.clicked_upgrade] == 11:
                    temporary.max_health_mult += 0.25
                if self.upgrade_choices[self.clicked_upgrade] == 20:
                    temporary.damage_mult += 0.2
                if self.upgrade_choices[self.clicked_upgrade] == 21:
                    temporary.knockback_mult += 0.2
                if self.upgrade_choices[self.clicked_upgrade] == 22:
                    temporary.resistance_mult += 0.2
                
                self.clicked_upgrade = None

                
            self.text1.set_text(str(self.level_manager.upgrade_names[self.upgrade_choices[0]]))
            self.text2.set_text(str(self.level_manager.upgrade_names[self.upgrade_choices[1]]))
            self.text3.set_text(str(self.level_manager.upgrade_names[self.upgrade_choices[2]]))
        elif self.state == 'death_screen':
            if self.death_opacity < 240:
                self.death_opacity += dt * 500
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
            self.text1.draw(surface)
            self.text2.draw(surface)
            self.text3.draw(surface)
        elif self.state == 'death_screen':
            fill = pygame.Surface((SCREEN_W, SCREEN_H))
            fill.fill((0, 0, 0))
            self.death_text.draw(fill)
            fill.set_alpha(self.death_opacity)
            surface.blit(fill, (0, 0))
            
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
    def set(self, scene):
        self.scenes = []
        self.scenes.append(scene)