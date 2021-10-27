import pygame, sys, pathlib, time
import engine
import helper
from world import World
from config import *

class timer():
    def __init__(self):
        self.times = []
        self.average = 0
        self.time_between = 0
        self.stop_time = 0
        self.start_time = 0
    def start(self):
        self.start_time = time.time()
    def stop(self):
        self.stop_time = time.time()
        self.time_between = self.stop_time - self.start_time
        self.times.append(self.time_between)
        self.average = sum(self.times) / len(self.times)
full_timer = timer()
update_timer = timer()
draw_timer = timer()

def Main():
    #######################################
    #  Initialize variables and funcions  #
    #######################################
    pygame.init()

    canvas = pygame.Surface((SCREEN_W, SCREEN_H))
    display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Platformer')

    player = helper.instantiate('player', SCREEN_W / 2, 400, False)
    player.gui = engine.GUI(player.camera)
    player.gui.add_sprite(helper.coin_images[0], (10, 10), (32, 32))
    coins_text = engine.Text(pygame.font.Font('assets/fonts/EquipmentPro.ttf', 50), '0', (245, 217, 76), (50, 2), 'topleft')
    player.gui.add_text(coins_text)
    player.gui.add_text(helper.combo_text)

    dummy = helper.make_dummy(SCREEN_W / 2, SCREEN_H / 2, False)

    camera_sys = engine.CameraSystem()

    wall_tileset = engine.load_spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\Walls.png', 32, 32)
    bg_tileset = engine.load_spritesheet(str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\background\\background.png', 32, 32)
    World(wall_tileset, bg_tileset, str(pathlib.Path(__file__).parent.resolve()) + '\\assets\\tilesets\\walls\\Map.json')

    engine.entities.append(dummy)
    engine.entities.append(player)

    ####################
    #  Main game loop  #
    ####################
    running = True
    while running:
        if DEBUG: full_timer.start()
        # Get time between each this frame and last frame, used for frame independance
        dt = engine.deltaTime()
        
        hit = False
        # Get Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.controller.attack()
                    hit = True
                if event.button == 4:
                    player.camera.zoom -= dt * 6
                    player.camera.zoom = max(player.camera.zoom, 0.5)
                if event.button == 5:
                    player.camera.zoom += dt * 6
                    player.camera.zoom = min(player.camera.zoom, 2)
        # Keyboard input
        active_keys = pygame.key.get_pressed()
        if active_keys[pygame.K_ESCAPE]:
            running = False
        if active_keys[pygame.K_SPACE]:
            player.controller.is_jumping = True
        player.controller.direction = STOP
        if hit == False:
            if active_keys[pygame.K_a] and not active_keys[pygame.K_d]:
                player.controller.direction = LEFT
            elif active_keys[pygame.K_d] and not active_keys[pygame.K_a]:
                player.controller.direction = RIGHT
        if active_keys[pygame.K_LSHIFT]:
            player.controller.is_dashing = True

        # Update entities
        if DEBUG: update_timer.start()
        engine.update(dt, player)
        if DEBUG: update_timer.stop()

        coins_text.set_text(str(player.score))

        # Draw entities
        canvas.fill((0, 0, 0))

        if DEBUG: draw_timer.start()
        camera_sys.update(canvas)
        if DEBUG: draw_timer.stop()
        
        display.blit(pygame.transform.scale(canvas, (SCREEN_W * 4, SCREEN_H * 4)), camera_sys.offset)
        pygame.display.flip()
        if DEBUG: full_timer.stop()
        if DEBUG: print(f"Draw is {round((draw_timer.average / full_timer.average) * 100, 2)}%, Update is {round((update_timer.average / full_timer.average) * 100, 2)}%")

if __name__ == "__main__":
    Main()