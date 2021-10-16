import pygame
import engine
import helper
from config import *

class Dummy:
    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.collider.pos.x = self.transform.pos.x + self.transform.size.x - self.collider.pos.x
        self.collider.pos.y = self.transform.pos.y + self.transform.size.y - self.collider.pos.y
        self.animations = _self.animations

        
        self.rect = self.collider.get_rect()
        self.vel = pygame.math.Vector2(0, 0)
        self.terminal_velocity = 1500
        self.is_grounded = False
        self.friction = 6.4

        self.combo = 0
        
    def update(self, dt):
        self.animations.next('idle')

        self.collider.pos.x = self.transform.pos.x + self.transform.size.x / 2 - self.collider.size.x / 2
        self.collider.pos.y = (self.transform.pos.y + self.transform.size.y) - self.collider.size.y

        self.horizontal_movement(dt)
        self.rect.x = self.collider.pos.x + self.vel.x * dt
        self.horizontal_collision()
        self.rect.x = self.collider.pos.x
        self.vertical_movement(dt)
        self.rect.y = self.collider.pos.y + self.vel.y * dt
        self.vertical_collision()
        self.rect.y = self.collider.pos.y

        self.transform.pos += self.vel * dt


    def horizontal_movement(self, dt):
        ...

    def horizontal_collision(self):
        for entity in engine.entities:
            if entity.static_collision:
                collider = entity.transform.get_rect()
                if self.rect.bottom > collider.top and self.rect.top < collider.bottom:
                    if self.rect.right >= collider.left and self.rect.left <= collider.right:
                        self.vel.x = 0


    def vertical_movement(self, dt):
        self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)


    def vertical_collision(self):
        self.is_grounded = False
        for entity in engine.entities:
            if entity.static_collision:
                collider = entity.transform.get_rect()
                if self.rect.right > collider.left and self.rect.left < collider.right:
                    if self.rect.bottom >= collider.top and self.rect.top <= collider.bottom:
                        self.vel.y = 0
                        if self.transform.pos.y < collider.top:
                            self.is_grounded = True

                            # fix wierd bug caused by gravity being constant
                            self.transform.pos.y = collider.top - self.transform.size.y
    
    def hit(self):
        self.combo += 1
        if self.animations.state == 'hit':
            self.animations.animations_list['hit'].image_index = 0
        else:
            self.animations.next('hit')
            self.animations.force_skip()
        helper.combo_text.set_text(str(self.combo))
        helper.spawn_coins(self.collider.pos.x + self.collider.size.x / 2, self.collider.pos.y + self.collider.size.y / 2)