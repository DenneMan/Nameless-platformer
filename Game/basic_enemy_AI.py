import pygame, random
import engine
import helper
from config import *
import math

class Enemy():
    def __init__(self, _self):
        self._self = _self
        self.transform = _self.transform
        self.collider = _self.collider
        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.animations = _self.animations
        self.animations.next('idle')

        self.vel = pygame.math.Vector2(0, 0)
        self.terminal_velocity = 1500
        self.friction = 6.4
        self.direction = LEFT

        self.is_attacking = False
        self.is_grounded = False
        self.is_jumping = False

        self.jump_force = 1000

        self.combo = 0

        self.collide_right = False
        self.collide_left = False
        self.wallslide_right = False
        self.wallslide_left = False

        self.state_timer = 0
        self.time_until_next_state = 3

        self.attack_delay = 0.8
        self.attack_timer = 0.8

        self.is_currently_attacking = False
        self.time_since_attack = 0


        self.target = engine.find_entity('player')
        self.world = engine.find_entity('world')

        self.health = 300
        self.max_health = 300

        self.damage = 100

        self.has_activated = False
        
    def update(self, dt):
        if self.health > 0:
            if self.is_currently_attacking == True:
                self.time_since_attack += dt
            if self.time_since_attack > 1:
                self.attack_check()
                self.is_currently_attacking = False
            if self.is_currently_attacking == False:
                self.time_since_attack = 0

            self.AI(dt)

            self.horizontal_movement(dt)
        else:
            self.vel.x = 0
        self.vertical_movement(dt)


        self.collider.set_top(self.collider.t + self.vel.y * dt)
        if self.animations.state != 'attack':
            self.collider.set_left(self.collider.l + self.vel.x * dt)

        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.collision()

        self.set_state()
        
        
        if self.health <= 0 and self.has_activated == False:
            self.animations.next("die")
            self.animations.force_skip()
            self._self.destruct = True
            self._self.destruct_timer = 2.6
            self.has_activated = True


    
    def AI(self, dt):
        dist_from_player = math.sqrt(math.pow(self.target.collider.l - self.collider.l, 2) + math.pow(self.target.collider.t - self.collider.t, 2))

        if dist_from_player < SCREEN_W/2:

            tile_x = int((self.transform.l + self.transform.w/2)/TILE_SIZE)
            tile_y = int((self.transform.t + self.transform.h/2)/TILE_SIZE)

            self.tile_pos = (tile_x, tile_y)

            if self.direction == RIGHT:
                if str((tile_x + 1, tile_y)) in self.world.children:
                    if str((tile_x + 1, tile_y - 1)) not in self.world.children:
                        self.is_jumping = True
                else:
                    if str((tile_x, tile_y + 1)) not in self.world.children:
                        if str((tile_x + 1, tile_y + 1)) not in self.world.children:
                            if str((tile_x, tile_y + 2)) not in self.world.children:
                                self.is_jumping = True
            elif self.direction == LEFT:
                if str((tile_x - 1, tile_y)) in self.world.children:
                    if str((tile_x - 1, tile_y - 1)) not in self.world.children:
                        self.is_jumping = True
                else:
                    if str((tile_x, tile_y + 1)) not in self.world.children:
                        if str((tile_x - 1, tile_y + 1)) not in self.world.children:
                            if str((tile_x, tile_y + 2)) not in self.world.children:
                                self.is_jumping = True

            dist_x = (self.collider.l + self.collider.w / 2) - (self.target.collider.l + self.target.collider.w / 2)

            if -100 < dist_x < 100:
                if self.target.collider.b < self.collider.t:
                    if not self.target.collider.b < self.collider.t - 256:
                        self.is_jumping = True

            self.attack_timer -= dt

            if self.target.collider.l > self.collider.l + 10:
                self.direction = RIGHT
            elif self.target.collider.l < self.collider.l - 10:
                self.direction = LEFT
            else:
                self.direction = STOP

            if dist_from_player < 100:
                self.direction = STOP
                if self.attack_timer < 0:
                    self.is_attacking = True
                    self.attack_timer = self.attack_delay
        else:
            self.state_timer += dt

            if self.state_timer > self.time_until_next_state:
                self.time_until_next_state = random.randrange(2, 6)
                if self.direction == STOP:
                    self.direction = random.randint(1, 2)
                if self.direction == RIGHT:
                    self.direction = random.randint(0, 1)
                if self.direction == LEFT:
                    self.direction = (random.randint(0, 1) - 1)%2

            if self.collide_right:
                self.direction = LEFT
            if self.collide_left:
                self.direction = RIGHT



    def horizontal_movement(self, dt):
        if self.direction == RIGHT:
            self.vel.x = 200
        if self.direction == LEFT:
            self.vel.x = -200
        if self.direction == STOP:
            self.vel.x = 0

    def vertical_movement(self, dt):
        if self.is_jumping:
            if self.is_grounded:
                self.jump()
            self.is_jumping = False
        self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)
    
    def jump(self):
        self.vel.y = -self.jump_force

    def collision(self):
        self.is_grounded = False
        self.collide_left = False
        self.collide_right = False
        for entity in engine.entities:
            if entity.children != None:
                for child in entity.children:
                    if type(entity.children) == dict:
                        child = entity.children[child]
                    self._collision(child)
            else:
                self._collision(entity)
    def _collision(self, entity):
        if entity.static_collision:
            rect = entity.transform
            if self.collider.b < rect.t or self.collider.t > rect.b or self.collider.l > rect.r or self.collider.r < rect.l: 
                return

            
            if self.collider.b >= rect.t and self.collider.old_b < rect.old_t:
                self.vel.y = 0
                self.collider.set_bottom(rect.t - C_THRESHOLD)
                self.is_grounded = True

            elif self.collider.t <= rect.b and self.collider.old_t > rect.old_b:
                self.vel.y = 0
                self.collider.set_top(rect.b + C_THRESHOLD)

            elif self.collider.r >= rect.l and self.collider.old_r < rect.old_l:
                self.vel.x = 0
                self.collider.set_right(rect.l - C_THRESHOLD)
                self.collide_right = True

            elif self.collider.l <= rect.r and self.collider.old_l > rect.old_r:
                self.vel.x = 0
                self.collider.set_left(rect.r + C_THRESHOLD)
                self.collide_left = True

    def attack_check(self):
        rect = pygame.Rect(self.transform.l, self.transform.t, self.transform.w, self.transform.h)

        if self.transform.mirrored:
            attack_rect = pygame.Rect(rect.x + 10, rect.y + rect.height / 2, rect.width * 0.7, rect.height / 2)
        else:
            attack_rect = pygame.Rect(rect.x + rect.width - 10 - rect.width * 0.7, rect.y + rect.height / 2, rect.width * 0.7, rect.height / 2)

        if DEBUG:
            attack_entity = engine.Entity()
            attack_entity.collider = engine.Transform(attack_rect.x, attack_rect.y, attack_rect.width, attack_rect.height, False)
            attack_entity.destruct = True
            attack_entity.destruct_timer = 0.5
            engine.entities.append(attack_entity)

        for entity in engine.entities:
            if entity.name == 'player':
                c = pygame.Rect(entity.collider.l, entity.collider.t, entity.collider.w, entity.collider.h)
                if attack_rect.colliderect(c):
                    entity.controller.hit(self.damage)
    
    def hit(self, damage):
        if self.health > 0:
            self.combo += 1
            self.is_currently_attacking = False
            if self.animations.state == 'hit':
                self.animations.animations_list['hit'].image_index = 0
            else:
                self.animations.next('hit')
                self.animations.force_skip()
            helper.combo_text.set_text(str(self.combo))
            helper.spawn_coins(self.collider.l + self.collider.w / 2, self.collider.t + self.collider.h / 2, 1)
            self.health -= damage

    def set_state(self):
        if self.health > 0:
            if self.is_grounded:
                if self.is_attacking:
                    if self.animations.state != 'attack':
                        self.animations.next('attack')
                        self.animations.force_skip()
                        self.is_attacking = False
                        self.is_currently_attacking = True
                if self.direction == RIGHT:
                    self.transform.mirrored = False
                    self.animations.next('run')
                    if self.animations.state == 'idle':
                        self.animations.force_skip()
                elif self.direction == LEFT:
                    self.transform.mirrored = True
                    self.animations.next('run')
                    if self.animations.state == 'idle':
                        self.animations.force_skip()
                elif self.direction == STOP:
                    self.animations.next('idle')
                    if self.animations.state == 'run':
                        self.animations.force_skip()
            else:
                self.animations.next('idle')
                if self.animations.state != 'idle':
                    self.animations.force_skip()