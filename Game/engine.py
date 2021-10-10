import pygame
from settings import *
pygame.font.init()

#######################################################
#  Loads images from spritesheet to a list of images  #
#######################################################
def load_spritesheet(filename, sprite_size):
    spritesheet = pygame.image.load(filename)
    spritesheet_rect = spritesheet.get_rect()
    sprites_x = int(spritesheet_rect.width / sprite_size)
    sprites_y = int(spritesheet_rect.height / sprite_size)

    sprites = []

    for y in range(sprites_y):
        for x in range(sprites_x):
            sprite = pygame.Surface((sprite_size, sprite_size))
            sprite.blit(spritesheet, (-x * sprite_size, -y * sprite_size))
            sprites.append(sprite)
    
    return sprites

##################################################################################
#  Sophisticated text creator that has way more features than basic pygame text  #
##################################################################################
class Text(pygame.sprite.Sprite):

    def __init__(self, font, text, color, position, anchor, outline):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.color = color
        self.anchor = anchor
        self.position = position
        self.outline = outline
        self.render()


    def render(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect(**{self.anchor: self.position})


    def clip(self, rect):
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect(**{self.anchor: self.position})


    def draw(self, surface):
        if self.outline:
            mask = pygame.mask.from_surface(self.image)
            mask_surf = mask.to_surface()
            mask_surf.set_colorkey((0,0,0))
            surface.blit(mask_surf, (self.rect[0] - self.outline, self.rect[1]))
            surface.blit(mask_surf, (self.rect[0] + self.outline, self.rect[1]))
            surface.blit(mask_surf, (self.rect[0], self.rect[1] - self.outline))
            surface.blit(mask_surf, (self.rect[0], self.rect[1] + self.outline))
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

################################
#  Class to handle animations  #
################################
class Animation():

    def __init__(self, images, animations_per_second, start_index, end_index):
        self.images = images
        self.image_index = start_index
        self.animation_timer = 0
        self.animations_per_second = animations_per_second
        self.start_index = start_index
        self.end_index = end_index


    def update(self, dt):
        self.animation_timer += dt

        if self.animation_timer >= 1 / self.animations_per_second:
            self.image_index += 1
            self.animation_timer = 0
            if self.image_index > self.end_index:
                self.image_index = self.start_index


    def set_start_index(self, index):
        self.start_index = index
        self.image_index = self.start_index


    def set_end_index(self, index):
        self.end_index = index
        self.image_index = self.start_index


    def draw(self, surface, position, size, flip):
        surface.blit(pygame.transform.scale(pygame.transform.flip(self.images[self.image_index], flip, False), size), position)
