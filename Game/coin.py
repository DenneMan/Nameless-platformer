import pygame, random
from config import *
import engine

class Coin():

    def __init__(self, transform):
        self.transform = transform
        self.rect = transform.get_rect()
        self.vel = pygame.math.Vector2(0, 0)
        self.vel.x = random.randrange(-100, 100)
        self.vel.y = -10
        self.terminal_velocity = 1500
        self.is_grounded = False
        self.friction = 6.4


    def update(self, dt):
        self.horizontal_movement(dt)
        self.rect.x = self.transform.pos.x + self.vel.x * dt
        self.horizontal_collision()
        self.rect.x = self.transform.pos.x
        self.vertical_movement(dt)
        self.rect.y = self.transform.pos.y + self.vel.y * dt
        self.vertical_collision()
        self.rect.y = self.transform.pos.y

        self.transform.pos += self.vel * dt

        self.handle_out_of_bounds()
        
    def horizontal_movement(self, dt):
        if self.is_grounded:
            self.vel.x -= self.vel.x * self.friction * dt

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


    def handle_out_of_bounds(self):
        # Handle out of bounds on x axis
        if self.rect.left > SCREEN_W:
            self.transform.pos.x = 0 + self.transform.size.x
        if self.rect.right < 0:
            self.transform.pos.x = SCREEN_W
        # Handle out of bounds on y axis
        if self.rect.top > SCREEN_H:
            self.transform.pos.y = 0 - self.transform.size.y
        
        if self.rect.bottom < 0:
            self.transform.pos.y = SCREEN_H