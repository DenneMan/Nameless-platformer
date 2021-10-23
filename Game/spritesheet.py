import pygame
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename + '.png').convert_alpha()
        with open(filename + '.json', 'r') as f:
            self.data = json.load(f)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite_data = self.data['tile_data'][name]
        x, y, w, h = sprite_data['x'], sprite_data['y'], sprite_data['w'], sprite_data['h'],
        image = self.get_sprite(x, y, w, h)
        return image

    def parse_all(self):
        images = {}
        for tile in self.data['tile_data']:
            images[tile] = (
                self.parse_sprite(tile)
            )
        return images

