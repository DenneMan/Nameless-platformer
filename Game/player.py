import pygame
from settings import *

#################################################
#  Main player class, used for the player only  #
#################################################
class Player():

    def __init__(self, animations):
        self.state = 'idle'

        self.animations = animations

        self.rect = pygame.transform.scale(self.animations.animations_list['idle'].images[0], (64, 64)).get_rect()

        self.pos = pygame.math.Vector2(SCREEN_W / 2, SCREEN_H / 3)
        self.vel = pygame.math.Vector2(0, 0)

        self.acceleration = 1000
        self.friction = 6.4
        self.max_speed = 350
        self.terminal_velocity = 1500

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

    def update(self, dt, direction, colliders, center_text):
        self.direction = direction

        # TODO fix unstoppable_animation
        # First part of checking if last frame, player was in air and the next frame on ground, then playing a landing animation
        #if self.is_grounded:
        #    before_update_grounded = True
        #else:
        #    before_update_grounded = False

        self.horizontal_movement(dt, direction)
        self.rect.x = self.pos.x + self.vel.x * dt
        self.horizontal_collision(colliders)
        self.rect.x = self.pos.x
        self.vertical_movement(dt)
        self.rect.y = self.pos.y + self.vel.y * dt
        self.vertical_collision(colliders)
        self.rect.y = self.pos.y

        # Second part of last comment
        #if self.is_grounded and before_update_grounded == False:
        #    self.state = 'land'
        #    #self.animations.animations_list[self.state].set_index(0)
        #    print(self.animations.animations_list[self.state].image_index)
        #    self.unstoppable_animation = True

        self.pos += self.vel * dt

        self.handle_out_of_bounds()


    def horizontal_movement(self, dt, direction):
        self.dash_timer -= dt

        if direction == LEFT:
            self.vel.x -= self.acceleration * dt
        if direction == RIGHT:
            self.vel.x += self.acceleration * dt
        if self.is_dashing and self.dash_timer < 0:
            self.dash(direction)
        self.is_dashing = False
        # Slow the player down if speed is over max speed
        if self.vel.x > self.max_speed or self.vel.x < -self.max_speed:
            self.vel.x *= 1 - dt * 5

        if (self.vel.x > 0 and direction == LEFT) or (self.vel.x < 0 and direction == RIGHT) or direction == STOP:
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
                    if self.pos.y < collider.top:
                        self.is_grounded = True


    def handle_out_of_bounds(self):
        # Handle out of bounds on x axis
        if self.rect.left > SCREEN_W:
            self.pos.x = 0 + self.rect.width
        if self.rect.right < 0:
            self.pos.x = SCREEN_W
        # Handle out of bounds on y axis
        if self.rect.top > SCREEN_H:
            self.pos.y = 0 - self.rect.height
        
        if self.rect.bottom < 0:
            self.pos.y = SCREEN_H
    

    def draw(self, surface, dt):
        if self.direction == RIGHT:
            self.flip_image = False
        elif self.direction == LEFT:
            self.flip_image = True
        # Animation logic
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
        self.animation = self.animations.animations_list[self.state]
        self.animation.update(dt)
        self.animation.draw(surface, self.pos, (64, 64), self.flip_image, False)

    def state0(self):
        self.animation.set_start_index(0)
        self.animation.set_end_index(2)
        self.animation.set_animations_per_second(3)
    def state1(self):
        self.animation.set_start_index(8)
        self.animation.set_end_index(15)
        self.animation.set_animations_per_second(8)
    def state2(self):
        self.animation.set_start_index(9)
        self.animation.set_end_index(9)
        self.animation.set_animations_per_second(1)
    def state3(self):
        self.animation.set_start_index(8)
        self.animation.set_end_index(8)
        self.animation.set_animations_per_second(1)
    def state4(self):
        self.animation.set_start_index(10)
        self.animation.set_end_index(10)
        self.animation.set_animations_per_second(1)