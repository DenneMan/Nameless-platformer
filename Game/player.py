import pygame
import engine, helper, universal
from config import *

class Player():

    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.animations = _self.animations
        self.animations.next('idle')

        self.vel = pygame.math.Vector2(0, 0)

        self.acceleration = 1000
        self.friction = 6.4
        self.max_speed = 400
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

        self.collide_right = False
        self.collide_left = False
        self.wallslide_right = False
        self.wallslide_left = False

        self.attack_delay = 0.5
        self.attack_timer = 0.5

        self.health = 1000
        self.max_health = 1000
        self.damage = 100

    def update(self, dt):
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_timer = self.attack_delay

        if self.transform.mirrored == True:
            is_flipped_last_frame = True
        else:
            is_flipped_last_frame = False

        if self.direction == RIGHT:
            self.transform.mirrored = False
        elif self.direction == LEFT:
            self.transform.mirrored = True

        if self.is_grounded:
            if self.transform.mirrored == True and is_flipped_last_frame == False:
                self.animations.next('turn')
                self.animations.force_skip()
            elif self.transform.mirrored == False and is_flipped_last_frame == True:
                self.animations.next('turn')
                self.animations.force_skip()


        self.horizontal_movement(dt)
        self.vertical_movement(dt)

        self.collider.set_top(self.collider.t + self.vel.y * dt)
        self.collider.set_left(self.collider.l + self.vel.x * dt)

        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        if self.is_grounded:
            last_grounded = True
        else:
            last_grounded = False
        self.collision()
        if last_grounded == False and self.is_grounded == True:
            engine.entities.append(helper.instantiate('dust_landing', self.collider.l + self.collider.w / 2, self.collider.b, self.transform.mirrored))

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
            engine.entities.append(helper.instantiate('dash', self.collider.l, self.collider.b, True))
            self.animations.next('dash')
            self.animations.force_skip()
            self.dash_timer = self.dash_delay
        if direction == RIGHT:
            self.vel.x = self.dash_force
            engine.entities.append(helper.instantiate('dash', self.collider.r, self.collider.r, False))
            self.animations.next('dash')
            self.animations.force_skip()
            self.dash_timer = self.dash_delay

    def vertical_movement(self, dt):
        if self.is_jumping:
            if self.is_grounded:
                self.jump()
            elif self.wallslide_right:
                self.wall_jump(LEFT)
            elif self.wallslide_left:
                self.wall_jump(RIGHT)
            self.is_jumping = False

        self.wallslide_right = False
        self.wallslide_left = False
        if self.collide_right and self.is_grounded == False and self.direction == RIGHT:
            self.vel.y = GRAVITY / 10
            self.wallslide_right = True
        elif self.collide_left and self.is_grounded == False and self.direction == LEFT:
            self.vel.y = GRAVITY / 10
            self.wallslide_left = True
        else:
            self.vel.y += GRAVITY * dt
        self.vel.y = max(min(self.terminal_velocity, self.vel.y), -self.terminal_velocity)


    def jump(self):
        self.vel.y = -self.jump_force

    def wall_jump(self, direction):
        self.vel.y = -self.jump_force
        if direction == RIGHT:
            self.vel.x = self.jump_force
        elif direction == LEFT:
            self.vel.x = -self.jump_force
        self.transform.mirrored = not self.transform.mirrored

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


    def attack(self):
        self.is_attacking = True
        self.direction = STOP

    def attack_check(self, type):
        rect = pygame.Rect(self.transform.l, self.transform.t, self.transform.w, self.transform.h)
        if self.transform.mirrored:
            if type == 1:
                attack_rect = pygame.Rect(rect.x + 10, rect.y + rect.height / 2, rect.width / 4, rect.height / 2)
            elif type == 2:
                attack_rect = pygame.Rect(rect.x + 10, rect.y + rect.height / 2, rect.width * 0.7, rect.height / 2)
        else:
            if type == 1:
                attack_rect = pygame.Rect(rect.x + rect.width - 10 - rect.width / 4, rect.y + rect.height / 2, rect.width / 4, rect.height / 2)
            elif type == 2:
                attack_rect = pygame.Rect(rect.x + rect.width - 10 - rect.width * 0.7, rect.y + rect.height / 2, rect.width * 0.7, rect.height / 2)

        if DEBUG:
            attack_entity = engine.Entity()
            attack_entity.collider = engine.Transform(attack_rect.x, attack_rect.y, attack_rect.width, attack_rect.height, False)
            attack_entity.destruct = True
            attack_entity.destruct_timer = 0.5
            engine.entities.append(attack_entity)

        for entity in engine.entities:
            if entity.name == 'enemy':
                c = pygame.Rect(entity.collider.l, entity.collider.t, entity.collider.w, entity.collider.h)
                if attack_rect.colliderect(c):
                    damage_mod = 1
                    for upgrade in universal.scene_manager.scenes[-1].active_upgrades:
                        if upgrade == 20:
                            damage_mod *= 1.2
                    entity.controller.hit(self.damage * damage_mod)
            elif entity.name == 'dummy':
                c = pygame.Rect(entity.collider.l, entity.collider.t, entity.collider.w, entity.collider.h)
                if attack_rect.colliderect(c):
                    entity.controller.hit()

    def hit(self, damage):
        self.health -= damage

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
                        universal.sound_manager.playSound('slash_2')
                        self.attack_check(2)
                    if do_attack_one:
                        universal.sound_manager.playSound('slash_1')
                        self.attack_check(1)

                    self.is_attacking = False
            self.last_attack = self.animations.state
            # IDLE OR RUN
            if -50 < self.vel.x < 50:
                self.animations.next('idle')
                if self.animations.state == 'run' or self.animations.state == 'fall' or self.animations.state == 'wallslide':
                    self.animations.force_skip()
            else:
                self.animations.next('run')
                self.animations.animations_list['run'].set_fps(abs(self.vel.x) / 35 + 4)
                if self.animations.state == 'idle' or self.animations.state == 'fall' or self.animations.state == 'wallslide':
                    self.animations.force_skip()
        else:
            if self.wallslide_right:
                self.transform.mirrored = True
                self.animations.next('wallslide')
                self.animations.force_skip()
            elif self.wallslide_left:
                self.transform.mirrored = False
                self.animations.next('wallslide')
                self.animations.force_skip()
            else:
            # PARTS OF JUMP
                if -200 < self.vel.y < 200:
                    self.animations.next('apex')
                    if self.animations.state == 'run' or self.animations.state == 'idle' or self.animations.state == 'wallslide' or self.animations.state == 'jump':
                        self.animations.force_skip()
                elif self.vel.y < 0:
                    self.animations.next('jump')
                    if self.animations.state == 'run' or self.animations.state == 'idle' or self.animations.state == 'wallslide':
                        self.animations.force_skip()
                elif self.vel.y > 0:
                    self.animations.next('fall')
                    if self.animations.state == 'run' or self.animations.state == 'idle' or self.animations.state == 'wallslide' or self.animations.state == 'jump':
                        self.animations.force_skip()
                if self.vel.x > 0:
                    self.transform.mirrored = False
                if self.vel.x < 0:
                    self.transform.mirrored = True
