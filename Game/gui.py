import pygame
import engine

class GUI():
    def __init__(self):
        self.enemies = []
        for e in engine.entities:
            if e.name == "player":
                self.player = e
            if e.name == "enemy":
                self.enemies.append(e)
    def update(self, surface, offset):
        print(self.enemies)
        #player health
        player_health_percentage = self.player.controller.health / self.player.controller.max_health
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(30, 30, 160*player_health_percentage, 20))
        #enemy health
        for e in self.enemies:
            health_percentage = e.controller.health / e.controller.max_health
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect((e.collider.l + e.collider.w/2) + offset.x - 80, (e.collider.t) + offset.y, 160*health_percentage, 20))
        #dash bar
