import pygame
import engine, temporary
from config import *

class GUI():
    def __init__(self):
        self.enemies = []
        for e in engine.entities:
            if e.name == "player":
                self.player = e
            if e.name == "enemy":
                self.enemies.append(e)
        self.healthbar = engine.load_spritesheet('assets\\sprites\\Healthbar.png', 38, 9)
        temp = []
        for i in self.healthbar:
            temp.append(pygame.transform.scale(i, (38*4, 9*4)))
        self.healthbar = temp

        self.enemy_healthbar = engine.load_spritesheet('assets\\sprites\\EnemyHealthbar.png', 31, 5)
        temp = []
        for i in self.enemy_healthbar:
            temp.append(pygame.transform.scale(i, (31*4, 5*4)))
        self.enemy_healthbar = temp

        self.player_health_percent = 1
        self.coins = engine.Text(pygame.font.Font("assets\\fonts\\EquipmentPro.ttf", 50), '0', (218, 165, 32), (SCREEN_W - 20, 20), "topright")
    def update(self, dt):
        self.enemies = []
        for e in engine.entities:
            if e.name == "player":
                self.player = e
            if e.name == "enemy":
                if e.controller.health > 0:
                    self.enemies.append(e)
                    
        self.desired_health_percent = self.player.controller.health / self.player.controller.max_health

        self.player_health_percent -= (self.player_health_percent - self.desired_health_percent) / 20

    def draw(self, surface, offset):
        #player health
        x = (self.player.collider.l + self.player.collider.w/2) + offset.x
        y = (self.player.collider.t) + offset.y

        surface.blit(self.healthbar[0], (x - 76, y - 44))
        pygame.draw.rect(surface, (193, 42, 68), pygame.Rect(x - 64, y - 40, 132 * self.player_health_percent, 28))
        pygame.draw.rect(surface, (151, 18, 41), pygame.Rect(x - 64, y - 40 + 20, 132 * self.player_health_percent, 8))
        surface.blit(self.healthbar[1], (x + 132 * self.player_health_percent - 88, y - 44))
        surface.blit(self.healthbar[2], (x - 76, y - 44))

        #enemy health
        for e in self.enemies:
            x = (e.collider.l + e.collider.w/2) + offset.x
            y = (e.collider.t) + offset.y
            health_percent = e.controller.health / e.controller.max_health
                
            surface.blit(self.enemy_healthbar[0], (x - 76, y - 44))
            pygame.draw.rect(surface, (193, 42, 68), pygame.Rect(x - 68, y - 40, 29 * 4 * health_percent, 12))
            pygame.draw.rect(surface, (151, 18, 41), pygame.Rect(x - 68, y - 40 + 8, 29 * 4 * health_percent, 4))
            surface.blit(self.enemy_healthbar[1], (x - 76, y - 44))

        print(self.player.controller.sweep_timer)
        height = 250 * (self.player.controller.sweep_timer / self.player.controller.sweep_delay)
        pygame.draw.rect(surface, (90, 90, 90), pygame.Rect(SCREEN_W - 40, SCREEN_H - 260, 30, 250))
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(SCREEN_W - 40, SCREEN_H - height - 10, 30, height))

        self.coins.set_text(str(temporary.coins))
        self.coins.draw(surface)
        #dash bar