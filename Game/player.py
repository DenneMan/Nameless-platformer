import pygame
import engine
import helper
from config import *

#################################################
#  Main player class, used for the player only  #
#################################################
class Player():

    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.collider.pos.x = self.transform.pos.x + self.transform.size.x - self.collider.pos.x
        self.collider.pos.y = self.transform.pos.y + self.transform.size.y - self.collider.pos.y
        self.animations = _self.animations
        self.animations.next('idle')

        self.rect = self.collider.get_rect()

        self.vel = pygame.math.Vector2(0, 0)

        self.acceleration = 1000
        self.friction = 6.4
        self.max_speed = 350
        self.terminal_velocity = 1500
        self.direction = STOP

        self.is_grounded = False
        self.is_jumping = False
        self.is_dashing = False
        self.is_attacking = False
        self.attack_index = 0

        self.dash_timer = 1.5 
        self.dash_delay = 1.5

        self.jump_force = 1000
        self.dash_force = 1600

        self.health = 3

        self.flip_image = False

        self.unstoppable_animation = False
        self.last_attack = None
        self.grounded_list = []

        self.collide_wall = False
        self.wallslide_right = False
        self.wallslide_left = False

    def update(self, dt):
        self.collider.pos.x = self.transform.pos.x + self.transform.size.x / 2 - self.collider.size.x / 2
        self.collider.pos.y = (self.transform.pos.y + self.transform.size.y) - self.collider.size.y

        if self.transform.mirrored == True:
            is_flipped_last_frame = True
        else:
            is_flipped_last_frame = False

        if self.direction == RIGHT:
            self.transform.mirrored = False
        elif self.direction == LEFT:
            self.transform.mirrored = True

        if self.transform.mirrored == True and is_flipped_last_frame == False:
            self.animations.next('turn')
            self.animations.force_skip()
        elif self.transform.mirrored == False and is_flipped_last_frame == True:
            self.animations.next('turn')
            self.animations.force_skip()

        if self.is_grounded:
            last_grounded = True
        else:
            last_grounded = False

        self.horizontal_movement(dt)
        self.rect.x = self.collider.pos.x + self.vel.x * dt
        self.horizontal_collision()
        self.rect.x = self.collider.pos.x
        self.vertical_movement(dt)
        self.rect.y = self.collider.pos.y + self.vel.y * dt
        self.vertical_collision()
        self.rect.y = self.collider.pos.y

        #if last_grounded == False and self.is_grounded == True:
        #    engine.entities.append(helper.instantiate('dust_landing', self.rect.center[0], self.rect.bottom, False))

        self.transform.pos += self.vel * dt

        #self.handle_out_of_bounds()
        self.set_state()


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
            engine.entities.append(helper.instantiate('dash', self.rect.left, self.rect.bottom, True))
            self.animations.next('dash')
            self.animations.force_skip()
            self.dash_timer = self.dash_delay
        if direction == RIGHT:
            self.vel.x = self.dash_force
            engine.entities.append(helper.instantiate('dash', self.rect.right, self.rect.bottom, False))
            self.animations.next('dash')
            self.animations.force_skip()
            self.dash_timer = self.dash_delay

    def horizontal_collision(self):
        self.collide_wall = False
        for entity in engine.entities:
            if entity.static_collision:
                collider = entity.transform.get_rect()
                if self.rect.bottom > collider.top and self.rect.top < collider.bottom:
                    if self.rect.right >= collider.left and self.rect.left <= collider.right:
                        self.vel.x = 0
                        self.collide_wall = True
                    '''
                    # Collide right
                    if self.rect.left <= collider.right:
                        self.vel.x = 0
                        self.collide_right = True
                    # Collide left
                    if self.rect.right >= collider.left:
                        self.vel.x = 0
                        self.collide_left = True
                    '''


    def vertical_movement(self, dt):
        if self.is_jumping and self.is_grounded:
            self.jump()
        self.is_jumping = False

        self.wallslide_right = False
        self.wallslide_left = False
        if self.collide_wall and self.is_grounded == False and self.direction == RIGHT:
            self.vel.y = GRAVITY / 10
            self.wallslide_right = True
        elif self.collide_wall and self.is_grounded == False and self.direction == LEFT:
            self.vel.y = GRAVITY / 10
            self.wallslide_left = True
        else:
            self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)


    def jump(self):
        self.vel.y = -self.jump_force


    def vertical_collision(self):
        self.is_grounded = False
        for entity in engine.entities:
            if entity.static_collision:
                collider = entity.transform.get_rect()
                if self.rect.right > collider.left and self.rect.left < collider.right:
                    if self.rect.bottom >= collider.top and self.rect.top <= collider.bottom:
                        self.vel.y = 0
                        if self.collider.pos.y < collider.top:
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

    def attack(self):
        self.is_attacking = True
        self.direction = STOP

    def attack_check(self, type):
        if type == 1:
            rect = self.transform.get_rect()
            if self.transform.mirrored:
                attack_rect = pygame.Rect(rect.x + 30, rect.y, rect.width / 4, rect.height)
            else:
                attack_rect = pygame.Rect(rect.x + rect.width - 30 - rect.width / 4, rect.y, rect.width / 4, rect.height)
        if type == 2:
            rect = self.transform.get_rect()
            if self.transform.mirrored:
                attack_rect = pygame.Rect(rect.x + 30, rect.y, rect.width / 4, rect.height)
            else:
                attack_rect = pygame.Rect(rect.x + rect.width - 30 - rect.width / 2, rect.y, rect.width / 2, rect.height)
        
        for entity in engine.entities:
            if entity.type == 'enemy':
                if attack_rect.colliderect(entity.collider.get_rect()):
                    entity.controller.hit()


    def set_state(self):
        # GROUNDED OR NOT
        if self.is_grounded:
            # ATTACK
            if self.is_attacking:
                # TODO - Logic for attacking, so that it switches to the second attack if first attack is executing but otherwise allways do first attack
                if self.animations.state != 'attack' and self.animations.state != 'attack2':
                    self.animations.next('attack')
                    self.animations.force_skip()
                    do_attack_one = True

                    if self.last_attack == 'attack':
                        self.animations.next('attack2')
                        self.animations.force_skip()
                        do_attack_one = False
                        self.attack_check(2)
                    if do_attack_one:
                        self.attack_check(1)

                    self.is_attacking = False
            self.last_attack = self.animations.state
            # IDLE OR RUN
            if -50 < self.vel.x < 50:
                self.animations.next('idle')
                if self.animations.state == 'run':
                    self.animations.force_skip()
            else:
                self.animations.next('run')
                if self.animations.state == 'idle':
                    self.animations.force_skip()
        else:
            
            if self.wallslide_right:
                self.transform.mirrored = True
                self.animations.next('wallslide')
                self.animations.force_skip()
            if self.wallslide_left:
                self.transform.mirrored = False
                self.animations.next('wallslide')
                self.animations.force_skip()
            # PARTS OF JUMP
            if -200 < self.vel.y < 200:
                self.animations.next('apex')
            elif self.vel.y < 0:
                self.animations.next('jump')
                if self.animations.state == 'run' or self.animations.state == 'idle':
                    self.animations.force_skip()
            elif self.vel.y > 0:
                self.animations.next('fall')