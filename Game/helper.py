import engine
from config import *
from player import Player
from dummy import Dummy
from coin import Coin
import pygame

combo_text = engine.GUIText(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '0', (245, 217, 76), (500, 2), 'topleft')

Run = engine.load_spritesheet('assets/sprites/player/_Run.png', 120, 80)
Idle = engine.load_spritesheet('assets/sprites/player/_Idle.png', 120, 80)
Jump = engine.load_spritesheet('assets/sprites/player/_Jump.png', 120, 80)
Apex = engine.load_spritesheet('assets/sprites/player/_JumpFallInbetween.png', 120, 80)
Fall = engine.load_spritesheet('assets/sprites/player/_Fall.png', 120, 80)
Dash = engine.load_spritesheet('assets/sprites/player/_Dash.png', 120, 80)
Attack = engine.load_spritesheet('assets/sprites/player/_Attack.png', 120, 80)
Attack2 = engine.load_spritesheet('assets/sprites/player/_Attack2.png', 120, 80)
_Turn = engine.load_spritesheet('assets/sprites/player/_TurnAround.png', 120, 80)
Wallslide = engine.load_spritesheet('assets/sprites/player/_WallSlide.png', 120, 80)

Turn = []
for frame in _Turn:
    frame = pygame.transform.flip(frame, True, False)
    Turn.append(frame)

Dummy_idle = engine.load_spritesheet('assets/sprites/Test_dummy/idle.png', 32, 32)
Dummy_hit = engine.load_spritesheet('assets/sprites/Test_dummy/hit.png', 32, 32)

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
        player.transform = engine.Transform(x, y, 360, 240, mirror)
        player.collider = engine.Transform(x, y, 70, 126, mirror)
        player.animations = engine.Animations()
        player.animations.add('idle', engine.Animation(Idle, 7))
        player.animations.add('run', engine.Animation(Run, 12))
        player.animations.add('jump', engine.Animation(Jump, 7))
        player.animations.add('apex', engine.Animation(Apex, 7))
        player.animations.add('fall', engine.Animation(Fall, 7))
        player.animations.add('dash', engine.Animation(Dash, 7))
        player.animations.add('attack', engine.Animation(Attack, 14))
        player.animations.add('attack2', engine.Animation(Attack2, 14))
        player.animations.add('turn', engine.Animation(Turn, 14))
        player.animations.add('wallslide', engine.Animation(Wallslide, 14))
        player.controller = Player(player)
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

def make_dummy(x, y, flip):
    dummy = engine.Entity()
    dummy.transform = engine.Transform(x, y, 96, 96, flip)
    dummy.collider = engine.Transform(x, y, 96, 96, flip)
    dummy.animations = engine.Animations()
    dummy.animations.add('idle', engine.Animation(Dummy_idle, 10))
    dummy.animations.add('hit', engine.Animation(Dummy_hit, 10))
    dummy.controller = Dummy(dummy)
    dummy.type = 'enemy'
    return dummy
    

def load_level():
    for y, list in enumerate(level):
        for x, string in enumerate(list):
            if string != -1:
                tile = make_tile(x, y, string)
                engine.entities.append(tile)

def spawn_coins(x, y):
    for i in range(5):
        engine.entities.append(instantiate('coin', x - 16, y - 16, False))
