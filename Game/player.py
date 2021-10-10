import pygame
from settings import *

class Player():

    def __init__(self, animation):
        self.animation = animation

        self.rect = pygame.transform.scale(self.animation.images[0], (64, 64)).get_rect()

        self.pos = pygame.math.Vector2(SCREEN_W / 2, SCREEN_H / 3 - 50)
        self.vel = pygame.math.Vector2(0, 0)

        self.acceleration = 1000
        self.friction = 6.4
        self.max_speed = 350

        self.is_grounded = False
        self.is_jumping = False
        self.is_idle = False
        self.is_sprinting = False

        self.jump_force = 800

        self.health = 3

        self.flip_image = False


    def update(self, dt, direction, colliders, center_text):
        self.direction = direction

        self.horizontal_movement(dt, direction)
        self.vertical_movement(dt)
        self.rect.x = self.pos.x + self.vel.x * dt
        self.rect.y = self.pos.y + self.vel.y * dt
        self.horizontal_collision(colliders)
        self.vertical_collision(colliders)

        self.pos += self.vel * dt

        self.handle_damage(center_text)


    def horizontal_movement(self, dt, direction):
        if direction == LEFT:
            self.vel.x -= self.acceleration * dt
        if direction == RIGHT:
            self.vel.x += self.acceleration * dt
        self.vel.x = max(min(self.max_speed, self.vel.x), -self.max_speed)

        if direction == STOP and self.is_grounded:
            if self.vel.x != 0:
                self.vel.x -= self.vel.x * self.friction * dt


    def horizontal_collision(self, colliders):
        for collider in colliders:
            if self.rect.bottom > collider.top and self.rect.top < collider.bottom:
                if self.rect.right >= collider.left and self.rect.left <= collider.right:
                    self.vel.x = 0


    def vertical_movement(self, dt):
        if self.is_jumping and self.is_grounded:
            self.jump()
        self.is_jumping = False
        self.vel.y -= GRAVITY * dt


    def jump(self):
        self.vel.y = -self.jump_force


    def vertical_collision(self, colliders):
        self.is_grounded = False
        for collider in colliders:
            if self.rect.right > collider.left and self.rect.left < collider.right:
                if self.rect.bottom >= collider.top and self.rect.top <= collider.bottom:
                    self.vel.y = 0
                    self.is_grounded = True


    def handle_damage(self, center_text):
        # Handle out of bounds on x axis
        if self.rect.left > SCREEN_W or self.rect.right < 0:
            self.health = 0
        # Handle out of bounds on y axis
        if self.rect.top > SCREEN_H or self.rect.bottom < 0:
            self.health = 0
        
        if self.health <= 0:
            center_text.set_text('YOU DIED')
    

    def draw(self, surface, dt):
        if self.direction == RIGHT:
            self.flip_image = False
        elif self.direction == LEFT:
            self.flip_image = True
        self.animation.update(dt)
        self.animation.draw(surface, self.pos, (64, 64), self.flip_image)