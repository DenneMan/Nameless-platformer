import engine
from config import *
from player import Player
from coin import Coin

player_images = engine.load_spritesheet('assets/sprites/character.png', 16, 16)
coin_images = engine.load_spritesheet('assets/sprites/coin.png', 8, 8)
dash_images = engine.load_spritesheet('assets/sprites/smoke_effects/Dash.png', 48, 32)
dust_landing_images = engine.load_spritesheet('assets/sprites/smoke_effects/Dust_landing.png', 32, 16)
tileset = engine.load_spritesheet('assets/tileset/tileset.png', 16, 16)

def instantiate(entity_name, x, y, mirror):
    if entity_name == 'dash':
        dash = engine.Entity()
        if mirror:
            dash.transform = engine.Transform(x, y - 128, 192, 128, mirror)
        else:
            dash.transform = engine.Transform(x - 192, y - 128, 192, 128, mirror)
        dash.animations = engine.Animations()
        dash.animations.add('idle', engine.Animation(dash_images[0:8], 10, False))
        return dash
    elif entity_name == 'player':
        player = engine.Entity()
        player.transform = engine.Transform(x, y, 64, 64, mirror)
        player.animations = engine.Animations()
        player.animations.add('idle', engine.Animation(player_images[0:3], 2))
        player.animations.add('running', engine.Animation(player_images[8:16], 8))
        player.animations.add('jump', engine.Animation(player_images[8:9], 1))
        player.animations.add('apex', engine.Animation(player_images[9:10], 1))
        player.animations.add('fall', engine.Animation(player_images[10:11], 1))
        player.animations.add('land', engine.Animation(player_images[3:8], 16))
        player.controller = Player(player.transform)
        player.camera = engine.Camera(0, 0, SCREEN_W, SCREEN_H)
        player.camera.set_world_pos(player.transform.pos.x, player.transform.pos.y)
        player.camera.track_entity(player)
        return player
    elif entity_name == 'coin':
        coin = engine.Entity()
        coin.transform = engine.Transform(x, y, 32, 32, mirror)
        coin.animations = engine.Animations()
        coin.animations.add('idle', engine.Animation(coin_images, 14))
        coin.controller = Coin(coin.transform)
        coin.type = 'collectable'
        return coin
    elif entity_name == 'dust_landing':
        dust_landing = engine.Entity()
        dust_landing.transform = engine.Transform(x - 64, y - 64, 128, 64, mirror)
        dust_landing.animations = engine.Animations()
        dust_landing.animations.add('idle', engine.Animation(dust_landing_images[0:8], 10, False))
        return dust_landing

def make_tile(x, y, index):
    tile = engine.Entity()
    tile.transform = engine.Transform(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, False)
    tile.sprite = engine.Sprite(tileset[index])
    tile.static_collision = True
    return tile

def load_level():

    for y, list in enumerate(level):
        for x, string in enumerate(list):
            if string != -1:
                tile = make_tile(x, y, string)
                engine.entities.append(tile)
