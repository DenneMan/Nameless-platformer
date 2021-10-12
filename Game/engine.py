import pygame, time
from settings import *
pygame.font.init()

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, surface, entities, colliders):
        for entity in entities:
            if self.check(entity):
                self._update(surface, entity, entities, colliders)
    def _update(self, surface, entity, entities, colliders):
        pass

class CameraSystem(System):
    def __init__(self):
        super().__init__()
    def check(self, entity):
        return entity.camera is not None
    def _update(self, surface, entity, entities, colliders):
        
        surface.set_clip(entity.camera.get_rect())
        surface.fill((28, 28, 28))

        if entity.camera.tracked_entity != None:
            entity.camera.world_x += ((entity.camera.tracked_entity.transform.pos.x + entity.camera.tracked_entity.transform.size.x / 2 - entity.camera.world_x) / 200) / entity.camera.zoom
            entity.camera.world_y += ((entity.camera.tracked_entity.transform.pos.y + entity.camera.tracked_entity.transform.size.y / 2 - entity.camera.world_y) / 200) / entity.camera.zoom

        offset = pygame.math.Vector2(entity.camera.pos.x + entity.camera.size.x/2 - (entity.camera.world_x / entity.camera.zoom), entity.camera.pos.y + entity.camera.size.y/2 - (entity.camera.world_y / entity.camera.zoom))

        # Draw platforms
        for collider in colliders:
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(collider.x / entity.camera.zoom + offset.x, collider.y / entity.camera.zoom + offset.y, collider.width / entity.camera.zoom, collider.height / entity.camera.zoom))
        # Draw entities
        for e in entities:
            if e.controller == None:
                e.animations.animations_list[e.state].draw(surface, e.transform.pos / entity.camera.zoom + offset, e.transform.size / entity.camera.zoom, False, False)
            else:
                e.state = e.controller.get_state()
                e.animations.animations_list[e.state].draw(surface, e.transform.pos / entity.camera.zoom + offset, e.transform.size / entity.camera.zoom, e.controller.get_flipped(), False)

        surface.set_clip(None)

################
#  Components  #
################

class Transform():
    def __init__(self, x, y, width, height):
        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)
    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

class Camera():
    def __init__(self, x, y, width, height):
        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)
        self.world_x = 0
        self.world_y = 0
        self.tracked_entity = None
        self.zoom = 1
    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
    def set_world_pos(self, x, y):
        self.world_x = x
        self.world_y = y
    def track_entity(self, entity):
        self.tracked_entity = entity
    #def lerp_entity(self, entity):

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


    def draw(self, surface, pos, size, flip_x, flip_y):
        scaled_image = pygame.transform.scale(self.images[self.image_index], (int(size.x), int(size.y)))
        flipped_image = pygame.transform.flip(scaled_image, flip_x, flip_y)
        surface.blit(flipped_image, (int(pos.x), int(pos.y)))


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

last_frame_time = time.time()
def deltaTime():
    global last_frame_time
    this_frame_time = time.time()
    delta_time = this_frame_time - last_frame_time
    last_frame_time = this_frame_time
    return delta_time

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

class Entity():
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.transform = None
        self.animations = Animations()
        self.controller = None
        self.camera = None