import pygame
import engine
import helper
from config import *

class Dummy():
    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.animations = _self.animations

        self.vel = pygame.math.Vector2(0, 0)
        self.terminal_velocity = 1500
        self.is_grounded = False
        self.friction = 6.4

        self.combo = 0
        
    def update(self, dt):
        self.animations.next('idle')

        self.horizontal_movement(dt)
        self.vertical_movement(dt)

        self.collider.set_top(self.collider.t + self.vel.y * dt)
        self.collider.set_left(self.collider.l + self.vel.x * dt)

        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.collision()


    def horizontal_movement(self, dt):
        ...

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