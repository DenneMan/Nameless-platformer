import engine
from config import *
from player import Player
from dummy import Dummy
from coin import Coin
from creative import CreativePlayer
import pygame

combo_text = engine.GUIText(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '0', (245, 217, 76), (500, 2), 'topleft')

#Run = engine.load_spritesheet('assets/sprites/player/_Run.png', 120, 80)
#Idle = engine.load_spritesheet('assets/sprites/player/_Idle.png', 120, 80)
#Jump = engine.load_spritesheet('assets/sprites/player/_Jump.png', 120, 80)
#Apex = engine.load_spritesheet('assets/sprites/player/_JumpFallInbetween.png', 120, 80)
#Fall = engine.load_spritesheet('assets/sprites/player/_Fall.png', 120, 80)
#Dash = engine.load_spritesheet('assets/sprites/player/_Dash.png', 120, 80)
#Attack = engine.load_spritesheet('assets/sprites/player/_Attack.png', 120, 80)
#Attack2 = engine.load_spritesheet('assets/sprites/player/_Attack2.png', 120, 80)
#_Turn = engine.load_spritesheet('assets/sprites/player/_TurnAround.png', 120, 80)
#Wallslide = engine.load_spritesheet('assets/sprites/player/_WallSlide.png', 120, 80)
#
#Turn = []
#for frame in _Turn:
#    frame = pygame.transform.flip(frame, True, False)
#    Turn.append(frame)

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

Dummy_idle = engine.load_spritesheet('assets/sprites/Test_dummy/idle.png', 32, 32)
Dummy_hit = engine.load_spritesheet('assets/sprites/Test_dummy/hit.png', 32, 32)

coin_images = engine.load_spritesheet('assets/sprites/coin.png', 8, 8)
dash_images = engine.load_spritesheet('assets/sprites/smoke_effects/Dash.png', 48, 32)
dust_landing_images = engine.load_spritesheet('assets/sprites/smoke_effects/Dust_landing.png', 32, 16)
tileset = engine.load_spritesheet('assets/tilesets/tileset.png', 16, 16)

def instantiate(entity_name, x, y, mirror):
    if entity_name == 'dash':
        entity = engine.Entity()
        entity.name == 'dash'
        if mirror:
            entity.transform = engine.Transform(x, y - 128, 192, 128, mirror)
        else:
            entity.transform = engine.Transform(x - 192, y - 128, 192, 128, mirror)
        entity.animations = engine.Animations()
        entity.animations.add('idle', engine.Animation(dash_images[0:8], 10))
        entity.destruct = True
        entity.destruct_timer = 0.8
        return entity
    elif entity_name == 'player':
        entity = engine.Entity()
        entity.name = 'player'
        entity.transform = engine.Transform(x, y, 480, 320, mirror)
        entity.collider = engine.Transform(x, y, 95, 150, mirror)
        entity.animations = engine.Animations()
        entity.animations.add('idle', engine.Animation(idle, 7))
        entity.animations.add('run', engine.Animation(run, 12))
        entity.animations.add('jump', engine.Animation(jump, 7))
        entity.animations.add('apex', engine.Animation(apex, 7))
        entity.animations.add('fall', engine.Animation(fall, 7))
        entity.animations.add('dash', engine.Animation(dash, 7))
        entity.animations.add('attack', engine.Animation(attack, 14))
        entity.animations.add('attack2', engine.Animation(attack2, 14))
        entity.animations.add('turn', engine.Animation(turn, 14))
        entity.animations.add('wallslide', engine.Animation(wallslide, 14))
        entity.controller = Player(entity)
        entity.score = 0
        entity.camera = engine.Camera(0, 0, SCREEN_W, SCREEN_H)
        entity.camera.set_world_pos(entity.transform.pos.x, entity.transform.pos.y)
        entity.camera.track_entity(entity)
        return entity
    elif entity_name == 'coin':
        entity = engine.Entity()
        entity.name = 'coin'
        entity.transform = engine.Transform(x, y, 32, 32, mirror)
        entity.collider = engine.Transform(x, y, 32, 32, mirror)
        entity.animations = engine.Animations()
        entity.animations.add('idle', engine.Animation(coin_images, 14))
        entity.controller = Coin(entity)
        entity.type = 'collectable'
        return entity
    elif entity_name == 'dust_landing':
        entity = engine.Entity()
        entity.name = 'dust_landing'
        if mirror:
            entity.transform = engine.Transform(x - 48, y - 64, 128, 64, mirror)
        else:
            entity.transform = engine.Transform(x - 80, y - 64, 128, 64, mirror)
        entity.animations = engine.Animations()
        entity.animations.add('idle', engine.Animation(dust_landing_images[0:8], 10))
        entity.destruct = True
        entity.destruct_timer = 0.8
        return entity

def make_dummy(x, y, flip):
    entity = engine.Entity()
    entity.name = 'dummy'
    entity.transform = engine.Transform(x, y, 128, 128, flip)
    if flip:
        ...
    else:
        entity.collider = engine.Transform(x, y, 64, 128, flip)
    entity.animations = engine.Animations()
    entity.animations.add('idle', engine.Animation(Dummy_idle, 10))
    entity.animations.add('hit', engine.Animation(Dummy_hit, 10))
    entity.controller = Dummy(entity)
    entity.type = 'enemy'
    return entity

def spawn_coins(x, y, amount):
    for i in range(amount):
        engine.entities.append(instantiate('coin', x - 16, y - 16, False))

def make_moveable_empty(x, y):
    player = engine.Entity()
    player.transform = engine.Transform(x, y, 1, 1, False)
    player.controller = CreativePlayer(player)
    player.camera = engine.Camera(0, 0, SCREEN_W, SCREEN_H)
    player.camera.set_world_pos(player.transform.pos.x, player.transform.pos.y)
    player.camera.track_entity(player)
    return player
