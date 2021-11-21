import engine, helper
from config import *

class Soul:
    def __init__(self, _self):
        self.transform = _self.transform
        self.collider = _self.collider
        self.transform.set_left(self.collider.l - ((self.transform.w - self.collider.w) / 2))
        self.transform.set_bottom(self.collider.b)

        self.animations = _self.animations
        self.animations.next('intro')

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

        if self.direction == 'right':
            self.transform.mirrored = False
        elif self.direction == 'left':
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
