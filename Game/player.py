import pygame
from settings import *

#################################################
#  Main player class, used for the player only  #
#################################################
class Player():

    def __init__(self, transform):
        self.transform = transform
        self.state = 'idle'

        self.rect = pygame.Rect(self.transform.pos.x, self.transform.pos.y, self.transform.size.x, self.transform.size.y)

        self.vel = pygame.math.Vector2(0, 0)

        self.acceleration = 1000
        self.friction = 6.4
        self.max_speed = 350
        self.terminal_velocity = 1500
        self.direction = STOP

        self.is_grounded = False
        self.is_jumping = False
        self.is_idle = False
        self.is_dashing = False

        self.dash_timer = 1.5 
        self.dash_delay = 1.5

        self.jump_force = 800
        self.dash_force = 1600

        self.health = 3

        self.flip_image = False

        self.unstoppable_animation = False

    def update(self, dt, colliders):

        # TODO fix unstoppable_animation
        # First part of checking if last frame, player was in air and the next frame on ground, then playing a landing animation
        #if self.is_grounded:
        #    before_update_grounded = True
        #else:
        #    before_update_grounded = False

        self.horizontal_movement(dt)
        self.rect.x = self.transform.pos.x + self.vel.x * dt
        self.horizontal_collision(colliders)
        self.rect.x = self.transform.pos.x
        self.vertical_movement(dt)
        self.rect.y = self.transform.pos.y + self.vel.y * dt
        self.vertical_collision(colliders)
        self.rect.y = self.transform.pos.y

        # Second part of last comment
        #if self.is_grounded and before_update_grounded == False:
        #    self.state = 'land'
        #    #self.animations.animations_list[self.state].set_index(0)
        #    print(self.animations.animations_list[self.state].image_index)
        #    self.unstoppable_animation = True

        self.transform.pos += self.vel * dt

        self.handle_out_of_bounds()


    def horizontal_movement(self, dt):
        self.dash_timer -= dt

        if self.direction == LEFT:
            self.vel.x -= self.acceleration * dt
        if self.direction == RIGHT:
            self.vel.x += self.acceleration * dt
        if self.is_dashing and self.dash_timer < 0:
            self.dash(self.direction)
        self.is_dashing = False
        # Slow the player down if speed is over max speed
        if self.vel.x > self.max_speed or self.vel.x < -self.max_speed:
            self.vel.x *= 1 - dt * 5

        if (self.vel.x > 0 and self.direction == LEFT) or (self.vel.x < 0 and self.direction == RIGHT) or self.direction == STOP:
            if self.is_grounded:
                self.vel.x -= self.vel.x * self.friction * dt

    def dash(self, direction):
        if direction == LEFT:
            self.vel.x = -self.dash_force
        if direction == RIGHT:
            self.vel.x = self.dash_force
        self.dash_timer = self.dash_delay

    def horizontal_collision(self, colliders):
        for collider in colliders:
            if self.rect.bottom > collider.top and self.rect.top < collider.bottom:
                if self.rect.right >= collider.left and self.rect.left <= collider.right:
                    self.vel.x = 0


    def vertical_movement(self, dt):
        if self.is_jumping and self.is_grounded:
            self.jump()
        self.is_jumping = False
        self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)


    def jump(self):
        self.vel.y = -self.jump_force


    def vertical_collision(self, colliders):
        self.is_grounded = False
        for collider in colliders:
            if self.rect.right > collider.left and self.rect.left < collider.right:
                if self.rect.bottom >= collider.top and self.rect.top <= collider.bottom:
                    self.vel.y = 0
                    if self.transform.pos.y < collider.top:
                        self.is_grounded = True


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

    def get_state(self):
        if self.is_grounded:
            if -50 < self.vel.x < 50:
                self.state = 'idle'
            else:
                self.state = 'running'
        else:
            if -200 < self.vel.y < 200:
                self.state = 'jump'
            elif self.vel.y < 0:
                self.state = 'apex'
            elif self.vel.y > 0:
                self.state = 'fall'
        return self.state
    
    def get_flipped(self):
        if self.direction == RIGHT:
            self.flip_image = False
        elif self.direction == LEFT:
            self.flip_image = True
        return self.flip_image