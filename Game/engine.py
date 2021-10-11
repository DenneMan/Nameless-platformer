import pygame
from settings import *
pygame.font.init()

################
#  Components  #
################

class Transform():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Animations():
    def __init__(self):
        self.animations_list = {}
    def add(self, state, animation):
        self.animations_list[state] = animation


# Class to handle animations
class Animation():

    def __init__(self, images, animations_per_second):
        self.images = images
        self.image_index = 0
        self.animation_timer = 0
        self.animations_per_second = animations_per_second
        self.has_looped = False


    def update(self, dt):
        # Increment animation_timer by the time between frames
        self.animation_timer += dt

        if self.animation_timer >= 1 / self.animations_per_second:
            self.image_index += 1
            self.animation_timer = 0
            self.has_looped = False
            if self.image_index >= len(self.images):
                # Reset frame when it reaches the end
                self.image_index = 0
                self.has_looped = True

    
    def get_looped(self):
        return self.has_looped


    def set_index(self, index):
        self.image_index = index

    
    def set_animations_per_second(self, animations_per_second):
        self.animations_per_second = animations_per_second


    def draw(self, surface, position, size, flip_x, flip_y):
        scaled_image = pygame.transform.scale(self.images[self.image_index], size)
        flipped_image = pygame.transform.flip(scaled_image, flip_x, flip_y)
        surface.blit(flipped_image, position)


###############
#  Functions  #
###############

# Loads images from spritesheet to a list of images
def load_spritesheet(filename, sprite_size):
    spritesheet = pygame.image.load(filename)
    spritesheet_rect = spritesheet.get_rect()
    sprites_x = int(spritesheet_rect.width / sprite_size)
    sprites_y = int(spritesheet_rect.height / sprite_size)

    sprites = []

    for y in range(sprites_y):
        for x in range(sprites_x):
            sprite = pygame.Surface((sprite_size, sprite_size))
            sprite.set_colorkey((0, 0, 0))
            sprite.blit(spritesheet, (-x * sprite_size, -y * sprite_size))
            sprites.append(sprite)
    
    return sprites


##################
#  Object types  #
##################

# Sophisticated text creator that has way more features than basic pygame text
class Text(pygame.sprite.Sprite):

    def __init__(self, font, text, color, position, anchor):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.color = color
        self.anchor = anchor
        self.position = position
        self.render()


    def render(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect(**{self.anchor: self.position})


    def clip(self, rect):
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect(**{self.anchor: self.position})


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def set_text(self, text):
        self.text = text
        self.render()


    def set_font(self, font):
        self.font = font
        self.render()


    def set_color(self, color):
        self.color = color
        self.render()


    def set_position(self, position, anchor=None):
        self.position = position
        if anchor:
            self.anchor = anchor

        self.rect = self.image.get_rect(**{self.anchor: self._position})

class Camera():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Entity():
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.transform = None
        self.animations = Animations()
        self.controller = None