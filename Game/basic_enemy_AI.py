import pygame, random
import engine
import helper
from config import *
import math

class Enemy():
    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.animations = _self.animations
        self.animations.next('idle')

        self.vel = pygame.math.Vector2(0, 0)
        self.terminal_velocity = 1500
        self.is_grounded = False
        self.friction = 6.4
        self.direction = LEFT

        self.is_attacking = False

        self.combo = 0

        self.collide_right = False
        self.collide_left = False
        self.wallslide_right = False
        self.wallslide_left = False

        self.state_timer = 0

        self.attack_delay = 1
        self.attack_timer = 1

        self.target = engine.find_entity('player')
        self.world = engine.find_entity('world')
        
    def update(self, dt):

        self.AI(dt)

        self.horizontal_movement(dt)
        self.vertical_movement(dt)


        self.collider.set_top(self.collider.t + self.vel.y * dt)
        if self.animations.state != 'attack':
            self.collider.set_left(self.collider.l + self.vel.x * dt)

        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.collision()

        self.set_state()

    
    def AI(self, dt):
        # Find current grid position

        if (int((self.transform.l + self.transform.w/2)//128 -1), int((self.transform.t + self.transform.h/2)//128)) in self.world.children:
            print('AAAAAH')


        # Find fastest path to player
        # Move along path

        self.attack_timer -= dt


        if self.collide_right:
            self.direction = LEFT
        if self.collide_left:
            self.direction = RIGHT

        if self.target.collider.l > self.collider.l:
            self.direction = RIGHT
        elif self.target.collider.l < self.collider.l:
            self.direction = LEFT

        dist_from_player = math.sqrt(math.pow(self.target.collider.l - self.collider.l, 2) + math.pow(self.target.collider.t - self.collider.t, 2))
        if dist_from_player < 100:
            self.direction = STOP
            if self.attack_timer < 0:
                self.is_attacking = True
                self.attack_timer = self.attack_delay


    def horizontal_movement(self, dt):
        if self.direction == RIGHT:
            self.vel.x = 200
        if self.direction == LEFT:
            self.vel.x = -200
        if self.direction == STOP:
            self.vel.x = 0

    def vertical_movement(self, dt):
        self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)
    
    
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
    
    def hit(self):
        self.combo += 1
        if self.animations.state == 'hit':
            self.animations.animations_list['hit'].image_index = 0
        else:
            self.animations.next('hit')
            self.animations.force_skip()
        helper.combo_text.set_text(str(self.combo))
        helper.spawn_coins(self.collider.l + self.collider.w / 2, self.collider.t + self.collider.h / 2, 1)

    def set_state(self):
        # GROUNDED OR NOT
        if self.is_grounded:
            # ATTACK
            if self.is_attacking:
                if self.animations.state != 'attack':
                    self.animations.next('attack')
                    self.animations.force_skip()
                    self.is_attacking = False
            # IDLE OR RUN
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