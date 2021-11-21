import pygame, time
from config import *
pygame.font.init()

entities = []

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, surface):
        for entity in entities:
            if self.check(entity):
                self._update(surface, entity)
    def _update(self, surface, entity):
        pass

class CameraSystem(System):
    def __init__(self, fill_color, out_of_bounds):
        super().__init__()
        self.fill_color = fill_color
        self.out_of_bounds = out_of_bounds
    def check(self, entity):
        return entity.camera is not None
    def _update(self, surface, entity):
        
        surface.set_clip(entity.camera.get_rect())

        if self.fill_color != None:
            surface.fill(self.fill_color)

        if entity.camera.tracked_entity != None:
            entity.camera.world_x += ((entity.camera.tracked_entity.transform.l + entity.camera.tracked_entity.transform.w / 2 - entity.camera.world_x) / LERP_SPEED[0]) / entity.camera.zoom
            entity.camera.world_y += ((entity.camera.tracked_entity.transform.t + entity.camera.tracked_entity.transform.h / 2 - entity.camera.world_y) / LERP_SPEED[1]) / entity.camera.zoom

        self.offset = pygame.math.Vector2(entity.camera.pos.x + entity.camera.size.x/2 - (entity.camera.world_x / entity.camera.zoom), entity.camera.pos.y + entity.camera.size.y/2 - (entity.camera.world_y / entity.camera.zoom))

        if self.out_of_bounds != None:
            if entity.camera.size.y - self.offset.y > self.out_of_bounds:
                self.offset.y = entity.camera.size.y - self.out_of_bounds

        # Draw entities
        for e in entities:
            self.draw_entity(e, surface, entity)
            if DEBUG:
                if e.collider != None:
                    collider = pygame.Rect(e.collider.l, e.collider.t, e.collider.w, e.collider.h)
                    pygame.draw.rect(surface, (255, 0, 0, 10), pygame.Rect(int(collider.x / entity.camera.zoom + self.offset.x), int(collider.y / entity.camera.zoom + self.offset.y), int(collider.width / entity.camera.zoom), int(collider.height / entity.camera.zoom)))

        surface.set_clip(None)
    
    def draw_entity(self, e, surface, entity):
        if e.transform != None:
            entity_pos = (e.transform.l / entity.camera.zoom + self.offset.x, e.transform.t / entity.camera.zoom + self.offset.y)
            entity_size = (e.transform.w / entity.camera.zoom, e.transform.h / entity.camera.zoom)
        if e.animations != None:
            if e.controller == None:
                e.animations.animations_list[e.state].draw(surface, entity_pos, entity_size, e.transform.mirrored, False)
            else:
                e.animations.draw(surface, entity_pos, entity_size, e.transform.mirrored, False)
        elif e.sprite != None:
            e.sprite.draw(surface, entity_pos, entity_size, e.transform.mirrored, False)
        if e.children != None:
            for child in e.children:
                if type(e.children) == dict:
                    child = e.children[child]
                self.draw_entity(child, surface, entity)

################
#  Components  #
################

class Transform():
    def __init__(self, x, y, w, h, mirrored):
        self.t = y
        self.b = y + h
        self.l = x
        self.r = x + w
        self.old_t = y
        self.old_b = y + h
        self.old_l = x
        self.old_r = x + w

        self.w = w
        self.h = h

        self.mirrored = mirrored
    def set_top(self, t):
        self.old_t = self.t
        self.old_b = self.b
        self.t = t
        self.b = t + self.h
    def set_bottom(self, b):
        self.old_b = self.b
        self.old_t = self.t
        self.b = b
        self.t = b - self.h
    def set_left(self, l):
        self.old_l = self.l
        self.old_r = self.r
        self.l = l
        self.r = l + self.w
    def set_right(self, r):
        self.old_r = self.r
        self.old_l = self.l
        self.r = r
        self.l = r - self.w

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

class Animations():
    def __init__(self):
        self.animations_list = {}
        self.state = 'idle'
        self.next_state = self.state
    def add(self, state, animation):
        self.animations_list[state] = animation
    def next(self, state):
        self.next_state = state
    def force_skip(self):
        self.state = self.next_state
    def draw(self, surface, pos, size, flip_x, flip_y):
        self.animations_list[self.state].draw(surface, pos, size, flip_x, flip_y)
    def update(self, dt):
        if self.animations_list[self.state].update(dt):
            self.state = self.next_state

class Animation():

    def __init__(self, images, fps):
        self.images = images
        self.image_index = 0
        self.animation_timer = 0
        self.fps = fps


    def update(self, dt):
        # Increment animation_timer by the time between frames
        self.animation_timer += dt

        if self.animation_timer >= 1 / self.fps:
            self.image_index += 1
            self.animation_timer = 0
            if self.image_index >= len(self.images):
                # Reset frame when it reaches the end
                self.image_index = 0
                return True


    def set_index(self, index):
        self.image_index = index

    
    def set_fps(self, fps):
        self.fps = fps


    def draw(self, surface, pos, size, flip_x, flip_y):
        scaled_image = pygame.transform.scale(self.images[self.image_index], (int(size[0]), int(size[1])))
        flipped_image = pygame.transform.flip(scaled_image, flip_x, flip_y)
        surface.blit(flipped_image, (int(pos[0]), int(pos[1])))

###############
#  Functions  #
###############

# Loads images from spritesheet to a list of images
def load_spritesheet(filename, sprite_width, sprite_height):
    spritesheet = pygame.image.load(filename).convert_alpha()
    spritesheet_rect = spritesheet.get_rect()
    sprites_x = int(spritesheet_rect.width / sprite_width)
    sprites_y = int(spritesheet_rect.height / sprite_height)

    sprites = []

    for y in range(sprites_y):
        for x in range(sprites_x):
            sprite = pygame.Surface((sprite_width, sprite_height))
            sprite.set_colorkey((0, 0, 0))
            sprite.blit(spritesheet, (-x * sprite_width, -y * sprite_height))
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

class Button():
    def __init__(self, text, defualt_color, highlight_color):
        self.text = text
        self.rect = self.text.rect
        self.default_color = defualt_color
        self.highlight_color = highlight_color
    def collide(self, point):
        return self.rect.collidepoint(point)
    def highlight(self, point):
        if self.collide(point):
            self.text.set_color(self.highlight_color)
        else:
            self.text.set_color(self.default_color)
    def draw(self, surface):
        self.text.draw(surface)

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

class GUI():
    def __init__(self, camera):
        self.camera = camera
        self.gui_sprites = []
        self.gui_texts = []
    def add_sprite(self, image, offset, size, anchor='topleft'):
        self.gui_sprites.append(GUISprite(image, offset, size, anchor))
    def add_text(self, text_element):
        self.gui_texts.append(text_element)
    def draw(self, surface):
        for gui_sprite in self.gui_sprites:
            gui_sprite.draw(surface, self.camera)
        for gui_text in self.gui_texts:
            gui_text.draw(surface)

class GUISprite():
    def __init__(self, image, offset, size, anchor):
        self.position = offset
        self.anchor = anchor
        self.image = image
        self.size = size
    def draw(self, surface, camera):
        if self.anchor == 'topleft':
            surface.blit(pygame.transform.scale(self.image, self.size), (
                self.position
            ))
        if self.anchor == 'topright':
            surface.blit(pygame.transform.scale(self.image, self.size), (
                self.position[0] + camera.size.width,
                self.position[1]
            ))
        if self.anchor == 'bottomleft':
            surface.blit(pygame.transform.scale(self.image, self.size), (
                self.position[0],
                self.position[1] + camera.size.height
            ))
        if self.anchor == 'bottomright':
            surface.blit(pygame.transform.scale(self.image, self.size), (
                self.position[0] + camera.size.width,
                self.position[1] + camera.size.height
            ))

class Sprite():
    def __init__(self, image):
        self.image = image
    def draw(self, surface, pos, size, flip_x, flip_y):
        scaled_image = pygame.transform.scale(self.image, (int(size[0]), int(size[1])))
        flipped_image = pygame.transform.flip(scaled_image, flip_x, flip_y)
        surface.blit(flipped_image, (int(pos[0]), int(pos[1])))

class Entity():
    def __init__(self):
        self.name = None

        self.state = 'idle'
        self.type = 'normal'
        self.transform = None
        self.collider = None
        # Entity has the option to have sprite/animation but not both
        self.animations = None
        self.sprite = None


        self.controller = None
        self.camera = None

        self.static_collision = False

        self.destruct = False
        self.destruct_timer = None
        self.children = None

def collide_rects(this, other):
    cu, cd, cl, cr = False, False, False, False

    if this.b < other.t or this.t > other.b or this.l > other.r or this.r < other.l: 
        pass
    elif this.t <= other.b and this.old_t > other.old_b:
        cu = True
    elif this.b >= other.t and this.old_b < other.old_t:
        cd = True
    elif this.l <= other.r and this.old_l > other.old_r:
        cl = True
    elif this.r >= other.l and this.old_r < other.old_l:
        cr = True

    return [cu, cd, cl, cr]

def find_entity(name):
    for e in entities:
        if e.name == name:
            return e

def ease_in_out(speed, time):
    a = speed
    x = time
    return (x ** a) / (x ** a + (1 - x) ** a)
