import pygame
import engine
import helper
from config import *

class Enemy():
    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.collider.pos.x = self.transform.pos.x + self.transform.size.x - self.collider.pos.x
        self.collider.pos.y = self.transform.pos.y + self.transform.size.y - self.collider.pos.y
        self.animations = _self.animations
        self.difference = pygame.math.Vector2((self.transform.size.x - self.collider.size.x) / 2, self.transform.size.y - self.collider.size.y)

        self.direction = RIGHT
        self.rect = self.collider.get_rect()
        self.vel = pygame.math.Vector2(0, 0)
        self.terminal_velocity = 1500
        self.is_grounded = False
        self.friction = 6.4
        
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
        self.dash_timer -= dt

        if self.direction == LEFT:
            self.vel.x -= self.acceleration * dt
        if self.direction == RIGHT:
            self.vel.x += self.acceleration * dt
        if self.is_dashing and self.dash_timer < 0:
            self.dash(self.direction)
        self.is_dashing = False
        # Slow the entity down if speed is over max speed
        if self.vel.x > self.max_speed or self.vel.x < -self.max_speed:
            self.vel.x *= 1 - dt * 5

        if (self.vel.x > 0 and self.direction == LEFT) or (self.vel.x < 0 and self.direction == RIGHT) or self.direction == STOP:
            if self.is_grounded:
                self.vel.x -= self.vel.x * self.friction * dt

    def horizontal_collision(self):
        self.collide_wall = False
        for entity in engine.entities:
            if entity.children != None:
                for child in entity.children:
                    if type(entity.children) == dict:
                        child = entity.children[child]
                    self._horizontal_collision(child)
            else:
                self._horizontal_collision(entity)
    def _horizontal_collision(self, entity):
        if entity.static_collision:
            collider = entity.transform.get_rect()
            if self.rect.bottom > collider.top and self.rect.top < collider.bottom:
                if self.rect.right >= collider.left and self.rect.left <= collider.right:
                    self.vel.x = 0
                    self.collide_wall = True

                    if self.collider.pos.x < collider.left:
                        self.transform.pos.x = collider.left - self.transform.size.x + self.difference.x
                    else:
                        self.transform.pos.x = collider.right - self.difference.x + 1


    def vertical_movement(self, dt):
        self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)


    def vertical_collision(self):
        self.is_grounded = False
        for entity in engine.entities:
            if entity.children != None:
                for child in entity.children:
                    if type(entity.children) == dict:
                        child = entity.children[child]
                    self._vertical_collision(child)
            else:
                self._vertical_collision(entity)
    def _vertical_collision(self, entity):
        if entity.static_collision:
            collider = entity.transform.get_rect()
            if self.rect.right > collider.left and self.rect.left < collider.right:
                if self.rect.bottom >= collider.top and self.rect.top <= collider.bottom:
                    self.vel.y = 0
                    if self.collider.pos.y < collider.top:
                        self.is_grounded = True

                        self.transform.pos.y = collider.top - self.transform.size.y
                    else:
                        self.transform.pos.y = collider.bottom - self.difference.y + 1
    
    def hit(self):
        if self.animations.state == 'hit':
            self.animations.animations_list['hit'].image_index = 0
        else:
            self.animations.next('hit')
            self.animations.force_skip()
        helper.spawn_coins(self.collider.pos.x + self.collider.size.x / 2, self.collider.pos.y + self.collider.size.y / 2, 1)