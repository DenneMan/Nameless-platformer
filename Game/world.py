import pygame
import engine
import json
from config import *

class World():
    def __init__(self, wall_tileset, bg_tileset, level):
        self.wall_tileset = wall_tileset
        self.bg_tileset = bg_tileset
        tiles = {}
        background_tiles = {}
        with open(level, 'r') as f:
            data = json.load(f)
            self.width = data['layers']['walls']['width']
            level = data['layers']['walls']['data']
            bg = data['layers']['background']['data']
            current_x = 0
            current_y = 0
            for wall_index in level:
                pos = (current_x, current_y)
                if wall_index - 5 >= 0:
                    tiles[str(pos)] = self.make_tile(current_x, current_y, wall_index - 5)

                current_x += 1
                if current_x >= self.width:
                    current_x = 0
                    current_y += 1
            current_x = 0
            current_y = 0
            for bg_index in bg:
                pos = (current_x, current_y)
                if bg_index - 53 >= 0:
                    background_tiles[str(pos)] = self.make_bg_tile(current_x, current_y, bg_index - 5 - 48)

                current_x += 1
                if current_x >= self.width:
                    current_x = 0
                    current_y += 1
        world = engine.Entity()
        world.name = 'world'
        world.children = tiles
        engine.entities.append(world)
        background = engine.Entity()
        background.name = 'background'
        background.children = background_tiles
        engine.entities.append(background)

    def make_tile(self, x, y, index):
        tile = engine.Entity()
        tile.transform = engine.Transform(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, False)
        tile.sprite = engine.Sprite(self.wall_tileset[index])
        tile.static_collision = True
        return tile

    def make_bg_tile(self, x, y, index):
        tile = engine.Entity()
        tile.transform = engine.Transform(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, False)
        tile.sprite = engine.Sprite(self.bg_tileset[index])
        return tile