import pygame
import engine
from player import Player
from dummy import Dummy
from coin import Coin
from soul import Soul
from enemy import Enemy
from config import *

combo_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '0', (245, 217, 76), (500, 2), 'topleft')

def spawn_dash(x, y, mirror):
    entity = engine.Entity()
    entity.name == 'dash'
    if mirror:
        entity.transform = engine.Transform(x, y - 128, 192, 128, mirror)
    else:
        entity.transform = engine.Transform(x - 192, y - 128, 192, 128, mirror)
    entity.animations = engine.Animations()
    dash_images = engine.load_spritesheet('assets/sprites/smoke_effects/Dash.png', 48, 32)
    entity.animations.add('idle', engine.Animation(dash_images[0:8], 10))
    entity.destruct = True
    entity.destruct_timer = 0.8
    return entity
def spawn_player(x, y, mirror):
    entity = engine.Entity()
    entity.name = 'player'
    entity.transform = engine.Transform(0, 0, 480, 320, mirror)
    entity.collider = engine.Transform(x, y, 95, 150, mirror)
    entity.animations = engine.Animations()
    run = engine.load_spritesheet('assets/sprites/MyCharacter/run.png', 120, 80)
    idle = engine.load_spritesheet('assets/sprites/MyCharacter/idle.png', 120, 80)
    jump = engine.load_spritesheet('assets/sprites/MyCharacter/jump.png', 120, 80)
    apex = engine.load_spritesheet('assets/sprites/MyCharacter/apex.png', 120, 80)
    fall = engine.load_spritesheet('assets/sprites/MyCharacter/fall.png', 120, 80)
    dash = engine.load_spritesheet('assets/sprites/MyCharacter/dash.png', 120, 80)
    attack = engine.load_spritesheet('assets/sprites/MyCharacter/attack.png', 120, 80)
    attack2 = engine.load_spritesheet('assets/sprites/MyCharacter/attack2.png', 120, 80)
    turn = engine.load_spritesheet('assets/sprites/MyCharacter/turn.png', 120, 80)
    wallslide = engine.load_spritesheet('assets/sprites/MyCharacter/wallslide.png', 120, 80)
    entity.animations.add('idle', engine.Animation(idle, 7))
    entity.animations.add('run', engine.Animation(run, 14))
    entity.animations.add('jump', engine.Animation(jump, 7))
    entity.animations.add('apex', engine.Animation(apex, 7))
    entity.animations.add('fall', engine.Animation(fall, 7))
    entity.animations.add('dash', engine.Animation(dash, 7))
    entity.animations.add('attack', engine.Animation(attack, 14))
    entity.animations.add('attack2', engine.Animation(attack2, 14))
    entity.animations.add('turn', engine.Animation(turn, 14))
    entity.animations.add('wallslide', engine.Animation(wallslide, 14))
    entity.controller = Player(entity)
    entity.camera = engine.Camera(0, 0, SCREEN_W, SCREEN_H)
    entity.camera.set_world_pos(x, y)
    entity.camera.track_entity(entity)
    return entity
def spawn_coin(x, y, mirror):
    entity = engine.Entity()
    entity.name = 'coin'
    entity.transform = engine.Transform(x, y, 32, 32, mirror)
    entity.collider = engine.Transform(x, y, 32, 32, mirror)
    entity.animations = engine.Animations()
    coin_images = engine.load_spritesheet('assets/sprites/coin.png', 8, 8)
    entity.animations.add('idle', engine.Animation(coin_images, 14))
    entity.controller = Coin(entity)
    entity.type = 'collectable'
    return entity
def spawn_dustlanding(x, y, mirror):
    entity = engine.Entity()
    entity.name = 'dust_landing'
    if mirror:
        entity.transform = engine.Transform(x - 48, y - 64, 128, 64, mirror)
    else:
        entity.transform = engine.Transform(x - 80, y - 64, 128, 64, mirror)
    entity.animations = engine.Animations()
    dust_landing_images = engine.load_spritesheet('assets/sprites/smoke_effects/Dust_landing.png', 32, 16)
    entity.animations.add('idle', engine.Animation(dust_landing_images[0:8], 10))
    entity.destruct = True
    entity.destruct_timer = 0.8
    return entity
def spawn_dummy(x, y, flip):
    entity = engine.Entity()
    entity.name = 'dummy'
    entity.transform = engine.Transform(x, y, 128, 128, flip)
    if flip:
        ...
    else:
        entity.collider = engine.Transform(x, y, 64, 128, flip)
    entity.animations = engine.Animations()
    Dummy_idle = engine.load_spritesheet('assets/sprites/Test_dummy/idle.png', 32, 32)
    Dummy_hit = engine.load_spritesheet('assets/sprites/Test_dummy/hit.png', 32, 32)
    entity.animations.add('idle', engine.Animation(Dummy_idle, 10))
    entity.animations.add('hit', engine.Animation(Dummy_hit, 10))
    entity.controller = Dummy(entity)
    entity.type = 'enemy'
    return entity

def spawn_coins(x, y, amount):
    for i in range(amount):
        engine.entities.append(spawn_coin(x - 16, y - 16, False))

def spawn_enemy(x, y):
        entity = engine.Entity()
        entity.name = 'enemy'
        entity.transform = engine.Transform(0, 0, 48*4, 43*4, False)
        entity.collider = engine.Transform(x, y, 16*4, 30*4, False)
        entity.animations = engine.Animations()
        tileset = engine.load_spritesheet('assets/sprites/skeletons/warrior.png', 48, 43)
        entity.animations.add('idle', engine.Animation(tileset[0:8], 8))
        entity.animations.add('attack', engine.Animation(tileset[13:26], 18))
        entity.animations.add('run', engine.Animation(tileset[26:32], 8))
        entity.animations.add('hit', engine.Animation(tileset[39:44], 8))
        entity.animations.add('die', engine.Animation(tileset[52:78], 12))
        entity.controller = Enemy(entity)
        return entity

def spawn_soul(x, y, flip):
    entity = engine.Entity()
    entity.name = 'projectile'
    entity.transform = engine.Transform(0, 0, 48*4, 43*4, False)

